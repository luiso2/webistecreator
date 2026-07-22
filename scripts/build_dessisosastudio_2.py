import re

h = open('output/dessisosastudio/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:200]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/57332_dessisosa-studio_nail-salon_15761_tampa'
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/dessisosastudio/'
h = h.replace(OLD_IG_URL, NEW_IG_URL)
h = h.replace('@pure.artistrysk', '@dessisosastudio')

# ---------- IDIOMA: negocio ES, default espanol ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- HEAD ----------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>DessiSosa Studio · Nail Salon &amp; Lash Studio en Tampa, FL | 5.0 en Booksy</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="DessiSosa Studio, Tampa FL: manicura en gel, acrilico, polygel y pedicure, mas extension de pestanas y diseno de cejas. 5.0 perfecto en 46 resenas de Booksy. Reserva en linea." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="DessiSosa Studio · Nail Salon &amp; Lash Studio en Tampa, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Unas en gel y acrilico, pedicure y extension de pestanas. 5.0 en Booksy. Reserva en linea." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-11.jpg" />')

old_ldjson = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_ldjson = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "DessiSosa Studio",
    "description": "Nail salon y lash studio en Tampa, FL: manicura en gel, acrilico, polygel, rubber gel y builder gel, pedicure, extension de pestanas y diseno de cejas.",
    "address": { "@type": "PostalAddress", "streetAddress": "7208 North Armenia Avenue, Suite B", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33604", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.0043, "longitude": -82.45143 },
    "sameAs": ["''' + BOOKSY + '''", "''' + NEW_IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "46", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "10:00", "closes": "19:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de unas y pestanas", "itemListElement": [
      { "@type": "Offer", "price": "115", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Extension de pestanas" } },
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicura gel" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic nails" } }
    ] }
  }
  </script>'''
assert old_ldjson in h
h = h.replace(old_ldjson, new_ldjson, 1)

# ---------- PRELOADER ----------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">DS</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">DessiSosa Studio</span>')

# ---------- NAV ----------
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,98,212,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="DessiSosa Studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,98,212,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">DessiSosa <span class="text-[color:var(--accent-deep)]">Studio</span></span>')

# ---------- HERO ----------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Tampa, FL · Nail &amp; Lash Studio" data-en="Tampa, FL · Nail &amp; Lash Studio">Tampa, FL · Nail &amp; Lash Studio</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Uñas y pestañas, hechas con dedicación." data-en="Nails and lashes, made with dedication.">Uñas y pestañas, hechas con dedicación.</p>', 2)
rep('''<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>''',
    '''<span data-es="Uñas y pestañas," data-en="Nails and lashes,">Uñas y pestañas,</span><br /><span data-es="hechas para " data-en="made to ">hechas para </span><span class="text-shine" data-es="brillar" data-en="shine">brillar</span>''')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Manicura en gel, acrílico, polygel y rubber gel, pedicure y extensión de pestañas clásica o de volumen, todo en un suite privado en el norte de Tampa. Un equipo de tres técnicas con 5.0 perfecto en 46 reseñas de Booksy." data-en="Gel, acrylic, polygel and rubber gel manicures, pedicures and classic or volume lash extensions, all in a private suite in North Tampa. A team of three technicians with a perfect 5.0 across 46 Booksy reviews.">Manicura en gel, acrílico, polygel y rubber gel, pedicure y extensión de pestañas clásica o de volumen, todo en un suite privado en el norte de Tampa. Un equipo de tres técnicas con 5.0 perfecto en 46 reseñas de Booksy.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 46 reseñas en Booksy" data-en="5.0 · 46 reviews on Booksy">5.0 · 46 reseñas en Booksy</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-11.jpg" alt="Manicura terminada con diseño en blanco y rosa en DessiSosa Studio, Tampa" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg">Manicura Gel</p>')
rep('data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="Desde $30 · 1h 30min" data-en="From $30 · 1h 30min">Desde $30 · 1h 30min</p>')

# ---------- STRIP ----------
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
    '<span data-count="46">46</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Uñas <span class="text-shine">&amp;</span> Pestañas</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel · Acrílico · Extensiones" data-en="Gel · Acrylic · Extensions">Gel · Acrílico · Extensiones</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Se habla" data-en="We speak">Se habla</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Español" data-en="Spanish">Español</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">N Armenia Ave</p></div>')

# ---------- MARQUEE (x2, 4 ocurrencias por palabra) ----------
marquee_words = [
    ('Silk Press', 'Extensión de Pestañas'),
    ('Loc Retwist', 'Retoque de Pestañas'),
    ('Knotless Braids', 'Manicura Gel'),
    ('K-Tip Extensions', 'Pedicure'),
    ('Keratin', 'Acrylic Nails'),
    ('Orlando, FL', 'Tampa, FL'),
]
for old, new in marquee_words:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f'{old_span}: {h.count(old_span)}'
    h = h.replace(old_span, new_span)

open('output/dessisosastudio/index.html', 'w').write(h)
print('head+preloader+nav+hero+strip+marquee OK')
