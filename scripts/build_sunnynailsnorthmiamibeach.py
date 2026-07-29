#!/usr/bin/env python3
"""Build de Sunny Nails (sunny-nails-north-miami-beach) por transformacion anclada desde
templates/light-v2/index.html. Metodo: SKELETONS-V2.md. Cada rep() hace assert de que el
ancla exista antes de reemplazar.
"""
import os
import re

SRC = 'templates/light-v2/index.html'
OUT = 'output/sunny-nails-north-miami-beach/index.html'

h = open(SRC, encoding='utf-8').read()


def rep(a, b, n=None):
    global h
    assert a in h, 'NO ENCONTRADO: ' + a[:160]
    if n is not None:
        c = h.count(a)
        assert c == n, f'count esperado {n}, encontrado {c}: {a[:100]}'
    h = h.replace(a, b)


def rep_regex(pattern, replacement, n=1, flags=re.S):
    global h
    matches = re.findall(pattern, h, flags=flags)
    assert len(matches) == n, f'regex matches {len(matches)} esperado {n}: {pattern[:100]}'
    h = re.sub(pattern, replacement, h, flags=flags)


BOOKSY = 'https://booksy.com/en-us/1237239_sunny-nails_nail-salon_15892_north-miami-beach'
IG_URL = 'https://www.instagram.com/sunny_nails_by_mairi/'
IG_HANDLE = '@sunny_nails_by_mairi'

# ============================================================
# 1. PALETA: dusty powder blue sobre crema calida (madera + cesped
# artificial + letrero dorado del local real). NO reutiliza coral fairy,
# caramelo, esmeralda, teal acero, violeta dark, rosa dark ni el dorado
# puro de otros sites (el dorado queda SOLO en el badge Merktop).
# ============================================================
HEX_PAIRS = [
    ('#a04a72', '#3d6a86'),  # accent-deep
    ('#5c2140', '#16303e'),  # btn-3d "sole" / book-float shadow (mas oscuro)
    ('#f0bed7', '#aed3e0'),  # dark-band light-blue family (5x)
    ('#faf2f6', '#faf7f0'),  # bg / dark-band ink (cream calido)
    ('#c47a9c', '#6f97ad'),  # accent-mid
    ('#8a5573', '#35617a'),  # dark-band btn "sole"
    ('#f3e0ea', '#e3edf1'),  # bg-2 / accent-soft
    ('#d9a8c2', '#8fb9cc'),  # orb-b / dark-band text-shine stop3
    ('#7d3457', '#24455a'),  # btn-3d gradient bottom / scroll-progress mid
    ('#5f2c48', '#1c3a4a'),  # text-shine deep / step-num deep
    ('#33222c', '#2b2925'),  # ink (neutro calido)
    ('#fbf3f8', '#f4f9fb'),  # tile-cap text
    ('#fbeff5', '#e7f1f5'),  # dark-band btn-3d stop1
    ('#f8dfeb', '#cfe6ee'),  # dark-band text-shine stop2
    ('#f6f1ea', '#f7f2e6'),  # theme-color meta
    ('#f2d5e3', '#cfe4ec'),  # orb-a
    ('#f2cfe0', '#bfdce8'),  # dark-band text-shine last
    ('#efd0e0', '#cfe2ea'),  # dark-band btn-3d stop2
    ('#e5c1d4', '#bcdbe6'),  # orb-c
    ('#dc9dbe', '#4f7f97'),  # scroll-progress last
    ('#d3a2bc', '#9cc4d6'),  # dark-band btn-3d stop3
    ('#c9789f', '#6a9bb5'),  # text-shine stop2
    ('#b25a85', '#2f5872'),  # text-shine last stop
    ('#2a1722', '#111f27'),  # cta-final bg start
    ('#1f0f18', '#0c161c'),  # cta-final bg end
    ('#1c0f16', '#0d1a20'),  # footer bg
]
for a, b in HEX_PAIRS:
    rep(a, b)

RGBA_PAIRS = [
    ('rgba(160,74,114,', 'rgba(61,106,134,'),   # accent-deep alpha
    ('rgba(51,34,44,', 'rgba(43,41,37,'),       # ink alpha
    ('rgba(70,25,50,', 'rgba(22,48,62,'),       # btn-3d inset shadow
    ('rgba(240,190,215,', 'rgba(174,211,224,'),  # dark-band pink->blue alpha
    ('rgba(253,246,250,', 'rgba(250,248,243,'),  # surface / glass-hover bg
    ('rgba(125,52,87,', 'rgba(36,69,90,'),       # dark-band btn shadow alpha
    ('rgba(250,242,246,', 'rgba(250,247,240,'),  # nav scrolled bg / dark-band ink alpha
    ('rgba(233,205,186,', 'rgba(158,196,210,'),  # dark-band accent-ghost
    ('rgba(185,138,128,', 'rgba(120,168,186,'),  # dark-band orb-b
]
for a, b in RGBA_PAIRS:
    rep(a, b)

# ============================================================
# 2. GLOBALES: Booksy URL, IG handle/URL, logo
# ============================================================
rep('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach', BOOKSY)
rep('https://www.instagram.com/_lashbloom/', IG_URL)
rep('@_lashbloom', IG_HANDLE)

# ============================================================
# 3. HEAD: title, meta, og, favicon, JSON-LD, theme-color
# ============================================================
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Sunny Nails · Nail Salon in North Miami Beach, FL | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Sunny Nails by Mairi, North Miami Beach FL: gel, acrylic and Russian hard gel manicures, spa pedicures and custom nail art. Perfect 5.0 across 51 Booksy reviews. Book online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Sunny Nails · Nail Salon in North Miami Beach, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gel, acrylic and Russian manicures. Spa pedicures. 5.0 on Booksy. Book online." />',
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
    "name": "Sunny Nails",
    "description": "Sunny Nails is a nail salon dedicated to enhancing your beauty through high-quality manicure, pedicure, and nail care services in North Miami Beach, FL. We speak both English and Spanish.",
    "telephone": "+1-786-712-4679",
    "address": { "@type": "PostalAddress", "streetAddress": "16215 Biscayne Blvd, Suite 108", "addressLocality": "North Miami Beach", "addressRegion": "FL", "postalCode": "33160", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.94213, "longitude": -80.1232 },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "10:00", "closes": "19:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "15:00" }
    ],
    "sameAs": ["https://booksy.com/en-us/1237239_sunny-nails_nail-salon_15892_north-miami-beach", "https://www.instagram.com/sunny_nails_by_mairi/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "51", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "85", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Russian Hard Gel Manicure" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Sunny Spa Pedicura" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Set de Acrilico" } },
      { "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel X + Gel Pedicure" } }
    ] }
  }
  </script>'''
rep(JSON_LD_OLD, JSON_LD_NEW, n=1)

# ============================================================
# 4. IDIOMA: principal = en (queda igual que el esqueleto, no se toca
# el default de applyLang ni el <html lang>)
# ============================================================

# ============================================================
# 5. PRELOADER
# ============================================================
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">SN</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Sunny Nails</span>')

# ============================================================
# 6. NAV (brand + logo alt)
# ============================================================
rep(
    '''<a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(61,106,134,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>
      </a>''',
    '''<a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/logo.jpg" alt="Sunny Nails" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(61,106,134,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Sunny <span class="text-[color:var(--accent-deep)]">Nails</span></span>
      </a>''',
)

# ============================================================
# 7. HERO
# ============================================================
rep(
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="North Miami Beach, FL · Nail Salon" data-en="North Miami Beach, FL · Nail Salon">North Miami Beach, FL · Nail Salon</p>',
)
rep(
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Uñas hechas con sol y cariño." data-en="Nails made with sunshine and care.">Nails made with sunshine and care.</p>',
)
rep(
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>
        </h1>''',
    '''<h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Manicures en gel, acrílico y" data-en="Gel, acrylic and Russian">Gel, acrylic and Russian</span><br /><span data-es="al estilo ruso, hechos para " data-en="manicures, made to ">manicures, made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>
        </h1>''',
)
rep(
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Estudio de una sola artista sobre Biscayne Blvd, en North Miami Beach: Mairi pinta a mano cada manicure en gel, acrílico y Russian hard gel, además de pedicures spa y nail art personalizado. Se habla inglés y español, y su calificación es un 5.0 perfecto en 51 reseñas de Booksy." data-en="One-artist studio on Biscayne Blvd in North Miami Beach: Mairi hand-paints every gel, acrylic and Russian hard gel manicure, plus spa pedicures and custom nail art. English and Spanish spoken, with a perfect 5.0 across 51 Booksy reviews.">One-artist studio on Biscayne Blvd in North Miami Beach: Mairi hand-paints every gel, acrylic and Russian hard gel manicure, plus spa pedicures and custom nail art. English and Spanish spoken, with a perfect 5.0 across 51 Booksy reviews.</p>',
)
rep(
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 51 reseñas en Booksy" data-en="5.0 · 51 reviews on Booksy">5.0 · 51 reviews on Booksy</span>',
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
            <img src="assets/raw/hero.jpg" alt="Elegant French manicure with rings, done at Sunny Nails by Mairi" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Russian Hard Gel Manicure</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$85+ · 90min" data-en="$85+ · 90min">$85+ · 90min</p>
          </div>''',
)

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep(
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="51">51</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Gel <span class="text-shine">&amp;</span> Acrylic</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Manicure · Pedicure · Nail art" data-en="Manicure · Pedicure · Nail art">Manicure · Pedicure · Nail art</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl text-shine">EN / ES</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Se habla inglés y español" data-en="English and Spanish spoken">English and Spanish spoken</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">North Miami Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">16215 Biscayne Blvd</p></div>',
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
    '''<span class="marquee-word">Russian Manicure</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Gel X</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Acrylic Full Set</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Spa Pedicure</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Nail Art</span><span class="marquee-star">✦</span>
        <span class="marquee-word">North Miami Beach, FL</span><span class="marquee-star">✦</span>''',
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
          <img src="assets/raw/about-1.jpg" alt="Delicate nude manicure with a gold ring, Sunny Nails by Mairi" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-2.jpg" alt="Client hands with a fresh French manicure in front of the Sunny Nails by Mairi sign" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>''',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un estudio de una" data-en="A one-artist studio">A one-artist studio</span><br /><span class="text-shine" data-es="sola artista" data-en="made by hand">made by hand</span></h2>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Sunny Nails es el estudio de una sola artista sobre Biscayne Blvd: Mairi. Cada manicure en gel, acrílico o Russian hard gel se trabaja a mano, en inglés o español, dentro de un suite luminoso con pared verde viva y acentos dorados." data-en="Sunny Nails is the studio of one nail artist on Biscayne Blvd: Mairi. Every gel, acrylic or Russian hard gel manicure is shaped and painted by hand, in English or Spanish, inside a bright suite with a living green wall and gold accents.">Sunny Nails is the studio of one nail artist on Biscayne Blvd: Mairi. Every gel, acrylic or Russian hard gel manicure is shaped and painted by hand, in English or Spanish, inside a bright suite with a living green wall and gold accents.</p>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="El resultado: un 5.0 perfecto en 51 reseñas verificadas en Booksy, con clientas que la describen como atenta, profesional y encantadora, cita tras cita." data-en="The result: a perfect 5.0 across 51 verified Booksy reviews, with regulars describing her as attentive, professional and kind, appointment after appointment.">The result: a perfect 5.0 across 51 verified Booksy reviews, with regulars describing her as attentive, professional and kind, appointment after appointment.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="51">51</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(61,106,134,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>
          </div>''',
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/logo.jpg" alt="Mairi, Sunny Nails" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(61,106,134,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Mairim · <span class="text-[color:var(--ink-40)]" data-es="Artista de uñas" data-en="Nail artist">Nail artist</span></span>
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
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu gel, acrílico, pedicure o combo en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your gel, acrylic, pedicure or combo on Booksy with clear price and duration, and confirm instantly.">Pick your gel, acrylic, pedicure or combo on Booksy with clear price and duration, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Preparación" data-en="Shape &amp; prep">Shape &amp; prep</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cutícula, limado y forma: la base perfecta para que el gel, el acrílico o el dip powder dure semanas sin levantarse." data-en="Cuticle care, filing and shaping set the base so gel, acrylic or dip powder lasts for weeks without lifting.">Cuticle care, filing and shaping set the base so gel, acrylic or dip powder lasts for weeks without lifting.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Color y diseño" data-en="Color &amp; design">Color &amp; design</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges color, punta francesa, acabado Russian gel o nail art personalizado, pintado a mano uña por uña." data-en="Choose your color, French tip, Russian gel finish or custom nail art, hand-painted nail by nail.">Choose your color, French tip, Russian gel finish or custom nail art, hand-painted nail by nail.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Salida perfecta" data-en="Finishing touch">Finishing touch</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu manicure o pedicure sellado y curado, y tu próxima cita agendada si la quieres." data-en="You leave with a sealed, fully cured manicure or pedicure, and your next appointment booked if you want one.">You leave with a sealed, fully cured manicure or pedicure, and your next appointment booked if you want one.</p>',
)

# ============================================================
# 12. SERVICIOS: subtitulo + grid destacados (regex) + nota + menu completo
# ============================================================
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Sunny Nails en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Sunny Nails on Booksy. Booking confirms instantly.">Prices and durations as published by Sunny Nails on Booksy. Booking confirms instantly.</p>',
)

SERVICES_GRID_NEW = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Técnica insignia" data-en="Signature technique">Signature technique</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Russian Hard Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La especialidad de Mairi: un manicure en gel duro de larga duración con el acabado Russian impecable, cutícula incluida." data-en="Mairi's specialty: a long-lasting hard gel manicure with the flawless Russian finish, cuticle work included.">Mairi's specialty: a long-lasting hard gel manicure with the flawless Russian finish, cuticle work included.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">90min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(61,106,134,0.4); box-shadow: 0 18px 50px rgba(43,41,37,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Sunny Spa Pedicura</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El pedicure spa propio del salón, con remojo, exfoliación y masaje, terminado en esmalte regular o gel." data-en="The salon's own spa pedicure with soak, scrub and massage, finished in regular or gel polish.">The salon's own spa pedicure with soak, scrub and massage, finished in regular or gel polish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Larga duración" data-en="Long lasting">Long lasting</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Full Set de Acrílico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de acrílico esculpido en el largo que prefieras, de corto y natural a extra largo." data-en="Sculpted acrylic full set in your choice of length, from short and natural to extra long.">Sculpted acrylic full set in your choice of length, from short and natural to extra long.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Combo popular" data-en="Popular combo">Popular combo</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel X + Gel Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manos y pies en una sola visita: manicure Gel X junto a un pedicure en gel, el combo más pedido del estudio." data-en="Hands and feet in one visit: Gel X manicure paired with a gel pedicure, the studio's most popular combo.">Hands and feet in one visit: Gel X manicure paired with a gel pedicure, the studio's most popular combo.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$130+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 5min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
rep_regex(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    SERVICES_GRID_NEW,
    n=1,
)


def row(name, price):
    return (f'<div class="flex items-baseline justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)]">'
            f'<span class="font-light">{name}</span>'
            f'<span class="text-[color:var(--ink-60)] whitespace-nowrap">{price}</span></div>')


CATEGORIES = [
    ('GEL', 'GEL', [
        ('Russian hard gel manicure/ natural nails', '$85+ · 1h 30min'),
        ('Gel x', '$75+ · 1h 15min'),
        ('Builder gel full set', '$80+ · 1h 30min'),
        ('Poly gel fill', '$70+ · 1h 15min'),
        ('Builder gel fill', '$75+ · 1h 30min'),
        ('Polly gel full set', '$80+ · 1h 30min'),
        ('Russian hard gel manicure w/extension', '$110 · 2h'),
        ('Gel manicura', '$40 · 45min'),
        ('Rifill hard gel (no Russian manicure)', '$75+ · 1h'),
        ('Polish change on Gel', '$30 · 20min'),
    ]),
    ('Pedicuras', 'Pedicures', [
        ('Acrylic of feet', '$80+ · 1h 15min'),
        ('Pedicure regular', '$40 · 45min'),
        ('Russian Gel pedicure', '$100 · 1h 30min'),
        ('Gel pedicura', '$55 · 50min'),
        ('Sunny spa pedicura', '$70+ · 1h 15min'),
        ('Spa pedicura', '$60+ · 1h'),
    ]),
    ('Acrílico', 'Acrylic', [
        ('Full Set de acrílico', '$70+ · 1h 15min'),
        ('Rifill acrylic', '$70+ · 1h'),
    ]),
    ('Dipping Powder', 'Dipping Powder', [
        ('Dip powder tips', '$75+ · 1h'),
        ('Dip Natural nails', '$65+ · 1h'),
    ]),
    ('Combos', 'Combos', [
        ('Gel x + pedicure regular', '$115+ · 2h'),
        ('Gel x + Gel pedicure', '$130+ · 2h 5min'),
        ('Regular hands and feet', '$65 · 1h 15min'),
        ('Gel Hands and feet', '$90 · 1h 35min'),
        ('Dip powder and pedicura regular', '$105+ · 1h 45min'),
        ('Dip powder and gel pedicura', '$120+ · 1h 50min'),
        ('Nails gel pedicure regular', '$80 · 1h 30min'),
    ]),
    ('Otros', 'Others', [
        ('Regular manicure', '$25 · 30min'),
        ('Reparación de Uñas', '$15 · 15min'),
        ('French design', '$20 · 20min'),
        ('Nails art', '$20+ · 20min'),
        ('Polish change regular hands', '$20 · 15min'),
    ]),
]

cat_blocks = []
for es_label, en_label, services in CATEGORIES:
    rows_html = '\n          '.join(row(name, price) for name, price in services)
    cat_blocks.append(
        f'''<div>
          <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="{es_label}" data-en="{en_label}">{en_label}</p>
          <div class="grid sm:grid-cols-2 gap-x-8 gap-y-0 text-sm">
          {rows_html}
          </div>
        </div>'''
    )
menu_categories_html = '\n        '.join(cat_blocks)

MENU_COMPLETO = f'''<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Menú completo de 32 servicios y disponibilidad en Booksy." data-en="Full menu of 32 services and availability on Booksy.">Full menu of 32 services and availability on Booksy.</span></p>
      <div class="reveal glass rounded-3xl p-6 sm:p-8 mt-8 space-y-8" style="transition-delay:120ms">
        {menu_categories_html}
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
    f'''<a href="{IG_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          {IG_HANDLE}
        </a>''',
    f'''<a href="{IG_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          {IG_HANDLE}
        </a>''',
    n=1,
)

GALLERY_GRID_NEW = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Cerezas y francesa" data-en="Cherry French tips">Cherry French tips</span><img src="assets/raw/gallery-wide.jpg" alt="Cherry nail art French tips with the Miami skyline in the background" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Almendra nude larga" data-en="Long almond nude">Long almond nude</span><img src="assets/raw/gallery-1.jpg" alt="Long almond nude acrylic nails with a ring" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Mariposas a mano" data-en="Hand-painted butterflies">Hand-painted butterflies</span><img src="assets/raw/gallery-2.jpg" alt="Hand-painted butterfly nail art against a green wall" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Contorno dorado" data-en="Gold chrome outline">Gold chrome outline</span><img src="assets/raw/gallery-3.jpg" alt="Nude nails with a gold chrome outline design" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Lunares y estrellas" data-en="Polka dots &amp; stars">Polka dots &amp; stars</span><img src="assets/raw/gallery-4.jpg" alt="Nail art with polka dots and stars, palm trees in the background" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Francesa con lunares" data-en="Dotted French tips">Dotted French tips</span><img src="assets/raw/gallery-5.jpg" alt="French manicure with white polka dot accents on both hands" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
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
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 51 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 51 verified reviews on Booksy">5.0 out of 5 · 51 verified reviews on Booksy</span></p>',
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Absolute amazing, Mairi rescued me from a disaster I had on my nails, she is super attentive to detail and kind. Will come again when I come visit Miami! Thank you!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Paula G.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I love my nails! Mairim did an amazing job by listening and bringing to life how I envision my nails! Highly recommend"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Roxanna N.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mairim provides a professional and reliable service. Highly recommend"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rosaura L.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>'''
rep(REVIEWS_OLD, REVIEWS_NEW, n=1)

rep(
    f'<a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    f'<a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 51 reseñas en Booksy" data-en="Read all 51 reviews on Booksy">Read all 51 reviews on Booksy</a>',
)

# ============================================================
# 15. UBICACION
# ============================================================
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">North Miami Beach</span></h2>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(61,106,134,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">16215 Biscayne Blvd, Suite 108, North Miami Beach, FL 33160</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(61,106,134,0.4)]" href="https://www.google.com/maps?q=16215+Biscayne+Blvd,+North+Miami+Beach,+FL+33160" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Lunes a viernes, 10:00 am a 7:00 pm. Sábados, 10:00 am a 3:00 pm. Estacionamiento y Wi-Fi en el local." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Monday to Friday, 10:00 am to 7:00 pm. Saturday, 10:00 am to 3:00 pm. Parking and Wi-Fi on site.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Monday to Friday, 10:00 am to 7:00 pm. Saturday, 10:00 am to 3:00 pm. Parking and Wi-Fi on site.</p>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los diseños más recientes de Mairi y escribe por DM cualquier duda antes de tu cita." data-en="See Mairi\'s latest designs and DM any questions before your appointment.">See Mairi\'s latest designs and DM any questions before your appointment.</p>',
)
rep(
    '''<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"''',
    '''<iframe title="Mapa: Sunny Nails, 16215 Biscayne Blvd, North Miami Beach FL"
          src="https://www.google.com/maps?q=16215+Biscayne+Blvd,+North+Miami+Beach,+FL+33160&output=embed"''',
)

# ============================================================
# 16. CTA FINAL
# ============================================================
rep(
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Uñas hechas con sol y cariño." data-en="Nails made with sunshine and care.">Nails made with sunshine and care.</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo manicure" data-en="Your next manicure">Your next manicure</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu gel, acrílico, Russian manicure o el pedicure que ya te toca." data-en="Book online in seconds: your gel, acrylic, Russian manicure or the pedicure you are due for.">Book online in seconds: your gel, acrylic, Russian manicure or the pedicure you are due for.</p>',
)

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Sunny Nails</span>')
rep(
    '''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(174,211,224,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/raw/logo.jpg" alt="Sunny Nails" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(174,211,224,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Sunny Nails</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de una sola artista en North Miami Beach, FL. Atención con cita previa." data-en="One-artist nail studio in North Miami Beach, FL. By appointment only.">One-artist nail studio in North Miami Beach, FL. By appointment only.</p>''',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>16215 Biscayne Blvd, Suite 108, North Miami Beach, FL 33160</p>\n        <p><a href="tel:+17867124679">(786) 712-4679</a></p>',
)
rep(
    f'<p><a href="{BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#aed3e0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    f'<p><a href="{BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#aed3e0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
)
rep(
    f'<p><a href="{IG_URL}" target="_blank" rel="noopener" class="hover:text-[#aed3e0]">Instagram · {IG_HANDLE}</a></p>',
    f'<p><a href="{IG_URL}" target="_blank" rel="noopener" class="hover:text-[#aed3e0]">Instagram · {IG_HANDLE}</a></p>',
)
rep(
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Sunny Nails.</p>',
)

# ============================================================
# Guardar
# ============================================================
os.makedirs('output/sunny-nails-north-miami-beach', exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(h)
print('build OK ->', OUT, len(h), 'bytes')
