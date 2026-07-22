import re
import os
import shutil
import colorsys

SLUG = "nails-by-juliet-tampa"
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

# ---------- 2. Paleta: rotacion de matiz (HUE_SHIFT=64, plum-pink a04a72 -> gold/amber) ----------
HUE_SHIFT = 64.0


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

# ---------- 3. Globales: Booksy (replace all; no IG real, se maneja aparte) ----------
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)
print("GLOBALS done")

# ---------- 4. HEAD: title, meta, JSON-LD, favicon ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    "<title>Nails by Juliet · Nail Salon in Tampa, FL | 5.0 on Booksy</title>")
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Nails by Juliet, Tampa FL: manicure, pedicure, gel manicure, builder gel and Apres nail systems with a perfect 5.0 across 28 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Nails by Juliet · Nail Salon in Tampa, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicure, pedicure, gel and builder gel. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-16.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-8.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nails by Juliet",
    "description": "Nail salon in Tampa, FL: manicure, pedicure, gel manicure, builder gel and Apres nail systems.",
    "address": { "@type": "PostalAddress", "streetAddress": "1815 W Sligh Ave, Suite B", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33604", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.011060785318804, "longitude": -82.4783078882191 },
    "sameAs": ["https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "28", "bestRating": "5" },
    "openingHoursSpecification": [{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "09:30", "closes": "19:00" }],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel manicure" } },
      { "@type": "Offer", "price": "20", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure regular" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure Regular" } },
      { "@type": "Offer", "price": "55", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder Pedicura" } }
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
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NJ</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Nails by Juliet</span>')

# ---------- 7. NAV ----------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,126,74,0.35)]" />',
    '<img src="assets/raw/bk-8.jpg" alt="Nails by Juliet" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,126,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails <span class="text-[color:var(--accent-deep)]">by Juliet</span></span>')
print("NAV done")

# ---------- 8. HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tampa, FL · Salón de uñas" data-en="Tampa, FL · Nail Salon">Tampa, FL · Salón de uñas</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Elegancia dorada en cada uña." data-en="Golden elegance, nail by nail.">Elegancia dorada en cada uña.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicure, pedicure" data-en="Manicure, pedicure">Manicure, pedicure</span><br /><span data-es="y nail art, hechos para " data-en="and nail art, made to ">y nail art, hechos para </span><span class="text-shine" data-es="durar" data-en="last">durar</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '''data-es="Manicure regular, pedicure spa, gel y builder gel, de la mano de Juliet Lozano en su salón en Tampa, FL. Un 5.0 perfecto en 28 reseñas de Booksy." data-en="Regular manicure, spa pedicure, gel and builder gel, by Juliet Lozano in her salon in Tampa, FL. A perfect 5.0 across 28 Booksy reviews.">Regular manicure, spa pedicure, gel and builder gel, by Juliet Lozano in her salon in Tampa, FL. A perfect 5.0 across 28 Booksy reviews.</p>''')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 28 reseñas en Booksy" data-en="5.0 · 28 reviews on Booksy">5.0 · 28 reseñas en Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-16.jpg" alt="Uñas almendra nude con anillos dorados, terminado de Nails by Juliet" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Gel Manicure</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$35 · 1h" data-en="$35 · 1h">$35 · 1h</p>')
# Segundo boton del hero (era Instagram): no hay IG real, se redirige a Servicios
rep('''          <a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @_lashbloom
          </a>''',
    '''          <a href="#servicios" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg>
            <span data-es="Ver servicios" data-en="See services">Ver servicios</span>
          </a>''')
print("HERO done")

# ---------- 9. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="28">28</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Manicure <span class="text-shine">&amp;</span> Pedicure</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicios completos" data-en="Full services">Servicios completos</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">11 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Menú completo en Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W Sligh Ave</p></div>')
print("STRIP done")

# ---------- 10. MARQUEE (x4 cada palabra) ----------
for old, new in [
    ('Classic Set', 'Manicure Gel'),
    ('Hybrid Set', 'Pedicure Spa'),
    ('Volume Set', 'Builder Gel'),
    ('Mega Volume', 'Apres Nails'),
    ('Bottom Lashes', 'Acrílic Remove'),
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
    '<img src="assets/raw/bk-8.jpg" alt="Uñas almendra nude con anillos dorados, cerca y elegante" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Mano con anillos dorados y uñas nude, terminado de Nails by Juliet" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un salón" data-en="A salon">Un salón</span><br /><span class="text-shine" data-es="detallista y personal" data-en="that is detailed and personal">detallista y personal</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '''data-es="Nails by Juliet es el salón de Juliet Lozano, en Tampa, FL. Sus clientas la describen como profesional, detallista y rápida, con un trabajo impecable en cada cita." data-en="Nails by Juliet is Juliet Lozano's salon in Tampa, FL. Her clients describe her as professional, detail-oriented and fast, with impeccable work at every visit.">Nails by Juliet is Juliet Lozano's salon in Tampa, FL. Her clients describe her as professional, detail-oriented and fast, with impeccable work at every visit.</p>''')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 28 reseñas verificadas en Booksy, y clientas que aseguran que sus uñas siguen luciendo bien semanas después." data-en="The result: a perfect 5.0 across 28 verified Booksy reviews, and clients who say their nails still look great weeks later.">The result: a perfect 5.0 across 28 verified Booksy reviews, and clients who say their nails still look great weeks later.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="28">28</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,126,74,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-8.jpg" alt="Nails by Juliet" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,126,74,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Juliet · <span class="text-[color:var(--ink-40)]" data-es="Manicurista" data-en="Nail artist">Nail artist</span></span>')
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
    '''          <h3 class="font-display text-xl mb-3" data-es="Elige el sistema" data-en="Choose the system">Elige el sistema</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Manicure regular, gel, builder gel, pedicure spa o el sistema Apres: Juliet te ayuda a elegir según lo que buscas." data-en="Regular manicure, gel, builder gel, spa pedicure or the Apres system: Juliet helps you choose based on what you're looking for.">Manicure regular, gel, builder gel, pedicure spa o el sistema Apres: Juliet te ayuda a elegir según lo que buscas.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Trabajo detallista" data-en="Detailed work">Trabajo detallista</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Juliet se toma su tiempo para perfeccionar cada uña, con un servicio profesional y cuidado." data-en="Juliet takes her time to perfect every nail, with professional and careful service.">Juliet se toma su tiempo para perfeccionar cada uña, con un servicio profesional y cuidado.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">Salida</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con uñas limpias, cuidadas y hermosas, listas para tu próxima cita." data-en="You leave with nails that are clean, cared for and beautiful, ready for your next appointment.">Sales con uñas limpias, cuidadas y hermosas, listas para tu próxima cita.</p>''')
print("METODO done")

# ---------- 13. SERVICIOS ----------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Nails by Juliet en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Nails by Juliet on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Nails by Juliet en Booksy. Reserva con confirmación inmediata.</p>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Todos los días" data-en="Everyday">Todos los días</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Regular" data-en="Regular Manicure">Manicure Regular</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure clásica con esmaltado tradicional, para unas manos cuidadas todos los días." data-en="Classic manicure with traditional polish, for everyday cared-for hands.">Manicure clásica con esmaltado tradicional, para unas manos cuidadas todos los días.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$20</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">20min</p></div>
            <a href="https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,126,74,0.4); box-shadow: 0 18px 50px rgba(51,42,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Favorito del salón</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel Manicure" data-en="Gel Manicure">Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El gel de larga duración de Nails by Juliet, con acabado brillante que dura semanas." data-en="Nails by Juliet's long-lasting gel, with a glossy finish that lasts for weeks.">El gel de larga duración de Nails by Juliet, con acabado brillante que dura semanas.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies cuidados" data-en="Cared-for feet">Pies cuidados</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pedicure Regular" data-en="Regular Pedicure">Pedicure Regular</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicure regular con cuidado completo del pie, para después de un día largo." data-en="Regular pedicure with full foot care, perfect after a long day.">Pedicure regular con cuidado completo del pie, para después de un día largo.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">45min</p></div>
            <a href="https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Resistencia" data-en="Durability">Resistencia</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Builder Pedicura" data-en="Builder Pedicure">Builder Pedicura</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Builder gel resistente aplicado en pedicure, para un acabado duradero." data-en="Durable builder gel applied to a pedicure, for a long-lasting finish.">Builder gel resistente aplicado en pedicure, para un acabado duradero.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$55</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">45min</p></div>
            <a href="https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: pedí gel, builder gel, acrílic remove, apres nails corto y largo, pedicure spa y volcano spa pedicure. Menú completo de 11 servicios y disponibilidad en Booksy." data-en="Also available: gel pedi, builder gel, acrylic removal, short and long apres nails, spa pedicure and volcano spa pedicure. Full 11-service menu and availability on Booksy.">También: pedí gel, builder gel, acrílic remove, apres nails corto y largo, pedicure spa y volcano spa pedicure. Menú completo de 11 servicios y disponibilidad en Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 14. GALERIA ----------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Trabajo</span> <span class="text-shine" data-es="real" data-en="nail work">real</span>')

# El link junto al titulo de la galeria era Instagram: no hay IG real, se redirige a Booksy
rep('''        <a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @_lashbloom
        </a>''',
    '''        <a href="https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>''')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño dorado sobre césped" data-en="Gold dotted design on grass">Diseño dorado sobre césped</span><img src="assets/raw/bk-6.jpg" alt="Diseño de uñas con pecas doradas y naranjas sobre fondo de césped, terminado de Nails by Juliet" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Nude y dorado con joyería" data-en="Nude and gold with jewelry">Nude y dorado con joyería</span><img src="assets/raw/bk-11.jpg" alt="Uñas nude y doradas junto a joyería sobre tela blanca, terminado de Nails by Juliet" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Gel lila en el auto" data-en="Lilac gel in the car">Gel lila en el auto</span><img src="assets/raw/bk-12.jpg" alt="Uñas en gel color lila, mano apoyada en el interior de un auto" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Nail art nude con anillos" data-en="Nude nail art with rings">Nail art nude con anillos</span><img src="assets/raw/bk-13.jpg" alt="Uñas nude con nail art elaborado y varios anillos dorados" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Francesa clásica con anillos" data-en="Classic French with rings">Francesa clásica con anillos</span><img src="assets/raw/bk-14.jpg" alt="Uñas con manicure francesa clásica y anillos sobre tela oscura" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Nude con anillos, luz suave" data-en="Nude with rings, soft light">Nude con anillos, luz suave</span><img src="assets/raw/bk-15.jpg" alt="Uñas nude con anillos dorados, iluminación suave" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 15. OPINIONES ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 28 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 28 verified reviews on Booksy">5.0 de 5 · 28 reseñas verificadas en Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Love them every time 💓💓"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ayshalinette P.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Juliet did a wonderful job. My nails still look great 2 weeks later."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jennifer M.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Espectacular el servicio y ame el resultado es la mejor"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Clarislenys R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 28 reseñas en Booksy" data-en="Read all 28 reviews on Booksy">Leer las 28 reseñas en Booksy</a>')
print("OPINIONES done")

# ---------- 16. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Tampa</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1815 W Sligh Ave, Suite B, Tampa, FL 33604</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=1815+W+Sligh+Ave,+Suite+B,+Tampa,+FL+33604"')

# La tercera tarjeta era Instagram: no hay IG real, se reemplaza por el Horario real
rep('''          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener">@_lashbloom</a>
            </div>
          </div>''',
    '''          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Horario</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sábado, 9:30 am a 7:00 pm. Cerrado los domingos." data-en="Monday to Saturday, 9:30 am to 7:00 pm. Closed Sundays.">Lunes a sábado, 9:30 am a 7:00 pm. Cerrado los domingos.</p>
            </div>
          </div>''')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Nails by Juliet, 1815 W Sligh Ave, Tampa FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=1815+W+Sligh+Ave,+Suite+B,+Tampa,+FL+33604&output=embed"')
print("UBICACION done")

# ---------- 17. CTA FINAL ----------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Elegancia dorada en cada uña." data-en="Golden elegance, nail by nail.">Elegancia dorada en cada uña.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Tu próxima cita</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en línea en segundos: tu manicure, tu pedicure o el servicio que ya te toca." data-en="Book online in seconds: your manicure, your pedicure, or the service you are due for.">Reserva en línea en segundos: tu manicure, tu pedicure o el servicio que ya te toca.</p>')
# Boton secundario del CTA era "Seguir en Instagram": no hay IG real, se elimina y queda solo el CTA principal
rep('''      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>
      </div>''',
    '''      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="https://booksy.com/en-us/1725013_nails-by-juliet_nail-salon_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
      </div>''')
print("CTA FINAL done")

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Nails by Juliet</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,218,190,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-8.jpg" alt="Nails by Juliet" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,218,190,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Nails by Juliet</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Tampa, FL. Atención con cita previa." data-en="Nail salon in Tampa, FL. By appointment only.">Salón de uñas en Tampa, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>1815 W Sligh Ave, Suite B, Tampa, FL 33604</p>')
# La columna "Siguenos" con Instagram no aplica (no hay IG real): se reemplaza por Horario real
rep('''      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @_lashbloom</a></p>
      </div>''',
    '''      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Horario" data-en="Hours">Horario</p>
        <p data-es="Lun a sáb: 9:30 am - 7:00 pm" data-en="Mon to Sat: 9:30 am - 7:00 pm">Lun a sáb: 9:30 am - 7:00 pm</p>
        <p data-es="Cerrado los domingos" data-en="Closed Sundays">Cerrado los domingos</p>
      </div>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Nails by Juliet.</p>')
print("FOOTER done")

# ---------- 19. book-float (URL ya reemplazada en el paso global) ----------
assert 'class="book-float"' in h
assert 'instagram.com' not in h, "quedo un link de Instagram sin reemplazar"
assert '_lashbloom' not in h, "quedo un handle de IG sin reemplazar"
print("BOOK-FLOAT ok / sin restos de Instagram")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
