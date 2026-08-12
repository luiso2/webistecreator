import re, os, shutil

SLUG = "star-struck-nails-sarasota"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/dark-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, 1)


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop (dorado SIEMPRE)
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: gold (Pure Artistry) -> deep magenta / rose-fuchsia
#    (paleta NUEVA, no repite mizu/amani/mare/alea/pausa ni las ya usadas en
#    los batches v2: coral fairy, caramelo, esmeralda, teal acero, violeta
#    dark, rosa dark, gold dark original)
# ---------------------------------------------------------------------------
PALETTE = [
    ("#0f0b07", "#130a10"),
    ("#171207", "#1d0f18"),
    ("#f5efe3", "#f6ecf1"),
    ("#d4a84b", "#a13d6f"),
    ("#b8934a", "#c96fa0"),
    ("#241c0e", "#2b1220"),
    ("#f0dc9e", "#f3c9de"),
    ("#9a7431", "#6f1f45"),
    ("#e5c374", "#e0a0c4"),
    ("#e8c476", "#e8a0c8"),
    ("#c9a04a", "#c9528f"),
    ("#96742c", "#7a2350"),
    ("#1c1408", "#2a0e1c"),
    ("#6b5222", "#5c1a3d"),
    ("#e9c3ab", "#e3a8c8"),
    ("#8a744a", "#7a3155"),
    ("#faf1dc", "#fbe6f0"),
    ("#ecd9a8", "#eab8d4"),
    ("#c9ab6b", "#b3568e"),
    ("#e8cf96", "#e8a8c8"),
    ("#f8eed3", "#fbe6f0"),
    ("#bfa060", "#9c4a72"),
    ("#f0dcae", "#f0c2da"),
    ("#fbf6ea", "#fbeef4"),
    ("#191307", "#200a16"),
    ("#100c05", "#150a10"),
    ("#0c0905", "#12080e"),
]
for old, new in PALETTE:
    assert old in h, "PALETTE MISS: " + old
    h = h.replace(old, new)

# rgba() families: reemplazo por PREFIJO (sin cerrar parentesis) para cubrir
# TODAS las variantes de alpha de una sola vez.
RGBA_PREFIXES = [
    ("rgba(212,168,75,", "rgba(161,61,111,"),
    ("rgba(122,90,30,", "rgba(122,30,90,"),
    ("rgba(180,140,60,", "rgba(180,60,140,"),
    ("rgba(245,239,227,", "rgba(246,236,241,"),
    ("rgba(80,58,18,", "rgba(90,20,55,"),
    ("rgba(54,42,38,", "rgba(60,20,40,"),
    ("rgba(15,11,7,", "rgba(19,10,16,"),
    ("rgba(232,210,160,", "rgba(232,150,200,"),
    ("rgba(232,207,150,", "rgba(232,150,200,"),
    ("rgba(185,138,128,", "rgba(185,128,160,"),
    ("rgba(110,85,35,", "rgba(120,40,80,"),
]
for old, new in RGBA_PREFIXES:
    assert old in h, "RGBA MISS: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: Booksy, IG/handle -> no hay IG confirmado, no queda ningun
#    @handle de IG en el HTML (se sustituye por Facebook / telefono real).
# ---------------------------------------------------------------------------
OLD_BOOKSY = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_BOOKSY = "https://booksy.com/en-us/8054_star-struck-nails_nail-salon_134767_sarasota"
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

FACEBOOK_URL = "https://www.facebook.com/StarStruckNailsinGulfGateKimmieBSalon"
PHONE_DISPLAY = "(941) 549-8871"
PHONE_TEL = "tel:+19415498871"

print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, OG, favicon, JSON-LD (NailSalon)
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Star Struck Nails · Nail Salon in Sarasota, FL | Gulf Gate | 5.0 on Booksy</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Star Struck Nails, Sarasota FL (Gulf Gate): full sets, pink and white, gel polish and spa pedicures inside Kimmie B\'s Salon since 1994. 5.0 with 36 reviews on Booksy. Book online." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Star Struck Nails · Nail Salon in Sarasota, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Full sets, pink and white, gel polish and spa pedicures. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />', '<meta property="og:image" content="assets/raw/bk-7.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Star Struck Nails",
    "description": "Nail salon in Sarasota, FL (Gulf Gate), operating since 1994 inside Kimmie B's Salon. Acrylic full sets, pink and white, gel polish, nail art and spa pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "6637 Superior Ave, Suite A (inside Kimmie B's Salon)", "addressLocality": "Sarasota", "addressRegion": "FL", "postalCode": "34231", "addressCountry": "US" },
    "telephone": "+1-941-549-8871",
    "geo": { "@type": "GeoCoordinates", "latitude": 27.25936, "longitude": -82.51532 },
    "sameAs": ["https://booksy.com/en-us/8054_star-struck-nails_nail-salon_134767_sarasota", "https://www.facebook.com/StarStruckNailsinGulfGateKimmieBSalon"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "36", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "10:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "10:00", "closes": "15:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Star Struck Full Set" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pink & White Full Set" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Spa Pedicure With Mask" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Polish Manicure" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio en ingles = idioma por defecto del esqueleto (EN). No
#    hace falta tocar <html lang> ni applyLang default.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 6. PRELOADER + NAV
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">SS</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Star Struck Nails</span>')

rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />'.replace("212,168,75", "161,61,111"),
    '<img src="assets/raw/bk-2.jpg" alt="Star Struck Nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(161,61,111,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Star <span class="text-[color:var(--accent-deep)]">Struck</span> Nails</span>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Sarasota, FL · Salon de Uñas" data-en="Sarasota, FL · Nail Salon">Sarasota, FL · Nail Salon</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Uñas que te dejan fascinada." data-en="Nails that leave you star struck.">Nails that leave you star struck.</p>')
rep('''          <span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>''',
    '''          <span data-es="Acrílico, pink and white" data-en="Acrylics, pink &amp; white">Acrylics, pink &amp; white</span><br /><span data-es="y gel, bien hechos " data-en="and gel, done right ">and gel, done right </span><span class="text-shine" data-es="desde 1994" data-en="since 1994">since 1994</span>''')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Un estudio privado de uñas dentro de Kimmie B\'s Salon en Gulf Gate, atendido por Star y Ciara desde 1994. Full sets, pink and white, gel polish y pedicura spa, con un 5.0 perfecto en 36 reseñas en Booksy." data-en="A private nail studio inside Kimmie B\'s Salon in Gulf Gate, run by Star and Ciara since 1994. Full sets, pink and white, gel polish and spa pedicures, with a perfect 5.0 across 36 Booksy reviews.">A private nail studio inside Kimmie B\'s Salon in Gulf Gate, run by Star and Ciara since 1994. Full sets, pink and white, gel polish and spa pedicures, with a perfect 5.0 across 36 Booksy reviews.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 36 reseñas en Booksy" data-en="5.0 · 36 reviews on Booksy">5.0 · 36 reviews on Booksy</span>
        </div>
''')
rep('''          <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @pure.artistrysk
          </a>''',
    f'''          <a href="{PHONE_TEL}" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <span data-es="Llamar {PHONE_DISPLAY}" data-en="Call {PHONE_DISPLAY}">Call {PHONE_DISPLAY}</span>
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-7.jpg" alt="Pink glitter almond nail set at Star Struck Nails, Sarasota" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg" data-es="Star Struck Full Set" data-en="Star Struck Full Set">Star Struck Full Set</p>')
rep('data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="$70 · 1h 30min" data-en="$70 · 1h 30min">$70 · 1h 30min</p>')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="36">36</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Full Sets <span class="text-shine">&amp;</span> Pink White</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Acrílico · Gel · Pedicura" data-en="Acrylic · Gel · Pedicure">Acrylic · Gel · Pedicure</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">32 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="En Gulf Gate desde 1994" data-en="In Gulf Gate since 1994">In Gulf Gate since 1994</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Sarasota</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Superior Ave</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra debe aparecer 4 veces en total)
# ---------------------------------------------------------------------------
for old, new in [
    ('Silk Press', 'Full Sets'),
    ('Loc Retwist', 'Pink &amp; White'),
    ('Knotless Braids', 'Gel Polish'),
    ('K-Tip Extensions', 'Nail Art'),
    ('Keratin', 'Spa Pedicure'),
    ('Orlando, FL', 'Sarasota, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Classic french tip acrylic set at Star Struck Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Glitter stiletto nails with gems at Star Struck Nails" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="desde 1994" data-en="since 1994">since 1994</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Star Struck Nails es el estudio de uñas de Star y Ciara, dentro de Kimmie B\'s Salon en el barrio de Gulf Gate. Atendiendo desde 1994, con acrílico, pink and white, gel y diseños hechos a mano en un ambiente tranquilo y privado." data-en="Star Struck Nails is Star and Ciara\'s nail studio, inside Kimmie B\'s Salon in the Gulf Gate neighborhood. Open since 1994, with acrylic, pink and white, gel and hand-painted nail art in a calm, private setting.">Star Struck Nails is Star and Ciara\'s nail studio, inside Kimmie B\'s Salon in the Gulf Gate neighborhood. Open since 1994, with acrylic, pink and white, gel and hand-painted nail art in a calm, private setting.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus clientas lo confirman: reseñas que la describen como la mejor artista de esculpido en acrílico del estado. 5.0 perfecto en 36 reseñas verificadas de Booksy." data-en="Her clients confirm it: reviews that describe her as the best acrylic sculpting nail artist around. A perfect 5.0 across 36 verified Booksy reviews.">Her clients confirm it: reviews that describe her as the best acrylic sculpting nail artist around. A perfect 5.0 across 36 verified Booksy reviews.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="36">36</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />'.replace("212,168,75", "161,61,111"),
    '<img src="assets/raw/bk-2.jpg" alt="Star Struck Nails logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(161,61,111,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="text-sm font-light">Star &amp; Ciara · <span class="text-[color:var(--ink-40)]" data-es="Desde 1994" data-en="Since 1994">Since 1994</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>')
rep('data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: full set, pink and white, gel o pedicura, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: full set, pink and white, gel or pedicure, and confirm instantly.">Pick your service on Booksy with clear price and duration: full set, pink and white, gel or pedicure, and confirm instantly.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de uñas" data-en="Nail consult">Nail consult</h3>')
rep('data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    'data-es="La forma, el largo y el sistema que buscas (acrílico, pink and white, gel) definen la técnica antes de empezar." data-en="Your preferred shape, length and system (acrylic, pink and white, gel) define the technique before we start.">Your preferred shape, length and system (acrylic, pink and white, gel) define the technique before we start.</p>')
rep('data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    'data-es="Del cambio de esmalte de 15 minutos al full set de 1h 30: cada servicio recibe su tiempo completo, sin citas dobles." data-en="From a 15-minute polish change to a 1h 30min full set: every service gets its full time, no double booking, no rushing.">From a 15-minute polish change to a 1h 30min full set: every service gets its full time, no double booking, no rushing.</p>')
rep('data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    'data-es="Sales con tu set terminado y las indicaciones para cuidarlo en casa. Tu próximo relleno queda agendado antes de irte." data-en="You leave with your finished set and the guidance to keep it that way at home. Your next fill is booked before you go.">You leave with your finished set and the guidance to keep it that way at home. Your next fill is booked before you go.</p>')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (destacados + menu completo agrupado, TODO VISIBLE, sin
#     acordeones, con los 25 servicios reales de data.json)
# ---------------------------------------------------------------------------
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Star Struck Nails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Star Struck Nails on Booksy. Booking confirms instantly.">Prices and durations as published by Star Struck Nails on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="set" data-en="set">set</span>')

services_block = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*'
    r'<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">.*?</p>',
    h, flags=re.S)
assert services_block, "services block not found"

NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(161,61,111,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Star Struck Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El set que le da nombre al salon: acrilico esculpido a mano, listo para lucirse." data-en="The set the salon is named after: hand-sculpted acrylic, ready to show off.">The set the salon is named after: hand-sculpted acrylic, ready to show off.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especialidad" data-en="Specialty">Specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pink &amp; White Full Set" data-en="Pink &amp; White Full Set">Pink &amp; White Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un clasico de manicura francesa esculpido a mano. Relleno disponible desde $50, 1h 15min." data-en="A hand-sculpted take on the classic French manicure. Backfill available from $50, 1h 15min.">A hand-sculpted take on the classic French manicure. Backfill available from $50, 1h 15min.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pedicura" data-en="Pedicure">Pedicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Spa Pedicure With Mask" data-en="Spa Pedicure With Mask">Spa Pedicure With Mask</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La pedicura completa: remojo, exfoliacion, mascarilla y masaje. Version express de 30 minutos desde $35." data-en="The full pedicure ritual: soak, scrub, mask and massage. A 30-minute express version is available from $35.">The full pedicure ritual: soak, scrub, mask and massage. A 30-minute express version is available from $35.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito" data-en="Popular">Popular</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gel Polish Manicure" data-en="Gel Polish Manicure">Gel Polish Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura regular con gel polish de larga duracion. Solo gel polish en manos desde $20." data-en="A regular manicure finished with long-lasting gel polish. Gel polish on hands only is available from $20.">A regular manicure finished with long-lasting gel polish. Gel polish on hands only is available from $20.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Precio fijo" data-en="Flat rate">Flat rate</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-8">
        <div class="glass rounded-3xl p-7 reveal">
          <h3 class="font-display text-lg mb-4 text-[color:var(--accent-deep)]" data-es="Manicura &amp; Esmalte" data-en="Manicure &amp; Polish">Manicure &amp; Polish</h3>
          <div class="space-y-2.5 text-sm text-[color:var(--ink-60)] font-light">
            <div class="flex justify-between gap-3"><span data-es="Manicura regular" data-en="Reg. Manicure">Reg. Manicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$30 · 30min</span></div>
            <div class="flex justify-between gap-3"><span data-es="Solo cambio de esmalte (manos)" data-en="Hands Polish Change Only">Hands Polish Change Only</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$15 · 15min</span></div>
            <div class="flex justify-between gap-3"><span data-es="Solo gel polish (manos)" data-en="Gel Polish Hands Only">Gel Polish Hands Only</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$20</span></div>
            <div class="flex justify-between gap-3"><span data-es="Gel polish" data-en="Gel polish">Gel polish</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$20</span></div>
            <div class="flex justify-between gap-3"><span data-es="Cambio de esmalte (pies)" data-en="Toe Polish Change">Toe Polish Change</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$20</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:80ms">
          <h3 class="font-display text-lg mb-4 text-[color:var(--accent-deep)]" data-es="Pedicura" data-en="Pedicure">Pedicure</h3>
          <div class="space-y-2.5 text-sm text-[color:var(--ink-60)] font-light">
            <div class="flex justify-between gap-3"><span data-es="Pedicura" data-en="Pedicure">Pedicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$55</span></div>
            <div class="flex justify-between gap-3"><span data-es="Pedicura express 30 min" data-en="30 min express pedicure">30 min express pedicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$35</span></div>
            <div class="flex justify-between gap-3"><span data-es="Pedicura con gel polish" data-en="Gel polish Pedicure">Gel polish Pedicure</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$65</span></div>
            <div class="flex justify-between gap-3"><span data-es="Cambio de gel polish (pies)" data-en="Gel Toes Polish Change Only">Gel Toes Polish Change Only</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$25 · 30min</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:160ms">
          <h3 class="font-display text-lg mb-4 text-[color:var(--accent-deep)]" data-es="Acrílico, Gel &amp; Rellenos" data-en="Acrylic, Gel &amp; Fills">Acrylic, Gel &amp; Fills</h3>
          <div class="space-y-2.5 text-sm text-[color:var(--ink-60)] font-light">
            <div class="flex justify-between gap-3"><span data-es="Set completo regular" data-en="Reg. Full set">Reg. Full set</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$55</span></div>
            <div class="flex justify-between gap-3"><span data-es="Relleno regular con esmalte" data-en="Reg. Fill with polish">Reg. Fill with polish</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$40</span></div>
            <div class="flex justify-between gap-3"><span data-es="Relleno Pink &amp; White" data-en="Backfill Pink &amp; White">Backfill Pink &amp; White</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$50 · 1h 15min</span></div>
            <div class="flex justify-between gap-3"><span data-es="Relleno Star Struck" data-en="Star Struck Nails Backfill">Star Struck Nails Backfill</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$55</span></div>
            <div class="flex justify-between gap-3"><span data-es="Set completo acrílico en pies" data-en="Acrylic Toes Full Set">Acrylic Toes Full Set</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$45 · 40min</span></div>
            <div class="flex justify-between gap-3"><span data-es="Relleno acrílico en pies" data-en="Acrylic Toe Fill">Acrylic Toe Fill</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$35</span></div>
            <div class="flex justify-between gap-3"><span data-es="Gel X" data-en="Gel X">Gel X</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$40</span></div>
            <div class="flex justify-between gap-3"><span data-es="Relleno Gel X" data-en="Gel X Fill">Gel X Fill</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$40</span></div>
            <div class="flex justify-between gap-3"><span data-es="Retiro" data-en="Removal">Removal</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$25 · 30min</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:240ms">
          <h3 class="font-display text-lg mb-4 text-[color:var(--accent-deep)]" data-es="Extras" data-en="Extras">Extras</h3>
          <div class="space-y-2.5 text-sm text-[color:var(--ink-60)] font-light">
            <div class="flex justify-between gap-3"><span data-es="Arte en uñas" data-en="Nail Art">Nail Art</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$5 · 15min</span></div>
            <div class="flex justify-between gap-3"><span data-es="Reparación de uña" data-en="Nail Repair">Nail Repair</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$5 · 15min</span></div>
            <div class="flex justify-between gap-3"><span data-es="Pamper" data-en="Pamper">Pamper</span><span class="text-[color:var(--ink-40)] whitespace-nowrap">$30 · 30min</span></div>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 25 servicios que ves arriba son el menú completo de Star Struck Nails en Booksy, con disponibilidad y confirmación al instante." data-en="The 25 services above are Star Struck Nails\' full Booksy menu, with availability and instant confirmation.">The 25 services above are Star Struck Nails' full Booksy menu, with availability and instant confirmation.</span></p>'''

NEW_SERVICES = NEW_SERVICES.replace("__BOOKSY__", NEW_BOOKSY)
h = h[:services_block.start()] + NEW_SERVICES + h[services_block.end():]
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (solo bk-3, bk-4, bk-6, bk-7, bk-9: 5 fotos reales, sin
#     selfies ni fotos borrosas, PIPELINE.md: menos fotos buenas > relleno)
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')
rep('''        <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @pure.artistrysk
        </a>''',
    f'''        <a href="{FACEBOOK_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          <span data-es="Facebook" data-en="Facebook">Facebook</span>
        </a>''')

gallery_block = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_block, "gallery block not found"
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño de mariposa en verde" data-en="Butterfly art in green">Butterfly art in green</span><img src="assets/raw/bk-3.jpg" alt="Green stiletto acrylic nails with hand-painted butterfly art at Star Struck Nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Puntas francesas clásicas" data-en="Classic french tips">Classic french tips</span><img src="assets/raw/bk-4.jpg" alt="Classic french tip acrylic nail set at Star Struck Nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Stiletto con pedrería" data-en="Stiletto glam with gems">Stiletto glam with gems</span><img src="assets/raw/bk-6.jpg" alt="Glitter stiletto nails with rhinestone gems at Star Struck Nails" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Set almendra glitter rosa" data-en="Pink glitter almond set">Pink glitter almond set</span><img src="assets/raw/bk-7.jpg" alt="Pink glitter almond acrylic nail set at Star Struck Nails" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Pedicura spa con glitter" data-en="Glitter spa pedicure">Glitter spa pedicure</span><img src="assets/raw/bk-9.jpg" alt="Colorful glitter spa pedicure at Star Struck Nails" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_block.start()] + NEW_GALLERY + h[gallery_block.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES (3 reseñas verbatim reales de data.json)
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 36 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 36 verified reviews on Booksy">5.0 out of 5 · 36 verified reviews on Booksy</span></p>')

reviews_block = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_block, "reviews block not found"
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"amazing place to get your nails done. no feeling like you're being rushed, private setting. nail work is on point! been going here for about 4-5 years now...never been disappointed!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yvette H…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The absolute best acrylic sculpting nail artist in the state! 100% impressed by her talents, technique and consistency. Each nail was sculpted with perfection! I am grateful for finding Ciara at Star Struck Nails in SRQ! 🙌💅"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karen W…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"All was great. I will go again."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ilona H…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_block.start()] + NEW_REVIEWS + h[reviews_block.end():]

# OJO: el href ya quedo en NEW_BOOKSY por el replace global del paso 3.
rep(f'<a href="{NEW_BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    f'<a href="{NEW_BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 36 reseñas en Booksy" data-en="Read all 36 reviews on Booksy">Read all 36 reviews on Booksy</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION (direccion real, mapa embed, telefono click-to-call en vez
#     de Instagram ya que no hay handle confirmado)
# ---------------------------------------------------------------------------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Sarasota</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">6637 Superior Ave, Suite A (inside Kimmie B\'s Salon), Sarasota, FL 34231</p>')
rep('href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806"',
    'href="https://www.google.com/maps?q=6637+Superior+Ave,+Sarasota,+FL+34231"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener">@pure.artistrysk</a>
            </div>
          </div>'''.replace("212,168,75", "161,61,111"),
    f'''          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Teléfono" data-en="Phone">Phone</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Llama para preguntas rápidas o para confirmar disponibilidad el mismo día." data-en="Call for quick questions or to check same-day availability.">Call for quick questions or to check same-day availability.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(161,61,111,0.4)]" href="{PHONE_TEL}">{PHONE_DISPLAY}</a>
            </div>
          </div>''')
rep('title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"',
    'title="Map: Star Struck Nails, 6637 Superior Ave, Sarasota FL"')
rep('src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    'src="https://www.google.com/maps?q=6637+Superior+Ave,+Sarasota,+FL+34231&output=embed"')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Uñas que te dejan fascinada." data-en="Nails that leave you star struck.">Nails that leave you star struck.</p>')
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva en línea en segundos: tu full set, tu pink and white o esa pedicura spa que llevas planeando." data-en="Book online in seconds: your full set, your pink and white, or that spa pedicure you have been planning.">Book online in seconds: your full set, your pink and white, or that spa pedicure you have been planning.</p>')
rep('<a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    f'<a href="{PHONE_TEL}" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Llamar {PHONE_DISPLAY}" data-en="Call {PHONE_DISPLAY}">Call {PHONE_DISPLAY}</a>')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Star Struck Nails</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />'.replace("232,207,150", "232,150,200"),
    '<img src="assets/raw/bk-2.jpg" alt="Star Struck Nails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,150,200,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Star Struck Nails</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Gulf Gate, Sarasota, FL. Atención con cita previa." data-en="Nail salon in Gulf Gate, Sarasota, FL. By appointment only.">Nail salon in Gulf Gate, Sarasota, FL. By appointment only.</p>')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', '<p>6637 Superior Ave, Suite A, Sarasota, FL 34231</p>')
rep(f'<p><a href="{NEW_BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'.replace("e9c3ab", "e3a8c8"),
    f'<p><a href="{NEW_BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#e3a8c8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · @pure.artistrysk</a></p>'.replace("e9c3ab", "e3a8c8"),
    f'<p><a href="{FACEBOOK_URL}" target="_blank" rel="noopener" class="hover:text-[#e3a8c8]">Facebook · Star Struck Nails</a></p>\n        <p><a href="{PHONE_TEL}" class="hover:text-[#e3a8c8]">{PHONE_DISPLAY}</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Star Struck Nails.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante de reserva (book-float) -> ya apunta a NEW_BOOKSY por
#     el replace global del paso 3.
# ---------------------------------------------------------------------------

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
