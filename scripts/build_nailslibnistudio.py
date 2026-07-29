import re
import os
import shutil
import colorsys

SLUG = "nailslibnistudio"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
shutil.copyfile("templates/assets/tailwind.js", f"output/{SLUG}/assets/tailwind.js")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:160]
    h = h.replace(a, b, n)


# ---------- 1. Proteger el badge Merktop ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------- 2. Paleta: rotacion de matiz (HUE_SHIFT=47, plum-pink a04a72 -> coral-terracota) ----------
HUE_SHIFT = 47.0


def shift_hex(hexcode):
    r = int(hexcode[0:2], 16) / 255.0
    g = int(hexcode[2:4], 16) / 255.0
    b = int(hexcode[4:6], 16) / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l, s)
    return '%02x%02x%02x' % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def shift_rgb_tuple(rr, gg, bb):
    r, g, b = rr / 255.0, gg / 255.0, bb / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l, s)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def repl_hex(mo):
    return '#' + shift_hex(mo.group(1))


def repl_rgba(mo):
    rr, gg, bb = int(mo.group(1)), int(mo.group(2)), int(mo.group(3))
    alpha = mo.group(4)
    nr, ng, nb = shift_rgb_tuple(rr, gg, bb)
    if alpha is not None:
        return 'rgba(%d,%d,%d,%s)' % (nr, ng, nb, alpha)
    return 'rgb(%d,%d,%d)' % (nr, ng, nb)


h = re.sub(r'#([0-9a-fA-F]{6})\b', repl_hex, h)
h = re.sub(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)', repl_rgba, h)

h = h.replace('@@BADGE@@', badge_block, 1)
print("PALETTE done ->", shift_hex('a04a72'), shift_hex('c47a9c'))

# Colores derivados que necesito reproducir a mano en literales nuevos (ya vienen
# shifteados en todo `h` desde el paso global de arriba; los recalculo para
# poder escribir anclas/strings nuevos que calcen exactamente).
DEEP_RGB = shift_rgb_tuple(160, 74, 114)      # accent-deep
INK_RGB = shift_rgb_tuple(51, 34, 44)         # --ink (sombras)
DARKPINK_RGB = shift_rgb_tuple(240, 190, 215)  # acento shine en dark-band

# ---------- 3. Globales: Booksy, Instagram, handle ----------
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1628998_nails-libni-studio_nail-salon_15889_miami'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG = 'https://www.instagram.com/_lashbloom/'
NEW_IG = 'https://www.instagram.com/nail_by_libni/'
assert OLD_IG in h
h = h.replace(OLD_IG, NEW_IG)

OLD_HANDLE = '@_lashbloom'
NEW_HANDLE = '@nail_by_libni'
assert OLD_HANDLE in h
h = h.replace(OLD_HANDLE, NEW_HANDLE)
print("GLOBALS done")

# ---------- 4. HEAD: title, meta, JSON-LD, favicon ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    "<title>Nails Libni Studio · Nail Salon in Miami, FL | 5.0 on Booksy</title>")
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Nails Libni Studio, Miami FL: apres, rubber base gel, builder gel, acrylic and nail art with a perfect 5.0 across 66 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Nails Libni Studio · Nail Salon in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Apres, rubber base gel, builder gel, acrylic and nail art. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-14.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-11.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nails Libni Studio",
    "description": "Nail salon in Miami, FL: apres, rubber base gel, builder gel, acrylic and nail art.",
    "address": { "@type": "PostalAddress", "streetAddress": "2715 SW 37th Ave", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33133", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.740260556778058, "longitude": -80.25394000000001 },
    "sameAs": ["https://booksy.com/en-us/1628998_nails-libni-studio_nail-salon_15889_miami", "https://www.instagram.com/nail_by_libni/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "66", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres" } },
      { "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Set de Builder Gel o Poli Gel (largas)" } },
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicura de gel" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrílico Full Set (uñas largas)" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------- 5. Idioma: ES por defecto ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")
print("LANG done")

# ---------- 6. PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NL</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Nails Libni</span>')

# ---------- 7. NAV ----------
rep(f'<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba({DEEP_RGB[0]},{DEEP_RGB[1]},{DEEP_RGB[2]},0.35)]" />',
    f'<img src="assets/raw/bk-9.jpg" alt="Libni Pérez, artista de Nails Libni Studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba({DEEP_RGB[0]},{DEEP_RGB[1]},{DEEP_RGB[2]},0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails <span class="text-[color:var(--accent-deep)]">Libni</span></span>')
print("NAV done")

# ---------- 8. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Salón de Uñas" data-en="Miami, FL · Nail Salon">Miami, FL · Salón de Uñas</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Color y detalle en cada diseño." data-en="Color and detail in every design.">Color y detalle en cada diseño.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Uñas con arte y color," data-en="Colorful nail art,">Uñas con arte y color,</span><br /><span data-es="hechas para " data-en="made to ">hechas para </span><span class="text-shine" data-es="brillar" data-en="shine">brillar</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '''data-es="Apres, rubber base gel, builder gel, acrílico y nail art, de la mano de Libni Pérez en su propio estudio en Miami, FL. Un 5.0 perfecto en 66 reseñas de Booksy." data-en="Apres, rubber base gel, builder gel, acrylic and nail art, by Libni Pérez in her own studio in Miami, FL. A perfect 5.0 across 66 Booksy reviews.">Apres, rubber base gel, builder gel, acrylic and nail art, by Libni Pérez in her own studio in Miami, FL. A perfect 5.0 across 66 Booksy reviews.</p>''')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 66 reseñas en Booksy" data-en="5.0 · 66 reviews on Booksy">5.0 · 66 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-5.jpg" alt="Manicura francesa en rosa y blanco junto a un tulipán rosado, terminado de Nails Libni Studio" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Builder Gel o Poli Gel (largas)</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$130 · 2h" data-en="$130 · 2h">$130 · 2h</p>')
print("HERO done")

# ---------- 9. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="66">66</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Acrílico</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sistemas completos · Refills" data-en="Full systems · Refills">Sistemas completos · Refills</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">34 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Menú completo en Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">SW 37th Ave</p></div>')
print("STRIP done")

# ---------- 10. MARQUEE (x4 cada palabra) ----------
for old, new in [
    ('Classic Set', 'Rubber Base Gel'),
    ('Hybrid Set', 'Builder Gel'),
    ('Volume Set', 'Acrílico'),
    ('Mega Volume', 'Dip Manicura'),
    ('Bottom Lashes', 'Nail Art'),
    ('West Palm Beach, FL', 'Miami, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------- 11. EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Uñas nude sobre un fondo rosa afelpado, terminado de Nails Libni Studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Uñas ovaladas en rosa clásico y limpio, terminado de Nails Libni Studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio" data-en="A studio">Un estudio</span><br /><span class="text-shine" data-es="de arte y color" data-en="of art and color">de arte y color</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '''data-es="Nails Libni Studio es el estudio de Libni Pérez en Miami, FL. Sus clientas la describen como profesional y detallista, siempre asegurándose de que cada diseño quede perfecto, en un ambiente donde te sientes cómoda desde que llegas." data-en="Nails Libni Studio is Libni Pérez's studio in Miami, FL. Her clients describe her as professional and detail-oriented, always making sure every design comes out perfect, in a space where you feel comfortable from the moment you arrive.">Nails Libni Studio is Libni Pérez's studio in Miami, FL. Her clients describe her as professional and detail-oriented, always making sure every design comes out perfect, in a space where you feel comfortable from the moment you arrive.</p>''')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 66 reseñas verificadas en Booksy, y clientas que la recomiendan sin dudarlo." data-en="The result: a perfect 5.0 across 66 verified Booksy reviews, and clients who recommend her without hesitation.">The result: a perfect 5.0 across 66 verified Booksy reviews, and clients who recommend her without hesitation.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="66">66</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep(f'<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba({DEEP_RGB[0]},{DEEP_RGB[1]},{DEEP_RGB[2]},0.3)]" loading="lazy" />',
    f'<img src="assets/raw/bk-9.jpg" alt="Libni Pérez, artista de Nails Libni Studio" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba({DEEP_RGB[0]},{DEEP_RGB[1]},{DEEP_RGB[2]},0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Libni · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ---------- 12. METODO ----------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, uña" data-en="Your visit, nail">Tu cita, uña</span> <span class="text-shine" data-es="por uña" data-en="by nail">por uña</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio claro, y confirmas al instante." data-en="Pick your service on Booksy with clear pricing, and confirm instantly.">Eliges tu servicio en Booksy con precio claro, y confirmas al instante.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Elige el sistema" data-en="Choose the system">Elige el sistema</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Rubber base gel, acrílico, builder gel o dip: Libni te ayuda a elegir según el look que buscas." data-en="Rubber base gel, acrylic, builder gel or dip: Libni helps you choose based on the look you want.">Rubber base gel, acrílico, builder gel o dip: Libni te ayuda a elegir según el look que buscas.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Diseño y color" data-en="Design and color">Diseño y color</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nail art, francesa o efecto espejo cromado: cada diseño se personaliza uña por uña." data-en="Nail art, French tips or chrome mirror effect: every design is personalized nail by nail.">Nail art, francesa o efecto espejo cromado: cada diseño se personaliza uña por uña.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">Salida</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con uñas limpias, cuidadas y hermosas, listas para tu próxima cita." data-en="You leave with nails that are clean, cared for and beautiful, ready for your next appointment.">Sales con uñas limpias, cuidadas y hermosas, listas para tu próxima cita.</p>''')
print("METODO done")

# ---------- 13. SERVICIOS ----------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios publicados por Nails Libni Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices as published by Nails Libni Studio on Booksy. Booking confirms instantly.">Precios publicados por Nails Libni Studio en Booksy. Reserva con confirmación inmediata.</p>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema Aprés" data-en="Aprés system">Sistema Aprés</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Apres</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sistema Aprés, ligero y de acabado natural." data-en="The Aprés system, light with a natural finish.">Sistema Aprés, ligero y de acabado natural.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p></div>
            <a href="https://booksy.com/en-us/1628998_nails-libni-studio_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba({DEEP_RGB[0]},{DEEP_RGB[1]},{DEEP_RGB[2]},0.4); box-shadow: 0 18px 50px rgba({INK_RGB[0]},{INK_RGB[1]},{INK_RGB[2]},0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Favorito del salón</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Set de Builder Gel o Poli Gel (largas)" data-en="Builder Gel or Poli Gel Full Set (long)">Full Set de Builder Gel o Poli Gel (largas)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full set con builder gel o poli gel en uñas largas, con acabado duradero y personalizado." data-en="Full set with builder gel or poly gel on long nails, with a durable, personalized finish.">Full set con builder gel o poli gel en uñas largas, con acabado duradero y personalizado.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$130</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="https://booksy.com/en-us/1628998_nails-libni-studio_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Uso diario" data-en="Everyday">Uso diario</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura de gel" data-en="Gel Manicure">Manicura de gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Esmaltado en gel de larga duración sobre tus uñas naturales." data-en="Long-lasting gel polish over your natural nails.">Esmaltado en gel de larga duración sobre tus uñas naturales.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="https://booksy.com/en-us/1628998_nails-libni-studio_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Acrílico" data-en="Acrylic">Acrílico</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Acrílico Full Set (uñas largas)" data-en="Acrylic Full Set (long nails)">Acrílico Full Set (uñas largas)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full set de acrílico en uñas largas, con la resistencia clásica del sistema." data-en="Acrylic full set on long nails, with the system's classic durability.">Full set de acrílico en uñas largas, con la resistencia clásica del sistema.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p></div>
            <a href="https://booksy.com/en-us/1628998_nails-libni-studio_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También disponibles: pedicura, dip manicura, jelly spa, manicura francesa y nail art, y 30 más. Menú completo de 34 servicios y disponibilidad en Booksy." data-en="Also available: pedicure, dip manicure, jelly spa, French manicure and nail art, and 30 more. Full 34-service menu and availability on Booksy.">También disponibles: pedicura, dip manicura, jelly spa, manicura francesa y nail art, y 30 más. Menú completo de 34 servicios y disponibilidad en Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 14. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Diseños" data-en="Real">Diseños</span> <span class="text-shine" data-es="reales" data-en="designs">reales</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño abstracto en coral y neón" data-en="Neon coral abstract design">Diseño abstracto en coral y neón</span><img src="assets/raw/bk-14.jpg" alt="Diseño abstracto en coral y rosa neón, terminado de Nails Libni Studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Anillos y nail art floral en azul" data-en="Rings and blue floral nail art">Anillos y nail art floral en azul</span><img src="assets/raw/bk-1.jpg" alt="Manos con anillos y nail art floral en azul, terminado de Nails Libni Studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Base blanca con flores en naranja y rojo" data-en="White base with orange and red floral art">Base blanca con flores en naranja y rojo</span><img src="assets/raw/bk-3.jpg" alt="Uñas con base blanca y arte floral en naranja y rojo, terminado de Nails Libni Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Patrón atrevido en amarillo, negro y dorado" data-en="Bold yellow, black and gold pattern">Patrón atrevido en amarillo, negro y dorado</span><img src="assets/raw/bk-7.jpg" alt="Uñas con patrón atrevido en amarillo, negro y dorado, terminado de Nails Libni Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Ombré nude con confeti sobre madera" data-en="Nude ombre with confetti on wood">Ombré nude con confeti sobre madera</span><img src="assets/raw/bk-10.jpg" alt="Uñas en ombré nude y blanco con confeti sobre mesa de madera, terminado de Nails Libni Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Uñas nude limpias y naturales" data-en="Clean, natural nude nails">Uñas nude limpias y naturales</span><img src="assets/raw/bk-11.jpg" alt="Uñas nude limpias y naturales, terminado de Nails Libni Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 15. OPINIONES ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 66 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 66 verified reviews on Booksy">5.0 de 5 · 66 reseñas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing customer service very welcoming and warming love how my nails looks, overall very satisfied. I definitely recommend."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mitzi C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"¡Súper recomendada! 💅✨ Quedé encantada con el trabajo de mi manicurista. Es muy profesional, detallista y siempre se asegura de que cada diseño quede perfecto. Además, el ambiente es agradable y te hace sentir muy cómoda desde que llegas. 🩷 Si estás buscando a alguien que deje tus uñas hermosas, duraderas y con acabados impecables, no dudes en visitarla. ¡Definitivamente volveré! 😍👏💖"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Angie C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"AMAZING!!!🫶🏼"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mariell</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1628998_nails-libni-studio_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1628998_nails-libni-studio_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 66 reseñas en Booksy" data-en="Read all 66 reviews on Booksy">Leer las 66 reseñas en Booksy</a>')
print("OPINIONES done")

# ---------- 16. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Miami</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">2715 SW 37th Ave, Miami, FL 33133</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=2715+SW+37th+Ave,+Miami,+FL+33133"')
rep("data-es=\"Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita.\" data-en=\"See Yesi's latest sets and DM any questions before your appointment.\">See Yesi's latest sets and DM any questions before your appointment.</p>",
    "data-es=\"Mira los diseños más recientes de Libni y escribe por DM cualquier duda antes de tu cita.\" data-en=\"See Libni's latest designs and DM any questions before your appointment.\">Mira los diseños más recientes de Libni y escribe por DM cualquier duda antes de tu cita.</p>")
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Nails Libni Studio, 2715 SW 37th Ave, Miami FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=2715+SW+37th+Ave,+Miami,+FL+33133&output=embed"')
print("UBICACION done")

# ---------- 17. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Arte en cada uña." data-en="Art in every nail.">Arte en cada uña.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Tu próxima cita</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu apres, tu acrílico, tu builder gel o el nail art que ya tienes en mente." data-en="Book online in seconds: your apres, your acrylic, your builder gel, or the nail art you already have in mind.">Reserva en línea en segundos: tu apres, tu acrílico, tu builder gel o el nail art que ya tienes en mente.</p>')
print("CTA FINAL done")

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Nails Libni</span>')
rep(f'<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba({DARKPINK_RGB[0]},{DARKPINK_RGB[1]},{DARKPINK_RGB[2]},0.35)]" loading="lazy" />',
    f'<img src="assets/raw/bk-9.jpg" alt="Libni Pérez, artista de Nails Libni Studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba({DARKPINK_RGB[0]},{DARKPINK_RGB[1]},{DARKPINK_RGB[2]},0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Nails Libni Studio</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Miami, FL. Atención con cita previa." data-en="Nail salon in Miami, FL. By appointment only.">Salón de uñas en Miami, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>2715 SW 37th Ave, Miami, FL 33133</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Nails Libni Studio.</p>')
print("FOOTER done")

# ---------- 19. book-float (URL ya reemplazada en el paso global) ----------
assert 'class="book-float"' in h
print("BOOK-FLOAT ok")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
