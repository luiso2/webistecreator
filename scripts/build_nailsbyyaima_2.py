import re

h = open('output/nailsbyyaima/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/1019645_nails-by-yaima_nail-salon_15761_tampa'
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/nailsbyyaima/'
assert h.count(OLD_IG_URL) >= 1
h = h.replace(OLD_IG_URL, NEW_IG_URL)
h = h.replace('@pure.artistrysk', '@nailsbyyaima')

# nota: el logo real (bk-2.jpg, wordmark dorado sobre negro) coincide con el mismo
# archivo que el esqueleto ya usaba para nav/footer/avatar: NO hace falta swap global.
# Solo el uso de bk-2.jpg como FOTO 1 de experiencia (no logo) se reemplaza en el script 3.

# ---------- HEAD ----------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Nails by Yaima · Nail Salon in Tampa, FL | Manicures, Russian Gel &amp; Builder Gel | 5.0 on Booksy</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Nails by Yaima, Tampa FL: classic and luxury spa manicures, Russian gel, builder gel overlays and nail extensions by Yaima Perdomo. 5.0 with 159 reviews on Booksy. Book online." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Nails by Yaima · Nail Salon in Tampa, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Manicures, Russian gel, builder gel and nail extensions. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-3.jpg" />')
old_ldjson = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_ldjson = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nails by Yaima",
    "description": "Nail salon in Tampa, FL: classic and luxury spa manicures, Russian gel manicures, builder gel overlays, refills and nail extensions, by appointment only.",
    "address": { "@type": "PostalAddress", "streetAddress": "7340 Ponderosa Dr", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33637", "addressCountry": "US" },
    "telephone": "+1-813-493-7405",
    "sameAs": ["''' + BOOKSY + '''", "https://www.instagram.com/nailsbyyaima/", "https://www.facebook.com/nailsbyyaima/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "159", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "23", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic Manicure" } },
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Russian Gel Manicure" } },
      { "@type": "Offer", "price": "59", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder Gel Overlay" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder Gel Nail Extensions (long)" } }
    ] }
  }
  </script>'''
assert old_ldjson in h
h = h.replace(old_ldjson, new_ldjson, 1)

# ---------- PRELOADER ----------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">NY</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Nails by Yaima</span>')

# ---------- NAV ----------
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,191,75,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Nails by Yaima" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,191,75,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails by <span class="text-[color:var(--accent-deep)]">Yaima</span></span>')

# ---------- HERO ----------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Tampa, FL · Nail Salon" data-en="Tampa, FL · Nail Salon">Tampa, FL · Nail Salon</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Técnica maestra de uñas en Tampa." data-en="Master Nail Technician in Tampa.">Master Nail Technician in Tampa.</p>', 2)
rep('''<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>''',
    '''<span data-es="Manicura, gel ruso y" data-en="Manicures, Russian gel and">Manicures, Russian gel and</span><br /><span data-es="extensiones hechas para " data-en="extensions built to ">extensions built to </span><span class="text-shine" data-es="durar" data-en="last">last</span>''')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Manicura clásica y de spa, gel ruso, overlay y extensiones en builder gel, hechas a mano una cita a la vez por Yaima Perdomo. 5.0 perfecto en 159 reseñas de Booksy, servicio en inglés y español." data-en="Classic and luxury spa manicures, Russian gel, builder gel overlays and nail extensions, done one appointment at a time by Yaima Perdomo. A perfect 5.0 across 159 Booksy reviews, service in English and Spanish.">Classic and luxury spa manicures, Russian gel, builder gel overlays and nail extensions, done one appointment at a time by Yaima Perdomo. A perfect 5.0 across 159 Booksy reviews, service in English and Spanish.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 159 reseñas en Booksy" data-en="5.0 · 159 reviews on Booksy">5.0 · 159 reviews on Booksy</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-3.jpg" alt="Glossy natural pink manicure at Nails by Yaima, Tampa" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg">Russian Gel Manicure</p>')
rep('data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="$75 · 1h 15min" data-en="$75 · 1h 15min">$75 · 1h 15min</p>')

# ---------- STRIP DE CONFIANZA ----------
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
    '<span data-count="159">159</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Russian</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicura · Overlay · Refill" data-en="Manicure · Overlay · Refill">Manicure · Overlay · Refill</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">EN <span class="text-shine">&amp;</span> ES</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Servicio en inglés y español" data-en="Service in English &amp; Spanish">Service in English &amp; Spanish</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">7340 Ponderosa Dr</p></div>')

# ---------- MARQUEE (x2, 4 ocurrencias por palabra) ----------
marquee_words = [
    ('Silk Press', 'Russian Gel'),
    ('Loc Retwist', 'Builder Gel'),
    ('Knotless Braids', 'Nail Extensions'),
    ('K-Tip Extensions', 'Classic Manicure'),
    ('Keratin', 'Spa Manicure'),
    ('Orlando, FL', 'Tampa, FL'),
]
for old, new in marquee_words:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f'{old_span}: {h.count(old_span)}'
    h = h.replace(old_span, new_span)

open('output/nailsbyyaima/index.html', 'w').write(h)
print('head+preloader+nav+hero+strip+marquee OK')
