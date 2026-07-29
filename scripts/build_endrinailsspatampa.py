import re
import os
import shutil
import colorsys

SLUG = "endri-nails-spa-tampa"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
if not os.path.exists(f"output/{SLUG}/assets/tailwind.js"):
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

# ---------- 2. Paleta: rotacion de matiz (HUE_SHIFT=177, plum-pink a04a72 -> emerald/sage) ----------
HUE_SHIFT = 177.0


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
print("PALETTE done -> accent-deep", shift_hex('a04a72'), "accent-mid", shift_hex('c47a9c'))

# ---------- 3. Globales: Booksy, Instagram, handle ----------
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1136389_endri-nails-spa_nail-salon_15761_tampa'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG = 'https://www.instagram.com/_lashbloom/'
NEW_IG = 'https://www.instagram.com/endri.nails.spa/'
assert OLD_IG in h
h = h.replace(OLD_IG, NEW_IG)

OLD_HANDLE = '@_lashbloom'
NEW_HANDLE = '@endri.nails.spa'
assert OLD_HANDLE in h
h = h.replace(OLD_HANDLE, NEW_HANDLE)
print("GLOBALS done")

# ---------- 4. HEAD: title, meta, JSON-LD, favicon ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Endri Nails Spa · Nail Salon in Tampa, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Endri Nails Spa, Tampa FL: Russian manicure, spa gel, deluxe pedicures and custom nail art with a perfect 5.0 across 35 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Endri Nails Spa · Nail Salon in Tampa, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Russian manicure, spa gel and deluxe pedicures. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-7.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-6.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Endri Nails Spa",
    "description": "Nail salon and spa in Tampa, FL: Russian manicure, spa gel, deluxe pedicures and custom nail art.",
    "address": { "@type": "PostalAddress", "streetAddress": "4025 W Waters Ave #114", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33614", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.0258526, "longitude": -82.5118645 },
    "sameAs": ["https://booksy.com/en-us/1136389_endri-nails-spa_nail-salon_15761_tampa", "https://www.instagram.com/endri.nails.spa/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "35", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "38", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic Gel Manicure" } },
      { "@type": "Offer", "price": "48", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Russian Manicure - Spa Rubber Base" } },
      { "@type": "Offer", "price": "71", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Deluxe Spa Pedicure" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Soft Gel Extensions" } }
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
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">EN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Endri Nails</span>')

# ---------- 7. NAV ----------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,116,0.35)]" />',
    '<img src="assets/raw/bk-6.jpg" alt="Endri Nails Spa" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,116,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Endri <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# ---------- 8. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tampa, FL · Nail Spa" data-en="Tampa, FL · Nail Spa">Tampa, FL · Nail Spa</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Uñas cuidadas como un ritual." data-en="Nails cared for like a ritual.">Uñas cuidadas como un ritual.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicura rusa, spa" data-en="Russian manicure, spa">Manicura rusa, spa</span><br /><span data-es="y diseños hechos para " data-en="and designs made to ">y diseños hechos para </span><span class="text-shine" data-es="durar" data-en="last">durar</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '''data-es="Manicura rusa, gel spa, pedicura de lujo y diseños de uñas personalizados, de la mano de Endrina Rincon en su salón de Tampa, FL. Un 5.0 perfecto en 35 reseñas de Booksy." data-en="Russian manicure, spa gel, deluxe pedicures and custom nail art, by Endrina Rincon in her Tampa, FL salon. A perfect 5.0 across 35 Booksy reviews.">Russian manicure, spa gel, deluxe pedicures and custom nail art, by Endrina Rincon in her Tampa, FL salon. A perfect 5.0 across 35 Booksy reviews.</p>''')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 35 reseñas en Booksy" data-en="5.0 · 35 reviews on Booksy">5.0 · 35 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-7.jpg" alt="Pedicura spa con los pies descansando sobre piel blanca suave, ambiente de Endri Nails Spa" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Deluxe Spa Pedicure</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$71 · 1h 30min" data-en="$71 · 1h 30min">$71 · 1h 30min</p>')
print("HERO done")

# ---------- 9. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="35">35</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Manicura <span class="text-shine">&amp;</span> Spa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicios completos" data-en="Full services">Servicios completos</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">26 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Menú completo en Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W Waters Ave</p></div>')
print("STRIP done")

# ---------- 10. MARQUEE (x4 cada palabra) ----------
for old, new in [
    ('Classic Set', 'Manicura Rusa'),
    ('Hybrid Set', 'Spa Pedicure'),
    ('Volume Set', 'Builder Gel'),
    ('Mega Volume', 'Nail Art'),
    ('Bottom Lashes', 'Cuidado Spa'),
    ('West Palm Beach, FL', 'Tampa, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------- 11. EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Endrina aplicando una manicura con atención al detalle en Endri Nails Spa" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-11.jpg" alt="Manos relajadas con anillos y manicura nude rosa en Endri Nails Spa" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un trabajo" data-en="Work">Un trabajo</span><br /><span class="text-shine" data-es="detallista y profesional" data-en="that is detailed and professional">detallista y profesional</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '''data-es="Endri Nails Spa es el salón de Endrina Rincon en Tampa, FL. Sus clientas destacan lo detallista y profesional que es en cada servicio, desde la manicura rusa hasta la pedicura spa, en un ambiente cómodo con atención de primera." data-en="Endri Nails Spa is Endrina Rincon's salon in Tampa, FL. Her clients highlight how detail-oriented and professional she is in every service, from Russian manicures to spa pedicures, in a comfortable space with top-notch attention.">Endri Nails Spa is Endrina Rincon's salon in Tampa, FL. Her clients highlight how detail-oriented and professional she is in every service, from Russian manicures to spa pedicures, in a comfortable space with top-notch attention.</p>''')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 35 reseñas verificadas en Booksy, y clientas que la recomiendan sin dudarlo." data-en="The result: a perfect 5.0 across 35 verified Booksy reviews, and clients who recommend her without hesitation.">The result: a perfect 5.0 across 35 verified Booksy reviews, and clients who recommend her without hesitation.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="35">35</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,116,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Endrina Rincon, dueña de Endri Nails Spa" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,116,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Endrina · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ---------- 12. METODO ----------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, uña" data-en="Your visit, nail">Tu cita, uña</span> <span class="text-shine" data-es="por uña" data-en="by nail">por uña</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Elige tu servicio" data-en="Choose your service">Elige tu servicio</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Manicura rusa, gel spa, pedicura de lujo o diseños personalizados: Endrina te ayuda a elegir según lo que buscas." data-en="Russian manicure, spa gel, deluxe pedicure or custom nail art: Endrina helps you choose based on what you want.">Manicura rusa, gel spa, pedicura de lujo o diseños personalizados: Endrina te ayuda a elegir según lo que buscas.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Trabajo detallista" data-en="Detailed work">Trabajo detallista</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Endrina se toma su tiempo para perfeccionar cada uña, con un ambiente cómodo y una atención de primera." data-en="Endrina takes her time to perfect every nail, in a comfortable space with top-notch attention.">Endrina se toma su tiempo para perfeccionar cada uña, con un ambiente cómodo y una atención de primera.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">Salida</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con uñas hermosas y duraderas, listas para lucir." data-en="You leave with beautiful, long-lasting nails, ready to show off.">Sales con uñas hermosas y duraderas, listas para lucir.</p>''')
print("METODO done")

# ---------- 13. SERVICIOS ----------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Endri Nails Spa en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Endri Nails Spa on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Endri Nails Spa en Booksy. Reserva con confirmación inmediata.</p>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clásico" data-en="Classic">Clásico</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Classic Gel Manicure" data-en="Classic Gel Manicure">Classic Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura en gel clásica con cuidado spa completo de manos." data-en="A classic gel manicure with full spa hand care.">Manicura en gel clásica con cuidado spa completo de manos.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$38</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/1136389_endri-nails-spa_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(74,160,116,0.4); box-shadow: 0 18px 50px rgba(45,51,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Favorito del salón</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Russian Manicure – Spa Rubber Base" data-en="Russian Manicure - Spa Rubber Base">Russian Manicure – Spa Rubber Base</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura rusa de precisión sobre una base rubber, con acabado impecable." data-en="Precision Russian manicure over a rubber base, with a flawless finish.">Manicura rusa de precisión sobre una base rubber, con acabado impecable.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$48</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://booksy.com/en-us/1136389_endri-nails-spa_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura de lujo" data-en="Deluxe pedicure">Pedicura de lujo</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Deluxe Spa Pedicure" data-en="Deluxe Spa Pedicure">Deluxe Spa Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura spa con toallas calientes y cuidado completo de pies." data-en="Spa pedicure with hot towels and full foot care.">Pedicura spa con toallas calientes y cuidado completo de pies.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$71</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://booksy.com/en-us/1136389_endri-nails-spa_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extensiones" data-en="Extensions">Extensiones</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Soft Gel Extensions – Apres Style" data-en="Soft Gel Extensions - Apres Style">Soft Gel Extensions – Apres Style</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sistema de extensiones en gel suave, estilo Apres, con acabado natural." data-en="Soft gel extension system, Apres style, with a natural finish.">Sistema de extensiones en gel suave, estilo Apres, con acabado natural.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://booksy.com/en-us/1136389_endri-nails-spa_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: pedicura clásica en gel, manicura + pedicura combo, retiro de gel, diseños personalizados y 22 servicios más. Menú completo de 26 servicios y disponibilidad en Booksy." data-en="Also available: classic gel pedicure, manicure + pedicure combos, gel soak-off, custom nail designs and 22 more services. Full 26-service menu and availability on Booksy.">También: pedicura clásica en gel, manicura + pedicura combo, retiro de gel, diseños personalizados y 22 servicios más. Menú completo de 26 servicios y disponibilidad en Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 14. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Trabajo</span> <span class="text-shine" data-es="real" data-en="nail work">real</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Ojo de gato con brillante" data-en="Cat-eye with rhinestone">Ojo de gato con brillante</span><img src="assets/raw/bk-8.jpg" alt="Uñas negras estilo ojo de gato con acento de piedra brillante, terminado de Endri Nails Spa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Pedicura morada con flor" data-en="Purple pedicure with flower">Pedicura morada con flor</span><img src="assets/raw/bk-4.jpg" alt="Pedicura morada con diseño floral blanco en el dedo gordo, terminado de Endri Nails Spa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Rojo con diseño de corazón" data-en="Red with heart design">Rojo con diseño de corazón</span><img src="assets/raw/bk-12.jpg" alt="Manicura roja con pequeño diseño de corazón, terminado de Endri Nails Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Gel color lila" data-en="Lilac gel">Gel color lila</span><img src="assets/raw/bk-3.jpg" alt="Manicura en gel color lila y lavanda, terminado de Endri Nails Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Floral en nude" data-en="Floral on nude">Floral en nude</span><img src="assets/raw/bk-13.jpg" alt="Uñas nude con diseño floral blanco, terminado de Endri Nails Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Rosa clásico" data-en="Classic pink">Rosa clásico</span><img src="assets/raw/bk-16.jpg" alt="Manicura corta en rosa clásico, terminado de Endri Nails Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 15. OPINIONES ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 35 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 35 verified reviews on Booksy">5.0 de 5 · 35 reseñas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">“Excelente técnico de uñas 💅✨ Súper profesional, detallista y con un trabajo impecable. Se nota la pasión en cada diseño y el cuidado en cada paso. Además, el ambiente es cómodo y la atención es de primera. Mis uñas quedaron hermosas y duraderas. ¡Totalmente recomendado!”</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yoleima H.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Endri..is a very professional nail technician: I highly recommend her. I had been with my previous technician for three years, but after moving to Tampa, choosing Endri was the best decision. She is very professional, and I'm very happy with my nails. 💕"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">NIlka P.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very professional and clean. Excellent service."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Patrece S.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1136389_endri-nails-spa_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1136389_endri-nails-spa_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 35 reseñas en Booksy" data-en="Read all 35 reviews on Booksy">Leer las 35 reseñas en Booksy</a>')
print("OPINIONES done")

# ---------- 16. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Tampa</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">4025 W Waters Ave #114, Tampa, FL 33614</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=4025+W+Waters+Ave+%23114,+Tampa,+FL+33614"')
rep("data-es=\"Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita.\" data-en=\"See Yesi's latest sets and DM any questions before your appointment.\">See Yesi's latest sets and DM any questions before your appointment.</p>",
    "data-es=\"Mira los diseños más recientes de Endrina y escribe por DM cualquier duda antes de tu cita.\" data-en=\"See Endrina's latest designs and DM any questions before your appointment.\">Mira los diseños más recientes de Endrina y escribe por DM cualquier duda antes de tu cita.</p>")
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Endri Nails Spa, 4025 W Waters Ave #114, Tampa FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=4025+W+Waters+Ave+%23114,+Tampa,+FL+33614&output=embed"')
print("UBICACION done")

# ---------- 17. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Uñas cuidadas como un ritual." data-en="Nails cared for like a ritual.">Uñas cuidadas como un ritual.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Tu próxima cita</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    "data-es=\"Reserva en línea en segundos: tu manicura rusa, tu pedicura spa o el diseño que ya quieres.\" data-en=\"Book online in seconds: your Russian manicure, your spa pedicure, or the nail art you've been wanting.\">Reserva en línea en segundos: tu manicura rusa, tu pedicura spa o el diseño que ya quieres.</p>")
print("CTA FINAL done")

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Endri Nails Spa</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,212,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Endri Nails Spa" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,212,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Endri Nails Spa</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Tampa, FL. Atención con cita previa." data-en="Nail salon in Tampa, FL. By appointment only.">Salón de uñas en Tampa, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>4025 W Waters Ave #114, Tampa, FL 33614</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Endri Nails Spa.</p>')
print("FOOTER done")

# ---------- 19. book-float (URL ya reemplazada en el paso global) ----------
assert 'class="book-float"' in h
print("BOOK-FLOAT ok")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
