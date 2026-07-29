import re
import os
import shutil
import colorsys

SLUG = "im-nail-studio-hialeah"
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

# ---------- 2. Paleta: rotacion de matiz (HUE_SHIFT=275, plum-pink a04a72 -> indigo-violeta) ----------
HUE_SHIFT = 275.0


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

# ---------- 3. Globales: Booksy, Instagram, handle ----------
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1227178_im-nail-studio_nail-salon_15886_hialeah'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG = 'https://www.instagram.com/_lashbloom/'
NEW_IG = 'https://www.instagram.com/im.nailss/'
assert OLD_IG in h
h = h.replace(OLD_IG, NEW_IG)

OLD_HANDLE = '@_lashbloom'
NEW_HANDLE = '@im.nailss'
assert OLD_HANDLE in h
h = h.replace(OLD_HANDLE, NEW_HANDLE)
print("GLOBALS done")

# ---------- 4. HEAD: title, meta, JSON-LD, favicon ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Im.nail studio · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Im.nail studio, Hialeah FL: gel manicures, pedicures, builder gel, polygel and apres nail sets, with a perfect 5.0 across 23 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Im.nail studio · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel manicures, pedicures, builder gel and polygel sets. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-16.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Im.nail studio",
    "description": "Nail salon in Hialeah, FL: gel manicures, pedicures, builder gel, polygel, apres and luxury pedicure services.",
    "address": { "@type": "PostalAddress", "streetAddress": "2594 W 84th St", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33016", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.897113360798993, "longitude": -80.33621314913034 },
    "sameAs": ["https://booksy.com/en-us/1227178_im-nail-studio_nail-salon_15886_hialeah", "https://www.instagram.com/im.nailss/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "23", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Regular básico" } },
      { "@type": "Offer", "price": "150", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Servicio V.I.P" } },
      { "@type": "Offer", "price": "105", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicura con Builder/Rubber o Luminary + PediGel" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "LUXURY PEDICURE GEL" } }
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
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">IM</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Im.nail studio</span>')

# ---------- 7. NAV ----------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(84,74,160,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Im.nail studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(84,74,160,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Im<span class="text-[color:var(--accent-deep)]">.nail studio</span></span>')
print("NAV done")

# ---------- 8. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Salón de uñas" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Salón de uñas</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Manos y pies que brillan con cuidado." data-en="Hands and feet that shine with care.">Manos y pies que brillan con cuidado.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicura, pedicura" data-en="Manicures, pedicures">Manicura, pedicura</span><br /><span data-es="y sets hechos para " data-en="and sets made to ">y sets hechos para </span><span class="text-shine" data-es="durar" data-en="last">durar</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura y pedicura en gel, builder, rubber, polygel y apres, más pedicura de lujo y diseños de uñas, todo de la mano de Isleydi Mejias en su estudio de Hialeah. Un 5.0 perfecto en 23 reseñas de Booksy." data-en="Gel manicures and pedicures, builder, rubber, polygel and apres sets, plus luxury pedicures and nail art, all by Isleydi Mejias at her Hialeah studio. A perfect 5.0 across 23 Booksy reviews.">Manicura y pedicura en gel, builder, rubber, polygel y apres, más pedicura de lujo y diseños de uñas, todo de la mano de Isleydi Mejias en su estudio de Hialeah. Un 5.0 perfecto en 23 reseñas de Booksy.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 23 reseñas en Booksy" data-en="5.0 · 23 reviews on Booksy">5.0 · 23 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-16.jpg" alt="Manicura roja brillante terminada en Im.nail studio" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Servicio V.I.P</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$150 · 3h" data-en="$150 · 3h">$150 · 3h</p>')
print("HERO done")

# ---------- 9. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="23">23</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Manicure <span class="text-shine">&amp;</span> Pedicure</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Combos completos" data-en="Full combos">Combos completos</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">23 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Menú completo en Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">2594 W 84th St</p></div>')
print("STRIP done")

# ---------- 10. MARQUEE (x4 cada palabra) ----------
for old, new in [
    ('Classic Set', 'Manicure'),
    ('Hybrid Set', 'Pedicure'),
    ('Volume Set', 'Polygel'),
    ('Mega Volume', 'Builder Gel'),
    ('Bottom Lashes', 'Apres'),
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
    '<img src="assets/raw/bk-4.jpg" alt="Manicura y pedicura en negro combinadas, en manos y pies, en Im.nail studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Pedicura en tono nude sobre alfombra de piel en Im.nail studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Isleydi," data-en="Isleydi,">Isleydi,</span><br /><span class="text-shine" data-es="cuidado en cada detalle" data-en="care in every detail">cuidado en cada detalle</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Im.nail studio es el estudio de Isleydi Mejias en 2594 W 84th St, Hialeah. Cada cita, de la manicura regular al builder gel, polygel o apres, se hace con atención al detalle en manos y pies." data-en="Im.nail studio is Isleydi Mejias\' studio at 2594 W 84th St, Hialeah. Every appointment, from a regular manicure to builder gel, polygel or apres, is done with attention to detail on hands and feet.">Im.nail studio es el estudio de Isleydi Mejias en 2594 W 84th St, Hialeah. Cada cita, de la manicura regular al builder gel, polygel o apres, se hace con atención al detalle en manos y pies.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 23 reseñas verificadas en Booksy, y clientas que la conocen simplemente como \'islady\'." data-en="The result: a perfect 5.0 across 23 verified Booksy reviews, and clients who simply call her \'islady\'.">El resultado: 5.0 perfecto en 23 reseñas verificadas en Booksy, y clientas que la conocen simplemente como \'islady\'.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="23">23</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(84,74,160,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Isleydi Mejias, dueña de Im.nail studio" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(84,74,160,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Isleydi · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ---------- 12. METODO ----------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Uñas hechas" data-en="Nails made">Uñas hechas</span> <span class="text-shine" data-es="con detalle" data-en="with detail">con detalle</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio claro, y confirmas al instante." data-en="Pick your service on Booksy with clear pricing, and confirm instantly.">Eliges tu servicio en Booksy con precio claro, y confirmas al instante.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y sistema" data-en="Shape and system">Forma y sistema</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Hablamos de la forma y el sistema: gel, builder, rubber, luminary, polygel o apres, según lo que busques." data-en="We talk shape and system: gel, builder, rubber, luminary, polygel or apres, based on what you want.">Hablamos de la forma y el sistema: gel, builder, rubber, luminary, polygel o apres, según lo que busques.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">Manos a la obra</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Isleydi trabaja con calma y detalle, hasta 3h de aplicación en el Servicio V.I.P." data-en="Isleydi works calmly and carefully, up to 3h of application for the V.I.P. service.">Isleydi trabaja con calma y detalle, hasta 3h de aplicación en el Servicio V.I.P.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El acabado" data-en="The finish">El acabado</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con manos y pies impecables, de la manicura básica a la pedicura de lujo." data-en="You leave with flawless hands and feet, from the basic manicure to the luxury pedicure.">Sales con manos y pies impecables, de la manicura básica a la pedicura de lujo.</p>''')
print("METODO done")

# ---------- 13. SERVICIOS ----------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Im.nail studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Im.nail studio on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Im.nail studio en Booksy. Reserva con confirmación inmediata.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clásico de todos los días" data-en="Everyday classic">Clásico de todos los días</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Regular básico" data-en="Manicure Regular básico">Manicure Regular básico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura regular limpia y prolija con esmaltado clásico, el punto de partida de siempre." data-en="A clean, precise regular manicure with classic polish, the everyday starting point.">A clean, precise regular manicure with classic polish, the everyday starting point.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="https://booksy.com/en-us/1227178_im-nail-studio_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(84,74,160,0.4); box-shadow: 0 18px 50px rgba(34,34,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Favorito del estudio</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Servicio V.I.P" data-en="Servicio V.I.P">Servicio V.I.P</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La cita completa de Isleydi: manos y pies con la mayor dedicación, de principio a fin." data-en="Isleydi\'s full appointment: hands and feet with the most dedicated attention, start to finish.">Isleydi\'s full appointment: hands and feet with the most dedicated attention, start to finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$150</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h</p></div>
            <a href="https://booksy.com/en-us/1227178_im-nail-studio_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Combo popular" data-en="Popular combo">Combo popular</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Builder/Rubber o Luminary + PediGel" data-en="Builder/Rubber or Luminary + PediGel">Builder/Rubber o Luminary + PediGel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura con builder, rubber o luminary, más pedicura en gel: manos y pies en una sola cita." data-en="Builder, rubber or luminary manicure, plus a gel pedicure: hands and feet in one appointment.">Builder, rubber or luminary manicure, plus a gel pedicure: hands and feet in one appointment.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$105</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>
            <a href="https://booksy.com/en-us/1227178_im-nail-studio_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies" data-en="Feet">Pies</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luxury Pedicure Gel" data-en="Luxury Pedicure Gel">Luxury Pedicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura de lujo con esmaltado en gel de larga duración, para pies impecables." data-en="A luxury pedicure with long-lasting gel polish, for flawless feet.">A luxury pedicure with long-lasting gel polish, for flawless feet.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p></div>
            <a href="https://booksy.com/en-us/1227178_im-nail-studio_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: manicura y pedicura de mujer y hombre, apres, polygel con extensión, diseños de uñas y reparación de uñas. Menú completo de 23 servicios y disponibilidad en Booksy." data-en="Also available: women\'s and men\'s manicures and pedicures, apres, polygel with extension, nail designs and nail repair. Full 23-service menu and availability on Booksy.">También: manicura y pedicura de mujer y hombre, apres, polygel con extensión, diseños de uñas y reparación de uñas. Menú completo de 23 servicios y disponibilidad en Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 14. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Trabajo</span> <span class="text-shine" data-es="real" data-en="nail work">real</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Manicura y pedicura combinadas" data-en="Matching manicure and pedicure">Manicura y pedicura combinadas</span><img src="assets/raw/bk-12.jpg" alt="Manicura en tonos pastel azul, rosa y verde junto a una pedicura a juego, sobre alfombra de piel, en Im.nail studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Francesa azul marino con glitter" data-en="Navy French with glitter">Francesa azul marino con glitter</span><img src="assets/raw/bk-11.jpg" alt="Manicura francesa en azul marino con acentos de glitter" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Azul lavanda" data-en="Lavender blue">Azul lavanda</span><img src="assets/raw/bk-3.jpg" alt="Manicura en tono azul lavanda con acabado brillante" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Lavanda junto a un tulipán" data-en="Lavender next to a tulip">Lavanda junto a un tulipán</span><img src="assets/raw/bk-5.jpg" alt="Manicura lavanda junto a un tulipán blanco" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Diseño de uñas deportivo" data-en="Sports-themed nail art">Diseño de uñas deportivo</span><img src="assets/raw/bk-7.jpg" alt="Manicura en tonos pastel con diseño de uñas de balón de futbol" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Pedicura nude de cerca" data-en="Nude pedicure close-up">Pedicura nude de cerca</span><img src="assets/raw/bk-14.jpg" alt="Detalle de pedicura en tono nude" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 15. OPINIONES (reales, verbatim de data.json) ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 23 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 23 verified reviews on Booksy">5.0 de 5 · 23 reseñas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"wonderful. islady is super profesional, detailed in her work and friendly"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Lucina</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"La mejor! Muy recomendado"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Camila Z.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Increíbles como siempre ❤️"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Eva G.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1227178_im-nail-studio_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1227178_im-nail-studio_nail-salon_15886_hialeah" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 23 reseñas en Booksy" data-en="Read all 23 reviews on Booksy">Leer las 23 reseñas en Booksy</a>')
print("OPINIONES done")

# ---------- 16. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Hialeah</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">2594 W 84th St, Hialeah, FL 33016</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=2594+W+84th+St,+Hialeah,+FL+33016"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Martes a sábado, con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="Tuesday through Saturday, by appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Martes a sábado, con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los diseños más recientes de Isleydi y escribe por DM cualquier duda antes de tu cita." data-en="See Isleydi\'s latest designs and DM any questions before your appointment.">Mira los diseños más recientes de Isleydi y escribe por DM cualquier duda antes de tu cita.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Im.nail studio, 2594 W 84th St, Hialeah FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=2594+W+84th+St,+Hialeah,+FL+33016&output=embed"')
print("UBICACION done")

# ---------- 17. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Manos y pies que brillan con cuidado." data-en="Hands and feet that shine with care.">Manos y pies que brillan con cuidado.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Tu próxima cita</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu manicura, tu pedicura o el Servicio V.I.P. que ya te toca." data-en="Book online in seconds: your manicure, your pedicure, or the V.I.P. service you are due for.">Reserva en línea en segundos: tu manicura, tu pedicura o el Servicio V.I.P. que ya te toca.</p>')
print("CTA FINAL done")

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Im.nail studio</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(194,190,240,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Im.nail studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(194,190,240,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Im.nail studio</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Hialeah, FL. Atención con cita previa, martes a sábado." data-en="Nail salon in Hialeah, FL. By appointment only, Tuesday through Saturday.">Salón de uñas en Hialeah, FL. Atención con cita previa, martes a sábado.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>2594 W 84th St, Hialeah, FL 33016</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Im.nail studio.</p>')
print("FOOTER done")

# ---------- 19. book-float (URL ya reemplazada en el paso global) ----------
assert 'class="book-float"' in h
print("BOOK-FLOAT ok")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
