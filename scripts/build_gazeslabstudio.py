import re
import colorsys

h = open('output/gazeslabstudio/index.html').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)


# ---------- 1. Proteger el badge Merktop ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# ---------- 2. JSON-LD completo ----------
NEW_JSONLD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Gazes Lab. Studio",
    "description": "Lash and brow studio in Miami, FL (West Flagler / Westchester): classic, wet effect, hybrid, medium volume and mega volume lash extensions, brow lamination, lash lift and nano powder brows.",
    "address": { "@type": "PostalAddress", "streetAddress": "7795 West Flagler Street", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33144", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.773461888166455, "longitude": -80.32224523657015 },
    "sameAs": ["https://booksy.com/en-us/1238839_gazes-lab-studio_brows-lashes_15889_miami", "https://www.instagram.com/gazeslab._/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "29", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "13:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Lash & brow services", "itemListElement": [
      { "@type": "Offer", "price": "102", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Set Classic" } },
      { "@type": "Offer", "price": "111", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Set Hybrid Glam" } },
      { "@type": "Offer", "price": "128", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Set Mega Volumen" } },
      { "@type": "Offer", "price": "77", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Laminado de cejas" } }
    ] }
  }
  </script>'''
h = re.sub(r'<script type="application/ld\+json">.*?</script>', NEW_JSONLD, h, count=1, flags=re.S)

# ---------- 3. HEAD ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Gazes Lab. Studio · Lash & Brow Studio in Miami, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Gazes Lab. Studio, West Flagler, Miami FL: classic, wet effect, hybrid and mega volume lash extensions, brow lamination and nano powder brows, with a perfect 5.0 across 29 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Gazes Lab. Studio · Lash & Brow Studio in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Lash extensions, brow lamination and nano powder brows. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/hero.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/interior.jpg" />')

# ---------- 4. PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">GL</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Gazes Lab</span>')

# ---------- 5. NAV brand + logo (monogram, sin foto) ----------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(160,74,114,0.35)]" style="background:rgba(160,74,114,0.08); color:var(--accent-deep)" aria-hidden="true">GL</span>')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Gazes <span class="text-[color:var(--accent-deep)]">Lab</span></span>')

# ---------- 6. HERO ----------
rep('<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Miami, FL · Estudio de Pestañas y Cejas" data-en="Miami, FL · Lash &amp; Brow Studio">Miami, FL · Lash &amp; Brow Studio</p>')
rep('<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Llevamos tu mirada a otro nivel." data-en="We take your gaze to the next level.">We take your gaze to the next level.</p>')
rep('''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>
        </h1>''',
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Extensiones de pestañas" data-en="Lash extensions and">Lash extensions and</span><br /><span data-es="y diseño de cejas, hechos para " data-en="brow design, made to ">brow design, made to </span><span class="text-shine" data-es="resaltar" data-en="stand out">stand out</span>
        </h1>''')
rep('<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Sets completos clásicos, wet effect, híbrido, volumen medio y mega volumen, además de laminado de cejas, lash lift y cejas en nano powder. Una sola artista, Yoana, en su estudio de West Flagler Street, con un 5.0 perfecto en Booksy." data-en="Full classic, wet effect, hybrid, medium volume and mega volume lash sets, plus brow lamination, lash lift and nano powder brows. One artist, Yoana, in her West Flagler Street studio, with a perfect 5.0 on Booksy.">Full classic, wet effect, hybrid, medium volume and mega volume lash sets, plus brow lamination, lash lift and nano powder brows. One artist, Yoana, in her West Flagler Street studio, with a perfect 5.0 on Booksy.</p>')
rep('''<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>''',
    '''<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 29 reseñas en Booksy" data-en="5.0 · 29 reviews on Booksy">5.0 · 29 reviews on Booksy</span>
        </div>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/hero.jpg" alt="Extreme close-up of finished brow and lash extensions result at Gazes Lab. Studio, eyes open" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Full Set Mega Volumen</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$128 · 2h" data-en="$128 · 2h">$128 · 2h</p>''')

# ---------- 7. STRIP DE CONFIANZA ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="29">29</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Lash <span class="text-shine">&amp;</span> Brow</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones · Laminado" data-en="Extensions · Lamination">Extensions · Lamination</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">19 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Full menu on Booksy</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">7795 West Flagler St</p></div>')

# ---------- 8. MARQUEE (4 apariciones cada palabra) ----------
MARQUEE_WORDS = [
    ('Classic Set', 'Full Set Classic'),
    ('Hybrid Set', 'Wet Effect'),
    ('Volume Set', 'Hybrid Glam'),
    ('Mega Volume', 'Mega Volumen'),
    ('Bottom Lashes', 'Brow Lamination'),
    ('West Palm Beach, FL', 'Miami, FL'),
]
for old_w, new_w in MARQUEE_WORDS:
    old_span = f'<span class="marquee-word">{old_w}</span>'
    cnt = h.count(old_span)
    assert cnt == 4, f'{old_w}: se esperaban 4 apariciones, hay {cnt}'
    h = h.replace(old_span, f'<span class="marquee-word">{new_w}</span>')

# ---------- 9. LA EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/hero.jpg" alt="Close-up of finished lash extensions and brow lamination, eyes open" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/result-2.jpg" alt="Close-up portrait of a client after lash and brow work at Gazes Lab. Studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="dedicada a tu mirada" data-en="devoted to your gaze">devoted to your gaze</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Gazes Lab. Studio es el estudio de una sola artista, Yoana Martínez, en 7795 West Flagler Street, Miami. Cada set de pestañas y cada laminado de cejas se hace a mano, cita por cita, con productos que ella misma elige." data-en="Gazes Lab. Studio is the studio of one artist, Yoana Martinez, at 7795 West Flagler Street in Miami. Every lash set and every brow lamination is done by hand, appointment by appointment, with products she chooses herself.">Gazes Lab. Studio is the studio of one artist, Yoana Martinez, at 7795 West Flagler Street in Miami. Every lash set and every brow lamination is done by hand, appointment by appointment, with products she chooses herself.</p>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: un 5.0 perfecto en 29 reseñas verificadas de Booksy, y clientas que vuelven cita tras cita por sus pestañas y su ceja perfilada." data-en="The result: a perfect 5.0 across 29 verified Booksy reviews, and clients who come back appointment after appointment for their lashes and shaped brows.">The result: a perfect 5.0 across 29 verified Booksy reviews, and clients who come back appointment after appointment for their lashes and shaped brows.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="29">29</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />',
    '<img src="assets/raw/avatar-yoana.jpg" alt="Yoana Martinez, lash and brow artist at Gazes Lab. Studio" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Yoana Martínez · <span class="text-[color:var(--ink-40)]" data-es="Pestañas y cejas" data-en="Lash &amp; brow artist">Lash &amp; brow artist</span></span>')

# ---------- 10. EL METODO ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, mirada" data-en="Your visit, look">Your visit, look</span> <span class="text-shine" data-es="por mirada" data-en="by look">by look</span></h2>')
rep('<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio de pestañas o cejas en Booksy, con precio y duración claros, y confirmas al instante." data-en="Pick your lash or brow service on Booksy with clear price and duration, and confirm instantly.">Pick your lash or brow service on Booksy with clear price and duration, and confirm instantly.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Diseño a tu medida" data-en="Design for you">Design for you</h3>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, densidad natural y el efecto que buscas: de ahí sale el set clásico, híbrido, wet effect o volumen." data-en="Eye shape, natural density and the look you want: that is where the classic, hybrid, wet effect or volume set comes from.">Eye shape, natural density and the look you want: that is where the classic, hybrid, wet effect or volume set comes from.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="La aplicación" data-en="The application">The application</h3>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas y Yoana trabaja con calma, pestaña por pestaña o ceja por ceja, hasta 3 horas en los servicios de nano powder." data-en="You lie back and Yoana works calmly, lash by lash or brow by brow, up to 3 hours for nano powder sessions.">You lie back and Yoana works calmly, lash by lash or brow by brow, up to 3 hours for nano powder sessions.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Tu próxima cita" data-en="Your next visit">Your next visit</h3>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno o retoque ya agendado para mantener tu mirada siempre lista." data-en="You leave with your fill or retouch already booked to keep your look ready.">You leave with your fill or retouch already booked to keep your look ready.</p>')

# ---------- 11. SERVICIOS: header ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="mirada" data-en="look">look</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Gazes Lab. Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Gazes Lab. Studio on Booksy. Booking confirms instantly.">Prices and durations as published by Gazes Lab. Studio on Booksy. Booking confirms instantly.</p>')

# ---------- 12. SERVICIOS: grid de 4 cards + menu completo por categorias (regex, reemplazo entero) ----------
BOOKSY_NEW = 'https://booksy.com/en-us/1238839_gazes-lab-studio_brows-lashes_15889_miami'

CATS = [
    ('Lash Extensions', 'Pestañas', [
        ('Full Set Classic', '$102'),
        ('Refill Classic Set', '$60 · 2h'),
        ('Full Set Wet Effect', '$102'),
        ('Refill Wet Effect', '$68 · 2h'),
        ('Full Set Hybrid Glam', '$111'),
        ('Refill Hybrid Glam', '$72 · 1h 30min'),
        ('Full Set Volumen Medio', '$119 · 2h 30min'),
        ('Refill Volumen Medio', '$77'),
        ('Full Set Mega Volumen', '$128 · 2h'),
        ('Refill Mega Volumen', '$85'),
        ('Eyelash Lift', '$85'),
        ('Lash Removal', '$17 · 30min'),
    ]),
    ('Brows', 'Cejas', [
        ('Eyebrow Waxing / Depilación de cejas', '$21 · 30min'),
        ('Bozo Waxing', '$9'),
        ('Depilación de cejas + Tinte Henna', '$34 · 30min'),
        ('Laminado de cejas (incluye depilación y tinte)', '$77'),
        ('Laminado (incluye diseño y depilación)', '$80 · 30min'),
    ]),
    ('Nano Powder', 'Nano Powder', [
        ('Nano Powder', '$350 · 3h'),
        ('Retoque Nano Powder', '$100 · 2h'),
    ]),
]

cat_blocks = []
for i, (en_name, es_name, rows) in enumerate(CATS):
    rows_html = '\n'.join(
        f'          <div class="flex items-baseline justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)] last:border-0"><span class="text-sm font-light">{name}</span><span class="text-sm text-[color:var(--ink-40)] whitespace-nowrap">{price}</span></div>'
        for name, price in rows
    )
    delay = 60 * i
    cat_blocks.append(
        f'''        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:{delay}ms">
          <h3 class="font-display text-lg mb-4" data-es="{es_name}" data-en="{en_name}">{en_name}</h3>
{rows_html}
        </div>'''
    )
cat_grid = '\n'.join(cat_blocks)

NEW_SERVICES_GRID = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Efecto natural" data-en="Natural effect">Natural effect</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Full Set Classic</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una extensión por pestaña natural: el efecto limpio de siempre. Rellenos disponibles cada 2 semanas." data-en="One extension per natural lash: the clean, classic everyday effect. Fills available every 2 weeks.">One extension per natural lash: the clean, classic everyday effect. Fills available every 2 weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$102</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Full Set Hybrid Glam</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La mezcla perfecta entre clásico y volumen: textura con cuerpo y brillo natural." data-en="The perfect mix of classic and volume: textured, glamorous and still natural.">The perfect mix of classic and volume: textured, glamorous and still natural.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$111</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Máximo impacto" data-en="Maximum impact">Maximum impact</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Full Set Mega Volumen</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Abanicos densos para el efecto más dramático, hechos a mano pestaña por pestaña." data-en="Dense handmade fans for the most dramatic effect, built lash by lash.">Dense handmade fans for the most dramatic effect, built lash by lash.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$128</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas" data-en="Brows">Brows</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Laminado de cejas" data-en="Brow lamination">Brow lamination</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cejas peinadas hacia arriba, depiladas y con tinte incluido: arcos definidos por semanas." data-en="Brows brushed up, shaped and tinted in one visit: defined arches that last for weeks.">Brows brushed up, shaped and tinted in one visit: defined arches that last for weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$77</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-8">
{cat_grid}
      </div>
      '''

pattern_services = r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)'
assert re.search(pattern_services, h, flags=re.S), 'no se encontro grid de servicios'
h = re.sub(pattern_services, NEW_SERVICES_GRID, h, count=1, flags=re.S)

# ---------- 13. SERVICIOS: nota ----------
pattern_note = r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)'
assert re.search(pattern_note, h, flags=re.S), 'no se encontro nota de servicios'
h = re.sub(
    pattern_note,
    lambda mo: mo.group(1) + '<span data-es="Menú completo con 19 servicios y disponibilidad en tiempo real en Booksy." data-en="Full menu of 19 services and real-time availability on Booksy.">Full menu of 19 services and real-time availability on Booksy.</span>' + mo.group(2),
    h, count=1, flags=re.S,
)

# ---------- 14. GALERIA: header ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span></h2>')

# ---------- 15. GALERIA: grid (regex, reemplazo entero; 3 tiles: fotos reales limitadas) ----------
NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="El estudio de Yoana" data-en="Yoana's studio">Yoana's studio</span><img src="assets/raw/interior.jpg" alt="Gazes Lab. Studio wall sign inside the studio on West Flagler Street, Miami" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Pestañas y cejas terminadas" data-en="Finished lash &amp; brow result">Finished lash &amp; brow result</span><img src="assets/raw/hero.jpg" alt="Extreme close-up of finished eyebrow lamination and lash extensions, eyes open" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Detalle de la mirada" data-en="Close-up detail">Close-up detail</span><img src="assets/raw/result-2.jpg" alt="Close-up portrait of a client's eyes after lash and brow work at Gazes Lab. Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
      </div>
    </section>'''

pattern_gallery = r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>'
assert re.search(pattern_gallery, h, flags=re.S), 'no se encontro grid de galeria'
h = re.sub(pattern_gallery, NEW_GALLERY_GRID, h, count=1, flags=re.S)

# ---------- 16. OPINIONES ----------
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 29 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 29 verified reviews on Booksy">5.0 out of 5 · 29 verified reviews on Booksy</span></p>')

rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Perfecta"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Isaura L.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''')

rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Exelente servicio , me encantaron mis pestañas , quede super satisfecha.."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yuniely N.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''')

rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing lash experience! Super professional, gentle, and my lashes look absolutely beautiful. Highly recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Carolina M.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''')

rep('data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 29 reseñas en Booksy" data-en="Read all 29 reviews on Booksy">Read all 29 reviews on Booksy</a>')

# ---------- 17. UBICACION ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span></h2>')

rep('''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">7795 West Flagler Street, Miami, FL 33144</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=7795+West+Flagler+Street,+Miami,+FL+33144" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''')

rep('''<p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener">@_lashbloom</a>
            </div>
          </div>
        </div>
      </div>''',
    '''<p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira el trabajo más reciente de Yoana y escribe por DM cualquier duda antes de tu cita." data-en="See Yoana's latest work and DM any questions before your appointment.">See Yoana's latest work and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener">@_lashbloom</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a viernes 9:00 a.m. a 7:00 p.m. · Sábados 9:00 a.m. a 1:00 p.m." data-en="Monday to Friday 9:00 AM to 7:00 PM · Saturdays 9:00 AM to 1:00 PM">Monday to Friday 9:00 AM to 7:00 PM · Saturdays 9:00 AM to 1:00 PM</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Domingo cerrado" data-en="Closed Sunday">Closed Sunday</p>
            </div>
          </div>
        </div>
      </div>''')

rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Gazes Lab. Studio, 7795 West Flagler Street, Miami FL"\n          src="https://www.google.com/maps?q=7795+West+Flagler+Street,+Miami,+FL+33144&output=embed"')

# ---------- 18. CTA FINAL ----------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Llevamos tu mirada a otro nivel." data-en="We take your gaze to the next level.">We take your gaze to the next level.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima mirada" data-en="Your next look">Your next look</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set de pestañas, tu laminado de cejas o tus nano powder brows." data-en="Book online in seconds: your lash set, your brow lamination, or your nano powder brows.">Book online in seconds: your lash set, your brow lamination, or your nano powder brows.</p>')

# ---------- 19. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Gazes Lab</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>''',
    '''<span class="w-9 h-9 rounded-full flex items-center justify-center font-display text-xs ring-1 ring-[rgba(240,190,215,0.35)]" style="background:rgba(240,190,215,0.08); color:#f0bed7" aria-hidden="true">GL</span>
          <span class="font-display text-lg tracking-[0.1em] uppercase">Gazes Lab. Studio</span>''')
rep('<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de pestañas y cejas en Miami, FL (West Flagler). Solo con cita previa." data-en="Lash &amp; brow studio in Miami, FL (West Flagler). By appointment only.">Lash &amp; brow studio in Miami, FL (West Flagler). By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>7795 West Flagler Street, Miami, FL 33144</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Gazes Lab. Studio.</p>')

# ---------- 20. Idioma principal: ES (confirmado por descripcion real de Booksy y mayoria de resenas) ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- 21. Globales: Booksy URL, Instagram URL, @handle ----------
BOOKSY_OLD = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
cnt = h.count(BOOKSY_OLD)
assert cnt == 8, f'booksy url: se esperaban 8, hay {cnt}'
h = h.replace(BOOKSY_OLD, BOOKSY_NEW)

IG_OLD = 'https://www.instagram.com/_lashbloom/'
IG_NEW = 'https://www.instagram.com/gazeslab._/'
cnt = h.count(IG_OLD)
assert cnt == 5, f'ig url: se esperaban 5, hay {cnt}'
h = h.replace(IG_OLD, IG_NEW)

HANDLE_OLD = '@_lashbloom'
HANDLE_NEW = '@gazeslab._'
cnt = h.count(HANDLE_OLD)
assert cnt == 4, f'@handle: se esperaban 4, hay {cnt}'
h = h.replace(HANDLE_OLD, HANDLE_NEW)

# ---------- 22. Paleta: rotacion de matiz uniforme (plum-pink -> steel teal-blue) ----------
# a04a72 (hue ~332, "gaze"/mirada -> azul acero elegante). HUE_SHIFT=228 -> hue ~200.
# Distinto de otros lash/brow de Miami ya construidos: valashstudio (mauve/plum #8a4a6b, mismo zip 33144),
# massielbrowsstudio (sage-olive hue~107, Doral), lashartangie (sage green #5c7a5e, Kendall).
HUE_SHIFT = 228.0


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

# ---------- 23. Restaurar badge Merktop (siempre dorado) ----------
h = h.replace('@@BADGE@@', badge_block, 1)

open('output/gazeslabstudio/index.html', 'w').write(h)
print('build OK: gazeslabstudio')
