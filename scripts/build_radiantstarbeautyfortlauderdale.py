import re

SLUG = 'radiant-star-beauty-fort-lauderdale'
PATH = f'output/{SLUG}/index.html'
h = open(PATH).read()


def rep(a, b, n=1):
    global h
    assert h.count(a) >= n, 'NO ANCHOR (want >=%d, got %d): %s' % (n, h.count(a), a[:100])
    h = h.replace(a, b, n)


def rep_exact(a, b, n):
    global h
    c = h.count(a)
    assert c == n, 'COUNT MISMATCH (want %d, got %d): %s' % (n, c, a[:100])
    h = h.replace(a, b)


# =========================================================================
# 1) PROTEGER EL BADGE MERKTOP (queda dorado siempre)
# =========================================================================
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'no se encontro el bloque merktop-badge'
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# =========================================================================
# 2) PALETA: plum-pink -> gold/champagne (marca real: estrella dorada, crema,
#    blush, bandas negras en antes/despues)
# =========================================================================
HEX_PAIRS = [
    ('#a04a72', '#ab7d2f'),
    ('#5c2140', '#5c3f12'),
    ('#f0bed7', '#f0d9a0'),
    ('#faf2f6', '#faf5ec'),
    ('#c47a9c', '#cf9f52'),
    ('#8a5573', '#8a6a30'),
    ('#f3e0ea', '#f1e2c9'),
    ('#d9a8c2', '#d9b579'),
    ('#7d3457', '#7a561d'),
    ('#5f2c48', '#6e4d1a'),
    ('#33222c', '#33281c'),
    ('#fbf3f8', '#fbf3e6'),
    ('#fbeff5', '#fbf3e2'),
    ('#f8dfeb', '#f8ecd0'),
    ('#f6f1ea', '#faf5ec'),
    ('#f2d5e3', '#f2e2c0'),
    ('#f2cfe0', '#f2e0b0'),
    ('#efd0e0', '#efd9a8'),
    ('#e5c1d4', '#eed9ad'),
    ('#dc9dbe', '#e0bf7a'),
    ('#d3a2bc', '#cf9f52'),
    ('#c9789f', '#d4ac66'),
    ('#b25a85', '#c0923f'),
    ('#2a1722', '#241a0d'),
    ('#1f0f18', '#170f06'),
    ('#1c0f16', '#150e07'),
]
for old, new in HEX_PAIRS:
    n = h.count(old)
    assert n > 0, 'hex no encontrado: ' + old
    h = h.replace(old, new)

RGBA_PAIRS = [
    ('rgba(160,74,114', 'rgba(171,125,47'),
    ('rgba(51,34,44', 'rgba(51,40,28'),
    ('rgba(240,190,215', 'rgba(240,217,160'),
    ('rgba(70,25,50', 'rgba(90,60,20'),
    ('rgba(250,242,246', 'rgba(250,244,232'),
    ('rgba(125,52,87', 'rgba(110,80,30'),
    ('rgba(253,246,250', 'rgba(255,251,242'),
    ('rgba(40,16,30', 'rgba(35,24,10'),
    ('rgba(233,205,186', 'rgba(230,200,140'),
    ('rgba(185,138,128', 'rgba(185,148,88'),
]
for old, new in RGBA_PAIRS:
    n = h.count(old)
    assert n > 0, 'rgba no encontrado: ' + old
    h = h.replace(old, new)

# restaurar el badge (siempre dorado, intacto)
assert '@@BADGE@@' in h
h = h.replace('@@BADGE@@', badge_block, 1)

print('OK paso 1-2: badge protegido + paleta aplicada')

# =========================================================================
# 3) GLOBALES: Booksy URL, IG url/handle, FB url
# =========================================================================
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/523310_radiant-star-beauty_skin-care_15643_fort-lauderdale'
n = h.count(OLD_BOOKSY)
assert n > 0, n
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
NEW_IG_URL = 'https://www.instagram.com/radiantstarbeauty/'
n = h.count(OLD_IG_URL)
assert n > 0, n
h = h.replace(OLD_IG_URL, NEW_IG_URL)

n = h.count('@_lashbloom')
assert n > 0, n
h = h.replace('@_lashbloom', '@radiantstarbeauty')

print('OK paso 3: globales (booksy/ig)')

# =========================================================================
# 4) HEAD: title, meta description, og, JSON-LD, theme-color
# =========================================================================
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Radiant Star Beauty · Lash, Facial &amp; Brow Studio in Fort Lauderdale, FL | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Radiant Star Beauty in Fort Lauderdale, FL: lash extensions, custom facials and brow waxing with a perfect 5.0 across 53 Booksy reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Radiant Star Beauty · Lash, Facial &amp; Brow Studio in Fort Lauderdale, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Lash extensions, custom facials and brow waxing. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/client-smile.jpg" />',
)
old_jsonld_m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert old_jsonld_m
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Radiant Star Beauty",
    "description": "Lash, facial and brow studio in Fort Lauderdale, FL: lash extensions, custom facials and waxing.",
    "address": { "@type": "PostalAddress", "streetAddress": "4390 N Federal Hwy, Suite 207", "addressLocality": "Fort Lauderdale", "addressRegion": "FL", "postalCode": "33308", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 26.1822703, "longitude": -80.1188835 },
    "sameAs": ["https://booksy.com/en-us/523310_radiant-star-beauty_skin-care_15643_fort-lauderdale", "https://www.instagram.com/radiantstarbeauty/", "https://www.facebook.com/RadiantStarBeauty/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "53", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Thursday"], "opens": "10:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday", "Friday"], "opens": "10:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "10:00", "closes": "16:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Lash, facial and brow services", "itemListElement": [
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic Lashes" } },
      { "@type": "Offer", "price": "126", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Volume Set" } },
      { "@type": "Offer", "price": "162", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Mega Volume Lashes" } },
      { "@type": "Offer", "price": "135", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Radiant Star Luxe Facial Experience" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld_m.group(0), new_jsonld, 1)
print('OK paso 4: head + json-ld')

# =========================================================================
# 5) PRELOADER + NAV + LOGO ALT
# =========================================================================
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">RS</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Radiant Star</span>')

n = h.count('alt="Lash Bloom"')
assert n == 3, n
h = h.replace('alt="Lash Bloom"', 'alt="Radiant Star Beauty"')

rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Radiant <span class="text-[color:var(--accent-deep)]">Star</span></span>',
)

print('OK paso 5: preloader + nav')

# =========================================================================
# 6) HERO
# =========================================================================
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio<',
    'data-es="Fort Lauderdale, FL · Estudio de Pestañas y Faciales" data-en="Fort Lauderdale, FL · Lash &amp; Facial Studio">Fort Lauderdale, FL &middot; Lash &amp; Facial Studio<',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.<',
    'data-es="Donde la estrella brilla más fuerte." data-en="Where the star glows the brightest.">Where the star glows the brightest.<',
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Pestañas, faciales" data-en="Lashes, facials">Lashes, facials</span><br /><span data-es="y cejas, hechos para " data-en="and brows, made to ">and brows, made to </span><span class="text-shine" data-es="brillar" data-en="glow">glow</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.<',
    'data-es="Sets completos de pestañas clásicas, híbridas, volumen y mega volumen, faciales personalizados como el Radiant Star Luxe Facial Experience, y diseño de cejas y depilación, de la mano de una esteticista licenciada en un suite privado en Fort Lauderdale." data-en="Full classic, hybrid, volume and mega volume lash sets, custom facials like the Radiant Star Luxe Facial Experience, and brow shaping and waxing, all from one licensed esthetician in a private Fort Lauderdale suite.">Full classic, hybrid, volume and mega volume lash sets, custom facials like the Radiant Star Luxe Facial Experience, and brow shaping and waxing, all from one licensed esthetician in a private Fort Lauderdale suite.<',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy<',
    'data-es="5.0 · 53 reseñas en Booksy" data-en="5.0 · 53 reviews on Booksy">5.0 &middot; 53 reviews on Booksy<',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/hero-face.jpg" alt="Okami, esthetician at Radiant Star Beauty, in her Fort Lauderdale studio" class="blur-up w-full h-full object-cover" />',
)
rep(
    '<p class="font-display text-lg">Volume Full Set</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="font-display text-lg">Radiant Star Luxe Facial</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$135 · 1h 10min" data-en="$135 · 1h 10min">$135 &middot; 1h 10min</p>',
)
print('OK paso 6: hero')

# =========================================================================
# 7) STRIP DE CONFIANZA
# =========================================================================
rep(
    '<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-count="53">53</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
)
rep(
    '<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p>',
    '<p class="font-display text-2xl">Lash <span class="text-shine">&amp;</span> Facial</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Faciales" data-en="Full sets · Facials">Full sets &middot; Facials</p>',
)
rep(
    '<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p>',
    '<p class="font-display text-2xl"><span class="text-shine" data-count="25">25</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicios en el menú" data-en="Services on the menu">Services on the menu</p>',
)
rep(
    '<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p>',
    '<p class="font-display text-2xl">Fort Lauderdale</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4390 N Federal Hwy</p>',
)
print('OK paso 7: strip')

# =========================================================================
# 8) MARQUEE (palabras x4 cada una, en 2 bloques)
# =========================================================================
MARQ = [
    ('Classic Set', 'Classic Lashes'),
    ('Hybrid Set', 'Custom Facials'),
    ('Mega Volume', 'Brow Waxing'),
    ('Bottom Lashes', 'Okami Esthetics'),
    ('West Palm Beach, FL', 'Fort Lauderdale, FL'),
]
for old, new in MARQ:
    old_full = f'<span class="marquee-word">{old}</span>'
    new_full = f'<span class="marquee-word">{new}</span>'
    n = h.count(old_full)
    assert n == 4, (old, n)
    h = h.replace(old_full, new_full)
print('OK paso 8: marquee')

# =========================================================================
# 9) LA EXPERIENCIA
# =========================================================================
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/hero-hands.jpg" alt="Okami realizando un facial personalizado en Radiant Star Beauty" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/result-braids.jpg" alt="Resultado de pestañas y cejas terminado en Radiant Star Beauty" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un estudio privado" data-en="A private studio">A private studio</span><br /><span class="text-shine" data-es="hecho para brillar" data-en="made to glow">made to glow</span>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.<',
    'data-es="Radiant Star Beauty es el estudio de la esteticista licenciada Okami, dentro de un suite privado en el 4390 N Federal Hwy en Fort Lauderdale. Cada set de pestañas, facial y servicio de cejas se personaliza, desde un set clásico hasta el Radiant Star Luxe Facial Experience." data-en="Radiant Star Beauty is the studio of licensed esthetician Okami, inside a private suite at 4390 N Federal Hwy in Fort Lauderdale. Every lash set, facial and brow service is personalized, from a classic set to the signature Radiant Star Luxe Facial Experience.">Radiant Star Beauty is the studio of licensed esthetician Okami, inside a private suite at 4390 N Federal Hwy in Fort Lauderdale. Every lash set, facial and brow service is personalized, from a classic set to the signature Radiant Star Luxe Facial Experience.<',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.<',
    'data-es="Las clientas describen una silla de masaje con manta calientita durante los faciales, respuestas rápidas al reservar, y una esteticista que explica exactamente qué necesitan tu piel y tus pestañas. El resultado: un 5.0 perfecto en 53 reseñas verificadas en Booksy." data-en="Clients describe a heated massage chair and a warm blanket during facials, fast responses when booking, and an esthetician who explains exactly what your skin and lashes need. The result: a perfect 5.0 across 53 verified Booksy reviews.">Clients describe a heated massage chair and a warm blanket during facials, fast responses when booking, and an esthetician who explains exactly what your skin and lashes need. The result: a perfect 5.0 across 53 verified Booksy reviews.<',
)
rep(
    '<span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<span data-count="53">53</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
)
rep(
    '<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Okami · <span class="text-[color:var(--ink-40)]" data-es="Esteticista licenciada" data-en="Licensed esthetician">Licensed esthetician</span></span>',
)
print('OK paso 9: experiencia')

# =========================================================================
# 10) EL METODO
# =========================================================================
rep(
    '<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, de principio" data-en="Your visit, start to">Your visit, start to</span> <span class="text-shine" data-es="a fin" data-en="finish">finish</span>',
)
rep(
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.<',
    'data-es="Eliges tu set de pestañas, facial o depilación en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your lash set, facial or wax on Booksy with clear pricing and duration, and confirm instantly.">Pick your lash set, facial or wax on Booksy with clear pricing and duration, and confirm instantly.<',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.<',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta personalizada" data-en="Personal consult">Personal consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Okami revisa la forma de tu ojo, tu piel y tus objetivos para recomendarte el estilo de pestañas, facial o servicio de cejas ideal." data-en="Okami checks your eye shape, skin and goals to recommend the right lash style, facial or brow service for you.">Okami checks your eye shape, skin and goals to recommend the right lash style, facial or brow service for you.<',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.<',
    '<h3 class="font-display text-xl mb-3" data-es="El tratamiento" data-en="The treatment">The treatment</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te acomodas en la silla de masaje con manta calientita mientras Okami trabaja, pestaña por pestaña o capa por capa, hasta 2h 45min para un set mega volumen completo." data-en="Settle into the heated massage chair with a warm blanket while Okami works, lash by lash or layer by layer, up to 2h 45min for a full mega volume set.">Settle into the heated massage chair with a warm blanket while Okami works, lash by lash or layer by layer, up to 2h 45min for a full mega volume set.<',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.<',
    '<h3 class="font-display text-xl mb-3" data-es="Plan de mantenimiento" data-en="Aftercare plan">Aftercare plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con recomendaciones de cuidado en casa y tu próximo relleno o facial ya agendado en Booksy." data-en="You leave with home-care recommendations and your next fill or facial already booked on Booksy.">You leave with home-care recommendations and your next fill or facial already booked on Booksy.<',
)
print('OK paso 10: metodo')

# =========================================================================
# 11) SERVICIOS: subtitulo + grid de 4 destacados + menu completo agrupado
# =========================================================================
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.<',
    'data-es="Precios y duraciones publicados por Radiant Star Beauty en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Radiant Star Beauty on Booksy. Booking confirms instantly.">Prices and durations as published by Radiant Star Beauty on Booksy. Booking confirms instantly.<',
)

grid_re = re.compile(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    flags=re.S,
)
m = grid_re.search(h)
assert m, 'no se encontro el grid de servicios'

BOOK = NEW_BOOKSY
new_grid = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Efecto natural" data-en="Natural effect">Natural effect</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Classic Lashes</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una extensión por pestaña natural para un look limpio de todos los días. Rellenos disponibles a las 2 y 3 semanas." data-en="One extension per natural lash for a clean, everyday look. Refills available at 2 and 3 weeks.">One extension per natural lash for a clean, everyday look. Refills available at 2 and 3 weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(171,125,47,0.4); box-shadow: 0 18px 50px rgba(51,40,28,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Facial insignia" data-en="Signature facial">Signature facial</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Radiant Star Luxe Facial Experience</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un ritual facial personalizado que termina con mascarilla jelly y masaje, en la silla de masaje calientita con manta." data-en="A custom facial ritual finished with a jelly mask and massage, in the heated massage chair with a warm blanket.">A custom facial ritual finished with a jelly mask and massage, in the heated massage chair with a warm blanket.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$135</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 10min</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Máximo volumen" data-en="Maximum volume">Maximum volume</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Volume &amp; Mega</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Abanicos hechos a mano para densidad total: set de volumen $126, o más grande con Mega Volumen a $162." data-en="Handmade fans for full density: Volume full set $126, or go bigger with Mega Volume at $162.">Handmade fans for full density: Volume full set $126, or go bigger with Mega Volume at $162.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$126</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas y depilación" data-en="Brows &amp; waxing">Brows &amp; waxing</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cejas &amp; Depilación" data-en="Brows &amp; Waxing">Brows &amp; Waxing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Diseño y tinte de cejas, más depilación de cuerpo completo: desde cejas y labio hasta brazos completos." data-en="Eyebrow shaping and tinting, plus full body waxing from brows and lip to full arms.">Eyebrow shaping and tinting, plus full body waxing from brows and lip to full arms.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$9+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">15min+</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_grid + h[m.end():]
print('OK paso 11a: 4 cards de servicios')

# --- menu completo agrupado por categoria (menu grande: 25 servicios) ---


def row(name, price, dur=None):
    if dur:
        left = (f'<span class="block font-light">{name}</span>'
                f'<span class="block text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-0.5">{dur}</span>')
    else:
        left = f'<span class="block font-light">{name}</span>'
    return (f'<li class="flex items-start justify-between gap-3 pb-3 border-b border-[color:var(--accent-ghost)] last:border-0 last:pb-0">'
            f'<span>{left}</span><span class="font-display text-shine shrink-0">${price}</span></li>')


lash_rows = [
    row('Classic Lashes', 90, '2h'),
    row('Hybrid Set (Mix Set)', 113),
    row('Volume Set', 126, '2h'),
    row('Mega Volume Lashes', 162, '2h 45min'),
    row('Lash Removals', 18, '1h'),
    row('Classic Refill (2 Weeks)', 54, '1h 30min'),
    row('Classic Refill (3 Weeks)', 63, '2h'),
    row('Hybrid Refill (2 Weeks)', 59),
    row('Hybrid Refill (3 Weeks)', 72, '2h'),
    row('Volume Refill (2 Weeks)', 68, '2h'),
    row('Volume Refill (3 Weeks)', 81, '2h'),
    row('Mega Refill (2 Weeks)', 68, '2h'),
    row('Mega Refill (3 Weeks)', 86),
]
facial_rows = [
    row('Radiance Maintenance Facial', 113),
    row('Acne Reset Facial', 122, '1h 10min'),
    row('Radiant Star Luxe Facial Experience', 135, '1h 10min'),
    row('Back Facial', 86),
]
wax_rows = [
    row('Eyebrow Shaping &amp; Tinting', 23),
    row('Eyebrow Waxing', 9, '15min'),
    row('Upper Lip', 11, '15min'),
    row('Chin Waxing', 9, '15min'),
    row('Full Face Waxing', 32, '30min'),
    row('Underarms', 23),
    row('Full Arms', 36, '30min'),
    row('Half Arm', 27, '20min'),
]

full_menu = f'''<div class="mt-14 grid md:grid-cols-3 gap-6 items-start">
        <div class="glass rounded-3xl p-7 reveal">
          <h3 class="font-display text-xl mb-5" data-es="Pestañas" data-en="Lashes">Lashes</h3>
          <ul class="space-y-3 text-sm">
            {''.join(lash_rows)}
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <h3 class="font-display text-xl mb-5" data-es="Faciales" data-en="Facials">Facials</h3>
          <ul class="space-y-3 text-sm">
            {''.join(facial_rows)}
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <h3 class="font-display text-xl mb-5" data-es="Cejas &amp; Depilación" data-en="Brows &amp; Waxing">Brows &amp; Waxing</h3>
          <ul class="space-y-3 text-sm">
            {''.join(wax_rows)}
          </ul>
        </div>
      </div>
      '''

anchor = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8">'
assert anchor in h
h = h.replace(anchor, full_menu + anchor, 1)

rep(
    '<span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span>',
    '<span data-es="Precios y duraciones exactos publicados por Radiant Star Beauty en Booksy." data-en="Exact prices and durations as published by Radiant Star Beauty on Booksy.">Exact prices and durations as published by Radiant Star Beauty on Booksy.</span>',
)
print('OK paso 11b: menu completo agrupado')

# =========================================================================
# 12) GALERIA
# =========================================================================
rep(
    '<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span>',
)

gal_re = re.compile(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    flags=re.S,
)
m = gal_re.search(h)
assert m, 'no se encontro el grid de galeria'

new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Clienta feliz, mirada terminada" data-en="Happy client, fresh set">Happy client, fresh set</span><img src="assets/raw/client-smile.jpg" alt="Clienta sonriendo con su set de pestanas terminado en Radiant Star Beauty" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Mega Volumen" data-en="Mega Volume">Mega Volume</span><img src="assets/raw/lash-mega.jpg" alt="Closeup de pestanas mega volumen" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cejas &amp; Pestañas" data-en="Brows &amp; Lashes">Brows &amp; Lashes</span><img src="assets/raw/lash-glam.jpg" alt="Ceja y pestanas de volumen terminadas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Set de Volumen" data-en="Volume Set">Volume Set</span><img src="assets/raw/lash-volume.jpg" alt="Closeup de pestanas de volumen" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Pestañas Clásicas" data-en="Classic Lashes">Classic Lashes</span><img src="assets/raw/lash-classic.jpg" alt="Closeup de pestanas clasicas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Set Híbrido" data-en="Hybrid Set">Hybrid Set</span><img src="assets/raw/lash-hybrid.jpg" alt="Closeup de pestanas hibridas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:m.start()] + new_gallery + h[m.end():]
print('OK paso 12: galeria')

# =========================================================================
# 13) OPINIONES
# =========================================================================
rep(
    'data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy<',
    'data-es="5.0 de 5 · 53 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 53 verified reviews on Booksy">5.0 out of 5 &middot; 53 verified reviews on Booksy<',
)

testi_re = re.compile(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    flags=re.S,
)
m = testi_re.search(h)
assert m, 'no se encontro el grid de opiniones'
new_testi = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Love my lashes everytime! She always responds fast, she helps you choose the look you are trying to achieve, while you are there she educates you on your lashes and skin type and what products she recommends for at home skin care. My first time getting a facial and it was everything, she also has a massage chair and gives you a blanket, best time to get a nap in! Prices are very reasonable and worth it for the quality of care she provides"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Georgette M.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I had such an anazing experience! The facial had my skin glowing and the lash set came out perfect and super natural but still gave me that extra glam. The vibe was relaxing and the service was so welcoming. Okami is my favorite esthetician. Definitely will be a returning client!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mariah S.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The best full service beauty service o have received. I got my lashes, nails and facial done and all very natural. Great customer service"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Cachet S.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:m.start()] + new_testi + h[m.end():]

rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy<',
    'data-es="Leer las 53 reseñas en Booksy" data-en="Read all 53 reviews on Booksy">Read all 53 reviews on Booksy<',
)
print('OK paso 13: opiniones')

# =========================================================================
# 14) UBICACION
# =========================================================================
rep(
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Fort Lauderdale</span>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(171,125,47,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">4390 N Federal Hwy, Suite 207, Fort Lauderdale, FL 33308</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(171,125,47,0.4)]" href="https://www.google.com/maps?q=4390+N+Federal+Hwy+Suite+207,+Fort+Lauderdale,+FL+33308" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
)
rep(
    "data-es=\"Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita.\" data-en=\"See Yesi's latest sets and DM any questions before your appointment.\">See Yesi's latest sets and DM any questions before your appointment.<",
    "data-es=\"Mira los looks más recientes de Okami y escribe por DM cualquier duda antes de tu cita.\" data-en=\"See Okami's latest looks and DM any questions before your appointment.\">See Okami's latest looks and DM any questions before your appointment.<",
)

clock_svg = '<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>'
hours_card = (
    f'<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">\n'
    f'            {clock_svg}\n'
    '            <div>\n'
    '              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>\n'
    '              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lun, Mar, Jue 10am-5pm · Mié, Vie 10am-8pm · Sáb 10am-4pm · Cerrado domingo" data-en="Mon, Tue, Thu 10am-5pm · Wed, Fri 10am-8pm · Sat 10am-4pm · Closed Sunday">Mon, Tue, Thu 10am-5pm &middot; Wed, Fri 10am-8pm &middot; Sat 10am-4pm &middot; Closed Sunday</p>\n'
    '            </div>\n'
    '          </div>\n'
)
anchor_ig_card_end = '</a>\n            </div>\n          </div>\n        </div>\n      </div>\n      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">'
assert anchor_ig_card_end in h
h = h.replace(
    anchor_ig_card_end,
    '</a>\n            </div>\n          </div>\n          ' + hours_card + '        </div>\n      </div>\n      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">',
    1,
)

rep(
    '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Radiant Star Beauty, 4390 N Federal Hwy, Fort Lauderdale FL"\n          src="https://www.google.com/maps?q=4390+N+Federal+Hwy+Suite+207,+Fort+Lauderdale,+FL+33308&output=embed"',
)
print('OK paso 14: ubicacion')

# =========================================================================
# 15) CTA FINAL
# =========================================================================
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.<',
    'data-es="Donde la estrella brilla más fuerte." data-en="Where the star glows the brightest.">Where the star glows the brightest.<',
)
rep(
    '<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu momento de brillar" data-en="Your glow-up">Your glow-up</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.<',
    'data-es="Reserva en línea en segundos: tu set de pestañas, un facial personalizado, o el retoque de cejas y depilación que ya te toca." data-en="Book online in seconds: your lash set, a custom facial, or the brow and wax refresh you are due for.">Book online in seconds: your lash set, a custom facial, or the brow and wax refresh you are due for.<',
)
print('OK paso 15: cta final')

# =========================================================================
# 16) FOOTER
# =========================================================================
rep(
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Radiant Star Beauty</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.<',
    'data-es="Estudio de pestañas, faciales y cejas en Fort Lauderdale, FL. Atención con cita previa." data-en="Lash, facial and brow studio in Fort Lauderdale, FL. By appointment only.">Lash, facial and brow studio in Fort Lauderdale, FL. By appointment only.<',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>4390 N Federal Hwy, Suite 207, Fort Lauderdale, FL 33308</p>',
)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Radiant Star Beauty.</p>')
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Radiant Star Beauty</span>')
print('OK paso 16: footer')

# =========================================================================
# 17) BARRIDO FINAL: cualquier "Lash Bloom" plano restante (subtitulo de
#     servicios ya cambiado en paso 11, esto es solo red de seguridad)
# =========================================================================
remaining = h.count('Lash Bloom')
assert remaining == 0, f'quedan {remaining} instancias de "Lash Bloom" sin reemplazar'

open(PATH, 'w').write(h)
print('BUILD OK')
