import re
import os
import colorsys
import shutil

SLUG = "jama-manjares-catering"
SRC = "templates/light-v2/index.html"
DST = f"output/{SLUG}/index.html"

h = open(SRC, encoding="utf-8").read()


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
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> teal tropical (JAMA Completas & Mas)
# ---------------------------------------------------------------------------
_HEXES = ["#a04a72", "#5c2140", "#f0bed7", "#faf2f6", "#c47a9c", "#8a5573", "#f3e0ea",
          "#d9a8c2", "#7d3457", "#5f2c48", "#33222c", "#fbf3f8", "#fbeff5", "#f8dfeb",
          "#f6f1ea", "#f2d5e3", "#f2cfe0", "#efd0e0", "#e5c1d4", "#dc9dbe", "#d3a2bc",
          "#c9789f", "#b25a85", "#2a1722", "#1f0f18", "#1c0f16"]
_RGBAS = [(160, 74, 114), (51, 34, 44), (240, 190, 215), (70, 25, 50), (250, 242, 246),
          (125, 52, 87), (253, 246, 250), (40, 16, 30), (233, 205, 186), (185, 138, 128)]

TARGET_HUE = 175 / 360.0
SAT_MUL = 1.0


def _shift_hex(hx):
    hx = hx.lstrip('#')
    r, g, b = int(hx[0:2], 16) / 255, int(hx[2:4], 16) / 255, int(hx[4:6], 16) / 255
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(TARGET_HUE, l, min(1.0, s * SAT_MUL))
    return '#%02x%02x%02x' % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def _shift_rgb(rgb):
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(TARGET_HUE, l, min(1.0, s * SAT_MUL))
    return (round(r2 * 255), round(g2 * 255), round(b2 * 255))


PALETTE = [(hx, _shift_hex(hx)) for hx in _HEXES]
for old, new in PALETTE:
    rep_all(old, new)

RGBA_FAMILIES = [(rgb, _shift_rgb(rgb)) for rgb in _RGBAS]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

h = h.replace('@@BADGE@@', badge_block, 1)
print("PALETTE done")

# Valores ya desplazados (hue=175) que se reusan en reps literales:
RING1 = "rgba(74,160,153"   # era rgba(160,74,114
RING2 = "rgba(190,240,236"  # era rgba(240,190,215
SHADOW1 = "rgba(34,51,50"   # era rgba(51,34,44
HEX_HOVER = "#bef0ec"       # era #f0bed7

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform -> tel: ; SI hay IG real (@jamarestaurant305)
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+17865585548"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/jamarestaurant305/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@jamarestaurant305"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_ADDR = "9612 Fontainebleau Blvd, Miami, FL 33172"
NEW_MAPS = "https://www.google.com/maps?q=9612+Fontainebleau+Blvd,+Miami,+FL+33172"

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>JAMA Completas &amp; Mas · Cocina Cubana y Catering en Miami, FL | 4.8 en Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="JAMA Completas &amp; Mas by Manjares Catering, Miami FL: barra caliente cubana todos los dias y catering de bandejas para oficinas y eventos. 4.8 estrellas en 21 resenas de Google." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="JAMA Completas &amp; Mas · Cocina Cubana y Catering en Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Barra caliente cubana y catering de bandejas. 4.8 en Google con 21 resenas." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-storefront.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CateringService",
    "name": "JAMA Completas & Mas by Manjares Catering",
    "description": "Cocina cubana y catering en Miami, FL: barra caliente diaria con completas cubanas, arroz, frijoles y platanos, ademas de catering de bandejas para oficinas y eventos por Manjares Catering.",
    "address": { "@type": "PostalAddress", "streetAddress": "9612 Fontainebleau Blvd", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33172", "addressCountry": "US" },
    "telephone": "+1-786-558-5548",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "21", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "11:00", "closes": "20:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Cuban kitchen & catering", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Daily Hot Bar" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Office &amp; Event Catering" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Salad Bar" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Grilled &amp; Roasted" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio ES -> invertir default del esqueleto (que viene en EN)
# ---------------------------------------------------------------------------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")
print("IDIOMA done (invertido a ES)")

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.35)]" />',
    '<img src="assets/logo.jpg" alt="JAMA Completas y Mas" class="w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">JAMA <span class="text-[color:var(--accent-deep)]">Completas</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">JM</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">JAMA Completas &amp; Mas</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Llamar ahora</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Llamar ahora</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Cocina Cubana y Catering" data-en="Miami, FL · Cuban Kitchen &amp; Catering">Miami, FL · Cocina Cubana y Catering</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Jama real, todos los dias." data-en="Real Cuban food, every day.">Jama real, todos los dias.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Completas cubanas y catering" data-en="Cuban completas and catering">Completas cubanas y catering</span><br /><span data-es="de bandejas, hecho " data-en="trays, made ">de bandejas, hecho </span><span class="text-shine" data-es="con cuidado" data-en="with care">con cuidado</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Barra caliente cubana todos los dias con arroz, frijoles, platanos y puerco asado, ademas de catering de bandejas para oficinas y eventos por Manjares Catering. Abierto de lunes a sabado hasta que se acabe la jama." data-en="A daily Cuban hot bar with rice, beans, plantains and roast pork, plus office and event catering trays by Manjares Catering. Open Monday to Saturday until the jama runs out.">Barra caliente cubana todos los dias con arroz, frijoles, platanos y puerco asado, ademas de catering de bandejas para oficinas y eventos por Manjares Catering. Abierto de lunes a sabado hasta que se acabe la jama.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.8 · 21 resenas en Google" data-en="4.8 · 21 reviews on Google">4.8 · 21 resenas en Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llama al (786) 558-5548" data-en="Call (786) 558-5548">Llama al (786) 558-5548</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-storefront.jpg" alt="La fachada de JAMA Completas y Mas en Miami, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Horario" data-en="Hours">Horario</p>
            <p class="font-display text-lg">Lun-Sab</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="11 AM hasta que se acabe" data-en="11 AM until it runs out">11 AM hasta que se acabe</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="21">21</span> <span data-es="resenas en Google" data-en="reviews on Google">resenas en Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Completas <span class="text-shine">&amp;</span> Mas</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Barra caliente diaria" data-en="Daily hot bar">Barra caliente diaria</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">Lun-Sab</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Hasta que se acabe la jama" data-en="Until the jama runs out">Hasta que se acabe la jama</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Fontainebleau Blvd</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Completas Cubanas"),
    ("Hybrid Set", "Catering de Oficina"),
    ("Volume Set", "Barra de Ensaladas"),
    ("Mega Volume", "Puerco Asado"),
    ("Bottom Lashes", "Catering de Eventos"),
    ("West Palm Beach, FL", "Miami, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (1 sola foto real -> grid 1 col)
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
          <img src="assets/about-mural.jpg" alt="Mural de JAMA con cerditos voladores en el comedor" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Manjares Catering," data-en="Manjares Catering,">Manjares Catering,</span><br /><span class="text-shine" data-es="sabor cubano de siempre" data-en="classic Cuban flavor">sabor cubano de siempre</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="JAMA Completas &amp; Mas es el mostrador de comida cubana de Manjares Catering en Fontainebleau Blvd. Cada dia sale una barra caliente distinta (arroz, frijoles, platanos, puerco asado) y el mismo equipo arma bandejas de catering para oficinas y fiestas." data-en="JAMA Completas &amp; Mas is the Cuban food counter from Manjares Catering on Fontainebleau Blvd. A different hot bar comes out every day (rice, beans, plantains, roast pork), and the same team puts together catering trays for offices and parties.">JAMA Completas &amp; Mas es el mostrador de comida cubana de Manjares Catering en Fontainebleau Blvd. Cada dia sale una barra caliente distinta (arroz, frijoles, platanos, puerco asado) y el mismo equipo arma bandejas de catering para oficinas y fiestas.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 4.8 estrellas en 21 resenas de Google, con clientes que vuelven casi a diario por la variedad del menu." data-en="The result: a 4.8-star rating across 21 Google reviews, with customers who come back almost daily for the variety on the menu.">El resultado: 4.8 estrellas en 21 resenas de Google, con clientes que vuelven casi a diario por la variedad del menu.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="21">21</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Resenas" data-en="Reviews">Resenas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">6</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Dias a la semana" data-en="Days a week">Dias a la semana</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="JAMA Completas y Mas" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[' + RING1 + ',0.3)]" loading="lazy" />\n            <span class="text-sm font-light">JAMA · <span class="text-[color:var(--ink-40)]" data-es="Manjares Catering" data-en="Manjares Catering">Manjares Catering</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu pedido, plato" data-en="Your order, plate">Tu pedido, plato</span> <span class="text-shine" data-es="por plato" data-en="by plate">por plato</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Pasa o llama" data-en="Walk in or call">Pasa o llama</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Ven directo al mostrador en Fontainebleau Blvd, o llama para encargar bandejas de catering." data-en="Come straight to the counter on Fontainebleau Blvd, or call to order catering trays.">Ven directo al mostrador en Fontainebleau Blvd, o llama para encargar bandejas de catering.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="La jama del dia" data-en="Today's jama">La jama del dia</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="La barra caliente cambia cada dia: completas cubanas, arroz, frijoles, platanos y mas, recien hechos." data-en="The hot bar changes every day: Cuban completas, rice, beans, plantains and more, made fresh.">La barra caliente cambia cada dia: completas cubanas, arroz, frijoles, platanos y mas, recien hechos.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Para llevar o en bandeja" data-en="To go or by the tray">Para llevar o en bandeja</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llevate tu plato individual, o pide una bandeja completa de Manjares Catering para la oficina o la fiesta." data-en="Grab a single plate to go, or order a full Manjares Catering tray for the office or the party.">Llevate tu plato individual, o pide una bandeja completa de Manjares Catering para la oficina o la fiesta.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Vuelves manana" data-en="Come back tomorrow">Vuelves manana</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Manana sale otra barra distinta: por eso hay clientes que pasan casi todos los dias de la semana." data-en="Tomorrow a different hot bar comes out: that is why some customers stop by almost every day of the week.">Manana sale otra barra distinta: por eso hay clientes que pasan casi todos los dias de la semana.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Comida para" data-en="Food for">Comida para</span> <span class="text-shine" data-es="cada dia y cada evento" data-en="every day and every event">cada dia y cada evento</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="El menu del mostrador cambia a diario. Para bandejas de catering, el precio se cotiza segun el numero de personas." data-en="The counter menu changes daily. For catering trays, pricing is quoted based on headcount.">El menu del mostrador cambia a diario. Para bandejas de catering, el precio se cotiza segun el numero de personas.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: ''' + RING1 + ''',0.4); box-shadow: 0 18px 50px ''' + SHADOW1 + ''',0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo mas pedido" data-en="Most requested">Lo mas pedido</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Barra Caliente Diaria" data-en="Daily Hot Bar">Barra Caliente Diaria</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Completas cubanas, arroz, frijoles, platanos y puerco asado, distinto cada dia de lunes a sabado." data-en="Cuban completas, rice, beans, plantains and roast pork, different every day Monday to Saturday.">Completas cubanas, arroz, frijoles, platanos y puerco asado, distinto cada dia de lunes a sabado.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Ven al mostrador" data-en="Come to the counter">Ven al mostrador</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Llamar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Bandejas" data-en="Trays">Bandejas</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Catering de Oficina y Eventos" data-en="Office &amp; Event Catering">Catering de Oficina y Eventos</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Bandejas de Manjares Catering para almuerzos de oficina, fiestas y celebraciones de Thanksgiving." data-en="Manjares Catering trays for office lunches, parties and Thanksgiving celebrations.">Bandejas de Manjares Catering para almuerzos de oficina, fiestas y celebraciones de Thanksgiving.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Pide tu cotizacion" data-en="Get a quote">Pide tu cotizacion</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Llamar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Fresco" data-en="Fresh">Fresco</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Barra de Ensaladas" data-en="Salad Bar">Barra de Ensaladas</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Ensalada cesar y vegetales frescos para acompanar cualquier plato del mostrador." data-en="Caesar salad and fresh vegetables to go alongside any counter plate.">Ensalada cesar y vegetales frescos para acompanar cualquier plato del mostrador.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Ven al mostrador" data-en="Come to the counter">Ven al mostrador</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Llamar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="A la parrilla" data-en="Grilled">A la parrilla</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Asados y Horneados" data-en="Grilled &amp; Roasted">Asados y Horneados</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Costillas, pollo a la plancha y salmon al horno entre las opciones de proteina del dia." data-en="Ribs, grilled chicken and baked salmon among the daily protein options.">Costillas, pollo a la plancha y salmon al horno entre las opciones de proteina del dia.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Ven al mostrador" data-en="Come to the counter">Ven al mostrador</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Llamar</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Del dia" data-en="Daily">Del dia</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Completas cubanas" data-en="Cuban completas">Completas cubanas</li>
            <li class="flex items-center gap-2" data-es="Arroz y frijoles" data-en="Rice &amp; beans">Arroz y frijoles</li>
            <li class="flex items-center gap-2" data-es="Platanos maduros" data-en="Sweet plantains">Platanos maduros</li>
            <li class="flex items-center gap-2" data-es="Puerco asado" data-en="Roast pork">Puerco asado</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Catering" data-en="Catering">Catering</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Bandejas para oficina" data-en="Office trays">Bandejas para oficina</li>
            <li class="flex items-center gap-2" data-es="Pavo de Thanksgiving" data-en="Thanksgiving turkey">Pavo de Thanksgiving</li>
            <li class="flex items-center gap-2" data-es="Fiestas y celebraciones" data-en="Parties &amp; celebrations">Fiestas y celebraciones</li>
            <li class="flex items-center gap-2" data-es="Cotizacion por numero de invitados" data-en="Quoted by headcount">Cotizacion por numero de invitados</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Proteinas" data-en="Proteins">Proteinas</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Costillas en salsa BBQ" data-en="BBQ ribs">Costillas en salsa BBQ</li>
            <li class="flex items-center gap-2" data-es="Pollo a la plancha" data-en="Grilled chicken">Pollo a la plancha</li>
            <li class="flex items-center gap-2" data-es="Salmon al horno" data-en="Baked salmon">Salmon al horno</li>
            <li class="flex items-center gap-2" data-es="Ensalada cesar" data-en="Caesar salad">Ensalada cesar</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Llama al (786) 558-5548 para pedir bandejas de catering con anticipacion." data-en="Call (786) 558-5548 ahead to order catering trays.">Llama al (786) 558-5548 para pedir bandejas de catering con anticipacion.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="La jama" data-en="The jama">La jama</span> <span class="text-shine" data-es="de verdad" data-en="itself">de verdad</span>')
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

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="La barra caliente del dia" data-en="Today's hot bar">Today's hot bar</span><img src="assets/gallery-hotbar-wide.jpg" alt="La barra caliente de JAMA Completas y Mas con pescado, pollo y vegetales" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Ensalada cesar" data-en="Caesar salad">Caesar salad</span><img src="assets/gallery-caesar-salad.jpg" alt="Ensalada cesar fresca en la barra de JAMA Completas y Mas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Costillas y pollo asado" data-en="Ribs &amp; roast chicken">Ribs &amp; roast chicken</span><img src="assets/gallery-ribs-chicken.jpg" alt="Costillas en salsa BBQ y pollo asado con papas en JAMA Completas y Mas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Barra de ensaladas" data-en="Salad bar">Salad bar</span><img src="assets/gallery-salad-bar.jpg" alt="Barra de ensaladas y acompanantes en JAMA Completas y Mas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Arroz, frijoles y platanos" data-en="Rice, beans &amp; plantains">Rice, beans &amp; plantains</span><img src="assets/gallery-rice-beans-platanos.jpg" alt="Arroz congri, frijoles negros y platanos maduros con mas plato en JAMA" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="Lo que dicen" data-en="What">Lo que dicen</span> <span class="text-shine" data-es="en Miami" data-en="Miami says">en Miami</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★☆</span> &nbsp;<span data-es="4.8 de 5 · 21 resenas en Google" data-en="4.8 out of 5 · 21 reviews on Google">4.8 de 5 · 21 resenas en Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Cuban infused bowls and dishes. Friendly service. Definitely I'll come back!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ralph Aguilera</span> <span class="text-[color:var(--ink-40)]" data-es="Resena de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Used Manjares catering today for out Thanksgiving work lunch. The food was delicious! Great variety of side dishes and the turkey is moist and tender. Would definitely recommend."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Deborah Cortina</span> <span class="text-[color:var(--ink-40)]" data-es="Resena de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I pick up my food almost every day. I love the fact that there is so much variety each day without having to repeat the same meal for weeks. I look forward to dinner after work."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Marta Torres</span> <span class="text-[color:var(--ink-40)]" data-es="Resena de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=JAMA+Completas+Manjares+Catering+Miami+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Lee las 21 resenas en Google" data-en="Read all 21 reviews on Google">Lee las 21 resenas en Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION (direccion real disponible)
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visitanos en" data-en="Visit us in">Visitanos en</span> <span class="text-shine">Miami</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Direccion" data-en="Address">Direccion</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + NEW_ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Como llegar" data-en="Get directions">Como llegar</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Horario</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sabado, 11:00 AM hasta que se acabe la jama. Domingo cerrado." data-en="Monday to Saturday, 11:00 AM until the jama runs out. Closed Sunday.">Lunes a sabado, 11:00 AM hasta que se acabe la jama. Domingo cerrado.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_TEL + '''" data-es="Llama al (786) 558-5548" data-en="Call (786) 558-5548">Llama al (786) 558-5548</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
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
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira la barra del dia y escribe por DM para encargar tu bandeja de catering." data-en="See the day's hot bar and DM to order your catering tray.">Mira la barra del dia y escribe por DM para encargar tu bandeja de catering.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[''' + RING1 + ''',0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: JAMA Completas y Mas, 9612 Fontainebleau Blvd, Miami FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Jama real, todos los dias." data-en="Real Cuban food, every day.">Jama real, todos los dias.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu bandeja te" data-en="Your tray is">Tu bandeja te</span> <span class="text-shine" data-es="esta esperando" data-en="waiting for you">esta esperando</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Llama al (786) 558-5548 para tu bandeja de catering, o pasa de lunes a sabado por la barra caliente del dia." data-en="Call (786) 558-5548 for your catering tray, or stop by Monday to Saturday for the daily hot bar.">Llama al (786) 558-5548 para tu bandeja de catering, o pasa de lunes a sabado por la barra caliente del dia.</p>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llama al (786) 558-5548" data-en="Call (786) 558-5548">Llama al (786) 558-5548</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Siguenos en Instagram" data-en="Follow on Instagram">Siguenos en Instagram</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">JAMA</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[''' + RING2 + ''',0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="JAMA Completas y Mas" class="w-9 h-9 rounded-full object-cover ring-1 ring-[''' + RING2 + ''',0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">JAMA Completas &amp; Mas</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Cocina cubana y catering por Manjares Catering en Miami, FL." data-en="Cuban kitchen and catering by Manjares Catering in Miami, FL.">Cocina cubana y catering por Manjares Catering en Miami, FL.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HEX_HOVER + ''']" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[''' + HEX_HOVER + ''']" data-es="Llama al (786) 558-5548" data-en="Call (786) 558-5548">Llama al (786) 558-5548</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HEX_HOVER + ''']">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Siguenos" data-en="Follow">Siguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[''' + HEX_HOVER + ''']">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 JAMA Completas &amp; Mas.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_TEL + '" class="book-float" aria-label="Llamar a JAMA Completas y Mas">')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 20. Limpieza: tel: links no necesitan target=_blank/rel=noopener
# ---------------------------------------------------------------------------
h = h.replace(f'href="{NEW_TEL}" target="_blank" rel="noopener"', f'href="{NEW_TEL}"')
print("CLEANUP tel links done")

with open(DST, "w", encoding="utf-8") as f:
    f.write(h)
print("FINAL WRITE done ->", DST)
