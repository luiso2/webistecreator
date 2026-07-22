import re
import colorsys

h = open('output/massielbrowsstudio/index.html').read()


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
    "@type": "HealthAndBeautyBusiness",
    "name": "Massiel Brows Studio",
    "description": "Brow and lash studio in Miami, FL: brow design, brow lamination, lash lift and semi-permanent powder brow shading.",
    "address": { "@type": "PostalAddress", "streetAddress": "10890 NW 17th St, Unit 116", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33172", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/857068_massiel-brows-studio_brows-lashes_15889_miami", "https://instagram.com/massielreyesbrowstudio"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "46", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "09:00", "closes": "16:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Brow & lash services", "itemListElement": [
      { "@type": "Offer", "price": "30", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Diseno de Cejas Cera/ Wax" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Laminado de Cejas - Brow Lamination Deluxe" } },
      { "@type": "Offer", "price": "350", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Sombreado de Cejas" } },
      { "@type": "Offer", "price": "120", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lash Lift (Keratina de Pestana)" } }
    ] }
  }
  </script>'''
h = re.sub(r'<script type="application/ld\+json">.*?</script>', NEW_JSONLD, h, count=1, flags=re.S)

# ---------- 3. HEAD ----------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Massiel Brows Studio · Brow & Lash Studio in Miami, FL | 5.0 on Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Massiel Brows Studio, Miami FL: brow design, brow lamination, lash lift and semi-permanent powder brow shading with a perfect 5.0 across 46 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Massiel Brows Studio · Brow & Lash Studio in Miami, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Brow design, lamination, lash lift and powder brows. 5.0 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-5.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-1.jpg" />')

# ---------- 4. PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">MB</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Massiel Brows</span>')

# ---------- 5. NAV brand ----------
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Massiel <span class="text-[color:var(--accent-deep)]">Brows</span></span>')

# ---------- 6. HERO ----------
rep('<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Miami, FL · Estudio de Cejas y Pestañas" data-en="Miami, FL · Brow & Lash Studio">Miami, FL · Brow & Lash Studio</p>')
rep('<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Cejas con forma, sin prisa." data-en="Brows shaped, not rushed.">Brows shaped, not rushed.</p>')
rep('''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>
        </h1>''',
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Diseño de cejas y" data-en="Brow design and">Brow design and</span><br /><span data-es="lifting de pestañas, hechos para " data-en="lash lifts, made to ">lash lifts, made to </span><span class="text-shine" data-es="durar" data-en="last">last</span>
        </h1>''')
rep('<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Depilación y diseño de cejas con cera o hilo, laminado de cejas, lifting y tinte de pestañas, y sombreado semipermanente de cejas, todo en un mismo estudio en Miami, FL. Un 5.0 perfecto en 46 reseñas de Booksy, con una artista a la que sus clientas siguen regresando." data-en="Brow waxing and threading, brow lamination, lash lift and tint, and semi-permanent powder brow shading, all from one studio in Miami, FL. A perfect 5.0 across 46 Booksy reviews, from an artist her clients keep coming back to.">Brow waxing and threading, brow lamination, lash lift and tint, and semi-permanent powder brow shading, all from one studio in Miami, FL. A perfect 5.0 across 46 Booksy reviews, from an artist her clients keep coming back to.</p>')
rep('''<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>
        </div>''',
    '''<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 46 reseñas en Booksy" data-en="5.0 · 46 reviews on Booksy">5.0 · 46 reviews on Booksy</span>
        </div>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-5.jpg" alt="Close-up portrait after brow lamination and a lash lift, natural finish" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Brow Lamination Deluxe</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$100 · 1h 10min" data-en="$100 · 1h 10min">$100 · 1h 10min</p>''')

# ---------- 7. STRIP DE CONFIANZA ----------
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="46">46</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Brows <span class="text-shine">&amp;</span> Lashes</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Diseño · Laminado · Lifting" data-en="Design · Lamination · Lift">Design · Lamination · Lift</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">4+ <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas que regresan por años" data-en="Clients who return for years">Clients who return for years</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">10890 NW 17th St</p></div>')

# ---------- 8. MARQUEE (4 apariciones cada palabra) ----------
MARQUEE_WORDS = [
    ('Classic Set', 'Brow Design'),
    ('Hybrid Set', 'Brow Lamination'),
    ('Volume Set', 'Lash Lift'),
    ('Mega Volume', 'Powder Brows'),
    ('Bottom Lashes', 'Lash Tint'),
    ('West Palm Beach, FL', 'Miami, FL'),
]
for old_w, new_w in MARQUEE_WORDS:
    old_span = f'<span class="marquee-word">{old_w}</span>'
    cnt = h.count(old_span)
    assert cnt == 4, f'{old_w}: se esperaban 4 apariciones, hay {cnt}'
    h = h.replace(old_span, f'<span class="marquee-word">{new_w}</span>')

# ---------- 9. LA EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Close-up portrait of a client with full, groomed natural brows after shaping" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-8.jpg" alt="Close-up portrait of a client with a fresh brow tint and lash lift" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una artista," data-en="One artist,">One artist,</span><br /><span class="text-shine" data-es="dedicada a tus cejas" data-en="devoted to your brows">devoted to your brows</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Massiel Brows Studio es el estudio de una sola artista, Massiel Reyes. Cada ceja se diseña para tu rostro y cada lifting o tinte de pestañas se aplica a mano, en un estudio pequeño en 10890 NW 17th St, Miami, donde sus clientas dicen que escucha y nunca sobre-depila." data-en="Massiel Brows Studio is the studio of one artist, Massiel Reyes. Every brow is shaped for your face and every lash lift or tint is applied by hand, in a small studio at 10890 NW 17th St in Miami where clients say she listens and never overplucks.">Massiel Brows Studio is the studio of one artist, Massiel Reyes. Every brow is shaped for your face and every lash lift or tint is applied by hand, in a small studio at 10890 NW 17th St in Miami where clients say she listens and never overplucks.</p>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: un 5.0 perfecto en 46 reseñas verificadas de Booksy, y clientas que la describen como delicada, profesional y una artista con las cejas." data-en="The result: a perfect 5.0 across 46 verified Booksy reviews, and clients who describe her as gentle, professional and an artist with her brows.">The result: a perfect 5.0 across 46 verified Booksy reviews, and clients who describe her as gentle, professional and an artist with her brows.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="46">46</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Massiel Reyes · <span class="text-[color:var(--ink-40)]" data-es="Cejas y pestañas" data-en="Brow &amp; lash artist">Brow &amp; lash artist</span></span>')

# ---------- 10. EL METODO ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, ceja" data-en="Your visit, brow">Your visit, brow</span> <span class="text-shine" data-es="por ceja" data-en="by brow">by brow</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio: diseño de cejas, laminado, lifting de pestañas o sombreado, en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service: brow design, lamination, lash lift or shading, on Booksy with clear price and duration, and confirm instantly.">Pick your service: brow design, lamination, lash lift or shading, on Booksy with clear price and duration, and confirm instantly.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo de cejas" data-en="Brow mapping">Brow mapping</h3>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del rostro, patrón del vello y el efecto que buscas: de ahí sale el diseño con cera, hilo, tinte o laminado." data-en="Face shape, brow hair pattern and the look you want: that is where the wax, thread, tint or lamination design comes from.">Face shape, brow hair pattern and the look you want: that is where the wax, thread, tint or lamination design comes from.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="El tratamiento" data-en="The treatment">The treatment</h3>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te relajas mientras Massiel trabaja a mano, desde una cera rápida de 15 minutos hasta una corrección de color de 2h 50min." data-en="You relax while Massiel works by hand, from a quick 15-minute wax to a 2h 50min color correction session.">You relax while Massiel works by hand, from a quick 15-minute wax to a 2h 50min color correction session.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Retoque a los 45 días" data-en="45-day retouch">45-day retouch</h3>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu próximo retoque de cejas o refresco de pestañas ya agendado." data-en="You leave with your next brow retouch or lash refresh already booked.">You leave with your next brow retouch or lash refresh already booked.</p>')

# ---------- 11. SERVICIOS: header ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Encuentra tu" data-en="Find your">Find your</span> <span class="text-shine" data-es="forma" data-en="shape">shape</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Massiel Brows Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Massiel Brows Studio on Booksy. Booking confirms instantly.">Prices and durations as published by Massiel Brows Studio on Booksy. Booking confirms instantly.</p>')

# ---------- 12. SERVICIOS: grid de 4 cards + menu completo por categorias (regex, reemplazo entero) ----------
BOOKSY_NEW = 'https://booksy.com/en-us/857068_massiel-brows-studio_brows-lashes_15889_miami'

CATS = [
    ('Brow Design & Waxing', 'Diseño y Depilación de Cejas', [
        ('Diseño de Cejas Cera/ Wax', '$30 · 15min'),
        ('Diseño de Cejas Hilo/ Thread', '$30 · 15min'),
        ('Diseño de Cejas + bozo', '$40 · 20min'),
        ('Diseño con tinte', '$20'),
        ('Diseño de Cejas & Tinte Hib', '$45 · 30min'),
        ('Cejas hombre', '$36 · 20min'),
        ('Retoque de Cejas 45 Dias', '$120'),
        ('Depilacion de Rostro', '$38 · 40min'),
        ('Depilacion de Patillas', '$12 · 25min'),
    ]),
    ('Lamination & Lash Treatments', 'Laminado y Tratamientos de Pestañas', [
        ('Brow lamination', '$80 · 1h 10min'),
        ('Laminado de Cejas - Brow Lamination Deluxe', '$100 · 1h 10min'),
        ('Banhada Lash lift coreano', '$120'),
        ('Lash Lift (Keratina de Pestaña)', '$120'),
        ('Lash Tint | Tinte de Pestañas', '$20'),
        ('Evaluacion Maquillaje permanente', '$35 · 30min'),
    ]),
    ('Semi-Permanent Brows', 'Cejas Semipermanentes', [
        ('Sombreado de Cejas', '$350 · 2h 45min'),
        ('Correccion de Color', '$450 · 2h 50min'),
        ('Retoque PowderBrows anual', '$220 · 2h'),
    ]),
    ('Quick Facial Waxing', 'Depilación Facial Rápida', [
        ('Chin Waxing | Depilacion de Barbilla', '$10'),
        ('Depilacion de Orejas', '$10'),
        ('Depilacion de Nariz', '$10'),
    ]),
    ('Model Call Specials', 'Tarifa de Modelo', [
        ('Model Call- Lash Lift', '$60 · 50min'),
        ('Model Call- Brow Lamination (sin tinte )', '$50 · 50min'),
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
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Diseño diario" data-en="Everyday shaping">Everyday shaping</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Diseño de Cejas Cera/ Wax</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Diseño completo de cejas con cera caliente, limpiando el exceso y afinando tu arco natural." data-en="Full brow shaping with hot wax, cleaning up stray hairs and refining your natural arch.">Full brow shaping with hot wax, cleaning up stray hairs and refining your natural arch.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">15min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Laminado de Cejas - Brow Lamination Deluxe</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cejas peinadas hacia arriba y fijadas por semanas: arcos más llenos y con volumen, con acabado de queratina." data-en="Brows brushed up and set for weeks: fuller, fluffier arches with a keratin finish.">Brows brushed up and set for weeks: fuller, fluffier arches with a keratin finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 10min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Semipermanente" data-en="Semi-permanent">Semi-permanent</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Sombreado de Cejas</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Efecto en polvo suave y degradado que rellena cejas escasas. Incluye corrección de color de trabajos anteriores." data-en="A soft, shaded powder effect that fills sparse brows with a natural gradient. Color correction of previous work is available.">A soft, shaded powder effect that fills sparse brows with a natural gradient. Color correction of previous work is available.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$350</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 45min</p></div>
            <a href="{BOOKSY_NEW}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tratamiento de pestañas" data-en="Lash treatment">Lash treatment</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Lash Lift (Keratina de Pestaña)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un lifting de queratina que curva y fija tus pestañas naturales por semanas. Agrega tinte de pestañas por $20 más." data-en="A keratin lift that curls and holds your natural lashes for weeks. Add a lash tint for $20 more.">A keratin lift that curls and holds your natural lashes for weeks. Add a lash tint for $20 more.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$120</p></div>
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
    lambda mo: mo.group(1) + '<span data-es="Depilación facial y tarifas de modelo disponibles en Booksy. Menú completo y disponibilidad en Booksy." data-en="Facial waxing extras and model-rate sessions available on Booksy. Full menu and availability on Booksy.">Facial waxing extras and model-rate sessions available on Booksy. Full menu and availability on Booksy.</span>' + mo.group(2),
    h, count=1, flags=re.S,
)

# ---------- 14. GALERIA: header ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span></h2>')

# ---------- 15. GALERIA: grid (regex, reemplazo entero) ----------
NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Lifting de pestañas natural" data-en="Soft, natural lash lift">Soft, natural lash lift</span><img src="assets/raw/bk-6.jpg" alt="Extreme close-up of an eye after a soft, natural lash lift with brow above" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Laminado + tinte de pestañas" data-en="Brow lamination + lash tint">Brow lamination + lash tint</span><img src="assets/raw/bk-5.jpg" alt="Portrait of a client with laminated brows and a fresh lash lift and tint" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Diseño completo de cejas" data-en="Full brow shaping">Full brow shaping</span><img src="assets/raw/bk-9.jpg" alt="Close-up portrait of a client with full, groomed natural brows" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Tinte de cejas fresco" data-en="Fresh brow tint">Fresh brow tint</span><img src="assets/raw/bk-8.jpg" alt="Close-up portrait of a client with a fresh brow tint and lash lift" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Detalle de lifting de pestañas" data-en="Lash lift close-up">Lash lift close-up</span><img src="assets/raw/bk-7.jpg" alt="Macro close-up of an eye and brow after a lash lift treatment" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
      </div>
    </section>'''

pattern_gallery = r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>'
assert re.search(pattern_gallery, h, flags=re.S), 'no se encontro grid de galeria'
h = re.sub(pattern_gallery, NEW_GALLERY_GRID, h, count=1, flags=re.S)

# ---------- 16. OPINIONES ----------
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 46 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 46 verified reviews on Booksy">5.0 out of 5 · 46 verified reviews on Booksy</span></p>')

rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Después de muchos años atendiéndome con Massiel hoy probé el brow lamination y me encantó! Massiel es muy profesional y sus productos y manos son excelentes! Quede encanta con el resultado"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Andrea B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''')

rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Super nice un servicio excelente 👌 trasmites una energia tan bonita recomendada 100%"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Anonymous</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''')

rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my experience with Massiel, she’s gentle and truly listens to what you want while making recommendations. I love that she did not butcher my brows as I been letting them fill in !  Love her !"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Anonymous</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''')

rep('data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 46 reseñas en Booksy" data-en="Read all 46 reviews on Booksy">Read all 46 reviews on Booksy</a>')

# ---------- 17. UBICACION ----------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span></h2>')

rep('''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">10890 NW 17th St, Unit 116, Miami, FL 33172</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=10890+NW+17th+St,+Unit+116,+Miami,+FL+33172" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''')

# Nuevo bloque de horario (se inserta despues de la tarjeta de Instagram)
rep('''<p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener">@_lashbloom</a>
            </div>
          </div>
        </div>
      </div>''',
    '''<p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira el trabajo más reciente de Massiel y escribe por DM cualquier duda antes de tu cita." data-en="See Massiel's latest brow and lash work and DM any questions before your appointment.">See Massiel's latest brow and lash work and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener">@_lashbloom</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sábado · 9:00 a.m. a 4:00 p.m." data-en="Monday to Saturday · 9:00 AM to 4:00 PM">Monday to Saturday · 9:00 AM to 4:00 PM</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Domingo cerrado" data-en="Closed Sunday">Closed Sunday</p>
            </div>
          </div>
        </div>
      </div>''')

rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Massiel Brows Studio, 10890 NW 17th St, Unit 116, Miami FL"\n          src="https://www.google.com/maps?q=10890+NW+17th+St,+Unit+116,+Miami,+FL+33172&output=embed"')

# ---------- 18. CTA FINAL ----------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Cejas con forma, sin prisa." data-en="Brows shaped, not rushed.">Brows shaped, not rushed.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tus cejas ideales" data-en="Your best brows">Your best brows</span> <span class="text-shine" data-es="te están esperando" data-en="are waiting">are waiting</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: diseño de cejas, laminado, lifting de pestañas o la sesión de cejas en polvo que querías." data-en="Book online in seconds: brow design, lamination, lash lift or the powder brow session you have been wanting.">Book online in seconds: brow design, lamination, lash lift or the powder brow session you have been wanting.</p>')

# ---------- 19. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Massiel Brows</span>')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Massiel Brows Studio</span>')
rep('<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de cejas y pestañas en Miami, FL. Solo con cita previa." data-en="Brow & lash studio in Miami, FL. By appointment only.">Brow & lash studio in Miami, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>10890 NW 17th St, Unit 116, Miami, FL 33172</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Massiel Brows Studio.</p>')

# ---------- 20. Globales: Booksy URL, Instagram URL, @handle, logo ----------
BOOKSY_OLD = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
cnt = h.count(BOOKSY_OLD)
assert cnt == 8, f'booksy url: se esperaban 8, hay {cnt}'
h = h.replace(BOOKSY_OLD, BOOKSY_NEW)

IG_OLD = 'https://www.instagram.com/_lashbloom/'
IG_NEW = 'https://instagram.com/massielreyesbrowstudio'
cnt = h.count(IG_OLD)
assert cnt == 5, f'ig url: se esperaban 5, hay {cnt}'
h = h.replace(IG_OLD, IG_NEW)

HANDLE_OLD = '@_lashbloom'
HANDLE_NEW = '@massielreyesbrowstudio'
cnt = h.count(HANDLE_OLD)
assert cnt == 4, f'@handle: se esperaban 4, hay {cnt}'
h = h.replace(HANDLE_OLD, HANDLE_NEW)

LOGO_OLD = 'src="assets/raw/logo.jpg" alt="Lash Bloom"'
LOGO_NEW = 'src="assets/raw/bk-1.jpg" alt="Massiel Brows Studio"'
cnt = h.count(LOGO_OLD)
assert cnt == 3, f'logo: se esperaban 3, hay {cnt}'
h = h.replace(LOGO_OLD, LOGO_NEW)

# ---------- 21. Paleta: rotacion de matiz uniforme (plum-pink -> sage-olive) ----------
HUE_SHIFT = 135.0  # grados: plum-pink ~332 -> ~107, sage-olive muted, distinto de nails(42)/spa(310)/barber(170)/hair(250)


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

# ---------- 22. Restaurar badge Merktop (siempre dorado) ----------
h = h.replace('@@BADGE@@', badge_block, 1)

open('output/massielbrowsstudio/index.html', 'w').write(h)
print('build OK: massielbrowsstudio')
