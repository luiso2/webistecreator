import re
import colorsys

SLUG = 'arbellabeautyestudio'
PATH = f'output/{SLUG}/index.html'
h = open(PATH, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'NO ENCONTRADO: ' + a[:200]
    if n is None:
        h = h.replace(a, b)
    else:
        count = h.count(a)
        assert count == n, f'esperaba {n} ocurrencias, encontre {count}: ' + a[:160]
        h = h.replace(a, b, n)


# NOTA de orden: el contenido (textos, URLs, imagenes) se reemplaza PRIMERO mientras la
# paleta original sigue intacta (asi los anchors que incluyen rgba()/hex dentro de una
# clase larga siguen siendo validos). La rotacion de matiz (proteger badge -> shift ->
# restaurar badge) se aplica al final, sobre el documento ya completo, y cubre TODOS los
# hex/rgba del archivo (incluido cualquier literal dentro de las secciones nuevas).

# ---------- 3. Constantes del negocio ----------
BOOKSY = 'https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa'
IG_URL = 'https://instagram.com/Ar_bella_yudyth'
IG_HANDLE = '@Ar_bella_yudyth'
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
OLD_IG = 'https://www.instagram.com/_lashbloom/'
OLD_IG_HANDLE = '@_lashbloom'

# Reemplazo global de URLs (todas las ocurrencias)
rep(OLD_BOOKSY, BOOKSY, n=None)
rep(OLD_IG, IG_URL, n=None)
rep(OLD_IG_HANDLE, IG_HANDLE, n=None)

# ---------- 4. HEAD ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')

rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Arbella Beauty Studio · Day Spa en Tampa, FL | 5.0 en Booksy</title>'
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Arbella Beauty Studio, Tampa FL: faciales, microagujas y exosomas para la piel, cejas y labios con micropigmentación de lujo, y depilación. 5.0 en 35 reseñas de Booksy. Reserva online." />'
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Arbella Beauty Studio · Day Spa en Tampa, FL" />'
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Faciales, cejas, labios y depilación. 5.0 en Booksy. Reserva online." />'
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-12.jpg" />'
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-9.jpg" />'
)

OLD_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Lash Bloom LLC",
    "description": "Lash studio in West Palm Beach, FL: classic, hybrid, volume and mega volume eyelash extensions and fills.",
    "address": { "@type": "PostalAddress", "streetAddress": "4580 Cresthaven Blvd", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33415", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa", "https://instagram.com/Ar_bella_yudyth"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "86", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Lash services", "itemListElement": [
      { "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic full set" } },
      { "@type": "Offer", "price": "145", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Hybrid full set" } },
      { "@type": "Offer", "price": "155", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Volume full set" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic 2wk fill" } }
    ] }
  }
  </script>'''
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "DaySpa",
    "name": "Arbella Beauty Studio",
    "description": "Day spa boutique en Tampa, FL: faciales profundos, microagujas y exosomas para la piel, micropigmentación de cejas y labios de lujo, y depilación con cera.",
    "address": { "@type": "PostalAddress", "streetAddress": "4023 W Waters Ave", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33614", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.026173, "longitude": -82.510376 },
    "sameAs": ["https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa", "https://instagram.com/Ar_bella_yudyth"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "35", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "09:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "11:00", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de belleza", "itemListElement": [
      { "@type": "Offer", "price": "115", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Deep Facial Cleansing" } },
      { "@type": "Offer", "price": "350", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lip Blush" } },
      { "@type": "Offer", "price": "280", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luxury Microblading" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Lash Lift" } }
    ] }
  }
  </script>'''
rep(OLD_JSONLD, NEW_JSONLD)

# ---------- 5. Preloader ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">AB</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Arbella Beauty</span>')

# ---------- 6. NAV: logo + brand ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<img src="assets/raw/bk-9.jpg" alt="Arbella Beauty Studio" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />'
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Arbella <span class="text-[color:var(--accent-deep)]">Beauty</span></span>'
)

# ---------- 7. HERO ----------
rep(
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Tampa, FL · Day Spa" data-en="Tampa, FL · Day Spa">Tampa, FL · Day Spa</p>'
)
rep(
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu piel, tus cejas, tu mejor versión." data-en="Your skin, your brows, your best you.">Tu piel, tus cejas, tu mejor versión.</p>'
)
rep(
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>
        </h1>''',
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Facial, cejas y labios" data-en="Facials, brows and lips">Facial, cejas y labios</span><br /><span data-es="pensados para hacerte " data-en="designed to make you ">pensados para hacerte </span><span class="text-shine" data-es="brillar" data-en="glow">brillar</span>
        </h1>'''
)
rep(
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Un day spa de una sola especialista en el oeste de Tampa: faciales profundos, microagujas y exosomas para la piel, cejas y labios con micropigmentación de lujo, y depilación con cera. Todo con cita previa y Yudyth Arbella al frente de cada tratamiento." data-en="A one-specialist day spa in west Tampa: deep facials, microneedling and exosomes for the skin, luxury lip and brow micropigmentation, and waxing. Every treatment led personally by Yudyth Arbella, by appointment.">Un day spa de una sola especialista en el oeste de Tampa: faciales profundos, microagujas y exosomas para la piel, cejas y labios con micropigmentación de lujo, y depilación con cera. Todo con cita previa y Yudyth Arbella al frente de cada tratamiento.</p>'
)
rep(
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 35 reseñas en Booksy" data-en="5.0 · 35 reviews on Booksy">5.0 · 35 reseñas en Booksy</span>'
)
rep(
    '''<div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>
          </div>''',
    '''<div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-12.jpg" alt="Resultado de tratamiento de labios en primer plano" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Servicio de firma" data-en="Signature service">Servicio de firma</p>
            <p class="font-display text-lg">Lip Blush</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$350 · 2h 40min" data-en="$350 · 2h 40min">$350 · 2h 40min</p>
          </div>'''
)

# ---------- 8. STRIP DE CONFIANZA ----------
OLD_STRIP = '''<div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>
    </div>'''
NEW_STRIP = '''<div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="35">35</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Piel <span class="text-shine">&amp;</span> Cejas</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Faciales, depilación y más" data-en="Facials, waxing &amp; more">Faciales, depilación y más</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+30 <span class="text-shine" data-es="servicios" data-en="services">servicios</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Menú completo en Booksy</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4023 W Waters Ave</p></div>
    </div>'''
rep(OLD_STRIP, NEW_STRIP)

# ---------- 9. MARQUEE (x2 bloques completos) ----------
OLD_MARQUEE_1 = '''<div class="marquee" aria-hidden="true">
    <div class="marquee-track">
      <div class="marquee-seq">
        <span class="marquee-word">Classic Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hybrid Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Volume Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Mega Volume</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Bottom Lashes</span><span class="marquee-star">✦</span>
        <span class="marquee-word">West Palm Beach, FL</span><span class="marquee-star">✦</span>
      </div>
      <div class="marquee-seq">
        <span class="marquee-word">Classic Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hybrid Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Volume Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Mega Volume</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Bottom Lashes</span><span class="marquee-star">✦</span>
        <span class="marquee-word">West Palm Beach, FL</span><span class="marquee-star">✦</span>
      </div>
    </div>
  </div>'''
NEW_MARQUEE_1 = '''<div class="marquee" aria-hidden="true">
    <div class="marquee-track">
      <div class="marquee-seq">
        <span class="marquee-word">Facial Profundo</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hidrofacial</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lip Blush</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Microblading</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Lamination</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Tampa, FL</span><span class="marquee-star">✦</span>
      </div>
      <div class="marquee-seq">
        <span class="marquee-word">Facial Profundo</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hidrofacial</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lip Blush</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Microblading</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Lamination</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Tampa, FL</span><span class="marquee-star">✦</span>
      </div>
    </div>
  </div>'''
rep(OLD_MARQUEE_1, NEW_MARQUEE_1)

OLD_MARQUEE_2 = '''<div class="marquee marquee-reverse" aria-hidden="true">
    <div class="marquee-track">
      <div class="marquee-seq">
        <span class="marquee-word">Classic Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hybrid Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Volume Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Mega Volume</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Bottom Lashes</span><span class="marquee-star">✦</span>
        <span class="marquee-word">West Palm Beach, FL</span><span class="marquee-star">✦</span>
      </div>
      <div class="marquee-seq">
        <span class="marquee-word">Classic Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hybrid Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Volume Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Mega Volume</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Bottom Lashes</span><span class="marquee-star">✦</span>
        <span class="marquee-word">West Palm Beach, FL</span><span class="marquee-star">✦</span>
      </div>
    </div>
  </div>'''
NEW_MARQUEE_2 = '''<div class="marquee marquee-reverse" aria-hidden="true">
    <div class="marquee-track">
      <div class="marquee-seq">
        <span class="marquee-word">Facial Profundo</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hidrofacial</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lip Blush</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Microblading</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Lamination</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Tampa, FL</span><span class="marquee-star">✦</span>
      </div>
      <div class="marquee-seq">
        <span class="marquee-word">Facial Profundo</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hidrofacial</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lip Blush</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Microblading</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Lamination</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Tampa, FL</span><span class="marquee-star">✦</span>
      </div>
    </div>
  </div>'''
rep(OLD_MARQUEE_2, NEW_MARQUEE_2)

# ---------- 10. LA EXPERIENCIA (bloque completo) ----------
OLD_EXPERIENCIA = '''<div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-14 items-center">
      <div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>
          </div>
        </div>
      </div>
    </div>'''
NEW_EXPERIENCIA = '''<div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-14 items-center">
      <div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-9.jpg" alt="Interior del estudio Arbella Beauty Studio con decoración rosa y equipo profesional" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-4.jpg" alt="Tratamiento facial en proceso con luz led profesional" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un estudio boutique" data-en="A boutique studio">Un estudio boutique</span><br /><span class="text-shine" data-es="hecho a tu medida" data-en="made just for you">hecho a tu medida</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Arbella Beauty Studio es el espacio de una sola especialista licenciada, Yudyth Arbella, en el oeste de Tampa. Cada cita combina faciales profundos, microagujas y exosomas para la piel con micropigmentación de cejas y labios de alta gama, en un ambiente cuidado y personal." data-en="Arbella Beauty Studio is the space of one licensed specialist, Yudyth Arbella, in west Tampa. Every visit blends deep facials, microneedling and exosomes for the skin with high-end brow and lip micropigmentation, in a warm, personal setting.">Arbella Beauty Studio es el espacio de una sola especialista licenciada, Yudyth Arbella, en el oeste de Tampa. Cada cita combina faciales profundos, microagujas y exosomas para la piel con micropigmentación de cejas y labios de alta gama, en un ambiente cuidado y personal.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 5.0 perfecto en 35 reseñas verificadas y un menú de más de 30 servicios (faciales, cejas, pestañas, labios y depilación) pensado para que encuentres tu tratamiento ideal sin salir del estudio." data-en="The result: a perfect 5.0 across 35 verified reviews and a menu of more than 30 services (facials, brows, lips and waxing) so you can find your ideal treatment without leaving the studio.">El resultado: 5.0 perfecto en 35 reseñas verificadas y un menú de más de 30 servicios (faciales, cejas, pestañas, labios y depilación) pensado para que encuentres tu tratamiento ideal sin salir del estudio.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="35">35</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Atención personal</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-9.jpg" alt="Arbella Beauty Studio" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yudyth Arbella · <span class="text-[color:var(--ink-40)]" data-es="Especialista licenciada" data-en="Licensed specialist">Especialista licenciada</span></span>
          </div>
        </div>
      </div>
    </div>'''
rep(OLD_EXPERIENCIA, NEW_EXPERIENCIA)

# ---------- 11. EL METODO ----------
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, paso" data-en="Your visit, step">Tu cita, paso</span> <span class="text-shine" data-es="a paso" data-en="by step">a paso</span></h2>'
)
OLD_METODO_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>
        </div>
      </div>'''
NEW_METODO_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Reserva online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu tratamiento en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your treatment on Booksy with clear price and duration, and confirm instantly.">Eliges tu tratamiento en Booksy con precio y duración claros, y confirmas al instante.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Análisis de piel" data-en="Skin check-in">Análisis de piel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Yudyth revisa tu piel o tus cejas y ajusta la técnica exacta para el resultado que buscas." data-en="Yudyth checks your skin or brows and tailors the exact technique for the result you want.">Yudyth revisa tu piel o tus cejas y ajusta la técnica exacta para el resultado que buscas.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Tratamiento personalizado" data-en="Personalized treatment">Tratamiento personalizado</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas y te relajas mientras Yudyth trabaja con calma, paso a paso, en cada detalle." data-en="You lie back and relax while Yudyth works calmly, step by step, on every detail.">Te recuestas y te relajas mientras Yudyth trabaja con calma, paso a paso, en cada detalle.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Cuidado post-tratamiento" data-en="Aftercare guidance">Cuidado post-tratamiento</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con instrucciones claras de cuidado y, si aplica, tu próxima cita de retoque agendada." data-en="You leave with clear aftercare instructions and, if needed, your next touch-up booked.">Sales con instrucciones claras de cuidado y, si aplica, tu próxima cita de retoque agendada.</p>
        </div>
      </div>'''
rep(OLD_METODO_GRID, NEW_METODO_GRID)

# ---------- 12. SERVICIOS: encabezado ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="tratamiento" data-en="treatment">tratamiento</span></h2>'
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Arbella Beauty Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Arbella Beauty Studio on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Arbella Beauty Studio en Booksy. Reserva con confirmación inmediata.</p>'
)

# ---------- 13. SERVICIOS: 4 cards destacadas (regex sobre el grid completo) ----------
CARDS_PATTERN = re.compile(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    re.S
)
assert CARDS_PATTERN.search(h), 'no se encontro el grid de servicios'
NEW_CARDS = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Piel renovada" data-en="Renewed skin">Piel renovada</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Limpieza Facial Profunda" data-en="Deep Facial Cleansing">Limpieza Facial Profunda</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Limpieza profunda con extracción, doble exfoliación e hidratación para dejar la piel visiblemente más clara y suave." data-en="A deep cleanse with extraction, double exfoliation and hydration, leaving skin visibly clearer and smoother.">Limpieza profunda con extracción, doble exfoliación e hidratación para dejar la piel visiblemente más clara y suave.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$115</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 40min</p></div>
            <a href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Servicio de firma" data-en="Signature service">Servicio de firma</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Lip Blush</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Micropigmentación semi-permanente de labios que aporta color natural, definición y un efecto de labios más llenos. Incluye revisión de color y cuidado post-tratamiento." data-en="Semi-permanent lip micropigmentation that adds natural color, definition and a fuller-looking effect. Includes color check and aftercare guidance.">Micropigmentación semi-permanente de labios que aporta color natural, definición y un efecto de labios más llenos. Incluye revisión de color y cuidado post-tratamiento.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$350</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 40min</p></div>
            <a href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas pelo a pelo" data-en="Hair-stroke brows">Cejas pelo a pelo</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Luxury Microblading</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Técnica pelo a pelo para cejas con apariencia de vello natural, trazo por trazo, ideal para un efecto denso y definido." data-en="Hair-stroke technique for naturally full-looking brows, stroke by stroke, for a dense, defined effect.">Técnica pelo a pelo para cejas con apariencia de vello natural, trazo por trazo, ideal para un efecto denso y definido.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$280</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Mirada realzada" data-en="Lifted look">Mirada realzada</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Lash Lift</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Levantamiento de pestañas con tinte incluido para una mirada más abierta y definida sin necesidad de extensiones." data-en="Lash lift with tint included for a more open, defined look without extensions.">Levantamiento de pestañas con tinte incluido para una mirada más abierta y definida sin necesidad de extensiones.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = CARDS_PATTERN.sub(NEW_CARDS, h, count=1)

# ---------- 14. SERVICIOS: nota + menu completo agrupado por categoria ----------
NOTA_PATTERN = re.compile(
    r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)',
    re.S
)
assert NOTA_PATTERN.search(h), 'no se encontro la nota de servicios'


def item_row(name, price, duration=None):
    name = name.replace('&', '&amp;')
    dur = f' · {duration}' if duration else ''
    return (f'<div class="flex items-center justify-between gap-4 py-3 border-b border-[color:var(--accent-ghost)] last:border-b-0">'
            f'<p class="text-sm font-light text-[color:var(--ink-60)]">{name}</p>'
            f'<p class="text-sm font-display shrink-0">${price}<span class="text-xs text-[color:var(--ink-40)] font-sans">{dur}</span></p>'
            f'</div>')


FACIAL_ITEMS = [
    ('Exosome Skin Renewal / Rejuvenecimiento con exosomas', 180, '30min'),
    ('Salmon DNA Skin Repair Microneedling', 150, None),
    ('Deep facial cleansing / Limpieza facial profundo', 115, '1h 40min'),
    ('SNATCHED V-LINE ✨ Contorno & Reducción de Papada', 120, '50min'),
    ('Hidrofacial', 125, None),
    ('✨ Luxe Chemical Peel / Peeling Químico de Lujo', 100, '1h 30min'),
    ('LED light therapy / Terapia de luz led', 60, None),
    ('Dermaplaning', 65, None),
    ('Simple facial cleansing / Limpieza facial simple', 95, '1h 30min'),
    ('Facial cleansing + microdermoabrasion', 100, '1h 30min'),
    ('Face Hair Removal / Remover vellos de la cara', 60, None),
    ('Lip Waxing / Depilación de bigote', 10, None),
    ('Remoción de verrugas cutáneas / Skin wart removal', 45, '50min'),
    ('Hydralip Glass Lips Treatment / Hidratación de labios', 55, None),
    ('Back face / Facial de espalda', 125, None),
]
BROWS_ITEMS = [
    ('Luxury Microblading – Cejas Pelo a Pelo', 280, '2h'),
    ('NANO COMBO BROWS / Combinación de técnicas', 250, None),
    ('Powder brows / Efecto sombreado o maquillado', 250, None),
    ('Lip Blush / Labios micropigmentados', 350, '2h 40min'),
    ('Luxury Eyeliner Micropigmentation – Semi-Permanent', 150, None),
    ('Micropigmented eyebrow retouching / Retoque de ceja', 150, None),
    ('Eyebrow pigment removal / Remoción de cejas pigmentadas', 150, None),
    ('Luxury Brow Lamination / Laminado de Cejas de Lujo', 95, '1h 30min'),
    ('Eyebrow waxing / Depilación de cejas con cera', 25, None),
    ('Henna dye / Tinte henna / waxing', 45, '50min'),
    ('Lash Lift / Levantamiento de Pestaña + Tinte', 100, '1h 30min'),
    ('✨ Lash Removal / Remoción de Extensiones de Pestaña', 25, None),
]
BODY_ITEMS = [
    ('Brazilian wax + vajacial', 110, '1h 30min'),
    ('Underarm waxing / Depilación de axilas', 50, '40min'),
    ('Bikini Waxing', 75, '45min'),
]

full_menu_html = (
    '<div class="grid md:grid-cols-2 gap-6 mt-12">'
    '<div class="glass rounded-3xl p-7 reveal md:col-span-2" style="transition-delay:0ms">'
    '<h3 class="font-display text-xl mb-1" data-es="Faciales &amp; Piel" data-en="Facials &amp; Skin">Faciales &amp; Piel</h3>'
    '<p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-4" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Menú completo en Booksy</p>'
    + ''.join(item_row(*i) for i in FACIAL_ITEMS) +
    '</div>'
    '<div class="glass rounded-3xl p-7 reveal" style="transition-delay:90ms">'
    '<h3 class="font-display text-xl mb-1" data-es="Cejas, Pestañas &amp; Micropigmentación" data-en="Brows, Lashes &amp; Permanent Makeup">Cejas, Pestañas &amp; Micropigmentación</h3>'
    '<p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-4" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Menú completo en Booksy</p>'
    + ''.join(item_row(*i) for i in BROWS_ITEMS) +
    '</div>'
    '<div class="glass rounded-3xl p-7 reveal" style="transition-delay:180ms">'
    '<h3 class="font-display text-xl mb-1" data-es="Depilación &amp; Cuerpo" data-en="Waxing &amp; Body">Depilación &amp; Cuerpo</h3>'
    '<p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-4" data-es="Menú completo en Booksy" data-en="Full menu on Booksy">Menú completo en Booksy</p>'
    + ''.join(item_row(*i) for i in BODY_ITEMS) +
    '</div>'
    '</div>'
)

NOTA_NEW_TEXT = ('<span data-es="Estos son algunos favoritos. Debajo está el menú completo de Arbella Beauty Studio, '
                  'agrupado por categoría con precios y duraciones tal como aparecen en Booksy." '
                  'data-en="These are a few favorites. Below is Arbella Beauty Studio\'s full menu, grouped by category, '
                  'with prices and durations exactly as listed on Booksy.">Estos son algunos favoritos. Debajo está el menú '
                  'completo de Arbella Beauty Studio, agrupado por categoría con precios y duraciones tal como aparecen en Booksy.</span>')

h = NOTA_PATTERN.sub(lambda mo: mo.group(1) + NOTA_NEW_TEXT + mo.group(2) + full_menu_html, h, count=1)

# ---------- 15. GALERIA (regex sobre el grid completo) ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">reales</span></h2>'
)

GALLERY_PATTERN = re.compile(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    re.S
)
assert GALLERY_PATTERN.search(h), 'no se encontro el grid de galeria'
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Ambiente cálido del spa" data-en="Warm spa ambiance">Ambiente cálido del spa</span><img src="assets/raw/bk-7.jpg" alt="Clienta relajada durante un tratamiento en ambiente cálido con luz ámbar" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Resultado de labios" data-en="Lip treatment result">Resultado de labios</span><img src="assets/raw/bk-10.jpg" alt="Comparación antes y después de un tratamiento de labios" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Antes y después de pestañas" data-en="Lash before &amp; after">Antes y después de pestañas</span><img src="assets/raw/bk-13.jpg" alt="Comparación antes y después de pestañas y cejas" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Aplicación profesional" data-en="Professional application">Aplicación profesional</span><img src="assets/raw/bk-14.jpg" alt="Aplicación de tratamiento de pestañas o cejas con herramientas profesionales de cerca" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Mirada relajada" data-en="Relaxed finished look">Mirada relajada</span><img src="assets/raw/bk-15.jpg" alt="Resultado terminado de pestañas y cejas con mirada relajada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Tratamiento facial en proceso" data-en="Facial treatment in progress">Tratamiento facial en proceso</span><img src="assets/raw/bk-6.jpg" alt="Esteticista realizando un tratamiento facial profesional en camilla" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = GALLERY_PATTERN.sub(NEW_GALLERY, h, count=1)

# ---------- 16. OPINIONES ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What our">What our</span> <span class="text-shine" data-es="nuestras clientas" data-en="clients say">clients say</span></h2>'
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 35 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 35 verified reviews on Booksy">5.0 de 5 · 35 reseñas verificadas en Booksy</span></p>'
)
OLD_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
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
        </figure>
      </div>'''
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Just had an AMAZING facial!! I have always had problems with acne and my skin feels so healthy and smooth right now. I'll definitely be making another appointment soon. 😁"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tonya S…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente servicio, buena atencion, tomo su tiempo para explicar todo el procedimiento, ayudar a escoger el color mas conveniente, explicar y enviar instrucciones de cuidado, el lugar estaba nitido, todo sanitado, recomendado 100%"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Keity C…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing job! My first time and she handled me with care. Highly recommend!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Amber B…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>'''
rep(OLD_REVIEWS, NEW_REVIEWS)
rep(
    '<a href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 35 reseñas en Booksy" data-en="Read all 35 reviews on Booksy">Leer las 35 reseñas en Booksy</a>'
)

# ---------- 17. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Tampa</span></h2>'
)
OLD_UBICACION_CARDS = '''<div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://instagram.com/Ar_bella_yudyth" target="_blank" rel="noopener">@Ar_bella_yudyth</a>
            </div>
          </div>
        </div>'''
NEW_UBICACION_CARDS = '''<div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4023 W Waters Ave, Tampa, FL 33614</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4023+W+Waters+Ave,+Tampa,+FL+33614" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Horario</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a Sábado: 9:00 AM a 8:00 PM · Domingo: 11:00 AM a 5:00 PM" data-en="Monday to Saturday: 9:00 AM to 8:00 PM · Sunday: 11:00 AM to 5:00 PM">Lunes a Sábado: 9:00 AM a 8:00 PM · Domingo: 11:00 AM a 5:00 PM</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los tratamientos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See our latest treatments and DM any questions before your appointment.">Mira los tratamientos más recientes y escribe por DM cualquier duda antes de tu cita.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://instagram.com/Ar_bella_yudyth" target="_blank" rel="noopener">@Ar_bella_yudyth</a>
            </div>
          </div>
        </div>'''
rep(OLD_UBICACION_CARDS, NEW_UBICACION_CARDS)

rep(
    '''<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>''',
    '''<iframe title="Mapa: Arbella Beauty Studio, 4023 W Waters Ave, Tampa FL"
          src="https://www.google.com/maps?q=4023+W+Waters+Ave,+Tampa,+FL+33614&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'''
)

# ---------- 18. CTA FINAL ----------
rep(
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu piel, tus cejas, tu mejor versión." data-en="Your skin, your brows, your best you.">Tu piel, tus cejas, tu mejor versión.</p>'
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima cita" data-en="Your next appointment">Tu próxima cita</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span></h2>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu facial, tus cejas o tus labios con la especialista que ya recomiendan 35 clientas en Booksy." data-en="Book online in seconds: your facial, your brows or your lips with the specialist 35 clients already recommend on Booksy.">Reserva online en segundos: tu facial, tus cejas o tus labios con la especialista que ya recomiendan 35 clientas en Booksy.</p>'
)

# ---------- 19. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Arbella Beauty Studio</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Arbella Beauty Studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />'
)
rep(
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Arbella Beauty Studio</span>'
)
rep(
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Day spa en Tampa, FL. Atención con cita previa." data-en="Day spa in Tampa, FL. By appointment only.">Day spa en Tampa, FL. Atención con cita previa.</p>'
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>4023 W Waters Ave, Tampa, FL 33614</p>'
)
rep(
    '<p><a href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://booksy.com/en-us/1466319_arbella-beauty-estudio_wellness-day-spa_15761_tampa" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>'
)
rep(
    '<p><a href="https://instagram.com/Ar_bella_yudyth" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @Ar_bella_yudyth</a></p>',
    '<p><a href="https://instagram.com/Ar_bella_yudyth" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · @Ar_bella_yudyth</a></p>'
)
rep(
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Arbella Beauty Studio.</p>'
)

# ---------- 20. JS: idioma por defecto ES (negocio hispano) ----------
rep(
    "applyLang(lang === 'es' ? 'es' : 'en');",
    "applyLang(lang === 'en' ? 'en' : 'es');"
)

# ---------- 21. Verificacion de residuos de logo.jpg / hero-1 / about-2 (antes de tocar colores) ----------
assert 'logo.jpg' not in h, 'quedo una referencia a logo.jpg sin reemplazar'
assert 'hero-1.jpg' not in h, 'quedo una referencia a hero-1.jpg sin reemplazar'
assert 'about-2.jpg' not in h, 'quedo una referencia a about-2.jpg sin reemplazar'
assert 'Lash Bloom' not in h
assert 'Yesi' not in h
assert 'West Palm Beach' not in h
assert '519855' not in h
assert 'Cresthaven' not in h

# ---------- 22. Proteger el badge Merktop y aplicar la paleta (rotacion de matiz) ----------
# Se hace AL FINAL, sobre el documento ya completo: asi cubre todos los hex/rgba del
# archivo (incluidas las secciones nuevas) sin que los anchors de contenido de arriba
# se rompan por valores de color ya rotados.
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m, 'no se encontro el bloque .merktop-badge'
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# base plum-pink #a04a72 (hue ~332) -> HUE_SHIFT 310 -> hue ~282, lavanda-mauve suave (spa/calma)
HUE_SHIFT = 310.0


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

open(PATH, 'w', encoding='utf-8').write(h)
print('build OK:', PATH)
