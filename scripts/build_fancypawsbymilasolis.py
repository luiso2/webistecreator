import re

PATH = 'output/fancypawsbymilasolis/index.html'
h = open(PATH).read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:120]
    h = h.replace(a, b, n)

def rep_count(a, n):
    assert h.count(a) == n, f'COUNT MISMATCH ({h.count(a)} != {n}): ' + a[:100]

PHONE_E164 = '+17864386358'
PHONE_DISPLAY = '(786) 438-6358'
MAPS_URL = 'https://www.google.com/maps/place/Fancy+Paws+by+Mila+Solis/data=!4m7!3m6!1s0x88d9a964b462012b:0x8b08df62af982690!8m2!3d26.0387317!4d-80.2555629!16s%2Fg%2F11jd8b3n1_!19sChIJKwFitGSp2YgRkCaYr2LfCIs'
IG_URL = 'https://www.instagram.com/fancypawsbyms/'

# ============================================================
# 1. PALETA (jade/mint spa, nunca usada antes: no gold, no pink,
#    no teal-acero #4fb8b8, no mare #296167)
# ============================================================
hex_pairs = [
    ('#a04a72', '#1f7a63'),   # accent-deep
    ('#c47a9c', '#4caf8f'),   # accent-mid
    ('#faf2f6', '#f6fbf8'),   # bg / white-ish strokes
    ('#f3e0ea', '#dcefe4'),   # bg-2 / accent-soft
    ('#5c2140', '#0d3b30'),   # btn-3d shadow sole (light)
    ('#f0bed7', '#9fe0c2'),   # dark-band text-shine/stars/hover
    ('#8a5573', '#4f8a73'),   # dark-band btn-3d shadow sole
    ('#d9a8c2', '#79c7a8'),   # orb-b / dark-band text-shine 52%
    ('#7d3457', '#124a3c'),   # text-shine dark tone / scroll-progress start
    ('#5f2c48', '#11392e'),   # text-shine dark tone 2 / step-num end
    ('#33222c', '#1f2e2a'),   # ink
    ('#fbf3f8', '#f3fbf7'),   # tile-cap text
    ('#fbeff5', '#eafaf2'),   # dark-band btn-3d top
    ('#f8dfeb', '#c9ecd9'),   # dark-band text-shine 30%
    ('#f6f1ea', '#eef5f0'),   # theme-color meta
    ('#f2d5e3', '#cdeadd'),   # orb-a
    ('#f2cfe0', '#bfe4d2'),   # dark-band text-shine 100%
    ('#efd0e0', '#bfe4d2'),   # dark-band btn-3d mid
    ('#e5c1d4', '#bfe4d2'),   # orb-c
    ('#dc9dbe', '#8fd9bb'),   # scroll-progress end
    ('#d3a2bc', '#8fcdb0'),   # dark-band btn-3d bottom
    ('#c9789f', '#3fae8c'),   # text-shine mid 30%
    ('#b25a85', '#2a8f73'),   # text-shine end
    ('#2a1722', '#16211d'),   # cta-final bg top
    ('#1f0f18', '#0f1714'),   # cta-final bg bottom
    ('#1c0f16', '#13201c'),   # footer bg
]
for old, new in hex_pairs:
    assert old in h, 'NO HEX: ' + old
    h = h.replace(old, new)

rgba_pairs = [
    ('rgba(160,74,114', 'rgba(31,122,99'),
    ('rgba(51,34,44',   'rgba(31,46,42'),
    ('rgba(240,190,215', 'rgba(159,224,194'),
    ('rgba(70,25,50',   'rgba(10,45,36'),
    ('rgba(250,242,246', 'rgba(246,251,248'),
    ('rgba(125,52,87',  'rgba(18,74,60'),
    ('rgba(253,246,250', 'rgba(248,251,249'),
    ('rgba(40,16,30',   'rgba(22,34,30'),
    ('rgba(233,205,186', 'rgba(143,217,187'),
    ('rgba(185,138,128', 'rgba(121,199,168'),
]
for old, new in rgba_pairs:
    assert old in h, 'NO RGBA: ' + old
    h = h.replace(old, new)

# Badge Merktop (rgba(212,168,75 / #D4A84B / #f4eee2 / rgba(244,238,226 /
# rgba(36,28,20 / rgba(27,21,14) queda intacto: no aparece en las listas de arriba.

# ============================================================
# 2. HEAD: title, meta, og, icon, JSON-LD
# ============================================================
rep(
  '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
  '<title>Fancy Paws by Mila Solis · Dog Grooming in Pembroke Pines, FL | 5.0 on Google</title>'
)
rep(
  '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
  '<meta name="description" content="Fancy Paws by Mila Solis: private, one-on-one dog grooming, daycare and boarding in Pembroke Pines, FL. 5.0 stars across 57 Google reviews. Call to get a quote." />'
)
rep(
  '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
  '<meta property="og:title" content="Fancy Paws by Mila Solis · Dog Grooming in Pembroke Pines, FL" />'
)
rep(
  '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
  '<meta property="og:description" content="Private, one-on-one dog grooming, daycare and boarding. 5.0 stars, 57 Google reviews. Call for a quote." />'
)
rep(
  '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
  '<meta property="og:image" content="assets/raw/gmaps-8.jpg" />'
)
rep(
  '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
  '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />'
)

old_jsonld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Lash Bloom LLC",
    "description": "Lash studio in West Palm Beach, FL: classic, hybrid, volume and mega volume eyelash extensions and fills.",
    "address": { "@type": "PostalAddress", "streetAddress": "4580 Cresthaven Blvd", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33415", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach", "https://www.instagram.com/_lashbloom/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "86", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Lash services", "itemListElement": [
      { "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic full set" } },
      { "@type": "Offer", "price": "145", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Hybrid full set" } },
      { "@type": "Offer", "price": "155", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Volume full set" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic 2wk fill" } }
    ] }
  }
  </script>'''
new_jsonld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Fancy Paws by Mila Solis",
    "description": "Private, one-on-one dog grooming, daycare and boarding studio in Pembroke Pines, FL, run by Mila Solis.",
    "address": { "@type": "PostalAddress", "streetAddress": "8357 NW 38th St", "addressLocality": "Pembroke Pines", "addressRegion": "FL", "postalCode": "33024", "addressCountry": "US" },
    "telephone": "+1-786-438-6358",
    "image": "assets/raw/gmaps-8.jpg",
    "sameAs": ["''' + MAPS_URL + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "57", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "10:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "11:00", "closes": "16:00" }
    ],
    "makesOffer": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bath & brush-out" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Full grooming / haircut" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Doggy daycare" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Overnight boarding" } }
    ]
  }
  </script>'''
rep(old_jsonld, new_jsonld)

# ============================================================
# 3. GLOBALES: Booksy -> tel:, Instagram -> Google Maps / IG real
# ============================================================
BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
IG_OLD = 'https://www.instagram.com/_lashbloom/'

# 3a. El card de "Reservar en Booksy" dentro de Ubicacion (unico, por su clase)
rep(
  '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,99,0.4)]" href="' + BOOKSY + '" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
  '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,99,0.4)]" href="tel:' + PHONE_E164 + '" data-es="Llamar para disponibilidad" data-en="Call for availability">Llamar para disponibilidad</a>'
)

# 3b. Resto de "Reservar en Booksy" / "Book on Booksy" (hero + CTA final): quedan 2
rep_count('data-es="Reservar en Booksy" data-en="Book on Booksy"', 2)
h = h.replace(
  'data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy',
  'data-es="Llamar ahora" data-en="Call now">Llamar ahora'
)

# 3c. Todos los href de Booksy -> tel (quedan 11 en el body tras el paso 3a)
rep_count('href="' + BOOKSY + '"', 11)
h = h.replace('href="' + BOOKSY + '" target="_blank" rel="noopener"', 'href="tel:' + PHONE_E164 + '"')

# 3d. Nav: "Reservar cita" / "Book now" (desktop + mobile)
rep_count('data-es="Reservar cita" data-en="Book now"', 2)
h = h.replace('data-es="Reservar cita" data-en="Book now">Reservar cita', 'data-es="Llamar ahora" data-en="Call now">Llamar ahora')

# 3e. Servicios: 4 botones "Reservar"/"Book" (3 ghost + 1 btn-3d), mismo texto final
rep_count('data-es="Reservar" data-en="Book">Book', 4)
h = h.replace('data-es="Reservar" data-en="Book">Book', 'data-es="Llamar" data-en="Call">Call')

# 3f. "Leer las 86 resenas en Booksy" -> enlaza a Google Maps
rep(
  '<a href="tel:' + PHONE_E164 + '" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
  '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 57 reseñas en Google" data-en="Read all 57 reviews on Google">Read all 57 reviews on Google</a>'
)

# 3g. Footer: "Reservas online - Booksy" -> telefono real
rep(
  '<p><a href="tel:' + PHONE_E164 + '" class="hover:text-[#9fe0c2]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
  '<p><a href="tel:' + PHONE_E164 + '" class="hover:text-[#9fe0c2]" data-es="Llamar · ' + PHONE_DISPLAY + '" data-en="Call · ' + PHONE_DISPLAY + '">Call · ' + PHONE_DISPLAY + '</a></p>'
)

# 3h. Instagram: 5 ocurrencias en el cuerpo (no la de JSON-LD, ya reemplazada arriba)
rep_count('href="' + IG_OLD + '"', 5)

# hero secundario (btn-ghost px-8 py-4)
rep(
  '''<a href="''' + IG_OLD + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @_lashbloom
          </a>''',
  '''<a href="''' + MAPS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <span data-es="Ver en Google" data-en="View on Google">View on Google</span>
          </a>'''
)

# galeria top-right
rep(
  '''<a href="''' + IG_OLD + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @_lashbloom
        </a>''',
  '''<a href="''' + MAPS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <span class="stars text-xs" aria-hidden="true">★</span>
          <span data-es="5.0 en Google" data-en="5.0 on Google">5.0 on Google</span>
        </a>'''
)

# CTA final secundario
rep(
  '<a href="' + IG_OLD + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
  '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Ver en Google" data-en="View on Google">View on Google</a>'
)

# footer: Instagram real + Facebook (texto, sin URL confirmada)
rep(
  '<p><a href="' + IG_OLD + '" target="_blank" rel="noopener" class="hover:text-[#9fe0c2]">Instagram · @_lashbloom</a></p>',
  '<p><a href="' + IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#9fe0c2]">Instagram · @fancypawsbyms</a></p>\n        <p class="text-[color:var(--ink-40)]">Facebook · Fancy Paws by Mila Solis</p>'
)

# ============================================================
# 4. PRELOADER / NAV / NOMBRE DE MARCA
# ============================================================
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">FP</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Fancy Paws</span>')

rep(
  '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,122,99,0.35)]" />',
  '<img src="assets/raw/logo.jpg" alt="Fancy Paws by Mila Solis logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,122,99,0.35)]" />'
)
rep(
  '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
  '<span class="font-display text-xl tracking-[0.1em] uppercase">Fancy <span class="text-[color:var(--accent-deep)]">Paws</span></span>'
)

# ============================================================
# 5. HERO
# ============================================================
rep(
  'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio',
  'data-es="Pembroke Pines, FL · Dog Spa" data-en="Pembroke Pines, FL · Dog Spa">Pembroke Pines, FL · Dog Spa'
)
rep(
  'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.',
  'data-es="Grooming que tu perro va a disfrutar." data-en="Grooming your dog will actually enjoy.">Grooming your dog will actually enjoy.',
  n=1
)
rep(
  '''<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>''',
  '''<span data-es="Grooming tranquilo, uno a uno," data-en="Calm, one-on-one grooming,">Calm, one-on-one grooming,</span><br /><span data-es="sin " data-en="no ">no </span><span class="text-shine" data-es="jaulas" data-en="cages">cages</span>'''
)
rep(
  '''data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.''',
  '''data-es="Mila Solis baña, corta, cepilla y consiente a tu perro ella misma, uno a la vez, sin jaulas ni corridas en grupo. Baños, cortes de raza, uñas, oídos, desenredado y recortes de dientes, además de guardería y hospedaje para cuando viajas." data-en="Mila Solis bathes, cuts, brushes and pampers your dog herself, one at a time, with no cages or group runs. Baths, breed cuts, nails, ears, de-shedding and teeth cleaning, plus daycare and boarding for when you travel.">Mila Solis bathes, cuts, brushes and pampers your dog herself, one at a time, with no cages or group runs. Baths, breed cuts, nails, ears, de-shedding and teeth cleaning, plus daycare and boarding for when you travel.'''
)
rep(
  'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy',
  'data-es="5.0 · 57 reseñas en Google" data-en="5.0 · 57 reviews on Google">5.0 · 57 reviews on Google'
)
# (el boton "Reservar en Booksy" del hero ya quedo como "Llamar ahora" en el paso 3b)
# Glass card de precio -> glass card de "sin jaulas"
rep(
  '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
  '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Trato directo" data-en="Direct with Mila">Direct with Mila</p>
            <p class="font-display text-lg" data-es="Un perro a la vez" data-en="One dog at a time">One dog at a time</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Sin jaulas · trato privado" data-en="No cages · private suite">No cages · private suite</p>'''
)

# ============================================================
# 6. STRIP DE CONFIANZA
# ============================================================
rep(
  '''<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>''',
  '''<span data-count="57">57</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span>'''
)
rep(
  '<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p>',
  '<p class="font-display text-2xl">Groom <span class="text-shine">&amp;</span> Daycare</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Grooming · guardería · hospedaje" data-en="Grooming · daycare · boarding">Grooming · daycare · boarding</p>'
)
rep(
  '<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p>',
  '<p class="font-display text-2xl">No <span class="text-shine" data-es="jaulas" data-en="cages">cages</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Grooming tranquilo, uno a uno" data-en="Calm, one-on-one care">Calm, one-on-one care</p>'
)
rep(
  '<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p>',
  '<p class="font-display text-2xl">Pembroke Pines</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">8357 NW 38th St</p>'
)

# ============================================================
# 7. MARQUEE (x2 bloques, 6 palabras cada una, cada palabra x4 en total)
# ============================================================
marquee_words = [
    ('Classic Set', 'Grooming'),
    ('Hybrid Set', 'Bath &amp; Brush'),
    ('Volume Set', 'Daycare'),
    ('Mega Volume', 'Boarding'),
    ('Bottom Lashes', 'No Cages'),
    ('West Palm Beach, FL', 'Pembroke Pines, FL'),
]
for old_w, new_w in marquee_words:
    old_tag = '<span class="marquee-word">' + old_w + '</span>'
    rep_count(old_tag, 4)
    h = h.replace(old_tag, '<span class="marquee-word">' + new_w + '</span>')

# ============================================================
# 8. LA EXPERIENCIA
# ============================================================
rep(
  'data-es="La experiencia" data-en="The experience">La experiencia',
  'data-es="La experiencia" data-en="The experience">La experiencia'
)
rep(
  '<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
  '<span data-es="Cuidado privado," data-en="Private care,">Private care,</span><br /><span class="text-shine" data-es="no una jaula" data-en="not a cage">not a cage</span>'
)
rep(
  'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.',
  'data-es="Fancy Paws es el estudio de Mila Solis en Pembroke Pines: ella misma baña, corta y cepilla a cada perro, uno a la vez, sin jaulas ni corridas en grupo. Sus clientas cuentan que manda fotos del progreso durante la visita y que es paciente de verdad con perros nerviosos, mayores o ciegos." data-en="Fancy Paws is Mila Solis own studio in Pembroke Pines: she personally bathes, cuts and brushes every dog, one at a time, with no cages or group runs. Her clients say she sends picture updates during the visit and is genuinely patient with nervous, senior or blind dogs.">Fancy Paws is Mila Solis own studio in Pembroke Pines: she personally bathes, cuts and brushes every dog, one at a time, with no cages or group runs. Her clients say she sends picture updates during the visit and is genuinely patient with nervous, senior or blind dogs.'
)
rep(
  'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.',
  'data-es="El resultado: 5.0 perfecto en 57 reseñas de Google, donde una y otra vez se repiten las mismas palabras: dulce, gentil, paciente y atenta a lo que pides para tu mascota." data-en="The result: a perfect 5.0 across 57 Google reviews, where the same words keep coming up: sweet, gentle, patient and attentive to exactly what you ask for your pet.">The result: a perfect 5.0 across 57 Google reviews, where the same words keep coming up: sweet, gentle, patient and attentive to exactly what you ask for your pet.'
)
rep(
  '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
  '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="57">57</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>'
)
rep(
  '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
  '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>'
)
rep(
  '''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,122,99,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>''',
  '''<img src="assets/raw/logo.jpg" alt="Fancy Paws by Mila Solis logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,122,99,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Mila Solis · <span class="text-[color:var(--ink-40)]" data-es="Dueña y groomer" data-en="Owner &amp; groomer">Owner &amp; groomer</span></span>'''
)

# ============================================================
# 9. EL METODO
# ============================================================
rep(
  'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso',
  'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso'
)
rep(
  '<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
  '<span data-es="Tu cita," data-en="Your visit,">Your visit,</span> <span class="text-shine" data-es="paso a paso" data-en="step by step">step by step</span>'
)
rep(
  '''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
  '''<h3 class="font-display text-xl mb-3" data-es="Llama o escribe" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cuéntale a Mila la raza, el tamaño y lo que necesita tu perro. Ella te da el precio por teléfono antes de agendar." data-en="Tell Mila the breed, size and what your dog needs. She gives you the price by phone before you book.">Tell Mila the breed, size and what your dog needs. She gives you the price by phone before you book.</p>'''
)
rep(
  '''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
  '''<h3 class="font-display text-xl mb-3" data-es="Trae a tu peludo" data-en="Drop-off">Drop-off</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llegas al estudio en Pembroke Pines a tu hora agendada. Nada de jaulas de espera ni grupos de perros mezclados." data-en="You arrive at the Pembroke Pines studio at your scheduled time. No waiting cages, no dogs mixed together in a group.">You arrive at the Pembroke Pines studio at your scheduled time. No waiting cages, no dogs mixed together in a group.</p>'''
)
rep(
  '''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
  '''<h3 class="font-display text-xl mb-3" data-es="Grooming uno a uno" data-en="One-on-one grooming">One-on-one grooming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Mila trabaja con tu perro sola, a su ritmo, y te manda fotos del progreso si lo pides. Paciencia real con perros nerviosos o mayores." data-en="Mila works with your dog alone, at their pace, and sends picture updates if you ask. Real patience with nervous or senior dogs.">Mila works with your dog alone, at their pace, and sends picture updates if you ask. Real patience with nervous or senior dogs.</p>'''
)
rep(
  '''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
  '''<h3 class="font-display text-xl mb-3" data-es="Recogida feliz" data-en="Happy pickup">Happy pickup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Recoges a tu perro limpio, tranquilo y oliendo bien, con la próxima cita agendada si quieres." data-en="You pick up your dog clean, calm and smelling great, with the next visit booked if you want.">You pick up your dog clean, calm and smelling great, with the next visit booked if you want.</p>'''
)

# ============================================================
# 10. SERVICIOS (variante adaptada: sin precios publicos -> "se cotiza")
# ============================================================
rep(
  '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
  '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige el" data-en="Choose the">Choose the</span> <span class="text-shine" data-es="cuidado" data-en="care">care</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Mila no publica una lista de precios fija: te cotiza por telefono segun la raza, el tamaño y el pelaje de tu perro." data-en="Mila does not publish a fixed price list: she quotes you by phone based on your dog breed, size and coat.">Mila does not publish a fixed price list: she quotes you by phone based on your dog breed, size and coat.</p>'
)

services_old = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert services_old, 'NO SERVICES GRID MATCH'
services_new = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para el dia a dia" data-en="Everyday fresh">Everyday fresh</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Baño y cepillado" data-en="Bath &amp; Brush-Out">Bath &amp; Brush-Out</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Baño con shampoo, secado y cepillado profundo para aflojar el pelo muerto y dejar menos pelo suelto en casa." data-en="Shampoo bath, blow-dry and a deep brush-out to loosen dead coat and cut down on shedding at home.">Shampoo bath, blow-dry and a deep brush-out to loosen dead coat and cut down on shedding at home.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Se cotiza" data-en="Quote on call">Quote on call</p></div>
            <a href="tel:''' + PHONE_E164 + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(31,122,99,0.4); box-shadow: 0 18px 50px rgba(31,46,42,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo mas pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Grooming completo" data-en="Full Grooming">Full Grooming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte segun la raza, baño, uñas, limpieza de oidos y desenredado, terminado con un bandana o moño Fancy Paws." data-en="Breed-appropriate haircut, bath, nail trim, ear cleaning and de-matting, finished with a Fancy Paws bandana or bow.">Breed-appropriate haircut, bath, nail trim, ear cleaning and de-matting, finished with a Fancy Paws bandana or bow.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Se cotiza" data-en="Quote on call">Quote on call</p></div>
            <a href="tel:''' + PHONE_E164 + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Sin jaulas" data-en="No cages">No cages</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Guarderia" data-en="Doggy Daycare">Doggy Daycare</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cuidado tranquilo y supervisado durante el dia, sin jaulas, con fotos de actualizacion mientras no estas." data-en="Calm, supervised daytime care with no cages, plus picture updates sent while you are away.">Calm, supervised daytime care with no cages, plus picture updates sent while you are away.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Se cotiza" data-en="Quote on call">Quote on call</p></div>
            <a href="tel:''' + PHONE_E164 + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cuando viajas" data-en="When you travel">When you travel</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Hospedaje nocturno" data-en="Overnight Boarding">Overnight Boarding</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una estadia tipo hogar en el estudio de Mila, con la misma atencion uno a uno de cada visita de grooming." data-en="A home-like overnight stay at Mila's studio, with the same one-on-one attention as a grooming visit.">A home-like overnight stay at Mila's studio, with the same one-on-one attention as a grooming visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Se cotiza" data-en="Quote on call">Quote on call</p></div>
            <a href="tel:''' + PHONE_E164 + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_old.start()] + services_new + h[services_old.end():]

rep(
  '<span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span>',
  '<span data-es="Cada visita se cotiza por telefono segun raza, pelaje y tamaño. Sin letra chica, sin precio generico." data-en="Every visit is quoted by phone based on breed, coat and size. No fine print, no one-size price.">Every visit is quoted by phone based on breed, coat and size. No fine print, no one-size price.</span>'
)

# ============================================================
# 11. GALERIA (1 ancha 16/9 + 4 tiles 3/4, solo fotos reales curadas)
# ============================================================
rep(
  '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
  '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Clientes" data-en="Real">Real</span> <span class="text-shine" data-es="felices" data-en="happy clients">happy clients</span></h2>'
)

gallery_old = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert gallery_old, 'NO GALLERY GRID MATCH'
gallery_new = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Recien salidos del spa" data-en="Fresh from the spa">Fresh from the spa</span><img src="assets/raw/gmaps-6.jpg" alt="Dos perros recien peinados con monos festivos en el estudio Fancy Paws" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Herramientas del oficio" data-en="Tools of the trade">Tools of the trade</span><img src="assets/raw/gmaps-9.jpg" alt="Schnauzer recien peinado junto a cepillo y peine de grooming" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Raza pequeña, gran personalidad" data-en="Small breed, big personality">Small breed, big personality</span><img src="assets/raw/gmaps-5.jpg" alt="Chihuahua con corbata de lunares despues de su grooming" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Dos clientes felices" data-en="Two happy regulars">Two happy regulars</span><img src="assets/raw/gmaps-11.jpg" alt="Dos perros recien peinados frente a un cuadro colorido en el estudio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Listos para las fiestas" data-en="Holiday-ready">Holiday-ready</span><img src="assets/raw/gmaps-4.jpg" alt="Dos perros peinados y vestidos para las fiestas con una bolsa de regalo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_old.start()] + gallery_new + h[gallery_old.end():]

# ============================================================
# 12. OPINIONES (reseñas verbatim reales de Google)
# ============================================================
rep(
  '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
  '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="sus clientes" data-en="pet parents say">pet parents say</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 57 reseñas en Google" data-en="5.0 out of 5 · 57 reviews on Google">5.0 out of 5 · 57 reviews on Google</span></p>'
)

testimonios_old = re.search(r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10 reveal">)', h, flags=re.S)
assert testimonios_old, 'NO TESTIMONIOS MATCH'
testimonios_new = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mila is AMAZING! She is so gentle with the dogs, our dogs love her and they always come out looking and smelling amazing! Couldn't recommend her more highly!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Victoria Martinez</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mila has been grooming my dog since her first cut. She always takes good care of Coco. Coco always leaves Fancy Paws happy, with a cute cut and smelling so good. Thank you for treating Coco like your own."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jennifer Horenstein</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mila is very nice and very sweet. My pets warmed up to her right away, and one of them is blind! She took her time and they look great. She is very patient because I know my babies don't trust strangers."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Reina Hernandez</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
      </div>'''
h = h[:testimonios_old.start()] + testimonios_new + h[testimonios_old.end():]

rep(
  '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 57 reseñas en Google" data-en="Read all 57 reviews on Google">Read all 57 reviews on Google</a>',
  '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 57 reseñas en Google" data-en="Read all 57 reviews on Google">Read all 57 reviews on Google</a>'
)

# ============================================================
# 13. UBICACION
# ============================================================
rep(
  'data-es="Visítanos" data-en="Visit us">Visítanos',
  'data-es="Visítanos" data-en="Visit us">Visítanos'
)
rep(
  '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
  '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Pembroke Pines</span>'
)
rep(
  '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,99,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
  '<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light">8357 NW 38th St, Pembroke Pines, FL 33024</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,99,0.4)]" href="https://www.google.com/maps?q=8357+NW+38th+St,+Pembroke+Pines,+FL+33024" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
rep(
  '<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,99,0.4)]" href="tel:' + PHONE_E164 + '" data-es="Llamar para disponibilidad" data-en="Call for availability">Llamar para disponibilidad</a>',
  '<p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>\n              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a viernes 10am a 5pm, sabados 11am a 4pm. Domingos cerrado." data-en="Monday to Friday 10am to 5pm, Saturday 11am to 4pm. Closed Sunday.">Monday to Friday 10am to 5pm, Saturday 11am to 4pm. Closed Sunday.</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,99,0.4)]" href="tel:' + PHONE_E164 + '" data-es="Llamar para disponibilidad" data-en="Call for availability">Llamar para disponibilidad</a>'
)
rep(
  '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,99,0.4)]" href="''' + IG_OLD + '''" target="_blank" rel="noopener">@_lashbloom</a>
            </div>''',
  '''<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Llamar o escribir" data-en="Call or text">Call or text</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Habla directo con Mila antes de tu cita: cuentale la raza y el tamaño de tu perro." data-en="Speak directly with Mila before you book: tell her your dog's breed and size.">Speak directly with Mila before you book: tell her your dog's breed and size.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,122,99,0.4)]" href="tel:''' + PHONE_E164 + '''">''' + PHONE_DISPLAY + '''</a>
            </div>'''
)
rep(
  '<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
  '<iframe title="Mapa: Fancy Paws by Mila Solis, 8357 NW 38th St, Pembroke Pines FL"\n          src="https://www.google.com/maps?q=8357+NW+38th+St,+Pembroke+Pines,+FL+33024&output=embed"'
)

# ============================================================
# 14. CTA FINAL
# ============================================================
rep(
  'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.',
  'data-es="Grooming que tu perro va a disfrutar." data-en="Grooming your dog will actually enjoy.">Grooming your dog will actually enjoy.',
  n=1
)
rep(
  '<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
  '<span data-es="Tu perro" data-en="Your dog">Your dog</span> <span class="text-shine" data-es="se merece este mimo" data-en="deserves this">deserves this</span>'
)
rep(
  'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.',
  'data-es="Llama ahora, cuentale a Mila sobre tu perro y agenda su proximo baño, corte, dia de guarderia u hospedaje." data-en="Call now, tell Mila about your dog and book their next bath, haircut, daycare day or overnight stay.">Call now, tell Mila about your dog and book their next bath, haircut, daycare day or overnight stay.'
)

# ============================================================
# 15. FOOTER
# ============================================================
rep(
  '<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
  '<span class="foot-mark" aria-hidden="true">Fancy Paws</span>'
)
rep(
  '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(159,224,194,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
  '<img src="assets/raw/logo.jpg" alt="Fancy Paws by Mila Solis logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(159,224,194,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Fancy Paws</span>'
)
rep(
  'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.',
  'data-es="Estudio privado de grooming canino en Pembroke Pines, FL. Solo con cita." data-en="Private dog grooming studio in Pembroke Pines, FL. By appointment only.">Private dog grooming studio in Pembroke Pines, FL. By appointment only.'
)
rep(
  '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
  '<p>8357 NW 38th St, Pembroke Pines, FL 33024</p>'
)
rep(
  '© 2026 Lash Bloom.',
  '© 2026 Fancy Paws by Mila Solis.'
)

# ============================================================
# 16. BOOK-FLOAT (boton flotante -> llamar)
# ============================================================
rep(
  '<a href="tel:' + PHONE_E164 + '" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f6fbf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>',
  '<a href="tel:' + PHONE_E164 + '" class="book-float" aria-label="Llamar a Fancy Paws by Mila Solis">\n    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#f6fbf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n    <span class="book-float-label" data-es="Llamar ahora" data-en="Call now">Call now</span>\n  </a>'
)

# ============================================================
# 17. IMAGENES: hero + experiencia (orden: experiencia, hero, logo ya hecho)
# ============================================================
rep(
  '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
  '<img src="assets/raw/gmaps-7.jpg" alt="Pomerania recien peinado con bandana Fancy Paws en el estudio" class="blur-up w-full h-full object-cover" loading="lazy" />'
)
rep(
  '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
  '<img src="assets/raw/gmaps-3.jpg" alt="Bichon frise con bandana Fancy Paws sobre mesa de grooming" class="blur-up w-full h-full object-cover" loading="lazy" />'
)
rep(
  '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
  '<img src="assets/raw/gmaps-8.jpg" alt="Perro caniche recien peinado con moño rosa despues de su grooming" class="blur-up w-full h-full object-cover" />'
)

open(PATH, 'w').write(h)
print('PART 2 OK, len=', len(h))
