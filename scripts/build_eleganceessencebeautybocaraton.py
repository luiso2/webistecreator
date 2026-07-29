import re, os, shutil

SLUG = "elegance-essence-beauty-boca-raton"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, 1)


# ============ 1. PROTEGER BADGE MERKTOP ============
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ============ 2. PALETA: rosa magenta (lashbloom) -> rose gold / champagne boutique ============
PALETTE = [
    ("#1c0f16", "#1c140d"),
    ("#1f0f18", "#1f150e"),
    ("#2a1722", "#2a1f16"),
    ("#33222c", "#362a20"),
    ("#5c2140", "#5c3d20"),
    ("#5f2c48", "#5c3a1e"),
    ("#7d3457", "#7a4a22"),
    ("#8a5573", "#8a6234"),
    ("#a04a72", "#b5623f"),
    ("#b25a85", "#c17a49"),
    ("#c47a9c", "#d3966a"),
    ("#c9789f", "#d99a6a"),
    ("#d3a2bc", "#dbb37e"),
    ("#d9a8c2", "#ddb98c"),
    ("#dc9dbe", "#dba86e"),
    ("#e5c1d4", "#e8cda8"),
    ("#efd0e0", "#ecdcb8"),
    ("#f0bed7", "#f0d2a3"),
    ("#f2cfe0", "#f3dfbb"),
    ("#f2d5e3", "#f3ddc2"),
    ("#f3e0ea", "#f4e2cd"),
    ("#f6f1ea", "#f8f0e6"),
    ("#f8dfeb", "#faeed9"),
    ("#faf2f6", "#fbf1e9"),
    ("#fbeff5", "#faf1e0"),
    ("#fbf3f8", "#fbf3ec"),
]
for old, new in PALETTE:
    assert old in h, "MISSING HEX " + old
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(125,52,87", "rgba(125,80,52"),
    ("rgba(160,74,114", "rgba(181,98,63"),
    ("rgba(185,138,128", "rgba(190,155,110"),
    ("rgba(233,205,186", "rgba(235,208,165"),
    ("rgba(240,190,215", "rgba(240,210,163"),
    ("rgba(250,242,246", "rgba(251,241,233"),
    ("rgba(253,246,250", "rgba(253,247,240"),
    ("rgba(51,34,44", "rgba(54,42,32"),
    ("rgba(70,25,50", "rgba(70,45,25"),
]
for old, new in RGBA_PAIRS:
    assert old in h, "MISSING RGBA " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ============ 3. GLOBALES: Booksy URL, IG URL/handle ============
BOOKSY = "https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton"
assert 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach' in h
h = h.replace('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BOOKSY)
assert 'https://www.instagram.com/_lashbloom/' in h
h = h.replace('https://www.instagram.com/_lashbloom/', 'https://www.instagram.com/elegance_essence_corp/')
assert '@_lashbloom' in h
h = h.replace('@_lashbloom', '@elegance_essence_corp')
print("GLOBALES done")

# ============ 4. HEAD: title, meta, og, favicon, JSON-LD ============
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Elegance Essence Beauty · Nail Salon in Boca Raton, FL | 4.8 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Elegance Essence Beauty, Boca Raton FL: builder gel manicures, acrylics, pedicures and nail art with Camila, rated 4.8 across 42 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Elegance Essence Beauty · Nail Salon in Boca Raton, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Builder gel, acrylics, pedicures and nail art with Camila. 4.8 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-1.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Elegance Essence Beauty",
    "description": "Nail salon in Boca Raton, FL: builder gel manicures, acrylic full sets, pedicures and nail art with Camila.",
    "address": { "@type": "PostalAddress", "streetAddress": "2290 NW 2nd Ave, Unit 5", "addressLocality": "Boca Raton", "addressRegion": "FL", "postalCode": "33431", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton", "https://www.instagram.com/elegance_essence_corp/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "42", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder Gel Manicure + Solid Color" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Full Set + Design" } },
      { "@type": "Offer", "price": "55", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure + Gel Polish" } },
      { "@type": "Offer", "price": "15", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Nail Soak Off / Removal" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ============ 5. IDIOMA: negocio en ingles -> default en (ya es el default del esqueleto) ============
# (lang="en" ya es el default de light-v2, no se cambia el html lang ni el applyLang)

# ============ 6. PRELOADER + NAV ============
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">EE</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Elegance Essence</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,98,63,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Elegance Essence Beauty logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,98,63,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Elegance <span class="text-[color:var(--accent-deep)]">Essence</span></span>')
print("NAV done")

# ============ 7. HERO ============
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Boca Raton, FL · Nail Salon" data-en="Boca Raton, FL · Nail Salon">Boca Raton, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Cada set, hecho a tu manera." data-en="Every set, made your way.">Every set, made your way.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Manicura, acrilico y" data-en="Builder gel, acrylics">Builder gel, acrylics</span><br /><span data-es="pedicura, hechos para " data-en="and nail art, made to ">and nail art, made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Builder gel, French, acrilico y disenos hechos a mano, ademas de pedicura y removal. Camila atiende con calma y precision en un salon pequeno y limpio en Boca Raton, con 4.8 estrellas en 42 resenas de Booksy." data-en="Builder gel, French, acrylics and hand-painted nail art, plus pedicures and removal. Camila works with care and precision in a small, clean boutique salon in Boca Raton, rated 4.8 across 42 Booksy reviews.">Builder gel, French, acrylics and hand-painted nail art, plus pedicures and removal. Camila works with care and precision in a small, clean boutique salon in Boca Raton, rated 4.8 across 42 Booksy reviews.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.8 · 42 reseñas en Booksy" data-en="4.8 · 42 reviews on Booksy">4.8 · 42 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Diseno de unas azul degradado con detalles blancos en Elegance Essence Beauty" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg" data-es="Builder Gel + Design" data-en="Builder Gel + Design">Builder Gel + Design</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$100 · con Camila" data-en="$100 · with Camila">$100 · with Camila</p>')
print("HERO done")

# ============ 8. STRIP DE CONFIANZA ============
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="42">42</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Acrylic</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicura · Pedicura" data-en="Manicures · Pedicures">Manicures · Pedicures</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Camila</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Unas, pestanas, cejas y faciales" data-en="Nails, lashes, brows &amp; facials">Nails, lashes, brows &amp; facials</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Boca Raton</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">NW 2nd Ave</p></div>')
print("STRIP done")

# ============ 9. MARQUEE (x2, 4 apariciones cada palabra) ============
for old, new in [
    ('Classic Set', 'Builder Gel'),
    ('Hybrid Set', 'Acrylic Full Set'),
    ('Volume Set', 'Nail Art'),
    ('Mega Volume', 'Pedicure'),
    ('Bottom Lashes', 'Gel Polish'),
    ('West Palm Beach, FL', 'Boca Raton, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ============ 10. LA EXPERIENCIA ============
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Interior del salon Elegance Essence Beauty con luz natural" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Estacion de trabajo dentro del salon Elegance Essence Beauty" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un salon boutique" data-en="A boutique salon">A boutique salon</span><br /><span class="text-shine" data-es="pensado para durar" data-en="built to last">built to last</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Elegance Essence Beauty es un salon pequeno y limpio en Boca Raton. Camila hace unas, pestanas, cejas y faciales con builder gel, acrilico y disenos a mano, tomandose el tiempo que cada clienta necesita." data-en="Elegance Essence Beauty is a small, clean boutique salon in Boca Raton. Camila handles nails, lashes, brows and facials with builder gel, acrylics and hand-painted designs, taking the time each client needs.">Elegance Essence Beauty is a small, clean boutique salon in Boca Raton. Camila handles nails, lashes, brows and facials with builder gel, acrylics and hand-painted designs, taking the time each client needs.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 4.8 de 5 en 42 resenas verificadas en Booksy, con clientas que repiten porque Camila es detallista, dulce y se toma su tiempo con cada set." data-en="The result: a 4.8 out of 5 across 42 verified Booksy reviews, with clients who come back because Camila is detailed, sweet and takes her time with every set.">The result: a 4.8 out of 5 across 42 verified Booksy reviews, with clients who come back because Camila is detailed, sweet and takes her time with every set.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.8" data-decimals="1">4.8</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="42">42</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,98,63,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Elegance Essence Beauty logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(181,98,63,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Camila · <span class="text-[color:var(--ink-40)]" data-es="Unas, pestanas y cejas" data-en="Nails, lashes &amp; brows">Nails, lashes &amp; brows</span></span>')
print("EXPERIENCIA done")

# ============ 11. EL METODO ============
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, un set" data-en="Your visit, one set">Your visit, one set</span> <span class="text-shine" data-es="hecho a mano" data-en="made by hand">made by hand</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio claro, y confirmas al instante." data-en="Pick your service on Booksy with a clear price, and confirm instantly.">Pick your service on Booksy with a clear price, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta y diseno" data-en="Consult &amp; design">Consult &amp; design</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Largo, forma y color: Camila conversa contigo antes de empezar para que el diseno sea el tuyo." data-en="Length, shape and color: Camila talks it through with you before starting, so the design is really yours.">Length, shape and color: Camila talks it through with you before starting, so the design is really yours.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Preparacion" data-en="Prep work">Prep work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, cuticulas y base: la parte que no se ve pero hace que el set dure semanas sin levantarse." data-en="Filing, cuticles and base: the part you do not see, but the reason the set lasts weeks without lifting.">Filing, cuticles and base: the part you do not see, but the reason the set lasts weeks without lifting.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Acabado" data-en="Finish &amp; art">Finish &amp; art</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="French, color solido o nail art a mano, mas aceite de cuticulas para que salgas lista para lucirlas." data-en="French, solid color or hand-painted nail art, plus cuticle oil so you leave ready to show them off.">French, solid color or hand-painted nail art, plus cuticle oil so you leave ready to show them off.</p>''')
print("METODO done")

# ============ 12. SERVICIOS ============
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios publicados por Elegance Essence Beauty en Booksy. Reserva con confirmación inmediata." data-en="Prices as published by Elegance Essence Beauty on Booksy. Booking confirms instantly.">Prices as published by Elegance Essence Beauty on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_HIGHLIGHTS = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicura" data-en="Manicure">Manicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Builder Gel + Solid Color</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura en builder gel sobre una natural, con color solido a tu eleccion. Version con French por $90." data-en="Builder gel manicure on the natural nail, with solid color of your choice. French version available for $90.">Builder gel manicure on the natural nail, with solid color of your choice. French version available for $90.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Con Camila" data-en="With Camila">With Camila</p></div>
            <a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(181,98,63,0.4); box-shadow: 0 18px 50px rgba(54,42,32,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salon" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic Full Set + Design</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo en acrilico con diseno a mano. Version en color solido por $70 y con French por $90." data-en="Full acrylic set with hand-painted design. Solid color version available for $70 and French for $90.">Full acrylic set with hand-painted design. Solid color version available for $70 and French for $90.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Con Camila" data-en="With Camila">With Camila</p></div>
            <a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies" data-en="Toes">Toes</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Pedicure + Gel Polish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura completa con esmalte en gel de larga duracion. Version regular por $40, 55min." data-en="Full pedicure with long-lasting gel polish. Regular version available for $40, 55min.">Full pedicure with long-lasting gel polish. Regular version available for $40, 55min.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$55</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 10min</p></div>
            <a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Mantenimiento" data-en="Upkeep">Upkeep</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Nail Soak Off / Removal" data-en="Nail Soak Off / Removal">Nail Soak Off / Removal</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Retiro seguro de gel o acrilico antes de tu proximo set. Fill de acrilico disponible por $75." data-en="Safe removal of gel or acrylic before your next set. Acrylic fill available for $75.">Safe removal of gel or acrylic before your next set. Acrylic fill available for $75.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$15</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">20min</p></div>
            <a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_HIGHLIGHTS + h[services_grid.end():]

# Nota + menu completo agrupado por categoria (sin acordeon, todo visible)
rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '''<div class="reveal grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-8">
        <div class="glass rounded-3xl p-6">
          <p class="font-display text-lg mb-4" data-es="Manicura" data-en="Manicures">Manicures</p>
          <div class="space-y-2.5 text-sm">
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]">Builder Gel + Solid Color</span><span class="font-medium">$70</span></div>
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]">Builder Gel + French</span><span class="font-medium">$90</span></div>
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]">Builder Gel + Design</span><span class="font-medium">$100</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-6">
          <p class="font-display text-lg mb-4" data-es="Acrilico" data-en="Acrylics">Acrylics</p>
          <div class="space-y-2.5 text-sm">
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]" data-es="Set Completo (color solido)" data-en="Full Set (solid color)">Full Set (solid color)</span><span class="font-medium">$70</span></div>
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]" data-es="Set Completo + French" data-en="Full Set + French">Full Set + French</span><span class="font-medium">$90</span></div>
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]" data-es="Relleno" data-en="Fill">Fill</span><span class="font-medium">$75</span></div>
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]" data-es="Acrilico Dedo Gordo" data-en="Big Toe Acrylic">Big Toe Acrylic</span><span class="font-medium">$20</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-6">
          <p class="font-display text-lg mb-4" data-es="Pedicura" data-en="Pedicures">Pedicures</p>
          <div class="space-y-2.5 text-sm">
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]" data-es="Pedicura Regular" data-en="Regular Pedicure">Regular Pedicure</span><span class="font-medium">$40</span></div>
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]" data-es="Retiro de Acrilico (pies)" data-en="Pedi Acrylic Removal">Pedi Acrylic Removal</span><span class="font-medium">$10</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-6">
          <p class="font-display text-lg mb-4" data-es="Cabello con Mirsania" data-en="Hair with Mirsania">Hair with Mirsania</p>
          <div class="space-y-2.5 text-sm">
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]" data-es="Corte de Cabello" data-en="Haircut">Haircut</span><span class="font-medium">$45</span></div>
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]">Balayage</span><span class="font-medium">$100</span></div>
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]" data-es="Tratamiento de Keratina" data-en="Keratin Treatment">Keratin Treatment</span><span class="font-medium">$150</span></div>
            <div class="flex justify-between gap-3"><span class="text-[color:var(--ink-60)]" data-es="y mas servicios" data-en="and more">and more</span><span class="text-[color:var(--ink-40)]" data-es="ver Booksy" data-en="see Booksy">see Booksy</span></div>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menu completo de 24 servicios, con precios y duraciones exactas, disponible en Booksy." data-en="Full 24-service menu, with exact prices and durations, available on Booksy.">Full 24-service menu, with exact prices and durations, available on Booksy.</span></p>''')
print("SERVICIOS done")

# ============ 13. GALERIA ============
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail art">nail art</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Brillo cafe con dorado" data-en="Brown gold shimmer">Brown gold shimmer</span><img src="assets/raw/bk-16.jpg" alt="Unas almendra con esmalte cafe brillante y joyeria dorada en Elegance Essence Beauty" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Nude clasico" data-en="Classic nude">Classic nude</span><img src="assets/raw/bk-3.jpg" alt="Manicura nude con puntas blancas en Elegance Essence Beauty" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="French clasico" data-en="Classic French">Classic French</span><img src="assets/raw/bk-4.jpg" alt="Manicura French blanca clasica en Elegance Essence Beauty" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Lunares hechos a mano" data-en="Hand-painted dots">Hand-painted dots</span><img src="assets/raw/bk-5.jpg" alt="Diseno de lunares negros sobre base rosa brillante en Elegance Essence Beauty" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Pedicura con brillo" data-en="Pedicure with sparkle">Pedicure with sparkle</span><img src="assets/raw/bk-7.jpg" alt="Pedicura rosa con puntas blancas y strass en Elegance Essence Beauty" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ============ 14. OPINIONES (reales, con autor) ============
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.8 de 5 · 42 reseñas verificadas en Booksy" data-en="4.8 out of 5 · 42 verified reviews on Booksy">4.8 out of 5 · 42 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"It was my first time visiting, and I had a great experience! The service was excellent, and the overall experience went way beyond my expectations. I'll definitely be back!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karim</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Camila did an amazing job! She took her time and was knowledgeable in nail care! I definitely will be coming back!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Karen J…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The place looks so nice and Camila is the sweetest girl ever! She really takes her time and I'm beyond happy with how my nails came out 😊"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">veronica v…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:330ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Absolutely obsessed with my nails every single time ✨💅🏼 Camila is beyond talented, so sweet, professional, and truly pays attention to every..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Marcela</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:440ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Highly recommended👍🏼. Camila is very detailed, the salon is super clean, you will love her work and the salon atmosphere👌..."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Maria Alejandra</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 42 reseñas en Booksy" data-en="Read all 42 reviews on Booksy">Read all 42 reviews on Booksy</a>')
print("OPINIONES done")

# ============ 15. UBICACION ============
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Boca Raton</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">2290 NW 2nd Ave, Unit 5, Boca Raton, FL 33431</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=2290+NW+2nd+Ave,+Unit+5,+Boca+Raton,+FL+33431"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,98,63,0.4)]" href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(181,98,63,0.4)]" href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los disenos mas recientes de Camila y escribe por DM cualquier duda antes de tu cita." data-en="See Camila\'s latest designs and DM any questions before your appointment.">See Camila\'s latest designs and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Elegance Essence Beauty, 2290 NW 2nd Ave, Boca Raton FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=2290+NW+2nd+Ave,+Unit+5,+Boca+Raton,+FL+33431&output=embed"')
print("UBICACION done")

# ============ 16. CTA FINAL ============
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Cada set, hecho a tu manera." data-en="Every set, made your way.">Every set, made your way.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu builder gel, tu acrilico o la pedicura que ya te toca." data-en="Book online in seconds: your builder gel, your acrylic set, or the pedicure you are due for.">Book online in seconds: your builder gel, your acrylic set, or the pedicure you are due for.</p>')
rep('<a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# ============ 17. FOOTER ============
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Elegance Essence</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,210,163,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Elegance Essence Beauty logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,210,163,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Elegance Essence Beauty</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Boca Raton, FL. Atencion con cita previa." data-en="Nail salon in Boca Raton, FL. By appointment only.">Nail salon in Boca Raton, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>2290 NW 2nd Ave, Unit 5, Boca Raton, FL 33431</p>')
rep('<p><a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="hover:text-[#f0d2a3]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://booksy.com/en-us/1176109_elegance-essence-beauty_nail-salon_15945_boca-raton" target="_blank" rel="noopener" class="hover:text-[#f0d2a3]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/elegance_essence_corp/" target="_blank" rel="noopener" class="hover:text-[#f0d2a3]">Instagram · @elegance_essence_corp</a></p>',
    '<p><a href="https://www.instagram.com/elegance_essence_corp/" target="_blank" rel="noopener" class="hover:text-[#f0d2a3]">Instagram · @elegance_essence_corp</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Elegance Essence Beauty.</p>')
print("FOOTER done")

print("ALL DONE")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h))
