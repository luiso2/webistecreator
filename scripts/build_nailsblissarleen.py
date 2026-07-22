import re
import os
import shutil
import colorsys

SLUG = "nailsblissarleen"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, n)


# ---------- 1. Proteger el badge Merktop ----------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------- 2. Paleta: rotacion de matiz generica (colorsys), HUE_SHIFT=40 ----------
# base accent #a04a72 (plum-pink) -> ~#a05b4a (terracotta/coral calido)
HUE_SHIFT = 40.0


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
print("PALETTE done. accent-deep ->", shift_hex('a04a72'))

# ---------- 3. Globales: Booksy URL, IG URL, handle ----------
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG = 'https://www.instagram.com/_lashbloom/'
NEW_IG = 'https://www.instagram.com/nailsblissbyarleen/'
assert OLD_IG in h
h = h.replace(OLD_IG, NEW_IG)

assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@nailsblissbyarleen')
print("GLOBALS done")

# ---------- 4. HEAD ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>NailsBlissByArleen · Nail Salon in Miami, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="NailsBlissByArleen, Miami FL: manicures, gel sets, spa pedicures and apres nails with a perfect 5.0 across 27 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="NailsBlissByArleen · Nail Salon in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicures, gel sets and spa pedicures. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-5.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "NailsBlissByArleen",
    "description": "Nail salon in Miami, FL: manicures, gel manicures, gel and spa pedicures, apres nails and Dazzle Dry systems.",
    "address": { "@type": "PostalAddress", "streetAddress": "8440 SW 34 Terrace", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33155", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami", "https://www.instagram.com/nailsblissbyarleen/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "27", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "20", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicure" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Spa Pedicure" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres Nails" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------- 5. Idioma: negocio EN, esqueleto ya es EN default. Sin cambios. ----------

# ---------- 6. PRELOADER + NAV ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NB</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Nails Bliss by Arleen</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,91,74,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="NailsBlissByArleen logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,91,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails Bliss <span class="text-[color:var(--accent-deep)]">by Arleen</span></span>')
print("NAV done")

# ---------- 7. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Nail Salon" data-en="Miami, FL · Nail Salon">Miami, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Manos y pies felices, hechos con detalle." data-en="Happy hands and feet, made with detail.">Happy hands and feet, made with detail.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicura, gel y pedicura" data-en="Manicures, gel sets and">Manicures, gel sets and</span><br /><span data-es="hechos para " data-en="pedicures, made to ">pedicures, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura, pedicura, gel, Dazzle Dry y apres nails, todo con Arleen en un espacio privado y espectacular donde sus clientas dicen sentirse totalmente relajadas." data-en="Manicures, pedicures, gel, Dazzle Dry and apres nails, all with Arleen in a private, spotless space where her clients say they feel completely relaxed.">Manicures, pedicures, gel, Dazzle Dry and apres nails, all with Arleen in a private, spotless space where her clients say they feel completely relaxed.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 27 reseñas en Booksy" data-en="5.0 · 27 reviews on Booksy">5.0 · 27 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-5.jpg" alt="Manicura gel coral con anillo de compromiso, unas ovaladas brillantes" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Gel Manicure</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$40 · 1h" data-en="$40 · 1h">$40 · 1h</p>')
print("HERO done")

# ---------- 8. STRIP DE CONFIANZA ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="27">27</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Mani <span class="text-shine">&amp;</span> Pedi</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Regular, gel y Dazzle Dry" data-en="Regular, gel and Dazzle Dry">Regular, gel and Dazzle Dry</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+17 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">8440 SW 34 Terrace</p></div>')
print("STRIP done")

# ---------- 9. MARQUEE (x4 c/u) ----------
for old, new in [
    ('Classic Set', 'Manicure'),
    ('Hybrid Set', 'Pedicure'),
    ('Volume Set', 'Gel Manicure'),
    ('Mega Volume', 'Gel Pedicure'),
    ('Bottom Lashes', 'Apres Nails'),
    ('West Palm Beach, FL', 'Miami, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------- 10. EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Manicura rosa suave y brillante, mano apoyada en un case de celular" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Manicura blanco lechoso brillante, tomada al aire libre" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un espacio privado," data-en="One private suite,">One private suite,</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="NailsBlissByArleen es el espacio de Arleen en Miami, FL. Sus clientas describen el lugar como privado, espacioso, impecable y muy acogedor, con un trabajo meticuloso y minucioso en cada detalle." data-en="NailsBlissByArleen is Arleen\'s space in Miami, FL. Her clients describe the space as private, spacious, spotless and incredibly welcoming, with meticulous, detail oriented work on every set.">NailsBlissByArleen is Arleen\'s space in Miami, FL. Her clients describe the space as private, spacious, spotless and incredibly welcoming, with meticulous, detail oriented work on every set.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 27 resenas verificadas en Booksy, y clientas que dicen que definitivamente volveran." data-en="The result: a perfect 5.0 across 27 verified Booksy reviews, and clients who say they will definitely be back.">The result: a perfect 5.0 across 27 verified Booksy reviews, and clients who say they will definitely be back.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="27">27</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,91,74,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Arleen" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,91,74,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Arleen · <span class="text-[color:var(--ink-40)]" data-es="Nail artist" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ---------- 11. METODO ----------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, un set" data-en="Your visit, one set">Your visit, one set</span> <span class="text-shine" data-es="hecho con detalle" data-en="made with detail">made with detail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y color" data-en="Shape and color">Shape and color</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elegimos la forma de la una y el sistema: regular, gel, Dazzle Dry o apres, segun lo que buscas." data-en="We choose the nail shape and the system: regular, gel, Dazzle Dry or apres, based on what you want.">We choose the nail shape and the system: regular, gel, Dazzle Dry or apres, based on what you want.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Arleen trabaja con calma y precision, hasta 2h de aplicacion segun el servicio que elijas." data-en="Arleen works calmly and precisely, up to 2h of application depending on the service you choose.">Arleen works calmly and precisely, up to 2h of application depending on the service you choose.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tus unas terminadas y el color que elegiste, listo para durar." data-en="You leave with your finished nails and the color you chose, ready to last.">You leave with your finished nails and the color you chose, ready to last.</p>''')
print("METODO done")

# ---------- 12. SERVICIOS ----------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por NailsBlissByArleen en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by NailsBlissByArleen on Booksy. Booking confirms instantly.">Prices and durations as published by NailsBlissByArleen on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo esencial" data-en="The essential">The essential</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure" data-en="Manicure">Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura regular clasica, unas limadas, cuticulas cuidadas y esmalte a tu eleccion." data-en="Classic regular manicure: shaped nails, cared-for cuticles and the polish color of your choice.">Classic regular manicure: shaped nails, cared-for cuticles and the polish color of your choice.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$20</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,91,74,0.4); box-shadow: 0 18px 50px rgba(51,35,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salon" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel Manicure" data-en="Gel Manicure">Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura en gel de larga duracion, color brillante que no se desgasta ni se descascara." data-en="Long-lasting gel manicure with a glossy color that resists chipping and wear.">Long-lasting gel manicure with a glossy color that resists chipping and wear.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para relajarte" data-en="For unwinding">For unwinding</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Spa Pedicure" data-en="Spa Pedicure">Spa Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura spa completa: remojo, exfoliacion, masaje y esmalte, el ritual completo para tus pies." data-en="A full spa pedicure: soak, scrub, massage and polish, the complete ritual for your feet.">A full spa pedicure: soak, scrub, massage and polish, the complete ritual for your feet.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema premium" data-en="Premium system">Premium system</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Apres Nails" data-en="Apres Nails">Apres Nails</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El sistema Apres, una extension de gel duradera y de acabado natural." data-en="The Apres system, a long-lasting gel extension with a natural finish.">The Apres system, a long-lasting gel extension with a natural finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: pedicura regular, Dazzle Dry, Luminary, kids mani-pedi y polish refresh. Menu completo de 17 servicios y disponibilidad en Booksy." data-en="Also available: regular pedicure, Dazzle Dry, Luminary, kids mani-pedi and polish refresh. Full 17-service menu and availability on Booksy.">Also available: regular pedicure, Dazzle Dry, Luminary, kids mani-pedi and polish refresh. Full 17-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 13. GALERIA (solo 2 fotos reales de calidad quedaron disponibles) ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail work">nail work</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid sm:grid-cols-2 gap-5 sm:gap-6">
        <div class="frame zoomable aspect-[4/5] img-reveal"><span class="tile-cap" data-es="Manicura roja en gel" data-en="Red gel manicure">Red gel manicure</span><img src="assets/raw/bk-4.jpg" alt="Manicura roja brillante en cuadrado, junto a un frasco de esmalte gel CANNI" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[4/5] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Manicura borgoña con joyería" data-en="Burgundy mani with fine jewelry">Burgundy mani with fine jewelry</span><img src="assets/raw/bk-8.jpg" alt="Manicura borgona brillante en cuadrado, con anillos y pulsera de oro" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 14. OPINIONES (reales, con autor, 3 named_reviews verbatim) ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 27 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 27 verified reviews on Booksy">5.0 out of 5 · 27 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely loved my experience!! I'm so happy with my nails: they turned out beautiful! The work was flawless, with incredible attention to detail and a perfect finish. She was also kind, professional, and made the entire appointment enjoyable.<br /><br />The space itself was just as amazing. It's private, spacious, spotless, and incredibly welcoming. I was able to truly relax, clear my mind, and enjoy some much-needed time for myself. The atmosphere is peaceful and makes you feel comfortable from the moment you walk in.<br /><br />I highly recommend this place to anyone looking for exceptional nail services and a relaxing, high-quality experience. I'll definitely be coming back!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Gabby C&hellip;</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Amanda R&hellip;</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Loved my experience with Arleen! She was incredibly detail oriented and efficient. My nails came out perfect! 💯"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Carla L&hellip;</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 27 reseñas en Booksy" data-en="Read all 27 reviews on Booksy">Read all 27 reviews on Booksy</a>')
print("OPINIONES done")

# ---------- 15. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">8440 SW 34 Terrace, Miami, FL 33155</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=8440+SW+34+Terrace,+Miami,+FL+33155"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,91,74,0.4)]" href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,91,74,0.4)]" href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('''data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>''',
    '''data-es="Mira los trabajos mas recientes de Arleen y escribe por DM cualquier duda antes de tu cita." data-en="See Arleen's latest nail sets and DM any questions before your appointment.">See Arleen's latest nail sets and DM any questions before your appointment.</p>''')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: NailsBlissByArleen, 8440 SW 34 Terrace, Miami FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=8440+SW+34+Terrace,+Miami,+FL+33155&output=embed"')
print("UBICACION done")

# ---------- 16. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Manos y pies felices, hechos con detalle." data-en="Happy hands and feet, made with detail.">Happy hands and feet, made with detail.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu manicura, tu gel, tu pedicura spa o el apres que ya te toca." data-en="Book online in seconds: your manicure, your gel set, your spa pedicure, or the apres set you are due for.">Book online in seconds: your manicure, your gel set, your spa pedicure, or the apres set you are due for.</p>')
rep('<a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# ---------- 17. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Nails Bliss by Arleen</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,198,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="NailsBlissByArleen logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,198,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">NailsBlissByArleen</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Miami, FL. Atencion con cita previa." data-en="Nail salon in Miami, FL. By appointment only.">Nail salon in Miami, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>8440 SW 34 Terrace, Miami, FL 33155</p>')
rep('<p><a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="hover:text-[#f0c6be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="hover:text-[#f0c6be]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/nailsblissbyarleen/" target="_blank" rel="noopener" class="hover:text-[#f0c6be]">Instagram · @nailsblissbyarleen</a></p>',
    '<p><a href="https://www.instagram.com/nailsblissbyarleen/" target="_blank" rel="noopener" class="hover:text-[#f0c6be]">Instagram · @nailsblissbyarleen</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 NailsBlissByArleen.</p>')
print("FOOTER done")

# ---------- 18. book-float ----------
rep('<a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://booksy.com/en-us/1363980_nailsblissbyarleen_nail-salon_15889_miami" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
