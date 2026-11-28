import re
import shutil
import sys
sys.path.insert(0, 'scripts')
from _palette_shift import shift_html_palette

SLUG = "quality-handyman-services-and-installations"
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
# 1. Paleta: rosa Lash Bloom -> ocre/ambar tostado (hue shift +63deg, preserva
#    saturacion/luminosidad exactas; protege merktop-badge automaticamente)
# ---------------------------------------------------------------------------
h, palette_map = shift_html_palette(h, hue_delta_deg=63)
print("PALETTE done,", len(palette_map), "tonos")

PHONE = "+18137840747"
TEL = f"tel:{PHONE}"
MAPS_URL = "https://www.google.com/maps/place/Quality+Handyman+Services+and+Installations/data=!4m7!3m6!1s0x88c2cdd401aa72bb:0x665badbf9485acce!8m2!3d27.9799763!4d-82.2920433!16s%2Fg%2F11z6srvl_r!19sChIJu3KqAdTNwogRzqyFlL-tW2Y?authuser=0&hl=en&g_ep=EgoyMDI2MTEyMy4wIJJjKgBIAVAD&rclk=1"

# ---------------------------------------------------------------------------
# 2. Globales: sin Booksy/IG -> tel: ; sin logo foto -> quitamos el <img> del
#    monograma y dejamos solo el texto "QH" (no inventamos logo)
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
c = h.count(OLD_BOOK)
assert c == 13, c
h = h.replace(OLD_BOOK, TEL)
print("BOOK->TEL done", c)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
c = h.count(OLD_IG_URL)
assert c == 6, c
h = h.replace(OLD_IG_URL, MAPS_URL)
print("IG URL -> Maps URL done", c)

OLD_IG_HANDLE = "@_lashbloom"
c = h.count(OLD_IG_HANDLE)
assert c == 4, c
h = h.replace(OLD_IG_HANDLE, "Google Maps")
print("IG HANDLE done", c)

# Fix: "Read all 86 reviews on Booksy" quedo apuntando a tel: por el replace
# global de arriba; debe ir al listado real de Google.
rep(f'href="{TEL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    f'href="{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 10 reseñas en Google" data-en="Read all 10 reviews on Google">Read all 10 reviews on Google</a>')
print("REVIEWS LINK fixed")

# Icono IG (outline) -> icono de telefono en los lugares donde quedo el icono de
# camara de instagram apuntando ahora a tel:/maps (nav hero secundario + galeria link)
OLD_IG_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>'
NEW_MAP_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.9 10.1 12 2.1l-8.9 8a1 1 0 0 0 0 1.4l8.9 8 8.9-8a1 1 0 0 0 0-1.4Z"/><path d="M12 21.9V12"/></svg>'
rep_all(OLD_IG_ICON, NEW_MAP_ICON, expect=2)
print("ICON done")

# Logo: no hay foto de logo real (el listado de Google no publica una). Quitamos
# el <img> del monograma (nav + footer) y dejamos solo texto, sin inventar imagen.
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,124,74,0.35)]" />',
    '<span class="w-10 h-10 rounded-full ring-1 ring-[rgba(160,124,74,0.35)] bg-[color:var(--accent-soft)] flex items-center justify-center font-display text-sm text-[color:var(--accent-deep)]">QH</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,217,190,0.35)]" loading="lazy" />',
    '<span class="w-9 h-9 rounded-full ring-1 ring-[rgba(240,217,190,0.35)] bg-white/10 flex items-center justify-center font-display text-sm">QH</span>')
rep('''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,124,74,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>
          </div>''',
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <span class="w-10 h-10 rounded-full ring-1 ring-[rgba(160,124,74,0.3)] bg-[color:var(--accent-soft)] flex items-center justify-center font-display text-sm text-[color:var(--accent-deep)]">QH</span>
            <span class="text-sm font-light">Ryan · <span class="text-[color:var(--ink-40)]" data-es="Instalaciones y reparaciones" data-en="Installations &amp; repairs">Installations &amp; repairs</span></span>
          </div>''')
print("LOGO done")

# ---------------------------------------------------------------------------
# 3. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Quality Handyman Services and Installations · Brandon &amp; Seffner, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Quality Handyman Services and Installations, Brandon &amp; Seffner FL: flooring installation, bathroom remodeling, general repairs and installations. 5.0 stars across 10 Google reviews. Call for a free estimate." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Quality Handyman Services and Installations · Brandon &amp; Seffner, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Flooring, bathroom remodeling, repairs and installations. 5.0 on Google with 10 reviews. Call for a free estimate." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-8.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/gmaps-8.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Quality Handyman Services and Installations",
    "description": "Handyman company serving Seffner, Brandon and the Tampa Bay area, FL: flooring installation, bathroom remodeling, general repairs and installations.",
    "areaServed": [{ "@type": "City", "name": "Seffner" }, { "@type": "City", "name": "Brandon" }, { "@type": "City", "name": "Tampa" }],
    "telephone": "+1-813-784-0747",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "10", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Handyman services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Flooring Installation" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bathroom Remodeling" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "General Repairs" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Custom Installations" } }
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
# 5. PRELOADER + NAV
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">QH</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Quality Handyman</span>')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Quality <span class="text-[color:var(--accent-deep)]">Handyman</span></span>')

rep('<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '', n=1)
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '', n=1)

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Call now</span>', n=1)
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>')
print("NAV done")

# ---------------------------------------------------------------------------
# 6. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Seffner &amp; Brandon, FL · Handyman" data-en="Seffner &amp; Brandon, FL · Handyman">Seffner &amp; Brandon, FL · Handyman</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Reparaciones e instalaciones, hechas bien." data-en="Repairs and installations, done right.">Repairs and installations, done right.</p>',
    n=2)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Pisos, baños e instalaciones" data-en="Flooring, bathrooms and installs">Flooring, bathrooms and installs</span><br /><span data-es="hechos con el mismo cuidado " data-en="handled with the same care ">handled with the same care </span><span class="text-shine" data-es="cada vez" data-en="every time">every time</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Ryan y su equipo instalan pisos nuevos, remodelan baños y resuelven las reparaciones e instalaciones generales de la casa, con el mismo cuidado y limpieza al terminar cada trabajo. Calificacion perfecta de 5.0 en Google." data-en="Ryan and his team install new flooring, remodel bathrooms and handle the general repairs and installations a home needs, cleaning up after every job. A perfect 5.0 rating on Google.">Ryan and his team install new flooring, remodel bathrooms and handle the general repairs and installations a home needs, cleaning up after every job. A perfect 5.0 rating on Google.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 10 reseñas en Google" data-en="5.0 · 10 reviews on Google">5.0 · 10 reviews on Google</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Llamar al (813) 784-0747" data-en="Call (813) 784-0747">Call (813) 784-0747</span>', n=1)
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-8.jpg" alt="Cocina remodelada por Quality Handyman Services en Brandon" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Llama hoy" data-en="Call today">Call today</p>
            <p class="font-display text-lg">Free Estimate</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Seffner · Brandon · Tampa" data-en="Seffner · Brandon · Tampa">Seffner · Brandon · Tampa</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 7. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="10">10</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Floors <span class="text-shine">&amp;</span> Baths</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Instalaciones · Remodelacion" data-en="Installs · Remodeling">Installs · Remodeling</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl"><span data-es="Abierto" data-en="Open">Open</span> <span class="text-shine">7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Los 7 dias, 7:30am a 7pm" data-en="7 days a week, 7:30am-7pm">7 days a week, 7:30am-7pm</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Brandon, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">&amp; Tampa Bay area</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 8. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Flooring Installation"),
    ("Hybrid Set", "Bathroom Remodeling"),
    ("Volume Set", "General Repairs"),
    ("Mega Volume", "Custom Installations"),
    ("Bottom Lashes", "Free Estimates"),
    ("West Palm Beach, FL", "Brandon, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 9. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-1.jpg" alt="Remodelacion de bano en progreso por Quality Handyman, Brandon FL" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-3.jpg" alt="Bano terminado con ducha de marmol por Quality Handyman" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un equipo," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="todos los trabajos cubiertos" data-en="every job covered">every job covered</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Quality Handyman Services and Installations, liderado por Ryan, atiende Seffner, Brandon y el area de Tampa Bay: instalacion de pisos, remodelacion de baños y las reparaciones e instalaciones generales que una casa necesita, todo con el mismo equipo de un extremo al otro del proyecto." data-en="Quality Handyman Services and Installations, led by Ryan, serves Seffner, Brandon and the greater Tampa Bay area: flooring installation, bathroom remodeling and the general repairs and installations a home needs, handled by one crew from start to finish.">Quality Handyman Services and Installations, led by Ryan, serves Seffner, Brandon and the greater Tampa Bay area: flooring installation, bathroom remodeling and the general repairs and installations a home needs, handled by one crew from start to finish.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: una calificacion perfecta de 5.0 en 10 reseñas de Google, con clientes que destacan la calidad del trabajo, la limpieza al terminar y la rapidez para responder, visita tras visita." data-en="The result: a perfect 5.0 rating across 10 Google reviews, with clients specifically praising the quality of the work, the cleanup after each job and how quickly the team responds, visit after visit.">The result: a perfect 5.0 rating across 10 Google reviews, with clients specifically praising the quality of the work, the cleanup after each job and how quickly the team responds, visit after visit.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="10">10</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Ryan · <span class="text-[color:var(--ink-40)]" data-es="Fundador" data-en="Owner">Owner</span></span>', n=0) if False else None
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 10. EL METODO -> "Como trabajamos" (4 pasos adaptados, sin booking online)
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Como trabajamos" data-en="How we work">How we work</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="De la llamada" data-en="From the call">From the call</span> <span class="text-shine" data-es="al trabajo terminado" data-en="to the finished job">to the finished job</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Llamas o escribes" data-en="You call or text">You call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cuentas que necesitas y Ryan responde rapido para agendar una visita." data-en="Tell us what you need and Ryan responds quickly to schedule a visit.">Tell us what you need and Ryan responds quickly to schedule a visit.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Revisamos el trabajo en sitio y te damos un presupuesto claro, sin compromiso." data-en="We look at the job on site and give you a clear, no obligation estimate.">We look at the job on site and give you a clear, no obligation estimate.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="El trabajo" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Instalacion, remodelacion o reparacion, hecha con cuidado y limpiando al terminar." data-en="Installation, remodeling or repair, done with care and cleaned up when finished.">Installation, remodeling or repair, done with care and cleaned up when finished.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Garantia de satisfaccion" data-en="Satisfaction guaranteed">Satisfaction guaranteed</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Revisamos el resultado contigo antes de dar el trabajo por terminado." data-en="We walk through the result with you before calling the job done.">We walk through the result with you before calling the job done.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 11. SERVICIOS: reemplazo completo del grid (sin precios, "Cotizacion gratis")
# ---------------------------------------------------------------------------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Presupuesto gratis en cada trabajo. Llama y cuentanos que necesitas." data-en="Free estimate on every job. Call and tell us what you need.">Free estimate on every job. Call and tell us what you need.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Nuestros" data-en="Our">Our</span> <span class="text-shine" data-es="servicios" data-en="services">services</span>')

services_grid_re = re.compile(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    re.S)
m = services_grid_re.search(h)
assert m, "no se encontro el grid de servicios"
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Mas pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Instalacion de pisos" data-en="Flooring Installation">Flooring Installation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pisos nuevos de madera, laminado o vinilo, incluyendo escaleras, medidos y colocados con precision." data-en="New wood, laminate or vinyl flooring, stairs included, measured and installed with precision.">New wood, laminate or vinyl flooring, stairs included, measured and installed with precision.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Cotizacion gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,124,74,0.4); box-shadow: 0 18px 50px rgba(51,42,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especialidad" data-en="Specialty">Specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Remodelacion de banos" data-en="Bathroom Remodeling">Bathroom Remodeling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Duchas de marmol, impermeabilizacion y acabados completos de bano, de principio a fin." data-en="Marble showers, waterproofing and full bathroom finishes, start to finish.">Marble showers, waterproofing and full bathroom finishes, start to finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Cotizacion gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Todo tipo" data-en="All kinds">All kinds</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reparaciones generales" data-en="General Repairs">General Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Puertas correderas, carpinteria, plomeria menor y los arreglos que una casa necesita." data-en="Sliding doors, carpentry, minor plumbing and the fixes every home needs.">Sliding doors, carpentry, minor plumbing and the fixes every home needs.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Cotizacion gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="A medida" data-en="Custom">Custom</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Instalaciones a medida" data-en="Custom Installations">Custom Installations</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Calefaccion radiante bajo piso, gabinetes y proyectos a medida para tu casa." data-en="Radiant floor heating, cabinetry and custom builds for your home.">Radiant floor heating, cabinetry and custom builds for your home.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Cotizacion gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES + h[m.end():]

note_re = re.compile(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', re.S)
m2 = note_re.search(h)
assert m2
h = h[:m2.start()] + m2.group(1) + '<span data-es="Trabajo garantizado en Seffner, Brandon y Tampa Bay. Llama para un presupuesto." data-en="Guaranteed work across Seffner, Brandon and Tampa Bay. Call for a free quote.">Guaranteed work across Seffner, Brandon and Tampa Bay. Call for a free quote.</span>' + m2.group(2) + h[m2.end():]
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 12. GALERIA: reemplazo completo del grid (curada, sin selfies/reflejos de gente)
# ---------------------------------------------------------------------------
rep('<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n          ' + NEW_MAP_ICON + '\n          Google Maps\n        </a>',
    '')
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="work">work</span>')

gallery_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', re.S)
mg = gallery_re.search(h)
assert mg, "no se encontro el grid de galeria"
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Cocina remodelada" data-en="Remodeled kitchen">Remodeled kitchen</span><img src="assets/raw/gmaps-8.jpg" alt="Cocina remodelada por Quality Handyman Services en Brandon" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Ducha de marmol" data-en="Marble shower">Marble shower</span><img src="assets/raw/gmaps-2.jpg" alt="Ducha de marmol terminada por Quality Handyman" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Escalera de madera" data-en="Wood staircase">Wood staircase</span><img src="assets/raw/gmaps-4.jpg" alt="Escalera de madera nueva instalada por Quality Handyman" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Instalacion de pisos" data-en="Flooring install">Flooring install</span><img src="assets/raw/gmaps-5.jpg" alt="Instalacion de piso de madera en progreso" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Impermeabilizacion" data-en="Waterproofing">Waterproofing</span><img src="assets/raw/gmaps-6.jpg" alt="Impermeabilizacion de ducha antes de colocar azulejo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Calefaccion radiante" data-en="Radiant heating">Radiant heating</span><img src="assets/raw/gmaps-9.jpg" alt="Instalacion de calefaccion radiante bajo el piso" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:mg.start()] + NEW_GALLERY + h[mg.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 13. OPINIONES (3 reviews reales)
# ---------------------------------------------------------------------------
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 10 reseñas verificadas en Google" data-en="5.0 out of 5 · 10 verified reviews on Google">5.0 out of 5 · 10 verified reviews on Google</span></p>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Ryan did a great job. We’ve used him a few times. He does great work, is efficient and cleans up after himself. Highly recommend."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tiffany Williams</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I highly recommend this company! Ryan is fantastic! Quality work and good price. He put in my beautiful new floors through my house, and many other small repairs I needed."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Lori Ryan</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great service! Called Saturday morning, came that afternoon to look at the installation job we needed. Sent a professional quote that evening and scheduled the work fast."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Dustin Clark</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 14. UBICACION -> "Area de servicio" (sin direccion exacta ni mapa, negocio
#     de servicio a domicilio: la direccion de Maps es residencial)
# ---------------------------------------------------------------------------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Area de" data-en="Where we">Where we</span> <span class="text-shine" data-es="servicio" data-en="work">work</span>')
rep('data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    'data-es="Area de servicio" data-en="Service area">Service area</p>', n=1)

location_block_re = re.compile(r'<div class="space-y-4">.*?</div>\s*</div>\s*<div class="frame map-frame reveal min-h-\[380px\]".*?</div>\s*</section>', re.S)
mloc = location_block_re.search(h)
assert mloc, "no se encontro el bloque de ubicacion"
NEW_LOCATION = '''<div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Area que cubrimos" data-en="Areas we cover">Areas we cover</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Seffner, Brandon, Tampa y el area de Tampa Bay. Servicio a domicilio, sin direccion fija de tienda." data-en="Seffner, Brandon, Tampa and the greater Tampa Bay area. We come to you, no storefront address.">Seffner, Brandon, Tampa and the greater Tampa Bay area. We come to you, no storefront address.</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Llamar o escribir" data-en="Call or text">Call or text</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Cuentanos que necesitas y te damos un presupuesto gratis." data-en="Tell us what you need and get a free estimate.">Tell us what you need and get a free estimate.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,124,74,0.4)]" href="''' + TEL + '''">(813) 784-0747</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Los 7 dias, 7:30am a 7pm." data-en="7 days a week, 7:30am to 7pm.">7 days a week, 7:30am to 7pm.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>'''
h = h[:mloc.start()] + NEW_LOCATION + h[mloc.end():]
print("UBICACION done")

# ---------------------------------------------------------------------------
# 15. CTA FINAL
# ---------------------------------------------------------------------------
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proyecto" data-en="Your next project">Your next project</span> <span class="text-shine" data-es="empieza con una llamada" data-en="starts with a call">starts with a call</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Llama hoy para un presupuesto gratis: pisos, baños, reparaciones e instalaciones en Seffner, Brandon y Tampa Bay." data-en="Call today for a free estimate: flooring, bathrooms, repairs and installations across Seffner, Brandon and Tampa Bay.">Call today for a free estimate: flooring, bathrooms, repairs and installations across Seffner, Brandon and Tampa Bay.</p>')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="' + TEL + '" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (813) 784-0747" data-en="Call (813) 784-0747">Call (813) 784-0747</a>\n        <a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Ver en Google Maps" data-en="View on Google Maps">View on Google Maps</a>')
print("CTA done")

# ---------------------------------------------------------------------------
# 16. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Quality Handyman</span>')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Quality Handyman</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Servicio de handyman en Seffner, Brandon y Tampa Bay, FL. Presupuesto gratis." data-en="Handyman service in Seffner, Brandon and Tampa Bay, FL. Free estimates.">Handyman service in Seffner, Brandon and Tampa Bay, FL. Free estimates.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p data-es="Seffner, Brandon y Tampa Bay, FL" data-en="Seffner, Brandon and Tampa Bay, FL">Seffner, Brandon and Tampa Bay, FL</p>')
rep('<p><a href="' + TEL + '" target="_blank" rel="noopener" class="hover:text-[#f0d9be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + TEL + '" class="hover:text-[#f0d9be]">(813) 784-0747</a></p>')
rep('<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>\n        <p><a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="hover:text-[#f0d9be]">Instagram · Google Maps</a></p>',
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="En linea" data-en="Online">Online</p>\n        <p><a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="hover:text-[#f0d9be]">Google · 5.0 (10 reviews)</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Quality Handyman Services and Installations.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 17. Boton flotante: llamar (icono telefono)
# ---------------------------------------------------------------------------
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf6f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>',
    '<a href="' + TEL + '" class="book-float" aria-label="Llamar ahora">\n    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#faf6f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Llamar ahora" data-en="Call now">Call now</span>\n  </a>')
print("FLOAT done")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("WRITTEN", PATH)
