import re, os, shutil, colorsys

SLUG = "kais-beauty-boutique-miramar"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/dark-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, 1)


def rep_all(a, b, n=None):
    global h
    cnt = h.count(a)
    assert cnt > 0, "NO ANCHOR (all): " + a[:120]
    if n is not None:
        assert cnt == n, f"expected {n} got {cnt}: {a[:80]}"
    h = h.replace(a, b)


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop (dorado) antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. PALETA: gold-on-black (Pure Artistry) -> rosewood/champagne-rose-on-black
#    (Miramar luxury lash & brow studio: black leather chairs, grey marble,
#    gold jewelry in the real photos -> rose-gold on black fits the brand)
#    Derivado por rotacion de matiz (hue -48deg, saturacion x0.72) sobre cada
#    tono dorado del esqueleto, preservando luminancia para el contraste.
# ---------------------------------------------------------------------------
def rot_hex(hexcode, deg=-48, s_mult=0.72, l_add=0.0):
    hx = hexcode.lstrip('#')
    r, g, b = (int(hx[i:i + 2], 16) for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hh = (hh + deg / 360.0) % 1.0
    s = max(0, min(1, s * s_mult))
    l = max(0, min(1, l + l_add))
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l, s)
    return '#%02x%02x%02x' % tuple(round(c * 255) for c in (r2, g2, b2))


GOLD_HEXES = [
    "#d4a84b", "#b8934a", "#e9c3ab", "#8a744a", "#f0dc9e", "#e8cf96",
    "#e8c476", "#e5c374", "#c9a04a", "#9a7431", "#96742c", "#241c0e",
    "#6b5222", "#faf1dc", "#f8eed3", "#f0dcae", "#ecd9a8", "#c9ab6b",
    "#bfa060", "#fbf6ea",
]
PALETTE = [(hx, rot_hex(hx)) for hx in GOLD_HEXES]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_TRIOS = [
    ((212, 168, 75), (193, 94, 106)),
    ((232, 207, 150), (221, 161, 168)),
    ((80, 58, 18), (71, 27, 34)),
    ((110, 85, 35), (100, 45, 53)),
]
for (r, g, b), (r2, g2, b2) in RGBA_TRIOS:
    h = h.replace(f"rgba({r},{g},{b}", f"rgba({r2},{g2},{b2}")

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. GLOBALES: Acuity (booking), Instagram
# ---------------------------------------------------------------------------
BOOK = "https://kaisbeautyboutique.as.me/"
assert 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando' in h
rep_all('https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando', BOOK)
assert 'https://www.instagram.com/pure.artistrysk/' in h
rep_all('https://www.instagram.com/pure.artistrysk/', 'https://www.instagram.com/kaisbeautyboutique/')
rep_all('@pure.artistrysk', '@kaisbeautyboutique')
print("GLOBALES done")

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    "<title>Kai's Beauty Boutique · Lash &amp; Brow Studio in Miramar, FL | 5.0 on Google</title>")
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Kai\'s Beauty Boutique, Miramar FL: classic and mega volume lash extensions, brow lamination and hybrid tint. 5.0 with 28 reviews on Google. Book online." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Kai\'s Beauty Boutique · Lash &amp; Brow Studio in Miramar, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Lash extensions, brow lamination and tint. 5.0 on Google. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />', '<meta property="og:image" content="assets/raw/bk-12.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-12.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Kai's Beauty Boutique LLC",
    "description": "Lash and brow studio in Miramar, FL: classic and mega volume lash extensions, lash refills, brow lamination, hybrid tint and brow sculpting.",
    "telephone": "+1-954-408-2605",
    "email": "kaisbeautyboutique@gmail.com",
    "address": { "@type": "PostalAddress", "streetAddress": "8910 Miramar Pkwy, Ste 201E", "addressLocality": "Miramar", "addressRegion": "FL", "postalCode": "33025", "addressCountry": "US" },
    "sameAs": ["https://kaisbeautyboutique.as.me/", "https://www.instagram.com/kaisbeautyboutique/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "28", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "10:00", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Lash & brow services", "itemListElement": [
      { "@type": "Offer", "price": "140", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Soft Signature Classic Set" } },
      { "@type": "Offer", "price": "170", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Signature Luxe Mega Classic" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brow Lamination" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brow Sculpt (Wax)" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------------------------------------------------------------------------
# PRELOADER / NAV
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">KBB</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Kai\'s Beauty Boutique</span>')

rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />'.replace("212,168,75", "193,94,106"),
    '<img src="assets/raw/bk-2.jpg" alt="Kai\'s Beauty Boutique" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(193,94,106,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Kai\'s <span class="text-[color:var(--accent-deep)]">Beauty</span></span>')
print("NAV done")

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Miramar, FL · Lash &amp; Brow Studio" data-en="Miramar, FL · Lash &amp; Brow Studio">Miramar, FL · Lash &amp; Brow Studio</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>\n        <h1',
    'data-es="Miramar\'s #1 luxury lash and brow studio." data-en="Miramar\'s #1 luxury lash and brow studio.">Miramar\'s #1 luxury lash and brow studio.</p>\n        <h1')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Extensiones de pestañas y" data-en="Lash extensions and brow">Lash extensions and brow</span><br /><span data-es="cejas, hechas para " data-en="artistry, done to ">artistry, done to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Sets clásicos y Signature Luxe Mega, laminado de cejas con tinte híbrido, todo aplicado por Alex en un estudio pensado para relajarte. Un 5.0 perfecto en 28 reseñas de Google respalda cada cita." data-en="Classic and Signature Luxe Mega sets, brow lamination with hybrid tint, all applied by Alex in a studio built to help you unwind. A perfect 5.0 across 28 Google reviews backs every appointment.">Classic and Signature Luxe Mega sets, brow lamination with hybrid tint, all applied by Alex in a studio built to help you unwind. A perfect 5.0 across 28 Google reviews backs every appointment.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 28 reseñas en Google" data-en="5.0 · 28 reviews on Google">5.0 · 28 reviews on Google</span>
        </div>
''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-12.jpg" alt="Clienta con extensiones de pestañas terminadas en Kai\'s Beauty Boutique, Miramar" class="blur-up w-full h-full object-cover" />')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar en Acuity" data-en="Book on Acuity">Reservar en Acuity</span>')
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg" data-es="Signature Luxe Mega Classic" data-en="Signature Luxe Mega Classic">Signature Luxe Mega Classic</p>')
rep('data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="$170 · 2h 30min" data-en="$170 · 2h 30min">$170 · 2h 30min</p>')
print("HERO done")

# ---------------------------------------------------------------------------
# STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="28">28</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Lash <span class="text-shine">&amp;</span> Brow</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones · Laminado · Tinte" data-en="Extensions · Lamination · Tint">Extensions · Lamination · Tint</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">13 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Acuity" data-en="Full menu on Acuity">Full menu on Acuity</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miramar</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Miramar Pkwy</p></div>')

for old, new in [
    ('Silk Press', 'Signature Luxe Mega'),
    ('Loc Retwist', 'Brow Lamination'),
    ('Knotless Braids', 'Hybrid Tint'),
    ('K-Tip Extensions', 'Lash Extensions'),
    ('Keratin', 'Brow Sculpt'),
    ('Orlando, FL', 'Miramar, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("STRIP+MARQUEE done")

# ---------------------------------------------------------------------------
# LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Ambiente relajado durante un servicio de cejas en Kai\'s Beauty Boutique" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Diseño de cejas en proceso en Kai\'s Beauty Boutique" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    """data-es="Kai's Beauty Boutique es el estudio de pestañas y cejas de Miramar donde Alex diseña cada set y cada laminado a la medida de tu mirada, en una suite privada pensada para que salgas relajada y renovada." data-en="Kai's Beauty Boutique is Miramar's lash and brow studio, where Alex designs every set and lamination around your eyes, in a private suite built to send you home relaxed and renewed.">Kai's Beauty Boutique is Miramar's lash and brow studio, where Alex designs every set and lamination around your eyes, in a private suite built to send you home relaxed and renewed.</p>""")
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus clientas lo confirman: profesionalismo, ambiente relajado y una retención de pestañas que se nota. 5.0 perfecto en 28 reseñas verificadas de Google." data-en="Her clients confirm it: professionalism, a relaxed studio and lash retention that shows. A perfect 5.0 across 28 verified Google reviews.">Her clients confirm it: professionalism, a relaxed studio and lash retention that shows. A perfect 5.0 across 28 verified Google reviews.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="28">28</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />'.replace("212,168,75", "193,94,106"),
    """<img src="assets/raw/bk-9.jpg" alt="Kai's Beauty Boutique, estudio" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(193,94,106,0.3)]" loading="lazy" />""")
rep('<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="text-sm font-light">Kai\'s Beauty Boutique · <span class="text-[color:var(--ink-40)]" data-es="Estudio de pestañas y cejas" data-en="Lash &amp; brow studio">Lash &amp; brow studio</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# EL METODO
# ---------------------------------------------------------------------------
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Acuity con precio y duración claros: set clásico, Signature Luxe Mega, laminado o tinte, y confirmas al instante." data-en="Pick your service on Acuity with clear price and duration: classic set, Signature Luxe Mega, lamination or tint, and confirm instantly.">Pick your service on Acuity with clear price and duration: classic set, Signature Luxe Mega, lamination or tint, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta" data-en="Consultation">Consultation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="La forma de tu ojo o ceja y el efecto que buscas definen el set o el laminado, tal como lo pregunta el formulario de Kai\'s Beauty Boutique." data-en="Your eye or brow shape and the effect you want define the set or lamination, just like Kai\'s Beauty Boutique intake form asks.">Your eye or brow shape and the effect you want define the set or lamination, just like Kai's Beauty Boutique intake form asks.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="La aplicación" data-en="The application">The application</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas y cierras los ojos mientras Alex trabaja pestaña por pestaña: hasta 2h 30min para un set Signature Luxe Mega Classic." data-en="You lie back and close your eyes while Alex works lash by lash: up to 2h 30min for a Signature Luxe Mega Classic set.">You lie back and close your eyes while Alex works lash by lash: up to 2h 30min for a Signature Luxe Mega Classic set.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida lista" data-en="Ready to go">Ready to go</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el set o el laminado terminado y, si aplica, tu relleno de 2 a 3 semanas ya agendado." data-en="You leave with your set or lamination finished and, if needed, your 2 to 3 week fill already booked.">You leave with your set or lamination finished and, if needed, your 2 to 3 week fill already booked.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# SERVICIOS
# ---------------------------------------------------------------------------
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Kai\'s Beauty Boutique en Acuity. Reserva con confirmación inmediata." data-en="Prices and durations as published by Kai\'s Beauty Boutique on Acuity. Booking confirms instantly.">Prices and durations as published by Kai\'s Beauty Boutique on Acuity. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(193,94,106,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Signature Luxe Mega Classic" data-en="Signature Luxe Mega Classic">Signature Luxe Mega Classic</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El set mas denso y dramatico de la casa, aplicado pestaña por pestaña para un efecto luxe a proposito." data-en="The studio's densest, most dramatic set, applied lash by lash for a deliberate luxe effect.">The studio's densest, most dramatic set, applied lash by lash for a deliberate luxe effect.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$170</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para empezar" data-en="New to lashes">New to lashes</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Soft Signature Classic Set" data-en="Soft Signature Classic Set">Soft Signature Classic Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un set clasico y suave, una extension por pestaña natural, para una mirada definida sin exagerar." data-en="A soft, classic set, one extension per natural lash, for a defined look without going too far.">A soft, classic set, one extension per natural lash, for a defined look without going too far.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$140</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito de cejas" data-en="Brow favorite">Brow favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Brow Lamination &amp; Hybrid Tint" data-en="Brow Lamination &amp; Hybrid Tint">Brow Lamination &amp; Hybrid Tint</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Laminado que peina cada pelito en su lugar, combinado con tinte hibrido para cejas llenas y definidas por semanas." data-en="Lamination that sets every hair in place, combined with hybrid tint for full, defined brows that last for weeks.">Lamination that sets every hair in place, combined with hybrid tint for full, defined brows that last for weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$120</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extra rapido" data-en="Quick add-on">Quick add-on</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Bottom Lashes" data-en="Bottom Lashes">Bottom Lashes</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extensiones para el parpado inferior que enmarcan la mirada completa, ideal para sumar a cualquier set." data-en="Lower lash extensions that frame the whole eye, an easy add-on to any set.">Lower lash extensions that frame the whole eye, an easy add-on to any set.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$55</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">25min</p></div>
            <a href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

old_note = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>'
assert old_note in h
CATEGORY_BLOCKS = '''<div class="grid sm:grid-cols-2 gap-5 mt-10">
        <div class="glass rounded-3xl p-7 reveal">
          <h3 class="font-display text-xl mb-4" data-es="Extensiones de Pestañas" data-en="Eyelash Extensions">Eyelash Extensions</h3>
          <ul class="space-y-2.5 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span data-es="Soft Signature Classic Set · 2h 30min" data-en="Soft Signature Classic Set · 2h 30min">Soft Signature Classic Set · 2h 30min</span><span class="text-[color:var(--ink)] font-medium">$140</span></li>
            <li class="flex justify-between gap-3"><span data-es="Soft Signature Classic Refill · 2h" data-en="Soft Signature Classic Refill · 2h">Soft Signature Classic Refill · 2h</span><span class="text-[color:var(--ink)] font-medium">$90</span></li>
            <li class="flex justify-between gap-3"><span data-es="Signature Luxe Mega Classic · 2h 30min" data-en="Signature Luxe Mega Classic · 2h 30min">Signature Luxe Mega Classic · 2h 30min</span><span class="text-[color:var(--ink)] font-medium">$170</span></li>
            <li class="flex justify-between gap-3"><span data-es="Signature Luxe Mega Refill · 2h" data-en="Signature Luxe Mega Refill · 2h">Signature Luxe Mega Refill · 2h</span><span class="text-[color:var(--ink)] font-medium">$100</span></li>
            <li class="flex justify-between gap-3"><span data-es="Bottom Lashes · 25min" data-en="Bottom Lashes · 25min">Bottom Lashes · 25min</span><span class="text-[color:var(--ink)] font-medium">$55</span></li>
            <li class="flex justify-between gap-3"><span data-es="Lash Removal · 20min" data-en="Lash Removal · 20min">Lash Removal · 20min</span><span class="text-[color:var(--ink)] font-medium">$45</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:90ms">
          <h3 class="font-display text-xl mb-4" data-es="Cejas" data-en="Brows">Brows</h3>
          <ul class="space-y-2.5 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex justify-between gap-3"><span data-es="Brow Sculpt (Wax) · 40min" data-en="Brow Sculpt (Wax) · 40min">Brow Sculpt (Wax) · 40min</span><span class="text-[color:var(--ink)] font-medium">$30</span></li>
            <li class="flex justify-between gap-3"><span data-es="Hybrid Tint (Sculpt) · 1h" data-en="Hybrid Tint (Sculpt) · 1h">Hybrid Tint (Sculpt) · 1h</span><span class="text-[color:var(--ink)] font-medium">$60</span></li>
            <li class="flex justify-between gap-3"><span data-es="Brow Lamination · 1h" data-en="Brow Lamination · 1h">Brow Lamination · 1h</span><span class="text-[color:var(--ink)] font-medium">$90</span></li>
            <li class="flex justify-between gap-3"><span data-es="Brow Lamination &amp; Hybrid Tint · 1h" data-en="Brow Lamination &amp; Hybrid Tint · 1h">Brow Lamination &amp; Hybrid Tint · 1h</span><span class="text-[color:var(--ink)] font-medium">$120</span></li>
            <li class="flex justify-between gap-3"><span data-es="Upper Lip Wax · 5min" data-en="Upper Lip Wax · 5min">Upper Lip Wax · 5min</span><span class="text-[color:var(--ink)] font-medium">$10</span></li>
            <li class="flex justify-between gap-3"><span data-es="Chin Wax · 10min" data-en="Chin Wax · 10min">Chin Wax · 10min</span><span class="text-[color:var(--ink)] font-medium">$15</span></li>
            <li class="flex justify-between gap-3"><span data-es="Upper Lip &amp; Chin Wax Combo · 20min" data-en="Upper Lip &amp; Chin Wax Combo · 20min">Upper Lip &amp; Chin Wax Combo · 20min</span><span class="text-[color:var(--ink)] font-medium">$20</span></li>
          </ul>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 13 servicios completos, con Afterpay y Klarna disponibles, en Acuity." data-en="All 13 services, with Afterpay and Klarna available, on Acuity.">All 13 services, with Afterpay and Klarna available, on Acuity.</span></p>'''
h = h.replace(old_note, CATEGORY_BLOCKS, 1)
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="results">results</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Extensiones terminadas" data-en="Finished lash extensions">Finished lash extensions</span><img src="assets/raw/bk-2.jpg" alt="Clienta con extensiones de pestañas terminadas en Kai's Beauty Boutique" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Cejas recien esculpidas" data-en="Freshly sculpted brows">Freshly sculpted brows</span><img src="assets/raw/bk-11.jpg" alt="Clienta con cejas recien esculpidas en Kai's Beauty Boutique" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Laminado de cejas" data-en="Brow lamination">Brow lamination</span><img src="assets/raw/bk-3.jpg" alt="Resultado de laminado de cejas en Kai's Beauty Boutique" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Cejas definidas con tinte" data-en="Brows defined with tint">Brows defined with tint</span><img src="assets/raw/bk-5.jpg" alt="Cejas laminadas y con tinte en Kai's Beauty Boutique" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Set clásico terminado" data-en="Finished classic set">Finished classic set</span><img src="assets/raw/bk-8.jpg" alt="Set clasico de pestañas terminado en Kai's Beauty Boutique" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Detalle de ceja laminada" data-en="Laminated brow detail">Laminated brow detail</span><img src="assets/raw/bk-9.jpg" alt="Detalle de ceja laminada y con tinte en Kai's Beauty Boutique" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# OPINIONES (reales, con autor, fuente Google)
# ---------------------------------------------------------------------------
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 28 reseñas verificadas en Google" data-en="5.0 out of 5 · 28 verified reviews on Google">5.0 out of 5 · 28 verified reviews on Google</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Alex did my lashes, she is very professional, knowledgeable and informative. The booking process on the website was a breeze, all instructions/details were clear. Definitely a great environment, great service and I love the way my lashes came out and retention has been great!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ms. G.</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great customer service, very friendly and sweet. I felt so relaxed getting my eyebrows done, she added a quick face massage and I wanted to take a nap! Definitely recommend her"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Brianna AE</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Thank you, Alex, for being so patient. I like the way you took the time to explain the process and care for my lashes. They look fabulous! I will be back."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Annie Foster</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="https://reviews.birdeye.com/kais-beauty-boutique-170259548764575" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 28 reseñas" data-en="Read all 28 reviews">Read all 28 reviews</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# UBICACION
# ---------------------------------------------------------------------------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miramar</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">8910 Miramar Pkwy, Ste 201E, Miramar, FL 33025</p>')
rep('href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806"',
    'href="https://www.google.com/maps?q=8910+Miramar+Pkwy,+Miramar,+FL+33025"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
    'data-es="Con cita previa vía Acuity, martes a sábado de 10am a 7pm. Cerrado lunes y domingo." data-en="By appointment via Acuity, Tuesday to Saturday 10am to 7pm. Closed Monday and Sunday.">By appointment via Acuity, Tuesday to Saturday 10am to 7pm. Closed Monday and Sunday.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>'.replace("212,168,75", "193,94,106"),
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(193,94,106,0.4)]" href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" data-es="Reservar en Acuity" data-en="Book on Acuity">Book on Acuity</a>')
rep('data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="Mira los sets y laminados más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest sets and laminations and DM any questions before your appointment.">See the latest sets and laminations and DM any questions before your appointment.</p>')
rep('title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"',
    'title="Map: Kai\'s Beauty Boutique, 8910 Miramar Pkwy, Miramar FL"')
rep('src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    'src="https://www.google.com/maps?q=8910+Miramar+Pkwy,+Miramar,+FL+33025&output=embed"')
print("UBICACION done")

# ---------------------------------------------------------------------------
# CTA FINAL
# ---------------------------------------------------------------------------
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>\n      <h2',
    'data-es="Miramar\'s #1 luxury lash and brow studio." data-en="Miramar\'s #1 luxury lash and brow studio.">Miramar\'s #1 luxury lash and brow studio.</p>\n      <h2')
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva en línea en segundos: tu set clásico, tu Signature Luxe Mega o el laminado de cejas que ya te toca." data-en="Book online in seconds: your classic set, your Signature Luxe Mega, or the brow lamination you are due for.">Book online in seconds: your classic set, your Signature Luxe Mega, or the brow lamination you are due for.</p>')
rep('<a href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Acuity" data-en="Book on Acuity">Book on Acuity</a>')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Kai\'s Beauty Boutique</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(221,161,168,0.35)]" loading="lazy" />',
    """<img src="assets/raw/bk-2.jpg" alt="Kai's Beauty Boutique" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(221,161,168,0.35)]" loading="lazy" />""")
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Kai\'s Beauty Boutique</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Lash &amp; brow studio en Miramar, FL. Atención con cita previa." data-en="Lash &amp; brow studio in Miramar, FL. By appointment only.">Lash &amp; brow studio in Miramar, FL. By appointment only.</p>')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', '<p>8910 Miramar Pkwy, Ste 201E, Miramar, FL 33025</p>')
rep('<p><a href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'.replace("e9c3ab", "e0b4c6"),
    '<p><a href="https://kaisbeautyboutique.as.me/" target="_blank" rel="noopener" class="hover:text-[#e0b4c6]" data-es="Reservas online · Acuity" data-en="Online booking · Acuity">Online booking · Acuity</a></p>')
rep('<p><a href="https://www.instagram.com/kaisbeautyboutique/" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · @kaisbeautyboutique</a></p>'.replace("e9c3ab", "e0b4c6"),
    '<p><a href="https://www.instagram.com/kaisbeautyboutique/" target="_blank" rel="noopener" class="hover:text-[#e0b4c6]">Instagram · @kaisbeautyboutique</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Kai\'s Beauty Boutique.</p>')
print("FOOTER done")

# Idioma: negocio en ingles -> default en, coincide con el esqueleto (sin cambios)

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
