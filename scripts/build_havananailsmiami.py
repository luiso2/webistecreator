#!/usr/bin/env python3
"""Build de Havana Nails (havananailsmiami) por transformacion anclada desde templates/light-v2.
Metodo: SKELETONS-V2.md. Cada rep() hace assert de que el ancla exista antes de reemplazar.
"""
import re

SRC = 'templates/light-v2/index.html'
OUT = 'output/havananailsmiami/index.html'

h = open(SRC, encoding='utf-8').read()


def rep(a, b, n=None):
    global h
    assert a in h, 'NO ENCONTRADO: ' + a[:140]
    if n is not None:
        c = h.count(a)
        assert c == n, f'count esperado {n}, encontrado {c}: {a[:100]}'
    h = h.replace(a, b)


def rep_regex(pattern, replacement, n=1, flags=re.S):
    global h
    matches = re.findall(pattern, h, flags=flags)
    assert len(matches) == n, f'regex matches {len(matches)} esperado {n}: {pattern[:100]}'
    h = re.sub(pattern, replacement, h, flags=flags)


# ============================================================
# 1. PALETA (pares hex). Havana Nails: rosa rosewood/blush calido.
# NO tocar el badge Merktop: #D4A84B, rgba(212,168,75,*), #f4eee2,
# rgba(244,238,226,*), rgba(36,28,20,*), rgba(27,21,14,*).
# ============================================================
HEX_PAIRS = [
    ('#a04a72', '#b23f52'),  # accent-deep
    ('#5c2140', '#6e2333'),  # btn-3d / book-float shadow
    ('#f0bed7', '#f3c2c9'),  # dark-band pink family
    ('#faf2f6', '#fdf2ef'),  # bg
    ('#c47a9c', '#d9808f'),  # accent-mid
    ('#8a5573', '#8f5850'),  # dark-band btn shadow
    ('#f3e0ea', '#f7e0dd'),  # bg-2 / accent-soft
    ('#d9a8c2', '#e0a8ac'),  # orb-b / dark-band text-shine
    ('#7d3457', '#8a2e3f'),  # btn-3d gradient bottom / scroll-progress
    ('#5f2c48', '#6b2430'),  # text-shine deep / step-num deep
    ('#33222c', '#34201c'),  # ink
    ('#fbf3f8', '#fdf1ee'),  # tile-cap text
    ('#fbeff5', '#fdeeec'),  # dark-band btn-3d stop1
    ('#f8dfeb', '#fbe3e0'),  # dark-band text-shine stop2
    ('#f6f1ea', '#fdf2ef'),  # theme-color meta
    ('#f2d5e3', '#f5d9d5'),  # orb-a
    ('#f2cfe0', '#f0d0ce'),  # dark-band text-shine last
    ('#efd0e0', '#f0cdc9'),  # dark-band btn-3d stop2
    ('#e5c1d4', '#edc4bf'),  # orb-c
    ('#dc9dbe', '#e0a0a8'),  # scroll-progress last
    ('#d3a2bc', '#d6a19a'),  # dark-band btn-3d stop3
    ('#c9789f', '#dd8fa0'),  # text-shine stop2
    ('#b25a85', '#c15468'),  # text-shine last stop
    ('#2a1722', '#2b1613'),  # cta-final bg start
    ('#1f0f18', '#1d0e0c'),  # cta-final bg end
    ('#1c0f16', '#1a0d0b'),  # footer bg
]
for a, b in HEX_PAIRS:
    rep(a, b)

RGBA_PAIRS = [
    ('rgba(160,74,114,', 'rgba(178,63,82,'),
    ('rgba(51,34,44,', 'rgba(52,32,28,'),
    ('rgba(70,25,50,', 'rgba(90,30,42,'),
    ('rgba(240,190,215,', 'rgba(243,194,201,'),
    ('rgba(125,52,87,', 'rgba(139,47,63,'),
    ('rgba(253,246,250,', 'rgba(253,242,239,'),
    ('rgba(250,242,246,', 'rgba(253,242,239,'),
    ('rgba(233,205,186,', 'rgba(224,168,172,'),
    ('rgba(185,138,128,', 'rgba(200,140,130,'),
    ('rgba(40,16,30,', 'rgba(42,18,14,'),
]
for a, b in RGBA_PAIRS:
    rep(a, b)

# ============================================================
# 2. GLOBALES: Booksy URL, IG handle/URL
# ============================================================
rep(
    'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
    'https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami',
)
rep('_lashbloom', 'anynails82')  # cubre URL de IG (.../instagram.com/anynails82/) y @anynails82

# ============================================================
# 3. HEAD: title, meta, og, favicon, JSON-LD, theme-color
# ============================================================
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Havana Nails · Nail Salon en Flagami, Miami, FL | 5.0 en Booksy</title>',
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Havana Nails, salon de unas boutique en Flagami, Miami: gel manicure, gel pedicure, builder gel y disenos de unas personalizados. 5.0 de calificacion con 82 resenas en Booksy. Reserva en linea." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Havana Nails · Nail Salon en Flagami, Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel manicure, pedicure y nail art. 5.0 en Booksy. Reserva en linea." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/hero.jpg" />',
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
)

JSON_LD_OLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
JSON_LD_NEW = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Havana Nails",
    "description": "Salon de unas boutique en Flagami, Miami, FL: gel manicure, gel pedicure, builder gel y disenos de unas personalizados.",
    "address": { "@type": "PostalAddress", "streetAddress": "811 NW 43rd Ave, Apt 433", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33126", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.78019, "longitude": -80.26588 },
    "sameAs": ["https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami", "https://www.instagram.com/anynails82/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "82", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de unas", "itemListElement": [
      { "@type": "Offer", "price": "35", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicure" } },
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicura +Gel Pedicura" } },
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure Jelly Spa" } },
      { "@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Rubber Base Manicure" } }
    ] }
  }
  </script>'''
rep(JSON_LD_OLD, JSON_LD_NEW, n=1)

# ============================================================
# 4. IDIOMA: principal = es
# ============================================================
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep(
    "applyLang(lang === 'es' ? 'es' : 'en');",
    "applyLang(lang === 'en' ? 'en' : 'es');",
)

# ============================================================
# 5. PRELOADER
# ============================================================
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">HN</span>')
rep(
    '<span class="pre-word">Lash Bloom</span>',
    '<span class="pre-word">Havana Nails</span>',
)

# ============================================================
# 6. NAV (brand + logo alt)
# ============================================================
rep(
    '''<a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(178,63,82,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>
      </a>''',
    '''<a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/logo.jpg" alt="Havana Nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(178,63,82,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Havana <span class="text-[color:var(--accent-deep)]">Nails</span></span>
      </a>''',
)

# ============================================================
# 7. HERO
# ============================================================
rep(
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Miami, FL · Flagami · Nail Salon" data-en="Miami, FL · Flagami · Nail Salon">Miami, FL · Flagami · Nail Salon</p>',
)
rep(
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Uñas hechas a mano, diseño por diseño." data-en="Nails made by hand, design by design.">Nails made by hand, design by design.</p>',
)
rep(
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>
        </h1>''',
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Manicure y pedicure en gel," data-en="Gel manicures and pedicures,">Gel manicures and pedicures,</span><br /><span data-es="pensados para " data-en="made to ">made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>
        </h1>''',
)
rep(
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Gel manicure, gel pedicure, builder gel, rubber base y diseños de uñas personalizados en un estudio boutique en Flagami, a minutos del aeropuerto de Miami. Reserva en línea con confirmación inmediata y un 5.0 perfecto en 82 reseñas de Booksy." data-en="Gel manicures, gel pedicures, builder gel, rubber base and custom nail art at a boutique studio in Flagami, minutes from Miami International Airport. Book online with instant confirmation and a perfect 5.0 across 82 Booksy reviews.">Gel manicures, gel pedicures, builder gel, rubber base and custom nail art at a boutique studio in Flagami, minutes from Miami International Airport. Book online with instant confirmation and a perfect 5.0 across 82 Booksy reviews.</p>',
)
rep(
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 82 reseñas en Booksy" data-en="5.0 · 82 reviews on Booksy">5.0 · 82 reviews on Booksy</span>',
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
            <img src="assets/raw/hero.jpg" alt="Diseño de uñas negro y blanco geométrico hecho en Havana Nails Miami" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Gel Manicure</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$35 · 1h" data-en="$35 · 1h">$35 · 1h</p>
          </div>''',
)

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="82">82</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Builder</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicure · Pedicure · Nail art" data-en="Manicure · Pedicure · Nail art">Manicure · Pedicure · Nail art</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl text-shine">1:1</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención personalizada" data-en="Personalized attention">Personalized attention</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Flagami, Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">811 NW 43rd Ave</p></div>',
)

# ============================================================
# 9. MARQUEE (2 bloques identicos en estructura, se repiten x2 cada uno)
# ============================================================
rep(
    '''<span class="marquee-word">Classic Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Hybrid Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Volume Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Mega Volume</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Bottom Lashes</span><span class="marquee-star">✦</span>
        <span class="marquee-word">West Palm Beach, FL</span><span class="marquee-star">✦</span>''',
    '''<span class="marquee-word">Gel Manicure</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Builder Gel</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Rubber Base</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Pedicure Jelly Spa</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Polly Gel</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Miami, FL</span><span class="marquee-star">✦</span>''',
    n=4,
)

# ============================================================
# 10. LA EXPERIENCIA
# ============================================================
rep(
    '''<div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>''',
    '''<div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/exp-1.jpg" alt="Mano con manicure nude junto a una planta en Havana Nails" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/exp-2.jpg" alt="Manicure nude con vista al skyline de Miami desde Havana Nails" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>''',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un estudio boutique" data-en="A boutique studio">A boutique studio</span><br /><span class="text-shine" data-es="hecho a mano" data-en="made by hand">made by hand</span></h2>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Havana Nails es el estudio de una sola artista de uñas en Flagami: Annie Hernández. Cada set se trabaja a mano, diseño por diseño, en un salón de barrio a minutos del aeropuerto de Miami, con clientas que la describen en Booksy como profesional, talentosa y encantadora." data-en="Havana Nails is the studio of one nail artist in Flagami: Annie Hernandez. Every set is worked by hand, design by design, in a neighborhood salon minutes from Miami International Airport, with clients who describe her on Booksy as professional, talented and sweet.">Havana Nails is the studio of one nail artist in Flagami: Annie Hernandez. Every set is worked by hand, design by design, in a neighborhood salon minutes from Miami International Airport, with clients who describe her on Booksy as professional, talented and sweet.</p>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: un 5.0 perfecto en 82 reseñas verificadas en Booksy, con clientas que reservan cita tras cita en un salón donde cada mano y cada pie reciben el mismo cuidado." data-en="The result: a perfect 5.0 across 82 verified Booksy reviews, with clients who book visit after visit in a salon where every hand and every foot gets the same care.">The result: a perfect 5.0 across 82 verified Booksy reviews, with clients who book visit after visit in a salon where every hand and every foot gets the same care.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="82">82</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(178,63,82,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>
          </div>''',
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/logo.jpg" alt="Havana Nails" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(178,63,82,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Annie Hernández · <span class="text-[color:var(--ink-40)]" data-es="Artista de uñas" data-en="Nail artist">Nail artist</span></span>
          </div>''',
)

# ============================================================
# 11. EL METODO
# ============================================================
rep(
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, uña" data-en="Your visit, nail">Your visit, nail</span> <span class="text-shine" data-es="por uña" data-en="by nail">by nail</span></h2>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio de manicure, pedicure o gel en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your manicure, pedicure or gel service on Booksy with clear price and duration, and confirm instantly.">Pick your manicure, pedicure or gel service on Booksy with clear price and duration, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Preparación" data-en="Prep &amp; shape">Prep &amp; shape</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limado, forma y cutícula: la base perfecta para que el gel o el builder dure semanas sin levantarse." data-en="Filing, shape and cuticle care: the perfect base so gel or builder gel lasts for weeks without lifting.">Filing, shape and cuticle care: the perfect base so gel or builder gel lasts for weeks without lifting.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Color y diseño" data-en="Color &amp; design">Color &amp; design</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges color, gel o diseño personalizado: cada set se pinta a mano, uña por uña, en Havana Nails." data-en="Choose your color, gel or custom design: every set is hand painted, nail by nail, at Havana Nails.">Choose your color, gel or custom design: every set is hand painted, nail by nail, at Havana Nails.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Salida perfecta" data-en="Finishing touch">Finishing touch</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con manicure sellado, secado y tu próxima cita agendada si la quieres." data-en="You leave with a sealed, fully dried manicure and your next appointment booked if you want one.">You leave with a sealed, fully dried manicure and your next appointment booked if you want one.</p>',
)

# ============================================================
# 12. SERVICIOS: subtitulo + grid (regex) + nota + menu completo
# ============================================================
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Havana Nails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Havana Nails on Booksy. Booking confirms instantly.">Prices and durations as published by Havana Nails on Booksy. Booking confirms instantly.</p>',
)

SERVICES_GRID_NEW = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Efecto duradero" data-en="Long-lasting shine">Long-lasting shine</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure completo con esmaltado en gel de larga duración: brillo impecable desde el primer día." data-en="Full manicure with long-lasting gel polish: flawless shine from day one.">Full manicure with long-lasting gel polish: flawless shine from day one.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(178,63,82,0.4); box-shadow: 0 18px 50px rgba(52,32,28,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel Manicura +Gel Pedicura</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Gel manicure y gel pedicure en una sola visita: el combo favorito de las clientas de Havana Nails para manos y pies impecables." data-en="Gel manicure and gel pedicure in one visit: Havana Nails' favorite combo for flawless hands and feet.">Gel manicure and gel pedicure in one visit: Havana Nails' favorite combo for flawless hands and feet.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Manos + pies" data-en="Hands + feet">Hands + feet</p></div>
            <a href="https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Spa para pies" data-en="Pedicure spa">Pedicure spa</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Pedicure Jelly Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicure spa con tratamiento jelly, exfoliación e hidratación profunda para pies suaves y relajados." data-en="Spa pedicure with jelly treatment, exfoliation and deep hydration for soft, relaxed feet.">Spa pedicure with jelly treatment, exfoliation and deep hydration for soft, relaxed feet.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Larga duración" data-en="Long lasting">Long lasting</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Rubber Base Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Base de caucho flexible que protege la uña natural y aguanta semanas sin despegarse ni opacarse." data-en="Flexible rubber base that protects the natural nail and lasts weeks without lifting or losing shine.">Flexible rubber base that protects the natural nail and lasts weeks without lifting or losing shine.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
rep_regex(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    SERVICES_GRID_NEW,
    n=1,
)

MENU_COMPLETO = '''<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo de 11 servicios y disponibilidad en Booksy." data-en="Full menu of 11 services and availability on Booksy.">Full menu of 11 services and availability on Booksy.</span></p>
      <div class="reveal glass rounded-3xl p-6 sm:p-8 mt-8" style="transition-delay:120ms">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--accent-deep)] mb-5 text-center" data-es="Menú completo" data-en="Full menu">Menú completo</p>
        <div class="grid sm:grid-cols-2 gap-x-8 gap-y-1 text-sm">
          <div class="flex items-baseline justify-between gap-3 py-2.5 border-b border-[color:var(--accent-ghost)]"><span class="font-light">Gel Pedicure</span><span class="text-[color:var(--ink-60)] whitespace-nowrap">$35 · 1h</span></div>
          <div class="flex items-baseline justify-between gap-3 py-2.5 border-b border-[color:var(--accent-ghost)]"><span class="font-light">Builder Gel</span><span class="text-[color:var(--ink-60)] whitespace-nowrap">$70 · 1h</span></div>
          <div class="flex items-baseline justify-between gap-3 py-2.5 border-b border-[color:var(--accent-ghost)]"><span class="font-light">Polly Gel</span><span class="text-[color:var(--ink-60)] whitespace-nowrap">$70 · 1h</span></div>
          <div class="flex items-baseline justify-between gap-3 py-2.5 border-b border-[color:var(--accent-ghost)]"><span class="font-light">Apres Gel</span><span class="text-[color:var(--ink-60)] whitespace-nowrap">$60</span></div>
          <div class="flex items-baseline justify-between gap-3 py-2.5 border-b border-[color:var(--accent-ghost)]"><span class="font-light">Regular Pedicure</span><span class="text-[color:var(--ink-60)] whitespace-nowrap">$25 · 1h</span></div>
          <div class="flex items-baseline justify-between gap-3 py-2.5 border-b border-[color:var(--accent-ghost)]"><span class="font-light" data-es="Manicure Gel + Pedicure Regular" data-en="Manicure Gel + Pedicure Regular">Manicure Gel + Pedicure Regular</span><span class="text-[color:var(--ink-60)] whitespace-nowrap">$40 · 2h</span></div>
          <div class="flex items-baseline justify-between gap-3 py-2.5 sm:border-b-0 border-b border-[color:var(--accent-ghost)]"><span class="font-light">Terapia Con Parafina Manos Y Pies</span><span class="text-[color:var(--ink-60)] whitespace-nowrap">$20 · 20min</span></div>
        </div>
      </div>'''
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    MENU_COMPLETO,
    n=1,
)

# ============================================================
# 13. GALERIA
# ============================================================
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Diseños" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span></h2>',
)
rep(
    '''<a href="https://www.instagram.com/anynails82/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @anynails82
        </a>''',
    '''<a href="https://www.instagram.com/anynails82/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @anynails82
        </a>''',
    n=1,
)

GALLERY_GRID_NEW = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño floral en color" data-en="Colorful floral design">Colorful floral design</span><img src="assets/raw/gallery-wide.jpg" alt="Diseño de uñas floral en naranja y rojo hecho en Havana Nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Nail art floral" data-en="Floral nail art">Floral nail art</span><img src="assets/raw/gallery-1.jpg" alt="Manicure con arte floral blanco y dorado en Havana Nails" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Detalle de corazones" data-en="Heart detail">Heart detail</span><img src="assets/raw/gallery-2.jpg" alt="Manicure nude con detalle de corazones rojos" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Lila brillante" data-en="Glossy lilac">Glossy lilac</span><img src="assets/raw/gallery-3.jpg" alt="Manicure en gel color lila brillante" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Violeta con acento floral" data-en="Violet with floral accent">Violet with floral accent</span><img src="assets/raw/gallery-4.jpg" alt="Manicure violeta con uña de acento floral" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Azul con swirl dorado" data-en="Blue with gold swirl">Blue with gold swirl</span><img src="assets/raw/gallery-5.jpg" alt="Manicure azul brillante con diseño de swirl dorado" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
rep_regex(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    GALLERY_GRID_NEW,
    n=1,
)

# ============================================================
# 14. OPINIONES
# ============================================================
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
)
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 82 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 82 verified reviews on Booksy">5.0 out of 5 · 82 verified reviews on Booksy</span></p>',
)

REVIEWS_OLD = '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
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
        </figure>'''
REVIEWS_NEW = '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Beatiful my nails"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Baby T…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I’m supper happy they way she does my nails. She’s professional and very nice !! Very pleasing love how she does art THANK YOU 🙂"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Marlene R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"la mejor"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">lily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>'''
rep(REVIEWS_OLD, REVIEWS_NEW, n=1)

rep(
    '<a href="https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 82 reseñas en Booksy" data-en="Read all 82 reviews on Booksy">Read all 82 reviews on Booksy</a>',
)

# ============================================================
# 15. UBICACION
# ============================================================
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Flagami</span></h2>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(178,63,82,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">811 NW 43rd Ave, Apt 433, Miami, FL 33126 (Flagami)</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(178,63,82,0.4)]" href="https://www.google.com/maps?q=811+NW+43rd+Ave,+Miami,+FL+33126" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Lunes a sábado, 8:00 am a 2:00 pm." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Monday to Saturday, 8:00 am to 2:00 pm.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Monday to Saturday, 8:00 am to 2:00 pm.</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los diseños más recientes de Annie y escribe por DM cualquier duda antes de tu cita." data-en="See Annie\'s latest designs and DM any questions before your appointment.">See Annie\'s latest designs and DM any questions before your appointment.</p>',
)
rep(
    '''<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"''',
    '''<iframe title="Mapa: Havana Nails, 811 NW 43rd Ave, Miami FL"
          src="https://www.google.com/maps?q=811+NW+43rd+Ave,+Miami,+FL+33126&output=embed"''',
)

# ============================================================
# 16. CTA FINAL
# ============================================================
rep(
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Uñas hechas a mano, diseño por diseño." data-en="Nails made by hand, design by design.">Nails made by hand, design by design.</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu manicure, pedicure o el diseño personalizado que ya tienes en mente." data-en="Book online in seconds: your manicure, pedicure or the custom design you already have in mind.">Book online in seconds: your manicure, pedicure or the custom design you already have in mind.</p>',
)

# ============================================================
# 17. FOOTER
# ============================================================
rep(
    '<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Havana Nails</span>',
)
rep(
    '''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(243,194,201,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/raw/logo.jpg" alt="Havana Nails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(243,194,201,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Havana Nails</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Nail salon boutique en Flagami, Miami, FL. Atención con cita previa." data-en="Boutique nail salon in Flagami, Miami, FL. By appointment only.">Boutique nail salon in Flagami, Miami, FL. By appointment only.</p>''',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>811 NW 43rd Ave, Apt 433, Miami, FL 33126</p>',
)
rep(
    '<p><a href="https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="hover:text-[#f3c2c9]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://booksy.com/en-us/987327_havana-nails_nail-salon_15889_miami" target="_blank" rel="noopener" class="hover:text-[#f3c2c9]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
)
rep(
    '<p><a href="https://www.instagram.com/anynails82/" target="_blank" rel="noopener" class="hover:text-[#f3c2c9]">Instagram · @anynails82</a></p>',
    '<p><a href="https://www.instagram.com/anynails82/" target="_blank" rel="noopener" class="hover:text-[#f3c2c9]">Instagram · @anynails82</a></p>',
)
rep(
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Havana Nails.</p>',
)

# ============================================================
# Guardar
# ============================================================
import os
os.makedirs('output/havananailsmiami', exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(h)
print('build OK ->', OUT, len(h), 'bytes')
