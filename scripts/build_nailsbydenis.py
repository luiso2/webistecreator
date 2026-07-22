import re, os, shutil, colorsys

SLUG = "nailsbydenis"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:120]
    h = h.replace(a, b, n)


BOOKSY = "https://booksy.com/en-us/1716708_nailsnailsbydenis_nail-salon_15761_tampa"
IG_URL = "https://www.instagram.com/nailsnailsbydenis/"
IG_HANDLE = "@nailsnailsbydenis"

# ============ GLOBALS: Booksy URL, IG url/handle ============
old_booksy = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
assert h.count(old_booksy) > 5
h = h.replace(old_booksy, BOOKSY)
old_ig_url = 'https://www.instagram.com/_lashbloom/'
assert h.count(old_ig_url) > 1
h = h.replace(old_ig_url, IG_URL)
old_ig_handle = '@_lashbloom'
assert h.count(old_ig_handle) > 1
h = h.replace(old_ig_handle, IG_HANDLE)
print("GLOBALS done")

# ============ HEAD ============
rep('<meta name="theme-color" content="#f6f1ea" />', '<meta name="theme-color" content="#f6f1ea" />')
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Nails by Denis · Nail Salon in Tampa, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Nails by Denis, Tampa FL: acrylic, builder gel, polygel and gel manicures with a perfect 5.0 across 52 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Nails by Denis · Nail Salon in Tampa, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Builder gel, acrylic and polygel sets. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />', '<meta property="og:image" content="assets/raw/bk-3.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nails by Denis",
    "description": "Nail salon in Tampa, FL: acrylic, builder gel, polygel and gel manicures and pedicures.",
    "address": { "@type": "PostalAddress", "streetAddress": "1815 W Sligh Ave, Suite B", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33604", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1716708_nailsnailsbydenis_nail-salon_15761_tampa", "https://www.instagram.com/nailsnailsbydenis/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "52", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "24", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Regular" } },
      { "@type": "Offer", "price": "33", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Manicure Gel" } },
      { "@type": "Offer", "price": "48", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Builder Gel" } },
      { "@type": "Offer", "price": "110", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Combo Deluxe" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)
print("HEAD done")

# ============ PRELOADER + NAV ============
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">ND</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Nails by Denis</span>')

rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Nails by Denis logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails <span class="text-[color:var(--accent-deep)]">by Denis</span></span>')
print("NAV done")

# ============ HERO ============
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tampa, FL · Salon de unas" data-en="Tampa, FL · Nail Salon">Tampa, FL · Nail Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
    'data-es="Unas hermosas, una cita a la vez." data-en="Beautiful nails, one appointment at a time.">Beautiful nails, one appointment at a time.</p>\n        <h1')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Acrilico, builder gel" data-en="Acrylic, builder gel">Acrylic, builder gel</span><br /><span data-es="y polygel, hechos para " data-en="and polygel, made to ">and polygel, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Builder gel, acrilico, polygel y apres, mas manicura y pedicura en gel, todo hecho por Denise en su propio suite sobre W Sligh Ave, Tampa." data-en="Builder gel, acrylic, polygel and apres sets, plus gel manicures and pedicures, all done by Denise in her own suite on W Sligh Ave, Tampa.">Builder gel, acrylic, polygel and apres sets, plus gel manicures and pedicures, all done by Denise in her own suite on W Sligh Ave, Tampa.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>
''', '''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 52 reseñas en Booksy" data-en="5.0 · 52 reviews on Booksy">5.0 · 52 reviews on Booksy</span>
        </div>
''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-3.jpg" alt="Manicura con puntas francesas azul marino y lunares blancos" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Volume Full Set</p>', '<p class="font-display text-lg">Builder Gel</p>')
rep('data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="$48 · 1h" data-en="$48 · 1h">$48 · 1h</p>')
print("HERO done")

# ============ STRIP ============
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="52">52</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Acrylic <span class="text-shine">&amp;</span> Gel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Builder gel · Polygel" data-en="Builder gel · Polygel">Builder gel · Polygel</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">1:1</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Una sola artista, atencion personal" data-en="One artist, personal care">One artist, personal care</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W Sligh Ave, Suite B</p></div>')
print("STRIP done")

# ============ MARQUEE (6 words x4 each) ============
for old, new in [
    ('Classic Set', 'Builder Gel'),
    ('Hybrid Set', 'Polygel'),
    ('Volume Set', 'Gel Manicure'),
    ('Mega Volume', 'Pedicure Gel'),
    ('Bottom Lashes', 'Acrylic Nails'),
    ('West Palm Beach, FL', 'Tampa, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)
print("MARQUEE done")

# ============ EXPERIENCIA ============
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-8.jpg" alt="Unas nude con puntas azul marino y detalles de aros dorados" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-5.jpg" alt="Unas blancas estilo ombre con brillo dorado en la cuticula" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="tu enfoque total" data-en="your total focus">your total focus</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Nails by Denis es el suite propio de Denise Dulzaide dentro de un edificio de suites de belleza compartido sobre W Sligh Ave, en Tampa. Cada cita es uno a uno, de builder gel y acrilico a polygel y disenos de unas." data-en="Nails by Denis is Denise Dulzaide own suite inside a shared beauty-suite building on W Sligh Ave, Tampa. Every appointment is one on one, from builder gel and acrylic to polygel and nail art.">Nails by Denis is Denise Dulzaide own suite inside a shared beauty-suite building on W Sligh Ave, Tampa. Every appointment is one on one, from builder gel and acrylic to polygel and nail art.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 52 resenas verificadas en Booksy, y clientas que la llaman su tecnica de unas para siempre." data-en="The result: a perfect 5.0 across 52 verified Booksy reviews, and clients who call her their forever nail technician.">The result: a perfect 5.0 across 52 verified Booksy reviews, and clients who call her their forever nail technician.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="52">52</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Nails by Denis logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Denise · <span class="text-[color:var(--ink-40)]" data-es="Tecnica de unas" data-en="Nail artist">Nail artist</span></span>')
print("EXPERIENCIA done")

# ============ METODO ============
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, un set" data-en="Your visit, one set">Your visit, one set</span> <span class="text-shine" data-es="hecho con detalle" data-en="made with detail">made with detail</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duracion claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Pick your service on Booksy with clear price and duration, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Forma y sistema" data-en="Shape and system">Shape and system</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elegimos el largo, la forma y el sistema: acrilico, builder gel, polygel o apres, segun lo que buscas." data-en="We choose the length, shape and system: acrylic, builder gel, polygel or apres, based on what you want.">We choose the length, shape and system: acrylic, builder gel, polygel or apres, based on what you want.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Denise trabaja con calma y precision, hasta 1h 55min de aplicacion segun el servicio que elijas." data-en="Denise works calmly and precisely, up to 1h 55min of application depending on the service you choose.">Denise works calmly and precisely, up to 1h 55min of application depending on the service you choose.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Salida" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu set terminado, listo para durar hasta tu proxima cita." data-en="You leave with your finished set, ready to last until your next appointment.">You leave with your finished set, ready to last until your next appointment.</p>''')
print("METODO done")

# ============ SERVICIOS ============
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Nails by Denis en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Nails by Denis on Booksy. Booking confirms instantly.">Prices and durations as published by Nails by Denis on Booksy. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="set" data-en="set">set</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Todos los dias" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Regular" data-en="Manicure Regular">Manicure Regular</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura clasica con esmalte regular, la opcion simple y limpia para el dia a dia." data-en="A clean classic manicure with regular polish, the simple everyday option.">A clean classic manicure with regular polish, the simple everyday option.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$24</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salon" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Builder Gel" data-en="Builder Gel">Builder Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura de builder gel que fortalece la una natural y la deja creciendo sana: el servicio que las clientas piden por nombre." data-en="A strengthening builder gel manicure that keeps natural nails healthy and growing, the treatment clients ask for by name.">A strengthening builder gel manicure that keeps natural nails healthy and growing, the treatment clients ask for by name.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$48</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Acabado en gel" data-en="Gel finish">Gel finish</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicure Gel" data-en="Manicure Gel">Manicure Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura con esmalte en gel, brillo intenso y resistencia a los golpes por semanas." data-en="Gel polish manicure with a glossy, chip-resistant finish that lasts for weeks.">Gel polish manicure with a glossy, chip-resistant finish that lasts for weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$33</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">45min</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Ritual completo" data-en="Full ritual">Full ritual</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Combo Deluxe" data-en="Combo Deluxe">Combo Deluxe</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo deluxe completo: manicura y pedicura en gel juntas, para un look terminado de pies a manos." data-en="The full deluxe combo: gel manicure and pedicure together for a complete finished look.">The full deluxe combo: gel manicure and pedicure together for a complete finished look.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$110</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 55min</p></div>
            <a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''.replace('__BOOKSY__', BOOKSY)
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien disponible: acrilico, polygel, apres y pedicura spa. Menu completo de 32 servicios y disponibilidad en Booksy." data-en="Also available: acrylic, polygel, apres and spa pedicure. Full 32-service menu and availability on Booksy.">Also available: acrylic, polygel, apres and spa pedicure. Full 32-service menu and availability on Booksy.</span></p>')
print("SERVICIOS done")

# ============ GALERIA ============
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="nail work">nail work</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Frances pastel con flor 3D" data-en="Pastel French with 3D flower">Pastel French with 3D flower</span><img src="assets/raw/bk-6.jpg" alt="Puntas francesas pastel rosa, celeste y amarillo con flor 3D y dije de estrella dorada" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Mosaico azul y dorado" data-en="Blue and gold mosaic">Blue and gold mosaic</span><img src="assets/raw/bk-4.jpg" alt="Diseno de unas tipo mosaico azul marino y blanco con detalles dorados" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Estrellas festivas" data-en="Festive stars">Festive stars</span><img src="assets/raw/bk-7.jpg" alt="Unas con diseno de estrellas y confeti rojo, blanco y azul" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Puntas francesas con lunares" data-en="Polka dot French tips">Polka dot French tips</span><img src="assets/raw/bk-3.jpg" alt="Manicura con puntas francesas azul marino y lunares blancos" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Nude con aros dorados" data-en="Nude with gold hoops">Nude with gold hoops</span><img src="assets/raw/bk-8.jpg" alt="Unas nude con puntas azul marino y detalles de aros dorados" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Ombre blanco con brillo" data-en="White ombre with shimmer">White ombre with shimmer</span><img src="assets/raw/bk-5.jpg" alt="Unas blancas estilo ombre con brillo dorado en la cuticula" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ============ OPINIONES ============
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="En sus" data-en="In their">In their</span> <span class="text-shine" data-es="propias palabras" data-en="own words">own words</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 52 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 52 verified reviews on Booksy">5.0 out of 5 · 52 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Sweet nice ladies. I love my nails"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tainesha B…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Encantada con el servicio, súper amable y una atención 10/10"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Isabel G…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Loved my nails!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ashlyn H…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep('<a href="__BOOKSY_OLD__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>'.replace('__BOOKSY_OLD__', BOOKSY),
    '<a href="__BOOKSY__" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 52 reseñas en Booksy" data-en="Read all 52 reviews on Booksy">Read all 52 reviews on Booksy</a>'.replace('__BOOKSY__', BOOKSY))
print("OPINIONES done")

# ============ UBICACION ============
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Tampa</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1815 W Sligh Ave, Suite B, Tampa, FL 33604</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=1815+W+Sligh+Ave,+Suite+B,+Tampa,+FL+33604"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los sets mas recientes de Denise y escribe por DM cualquier duda antes de tu cita." data-en="See Denise\'s latest sets and DM any questions before your appointment.">See Denise\'s latest sets and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Mapa: Nails by Denis, 1815 W Sligh Ave, Tampa FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=1815+W+Sligh+Ave,+Suite+B,+Tampa,+FL+33604&output=embed"')
print("UBICACION done")

# ============ CTA FINAL ============
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Unas hermosas, una cita a la vez." data-en="Beautiful nails, one appointment at a time.">Beautiful nails, one appointment at a time.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu proximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en linea en segundos: tu builder gel, tu acrilico, tu polygel o la manicura en gel que ya te toca." data-en="Book online in seconds: your builder gel, your acrylic, your polygel, or the gel manicure you are due for.">Book online in seconds: your builder gel, your acrylic, your polygel, or the gel manicure you are due for.</p>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')
print("CTA FINAL done")

# ============ FOOTER ============
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Nails by Denis</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-2.jpg" alt="Nails by Denis logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Nails by Denis</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salon de unas en Tampa, FL. Atencion con cita previa." data-en="Nail salon in Tampa, FL. By appointment only.">Nail salon in Tampa, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>1815 W Sligh Ave, Suite B, Tampa, FL 33604</p>')
rep('<p><a href="__BOOKSY__" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'.replace('__BOOKSY__', BOOKSY),
    '<p><a href="__BOOKSY__" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'.replace('__BOOKSY__', BOOKSY))
rep('<p><a href="__IG__" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · __HANDLE__</a></p>'.replace('__IG__', IG_URL).replace('__HANDLE__', IG_HANDLE),
    '<p><a href="__IG__" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · __HANDLE__</a></p>'.replace('__IG__', IG_URL).replace('__HANDLE__', IG_HANDLE))
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Nails by Denis.</p>')
print("FOOTER done")

# ============ FINAL: BADGE PROTECT -> GENERIC HUE ROTATE -> RESTORE ============
HUE_SHIFT = -140.0

badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)


def shift_hex(hexcode):
    r = int(hexcode[0:2], 16) / 255.0
    g = int(hexcode[2:4], 16) / 255.0
    b = int(hexcode[4:6], 16) / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l, s)
    return '%02x%02x%02x' % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def shift_rgb_tuple(rr, gg, bb):
    r, g, b = rr / 255.0, gg / 255.0, bb / 255.0
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    hh = (hh * 360 + HUE_SHIFT) % 360 / 360
    r2, g2, b2 = colorsys.hls_to_rgb(hh, l, s)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def repl_hex(mo):
    return '#' + shift_hex(mo.group(1))


def repl_rgba(mo):
    rr, gg, bb = int(mo.group(1)), int(mo.group(2)), int(mo.group(3))
    alpha = mo.group(4)
    nr, ng, nb = shift_rgb_tuple(rr, gg, bb)
    if alpha is not None:
        return 'rgba(%d,%d,%d,%s)' % (nr, ng, nb, alpha)
    return 'rgb(%d,%d,%d)' % (nr, ng, nb)


h = re.sub(r'#([0-9a-fA-F]{6})\b', repl_hex, h)
h = re.sub(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)', repl_rgba, h)

h = h.replace('@@BADGE@@', badge_block, 1)
print('PALETTE (hue shift %.1f) done, base #a04a72 -> #%s' % (HUE_SHIFT, shift_hex('a04a72')))

open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print("ALL DONE", len(h))
