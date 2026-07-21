import re

h = open('output/vivianatales/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/941017_viviana-tales-lash-studio_brows-lashes_15889_miami'

# ---------- HEAD ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Viviana Tales Lash Studio · Estudio de Pestañas en Doral, FL | 5.0 en Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Viviana Tales Lash Studio, Doral FL: pestañas clásicas, volumen suave, wispy y mega volumen, laminado de cejas y henna. 5.0 en 35 reseñas de Booksy. Reserva online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Viviana Tales Lash Studio · Estudio de Pestañas en Doral, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Pestañas clásicas, volumen suave y wispy. 5.0 en Booksy. Reserva online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-6.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_ldjson = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_ldjson = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Viviana Tales Lash Studio",
    "description": "Estudio de pestañas en Doral, FL: sets clásicos, volumen suave, wispy y mega volumen, laminado de cejas y henna.",
    "address": { "@type": "PostalAddress", "streetAddress": "10640 NW 27th St", "addressLocality": "Doral", "addressRegion": "FL", "postalCode": "33172", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/941017_viviana-tales-lash-studio_brows-lashes_15889_miami", "https://www.instagram.com/vivianataleslashstudio/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "35", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Lash services", "itemListElement": [
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic Full Set" } },
      { "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Soft Volume Lashes" } },
      { "@type": "Offer", "price": "140", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Wispy Lashes" } },
      { "@type": "Offer", "price": "150", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Mega Volume Full Set" } }
    ] }
  }
  </script>'''
assert old_ldjson in h
h = h.replace(old_ldjson, new_ldjson, 1)

# ---------- PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">VT</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Viviana Tales</span>')

# ---------- NAV ----------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(140,63,82,0.37)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Viviana Tales Lash Studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(140,63,82,0.37)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Viviana <span class="text-[color:var(--accent-deep)]">Tales</span></span>')

# ---------- HERO ----------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Doral, FL · Estudio de Pestañas" data-en="Doral, FL · Lash Studio">Doral, FL · Estudio de Pestañas</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Pestañas que cuentan tu historia." data-en="Lashes that tell your story.">Pestañas que cuentan tu historia.</p>', 2)
rep('''<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>''',
    '''<span data-es="Pestañas clásicas, volumen" data-en="Classic, soft volume and">Pestañas clásicas, volumen</span><br /><span data-es="suave y wispy, hechas para " data-en="wispy lashes, made to ">suave y wispy, hechas para </span><span class="text-shine" data-es="brillar" data-en="shine">brillar</span>''')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Sets completos clásicos, de volumen suave, wispy y mega volumen, más laminado de cejas y henna, con Viviana Tales en Doral. Una sola artista, atención personalizada y 5.0 perfecto en 35 reseñas de Booksy." data-en="Full classic, soft volume, wispy and mega volume sets, plus brow lamination and henna, with Viviana Tales in Doral. One artist, personal attention, and a perfect 5.0 across 35 Booksy reviews.">Sets completos clásicos, de volumen suave, wispy y mega volumen, más laminado de cejas y henna, con Viviana Tales en Doral. Una sola artista, atención personalizada y 5.0 perfecto en 35 reseñas de Booksy.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 35 reseñas en Booksy" data-en="5.0 · 35 reviews on Booksy">5.0 · 35 reseñas en Booksy</span>')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-6.jpg" alt="Extensión de pestañas terminada de cerca en Viviana Tales Lash Studio" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Soft Volume Lashes</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$130 · 1h 30min" data-en="$130 · 1h 30min">$130 · 1h 30min</p>')

# ---------- STRIP ----------
rep('<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-count="35">35</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Clásico <span class="text-shine">&amp;</span> Volumen</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Sets completos · Rellenos</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Cejas <span class="text-shine">&amp;</span> Henna</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Laminado y diseño" data-en="Lamination &amp; design">Laminado y diseño</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Doral, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">10640 NW 27th St</p></div>')

# ---------- MARQUEE ----------
marquee_words = [
    ('Classic Set', 'Classic Set'),
    ('Hybrid Set', 'Soft Volume'),
    ('Volume Set', 'Wispy Lashes'),
    ('Mega Volume', 'Mega Volume'),
    ('Bottom Lashes', 'Brow Lamination'),
    ('West Palm Beach, FL', 'Doral, FL'),
]
for old, new in marquee_words:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f'{old_span}: {h.count(old_span)}'
    h = h.replace(old_span, new_span)

open('output/vivianatales/index.html', 'w').write(h)
print('head+preloader+nav+hero+strip+marquee OK')
