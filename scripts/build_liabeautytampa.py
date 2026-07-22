import re
import os
import shutil
import colorsys

SLUG = "lia-beauty-tampa"
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

# ---------- 2. Paleta: rotacion de matiz (plum-pink #a04a72 -> verde fresco #4aa04d) ----------
HUE_SHIFT = 150.0


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
print("PALETTE done")

# ---------- 3. Globales: Booksy, Instagram ----------
BOOKSY_OLD = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
BOOKSY_NEW = 'https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa'
IG_OLD = 'https://www.instagram.com/_lashbloom/'
IG_NEW = 'https://www.instagram.com/lianetnailstudio/'
IG_HANDLE_OLD = '@_lashbloom'
IG_HANDLE_NEW = '@lianetnailstudio'

assert BOOKSY_OLD in h
h = h.replace(BOOKSY_OLD, BOOKSY_NEW)
assert IG_OLD in h
h = h.replace(IG_OLD, IG_NEW)
assert IG_HANDLE_OLD in h
h = h.replace(IG_HANDLE_OLD, IG_HANDLE_NEW)
print("GLOBALS done")

# ---------- 4. HEAD ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Lia Beauty · Nail Salon in Tampa, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Lia Beauty, Tampa FL: Gel X, pink and white, acrylic full sets, manicures and pedicures by Lianet May, a perfect 5.0 across 43 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Lia Beauty · Nail Salon in Tampa, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel X, pink and white, full sets and pedicures. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-9.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Lia Beauty",
    "description": "Nail salon in Tampa, FL: Gel X, pink and white, acrylic full sets, manicures, pedicures and nail art by Lianet May and Daile.",
    "address": { "@type": "PostalAddress", "streetAddress": "1420 W Water Ave, Suite 104", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33604", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.01481, "longitude": -82.4851 },
    "sameAs": ["https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa", "https://www.instagram.com/lianetnailstudio/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "43", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "17:45" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "08:30", "closes": "16:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apress or Gel X" } },
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Extra Long Full Set" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Fill Pink and White Long" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Volcano Pedicure" } }
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
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Lia Beauty</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,77,0.35)]" />',
    '<img src="assets/raw/bk-1.jpg" alt="Lia Beauty" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,77,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lia <span class="text-[color:var(--accent-deep)]">Beauty</span></span>')
print("NAV done")

# ---------- 7. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tampa, FL · Salon de Unas" data-en="Tampa, FL · Nail Salon">Tampa, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas hechas con carino, por Lianet." data-en="Nails made with heart, by Lianet.">Nails made with heart, by Lianet.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Gel X, rosa y blanco" data-en="Gel X, pink and white">Gel X, pink and white</span><br /><span data-es="y nail art, hechos para " data-en="and nail art, made to ">and nail art, made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Gel X, rosa y blanco, sets completos de acrilico, manicura, pedicura y nail art, hechos con precision por Lianet May y Daile en un estudio luminoso de Tampa. Un 5.0 perfecto en 43 resenas de Booksy, y clientas como Bernice que llevan mas de siete anos confiando en Lianet." data-en="Gel X, pink and white, acrylic full sets, manicures, pedicures and nail art, done with precision by Lianet May and Daile inside a bright Tampa studio. A perfect 5.0 across 43 Booksy reviews, and clients like Bernice who have trusted Lianet for over seven years.">Gel X, pink and white, acrylic full sets, manicures, pedicures and nail art, done with precision by Lianet May and Daile inside a bright Tampa studio. A perfect 5.0 across 43 Booksy reviews, and clients like Bernice who have trusted Lianet for over seven years.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 43 reseñas en Booksy" data-en="5.0 · 43 reviews on Booksy">5.0 · 43 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-9.jpg" alt="Light pink French manicure with a hand painted butterfly accent nail at Lia Beauty" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Apress or Gel X</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$60 · 1h 30min" data-en="$60 · 1h 30min">$60 · 1h 30min</p>')
print("HERO done")

# ---------- 8. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="43">43</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Extensions <span class="text-shine">&amp;</span> Art</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel X · Rosa y blanco" data-en="Gel X · Pink and white">Gel X · Pink and white</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">30 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W Water Ave</p></div>')
print("STRIP done")

# ---------- 9. MARQUEE (6 palabras x 4 apariciones) ----------
for old, new in [
    ('Classic Set', 'Gel X'),
    ('Hybrid Set', 'Pink &amp; White'),
    ('Volume Set', 'Acrylic Full Set'),
    ('Mega Volume', 'Nail Art'),
    ('Bottom Lashes', 'Volcano Pedicure'),
    ('West Palm Beach, FL', 'Tampa, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------- 10. LA EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Long coffin shaped French tip nails with a crystal butterfly accent at Lia Beauty" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="White and pink abstract nail art with a gold foil accent at Lia Beauty" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Dos artistas," data-en="Two artists,">Two artists,</span><br /><span class="text-shine" data-es="un 5.0 perfecto" data-en="a perfect 5.0">a perfect 5.0</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Lia Beauty es el estudio de unas de Lianet May, junto a Daile, en un espacio luminoso de W Water Ave en Tampa. De Gel X y rosa y blanco a sets completos de acrilico y nail art, cada diseno se hace con la misma atencion cercana al detalle." data-en="Lia Beauty is Lianet May nail studio in Tampa, working alongside Daile inside a bright space on W Water Ave. From Gel X and pink and white to full acrylic sets and nail art, every design gets the same close attention to detail.">Lia Beauty is Lianet May nail studio in Tampa, working alongside Daile inside a bright space on W Water Ave. From Gel X and pink and white to full acrylic sets and nail art, every design gets the same close attention to detail.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 43 resenas verificadas en Booksy, y clientas como Bernice que llevan mas de siete anos confiando en Lianet para sus manicuras y pedicuras." data-en="The result: a perfect 5.0 across 43 verified Booksy reviews, and clients like Bernice who have trusted Lianet with their manicures and pedicures for over seven years.">The result: a perfect 5.0 across 43 verified Booksy reviews, and clients like Bernice who have trusted Lianet with their manicures and pedicures for over seven years.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="43">43</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,77,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Lia Beauty" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,160,77,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Lianet · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ---------- 11. METODO ----------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, unas" data-en="Your visit, nails">Your visit, nails</span> <span class="text-shine" data-es="a tu gusto" data-en="your way">your way</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio claro, y confirmas al instante." data-en="Pick your service on Booksy with clear pricing, and confirm instantly.">Pick your service on Booksy with clear pricing, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y estilo" data-en="Shape and style">Shape and style</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Hablamos de forma, largo y acabado, desde una manicura en gel clasica hasta Gel X, rosa y blanco o un diseno de nail art a tu gusto." data-en="We talk shape, length and finish, from a classic gel manicure to Gel X, pink and white or a custom nail art design.">We talk shape, length and finish, from a classic gel manicure to Gel X, pink and white or a custom nail art design.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El trabajo" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Lianet o Daile trabajan con cuidado y precision, desde sets completos de acrilico hasta rubber base y pedicura en gel." data-en="Lianet or Daile work with care and precision, from acrylic full sets to rubber base and gel pedicures.">Lianet or Daile work with care and precision, from acrylic full sets to rubber base and gel pedicures.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El acabado" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un set limpio y terminado, listo para lucirlo." data-en="You leave with a clean, finished set, ready to show off.">You leave with a clean, finished set, ready to show off.</p>''')
print("METODO done")

# ---------- 12. SERVICIOS ----------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Lia Beauty en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lia Beauty on Booksy. Booking confirms instantly.">Prices and durations as published by Lia Beauty on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema de extension" data-en="Extension system">Extension system</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Apress or Gel X</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El sistema Apress o Gel X en el largo que prefieras, ligero y con un acabado impecable de larga duracion." data-en="The Apress or Gel X system in a flattering length, lightweight with a flawless, long-lasting finish.">The Apress or Gel X system in a flattering length, lightweight with a flawless, long-lasting finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(74,160,77,0.4); box-shadow: 0 18px 50px rgba(36,51,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Largo insignia" data-en="Signature length">Signature length</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Extra Long Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un set completo de acrilico en largo extra, la forma mas dramatica y llamativa del menu." data-en="A full acrylic set in extra long length, the boldest, most dramatic shape on the menu.">A full acrylic set in extra long length, the boldest, most dramatic shape on the menu.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especialidad rosa y blanco" data-en="Pink and white specialty">Pink and white specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Fill Pink and White Long</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El clasico relleno rosa y blanco en largo, un look limpio y esculpido que crece de forma impecable." data-en="The classic pink and white fill in a long length, a clean, sculpted look that grows out beautifully.">The classic pink and white fill in a long length, a clean, sculpted look that grows out beautifully.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 15min</p></div>
            <a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura spa" data-en="Spa pedicure">Spa pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Volcano Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una pedicura spa mineral y calida que suaviza y relaja los pies cansados de punta a punta." data-en="A warming, mineral rich spa pedicure that softens and relaxes tired feet from heel to toe.">A warming, mineral rich spa pedicure that softens and relaxes tired feet from heel to toe.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Extensiones, rosa y blanco, manicura, pedicura y nail art, todo bajo un mismo techo en Lia Beauty. Menu completo de 30 servicios y disponibilidad en Booksy." data-en="Extensions, pink and white, manicures, pedicures and nail art, all under one roof at Lia Beauty. Full 30-service menu and availability on Booksy.">Extensions, pink and white, manicures, pedicures and nail art, all under one roof at Lia Beauty. Full 30-service menu and availability on Booksy.</span></p>')

# ---------- 12b. Menu completo por categoria (menu grande: 30 servicios reales) ----------
CATEGORIES = [
    ("Extensions &amp; Fills", "Extensiones y rellenos", [
        ("Apress or Gel X", 60, "1h 30min"),
        ("Refill Short", 50, None),
        ("Refill medium", 55, None),
        ("Refill long", 60, "1h 30min"),
        ("Polygel fill short", 55, None),
        ("Polygel fill medium", 60, "1h 30min"),
        ("Polygel fill long", 65, None),
        ("Short Acrílic Full Set", 60, "1h 30min"),
        ("Medium Full Set", 65, None),
        ("Long Full Set", 75, "2h 30min"),
        ("Extra Long Full Set", 85, "2h 30min"),
    ]),
    ("Pink &amp; White + Extras", "Rosa y blanco + extras", [
        ("Fills pink and white short", 65, None),
        ("Fill Pink and White Medium", 70, "2h"),
        ("Fill Pink and White Long", 80, "2h 15min"),
        ("Free nail art design", 5, None),
        ("New Nail (each) short, medium or long", 5, None),
        ("Encapsulated each", 5, None),
        ("Rubber Base", 45, "1h"),
        ("Paraffin", 5, None),
    ]),
    ("Manicure", "Manicura", [
        ("Gel Manicure", 30, "45min"),
        ("Regular Manicure", 20, "35min"),
        ("Gel color change", 25, "15min"),
        ("Regular polish change", 8, "15min"),
        ("Soak off", 10, "30min"),
    ]),
    ("Pedicure", "Pedicura", [
        ("Regular Pedicure", 35, "1h"),
        ("Gel pedicure", 45, "1h"),
        ("Gel polish change", 20, "35min"),
        ("Pedicure Jelly Spa", 50, None),
        ("Volcano Pedicure", 65, None),
        ("Men’s pedicure", 55, None),
    ]),
]

cat_blocks = []
for i, (name_en, name_es, rows) in enumerate(CATEGORIES):
    row_html = []
    for svc_name, price, duration in rows:
        price_txt = f"${price}" + (f" · {duration}" if duration else "")
        row_html.append(
            f'<div class="flex items-center justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)] text-sm"><span class="font-light text-[color:var(--ink-60)]">{svc_name}</span><span class="font-medium shrink-0 ml-3">{price_txt}</span></div>'
        )
    delay = 0 if i % 2 == 0 else 90
    cat_blocks.append(f'''        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:{delay}ms">
          <h3 class="font-display text-xl mb-4" data-es="{name_es}" data-en="{name_en}">{name_en}</h3>
          <div class="space-y-0.5">
{chr(10).join(row_html)}
          </div>
        </div>''')

MENU_FULL = '''<p class="reveal text-center text-sm text-[color:var(--ink-60)] font-light mt-16 mb-8" data-es="El menú completo, por categoría" data-en="The full menu, by category">The full menu, by category</p>
      <div class="grid sm:grid-cols-2 gap-5 mt-14">
''' + '\n'.join(cat_blocks) + '''
      </div>
      '''

marker = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Extensiones, rosa y blanco, manicura, pedicura y nail art, todo bajo un mismo techo en Lia Beauty. Menu completo de 30 servicios y disponibilidad en Booksy." data-en="Extensions, pink and white, manicures, pedicures and nail art, all under one roof at Lia Beauty. Full 30-service menu and availability on Booksy.">Extensions, pink and white, manicures, pedicures and nail art, all under one roof at Lia Beauty. Full 30-service menu and availability on Booksy.</span></p>'
assert marker in h
h = h.replace(marker, marker + '\n      ' + MENU_FULL, 1)
print("SERVICIOS done")

# ---------- 13. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Francesa rosa con mariposa" data-en="Pink French with a butterfly accent">Pink French with a butterfly accent</span><img src="assets/raw/bk-9.jpg" alt="Light pink French manicure with a hand painted butterfly accent nail on both hands at Lia Beauty" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Marmol rosa" data-en="Pink marble nails">Pink marble nails</span><img src="assets/raw/bk-5.jpg" alt="Soft pink marble nail art with a glossy finish at Lia Beauty" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Francesa roja audaz" data-en="Bold red-orange French">Bold red-orange French</span><img src="assets/raw/bk-4.jpg" alt="Long square nails with a bold red-orange French tip and crystal accents" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Francesa menta con margaritas" data-en="Mint French with daisies">Mint French with daisies</span><img src="assets/raw/bk-8.jpg" alt="Mint green French tip nails with hand painted daisy nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Unas nude con Mickey y Minnie" data-en="Nude nails, Mickey and Minnie art">Nude nails, Mickey and Minnie art</span><img src="assets/raw/bk-10.jpg" alt="Nude almond shaped nails with hand painted Mickey and Minnie Mouse nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Morado brillante con glitter" data-en="Glossy purple with glitter accent">Glossy purple with glitter accent</span><img src="assets/raw/bk-7.jpg" alt="Glossy deep purple nails with a glitter accent nail and a diamond ring" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 14. OPINIONES (reales, con autor) ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 43 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 43 verified reviews on Booksy">5.0 out of 5 · 43 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Lianet is awesome, the nails always come out amazing and the artwork is on point. Glad my daughter recommended her. Thank you Lianet! Nails are Perfect"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Diana</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Lianet is awesome. She is truly a nail artist. Highly recommended"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jeidy R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I wanted to express my sincere appreciation for the exceptional service I consistently receive. For over seven years, I have had the absolute pleasure of entrusting her with my regular manicures and pedicures, and I couldn't be more satisfied."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Bernice R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 43 reseñas en Booksy" data-en="Read all 43 reviews on Booksy">Read all 43 reviews on Booksy</a>')
print("OPINIONES done")

# ---------- 15. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Tampa</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1420 W Water Ave, Suite 104, Tampa, FL 33604</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=1420+W+Water+Ave,+Tampa,+FL+33604"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,77,0.4)]" href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,160,77,0.4)]" href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los disenos mas recientes de Lianet y escribe por DM cualquier duda antes de tu cita." data-en="See Lianet\'s latest designs and DM any questions before your appointment.">See Lianet\'s latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Lia Beauty, 1420 W Water Ave, Tampa FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=1420+W+Water+Ave,+Tampa,+FL+33604&output=embed"')
print("UBICACION done")

# ---------- 16. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas hechas con carino, por Lianet." data-en="Nails made with heart, by Lianet.">Nails made with heart, by Lianet.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu Gel X, rosa y blanco, set completo o pedicura, cuando lo necesites." data-en="Book online in seconds: your Gel X, pink and white, full set or pedicure, whenever you need a refresh.">Book online in seconds: your Gel X, pink and white, full set or pedicure, whenever you need a refresh.</p>')
rep('<a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# ---------- 17. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Lia Beauty</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Lia Beauty" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,240,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Lia Beauty</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Tampa, FL. Lun-Vie 8:30am-5:45pm, Sab 8:30am-4pm. Con cita previa." data-en="Nail salon in Tampa, FL. Mon-Fri 8:30am-5:45pm, Sat 8:30am-4pm. By appointment.">Nail salon in Tampa, FL. Mon-Fri 8:30am-5:45pm, Sat 8:30am-4pm. By appointment.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>1420 W Water Ave, Suite 104, Tampa, FL 33604</p>')
rep('<p><a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="hover:text-[#bef0be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://booksy.com/en-us/770997_lia-beauty_nail-salon_15761_tampa" target="_blank" rel="noopener" class="hover:text-[#bef0be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
assert '<p><a href="https://www.instagram.com/lianetnailstudio/" target="_blank" rel="noopener" class="hover:text-[#bef0be]">Instagram · @lianetnailstudio</a></p>' in h
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lia Beauty.</p>')
print("FOOTER done")

# ---------- 18. book-float (URL ya reemplazada en el paso global) ----------
assert 'class="book-float"' in h
print("BOOK-FLOAT ok")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
