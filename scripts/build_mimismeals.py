import re

h = open('output/mimismeals/index.html').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:120]
    c = h.count(a)
    assert c == n, f'count {c} != {n}: ' + a[:120]
    h = h.replace(a, b, n)


def rep_all(a, b, n):
    rep(a, b, n)


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de la paleta
# ---------------------------------------------------------------------------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'no se encontro bloque merktop-badge'
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# ---------------------------------------------------------------------------
# 2. Paleta: oro -> rojo-chile / naranja quemado (truck real es rojo/negro)
# ---------------------------------------------------------------------------
pairs = [
    ('#0f0b07', '#140d0a'),
    ('#171207', '#1c110c'),
    ('#d4a84b', '#c0392b'),
    ('#b8934a', '#e2572c'),
    ('#241c0e', '#2a1410'),
    ('rgba(212,168,75,0.16)', 'rgba(192,57,43,0.16)'),
    ('rgba(212,168,75,0.32)', 'rgba(192,57,43,0.32)'),
    ('rgba(212,168,75,0.08)', 'rgba(192,57,43,0.08)'),
    ('#f0dc9e', '#f6b88a'),
    ('#9a7431', '#7a2015'),
    ('#e5c374', '#e2772c'),
    ('rgba(212,168,75,0.2)', 'rgba(192,57,43,0.22)'),
    ('rgba(122,90,30,0.28)', 'rgba(120,25,15,0.3)'),
    ('rgba(180,140,60,0.18)', 'rgba(226,87,44,0.2)'),
    ('#e8c476', '#f3875a'),
    ('#c9a04a', '#e2572c'),
    ('#96742c', '#8a2317'),
    ('rgba(80,58,18,0.4)', 'rgba(70,20,10,0.4)'),
    ('#6b5222', '#6b1f12'),
    ('rgba(212,168,75,0.25)', 'rgba(226,87,44,0.3)'),
    ('rgba(80,58,18,0.45)', 'rgba(70,20,10,0.45)'),
    ('rgba(212,168,75,0.35)', 'rgba(192,57,43,0.35)'),
    ('rgba(212,168,75,0.7)', 'rgba(192,57,43,0.7)'),
    ('rgba(212,168,75,0.45)', 'rgba(192,57,43,0.45)'),
    ('rgba(212,168,75,0.4)', 'rgba(192,57,43,0.4)'),
    ('rgba(212,168,75,0.5)', 'rgba(192,57,43,0.5)'),
    ('rgba(232,210,160,0.16)', 'rgba(226,87,44,0.18)'),
    ('#e8cf96', '#f3a77a'),
    ('#f8eed3', '#fbe4d2'),
    ('#bfa060', '#9c3a22'),
    ('#f0dcae', '#f6b88a'),
    ('rgba(232,207,150,0.16)', 'rgba(226,87,44,0.18)'),
    ('rgba(185,138,128,0.14)', 'rgba(120,25,15,0.16)'),
    ('#faf1dc', '#ffd9b8'),
    ('#ecd9a8', '#f3a77a'),
    ('#c9ab6b', '#c0392b'),
    ('rgba(110,85,35,0.35)', 'rgba(90,30,15,0.35)'),
    ('#8a744a', '#8a3420'),
    ('rgba(232,207,150,0.18)', 'rgba(226,87,44,0.2)'),
    ('rgba(110,85,35,0.4)', 'rgba(90,30,15,0.4)'),
    ('rgba(232,207,150,0.35)', 'rgba(226,87,44,0.35)'),
    ('rgba(232,207,150,0.7)', 'rgba(226,87,44,0.7)'),
    ('rgba(232,207,150,0.08)', 'rgba(226,87,44,0.08)'),
    ('#e9c3ab', '#f3a77a'),
    ('rgba(232,207,150,0.4)', 'rgba(226,87,44,0.4)'),
    ('rgba(232,207,150,0.14)', 'rgba(226,87,44,0.16)'),
    ('rgba(232,207,150,0.09)', 'rgba(226,87,44,0.1)'),
    ('background: linear-gradient(180deg, #191307 0%, #100c05 100%);', 'background: linear-gradient(180deg, #201008 0%, #120a06 100%);'),
    ('bg-[#0c0905]', 'bg-[#140b08]'),
]
for a, b in pairs:
    assert a in h, 'paleta NO: ' + a
    h = h.replace(a, b)

h = h.replace('@@BADGE@@', badge_block, 1)
assert 'rgba(212,168,75,0.45)' in h, 'el badge se perdio la proteccion'

# ---------------------------------------------------------------------------
# 3. Globales: WhatsApp, Instagram, telefono, email
# ---------------------------------------------------------------------------
WA = 'https://wa.me/13053437354?text=Hi%21%20I%27d%20like%20to%20order%20from%20Mimi%27s%20Meals.'
IG_URL = 'https://www.instagram.com/mimis_meal/'
OLD_BOOK = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
cnt = h.count(OLD_BOOK)
assert cnt == 13, f'booksy count {cnt}'
h = h.replace(OLD_BOOK, WA)

cnt = h.count('https://www.instagram.com/pure.artistrysk/')
assert cnt == 6, f'ig url count {cnt}'
h = h.replace('https://www.instagram.com/pure.artistrysk/', IG_URL)

cnt = h.count('@pure.artistrysk')
assert cnt == 4, f'ig handle count {cnt}'
h = h.replace('@pure.artistrysk', '@mimis_meal')

# ---------------------------------------------------------------------------
# 4. Head: title, meta, og, icon, JSON-LD
# ---------------------------------------------------------------------------
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    "<title>Mimi's Meals · Cuban Food Truck in Okeechobee, FL | Empanadas, Sandwiches &amp; Picanha Steak</title>",
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Mimi\'s Meals, Okeechobee FL: Cuban and Latin American food truck serving empanadas, Cuban sandwiches, picanha steak and homemade burgers. 5.0 with 47 reviews on Google. Message us on WhatsApp." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Mimi\'s Meals · Cuban Food Truck in Okeechobee, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Empanadas, Cuban sandwiches, picanha steak and more. 5.0 on Google with 47 reviews. Message us on WhatsApp." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/hero-burger.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
)
old_jsonld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Pure Artistry",
    "description": "Hair studio in Orlando, FL: silk press, loc retwists and interlocks, knotless braids, K-Tip and microlink extensions, keratin treatments.",
    "address": { "@type": "PostalAddress", "streetAddress": "80 W Grant St, Suite 111, Studio 156", "addressLocality": "Orlando", "addressRegion": "FL", "postalCode": "32806", "addressCountry": "US" },
    "sameAs": ["https://wa.me/13053437354?text=Hi%21%20I%27d%20like%20to%20order%20from%20Mimi%27s%20Meals.", "https://www.instagram.com/mimis_meal/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "234", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Hair services", "itemListElement": [
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Silk Press" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full-head Loc Retwist" } },
      { "@type": "Offer", "price": "400", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Small Knotless Braids" } },
      { "@type": "Offer", "price": "750", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "K-Tip Extensions" } }
    ] }
  }
  </script>'''
new_jsonld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FoodEstablishment",
    "name": "Mimi's Meals",
    "description": "Cuban and Latin American food truck in Okeechobee, FL: empanadas, Cuban sandwiches, picanha steak, homemade burgers and loaded fries, made to order.",
    "servesCuisine": ["Cuban", "Latin American"],
    "priceRange": "$",
    "address": { "@type": "PostalAddress", "streetAddress": "1416 FL-70", "addressLocality": "Okeechobee", "addressRegion": "FL", "postalCode": "34974", "addressCountry": "US" },
    "telephone": "+1-305-343-7354",
    "image": "assets/raw/hero-burger.jpg",
    "sameAs": ["https://www.instagram.com/mimis_meal/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "47", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "10:00", "closes": "20:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Menu", "itemListElement": [
      { "@type": "Offer", "price": "13", "priceCurrency": "USD", "itemOffered": { "@type": "MenuItem", "name": "Homemade Burger" } },
      { "@type": "Offer", "price": "3", "priceCurrency": "USD", "itemOffered": { "@type": "MenuItem", "name": "Empanada" } },
      { "@type": "Offer", "price": "15", "priceCurrency": "USD", "itemOffered": { "@type": "MenuItem", "name": "Picanha Steak Sandwich" } },
      { "@type": "Offer", "price": "7", "priceCurrency": "USD", "itemOffered": { "@type": "MenuItem", "name": "Mimi's Fries" } }
    ] }
  }
  </script>'''
rep(old_jsonld, new_jsonld)

# ---------------------------------------------------------------------------
# 5. Preloader
# ---------------------------------------------------------------------------
rep(
    '''  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">PA</span>
    <span class="pre-word">Pure Artistry</span>
    <span class="pre-line"></span>
  </div>''',
    '''  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">MM</span>
    <span class="pre-word">Mimi's Meals</span>
    <span class="pre-line"></span>
  </div>''',
)

# ---------------------------------------------------------------------------
# 6. Nav (desktop + mobile), favicon-avatar, CTA
# ---------------------------------------------------------------------------
rep(
    '''      <a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(192,57,43,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>
      </a>''',
    '''      <a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/logo.jpg" alt="Mimi's Meals" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(192,57,43,0.45)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Mimi's <span class="text-[color:var(--accent-deep)]">Meals</span></span>
      </a>''',
)

nav_links = [
    ('data-es="La Experiencia" data-en="The Experience">La Experiencia</a>',
     'data-es="Nuestro Truck" data-en="Our Truck">Our Truck</a>'),
    ('data-es="El Método" data-en="The Method">El Método</a>',
     'data-es="Cómo Pedir" data-en="How to Order">How to Order</a>'),
    ('data-es="Servicios" data-en="Services">Servicios</a>',
     'data-es="Menú" data-en="Menu">Menu</a>'),
    ('data-es="Galería" data-en="Gallery">Galería</a>',
     'data-es="Galería" data-en="Gallery">Gallery</a>'),
    ('data-es="Opiniones" data-en="Reviews">Opiniones</a>',
     'data-es="Reseñas" data-en="Reviews">Reviews</a>'),
    ('data-es="Ubicación" data-en="Location">Ubicación</a>',
     'data-es="Encuéntranos" data-en="Find Us">Find Us</a>'),
]
for a, b in nav_links:
    c = h.count(a)
    assert c == 2, f'nav_links count {c}: ' + a[:60]
    h = h.replace(a, b)

rep(
    '''          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>''',
    '''          <span data-es="Pedir por WhatsApp" data-en="Order on WhatsApp">Order on WhatsApp</span>
        </a>''',
    n=1,
)
rep(
    '''        <a href="''' + WA + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>''',
    '''        <a href="''' + WA + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Pedir por WhatsApp" data-en="Order on WhatsApp">Order on WhatsApp</a>''',
)
rep('aria-label="Cambiar idioma">EN<', 'aria-label="Switch language">ES<')
rep('aria-label="Abrir menú">', 'aria-label="Open menu">')

# ---------------------------------------------------------------------------
# 7. Hero
# ---------------------------------------------------------------------------
rep(
    'data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Okeechobee, FL · Food Truck" data-en="Okeechobee, FL · Food Truck">Okeechobee, FL · Food Truck</p>',
)
rep(
    '''style="transition-delay:80ms" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>''',
    '''style="transition-delay:80ms" data-es="Comida casera, hecha con cariño." data-en="Homemade food, made with love.">Homemade food, made with love.</p>''',
)
rep(
    '''        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>
        </h1>''',
    '''        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Comida cubana casera," data-en="Homemade Cuban food,">Homemade Cuban food,</span><br /><span data-es="directo desde el " data-en="straight from the ">straight from the </span><span class="text-shine" data-es="truck" data-en="truck">truck</span>
        </h1>''',
)
rep(
    '''style="transition-delay:240ms" data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>''',
    '''style="transition-delay:240ms" data-es="Mimi's Meals es un food truck cubano y latino parqueado sobre la FL-70 en Okeechobee: empanadas, sandwiches cubanos, picanha steak, papas cargadas y milkshakes frescos, todo hecho al momento. 5.0 perfecto en 47 reseñas de Google, sin menu de pantalla: solo llegas y pides." data-en="Mimi's Meals is a Cuban and Latin American food truck parked on FL-70 in Okeechobee: empanadas, Cuban sandwiches, picanha steak, loaded fries and fresh fruit shakes, all made to order. A perfect 5.0 across 47 Google reviews, no app needed, just pull up and order.">Mimi's Meals is a Cuban and Latin American food truck parked on FL-70 in Okeechobee: empanadas, Cuban sandwiches, picanha steak, loaded fries and fresh fruit shakes, all made to order. A perfect 5.0 across 47 Google reviews, no app needed, just pull up and order.</p>''',
)
rep(
    'data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 47 reseñas en Google" data-en="5.0 · 47 reviews on Google">5.0 · 47 reviews on Google</span>',
    n=1,
)
rep(
    '''            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>''',
    '''            <span data-es="Pedir por WhatsApp" data-en="Order on WhatsApp">Order on WhatsApp</span>''',
)
rep(
    '''          <span data-es="Fotos reales" data-en="Real work">Fotos reales</span>
          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>
          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>''',
    '''          <span data-es="Comida real" data-en="Real food">Real food</span>
          <span data-es="Precios reales" data-en="Real prices">Real prices</span>
          <span data-es="Contacto directo" data-en="Direct contact">Direct contact</span>''',
)
rep(
    '<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/hero-burger.jpg" alt="Homemade burger with fried egg and loaded fries from Mimi\'s Meals food truck" class="blur-up w-full h-full object-cover" />',
)
rep(
    '''            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Plato estrella" data-en="House special">House special</p>
            <p class="font-display text-lg">Homemade Burger</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$13 · Papas incluidas" data-en="$13 · Fries included">$13 · Fries included</p>''',
)

# ---------------------------------------------------------------------------
# 8. Strip de confianza
# ---------------------------------------------------------------------------
rep(
    '''      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>''',
    '''      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="47">47</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Cuban <span class="text-shine">&amp;</span> Latin</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú hecho al día" data-en="Menu made daily">Menu made daily</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Food Truck" data-en="Food Truck">Food Truck</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Parqueado en la FL-70" data-en="Parked on FL-70">Parked on FL-70</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Okeechobee</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1416 FL-70</p></div>''',
)

# ---------------------------------------------------------------------------
# 9. Marquee (x2 bloques, cada palabra x4 ocurrencias totales)
# ---------------------------------------------------------------------------
marquee_words = [
    ('Silk Press', 'Cuban Sandwiches'),
    ('Loc Retwist', 'Empanadas'),
    ('Knotless Braids', 'Picanha Steak'),
    ('K-Tip Extensions', "Mimi's Fries"),
    ('Keratin', 'Homemade Burgers'),
    ('Orlando, FL', 'Okeechobee, FL'),
]
for a, b in marquee_words:
    tag = f'<span class="marquee-word">{a}</span>'
    c = h.count(tag)
    assert c == 4, f'marquee "{a}" count {c}'
    h = h.replace(tag, f'<span class="marquee-word">{b}</span>')

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA -> Our Truck
# ---------------------------------------------------------------------------
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/about-truck.jpg" alt="Mimi\'s Meals red food truck trailer parked on FL-70 with its menu board" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/about-picanha-rice.jpg" alt="Picanha steak over fried rice with chimichurri, a Mimi\'s Meals favorite" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    'data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="Nuestro truck" data-en="Our truck">Our truck</p>',
)
rep(
    '''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>''',
    '''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una familia," data-en="One family,">One family,</span><br /><span class="text-shine" data-es="comida casera de verdad" data-en="real home cooking">real home cooking</span></h2>''',
)
rep(
    '''style="transition-delay:160ms" data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>''',
    '''style="transition-delay:160ms" data-es="Mimi's Meals es un food truck cubano y latino con base en Okeechobee, FL. El trailer rojo sirve empanadas caseras, sandwiches cubanos, picanha steak y las papas cargadas de la casa, todo cocinado al momento y servido en la mesa de picnic junto al truck." data-en="Mimi's Meals is a Cuban and Latin American food truck based in Okeechobee, FL. The red trailer serves homemade empanadas, Cuban sandwiches, picanha steak and Mimi's signature loaded fries, all cooked to order and served at the picnic table next to the truck.">Mimi's Meals is a Cuban and Latin American food truck based in Okeechobee, FL. The red trailer serves homemade empanadas, Cuban sandwiches, picanha steak and Mimi's signature loaded fries, all cooked to order and served at the picnic table next to the truck.</p>''',
)
rep(
    '''style="transition-delay:220ms" data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>''',
    '''style="transition-delay:220ms" data-es="Los que viajan por trabajo y paran en Okeechobee lo encuentran de boca en boca: 5.0 perfecto en 47 reseñas verificadas de Google, con clientes que destacan las porciones y el cariño de los dueños." data-en="Travelers passing through Okeechobee for work keep finding it by word of mouth: a perfect 5.0 across 47 verified Google reviews, with regulars praising the portions and the owners' warmth.">Travelers passing through Okeechobee for work keep finding it by word of mouth: a perfect 5.0 across 47 verified Google reviews, with regulars praising the portions and the owners' warmth.</p>''',
)
rep(
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="47">47</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Diario" data-en="Daily">Daily</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Menú fresco" data-en="Fresh menu">Fresh menu</p></div>''',
)
rep(
    '''            <img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>''',
    '''            <img src="assets/raw/logo.jpg" alt="Mimi's Meals logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(192,57,43,0.35)]" loading="lazy" />
            <span class="text-sm font-light">Mimi's Meals · <span class="text-[color:var(--ink-40)]" data-es="Comida hecha con cariño" data-en="Food made with love">Food made with love</span></span>''',
)

# ---------------------------------------------------------------------------
# 11. EL METODO -> How to Order
# ---------------------------------------------------------------------------
rep(
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Así pides" data-en="How to order">How to order</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Comer aquí es" data-en="Eating here is">Eating here is</span> <span class="text-shine" data-es="fácil" data-en="easy">easy</span></h2>',
)
rep(
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Mensaje o llamada" data-en="Message or call">Message or call</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Escribe por WhatsApp o llama para avisar que vienes, o simplemente llega al truck." data-en="WhatsApp or call ahead to let us know you are coming, or just pull up to the truck.">WhatsApp or call ahead to let us know you are coming, or just pull up to the truck.</p>''',
)
rep(
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Elige tu plato" data-en="Pick your meal">Pick your meal</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Empanadas, un sandwich cubano, picanha steak o las papas cargadas de Mimi, armadas como te gusten." data-en="Empanadas, a Cuban sandwich, picanha steak or Mimi's loaded fries, built the way you like it.">Empanadas, a Cuban sandwich, picanha steak or Mimi's loaded fries, built the way you like it.</p>''',
)
rep(
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Lo cocinamos fresco" data-en="We cook it fresh">We cook it fresh</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Todo se prepara al momento dentro del truck, nada precocinado ni de microondas." data-en="Everything is made to order inside the truck, nothing pre-made or microwaved.">Everything is made to order inside the truck, nothing pre-made or microwaved.</p>''',
)
rep(
    '''          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Llegas y comes" data-en="Pull up and eat">Pull up and eat</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Toma una mesa de picnic junto al truck o llévatelo para el camino." data-en="Grab a seat at the picnic table next to the truck, or take it to go.">Grab a seat at the picnic table next to the truck, or take it to go.</p>''',
)

# ---------------------------------------------------------------------------
# 12. SERVICIOS -> Menu (eyebrow, h2, intro, 4 cards reales, nota)
# ---------------------------------------------------------------------------
rep(
    'data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    'data-es="Menú" data-en="Menu">Menu</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Pide tu" data-en="Pick your">Pick your</span> <span class="text-shine" data-es="favorito" data-en="favorite">favorite</span></h2>',
)
rep(
    '''style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>''',
    '''style="transition-delay:160ms" data-es="Precios reales tomados del menú del truck. Pide por WhatsApp o llega directo." data-en="Real prices taken straight from the truck's own menu board. Order on WhatsApp or just walk up.">Real prices taken straight from the truck's own menu board. Order on WhatsApp or just walk up.</p>''',
)

services_grid_re = re.compile(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    flags=re.S,
)
assert services_grid_re.search(h), 'no se encontro el grid de servicios'
new_services_grid = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(192,57,43,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Plato estrella" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Hamburguesa Casera" data-en="Homemade Burger">Homemade Burger</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Blend de carne, cebolla caramelizada, hongos, tocino, queso americano y azul, huevo frito, mayo chimichurri y mayo picante. Papas incluidas." data-en="Burger blend, caramelized onions, mushrooms, bacon, American and blue cheese, fried egg, chimichurri mayo and spicy mayo. Fries included.">Burger blend, caramelized onions, mushrooms, bacon, American and blue cheese, fried egg, chimichurri mayo and spicy mayo. Fries included.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$13</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Papas incluidas" data-en="Fries included">Fries included</p></div>
            <a href="''' + WA + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir" data-en="Order">Order</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para picar" data-en="Snack size">Snack size</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Empanadas</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="De carne, pollo, jamón y queso o guayaba y queso, fritas al momento." data-en="Beef, chicken, ham &amp; cheese or guava &amp; cheese, fried to order.">Beef, chicken, ham &amp; cheese or guava &amp; cheese, fried to order.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$3</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Cada una" data-en="Each">Each</p></div>
            <a href="''' + WA + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir" data-en="Order">Order</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sandwiches" data-en="Sandwiches">Sandwiches</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Picanha Steak" data-en="Picanha Steak">Picanha Steak</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Picanha (corte brasileño) en pan cubano con lechuga romana, cebolla morada, mayo chimichurri y queso derretido. Papas incluidas." data-en="Picanha (Brazilian steak) on Cuban bread with romaine, red onion, chimichurri mayo and melted cheese. Fries included.">Picanha (Brazilian steak) on Cuban bread with romaine, red onion, chimichurri mayo and melted cheese. Fries included.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$15</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Papas incluidas" data-en="Fries included">Fries included</p></div>
            <a href="''' + WA + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir" data-en="Order">Order</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para acompañar" data-en="Sides">Sides</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Lados" data-en="Sides">Sides</h3>
          <ul class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6 space-y-1.5">
            <li class="flex justify-between gap-3"><span data-es="Ensalada" data-en="Salad">Salad</span><span class="text-[color:var(--ink-40)]">$3</span></li>
            <li class="flex justify-between gap-3"><span data-es="Papas a la provenzal" data-en="Provenzal fries">Provenzal fries</span><span class="text-[color:var(--ink-40)]">$3</span></li>
            <li class="flex justify-between gap-3"><span data-es="Papas con trufa" data-en="Truffle fries">Truffle fries</span><span class="text-[color:var(--ink-40)]">$4</span></li>
            <li class="flex justify-between gap-3"><span data-es="Papas de Mimi" data-en="Mimi's Fries">Mimi's Fries</span><span class="text-[color:var(--ink-40)]">$7</span></li>
          </ul>
          <div class="mt-auto">
            <a href="''' + WA + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir" data-en="Order">Order</a>
          </div>
        </div>
      </div>
      '''
h = services_grid_re.sub(lambda _m: new_services_grid, h, count=1)

rep(
    '''<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>''',
    '''<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También en el menú: tazones de arroz frito y sandwiches con cerdo cubano, pollo, picanha o camarón, batidos de mango y mamey, y mas. Pregunta en el truck por el menú completo y los precios del día." data-en="Also on the menu: fried rice bowls and sandwiches with Cuban pork, chicken, picanha or shrimp, mango and mamey milkshakes, and more. Ask at the truck for the full board and today's prices.">Also on the menu: fried rice bowls and sandwiches with Cuban pork, chicken, picanha or shrimp, mango and mamey milkshakes, and more. Ask at the truck for the full board and today's prices.</span></p>''',
)

# ---------------------------------------------------------------------------
# 13. GALERIA (grid completo por regex: 1 wide + 3 regulares, fotos reales)
# ---------------------------------------------------------------------------
rep(
    'data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    'data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Comida" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="food">food</span></h2>',
)
gallery_grid_re = re.compile(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    flags=re.S,
)
assert gallery_grid_re.search(h), 'no se encontro el grid de galeria'
new_gallery_grid = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Papas cargadas con picanha" data-en="Picanha loaded fries">Picanha loaded fries</span><img src="assets/raw/gallery-wide-fries.jpg" alt="Picanha steak over Mimi's loaded fries with mozzarella, blue cheese and chimichurri" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Sandwiches de picanha" data-en="Picanha sandwiches">Picanha sandwiches</span><img src="assets/raw/gallery-sandwiches.jpg" alt="Two picanha steak sandwiches on toasted bread with fries, ready to go" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Pollo con arroz y tostones" data-en="Chicken, rice &amp; plantains">Chicken, rice &amp; plantains</span><img src="assets/raw/gallery-chicken-plate.jpg" alt="Crispy chicken thigh over rice and beans with sweet plantains" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Sandwich cubano" data-en="Cuban sandwich">Cuban sandwich</span><img src="assets/raw/gallery-cuban-sandwich.jpg" alt="Classic Cuban sandwich pressed and grilled, served with fries" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = gallery_grid_re.sub(lambda _m: new_gallery_grid, h, count=1)

# ---------------------------------------------------------------------------
# 14. OPINIONES: 3 reviews reales verbatim de Google
# ---------------------------------------------------------------------------
rep(
    '''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>''',
    '''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What our">What our</span> <span class="text-shine" data-es="nuestros clientes" data-en="customers say">customers say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 47 reseñas verificadas en Google" data-en="5.0 out of 5 · 47 verified reviews on Google">5.0 out of 5 · 47 verified reviews on Google</span></p>''',
)
rep(
    '''          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''',
    '''          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Food was super delicious for being a food truck!! Definitely surprised me!! I'm from Miami traveling here for work and was missing some cuban home cooked food and boy did this place deliver, and they were super courteous and nice. Great personality behind that kitchen!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jorge Diez</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>''',
)
rep(
    '''          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''',
    '''          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Highly recommend this food truck! The owners are incredibly friendly and the food is absolutely delicious. Great food and great service, I'll definitely be coming back!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Begonia</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>''',
)
rep(
    '''          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''',
    '''          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Stopped by on our way through the area. Got the chicken sandwich with fries and Cuban sandwich. Both were delicious, definitely recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ed's RV Solutions</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>''',
)
rep(
    '''        <a href="''' + WA + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>''',
    '''        <a href="https://www.google.com/maps/place/Mimi%27s+Meals/data=!4m7!3m6!1s0x88dc1f0046ef02a7:0x48164cf8b10d2906!8m2!3d27.2435334!4d-80.8149989!16s%2Fg%2F11v_4xvw95!19sChIJpwLvRgAf3IgRBikNsfhMFkg" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 47 reseñas en Google" data-en="Read all 47 reviews on Google">Read all 47 reviews on Google</a>''',
)

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep(
    'data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    'data-es="Visítanos" data-en="Find us">Find us</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Encuéntranos en" data-en="Find us in">Find us in</span> <span class="text-shine">Okeechobee</span></h2>',
)
rep(
    '''              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(192,57,43,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''              <p class="text-sm text-[color:var(--ink-60)] font-light">1416 FL-70, Okeechobee, FL 34974</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Martes a lunes, 10am a 8pm (cerrado sábado y domingo)" data-en="Tuesday to Monday, 10am to 8pm (closed Saturday and Sunday)">Tuesday to Monday, 10am to 8pm (closed Saturday and Sunday)</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(192,57,43,0.4)]" href="https://www.google.com/maps?q=1416+FL-70,+Okeechobee,+FL+34974" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>''',
)
rep(
    '''              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(192,57,43,0.4)]" href="''' + WA + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''              <p class="font-medium mb-1" data-es="Pedidos" data-en="Orders">Orders</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Escribe o llama para pedir con anticipación, sobre todo si quieres picanha steak antes de que se acabe." data-en="Message or call ahead to order, especially for the picanha steak, which can run out.">Message or call ahead to order, especially for the picanha steak, which can run out.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(192,57,43,0.4)]" href="''' + WA + '''" target="_blank" rel="noopener" data-es="Pedir por WhatsApp" data-en="Order on WhatsApp">Order on WhatsApp</a>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(192,57,43,0.4)] block mt-1" href="tel:+13053437354" data-es="O llama al (305) 343-7354" data-en="Or call (305) 343-7354">Or call (305) 343-7354</a>''',
)
rep(
    '''              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(192,57,43,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@mimis_meal</a>''',
    '''              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira las fotos mas recientes del truck y escribe por DM cualquier duda." data-en="See the truck's latest photos and DM any questions.">See the truck's latest photos and DM any questions.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(192,57,43,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">@mimis_meal</a>''',
)
rep(
    '''        <iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"
          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"''',
    '''        <iframe title="Map: Mimi's Meals, 1416 FL-70, Okeechobee FL"
          src="https://www.google.com/maps?q=1416+FL-70,+Okeechobee,+FL+34974&output=embed"''',
)

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep(
    'data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Comida casera, hecha con cariño." data-en="Homemade food, made with love.">Homemade food, made with love.</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="¿Tienes hambre?" data-en="Hungry?">Hungry?</span> <span class="text-shine" data-es="Estamos parqueados y listos" data-en="We are parked and ready">We are parked and ready</span></h2>',
)
rep(
    '''style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>''',
    '''style="transition-delay:180ms" data-es="Escríbenos por WhatsApp o llega directo al truck rojo sobre la FL-70. Empanadas, sandwiches cubanos y picanha steak, hechos frescos mientras esperas." data-en="Message us on WhatsApp or just pull up to the red truck on FL-70. Empanadas, Cuban sandwiches and picanha steak, made fresh while you wait.">Message us on WhatsApp or just pull up to the red truck on FL-70. Empanadas, Cuban sandwiches and picanha steak, made fresh while you wait.</p>''',
)
rep(
    '''        <a href="''' + WA + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''        <a href="''' + WA + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Pedir por WhatsApp" data-en="Order on WhatsApp">Order on WhatsApp</a>
        <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>''',
)

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Mimi\'s Meals</span>')
rep(
    '''        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(226,87,44,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/logo.jpg" alt="Mimi's Meals" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(226,87,44,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Mimi's Meals</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Food truck cubano y latino en Okeechobee, FL. Comida hecha con cariño." data-en="Cuban and Latin American food truck in Okeechobee, FL. Food made with love.">Cuban and Latin American food truck in Okeechobee, FL. Food made with love.</p>''',
)
rep(
    '''        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + WA + '''" target="_blank" rel="noopener" class="hover:text-[#f3a77a]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>1416 FL-70, Okeechobee, FL 34974</p>
        <p><a href="tel:+13053437354" class="hover:text-[#f3a77a]">(305) 343-7354</a></p>
        <p><a href="mailto:mimismeal41@gmail.com" class="hover:text-[#f3a77a]">mimismeal41@gmail.com</a></p>''',
)
rep(
    '''        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f3a77a]">Instagram · @mimis_meal</a></p>''',
    '''        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f3a77a]">Instagram · @mimis_meal</a></p>
        <p class="text-[color:var(--ink-40)]">Facebook · Mimis Meals</p>''',
)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Mimi\'s Meals.</p>')

# ---------------------------------------------------------------------------
# 18. Boton flotante de pedido (WhatsApp en vez de calendario)
# ---------------------------------------------------------------------------
rep(
    '''  <a href="''' + WA + '''" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
    <span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>
  </a>''',
    '''  <a href="''' + WA + '''" target="_blank" rel="noopener" class="book-float" aria-label="Order on WhatsApp">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="#1c1408" stroke="none"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.48 1.32 5l-1.4 5.09 5.21-1.37a9.9 9.9 0 0 0 4.78 1.22h.01c5.46 0 9.9-4.45 9.9-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm0 1.67a8.2 8.2 0 0 1 5.83 2.42 8.17 8.17 0 0 1 2.42 5.82c0 4.55-3.7 8.24-8.26 8.24a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.09.81.83-3.01-.2-.31a8.18 8.18 0 0 1-1.26-4.37c0-4.55 3.71-8.27 8.22-8.27zm-4.38 4.74c-.17 0-.44.06-.67.31s-.88.86-.88 2.1.9 2.43 1.03 2.6c.12.17 1.76 2.69 4.27 3.77.6.26 1.06.41 1.43.53.6.19 1.14.16 1.57.1.48-.07 1.47-.6 1.68-1.18s.21-1.08.15-1.18-.26-.16-.52-.28-1.55-.76-1.79-.85-.42-.13-.6.13-.68.85-.84 1.03-.31.19-.57.07-1.1-.41-2.11-1.3c-.78-.7-1.3-1.56-1.46-1.82s-.02-.4.11-.53c.12-.12.26-.31.39-.46.13-.15.17-.26.26-.44.09-.17.04-.33-.02-.46s-.6-1.45-.82-1.98c-.21-.52-.43-.44-.6-.45z"/></svg>
    <span class="book-float-label" data-es="Pedir por WhatsApp" data-en="Order">Order</span>
  </a>''',
)

open('output/mimismeals/index.html', 'w').write(h)
print('PASO 1-18 OK, len=', len(h))
