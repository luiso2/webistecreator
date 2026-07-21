import re

h = open('output/nailstudiomiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- HEAD ----------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>The Nail Studio Miami · Nail Salon in Miami, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="The Nail Studio Miami, Miami FL: gel and acrylic manicures, Apres Gel X, pedicures and waxing, with a 5.0 rating across 52 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="The Nail Studio Miami · Nail Salon in Miami, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel, acrylic and Apres nails. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-3.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_ldjson = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_ldjson = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "The Nail Studio Miami",
    "description": "Nail salon in Miami, FL: gel and acrylic manicures, Apres Gel X, pedicures and waxing.",
    "address": { "@type": "PostalAddress", "streetAddress": "8944 SW 152nd Path", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33196", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/418314_the-nail-studio-miami_nail-salon_15889_miami", "https://www.instagram.com/thenailstudiomiami/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "52", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicure & Pedicure" } },
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Refills with Gel Polish & Gel Pedicure" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres Gel X Fullset" } },
      { "@type": "Offer", "price": "55", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Regular Manicure & Regular Pedicure" } }
    ] }
  }
  </script>'''
assert old_ldjson in h
h = h.replace(old_ldjson, new_ldjson, 1)

# ---------- PRELOADER ----------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">TN</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">The Nail Studio</span>')

# ---------- NAV ----------
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(120,160,210,0.4)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="The Nail Studio Miami" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(120,160,210,0.4)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nail Studio <span class="text-[color:var(--accent-deep)]">Miami</span></span>')

# ---------- HERO ----------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Miami, FL · Nail Salon" data-en="Miami, FL · Nail Salon">Miami, FL · Nail Salon</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Uñas tratadas como arte." data-en="Nails treated like art.">Nails treated like art.</p>', 2)
rep('''<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>''',
    '''<span data-es="Uñas en gel, acrílico" data-en="Gel, acrylic and Apres">Gel, acrylic and Apres</span><br /><span data-es="y Apres, hechas para " data-en="nails made to ">nails made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>''')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Sets completos en gel y acrílico, Apres Gel X, pedicura clásica y en gel, y depilación con cera, todo con una sola técnica a la que sus clientas vuelven una y otra vez. Un espacio relajante en West Kendall con 5.0 perfecto en 52 reseñas de Booksy." data-en="Full gel and acrylic sets, Apres Gel X, classic and gel pedicures, and clean waxing, all from one nail tech clients keep coming back to. A relaxing space in West Kendall with a perfect 5.0 across 52 Booksy reviews.">Full gel and acrylic sets, Apres Gel X, classic and gel pedicures, and clean waxing, all from one nail tech clients keep coming back to. A relaxing space in West Kendall with a perfect 5.0 across 52 Booksy reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 52 reseñas en Booksy" data-en="5.0 · 52 reviews on Booksy">5.0 · 52 reviews on Booksy</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-3.jpg" alt="Coffin-shaped ombre gel manicure finished at The Nail Studio Miami" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg">Gel Manicure &amp; Pedicure</p>')
rep('data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="$70 · 2h" data-en="$70 · 2h">$70 · 2h</p>')

# ---------- STRIP ----------
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
    '<span data-count="52">52</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Acrylic</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+18 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Una técnica, clientas fieles" data-en="One tech, loyal clients">One tech, loyal clients</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">8944 SW 152nd Path</p></div>')

# ---------- MARQUEE (x2 idénticos, x4 ocurrencias por palabra) ----------
marquee_words = [
    ('Silk Press', 'Gel Manicure'),
    ('Loc Retwist', 'Acrylic Refills'),
    ('Knotless Braids', 'Apres Gel X'),
    ('K-Tip Extensions', 'Gel Pedicure'),
    ('Keratin', 'Nail Art'),
    ('Orlando, FL', 'Miami, FL'),
]
for old, new in marquee_words:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f'{old_span}: {h.count(old_span)}'
    h = h.replace(old_span, new_span)

open('output/nailstudiomiami/index.html', 'w').write(h)
print('head+preloader+nav+hero+strip+marquee OK')
