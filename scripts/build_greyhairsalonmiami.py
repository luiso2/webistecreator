import re
import os
import shutil
import colorsys

SLUG = "greyhairsalonmiami"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/dark-v2/index.html", f"output/{SLUG}/index.html")
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

# ---------- 2. Paleta: rotacion de matiz + desaturacion (gold -> bronze-taupe/mauve) ----------
# gold #d4a84b (H~41, S~0.61) -> shift -13 y desaturar x0.42 -> #ac8d73 (bronze-taupe calido)
HUE_SHIFT = -13.0
SAT_SCALE = 0.42


def shift_hex(hexcode):
    r = int(hexcode[0:2], 16) / 255.0
    g = int(hexcode[2:4], 16) / 255.0
    b = int(hexcode[4:6], 16) / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    s = max(0.0, min(1.0, s * SAT_SCALE))
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l, s)
    return '%02x%02x%02x' % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def shift_rgb_tuple(rr, gg, bb):
    r, g, b = rr / 255.0, gg / 255.0, bb / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    s = max(0.0, min(1.0, s * SAT_SCALE))
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
print("PALETTE done -> deep", shift_hex('d4a84b'), "mid", shift_hex('b8934a'))

# ---------- 3. Globales: Booksy, Instagram, handle ----------
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOKSY = 'https://booksy.com/en-us/830545_grey-hair-salon_hair-salon_15889_miami'
assert OLD_BOOKSY in h
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG = 'https://www.instagram.com/grey_hairestylistmiami/'
assert OLD_IG in h
h = h.replace(OLD_IG, NEW_IG)

OLD_HANDLE = '@pure.artistrysk'
NEW_HANDLE = '@grey_hairestylistmiami'
assert OLD_HANDLE in h
h = h.replace(OLD_HANDLE, NEW_HANDLE)
print("GLOBALS done")

# ---------- 4. HEAD: title, meta, JSON-LD, og:image ----------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Grey Hair Salon · Hair &amp; Nail Studio in Miami, FL | Grey Blending &amp; Keratin | 4.9 on Booksy</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Grey Hair Salon, Miami FL: grey blending, keratin treatments, signature haircuts and nail services. 4.9 with 64 reviews on Booksy. Book online." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Grey Hair Salon · Hair &amp; Nail Studio in Miami, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Grey blending, keratin treatments and nail services. 4.9 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />', '<meta property="og:image" content="assets/raw/bk-10.jpg" />')
# favicon: bk-2.jpg ya es el logo real de Grey Hair Salon, no requiere cambio de ruta.

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Grey Hair Salon",
    "description": "Hair and nail studio in Miami, FL: grey blending, keratin treatments, signature haircuts, balayage and nail services.",
    "address": { "@type": "PostalAddress", "streetAddress": "6578 SW 40th St", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33155", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.7332, "longitude": -80.30215 },
    "sameAs": ["https://booksy.com/en-us/830545_grey-hair-salon_hair-salon_15889_miami", "https://www.instagram.com/grey_hairestylistmiami/", "https://www.facebook.com/gretell.diez/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "64", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday", "Monday"], "opens": "10:00", "closes": "16:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:30", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Hair and nail services", "itemListElement": [
      { "@type": "Offer", "price": "350", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Keratin Treatment: Stem Cells by Ivera Paris" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Grey Blending Consultation" } },
      { "@type": "Offer", "price": "95", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Signature Haircut by Master Stylist" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Full Set" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------- 5. Idioma: dark-v2 ya es EN por defecto (no se toca) ----------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("LANG ok (EN default, sin cambios)")

# ---------- 6. PRELOADER ----------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">GH</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Grey Hair Salon</span>')

# ---------- 7. NAV ----------
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(172,141,115,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Grey Hair Salon" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(172,141,115,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Grey <span class="text-[color:var(--accent-deep)]">Hair Salon</span></span>')
print("NAV done")

# ---------- 8. HERO ----------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Miami, FL · Hair &amp; Nail Studio" data-en="Miami, FL · Hair &amp; Nail Studio">Miami, FL · Hair &amp; Nail Studio</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>\n        <h1',
    'data-es="Donde cada tono de canas se vuelve arte." data-en="Where every shade of grey becomes art.">Where every shade of grey becomes art.</p>\n        <h1')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Grey blending, color y" data-en="Grey blending, color and">Grey blending, color and</span><br /><span data-es="cortes hechos con " data-en="cuts crafted with ">cuts crafted with </span><span class="text-shine" data-es="arte" data-en="artistry">artistry</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    '''data-es="Grey blending, tratamientos de keratina, cortes de firma y servicios de uñas, todo bajo un mismo techo en Miami. Un 4.9 en 64 reseñas, liderado por la fundadora y colorista Gretell Diez." data-en="Grey blending, keratin treatments, signature haircuts and nail services, all under one roof in Miami. A 4.9 rating across 64 reviews, led by founder and colorist Gretell Diez.">Grey blending, keratin treatments, signature haircuts and nail services, all under one roof in Miami. A 4.9 rating across 64 reviews, led by founder and colorist Gretell Diez.</p>''')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.9 · 64 reseñas en Booksy" data-en="4.9 · 64 reviews on Booksy">4.9 · 64 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-10.jpg" alt="Clienta de espaldas con balayage y manos ajustando el cabello en Grey Hair Salon, Miami" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg" data-es="Grey Blending" data-en="Grey Blending">Grey Blending</p>')
rep('data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="Desde $90 · 1h" data-en="From $90 · 1h">From $90 · 1h</p>')
print("HERO done")

# ---------- 9. STRIP ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="64">64</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Hair <span class="text-shine">&amp;</span> Nails</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Grey blending · Keratina" data-en="Grey blending · Keratin">Grey blending · Keratin</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">29 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">SW 40th St</p></div>')
print("STRIP done")

# ---------- 10. MARQUEE (x4 cada palabra) ----------
for old, new in [
    ('Silk Press', 'Grey Blending'),
    ('Loc Retwist', 'Balayage'),
    ('Knotless Braids', 'Signature Cuts'),
    ('K-Tip Extensions', 'Nail Design'),
    ('Orlando, FL', 'Miami, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------- 11. EXPERIENCIA ----------
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Retrato de clienta con balayage cálido y sonrisa, en Grey Hair Salon" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Clienta con grey blending impecable, sonriendo en el salón" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Especialistas en" data-en="Specialists in">Specialists in</span><br /><span class="text-shine" data-es="grey blending" data-en="grey blending">grey blending</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    '''data-es="Grey Hair Salon es el estudio de Gretell Diez, fundadora y colorista principal, especializada en color avanzado, grey blending y transformaciones a medida. Junto a Ledieska Rodriguez, especialista en blowouts, cortes y tratamientos, el equipo atiende cabello y uñas en un mismo espacio en Miami." data-en="Grey Hair Salon is the studio of Gretell Diez, founder and lead colorist, specializing in advanced color, grey blending and customized transformations. Alongside Ledieska Rodriguez, a specialist in blowouts, haircuts and treatments, the team covers hair and nails under one roof in Miami.">Grey Hair Salon is the studio of Gretell Diez, founder and lead colorist, specializing in advanced color, grey blending and customized transformations. Alongside Ledieska Rodriguez, a specialist in blowouts, haircuts and treatments, the team covers hair and nails under one roof in Miami.</p>''')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus clientas lo confirman: un 4.9 en 64 reseñas verificadas en Booksy, y comentarios que destacan lo bien atendidas y hermosas que se sienten al salir." data-en="Her clients confirm it: a 4.9 across 64 verified Booksy reviews, with comments praising how well cared for and beautiful they feel leaving.">Her clients confirm it: a 4.9 across 64 verified Booksy reviews, with comments praising how well cared for and beautiful they feel leaving.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="64">64</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(172,141,115,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Grey Hair Salon" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(172,141,115,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="text-sm font-light">Grey Hair Salon · <span class="text-[color:var(--ink-40)]" data-es="El equipo" data-en="The team">The team</span></span>')
print("EXPERIENCIA done")

# ---------- 12. METODO ----------
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: grey blending, keratina, corte o uñas, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: grey blending, keratin, a haircut or nails, and confirm instantly.">Pick your service on Booksy with clear price and duration: grey blending, keratin, a haircut or nails, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta personalizada" data-en="Personal consult">Personal consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu cabello, sus canas y el resultado que buscas definen la técnica: el grey blending se piensa hebra por hebra." data-en="Your hair, its greys and the result you want define the technique: grey blending is planned strand by strand.">Your hair, its greys and the result you want define the technique: grey blending is planned strand by strand.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De la keratina de 3 horas al corte de firma de 1 hora: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 3-hour keratin treatment to the 1-hour signature haircut: every service gets its full time, no double booking, no rushing.">From the 3-hour keratin treatment to the 1-hour signature haircut: every service gets its full time, no double booking, no rushing.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el color, el corte o las uñas que buscabas, y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with the color, cut or nails you came in for, plus guidance to keep it that way at home. Next visit booked before you go.">You leave with the color, cut or nails you came in for, plus guidance to keep it that way at home. Next visit booked before you go.</p>''')
print("METODO done")

# ---------- 13. SERVICIOS ----------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Grey Hair Salon en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Grey Hair Salon on Booksy. Booking confirms instantly.">Prices and durations as published by Grey Hair Salon on Booksy. Booking confirms instantly.</p>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(172,141,115,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tratamiento premium" data-en="Premium treatment">Premium treatment</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Keratina: Stem Cells por Ivera Paris" data-en="Keratin: Stem Cells by Ivera Paris">Keratin: Stem Cells by Ivera Paris</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El tratamiento de keratina más solicitado de la casa, con células madre de Ivera Paris para un cabello liso, sano y con brillo real." data-en="The salon's most requested keratin treatment, with Ivera Paris stem cells for smooth, healthy hair with real shine.">The salon's most requested keratin treatment, with Ivera Paris stem cells for smooth, healthy hair with real shine.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$350</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h</p></div>
            <a href="https://booksy.com/en-us/830545_grey-hair-salon_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="La especialidad de la casa" data-en="House specialty">House specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Consulta de Grey Blending" data-en="Grey Blending Consultation">Grey Blending Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una técnica de color pensada para mezclar tus canas de forma natural, guiada por Gretell Diez, fundadora y colorista principal." data-en="A color technique designed to blend your greys naturally, guided by Gretell Diez, founder and lead colorist.">A color technique designed to blend your greys naturally, guided by Gretell Diez, founder and lead colorist.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/830545_grey-hair-salon_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Corte de firma" data-en="Signature cut">Signature cut</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte con Estilista Principal" data-en="Signature Haircut by Master Stylist">Signature Haircut by Master Stylist</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte de precisión con nuestra estilista principal, adaptado a la forma de tu rostro y a tu tipo de cabello." data-en="A precision cut with our master stylist, tailored to your face shape and hair type.">A precision cut with our master stylist, tailored to your face shape and hair type.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$95</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/830545_grey-hair-salon_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Uñas" data-en="Nails">Nails</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Set Completo de Acrílico" data-en="Acrylic Full Set">Acrylic Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrílico con acabado preciso y duradero. También disponible con French Design como adicional." data-en="A full acrylic set with a precise, long-lasting finish. Also available with a French Design add-on.">A full acrylic set with a precise, long-lasting finish. Also available with a French Design add-on.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p></div>
            <a href="https://booksy.com/en-us/830545_grey-hair-salon_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: manicura regular, blow dry, root touch-up, tratamiento de proteína y más. Menú completo de 29 servicios y disponibilidad en Booksy." data-en="Also: regular manicure, blow dry, root touch-ups, protein treatments and more. Full 29-service menu and availability on Booksy.">Also: regular manicure, blow dry, root touch-ups, protein treatments and more. Full 29-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# ---------- 14. GALERIA ----------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Acabado liso y brillante" data-en="Sleek, glossy finish">Sleek, glossy finish</span><img src="assets/raw/bk-9.jpg" alt="Cabello lacio y brillante con acabado editorial en Grey Hair Salon" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Balayage en tono rosado" data-en="Rose-toned balayage">Rose-toned balayage</span><img src="assets/raw/bk-3.jpg" alt="Cabello con balayage en tonos rosados vistos desde atrás" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Ondas con balayage cálido" data-en="Warm balayage waves">Warm balayage waves</span><img src="assets/raw/bk-11.jpg" alt="Ondas con balayage cálido y reflejos dorados" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Grey blending, la especialidad de la casa" data-en="Grey blending, the house specialty">Grey blending, the house specialty</span><img src="assets/raw/bk-14.jpg" alt="Primer plano de la raiz con canas mezcladas de forma natural, grey blending" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Color cobrizo" data-en="Copper color">Copper color</span><img src="assets/raw/bk-7.jpg" alt="Cabello con color cobrizo y reflejos vistos desde atrás" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Balayage y ondas" data-en="Balayage & waves">Balayage &amp; waves</span><img src="assets/raw/bk-12.jpg" alt="Primer plano de balayage con ondas sueltas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------- 15. OPINIONES ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What our">What our</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 64 reseñas verificadas en Booksy" data-en="4.9 out of 5 · 64 verified reviews on Booksy">4.9 out of 5 · 64 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Loved my appointment. Gretell was amazing through out the whole appointment and understood the style of cut I wanted."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Nancy U.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Staff was very nice and accommodating. I LOVE my nails, Dainet took her time and did an amazingly detailed job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Andrea B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Incredible servicio de uñas de Jessica! 10/10"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Daniela H.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/830545_grey-hair-salon_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/830545_grey-hair-salon_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 64 reseñas en Booksy" data-en="Read all 64 reviews on Booksy">Read all 64 reviews on Booksy</a>')
print("OPINIONES done")

# ---------- 16. UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">6578 SW 40th St, Miami, FL 33155</p>')
rep('href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806"',
    'href="https://www.google.com/maps?q=6578+SW+40th+St,+Miami,+FL+33155"')
rep('data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="Mira los trabajos más recientes de grey blending y color, y escribe por DM cualquier duda antes de tu cita." data-en="See the latest grey blending and color work, and DM any questions before your appointment.">See the latest grey blending and color work, and DM any questions before your appointment.</p>')
rep('title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"',
    'title="Mapa: Grey Hair Salon, 6578 SW 40th St, Miami FL"')
rep('src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    'src="https://www.google.com/maps?q=6578+SW+40th+St,+Miami,+FL+33155&output=embed"')
print("UBICACION done")

# ---------- 17. CTA FINAL ----------
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>\n      <h2',
    'data-es="Donde cada tono de canas se vuelve arte." data-en="Where every shade of grey becomes art.">Where every shade of grey becomes art.</p>\n      <h2')
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva en línea en segundos: tu consulta de grey blending, tu keratina, o el corte que llevas planeando." data-en="Book online in seconds: your grey blending consultation, your keratin treatment, or the cut you have been planning.">Book online in seconds: your grey blending consultation, your keratin treatment, or the cut you have been planning.</p>')
print("CTA FINAL done")

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Grey Hair Salon</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(208,190,174,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Grey Hair Salon" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(208,190,174,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Grey Hair Salon</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Salón de cabello y uñas en Miami, FL. Atención con cita previa." data-en="Hair and nail studio in Miami, FL. By appointment only.">Hair and nail studio in Miami, FL. By appointment only.</p>')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', '<p>6578 SW 40th St, Miami, FL 33155</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Grey Hair Salon.</p>')
print("FOOTER done")

# ---------- 19. book-float (URL ya reemplazada en el paso global) ----------
assert 'class="book-float"' in h
print("BOOK-FLOAT ok")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
