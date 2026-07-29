import re

SLUG = 'emery-beauty-bar-cape-coral'
PATH = f'output/{SLUG}/index.html'
h = open(PATH, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c >= 1, 'NO ANCHOR: ' + a[:120]
    if n == 'all':
        h = h.replace(a, b)
    else:
        assert c == n, f'expected {n} occurrences, found {c}: ' + a[:120]
        h = h.replace(a, b, n)


# ============================================================
# 1) PALETA: lash-plum -> emery terracotta-rose (warm cream base)
# ============================================================
PALETTE = [
    ('#f6f1ea', '#f6ece0'),
    ('#faf2f6', '#fbf3ec'),
    ('#f3e0ea', '#f4e0d0'),
    ('#33222c', '#3a2820'),
    ('#a04a72', '#a8524a'),
    ('#c47a9c', '#c9846a'),
    ('#5c2140', '#5c2d29'),
    ('#f0bed7', '#f0c9a8'),
    ('#8a5573', '#8a5a3f'),
    ('#d9a8c2', '#d9b295'),
    ('#7d3457', '#7a3d28'),
    ('#5f2c48', '#6b3224'),
    ('#fbf3f8', '#fbf3ee'),
    ('#fbeff5', '#fbf1e7'),
    ('#f8dfeb', '#f8e6d3'),
    ('#f2d5e3', '#f2ddc9'),
    ('#f2cfe0', '#f2ddc7'),
    ('#efd0e0', '#efddc7'),
    ('#e5c1d4', '#e5c9ae'),
    ('#dc9dbe', '#dcae8f'),
    ('#d3a2bc', '#d3ae8f'),
    ('#c9789f', '#cf8f74'),
    ('#b25a85', '#b9684f'),
    ('#2a1722', '#2a1c14'),
    ('#1f0f18', '#1f130c'),
    ('#1c0f16', '#1c130c'),
]
for a, b in PALETTE:
    rep(a, b, 'all')

RGBA_PALETTE = [
    ('160,74,114', '168,82,74'),
    ('51,34,44', '58,40,32'),
    ('240,190,215', '240,201,168'),
    ('70,25,50', '92,42,25'),
    ('250,242,246', '251,243,236'),
    ('125,52,87', '122,61,40'),
    ('253,246,250', '255,248,240'),
    ('40,16,30', '42,28,20'),
    ('185,138,128', '197,148,110'),
]
for a, b in RGBA_PALETTE:
    rep(a, b, 'all')

print('palette OK')

# ============================================================
# 2) GLOBALES: booking URL, IG, logo -> avatar real
# ============================================================
BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
GG = 'https://emerybeautybar.glossgenius.com/'
rep(BOOKSY, GG, 'all')

rep('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/emerybeautybar/', 'all')
rep('@_lashbloom', '@emerybeautybar', 'all')

# logo.jpg no existe para este negocio: reusar bk-7 (cierre de ceja terminado, ojo abierto) como avatar
rep('assets/raw/logo.jpg', 'assets/raw/bk-7.jpg', 'all')
rep('alt="Lash Bloom"', 'alt="Emery Beauty Bar esthetician logo"', 'all')

print('globales OK')

# ============================================================
# 3) HEAD: title, meta, JSON-LD
# ============================================================
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Emery Beauty Bar · Esthetician &amp; Waxing Bar in Cape Coral, FL | 5.0 on Google</title>',
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Emery Beauty Bar, Cape Coral FL: custom facials, full-body waxing, brow lamination and body sculpting with a perfect 5.0 across 64 Google reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Emery Beauty Bar · Esthetician &amp; Waxing Bar in Cape Coral, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Facials, waxing, brows and body treatments. 5.0 on Google. Book online." />',
)
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-9.jpg" />')

old_ldjson = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, flags=re.S)
assert old_ldjson, 'no JSON-LD found'
new_ldjson = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Emery Beauty Bar",
    "description": "Esthetician and waxing bar in Cape Coral, FL: custom facials, full-body waxing, brow lamination and body sculpting treatments.",
    "telephone": "+17544447046",
    "email": "emerybeautybar@gmail.com",
    "address": { "@type": "PostalAddress", "streetAddress": "900 SW Pine Island Rd Suite 209", "addressLocality": "Cape Coral", "addressRegion": "FL", "postalCode": "33993", "addressCountry": "US" },
    "sameAs": ["https://emerybeautybar.glossgenius.com/", "https://www.instagram.com/emerybeautybar/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "64", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Esthetician services", "itemListElement": [
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "60 min Customized European Facial" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brazilian Wax (Female)" } },
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brow Lamination" } },
      { "@type": "Offer", "price": "150", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Body Sculpting Treatment" } }
    ] }
  }
  </script>'''
h = h[:old_ldjson.start()] + new_ldjson + h[old_ldjson.end():]

print('head OK')

open(PATH, 'w', encoding='utf-8').write(h)
print('checkpoint 1 written, continue in part 2')

# ============================================================
# 4) PRELOADER + NAV BRAND
# ============================================================
rep('<span class="pre-mono">LB</span>\n    <span class="pre-word">Lash Bloom</span>',
    '<span class="pre-mono">EB</span>\n    <span class="pre-word">Emery Beauty Bar</span>')

rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Emery <span class="text-[color:var(--accent-deep)]">Beauty Bar</span></span>')

# ============================================================
# 5) HERO
# ============================================================
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Cape Coral, FL · Esthetician &amp; Waxing Bar" data-en="Cape Coral, FL · Esthetician &amp; Waxing Bar">Cape Coral, FL · Esthetician &amp; Waxing Bar</p>')

rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Enhancing your beauty, reminding you of yours." data-en="Enhancing your beauty, reminding you of yours.">Enhancing your beauty, reminding you of yours.</p>',
    n=2)

rep('''<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>''',
    '''<span data-es="Faciales, depilación y cejas" data-en="Facials, waxing and brows">Facials, waxing and brows</span><br /><span data-es="hechos para revelar tu " data-en="made to reveal your ">made to reveal your </span><span class="text-shine" data-es="brillo" data-en="glow">glow</span>''')

rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Faciales personalizados, depilacion de cuerpo completo, laminado de cejas y tratamientos corporales, cada uno ajustado a tu piel y tu comodidad. Un estudio de una sola esteticista, Asma, con un 5.0 perfecto en 64 reseñas de Google." data-en="Custom facials, full-body waxing, brow lamination and body sculpting treatments, each one tailored to your skin and comfort. A one-esthetician studio led by Asma, with a perfect 5.0 across 64 Google reviews.">Custom facials, full-body waxing, brow lamination and body sculpting treatments, each one tailored to your skin and comfort. A one-esthetician studio led by Asma, with a perfect 5.0 across 64 Google reviews.</p>')

rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 64 reseñas en Google" data-en="5.0 · 64 reviews on Google">5.0 · 64 reviews on Google</span>')

rep('''<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.instagram.com/emerybeautybar/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @emerybeautybar
          </a>''',
    '''<span data-es="Reservar en GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="tel:+17544447046" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            (754) 444-7046
          </a>''')

rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-9.jpg" alt="Customized European facial in progress at Emery Beauty Bar" class="blur-up w-full h-full object-cover" />')

rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">European Facial</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$100 · 60 min" data-en="$100 · 60 min">$100 · 60 min</p>''')

print('hero OK')

open(PATH, 'w', encoding='utf-8').write(h)
print('checkpoint 2 written')

# ============================================================
# 6) STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-count="64">64</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span>')

rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Facials <span class="text-shine">&amp;</span> Waxing</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cuidado facial y corporal" data-en="Skin &amp; body care">Skin &amp; body care</p></div>')

rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">42 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Faciales, cera, cejas y cuerpo" data-en="Facials, wax, brows &amp; body">Facials, wax, brows &amp; body</p></div>')

rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Cape Coral</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">900 SW Pine Island Rd</p></div>')

print('strip OK')

# ============================================================
# 7) MARQUEE (x2 bloques, 4 palabras cada uno x2 repeticiones = 8 asserts)
# ============================================================
MQ = [
    ('Classic Set', 'Facials'),
    ('Hybrid Set', 'Waxing'),
    ('Volume Set', 'Brow Lamination'),
    ('Mega Volume', 'Body Sculpting'),
    ('Bottom Lashes', 'Dermaplaning'),
    ('West Palm Beach, FL', 'Cape Coral, FL'),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    c = h.count(old_span)
    assert c == 4, f'{old_span} expected 4, got {c}'
    h = h.replace(old_span, new_span)

print('marquee OK')

# ============================================================
# 8) LA EXPERIENCIA
# ============================================================
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-11.jpg" alt="Belly facial treatment, moisturizing at Emery Beauty Bar" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-14.jpg" alt="Body sculpting treatment table at Emery Beauty Bar" class="blur-up w-full h-full object-cover" loading="lazy" />')

rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="La experiencia" data-en="The experience">The experience</p>')

rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un estudio" data-en="A studio">A studio</span><br /><span class="text-shine" data-es="hecho para resultados reales" data-en="made for real results">made for real results</span></h2>')

rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Emery Beauty Bar es el estudio de esteticista de Asma en Cape Coral: faciales, depilacion de cuerpo completo, laminado de cejas y tratamientos corporales, cada servicio ajustado a la clienta que esta en la silla." data-en="Emery Beauty Bar is the Cape Coral esthetician studio built around Asma: facials, full-body waxing, brow lamination and body sculpting, each service customized to the client in the chair.">Emery Beauty Bar is the Cape Coral esthetician studio built around Asma: facials, full-body waxing, brow lamination and body sculpting, each service customized to the client in the chair.</p>')

rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="La mision es simple: producir resultados naturales de forma segura mientras se ofrece una experiencia de calidad, con excelencia en cada servicio, resaltando tu belleza y recordandotela." data-en="The mission is simple: safely produce natural-looking results while providing a quality experience, with excellence in every single service, enhancing your beauty and reminding you of yours.">The mission is simple: safely produce natural-looking results while providing a quality experience, with excellence in every single service, enhancing your beauty and reminding you of yours.</p>')

rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="64">64</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')

rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Asma · <span class="text-[color:var(--ink-40)]" data-es="Esteticista principal" data-en="Lead esthetician">Lead esthetician</span></span>')

print('experiencia OK')

open(PATH, 'w', encoding='utf-8').write(h)
print('checkpoint 3 written')

# ============================================================
# 9) EL METODO
# ============================================================
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, paso" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="a paso" data-en="by step">by step</span></h2>')

rep('<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu facial, cera o tratamiento en GlossGenius con precio y duracion claros, y confirmas al instante." data-en="Pick your facial, wax or body treatment on GlossGenius with clear pricing and duration, and confirm instantly.">Pick your facial, wax or body treatment on GlossGenius with clear pricing and duration, and confirm instantly.</p>')

rep('<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Chequeo de piel" data-en="Skin &amp; goals check">Skin &amp; goals check</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Asma revisa tu piel, vello o zona a tratar antes de empezar, para que cada tratamiento se ajuste a ti." data-en="Asma reviews your skin, hair growth or focus area before starting, so every treatment is tailored to you.">Asma reviews your skin, hair growth or focus area before starting, so every treatment is tailored to you.</p>')

rep('<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Tu tratamiento" data-en="Your treatment">Your treatment</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas y relajas: desde un facial express de 30 min hasta una cera completa o sculpting, con mano suave y detallista." data-en="Lie back and relax: from a 30-min express facial to a full body wax or sculpting session, done with a gentle, detailed hand.">Lie back and relax: from a 30-min express facial to a full body wax or sculpting session, done with a gentle, detailed hand.</p>')

rep('<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Brillo y cuidado posterior" data-en="Glow &amp; aftercare">Glow &amp; aftercare</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con la piel visiblemente mas suave y calmada, y recomendaciones claras para que el resultado dure mas." data-en="You leave with visibly smoother, calmer skin and clear aftercare tips so the results last.">You leave with visibly smoother, calmer skin and clear aftercare tips so the results last.</p>')

print('metodo OK')

open(PATH, 'w', encoding='utf-8').write(h)
print('checkpoint 4 written')

# ============================================================
# 10) SERVICIOS: header + 4 cards destacadas (regex block replace)
# ============================================================
rep('data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Servicios" data-en="Services">Services</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="tratamiento" data-en="treatment">treatment</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Emery Beauty Bar en GlossGenius. Reserva con confirmacion inmediata." data-en="Prices and durations as published by Emery Beauty Bar on GlossGenius. Booking confirms instantly.">Prices and durations as published by Emery Beauty Bar on GlossGenius. Booking confirms instantly.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, 'no se encontro el grid de servicios'

BOOK = 'https://emerybeautybar.glossgenius.com/'
new_grid = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Facial insignia" data-en="Signature facial">Signature facial</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Facial Europeo de 60 min" data-en="60 Min Customized European Facial">60 Min Customized European Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una hora completa ajustada a tu tipo de piel: limpieza, exfoliacion y un masaje relajante de verdad." data-en="A full hour tailored to your skin type: cleansing, exfoliation and a genuinely relaxing massage.">A full hour tailored to your skin type: cleansing, exfoliation and a genuinely relaxing massage.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">60 min</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(168,82,74,0.4); box-shadow: 0 18px 50px rgba(58,40,32,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cera Brasileña (Mujer)" data-en="Brazilian Wax (Female)">Brazilian Wax (Female)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Depilacion brasileña completa con tecnica suave y detallista, en un estudio privado y comodo." data-en="Full Brazilian waxing done with a gentle, detailed technique in a private, comfortable studio setting.">Full Brazilian waxing done with a gentle, detailed technique in a private, comfortable studio setting.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">35 min</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas" data-en="Brows">Brows</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Laminado de Cejas" data-en="Brow Lamination">Brow Lamination</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cejas cepilladas, fijadas y tenidas en una forma mas llena y definida que dura semanas." data-en="Brows brushed, set and tinted into a fuller, more defined shape that holds for weeks.">Brows brushed, set and tinted into a fuller, more defined shape that holds for weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">60 min</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cuerpo" data-en="Body">Body</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tratamiento de Body Sculpting" data-en="Body Sculpting Treatment">Body Sculpting Treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un tratamiento corporal dirigido a contornear y tonificar zonas especificas en una sesion completa de 90 minutos." data-en="A targeted body treatment designed to contour and tone problem areas over a full 90-minute session.">A targeted body treatment designed to contour and tone problem areas over a full 90-minute session.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$150</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">90 min</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_grid + h[m.end():]
print('cards destacadas OK')

# MENU COMPLETO, agrupado por categoria, todo visible (sin acordeones)
def row(name_en, name_es, price):
    return (f'<div class="flex justify-between py-2 border-b border-[color:var(--accent-ghost)]">'
            f'<span data-es="{name_es}" data-en="{name_en}">{name_en}</span>'
            f'<span class="text-[color:var(--accent-deep)] font-medium">${price}</span></div>')

BROWS = [
    ('Eyebrow Wax', 'Cera de cejas', '20'),
    ('Hybrid Brow Stain &amp; Wax', 'Tinte y cera hibrida de cejas', '40'),
    ('Brow Lamination', 'Laminado de cejas', '85'),
    ('Brow Lamination Maintenance', 'Mantenimiento de laminado', '50'),
]
FACIALS = [
    ('60 min Customized European Facial', 'Facial europeo personalizado 60 min', '100'),
    ('30 min Customized European Facial', 'Facial europeo personalizado 30 min', '55'),
    ('Dermaplaning', 'Dermaplaning', '50'),
    ('Chemical Peel', 'Peeling quimico', '65'),
    ('Microdermabrasion', 'Microdermabrasion', '30'),
    ('LED Light Therapy', 'Terapia de luz LED', '15'),
    ('High Frequency', 'Alta frecuencia', '15'),
    ('Radio Frequency (face)', 'Radiofrecuencia facial', '20'),
    ('Extractions (add-on)', 'Extracciones (adicional)', '25'),
    ('Hydro Jelly Mask', 'Mascarilla hydro jelly', '10'),
]
BODY = [
    ('Belly Facial', 'Facial de vientre', '100'),
    ('Back Treatment', 'Tratamiento de espalda', '100'),
    ('Body Sculpting Treatment', 'Tratamiento de body sculpting', '150'),
    ('Sauna Detox', 'Sauna detox', '35'),
    ('Intimate Lightening', 'Aclarado intimo', '55'),
    ('Vajacial', 'Vajacial', '80'),
    ('Vajazzle (add on)', 'Vajazzle (adicional)', '5'),
]
WAXING = [
    ('Brazilian Wax (Female)', 'Cera brasileña (mujer)', '60'),
    ('Half Leg Wax', 'Cera media pierna', '50'),
    ('Full Leg Wax', 'Cera pierna completa', '85'),
    ('Bikini Wax', 'Cera bikini', '40'),
    ('Underarm Wax', 'Cera de axilas', '20'),
    ('Full Arm Wax', 'Cera brazo completo', '75'),
    ('Half Arm Wax', 'Cera medio brazo', '50'),
    ('Upper Thigh Wax', 'Cera muslo superior', '45'),
    ('Full Face Wax', 'Cera rostro completo', '70'),
    ('Full Back Wax', 'Cera espalda completa', '70'),
    ('Full Chest Wax', 'Cera pecho completo', '60'),
    ('Stomach Wax', 'Cera de abdomen', '50'),
    ('Butt Wax', 'Cera de gluteos', '45'),
    ('Upper Lip Wax', 'Cera de labio superior', '10'),
    ('Chin Wax', 'Cera de menton', '10'),
    ('Cheek Wax', 'Cera de mejillas', '18'),
    ('Sideburn Wax', 'Cera de patillas', '10'),
    ('Neck Wax', 'Cera de cuello', '20'),
    ('Ear Wax', 'Cera de orejas', '15'),
    ('Nose Wax', 'Cera de nariz', '15'),
    ('Happy Trail Strip', 'Franja happy trail', '10'),
]
assert len(BROWS) == 4 and len(FACIALS) == 10 and len(BODY) == 7 and len(WAXING) == 21

menu_block = f'''
      <!-- MENU COMPLETO, agrupado por categoria, todo visible (sin acordeones) -->
      <div class="mt-16 grid lg:grid-cols-2 gap-6">
        <div class="glass rounded-3xl p-7 sm:p-8 reveal">
          <h3 class="font-display text-xl mb-1" data-es="Faciales y cuidado de la piel" data-en="Facials &amp; Skin">Facials &amp; Skin</h3>
          <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="10 servicios" data-en="10 services">10 services</p>
          <div class="grid sm:grid-cols-2 gap-x-6 text-sm">
            {"".join(row(*s) for s in FACIALS)}
          </div>
        </div>

        <div class="glass rounded-3xl p-7 sm:p-8 reveal" style="transition-delay:80ms">
          <h3 class="font-display text-xl mb-1" data-es="Cejas" data-en="Brows">Brows</h3>
          <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="4 servicios" data-en="4 services">4 services</p>
          <div class="grid sm:grid-cols-2 gap-x-6 text-sm">
            {"".join(row(*s) for s in BROWS)}
          </div>
          <h3 class="font-display text-xl mb-1 mt-8" data-es="Cuerpo" data-en="Body Treatments">Body Treatments</h3>
          <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="7 servicios" data-en="7 services">7 services</p>
          <div class="grid sm:grid-cols-2 gap-x-6 text-sm">
            {"".join(row(*s) for s in BODY)}
          </div>
        </div>

        <div class="glass rounded-3xl p-7 sm:p-8 reveal lg:col-span-2" style="transition-delay:140ms">
          <h3 class="font-display text-xl mb-1" data-es="Depilacion" data-en="Waxing">Waxing</h3>
          <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="21 servicios, desde $10" data-en="21 services, from $10">21 services, from $10</p>
          <div class="grid sm:grid-cols-3 gap-x-6 text-sm">
            {"".join(row(*s) for s in WAXING)}
          </div>
        </div>
      </div>
'''

# nota de servicios
note_re = re.compile(r'<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">.*?</p>\s*(?=</div>\s*</section>\s*<!-- GALERIA)', flags=re.S)
m2 = note_re.search(h)
assert m2, 'no se encontro la nota de servicios'
new_note = menu_block + '\n      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="42 servicios en total: faciales, cera, cejas y cuerpo, todos disponibles para reservar en GlossGenius." data-en="42 services in total: facials, waxing, brows and body treatments, all bookable on GlossGenius.">42 services in total: facials, waxing, brows and body treatments, all bookable on GlossGenius.</span></p>\n'
h = h[:m2.start()] + new_note + h[m2.end():]
print('nota servicios OK')

open(PATH, 'w', encoding='utf-8').write(h)
print('checkpoint 5 written')

# ============================================================
# 11) GALERIA
# ============================================================
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span></h2>')

gallery_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
mg = gallery_re.search(h)
assert mg, 'no se encontro el grid de galeria'

new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Depilacion de cuerpo completo" data-en="Full-body waxing">Full-body waxing</span><img src="assets/raw/bk-15.jpg" alt="Warm wax application during a waxing service at Emery Beauty Bar" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Laminado de cejas terminado" data-en="Brow lamination finish">Brow lamination finish</span><img src="assets/raw/bk-6.jpg" alt="Finished brow lamination result at Emery Beauty Bar" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Definicion natural de cejas" data-en="Natural brow definition">Natural brow definition</span><img src="assets/raw/bk-7.jpg" alt="Natural brow shaping result at Emery Beauty Bar" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Brillo del facial europeo" data-en="European facial glow">European facial glow</span><img src="assets/raw/bk-10.jpg" alt="Client relaxing during a European facial at Emery Beauty Bar" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Herramientas del estudio" data-en="Studio tools, ready">Studio tools, ready</span><img src="assets/raw/bk-8.jpg" alt="Clean brow spoolie wands ready for treatments at Emery Beauty Bar" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Cuidado facial personalizado" data-en="Customized facial care">Customized facial care</span><img src="assets/raw/bk-9.jpg" alt="Customized European facial treatment at Emery Beauty Bar" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:mg.start()] + new_gallery + h[mg.end():]
print('galeria OK')

open(PATH, 'w', encoding='utf-8').write(h)
print('checkpoint 6 written')

# ============================================================
# 12) OPINIONES (reviews reales, Google via Birdeye)
# ============================================================
rep('data-es="Opiniones" data-en="Reviews">Opiniones</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    'data-es="Opiniones" data-en="Reviews">Reviews</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 64 reseñas verificadas en Google" data-en="5.0 out of 5 · 64 verified reviews on Google">5.0 out of 5 · 64 verified reviews on Google</span></p>')

rep('<div class="grid sm:grid-cols-3 gap-5 items-stretch">',
    '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">')

rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I had gotten a service done with Asma which required me to be vulnerable with my body and she was super welcoming and made me feel comfortable, it almost felt like I had known her for years!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Seline Shipman</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Asma is so sweet and very professional. My facial was absolutely amazing! She pays great attention to detail and really listens to your skincare needs."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Haley Hernandez</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I had such a great experience at Emery Beauty Bar! Asma did an amazing job on my brows, they look perfect. The studio is clean, welcoming, and professional."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rosario Rivas</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:330ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Highly recommend Asma! Her work is awesome and she has a great personality. I visited her for a full eyebrow lamination service and she beyond met my expectations."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Barbie Smith</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>''')

rep('<a href="https://emerybeautybar.glossgenius.com/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://g.co/kgs/bTknvM" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver las reseñas en Google" data-en="See reviews on Google">See reviews on Google</a>')

print('opiniones OK')

open(PATH, 'w', encoding='utf-8').write(h)
print('checkpoint 7 written')

# ============================================================
# 13) UBICACION
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Cape Coral</span></h2>')

rep('''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(168,82,74,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">900 SW Pine Island Rd Suite 209, Cape Coral, FL 33993</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light mt-1"><span data-es="Teléfono" data-en="Phone">Phone</span>: <a class="text-[color:var(--accent-deep)]" href="tel:+17544447046">(754) 444-7046</a></p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(168,82,74,0.4)]" href="https://www.google.com/maps?q=900+SW+Pine+Island+Rd+Suite+209,+Cape+Coral,+FL+33993" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>''')

rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(168,82,74,0.4)]" href="https://emerybeautybar.glossgenius.com/" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía GlossGenius: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via GlossGenius: pick the service, day and time, and the confirmation is instant.">By appointment via GlossGenius: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(168,82,74,0.4)]" href="https://emerybeautybar.glossgenius.com/" target="_blank" rel="noopener" data-es="Reservar en GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>''')

rep('''<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>''',
    '''<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los ultimos faciales, ceras y cejas de Asma y escribe por DM cualquier duda antes de tu cita." data-en="See Asma's latest facials, waxing and brow work and DM any questions before your appointment.">See Asma's latest facials, waxing and brow work and DM any questions before your appointment.</p>''')

rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Map: Emery Beauty Bar, 900 SW Pine Island Rd Suite 209, Cape Coral FL"\n          src="https://www.google.com/maps?q=900+SW+Pine+Island+Rd+Suite+209,+Cape+Coral,+FL+33993&output=embed"')

print('ubicacion OK')

# ============================================================
# 14) CTA FINAL
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mejor piel" data-en="Your best skin">Your best skin</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>')

rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu facial, cera, laminado de cejas o tratamiento corporal, al precio y duracion que Emery Beauty Bar publica en GlossGenius." data-en="Book online in seconds: your facial, wax, brow lamination or body treatment, at the price and duration Emery Beauty Bar publishes on GlossGenius.">Book online in seconds: your facial, wax, brow lamination or body treatment, at the price and duration Emery Beauty Bar publishes on GlossGenius.</p>')

rep('<a href="https://emerybeautybar.glossgenius.com/" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="https://www.instagram.com/emerybeautybar/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="https://emerybeautybar.glossgenius.com/" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>\n        <a href="https://www.instagram.com/emerybeautybar/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')

print('cta final OK')

open(PATH, 'w', encoding='utf-8').write(h)
print('checkpoint 8 written')

# ============================================================
# 15) FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Emery Beauty</span>')

rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Emery Beauty Bar</span>')

rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Esthetician bar en Cape Coral, FL. Atencion con cita previa." data-en="Esthetician bar in Cape Coral, FL. By appointment only.">Esthetician bar in Cape Coral, FL. By appointment only.</p>')

rep('<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>\n        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>\n        <p><a href="https://emerybeautybar.glossgenius.com/" target="_blank" rel="noopener" class="hover:text-[#f0c9a8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>\n        <p>900 SW Pine Island Rd Suite 209, Cape Coral, FL 33993</p>\n        <p><a href="tel:+17544447046" class="hover:text-[#f0c9a8]">(754) 444-7046</a></p>\n        <p><a href="https://emerybeautybar.glossgenius.com/" target="_blank" rel="noopener" class="hover:text-[#f0c9a8]" data-es="Reservas online · GlossGenius" data-en="Online booking · GlossGenius">Online booking · GlossGenius</a></p>')

rep('<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>',
    '<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>')

rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Emery Beauty Bar.</p>')

rep('<a href="https://emerybeautybar.glossgenius.com/" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://emerybeautybar.glossgenius.com/" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">')

print('footer OK')

open(PATH, 'w', encoding='utf-8').write(h)
print('checkpoint 9 written - build complete')
