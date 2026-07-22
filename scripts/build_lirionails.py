import re
import os
import shutil
import colorsys

SLUG = "lirionails"
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

# ---------- 2. Paleta: rotacion de matiz generica (dorado/plum #a04a72 -> indigo/violeta) ----------
HUE_SHIFT = -85.0


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

# ---------- 3. Globales: Booksy, IG, handle, logo ----------
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami'
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG = 'https://www.instagram.com/_lashbloom/'
NEW_IG = 'https://www.instagram.com/lirio_nails_99/'
assert h.count(OLD_IG) >= 1
h = h.replace(OLD_IG, NEW_IG)

assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@lirio_nails_99')

rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Lirio Nails · Nail Salon in Miami, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Lirio nails, Miami FL: gel and acrylic manicures, Apres and Poly Gel systems, plus facials, with a perfect 5.0 across 18 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Lirio Nails · Nail Salon in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Acrylic, Apres and Poly Gel sets, plus facials. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-8.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-4.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Lirio nails",
    "description": "Nail salon in Miami, FL: gel and acrylic manicures and pedicures, Apres and Poly Gel systems, plus deep facial treatments.",
    "address": { "@type": "PostalAddress", "streetAddress": "7801 Coral Wy #107", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33155", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami", "https://www.instagram.com/lirio_nails_99/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "18", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail and facial services", "itemListElement": [
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicura y pedicure gel" } },
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Nails" } },
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres Nail" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Limpieza Facial profunda" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------- 4. Idioma: ES principal ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")
print("LANG done")

# ---------- 5. PRELOADER + NAV ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">LN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Lirio Nails</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(84,74,160,0.35)]" />',
    '<img src="assets/raw/bk-4.jpg" alt="Lirio nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(84,74,160,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lirio <span class="text-[color:var(--accent-deep)]">Nails</span></span>')
print("NAV done")

# ---------- 6. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Salón de uñas" data-en="Miami, FL · Nail Salon">Miami, FL · Salón de uñas</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Como el lirio, tus manos florecen." data-en="Like the lily, your hands bloom.">Como el lirio, tus manos florecen.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Uñas hechas con" data-en="Nails made with">Uñas hechas con</span><br /><span data-es="el cuidado que " data-en="the care that ">el cuidado que </span><span class="text-shine" data-es="florece" data-en="blooms">florece</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura y pedicura en gel o acrílico, sistemas Apres y Poly Gel, limpiezas faciales profundas y cuidado de pestañas, todo con Lilliana Blandón en su salón de Coral Way, Miami." data-en="Gel and acrylic manicures and pedicures, Apres and Poly Gel systems, deep facial treatments and lash care, all with Lilliana Blandón at her Coral Way salon in Miami.">Manicura y pedicura en gel o acrílico, sistemas Apres y Poly Gel, limpiezas faciales profundas y cuidado de pestañas, todo con Lilliana Blandón en su salón de Coral Way, Miami.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 18 reseñas en Booksy" data-en="5.0 · 18 reviews on Booksy">5.0 · 18 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-8.jpg" alt="Diseño francés rojo con lazos blancos 3D terminado en Lirio nails" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Acrylic Nails</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$75 · 1h 30min" data-en="$75 · 1h 30min">$75 · 1h 30min</p>')
print("HERO done")

# ---------- 7. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="18">18</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Apres</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Sets completos · Rellenos</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+20 <span class="text-shine" data-es="servicios" data-en="services">servicios</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Menú completo en Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Coral Way #107</p></div>')

for old, new in [
    ('Classic Set', 'Manicure Gel'),
    ('Hybrid Set', 'Acrylic Nails'),
    ('Volume Set', 'Apres Nail'),
    ('Mega Volume', 'Poly Gel'),
    ('Bottom Lashes', 'Facial Profunda'),
    ('West Palm Beach, FL', 'Miami, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("STRIP+MARQUEE done")

# ---------- 8. EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Manicura marron chocolate con bolso de diseñador en Lirio nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Tratamiento de pestañas de cerca, antes y despues" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="El salón de" data-en="The salon of">El salón de</span><br /><span class="text-shine" data-es="Lilliana Blandón" data-en="Lilliana Blandón">Lilliana Blandón</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    "data-es=\"Lirio nails es el salón de Lilliana Blandón en Coral Way, Miami. Sus clientas la describen como creativa, perfeccionista y muy detallista, con un trabajo que combina manicura, acrílico, sistemas Apres y Poly Gel, faciales y pestañas.\" data-en=\"Lirio nails is Lilliana Blandón's salon on Coral Way in Miami. Her clients describe her as creative, a perfectionist and very detail oriented, with work that spans manicures, acrylics, Apres and Poly Gel systems, facials and lashes.\">Lirio nails es el salón de Lilliana Blandón en Coral Way, Miami. Sus clientas la describen como creativa, perfeccionista y muy detallista, con un trabajo que combina manicura, acrílico, sistemas Apres y Poly Gel, faciales y pestañas.</p>")
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 18 reseñas verificadas en Booksy, con clientas que la describen como la mejor de Miami y que aseguran que regresarán." data-en="The result: a perfect 5.0 across 18 verified Booksy reviews, with clients describing her as the best in Miami and saying they will be back.">El resultado: 5.0 perfecto en 18 reseñas verificadas en Booksy, con clientas que la describen como la mejor de Miami y que aseguran que regresarán.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="18">18</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Atención personal</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(84,74,160,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Lilliana Blandón" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(84,74,160,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Lilliana · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Manicurista</span></span>')
print("EXPERIENCIA done")

# ---------- 9. METODO ----------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, paso" data-en="Your visit, step">Tu cita, paso</span> <span class="text-shine" data-es="a paso" data-en="by step">a paso</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y color" data-en="Shape and color">Forma y color</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elegimos la forma de la uña, el sistema (gel, acrílico, Apres o Poly Gel) y el color o diseño que buscas." data-en="We choose your nail shape, the system (gel, acrylic, Apres or Poly Gel) and the color or design you want.">Elegimos la forma de la uña, el sistema (gel, acrílico, Apres o Poly Gel) y el color o diseño que buscas.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">Manos a la obra</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Lilliana trabaja con calma y precisión, hasta 1h 30min de aplicación según el servicio que elijas." data-en="Lilliana works calmly and precisely, up to 1h 30min of application depending on the service you choose.">Lilliana trabaja con calma y precisión, hasta 1h 30min de aplicación según el servicio que elijas.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">Salida</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tus uñas terminadas, o tu relleno de acrílico o Apres ya agendado para seguir luciendo perfectas." data-en="You leave with your finished nails, or your acrylic or Apres refill already booked to keep looking perfect.">Sales con tus uñas terminadas, o tu relleno de acrílico o Apres ya agendado para seguir luciendo perfectas.</p>''')
print("METODO done")

# ---------- 10. SERVICIOS ----------
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Lirio nails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lirio nails on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lirio nails en Booksy. Reserva con confirmación inmediata.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="set" data-en="set">set</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clásico" data-en="Classic">Clásico</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura y Pedicure Gel" data-en="Gel Manicure and Pedicure">Manicura y Pedicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura y pedicura en gel completas, el combo de todos los días. Version regular tambien disponible por $55." data-en="Full gel manicure and pedicure, the everyday combo. Regular version also available for $55.">Manicura y pedicura en gel completas, el combo de todos los días. Version regular tambien disponible por $55.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Precio fijo</p></div>
            <a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(84,74,160,0.4); box-shadow: 0 18px 50px rgba(34,34,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Favorito del salón</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Acrylic Nails" data-en="Acrylic Nails">Acrylic Nails</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrílico, base solida y duradera. Relleno de acrílico disponible por $70." data-en="Full acrylic set, a solid and long-lasting base. Acrylic refill available for $70.">Set completo de acrílico, base solida y duradera. Relleno de acrílico disponible por $70.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sistema moderno" data-en="Modern system">Sistema moderno</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Apres Nail" data-en="Apres Nail">Apres Nail</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El sistema Apres de Lirio nails, ligero y resistente. Relleno de Apres disponible por $70." data-en="Lirio nails Apres system, light and long-lasting. Apres refill available for $70.">El sistema Apres de Lirio nails, ligero y resistente. Relleno de Apres disponible por $70.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Piel" data-en="Skin">Piel</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Limpieza Facial Profunda" data-en="Deep Facial Cleanse">Limpieza Facial Profunda</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un tratamiento facial completo de limpieza profunda, para complementar tu cita de unas." data-en="A full deep-cleansing facial treatment, to round out your nail appointment.">Un tratamiento facial completo de limpieza profunda, para complementar tu cita de uñas.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: Poly Gel, Builder Gel, disenos desde $15, baby boomer y mas. Menú completo de 20 servicios y disponibilidad en Booksy." data-en="Also available: Poly Gel, Builder Gel, nail art from $15, baby boomer and more. Full 20-service menu and availability on Booksy.">También: Poly Gel, Builder Gel, disenos desde $15, baby boomer y mas. Menú completo de 20 servicios y disponibilidad en Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 11. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Trabajo</span> <span class="text-shine" data-es="real" data-en="work">real</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Set clásico rosa" data-en="Classic pink set">Set clásico rosa</span><img src="assets/raw/bk-1.jpg" alt="Set de manicura rosa clasico en ambas manos con anillos dorados en Lirio nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Rojo y dorado" data-en="Red and gold">Rojo y dorado</span><img src="assets/raw/bk-4.jpg" alt="Diseno frances rojo y dorado con acento de corazon" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Punta neón" data-en="Neon tip">Punta neón</span><img src="assets/raw/bk-5.jpg" alt="Manicura con punta francesa amarillo neon" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Almendra pastel" data-en="Pastel almond">Almendra pastel</span><img src="assets/raw/bk-7.jpg" alt="Unas almendra en amarillo pastel" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Limpieza facial" data-en="Facial treatment">Limpieza facial</span><img src="assets/raw/bk-10.jpg" alt="Mascarilla facial amarilla durante tratamiento de limpieza profunda" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Cuidado de pestañas" data-en="Lash care">Cuidado de pestañas</span><img src="assets/raw/bk-11.jpg" alt="Tratamiento de pestañas y cejas, antes y despues" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 12. OPINIONES (reales, con autor) ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 18 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 18 verified reviews on Booksy">5.0 de 5 · 18 reseñas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Estupenda la atención, súper recomendada, muy amable y el servicio está muy top.. I love it ✨💅"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rachel G.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Es super creativa y perfecionista. Super. Estare regresando👏🏼"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Zalec S.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very good job and super detailed"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Natalia A.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 18 reseñas en Booksy" data-en="Read all 18 reviews on Booksy">Leer las 18 reseñas en Booksy</a>')
print("OPINIONES done")

# ---------- 13. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Miami</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">7801 Coral Wy #107, Miami, FL 33155</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=7801+Coral+Wy+%23107,+Miami,+FL+33155"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>')
rep('''<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(84,74,160,0.4)]" href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">''',
    '''<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(84,74,160,0.4)]" href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">''')
rep('''data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>''',
    '''data-es="Mira los diseños más recientes de Lilliana y escribe por DM cualquier duda antes de tu cita." data-en="See Lilliana's latest designs and DM any questions before your appointment.">Mira los diseños más recientes de Lilliana y escribe por DM cualquier duda antes de tu cita.</p>''')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Lirio nails, 7801 Coral Wy #107, Miami FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=7801+Coral+Wy+%23107,+Miami,+FL+33155&output=embed"')
print("UBICACION done")

# ---------- 14. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Como el lirio, tus manos florecen." data-en="Like the lily, your hands bloom.">Como el lirio, tus manos florecen.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tus próximas uñas" data-en="Your next nails">Tus próximas uñas</span> <span class="text-shine" data-es="te esperan" data-en="are waiting">te esperan</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu acrílico, tu Apres, tu Poly Gel o la limpieza facial que ya te toca." data-en="Book online in seconds: your acrylic, your Apres, your Poly Gel, or the facial you are due for.">Reserva en línea en segundos: tu acrílico, tu Apres, tu Poly Gel o la limpieza facial que ya te toca.</p>')
print("CTA FINAL done")

# ---------- 15. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Lirio Nails</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(194,190,240,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Lirio nails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(194,190,240,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Lirio Nails</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Miami, FL. Atención con cita previa." data-en="Nail salon in Miami, FL. By appointment only.">Salón de uñas en Miami, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>7801 Coral Wy #107, Miami, FL 33155</p>')
rep('<p><a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="hover:text-[#c2bef0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="hover:text-[#c2bef0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
assert '<p><a href="https://www.instagram.com/lirio_nails_99/" target="_blank" rel="noopener" class="hover:text-[#c2bef0]">Instagram · @lirio_nails_99</a></p>' in h
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lirio Nails.</p>')
print("FOOTER done")

# ---------- 16. book-float ----------
rep('<a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://booksy.com/en-us/1269129_lirio-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">')

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
