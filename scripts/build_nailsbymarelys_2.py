import re

h = open('output/nailsbymarelys/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/608679_nails-by-marelys_nail-salon_15886_hialeah'
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
NEW_IG_URL = 'https://www.instagram.com/nailsby_marelyspacheco/'
h = h.replace(OLD_IG_URL, NEW_IG_URL)
h = h.replace('@_lashbloom', '@nailsby_marelyspacheco')

# logo: usar bk-2.jpg (monograma M, 150x150) en vez de logo.jpg
h = h.replace('assets/raw/logo.jpg', 'assets/raw/bk-2.jpg')

# ---------- HEAD ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Nails by Marelys · Nail Salon in Hialeah, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Nails by Marelys, Hialeah FL: gel, dip powder and acrylic manicures, pedicures and waxing, with a perfect 5.0 across 89 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Nails by Marelys · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel, dip powder and acrylic nails. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />')

old_ldjson = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_ldjson = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nails by Marelys",
    "description": "Nail salon in Hialeah, FL: gel, dip powder and acrylic manicures, pedicures and waxing.",
    "address": { "@type": "PostalAddress", "streetAddress": "8803 NW 107th Ln", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33018", "addressCountry": "US" },
    "sameAs": ["''' + BOOKSY + '''", "https://www.instagram.com/nailsby_marelyspacheco/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "89", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure & Pedicure Regular" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Gel & Pedicure Regular" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Acrylic Full Set" } },
      { "@type": "Offer", "price": "5", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "French Pedicure" } }
    ] }
  }
  </script>'''
assert old_ldjson in h
h = h.replace(old_ldjson, new_ldjson, 1)

# ---------- PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">NM</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Nails by Marelys</span>')

# ---------- NAV ----------
rep('<img src="assets/raw/bk-2.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,100,74,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Nails by Marelys" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,100,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails by <span class="text-[color:var(--accent-deep)]">Marelys</span></span>')

# ---------- HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Hialeah, FL · Nail Salon" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Uñas hechas con dedicación." data-en="Nails made with dedication.">Nails made with dedication.</p>', 2)
rep('''<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>''',
    '''<span data-es="Gel, dip powder y acrílico," data-en="Gel, dip powder and acrylic">Gel, dip powder and acrylic</span><br /><span data-es="uñas hechas para " data-en="nails made to ">nails made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>''')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura y pedicura en gel, dip powder y acrílico, con diseños y toques franceses, todo hecho a mano por una sola técnica. Un espacio de confianza en Hialeah con 5.0 perfecto en 89 reseñas de Booksy." data-en="Gel, dip powder and acrylic manicures and pedicures, with nail art and French touches, all hand-finished by one nail tech. A trusted spot in Hialeah with a perfect 5.0 across 89 Booksy reviews.">Gel, dip powder and acrylic manicures and pedicures, with nail art and French touches, all hand-finished by one nail tech. A trusted spot in Hialeah with a perfect 5.0 across 89 Booksy reviews.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 89 reseñas en Booksy" data-en="5.0 · 89 reviews on Booksy">5.0 · 89 reviews on Booksy</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-6.jpg" alt="Nude gel manicure with a gold foil accent nail at Nails by Marelys, Hialeah" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Gel Manicure &amp; Pedicure</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$70 · 1h 30min" data-en="$70 · 1h 30min">$70 · 1h 30min</p>')

# ---------- STRIP ----------
rep('<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-count="89">89</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Dip</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">1:1</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Una técnica, atención de cerca" data-en="One tech, close attention">One tech, close attention</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">8803 NW 107th Ln</p></div>')

# ---------- MARQUEE (x2, 4 ocurrencias por palabra) ----------
marquee_words = [
    ('Classic Set', 'Gel Manicure'),
    ('Hybrid Set', 'Dip Powder'),
    ('Volume Set', 'Acrylic Full Set'),
    ('Mega Volume', 'Gel Pedicure'),
    ('Bottom Lashes', 'Nail Art'),
    ('West Palm Beach, FL', 'Hialeah, FL'),
]
for old, new in marquee_words:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f'{old_span}: {h.count(old_span)}'
    h = h.replace(old_span, new_span)

open('output/nailsbymarelys/index.html', 'w').write(h)
print('head+preloader+nav+hero+strip+marquee OK')
