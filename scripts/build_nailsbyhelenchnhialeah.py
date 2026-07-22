import re
import os
import shutil
import colorsys

SLUG = "nailsbyhelenchn-hialeah"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
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

# ---------- 2. Paleta: rotacion de matiz (HUE_SHIFT=-24, plum-pink a04a72 -> magenta-orchid) ----------
HUE_SHIFT = -24.0


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
print("PALETTE done ->", shift_hex('a04a72'))

# ---------- 3. Globales: Booksy, Instagram, handle ----------
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1582379_nailsbyhelenchn_nail-salon_15886_hialeah'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG = 'https://www.instagram.com/_lashbloom/'
NEW_IG = 'https://www.instagram.com/nailsbyhelenchn_/'
assert OLD_IG in h
h = h.replace(OLD_IG, NEW_IG)

OLD_HANDLE = '@_lashbloom'
NEW_HANDLE = '@nailsbyhelenchn_'
assert OLD_HANDLE in h
h = h.replace(OLD_HANDLE, NEW_HANDLE)
print("GLOBALS done")

# ---------- 4. HEAD: title, meta, JSON-LD, favicon ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Nails by Helen Chavez · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Nails by Helen Chavez, Hialeah FL: polygel and acrylic sets, spa manicures and pedicures with a perfect 5.0 across 23 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Nails by Helen Chavez · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Polygel, acrylic, spa manicures and pedicures. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-12.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-14.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nails by Helen Chavez",
    "description": "Nail salon in Hialeah, FL: polygel sets, acrylic sets, spa manicures, spa pedicures and gel pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "1630 W 38th Pl", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33012", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.85661619742723, "longitude": -80.31603045482291 },
    "sameAs": ["https://booksy.com/en-us/1582379_nailsbyhelenchn_nail-salon_15886_hialeah", "https://www.instagram.com/nailsbyhelenchn_/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "23", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Polygel set nuevo long" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrilicas set nuevo medium" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicura spa" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicura spa" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------- 5. Idioma: EN por defecto (negocio bilingue, publicado en ingles, sin cambio) ----------
print("LANG skip (EN default matches skeleton)")

# ---------- 6. PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">HC</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Helen Chavez</span>')

# ---------- 7. NAV ----------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,148,0.35)]" />',
    '<img src="assets/raw/bk-14.jpg" alt="Nails by Helen Chavez" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,148,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Helen <span class="text-[color:var(--accent-deep)]">Chavez</span></span>')
print("NAV done")

# ---------- 8. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Salón de uñas" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Uñas con detalle y buena energía." data-en="Nails with detail and good energy.">Nails with detail and good energy.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Polygel y acrílico" data-en="Polygel and acrylic">Polygel and acrylic</span><br /><span data-es="sets, hechos para " data-en="sets, made to ">sets, made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '''data-es="Sets de polygel y acrílico, manicura y pedicura spa, de la mano de Helen Chávez en su propio salón en Hialeah, FL. Un 5.0 perfecto en 23 reseñas de Booksy, con cafecito incluido." data-en="Polygel and acrylic sets, spa manicures and pedicures, by Helen Chavez in her own salon in Hialeah, FL. A perfect 5.0 across 23 Booksy reviews, cafecito included.">Polygel and acrylic sets, spa manicures and pedicures, by Helen Chavez in her own salon in Hialeah, FL. A perfect 5.0 across 23 Booksy reviews, cafecito included.</p>''')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 23 reseñas en Booksy" data-en="5.0 · 23 reviews on Booksy">5.0 · 23 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-13.jpg" alt="Uñas stiletto blancas con puntos de color, terminado de Nails by Helen Chavez" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Polygel Set Long</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$85 · 2h" data-en="$85 · 2h">$85 · 2h</p>')
print("HERO done")

# ---------- 9. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="23">23</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Polygel <span class="text-shine">&amp;</span> Acrylic</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Refills" data-en="Full sets · Refills">Full sets · Refills</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">10 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W 38th Pl</p></div>')
print("STRIP done")

# ---------- 10. MARQUEE (x4 cada palabra) ----------
for old, new in [
    ('Classic Set', 'Polygel Set'),
    ('Hybrid Set', 'Acrylic Set'),
    ('Volume Set', 'Spa Manicure'),
    ('Mega Volume', 'Spa Pedicure'),
    ('Bottom Lashes', 'Gel Pedicure'),
    ('West Palm Beach, FL', 'Hialeah, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------- 11. EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Uñas nude con diseño floral blanco y acentos dorados" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Uñas blancas con francesa azul y diseño floral rosa" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un ambiente" data-en="A place">A place</span><br /><span class="text-shine" data-es="para relajarte y brillar" data-en="to unwind and shine">to unwind and shine</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '''data-es="Nails by Helen Chavez es el salón de Helen, en Hialeah, FL. Sus clientas destacan lo detallista que es, la buena energía del ambiente y hasta el cafecito que sirve durante la cita." data-en="Nails by Helen Chavez is Helen's salon in Hialeah, FL. Her clients highlight how detailed she is, the good energy of the space, and even the cafecito she serves during your visit.">Nails by Helen Chavez is Helen's salon in Hialeah, FL. Her clients highlight how detailed she is, the good energy of the space, and even the cafecito she serves during your visit.</p>''')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 23 reseñas verificadas en Booksy, y clientas que dicen estar siempre encantadas con el resultado." data-en="The result: a perfect 5.0 across 23 verified Booksy reviews, and clients who say they are always thrilled with the result.">The result: a perfect 5.0 across 23 verified Booksy reviews, and clients who say they are always thrilled with the result.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="23">23</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,148,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-14.jpg" alt="Nails by Helen Chavez" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,148,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Helen · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ---------- 12. METODO ----------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, uña" data-en="Your visit, nail">Your visit, nail</span> <span class="text-shine" data-es="por uña" data-en="by nail">by nail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Elige el sistema" data-en="Choose the system">Choose the system</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Polygel o acrílico, largo o medium: Helen te guía a la opción que mejor le queda a tu uña natural." data-en="Polygel or acrylic, long or medium: Helen guides you to the option that best suits your natural nail.">Polygel or acrylic, long or medium: Helen guides you to the option that best suits your natural nail.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Cafecito y detalle" data-en="Cafecito and detail">Cafecito and detail</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Con cafecito en mano, Helen trabaja con calma, hasta 2h de aplicación según el set elegido." data-en="Cafecito in hand, Helen works calmly, up to 2h of application depending on the set you choose.">Cafecito in hand, Helen works calmly, up to 2h of application depending on the set you choose.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu set terminado y el refill ya agendado para cuando lo necesites." data-en="You leave with your finished set and the refill already booked for when you need it.">You leave with your finished set and the refill already booked for when you need it.</p>''')
print("METODO done")

# ---------- 13. SERVICIOS ----------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Nails by Helen Chavez en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Nails by Helen Chavez on Booksy. Booking confirms instantly.">Prices and durations as published by Nails by Helen Chavez on Booksy. Booking confirms instantly.</p>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manos" data-en="Hands">Hands</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Spa" data-en="Spa Manicure">Spa Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura completa con tratamiento spa para manos suaves y uñas impecables." data-en="Full manicure with a spa treatment for soft hands and flawless nails.">Full manicure with a spa treatment for soft hands and flawless nails.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1582379_nailsbyhelenchn_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,148,0.4); box-shadow: 0 18px 50px rgba(51,34,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Polygel Set Long" data-en="Polygel Set Long">Polygel Set Long</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El sistema polygel de Nails by Helen Chavez en largo: ligero, resistente y con acabado impecable." data-en="Nails by Helen Chavez polygel system in a long length: lightweight, durable and with a flawless finish.">Nails by Helen Chavez polygel system in a long length: lightweight, durable and with a flawless finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="https://booksy.com/en-us/1582379_nailsbyhelenchn_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies" data-en="Feet">Feet</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicura Spa" data-en="Spa Pedicure">Spa Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura completa con tratamiento spa, para pies impecables." data-en="Full pedicure with a spa treatment, for flawless feet.">Full pedicure with a spa treatment, for flawless feet.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1582379_nailsbyhelenchn_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Acrílico" data-en="Acrylic">Acrylic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Acrílicas Set Medium" data-en="Acrylic Set Medium">Acrylic Set Medium</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set nuevo de acrílico en largo medium, resistente y con la forma que elijas." data-en="New acrylic set in a medium length, durable and in the shape you choose.">New acrylic set in a medium length, durable and in the shape you choose.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 35min</p></div>
            <a href="https://booksy.com/en-us/1582379_nailsbyhelenchn_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: parafina, pedicure regular, pedicure gel, refill de polygel y refill de acrílicas. Menú completo de 10 servicios y disponibilidad en Booksy." data-en="Also available: paraffin, regular pedicure, gel pedicure, polygel refill and acrylic refill. Full 10-service menu and availability on Booksy.">Also available: paraffin, regular pedicure, gel pedicure, polygel refill and acrylic refill. Full 10-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 14. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail work">nail work</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Flor blanca con joyas doradas" data-en="White flower with gold jewelry">White flower with gold jewelry</span><img src="assets/raw/bk-12.jpg" alt="Uñas nude con diseño de flor blanca y joyas doradas, terminado de Nails by Helen Chavez" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Rojo clásico brillante" data-en="Classic glossy red">Classic glossy red</span><img src="assets/raw/bk-11.jpg" alt="Uñas almendra en rojo clásico brillante, terminado de Nails by Helen Chavez" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Nude con arte de corazón" data-en="Nude with heart nail art">Nude with heart nail art</span><img src="assets/raw/bk-5.jpg" alt="Uñas nude stiletto con diseño de corazón en el dedo anular" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Flor y estrella dorada" data-en="Flower and gold star accent">Flower and gold star accent</span><img src="assets/raw/bk-6.jpg" alt="Uñas nude con diseño de flor y estrella dorada, anillos incluidos" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Concha dorada sobre nude" data-en="Gold shell accent on nude">Gold shell accent on nude</span><img src="assets/raw/bk-8.jpg" alt="Uñas nude con acentos de concha dorada 3D" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Pedicura con punta blanca" data-en="Pedicure with white tip">Pedicure with white tip</span><img src="assets/raw/bk-4.jpg" alt="Pedicura en tono marron con punta blanca en el dedo gordo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 15. OPINIONES ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 23 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 23 verified reviews on Booksy">5.0 out of 5 · 23 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Wonderful experience. Love the ambience and especially the cafecito. Helen is very detailed, and my nails look fantastic. Thank you."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ann I.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Siempre encantada con el resultado."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yailyn L.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Helen for me and my nails have been a blessing! Professional, caring, attentive to details. Makes the best cafecito. Make your appointment today!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lyn A.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1582379_nailsbyhelenchn_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1582379_nailsbyhelenchn_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 23 reseñas en Booksy" data-en="Read all 23 reviews on Booksy">Read all 23 reviews on Booksy</a>')
print("OPINIONES done")

# ---------- 16. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1630 W 38th Pl (Mis Fancy Suites), Hialeah, FL 33012</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=1630+W+38th+Pl,+Hialeah,+FL+33012"')
rep("data-es=\"Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita.\" data-en=\"See Yesi's latest sets and DM any questions before your appointment.\">See Yesi's latest sets and DM any questions before your appointment.</p>",
    "data-es=\"Mira los sets más recientes de Helen y escribe por DM cualquier duda antes de tu cita.\" data-en=\"See Helen's latest sets and DM any questions before your appointment.\">See Helen's latest sets and DM any questions before your appointment.</p>")
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Nails by Helen Chavez, 1630 W 38th Pl, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=1630+W+38th+Pl,+Hialeah,+FL+33012&output=embed"')
print("UBICACION done")

# ---------- 17. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Uñas con detalle y buena energía." data-en="Nails with detail and good energy.">Nails with detail and good energy.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu polygel, tu acrílico o la spa que ya te toca." data-en="Book online in seconds: your polygel set, your acrylic set, or the spa treatment you are due for.">Book online in seconds: your polygel set, your acrylic set, or the spa treatment you are due for.</p>')
print("CTA FINAL done")

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Helen Chavez</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,235,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-14.jpg" alt="Nails by Helen Chavez" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,235,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Helen Chavez</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Hialeah, FL. Atención con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Nail salon in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>1630 W 38th Pl, Hialeah, FL 33012</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Nails by Helen Chavez.</p>')
print("FOOTER done")

# ---------- 19. book-float (URL ya reemplazada en el paso global) ----------
assert 'class="book-float"' in h
print("BOOK-FLOAT ok")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
