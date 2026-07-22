import re
import os
import shutil
import colorsys

SLUG = "yesenia-nails-hialeah"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:160]
    h = h.replace(a, b, n)


# ---------- 1. Proteger el badge Merktop ----------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------- 2. Paleta: rotacion de matiz uniforme (plum-pink #a04a72 -> sage/oliva, HUE_SHIFT=100) ----------
HUE_SHIFT = 100.0


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
BOOKSY_OLD = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
BOOKSY_NEW = 'https://booksy.com/en-us/450151_yesenia_nail-salon_15886_hialeah'
IG_OLD = 'https://www.instagram.com/_lashbloom/'
IG_NEW = 'https://www.instagram.com/yesy_love_nails2814/'
IG_HANDLE_OLD = '@_lashbloom'
IG_HANDLE_NEW = '@yesy_love_nails2814'

assert BOOKSY_OLD in h
h = h.replace(BOOKSY_OLD, BOOKSY_NEW)
assert IG_OLD in h
h = h.replace(IG_OLD, IG_NEW)
assert IG_HANDLE_OLD in h
h = h.replace(IG_HANDLE_OLD, IG_HANDLE_NEW)
print("GLOBALS done")

# ---------- 4. HEAD ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Yesenia Nail Salon · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Yesenia Nail Salon, Hialeah FL: gel manicures, Apres and Poly Gel full sets, Russian mani and reinforced acrylic, plus classic and gel pedicures, with a perfect 5.0 across 20 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Yesenia Nail Salon · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel, Apres and Poly Gel nail sets. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-7.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-7.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Yesenia Nail Salon",
    "description": "Nail salon in Hialeah, FL: gel manicures, Apres and Poly Gel full sets, Russian mani, reinforced acrylic, and classic and gel pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "10410 W Okeechobee Rd, Suite 1104", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33018", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.8683858097143, "longitude": -80.3403661 },
    "sameAs": ["https://booksy.com/en-us/450151_yesenia_nail-salon_15886_hialeah", "https://www.instagram.com/yesy_love_nails2814/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "20", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Gel" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres full set Short/M/L" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure Gel" } },
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Reforzamiento en punta con Poly Gel + Rubber Base" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------- 5. Idioma: negocio EN, esqueleto ya EN default (sin cambios) ----------
mh = re.search(r'<html lang="(\w\w)"', h)
assert mh and mh.group(1) == 'en'
ml = re.search(r"applyLang\(lang === '(\w\w)' \? '\w\w' : '(\w\w)'\)", h)
assert ml and ml.group(2) == 'en'
print("LANG confirmed en/en")

# ---------- 6. PRELOADER + NAV ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">YN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Yesenia Nails</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(143,160,74,0.35)]" />',
    '<img src="assets/raw/bk-10.jpg" alt="Yesenia Nail Salon" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(143,160,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Yesenia <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# ---------- 7. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Salón de uñas" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Nail Salon</p>')
rep('<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Uñas hechas para durar, con un toque personal." data-en="Nails made to last, with a personal touch.">Nails made to last, with a personal touch.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Uñas en gel, acrílico" data-en="Gel, acrylic and Apres">Gel, acrylic and Apres</span><br /><span data-es="y Apres, hechas para " data-en="nails, made to ">nails, made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura en gel, full sets Apres y Poly Gel, russian mani y refuerzo en acrílico, más pedicura clásica y en gel: un menú completo de uñas con un 5.0 perfecto en 20 reseñas de Booksy, hecho con paciencia y precisión en su suite de W Okeechobee Rd, Hialeah." data-en="Gel manicures, Apres and Poly Gel full sets, Russian mani and reinforced acrylic, plus classic and gel pedicures: a full nail menu with a perfect 5.0 across 20 Booksy reviews, done with patience and precision at her W Okeechobee Rd suite in Hialeah.">Manicura en gel, full sets Apres y Poly Gel, russian mani y refuerzo en acrílico, más pedicura clásica y en gel: un menú completo de uñas con un 5.0 perfecto en 20 reseñas de Booksy, hecho con paciencia y precisión en su suite de W Okeechobee Rd, Hialeah.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 20 reseñas en Booksy" data-en="5.0 · 20 reviews on Booksy">5.0 · 20 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-7.jpg" alt="Manicura almendrada con flor rosa pintada a mano, perlas y estrella de mar dorada, en Yesenia Nail Salon" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Apres Full Set</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$65 · Full set" data-en="$65 · Full set">$65 · Full set</p>')
print("HERO done")

# ---------- 8. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="20">20</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Apres</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicura y pedicura" data-en="Manicures & pedicures">Manicures &amp; pedicures</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">22 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W Okeechobee Rd</p></div>')
print("STRIP done")

# ---------- 9. MARQUEE (6 palabras x 4 apariciones) ----------
for old, new in [
    ('Classic Set', 'Manicure Gel'),
    ('Hybrid Set', 'Pedicure Gel'),
    ('Volume Set', 'Apres Full Set'),
    ('Mega Volume', 'Russian Mani'),
    ('Bottom Lashes', 'Poly Gel'),
    ('West Palm Beach, FL', 'Hialeah, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------- 10. LA EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="El suite propio de Yesenia Nail Salon, con silla de pedicura y ambiente rosado en Hialeah" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Detalle de uñas en tono taupe con acento de brillo dorado" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Una sola artista," data-en="One nail artist,">One nail artist,</span><br /><span class="text-shine" data-es="atención al detalle" data-en="endless detail">endless detail</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Yesenia Nail Salon es la suite de una sola artista, Yesenia, dentro de un edificio de suites compartido en W Okeechobee Rd, Hialeah. Cada servicio, desde manicura en gel hasta russian mani y refuerzo en Poly Gel, se hace con paciencia y detalle pintado a mano." data-en="Yesenia Nail Salon is the suite of one nail artist, Yesenia, inside a shared suite building on W Okeechobee Rd in Hialeah. Every set, from gel manicures to Russian mani and reinforced Poly Gel, is done with patience and hand-painted detail.">Yesenia Nail Salon es la suite de una sola artista, Yesenia, dentro de un edificio de suites compartido en W Okeechobee Rd, Hialeah. Cada servicio, desde manicura en gel hasta russian mani y refuerzo en Poly Gel, se hace con paciencia y detalle pintado a mano.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 20 reseñas verificadas en Booksy, y clientas que dicen que nunca falla en entregar un trabajo excelente." data-en="The result: a perfect 5.0 across 20 verified Booksy reviews, and clients who say she never fails to deliver excellent work.">The result: a perfect 5.0 across 20 verified Booksy reviews, and clients who say she never fails to deliver excellent work.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="20">20</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(143,160,74,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-10.jpg" alt="Yesenia Nail Salon" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(143,160,74,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Yesenia · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ---------- 11. METODO ----------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, paso" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="a paso" data-en="by step">by step</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu manicura, pedicura o full set en Booksy con precio claro, y confirmas al instante." data-en="Pick your manicure, pedicure or full set on Booksy with clear pricing, and confirm instantly.">Pick your manicure, pedicure or full set on Booksy with clear pricing, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y sistema" data-en="Shape and system">Shape and system</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elegimos la forma de la uña y el sistema: gel, Apres, Poly Gel o russian mani, según lo que busques." data-en="We choose the nail shape and the system, gel, Apres, Poly Gel or Russian mani, based on what you want.">We choose the nail shape and the system, gel, Apres, Poly Gel or Russian mani, based on what you want.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El trabajo" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Yesenia trabaja con paciencia y precisión, tomándose su tiempo en cada set, del refuerzo al diseño pintado a mano." data-en="Yesenia works with patience and precision, taking her time on every set, from reinforcement to hand-painted design.">Yesenia works with patience and precision, taking her time on every set, from reinforcement to hand-painted design.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El acabado" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un set limpio y terminado, y un salón de uñas del que tus amigas van a preguntar." data-en="You leave with a clean, finished set, and a nail salon your friends will ask about.">You leave with a clean, finished set, and a nail salon your friends will ask about.</p>''')
print("METODO done")

# ---------- 12. SERVICIOS ----------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Yesenia Nail Salon en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Yesenia Nail Salon on Booksy. Booking confirms instantly.">Prices and durations as published by Yesenia Nail Salon on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
BOOKSY = BOOKSY_NEW
NEW_SERVICES = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clásico de todos los días" data-en="Everyday classic">Everyday classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Gel" data-en="Manicure Gel">Manicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura en gel, limpia y duradera, con esmaltado de larga duración. El punto de partida ideal." data-en="A gel manicure, clean and long-lasting, with polish that stays put. The ideal place to start.">A gel manicure, clean and long-lasting, with polish that stays put. The ideal place to start.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">50min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(143,160,74,0.4); box-shadow: 0 18px 50px rgba(50,51,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Apres full set Short/M/L" data-en="Apres full set Short/M/L">Apres full set Short/M/L</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El sistema Apres en el largo que elijas, corto, mediano o largo, ligero y de acabado natural." data-en="The Apres system in the length you choose, short, medium or long, lightweight with a natural finish.">The Apres system in the length you choose, short, medium or long, lightweight with a natural finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Full set" data-en="Full set">Full set</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Spa" data-en="Spa">Spa</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicure Gel" data-en="Pedicure Gel">Pedicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura completa con esmaltado en gel de larga duración, para pies impecables." data-en="A full pedicure with long-lasting gel polish, for flawless feet.">A full pedicure with long-lasting gel polish, for flawless feet.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Refuerzo premium" data-en="Premium reinforcement">Premium reinforcement</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reforzamiento en punta con Poly Gel + Rubber Base" data-en="Reforzamiento en punta con Poly Gel + Rubber Base">Reforzamiento en punta con Poly Gel + Rubber Base</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Refuerzo en la punta con Poly Gel y Rubber Base, para uñas naturales más fuertes y duraderas." data-en="Tip reinforcement with Poly Gel and Rubber Base, for stronger, longer-lasting natural nails.">Tip reinforcement with Poly Gel and Rubber Base, for stronger, longer-lasting natural nails.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h 45min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: pedicura regular, cambio de color, reparación y remoción de uñas, russian mani con rubber base o builder gel, diseño básico, con Swarovski o 3D, y stamping. Menú completo de 22 servicios y disponibilidad en Booksy." data-en="Also available: regular pedicure, color change, nail repair and removal, Russian mani with rubber base or builder gel, basic, Swarovski or 3D nail art, and stamping designs. Full 22-service menu and availability on Booksy.">Also available: regular pedicure, color change, nail repair and removal, Russian mani with rubber base or builder gel, basic, Swarovski or 3D nail art, and stamping designs. Full 22-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 13. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Flores borgoña con animal print" data-en="Burgundy florals with leopard print">Burgundy florals with leopard print</span><img src="assets/raw/bk-8.jpg" alt="Set en tono borgoña con flores pintadas a mano y acentos de animal print, en Yesenia Nail Salon" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Flores rosas y fresas 3D" data-en="Pink florals and 3D strawberries">Pink florals and 3D strawberries</span><img src="assets/raw/bk-5.jpg" alt="Uñas almendradas con flores rosas en 3D y diseño de fresas" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Francesa con perlas y estrella de mar" data-en="French tips with pearls and a starfish">French tips with pearls and a starfish</span><img src="assets/raw/bk-6.jpg" alt="Manicura francesa blanca con detalles de perlas y estrella de mar dorada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Mármol celeste con estrellas" data-en="Sky blue marble with stars">Sky blue marble with stars</span><img src="assets/raw/bk-9.jpg" alt="Uñas almendradas en azul celeste con efecto mármol y pequeñas estrellas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Flor pintada a mano y estrella dorada" data-en="Hand-painted flower and gold starfish">Hand-painted flower and gold starfish</span><img src="assets/raw/bk-7.jpg" alt="Uñas almendradas color nude con flor rosa pintada a mano, perlas y estrella de mar dorada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Francesa en rosa suave" data-en="Soft pink French manicure">Soft pink French manicure</span><img src="assets/raw/bk-10.jpg" alt="Manicura francesa en tono rosa suave y blanco de cerca" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 14. OPINIONES (reales, verbatim con autor) ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 20 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 20 verified reviews on Booksy">5.0 out of 5 · 20 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always attentive and very professional . Her work is beautiful."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mercedes R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesenia was amazing!! She is a perfectionist and her work shows it. She takes her time. I will definitely be booking again."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Cristy B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent service and I loved my nails ❤️"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Heidy P.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/450151_yesenia_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/450151_yesenia_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 20 reseñas en Booksy" data-en="Read all 20 reviews on Booksy">Read all 20 reviews on Booksy</a>')
print("OPINIONES done")

# ---------- 15. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">10410 W Okeechobee Rd, Suite 1104, Hialeah, FL 33018</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=10410+W+Okeechobee+Rd,+Suite+1104,+Hialeah,+FL+33018"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Abierto de lunes a viernes de 9am a 6pm, y sábados de 9am a 3:30pm. Reserva por Booksy con confirmación inmediata." data-en="Open Monday to Friday 9am to 6pm, and Saturday 9am to 3:30pm. Book through Booksy for instant confirmation.">Open Monday to Friday 9am to 6pm, and Saturday 9am to 3:30pm. Book through Booksy for instant confirmation.</p>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los últimos diseños de Yesenia y escribe por DM cualquier duda antes de tu cita." data-en="See Yesenia\'s latest designs and DM any questions before your appointment.">See Yesenia\'s latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Yesenia Nail Salon, 10410 W Okeechobee Rd, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=10410+W+Okeechobee+Rd,+Suite+1104,+Hialeah,+FL+33018&output=embed"')
print("UBICACION done")

# ---------- 16. CTA FINAL ----------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Uñas hechas para durar, con un toque personal." data-en="Nails made to last, with a personal touch.">Nails made to last, with a personal touch.</p>')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu manicura en gel, tu full set Apres, tu russian mani o la pedicura que ya te toca." data-en="Book online in seconds: your gel manicure, Apres full set, Russian mani, or the pedicure you are due for.">Book online in seconds: your gel manicure, Apres full set, Russian mani, or the pedicure you are due for.</p>')
print("CTA FINAL done")

# ---------- 17. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Yesenia Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,240,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-10.jpg" alt="Yesenia Nail Salon" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,240,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Yesenia Nails</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Hialeah, FL. Atención con cita previa." data-en="Nail salon in Hialeah, FL. By appointment only.">Nail salon in Hialeah, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>10410 W Okeechobee Rd, Suite 1104, Hialeah, FL 33018</p>')
assert '<p><a href="https://www.instagram.com/yesy_love_nails2814/" target="_blank" rel="noopener" class="hover:text-[#e8f0be]">Instagram · @yesy_love_nails2814</a></p>' in h
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Yesenia Nail Salon.</p>')
print("FOOTER done")

# ---------- 18. book-float (URL ya reemplazada en el paso global) ----------
assert 'class="book-float"' in h
print("BOOK-FLOAT ok")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))

# ---------- 19. Copiar assets compartidos ----------
shutil.copyfile("templates/assets/tailwind.js", f"output/{SLUG}/assets/tailwind.js")
shutil.copyfile("templates/.assetsignore-template", f"output/{SLUG}/.assetsignore")
print("ASSETS copied")
