import re

h = open('output/iloveawaxingmiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/1037088_i-love-waxing-miami_hair-removal_15889_miami'
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
NEW_IG_URL = 'https://www.instagram.com/ilovewaxingmiami/'
h = h.replace(OLD_IG_URL, NEW_IG_URL)
h = h.replace('@_lashbloom', '@ilovewaxingmiami')

# logo: bk-2.jpg es el logo real de la marca (grafica rosa "I Love Waxing Studio Miami")
h = h.replace('assets/raw/logo.jpg', 'assets/raw/bk-2.jpg')

# ---------- HEAD ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>I Love Waxing Miami · Waxing Studio in Miami, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="I Love Waxing Miami, on Biscayne Blvd: Brazilian, bikini, brow and full body waxing with a perfect 5.0 across 111 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="I Love Waxing Miami · Waxing Studio in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Brazilian, bikini, brow and body waxing. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />')
rep('<meta name="theme-color" content="#f6f4ea" />',
    '<meta name="theme-color" content="#faf0ea" />')

old_ldjson = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_ldjson = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "I Love Waxing Miami",
    "description": "Waxing studio in Miami, FL: Brazilian, bikini, brow, face and full body waxing by appointment.",
    "address": { "@type": "PostalAddress", "streetAddress": "2915 Biscayne Blvd, Suite 200-75", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33137", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.8045, "longitude": -80.18916 },
    "sameAs": ["''' + BOOKSY + '''", "''' + NEW_IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "111", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "09:00", "closes": "14:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "09:00", "closes": "12:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Friday"], "opens": "09:00", "closes": "15:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Thursday", "opens": "11:00", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Waxing services", "itemListElement": [
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "I Love Waxing Bikini" } },
      { "@type": "Offer", "price": "20", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Eyebrows" } },
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Legs" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Face" } }
    ] }
  }
  </script>'''
assert old_ldjson in h
h = h.replace(old_ldjson, new_ldjson, 1)

# ---------- PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">IW</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">I Love Waxing</span>')

# ---------- NAV ----------
rep('<img src="assets/raw/bk-2.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,92,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="I Love Waxing Miami" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,92,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">I Love <span class="text-[color:var(--accent-deep)]">Waxing</span></span>')

# ---------- HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Waxing Studio" data-en="Miami, FL · Waxing Studio">Miami, FL · Waxing Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Piel suave, sin apuros." data-en="Smooth skin, no rush.">Smooth skin, no rush.</p>', 2)
rep('''<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>''',
    '''<span data-es="Cera brasileña, cejas y cuerpo" data-en="Brazilian, brow and body">Brazilian, brow and body</span><br /><span data-es="completo, hecha para " data-en="waxing, made to ">waxing, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>''')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Cera brasileña, bikini, cejas, rostro y cuerpo completo en un suite privado sobre Biscayne Blvd. Gisele lleva más de una década perfeccionando cada cita, con clientas que la siguen desde entonces." data-en="Brazilian, bikini, brow, face and full body waxing in a private suite on Biscayne Blvd. Gisele has spent over a decade perfecting every appointment, with clients who have followed her ever since.">Brazilian, bikini, brow, face and full body waxing in a private suite on Biscayne Blvd. Gisele has spent over a decade perfecting every appointment, with clients who have followed her ever since.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 111 reseñas en Booksy" data-en="5.0 · 111 reviews on Booksy">5.0 · 111 reviews on Booksy</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Closeup of a brow and skin finish at I Love Waxing Miami" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Diva Bikini</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$65 · 1h" data-en="$65 · 1h">$65 · 1h</p>')

# ---------- STRIP ----------
rep('<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-count="111">111</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Brazilian <span class="text-shine">&amp;</span> Brow</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cera · Depilación" data-en="Waxing · Tinting">Waxing · Tinting</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+10 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">2915 Biscayne Blvd</p></div>')

# ---------- MARQUEE (x2, 4 ocurrencias por palabra) ----------
marquee_words = [
    ('Classic Set', 'Brazilian Wax'),
    ('Hybrid Set', 'Brow Wax'),
    ('Volume Set', 'Full Legs'),
    ('Mega Volume', 'Underarms'),
    ('Bottom Lashes', 'Full Face'),
    ('West Palm Beach, FL', 'Miami, FL'),
]
for old, new in marquee_words:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f'{old_span}: {h.count(old_span)}'
    h = h.replace(old_span, new_span)

open('output/iloveawaxingmiami/index.html', 'w').write(h)
print('head+preloader+nav+hero+strip+marquee OK')
