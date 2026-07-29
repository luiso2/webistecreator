import re
import os
import shutil
import colorsys

SLUG = "celinabeautynailstampa"
OUT_SLUG = "celina-beauty-nails-tampa"
os.makedirs(f"output/{OUT_SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{OUT_SLUG}/index.html")
h = open(f"output/{OUT_SLUG}/index.html", encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:160]
    h = h.replace(a, b, n)


# ---------- 1. Proteger el badge Merktop ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------- 2. Paleta: rotacion de matiz generica (HUE_SHIFT=30, a04a72 -> rosa coral calido) ----------
HUE_SHIFT = 30.0


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
NEW_BOOKSY = 'https://booksy.com/en-us/970283_celina-beauty-nails-studio_nail-salon_15761_tampa'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG = 'https://www.instagram.com/_lashbloom/'
NEW_IG = 'https://www.instagram.com/celinabeautynails_studio/'
assert OLD_IG in h
h = h.replace(OLD_IG, NEW_IG)

OLD_HANDLE = '@_lashbloom'
NEW_HANDLE = '@celinabeautynails_studio'
assert OLD_HANDLE in h
h = h.replace(OLD_HANDLE, NEW_HANDLE)
print("GLOBALS done")

# ---------- 4. HEAD: title, meta, JSON-LD, favicon ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Celina Beauty Nails &amp; Studio · Nail Salon in Tampa, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Celina Beauty Nails &amp; Studio, Tampa FL: Russian manicure, Gel X, Polygel and builder gel nail sets, plus deluxe and volcano spa pedicures, with a perfect 5.0 across 229 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Celina Beauty Nails &amp; Studio · Nail Salon in Tampa, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Russian manicure, Gel X and Polygel nail sets. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-8.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Celina Beauty Nails & Studio",
    "description": "Nail salon in Tampa, FL: Russian manicure, Gel X, Polygel and builder gel nail sets, plus regular, deluxe and volcano spa pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "8019 N Himes Ave, Suite 500", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33614", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.024279589730014, "longitude": -82.50016344854382 },
    "sameAs": ["https://booksy.com/en-us/970283_celina-beauty-nails-studio_nail-salon_15761_tampa", "https://www.instagram.com/celinabeautynails_studio/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "229", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "105", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Russian Manicure with Polygel Long" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Russian pedicura luxury" } },
      { "@type": "Offer", "price": "95", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder gel manicure with dual forms long" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Deluxe Pedicure" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------- 5. Idioma: ES por defecto (data.json language = es) ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")
print("LANG done")

# ---------- 6. PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">CB</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Celina Beauty</span>')

# ---------- 7. NAV ----------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,77,74,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Celina Beauty Nails & Studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,77,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Celina <span class="text-[color:var(--accent-deep)]">Beauty</span></span>')
print("NAV done")

# ---------- 8. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tampa, FL · Salón de uñas" data-en="Tampa, FL · Nail Salon">Tampa, FL · Salón de uñas</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Uñas hermosas, hechas con detalle." data-en="Beautiful nails, made with detail.">Uñas hermosas, hechas con detalle.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicura rusa, Gel X" data-en="Russian manicure, Gel X">Russian manicure, Gel X</span><br /><span data-es="y Polygel, hechos para " data-en="and Polygel, made to ">and Polygel, made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura rusa, Gel X, Polygel y builder gel, más pedicura regular, deluxe y spa volcán: 32 servicios con precio y duración claros, atendidos por Roxana en su estudio de Tampa." data-en="Russian manicure, Gel X, Polygel and builder gel sets, plus regular, deluxe and volcano spa pedicures: 32 services with clear price and duration, done by Roxana in her Tampa studio.">Manicura rusa, Gel X, Polygel y builder gel, más pedicura regular, deluxe y spa volcán: 32 servicios con precio y duración claros, atendidos por Roxana en su estudio de Tampa.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 229 reseñas en Booksy" data-en="5.0 · 229 reviews on Booksy">5.0 · 229 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-8.jpg" alt="Manicura rosa nude con lazo 3D y strass sobre fondo de trigo, Celina Beauty Nails & Studio" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Russian Manicure</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$105 · 2h" data-en="$105 · 2h">$105 · 2h</p>')
print("HERO done")

# ---------- 9. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="229">229</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Russian <span class="text-shine">&amp;</span> Gel X</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets de uñas premium" data-en="Premium nail sets">Premium nail sets</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">32 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo de servicios" data-en="Full service menu">Menú completo de servicios</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">N Himes Ave, Suite 500</p></div>')
print("STRIP done")

# ---------- 10. MARQUEE (x4 cada palabra) ----------
for old, new in [
    ('Classic Set', 'Gel X'),
    ('Hybrid Set', 'Polygel'),
    ('Volume Set', 'Russian Manicure'),
    ('Mega Volume', 'Builder Gel'),
    ('Bottom Lashes', 'Deluxe Pedicure'),
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
    '<img src="assets/raw/bk-6.jpg" alt="Manicura color vino tinto brillante sobre fondo de trigo seco, Celina Beauty Nails & Studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-5.jpg" alt="Set de uñas ovaladas color blanco lechoso, acabado brillante" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="El estudio de" data-en="The studio of">El estudio de</span><br /><span class="text-shine" data-es="Roxana en Tampa" data-en="Roxana in Tampa">Roxana in Tampa</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Celina Beauty Nails &amp; Studio es el estudio de Roxana Amaral Gomez, en Himes Ave, Suite 500, Tampa. Cada servicio, de la manicura rusa al Gel X y al Polygel, se hace con calma y atención al detalle." data-en="Celina Beauty Nails &amp; Studio is the studio of Roxana Amaral Gomez, on Himes Ave, Suite 500, Tampa. Every service, from Russian manicure to Gel X and Polygel, is done with care and attention to detail.">Celina Beauty Nails &amp; Studio es el estudio de Roxana Amaral Gomez, en Himes Ave, Suite 500, Tampa. Cada servicio, de la manicura rusa al Gel X y al Polygel, se hace con calma y atención al detalle.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 229 reseñas verificadas en Booksy, y clientas que piden a Roxana por su nombre cita tras cita." data-en="The result: a perfect 5.0 across 229 verified Booksy reviews, and clients who ask for Roxana by name appointment after appointment.">El resultado: 5.0 perfecto en 229 reseñas verificadas en Booksy, y clientas que piden a Roxana por su nombre cita tras cita.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="229">229</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,77,74,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Celina Beauty Nails & Studio" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,77,74,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Roxana · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ---------- 12. METODO ----------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Uñas hechas" data-en="Nails made">Uñas hechas</span> <span class="text-shine" data-es="con detalle" data-en="with detail">with detail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio entre 32 opciones en Booksy, con precio y duración claros, y confirmas al instante." data-en="Pick your service among 32 options on Booksy, with clear price and duration, and confirm instantly.">Eliges tu servicio entre 32 opciones en Booksy, con precio y duración claros, y confirmas al instante.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y sistema" data-en="Shape and system">Forma y sistema</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elegimos el largo, la forma y el sistema: Gel X, Polygel, acrílico o builder gel, según lo que busques." data-en="We choose the length, shape and system: Gel X, Polygel, acrylic or builder gel, based on what you want.">Elegimos el largo, la forma y el sistema: Gel X, Polygel, acrílico o builder gel, según lo que busques.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">Manos a la obra</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Roxana trabaja con calma y detalle, hasta 2h de aplicación según el servicio elegido." data-en="Roxana works calmly and carefully, up to 2h of application depending on the service you choose.">Roxana trabaja con calma y detalle, hasta 2h de aplicación según el servicio elegido.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">Salida</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tus manos y pies listos, de la manicura rusa a la pedicura deluxe o spa volcán." data-en="You leave with hands and feet ready, from the Russian manicure to the deluxe or volcano spa pedicure.">Sales con tus manos y pies listos, de la manicura rusa a la pedicura deluxe o spa volcán.</p>''')
print("METODO done")

# ---------- 13. SERVICIOS ----------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Celina Beauty Nails &amp; Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Celina Beauty Nails &amp; Studio on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Celina Beauty Nails &amp; Studio en Booksy. Reserva con confirmación inmediata.</p>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
BOOKSY = NEW_BOOKSY
NEW_SERVICES = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma del estudio" data-en="Studio signature">Firma del estudio</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Russian Manicure with Polygel Long</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La técnica rusa sobre Polygel en largo extendido: cutícula perfecta y forma esculpida a mano." data-en="The Russian technique over Polygel in an extended length: perfect cuticle work and a hand-sculpted shape.">La técnica rusa sobre Polygel en largo extendido: cutícula perfecta y forma esculpida a mano.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$105</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,77,74,0.4); box-shadow: 0 18px 50px rgba(51,34,36,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Favorito del estudio</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Russian pedicura luxury</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una pedicura rusa de lujo, cutícula y callos tratados a fondo, para pies impecables." data-en="A luxury Russian pedicure, deep cuticle and callus care, for flawless feet.">Una pedicura rusa de lujo, cutícula y callos tratados a fondo, para pies impecables.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Estructura" data-en="Structure">Estructura</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Builder Gel Manicure with Dual Forms Long</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Builder gel sobre dual forms en largo extendido: estructura resistente y acabado natural." data-en="Builder gel over dual forms in an extended length: durable structure with a natural finish.">Builder gel sobre dual forms en largo extendido: estructura resistente y acabado natural.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$95</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Spa" data-en="Spa">Spa</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Deluxe Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La pedicura deluxe del estudio: exfoliación, masaje e hidratación completa para tus pies." data-en="The studio's deluxe pedicure: exfoliation, massage and full hydration for your feet.">La pedicura deluxe del estudio: exfoliación, masaje e hidratación completa para tus pies.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

# Bloques de categorias completas (32 servicios, precio real, sin acordeon)
CATS = [
    ("Gel X", "Gel X", [
        ("Gel X Short", 65), ("Gel X medium", 75), ("Gel X long", 85),
    ]),
    ("Polygel", "Polygel", [
        ("Polygel small", 65), ("Polygel medium", 75), ("Polygel long", 85),
    ]),
    ("Manicura rusa", "Russian manicure", [
        ("Russian manicure with regular gel", 65), ("Russian manicure with polygel small", 80),
        ("Russian manicure with Polygel medium", 90), ("Russian manicure with Polygel long", 105),
    ]),
    ("Builder gel", "Builder gel", [
        ("Builder gel Manicure small", 65), ("Builder gel manicure medium", 75),
        ("Builder gel manicure with dual forms small", 75), ("Builder gel manicure with dual forms medium", 85),
        ("Builder gel manicure with dual forms long", 95),
    ]),
    ("Manicura esencial", "Essential manicure", [
        ("Gel Manicure", 40), ("French Manicure- With Gel", 45), ("Toe gel color change", 35),
    ]),
    ("Pedicura", "Pedicure", [
        ("Pedicure Regular", 55), ("Spa pedicure", 65), ("Deluxe Pedicure", 70),
        ("Volcano Pedicure", 75), ("Russian pedicura luxury", 100), ("Men's pedicure", 50),
    ]),
    ("Acrílico y encapsulado", "Acrylic and encapsulated", [
        ("Acrylic nails Small fullset", 70), ("Acrylic Nails Fullset M/L", 80),
        ("Acrylic Small fill", 65), ("Acrylics M/L fill", 75),
        ("Encapsulated Nails Small", 75), ("Encapsulated M/L acrylic nails", 80),
        ("Ombre Nails Acrylic", 85), ("Acrylic Toes- Two toes", 20),
    ]),
]
total_services = sum(len(items) for _, _, items in CATS)
assert total_services == 32, total_services

cat_cards = []
for es_label, en_label, items in CATS:
    rows = "\n".join(
        f'            <div class="flex items-baseline justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)] last:border-0"><span class="text-sm font-light">{name}</span><span class="text-sm font-medium whitespace-nowrap ml-3">${price}</span></div>'
        for name, price in items
    )
    cat_cards.append(f'''        <div class="glass glass-hover rounded-3xl p-6 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="{es_label}" data-en="{en_label}">{es_label}</p>
{rows}
        </div>''')

FULL_MENU = '''      <div class="mt-8">
        <p class="reveal text-center text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-6" data-es="El menú completo" data-en="The full menu">El menú completo</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
''' + "\n".join(cat_cards) + '''
        </div>
      </div>
      '''

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    FULL_MENU + '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="32 servicios en total. Precios y disponibilidad exactos en Booksy." data-en="32 services in total. Exact prices and availability on Booksy.">32 servicios en total. Precios y disponibilidad exactos en Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 14. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Trabajo</span> <span class="text-shine" data-es="real" data-en="nail work">real</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Manicura rosa nude con lazo 3D y strass" data-en="Nude pink manicure with a 3D bow and rhinestones">Manicura rosa nude con lazo 3D y strass</span><img src="assets/raw/bk-8.jpg" alt="Manicura en degradado rosa nude con lazo metálico 3D y strass sobre fondo de trigo, Celina Beauty Nails & Studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Blanco lechoso con brillo dorado" data-en="Milky white with a gold fleck accent">Blanco lechoso con brillo dorado</span><img src="assets/raw/bk-1.jpg" alt="Set de uñas almendra blanco lechoso con acento de brillo dorado en la cutícula" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cuadradas en tono crema" data-en="Square-shaped, cream tone">Cuadradas en tono crema</span><img src="assets/raw/bk-9.jpg" alt="Set de uñas cuadradas en tono crema, acabado brillante" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Blanco lechoso, otro ángulo" data-en="Milky white, another angle">Blanco lechoso, otro ángulo</span><img src="assets/raw/bk-4.jpg" alt="Set de uñas blanco lechoso con acento de brillo plateado y dorado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Degradado nude con brillo" data-en="Nude ombre with glitter">Degradado nude con brillo</span><img src="assets/raw/bk-7.jpg" alt="Set de uñas nude con degradado de brillo dorado y plateado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Vino tinto brillante" data-en="Glossy oxblood red">Vino tinto brillante</span><img src="assets/raw/bk-6.jpg" alt="Manicura color vino tinto brillante sobre fondo de trigo seco" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 15. OPINIONES ----------
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 229 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 229 verified reviews on Booksy">5.0 de 5 · 229 reseñas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I highly recommend her! She always does an amazing job on my pedicure, and my French nails come out absolutely beautiful every time. She’s professional, detail-oriented, and consistently delivers outstanding results. I’m always happy with her work! \U0001F485\U0001F90D"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Zulivette G.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Roxana es la mejor, siempre me hace las uñas hermosas, es muy detallista y muy atenta \U0001F496 siempre me va muy bien con ella y los diseños que hace"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sarah C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Siempre salgo super complacida … La mejor las \U0001F970\U0001F970\U0001F970\U0001F970\U0001F970"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Janice R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="' + NEW_BOOKSY + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_BOOKSY + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 229 reseñas en Booksy" data-en="Read all 229 reviews on Booksy">Leer las 229 reseñas en Booksy</a>')
print("OPINIONES done")

# ---------- 16. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Tampa</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">8019 N Himes Ave, Suite 500, Tampa, FL 33614</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=8019+N+Himes+Ave,+Suite+500,+Tampa,+FL+33614"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los sets más recientes de Roxana y escribe por DM cualquier duda antes de tu cita." data-en="See Roxana\'s latest sets and DM any questions before your appointment.">Mira los sets más recientes de Roxana y escribe por DM cualquier duda antes de tu cita.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Celina Beauty Nails & Studio, 8019 N Himes Ave, Suite 500, Tampa FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=8019+N+Himes+Ave,+Suite+500,+Tampa,+FL+33614&output=embed"')
print("UBICACION done")

# ---------- 17. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Uñas hermosas, hechas con detalle." data-en="Beautiful nails, made with detail.">Uñas hermosas, hechas con detalle.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Tu próxima cita</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu manicura rusa, tu Gel X, tu Polygel o la pedicura que ya te toca." data-en="Book online in seconds: your Russian manicure, your Gel X, your Polygel, or the pedicure you are due for.">Reserva en línea en segundos: tu manicura rusa, tu Gel X, tu Polygel o la pedicura que ya te toca.</p>')
print("CTA FINAL done")

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Celina Beauty</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Celina Beauty Nails & Studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Celina Beauty Nails</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Tampa, FL. Atención con cita previa." data-en="Nail salon in Tampa, FL. By appointment only.">Salón de uñas en Tampa, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>8019 N Himes Ave, Suite 500, Tampa, FL 33614</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Celina Beauty Nails &amp; Studio.</p>')
print("FOOTER done")

# Nota: los href de Booksy en nav/mobile-menu/hero/ubicacion/footer/book-float ya
# quedaron apuntando a NEW_BOOKSY desde el reemplazo global del paso 3; no hace
# falta un rep() adicional para ellos (su texto visible no cambia).

print("ALL DONE")
open(f"output/{OUT_SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))

# ---------- Copiar assets compartidos ----------
shutil.copyfile("templates/assets/tailwind.js", f"output/{OUT_SLUG}/assets/tailwind.js")
shutil.copyfile("templates/.assetsignore-template", f"output/{OUT_SLUG}/.assetsignore")
print("ASSETS done")
