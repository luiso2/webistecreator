import re

h = open('output/trulyblessedspa/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/1780520_truly-blessed-spa-boutique-llc_wellness-day-spa_15746_brandon'
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
NEW_IG_URL = 'https://www.instagram.com/truly_blessed_spa/'
h = h.replace(OLD_IG_URL, NEW_IG_URL)
h = h.replace('@_lashbloom', '@truly_blessed_spa')

# logo: usar bk-2.jpg (logo real, corazon morado) en vez de logo.jpg
h = h.replace('assets/raw/logo.jpg', 'assets/raw/bk-2.jpg')

# ---------- HEAD ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Truly Blessed Spa &amp; Boutique · Day Spa &amp; Nail Studio in Brandon, FL | 4.9 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Truly Blessed Spa &amp; Boutique, Brandon FL: nails, pedicures, waxing, facials and body contouring, with a 4.9 rating across 30 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Truly Blessed Spa &amp; Boutique · Day Spa &amp; Nail Studio in Brandon, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Nails, waxing, facials and body contouring. 4.9 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-14.jpg" />')

old_ldjson = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_ldjson = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "DaySpa",
    "name": "Truly Blessed Spa & Boutique LLC",
    "description": "Day spa and nail studio in Brandon, FL: nails, pedicures, waxing, facials and body contouring (cavitation and lymphatic massage).",
    "address": { "@type": "PostalAddress", "streetAddress": "873 E Bloomingdale Ave, 7A", "addressLocality": "Brandon", "addressRegion": "FL", "postalCode": "33511", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 27.89353, "longitude": -82.27194 },
    "sameAs": ["''' + BOOKSY + '''", "https://www.instagram.com/truly_blessed_spa/", "https://www.facebook.com/100066638177749"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "30", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday"], "opens": "09:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday"], "opens": "09:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "16:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Spa & nail services", "itemListElement": [
      { "@type": "Offer", "price": "71", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Ombré nail set" } },
      { "@type": "Offer", "price": "51", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Ultimate Pedicure" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Skin Treatment Facial" } },
      { "@type": "Offer", "price": "19", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Cavitation W/ RF & Lymphatic Massage" } }
    ] }
  }
  </script>'''
assert old_ldjson in h
h = h.replace(old_ldjson, new_ldjson, 1)

# ---------- PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">TB</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Truly Blessed</span>')

# ---------- NAV ----------
rep('<img src="assets/raw/bk-2.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(139,74,160,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Truly Blessed Spa & Boutique" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(139,74,160,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Truly <span class="text-[color:var(--accent-deep)]">Blessed</span></span>')

# ---------- HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Brandon, FL · Day Spa &amp; Nail Studio" data-en="Brandon, FL · Day Spa &amp; Nail Studio">Brandon, FL · Day Spa &amp; Nail Studio</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Self-care, truly blessed." data-en="Self-care, truly blessed.">Self-care, truly blessed.</p>', 2)
rep('''<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>''',
    '''<span data-es="Nails, facials and body" data-en="Nails, facials and body">Nails, facials and body</span><br /><span data-es="contouring, made to make you " data-en="contouring, made to make you ">contouring, made to make you </span><span class="text-shine" data-es="glow" data-en="glow">glow</span>''')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Nails from Gel-X to Ombré, pedicures, waxing, facials and cavitation with lymphatic massage, all in one boutique suite in Brandon. A rating of 4.9 across 30 Booksy reviews, with clients returning again and again." data-en="Nails from Gel-X to Ombré, pedicures, waxing, facials and cavitation with lymphatic massage, all in one boutique suite in Brandon. A 4.9 rating across 30 Booksy reviews, with clients coming back again and again.">Nails from Gel-X to Ombré, pedicures, waxing, facials and cavitation with lymphatic massage, all in one boutique suite in Brandon. A 4.9 rating across 30 Booksy reviews, with clients coming back again and again.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 30 reseñas en Booksy" data-en="4.9 · 30 reviews on Booksy">4.9 · 30 reviews on Booksy</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-14.jpg" alt="Finished ombre nail art set at Truly Blessed Spa &amp; Boutique, Brandon" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Ombré Nail Set</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$71" data-en="$71">$71</p>')

# ---------- STRIP ----------
rep('<span data-count="5.0" data-decimals="1">5.0</span>', '<span data-count="4.9" data-decimals="1">4.9</span>', 2)
rep('<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-count="30">30</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Nails <span class="text-shine">&amp;</span> Body</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel-X · Contorno corporal" data-en="Gel-X · Body contouring">Gel-X · Body contouring</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">39+</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicios en el menu" data-en="Services on the menu">Services on the menu</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Brandon, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">873 E Bloomingdale Ave</p></div>')

# ---------- MARQUEE (x2, 4 ocurrencias por palabra) ----------
marquee_words = [
    ('Classic Set', 'Gel-X'),
    ('Hybrid Set', 'Ombré'),
    ('Volume Set', 'Pedicure'),
    ('Mega Volume', 'Body Contouring'),
    ('Bottom Lashes', 'Facials'),
    ('West Palm Beach, FL', 'Brandon, FL'),
]
for old, new in marquee_words:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f'{old_span}: {h.count(old_span)}'
    h = h.replace(old_span, new_span)

open('output/trulyblessedspa/index.html', 'w').write(h)
print('head+preloader+nav+hero+strip+marquee OK')
