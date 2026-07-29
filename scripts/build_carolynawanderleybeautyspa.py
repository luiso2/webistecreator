#!/usr/bin/env python3
"""Build anclado: Beauty Spa Carolyna Wanderley (carolynawanderleybeautyspa) desde templates/light-v2."""
import re
import shutil

SLUG = 'carolynawanderleybeautyspa'
SRC = 'templates/light-v2/index.html'
OUT = f'output/{SLUG}/index.html'

shutil.copyfile(SRC, OUT)
h = open(OUT, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'NO ENCONTRADO: ' + a[:200]
    h = h.replace(a, b, n)


def rep_all(a, b):
    global h
    assert a in h, 'NO ENCONTRADO (all): ' + a[:200]
    h = h.replace(a, b)


def block(start_marker, end_marker, new_content, label):
    global h
    i = h.index(start_marker)
    j = h.index(end_marker, i)
    assert i != -1 and j != -1, 'ANCLA ROTA: ' + label
    h = h[:i] + new_content + h[j:]


# ============================================================
# 1. PALETA: plum-pink lashbloom -> terracotta clay (nueva, no repetida)
# ============================================================
PALETTE = [
    # --- Composites PRIMERO (contienen tokens que las reglas simples de abajo tambien tocan) ---
    ('linear-gradient(110deg, #a04a72 0%, #c9789f 30%, #5f2c48 52%, #a04a72 75%, #b25a85 100%)',
     'linear-gradient(110deg, #a8574a 0%, #d2967a 30%, #6b3226 52%, #a8574a 75%, #bd6b52 100%)'),
    ('linear-gradient(180deg, #c47a9c 0%, #a04a72 48%, #7d3457 100%)',
     'linear-gradient(180deg, #c98f76 0%, #a8574a 48%, #7a3a2c 100%)'),
    ('linear-gradient(180deg, #c47a9c 0%, #a04a72 100%)', 'linear-gradient(180deg, #c98f76 0%, #a8574a 100%)'),
    ('linear-gradient(180deg, #c47a9c, #5f2c48)', 'linear-gradient(180deg, #c98f76, #6b3226)'),
    ('linear-gradient(110deg, #f0bed7 0%, #f8dfeb 30%, #d9a8c2 52%, #f0bed7 75%, #f2cfe0 100%)',
     'linear-gradient(110deg, #f3d3bf 0%, #f8e6d8 30%, #d9a184 52%, #f3d3bf 75%, #f0c8ac 100%)'),
    ('linear-gradient(180deg, #fbeff5 0%, #efd0e0 48%, #d3a2bc 100%)',
     'linear-gradient(180deg, #fbf1e9 0%, #efd7c0 48%, #d3a884 100%)'),
    ('linear-gradient(90deg, #7d3457 0%, #a04a72 45%, #dc9dbe 100%)',
     'linear-gradient(90deg, #7a3a2c 0%, #a8574a 45%, #dba58a 100%)'),
    ('rgba(240,190,215,0.14) 0%, rgba(160,74,114,0.08) 42%',
     'rgba(243,211,191,0.14) 0%, rgba(168,87,74,0.08) 42%'),
    ('linear-gradient(180deg, #2a1722 0%, #1f0f18 100%)', 'linear-gradient(180deg, #2a1a12 0%, #1f120c 100%)'),
    # --- Simples ---
    ('#faf2f6', '#faf3ec'),
    ('#f3e0ea', '#f3e3d6'),
    ('rgba(253,246,250,0.7)', 'rgba(253,247,241,0.7)'),
    ('#33222c', '#33261f'),
    ('rgba(51,34,44,0.62)', 'rgba(51,38,31,0.62)'),
    ('rgba(51,34,44,0.42)', 'rgba(51,38,31,0.42)'),
    ('#a04a72', '#a8574a'),
    ('#c47a9c', '#c98f76'),
    ('rgba(160,74,114,0.14)', 'rgba(168,87,74,0.14)'),
    ('rgba(160,74,114,0.16)', 'rgba(168,87,74,0.16)'),
    ('rgba(160,74,114,0.32)', 'rgba(168,87,74,0.32)'),
    ('rgba(160,74,114,0.08)', 'rgba(168,87,74,0.08)'),
    ('rgba(160,74,114,0.7)', 'rgba(168,87,74,0.7)'),
    ('rgba(160,74,114,0.35)', 'rgba(168,87,74,0.35)'),
    ('rgba(160,74,114,0.25)', 'rgba(168,87,74,0.25)'),
    ('rgba(160,74,114,0.5)', 'rgba(168,87,74,0.5)'),
    ('rgba(51,34,44,0.14)', 'rgba(51,38,31,0.14)'),
    ('rgba(51,34,44,0.2)', 'rgba(51,38,31,0.2)'),
    ('rgba(51,34,44,0.12)', 'rgba(51,38,31,0.12)'),
    ('rgba(51,34,44,0.1)', 'rgba(51,38,31,0.1)'),
    ('rgba(51,34,44,0.28)', 'rgba(51,38,31,0.28)'),
    ('rgba(51,34,44,0.32)', 'rgba(51,38,31,0.32)'),
    ('rgba(51,34,44,0.25)', 'rgba(51,38,31,0.25)'),
    ('rgba(51,34,44,0.35)', 'rgba(51,38,31,0.35)'),
    ('rgba(51,34,44,0.4)', 'rgba(51,38,31,0.4)'),
    ('rgba(51,34,44,0.3)', 'rgba(51,38,31,0.3)'),
    ('#f2d5e3', '#f5dcc9'),
    ('#d9a8c2', '#dba58a'),
    ('#e5c1d4', '#e8c4ab'),
    ('rgba(70,25,50,0.4)', 'rgba(70,35,25,0.4)'),
    ('rgba(70,25,50,0.45)', 'rgba(70,35,25,0.45)'),
    ('#5c2140', '#4a2318'),
    ('rgba(233,205,186,0.16)', 'rgba(230,188,163,0.16)'),
    ('rgba(240,190,215,0.16)', 'rgba(243,211,191,0.16)'),
    ('rgba(185,138,128,0.14)', 'rgba(200,140,110,0.14)'),
    ('rgba(125,52,87,0.35)', 'rgba(125,70,52,0.35)'),
    ('rgba(125,52,87,0.4)', 'rgba(125,70,52,0.4)'),
    ('#8a5573', '#8a6142'),
    ('rgba(240,190,215,0.18)', 'rgba(243,211,191,0.18)'),
    ('rgba(240,190,215,0.35)', 'rgba(243,211,191,0.35)'),
    ('rgba(240,190,215,0.7)', 'rgba(243,211,191,0.7)'),
    ('rgba(240,190,215,0.08)', 'rgba(243,211,191,0.08)'),
    ('#f0bed7', '#f3d3bf'),
    ('rgba(240,190,215,0.4)', 'rgba(243,211,191,0.4)'),
    ('rgba(40,16,30,0.62)', 'rgba(42,24,16,0.62)'),
    ('rgba(240,190,215,0.09)', 'rgba(243,211,191,0.09)'),
    ('#1c0f16', '#1c120c'),
]
for a, b in PALETTE:
    rep_all(a, b)

# theme-color meta
rep('content="#f6f1ea"', 'content="#f3e3d6"')

print('paleta OK')

# ============================================================
# 2. GLOBALES: Booksy URL, IG URL, handle, logo
# ============================================================
OLD_BOOKSY = 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'
NEW_BOOKSY = 'https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami'
rep_all(OLD_BOOKSY, NEW_BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/_lashbloom/'
NEW_IG_URL = 'https://www.instagram.com/carolynawanderley/'
rep_all(OLD_IG_URL, NEW_IG_URL)

rep_all('@_lashbloom', '@carolynawanderley')
rep_all('assets/raw/logo.jpg', 'assets/raw/bk-2.jpg')

print('globales OK')

# ============================================================
# 3. HEAD: title, meta, og, favicon, JSON-LD
# ============================================================
old_head = '''  <title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>
  <meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />
  <meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />
  <meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="assets/raw/bk-6.jpg" />
  <link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Lash Bloom LLC",
    "description": "Lash studio in West Palm Beach, FL: classic, hybrid, volume and mega volume eyelash extensions and fills.",
    "address": { "@type": "PostalAddress", "streetAddress": "4580 Cresthaven Blvd", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33415", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami", "https://www.instagram.com/carolynawanderley/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "86", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Lash services", "itemListElement": [
      { "@type": "Offer", "price": "130", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic full set" } },
      { "@type": "Offer", "price": "145", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Hybrid full set" } },
      { "@type": "Offer", "price": "155", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Volume full set" } },
      { "@type": "Offer", "price": "70", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Classic 2wk fill" } }
    ] }
  }
  </script>'''
new_head = '''  <title>Beauty Spa Carolyna Wanderley &middot; Facial &amp; Brow Studio in Miami, FL | 5.0 on Booksy</title>
  <meta name="description" content="Beauty Spa Carolyna Wanderley in Flagami, Miami FL: custom facials, dermaplaning, brow lamination and lash extensions with a perfect 5.0 across 15 Booksy reviews. Book online." />
  <meta property="og:title" content="Beauty Spa Carolyna Wanderley &middot; Facial &amp; Brow Studio in Miami, FL" />
  <meta property="og:description" content="Facials, dermaplaning, brow lamination and lash extensions. 5.0 on Booksy. Book online." />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="assets/raw/bk-5.jpg" />
  <link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Beauty Spa Carolyna Wanderley",
    "description": "Facial and beauty studio in Miami, FL (Flagami): custom facials, dermaplaning, brow lamination and tinting, and classic, hybrid, volume and mega volume lash extensions.",
    "address": { "@type": "PostalAddress", "streetAddress": "3721 NW 7th St, Suite 39", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33126", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.78085055943928, "longitude": -80.25839000000002 },
    "sameAs": ["https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami", "https://www.instagram.com/carolynawanderley/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "15", "bestRating": "5" },
    "openingHoursSpecification": [ { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "10:00", "closes": "18:00" } ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Facial, brow and lash services", "itemListElement": [
      { "@type": "Offer", "price": "77", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Skin Glow Therapy" } },
      { "@type": "Offer", "price": "119", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Collagen Lift Therapy" } },
      { "@type": "Offer", "price": "94", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Dermaplaning Skin Therapy" } },
      { "@type": "Offer", "price": "72", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brow Lamination + Tinting" } }
    ] }
  }
  </script>'''
rep(old_head, new_head)
print('head OK')

# ============================================================
# 4. NAV: wordmark
# ============================================================
rep('<img src="assets/raw/bk-2.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(168,87,74,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Beauty Spa Carolyna Wanderley" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(168,87,74,0.35)]" />')
old_nav_brand = '''        <span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>'''
new_nav_brand = '''        <span class="font-display text-xl tracking-[0.1em] uppercase">Carolyna <span class="text-[color:var(--accent-deep)]">Wanderley</span></span>'''
rep(old_nav_brand, new_nav_brand)
print('nav OK')

# ============================================================
# 5. PRELOADER
# ============================================================
block('<!-- PRELOADER DE MARCA -->', '<!-- BARRA DE PROGRESO DE SCROLL -->', '''<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">CW</span>
    <span class="pre-word">Carolyna Wanderley</span>
    <span class="pre-line"></span>
  </div>

  ''', 'preloader')
print('preloader OK')

# ============================================================
# 6. HERO
# ============================================================
new_hero = '''<!-- HERO -->
  <section id="top" class="relative min-h-screen flex items-center grain overflow-hidden pt-28 pb-16">
    <div class="glow-bg"><div class="orb orb-a" data-parallax="0.14"></div><div class="orb orb-b" data-parallax="0.09"></div><div class="orb orb-c" data-parallax="0.2"></div></div>
    <div id="heroInner" class="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Flagami, Miami, FL &middot; Estudio Facial y de Belleza" data-en="Flagami, Miami, FL &middot; Facial &amp; Beauty Studio">Flagami, Miami, FL &middot; Facial &amp; Beauty Studio</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Piel radiante, cejas perfectas, un estudio de confianza." data-en="Glowing skin, perfect brows, one trusted studio.">Glowing skin, perfect brows, one trusted studio.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Terapia facial y arte" data-en="Facial therapy and brow">Facial therapy and brow</span><br /><span data-es="de cejas, hecho con " data-en="artistry, done with ">artistry, done with </span><span class="text-shine" data-es="cuidado" data-en="care">care</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Faciales personalizados, dermaplaning, laminado de cejas y extensiones de pestañas en un suite privado y personal dentro de My Suite Beauty Square. La esteticista licenciada Carolyna Wanderley diseña cada tratamiento según tu piel, con el mismo menú exacto que publica en Booksy." data-en="Custom facials, dermaplaning, brow lamination and lash extensions in a private one-on-one suite inside My Suite Beauty Square. Licensed esthetician Carolyna Wanderley designs every treatment around your skin, from the exact same menu she publishes on Booksy.">Custom facials, dermaplaning, brow lamination and lash extensions in a private one-on-one suite inside My Suite Beauty Square. Licensed esthetician Carolyna Wanderley designs every treatment around your skin, from the exact same menu she publishes on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 15 reseñas en Booksy" data-en="5.0 · 15 reviews on Booksy">5.0 · 15 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.instagram.com/carolynawanderley/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @carolynawanderley
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-5.jpg" alt="Radiofrequency facial treatment session at Beauty Spa Carolyna Wanderley" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Collagen Lift Therapy</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$119 · 2h" data-en="$119 · 2h">$119 · 2h</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''
block('<!-- HERO -->', '<!-- STRIP DE CONFIANZA -->', new_hero, 'hero')
print('hero OK')

# ============================================================
# 7. STRIP DE CONFIANZA
# ============================================================
new_strip = '''<!-- STRIP DE CONFIANZA -->
  <section class="relative border-y border-[color:var(--accent-ghost)] bg-[color:var(--bg-2)]">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="15">15</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Facial <span class="text-shine">&amp;</span> Brows</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Faciales · Cejas · Pestañas" data-en="Facials · Brows · Lashes">Facials · Brows · Lashes</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">1:1</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención personal, sin prisas" data-en="Personal, unhurried care">Personal, unhurried care</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Flagami, Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">3721 NW 7th St</p></div>
    </div>
  </section>

  '''
block('<!-- STRIP DE CONFIANZA -->', '<!-- MARQUEE -->', new_strip, 'strip')
print('strip OK')

# ============================================================
# 8. MARQUEE 1
# ============================================================
new_marquee1 = '''<!-- MARQUEE 1 -->
  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">
      <div class="marquee-seq">
        <span class="marquee-word">Facial Therapy</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Dermaplaning</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Collagen Lift</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Lamination</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lash Extensions</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Miami, FL</span><span class="marquee-star">✦</span>
      </div>
      <div class="marquee-seq">
        <span class="marquee-word">Facial Therapy</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Dermaplaning</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Collagen Lift</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Lamination</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lash Extensions</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Miami, FL</span><span class="marquee-star">✦</span>
      </div>
    </div>
  </div>

  '''
block('<!-- MARQUEE -->', '<!-- LA EXPERIENCIA -->', new_marquee1, 'marquee1')
print('marquee1 OK')

# ============================================================
# 9. LA EXPERIENCIA
# ============================================================
new_experiencia = '''<!-- LA EXPERIENCIA -->
  <section id="experiencia" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">01</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-14 items-center">
      <div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-1.jpg" alt="Interior of the treatment suite at Beauty Spa Carolyna Wanderley" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-7.jpg" alt="Facial treatment session with warm towel at Beauty Spa Carolyna Wanderley" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un estudio," data-en="One studio,">One studio,</span><br /><span class="text-shine" data-es="una esteticista licenciada" data-en="one licensed esthetician">one licensed esthetician</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Beauty Spa Carolyna Wanderley es un suite privado y personal dentro de My Suite Beauty Square, en Flagami, a pasos del Aeropuerto Internacional de Miami. Cada cita de facial, cejas o pestañas es con Carolyna en persona, en un espacio tranquilo pensado para resultados reales en tu piel, no una silla apurada en un salón grande." data-en="Beauty Spa Carolyna Wanderley is a private one-on-one suite inside My Suite Beauty Square in Flagami, steps from Miami International Airport. Every facial, brow and lash appointment is with Carolyna herself, in a calm room built for real skincare results, not a rushed chair in a big salon.">Beauty Spa Carolyna Wanderley is a private one-on-one suite inside My Suite Beauty Square in Flagami, steps from Miami International Airport. Every facial, brow and lash appointment is with Carolyna herself, in a calm room built for real skincare results, not a rushed chair in a big salon.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Su menú incluye faciales de firma como Collagen Lift y Melasma Balance Therapy, dermaplaning, laminado de cejas y sets completos de pestañas clásicas, híbridas, volumen y mega volumen, todo publicado con precios exactos en Booksy y respaldado por una calificación perfecta de 5.0." data-en="Her menu covers signature facials like Collagen Lift and Melasma Balance Therapy, dermaplaning, brow lamination and full sets of classic, hybrid, volume and mega volume lash extensions, all published with exact pricing on Booksy and backed by a perfect 5.0 rating.">Her menu covers signature facials like Collagen Lift and Melasma Balance Therapy, dermaplaning, brow lamination and full sets of classic, hybrid, volume and mega volume lash extensions, all published with exact pricing on Booksy and backed by a perfect 5.0 rating.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="15">15</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="Beauty Spa Carolyna Wanderley" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(168,87,74,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Carolyna Wanderley · <span class="text-[color:var(--ink-40)]" data-es="Esteticista licenciada" data-en="Licensed esthetician">Licensed esthetician</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''
block('<!-- LA EXPERIENCIA -->', '<!-- EL METODO -->', new_experiencia, 'experiencia')
print('experiencia OK')

# ============================================================
# 10. EL METODO
# ============================================================
new_metodo = '''<!-- EL METODO -->
  <section id="metodo" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">02</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="De la reserva a la" data-en="From booking to">From booking to</span> <span class="text-shine" data-es="piel radiante" data-en="glowing skin">glowing skin</span></h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elige tu facial, cejas o pestañas en Booksy con precio y duración claros, y confirma al instante." data-en="Pick your facial, brow or lash service on Booksy with clear price and duration, and confirm instantly.">Pick your facial, brow or lash service on Booksy with clear price and duration, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Diagnóstico" data-en="Skin check">Skin check</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Carolyna revisa tu piel o tus objetivos de cejas antes de empezar, para que cada producto y técnica se ajuste a lo que realmente necesitas." data-en="Carolyna reviews your skin or brow goals before starting, so every product and technique matches what you actually need.">Carolyna reviews your skin or brow goals before starting, so every product and technique matches what you actually need.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Tu tratamiento" data-en="Your treatment">Your treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te relajas en el suite privado mientras Carolyna realiza tu facial, dermaplaning, laminado o set de pestañas de principio a fin." data-en="You relax in the private suite while Carolyna works through your facial, dermaplaning, lamination or lash set start to finish.">You relax in the private suite while Carolyna works through your facial, dermaplaning, lamination or lash set start to finish.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Cuidado posterior" data-en="Aftercare">Aftercare</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con indicaciones claras de cuidado y tu próxima cita o retoque agendado, para que los resultados duren." data-en="You leave with clear aftercare tips and your next appointment or fill booked, so results last.">You leave with clear aftercare tips and your next appointment or fill booked, so results last.</p>
        </div>
      </div>
    </div>
  </section>

  '''
block('<!-- EL METODO -->', '<!-- SERVICIOS -->', new_metodo, 'metodo')
print('metodo OK')

# ============================================================
# 11. SERVICIOS: 4 cards destacadas + menu completo categorizado (44 servicios reales)
# ============================================================

def row(en_name, es_name, price, dur=''):
    dur_html = f' <span class="text-[color:var(--ink-40)]">· {dur}</span>' if dur else ''
    return (f'      <div class="flex items-baseline justify-between gap-4 py-2 border-b border-[color:var(--accent-ghost)] last:border-0">'
            f'<span class="text-[color:var(--ink-60)] font-light" data-es="{es_name}" data-en="{en_name}">{en_name}</span>'
            f'<span class="text-sm font-medium whitespace-nowrap">${price}{dur_html}</span></div>\n')


facials_rows = (
    row('Skin Glow Therapy', 'Skin Glow Therapy', 77)
    + row('Skin Reset Therapy', 'Skin Reset Therapy', 111)
    + row('Collagen Lift Therapy', 'Collagen Lift Therapy', 119, '2h')
    + row('Pore Balance Therapy', 'Pore Balance Therapy', 140, '2h')
    + row('Melasma Balance Therapy', 'Melasma Balance Therapy', 136, '1h 30min')
    + row('Acne Balance Therapy', 'Acne Balance Therapy', 111)
    + row('Teen Skin Therapy', 'Teen Skin Therapy', 70, '1h')
    + row('Dermaplaning Skin Therapy', 'Dermaplaning Skin Therapy', 94, '1h 30min')
    + row('Glow Peel Therapy', 'Glow Peel Therapy', 130, '1h 15min')
)
brows_rows = (
    row('Brow Shaping (tweezers, wax, thread)', 'Diseño de cejas (pinza, cera, hilo)', 17)
    + row('Brow Shaping + Tinting', 'Diseño de cejas + Tinte', 35, '1h')
    + row('Brow Lamination', 'Laminado de cejas', 60)
    + row('Brow Lamination + Tinting', 'Laminado de cejas + Tinte', 72, '1h 10min')
    + row('Eyebrow Reconstruction (analysis only)', 'Reconstrucción de cejas (solo análisis)', 25)
    + row('Eyebrow Reconstruction with analysis', 'Reconstrucción de cejas con análisis', 60)
)
lashes_rows = (
    row('Classic Lash Extensions', 'Extensiones clásicas', 85, '2h 30min')
    + row('Classic Lash Extensions Refill', 'Retoque clásico', 43)
    + row('Hybrid Lash Extensions', 'Extensiones híbridas', 102, '2h 30min')
    + row('Hybrid Lash Extensions Refill', 'Retoque híbrido', 51, '2h')
    + row('Volume Lash Extensions', 'Extensiones de volumen', 128, '2h 30min')
    + row('Volume Lash Extensions Refill', 'Retoque de volumen', 64, '2h')
    + row('Mega Volume Extension', 'Mega volumen', 200, '3h')
    + row('Mega Volume Extension Refill', 'Retoque mega volumen', 100, '2h 30min')
    + row('Allergy Test', 'Prueba de alergia', 26, '45min')
    + row('Lash Removal', 'Retiro de pestañas', 17)
    + row('Lash Lifting', 'Lifting de pestañas', 68, '1h')
    + row('Lash Lifting + Tinting', 'Lifting de pestañas + Tinte', 81, '1h 30min')
)
waxing_rows = (
    row('Upper Lip', 'Bigote', 9)
    + row('Nostrils', 'Fosas nasales', 9)
    + row('Chin', 'Mentón', 9)
    + row('Sideburns', 'Patillas', 13)
    + row('Ears', 'Orejas', 13)
    + row('Forehead', 'Frente', 13)
    + row('Chin &amp; Neck', 'Mentón y cuello', 17)
    + row('Neck (Front or Back)', 'Cuello (delante o detrás)', 17)
    + row('Cheeks', 'Mejillas', 17)
    + row('Full Face', 'Facial completo', 38, '1h')
)

new_servicios = '''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine">ritual</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Beauty Spa Carolyna Wanderley en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Beauty Spa Carolyna Wanderley on Booksy. Booking confirms instantly.">Prices and durations as published by Beauty Spa Carolyna Wanderley on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Brillo diario" data-en="Everyday glow">Everyday glow</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Skin Glow Therapy</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un facial suave e hidratante que renueva la piel cansada y devuelve el brillo natural, ideal como primera visita o mantenimiento mensual." data-en="A gentle, hydrating facial that resets tired skin and brings back natural glow, perfect as a first visit or monthly maintenance.">A gentle, hydrating facial that resets tired skin and brings back natural glow, perfect as a first visit or monthly maintenance.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$77</p></div>
            <a href="https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(168,87,74,0.4); box-shadow: 0 18px 50px rgba(51,38,31,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Collagen Lift Therapy</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El tratamiento de firma: estimulación profunda de colágeno para firmar, levantar y suavizar la textura de la piel, el facial más solicitado de Carolyna." data-en="The signature treatment: deep collagen stimulation to firm, lift and smooth skin texture, Carolyna's most requested facial.">The signature treatment: deep collagen stimulation to firm, lift and smooth skin texture, Carolyna's most requested facial.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$119</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Renovación de piel" data-en="Skin renewal">Skin renewal</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Dermaplaning Skin Therapy</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Exfoliación manual que elimina células muertas y vello facial fino para un rostro instantáneamente más suave y luminoso." data-en="Manual exfoliation that removes dead skin and peach fuzz for an instantly smoother, brighter complexion.">Manual exfoliation that removes dead skin and peach fuzz for an instantly smoother, brighter complexion.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$94</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especialidad en cejas" data-en="Brow specialty">Brow specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Laminado de cejas + Tinte" data-en="Brow Lamination + Tinting">Brow Lamination + Tinting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cejas levantadas, fijadas y tintadas para una forma más definida y llena que dura semanas, uno de los servicios más pedidos por las clientas." data-en="Brows lifted, set and tinted for a fuller, more defined shape that holds for weeks, one of the services clients ask for most.">Brows lifted, set and tinted for a fuller, more defined shape that holds for weeks, one of the services clients ask for most.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$72</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 10min</p></div>
            <a href="https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="44 servicios entre faciales, cejas, pestañas y depilación facial. Menú completo abajo, precios exactos y reservas en Booksy." data-en="44 services across facials, brows, lashes and facial waxing. Full menu below, exact pricing and booking on Booksy.">44 services across facials, brows, lashes and facial waxing. Full menu below, exact pricing and booking on Booksy.</span></p>

      <div class="grid lg:grid-cols-2 gap-6 mt-14">
        <div class="glass rounded-3xl p-8 reveal">
          <h3 class="font-display text-xl mb-5 text-[color:var(--accent-deep)]" data-es="Faciales" data-en="Facials">Facials</h3>
          <div class="text-sm">
''' + facials_rows + '''          </div>
          <p class="text-xs text-[color:var(--ink-40)] font-light mt-5 pt-4 border-t border-[color:var(--accent-ghost)]" data-es="También disponible: LED Therapy $20, Mascarilla de colágeno $30, Infusión ultrasónica $25, Microagujas con suero $50, Electroporación $50, Oxigenoterapia $20, Dermaplaning individual $20." data-en="Also available: LED Therapy $20, Collagen Mask $30, Ultrasonic Infusion $25, Microneedle with Serum $50, Electroporation $50, Oxygen Therapy $20, standalone Dermaplaning $20.">Also available: LED Therapy $20, Collagen Mask $30, Ultrasonic Infusion $25, Microneedle with Serum $50, Electroporation $50, Oxygen Therapy $20, standalone Dermaplaning $20.</p>
        </div>
        <div class="glass rounded-3xl p-8 reveal" style="transition-delay:80ms">
          <h3 class="font-display text-xl mb-5 text-[color:var(--accent-deep)]" data-es="Cejas" data-en="Brows">Brows</h3>
          <div class="text-sm">
''' + brows_rows + '''          </div>
        </div>
        <div class="glass rounded-3xl p-8 reveal" style="transition-delay:160ms">
          <h3 class="font-display text-xl mb-5 text-[color:var(--accent-deep)]" data-es="Pestañas" data-en="Lashes">Lashes</h3>
          <div class="text-sm">
''' + lashes_rows + '''          </div>
        </div>
        <div class="glass rounded-3xl p-8 reveal" style="transition-delay:240ms">
          <h3 class="font-display text-xl mb-5 text-[color:var(--accent-deep)]" data-es="Depilación Facial" data-en="Facial Waxing">Facial Waxing</h3>
          <div class="text-sm">
''' + waxing_rows + '''          </div>
        </div>
      </div>
    </div>
  </section>

  '''
block('<!-- SERVICIOS -->', '<!-- GALERIA -->', new_servicios, 'servicios')
print('servicios OK')

# ============================================================
# 12. GALERIA
# ============================================================
new_galeria = '''<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span></h2>
        </div>
        <a href="https://www.instagram.com/carolynawanderley/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @carolynawanderley
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Sesión de dermaplaning" data-en="Dermaplaning session">Dermaplaning session</span><img src="assets/raw/bk-10.jpg" alt="Dermaplaning facial treatment in progress at Beauty Spa Carolyna Wanderley" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Diseño de cejas" data-en="Brow shaping">Brow shaping</span><img src="assets/raw/bk-12.jpg" alt="Close-up of eyebrow shaping treatment with tweezers" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Resultado de laminado" data-en="Lamination result">Lamination result</span><img src="assets/raw/bk-16.jpg" alt="Before and after of brow lamination and tinting" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Aplicación de mascarilla" data-en="Mask application">Mask application</span><img src="assets/raw/bk-3.jpg" alt="Facial mask being applied during a treatment" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Facial con radiofrecuencia" data-en="Radiofrequency facial">Radiofrequency facial</span><img src="assets/raw/bk-6.jpg" alt="Radiofrequency facial treatment tool on client skin" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Microdermoabrasión" data-en="Microdermabrasion">Microdermabrasion</span><img src="assets/raw/bk-4.jpg" alt="Microdermabrasion treatment session" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''
block('<!-- GALERIA -->', '<!-- MARQUEE -->', new_galeria, 'galeria')
print('galeria OK')

# ============================================================
# 13. MARQUEE 2 (marquee-reverse): tras renombrar el marquee1, este
#     "<!-- MARQUEE -->" generico ahora es unico (el original de marquee-reverse).
# ============================================================
new_marquee2 = '''<!-- MARQUEE 2 -->
  <div class="marquee marquee-reverse" aria-hidden="true">
    <div class="marquee-track">
      <div class="marquee-seq">
        <span class="marquee-word">Facial Therapy</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Dermaplaning</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Collagen Lift</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Lamination</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lash Extensions</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Miami, FL</span><span class="marquee-star">✦</span>
      </div>
      <div class="marquee-seq">
        <span class="marquee-word">Facial Therapy</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Dermaplaning</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Collagen Lift</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Brow Lamination</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Lash Extensions</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Miami, FL</span><span class="marquee-star">✦</span>
      </div>
    </div>
  </div>

  '''
block('<!-- MARQUEE -->', '<!-- OPINIONES -->', new_marquee2, 'marquee2')
print('marquee2 OK')

# ============================================================
# 14. OPINIONES (3 quotes verbatim reales de Booksy, idioma original)
# ============================================================
new_opiniones = '''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Reviews</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 15 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 15 verified reviews on Booksy">5.0 out of 5 · 15 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Carolyna was amazing! Great customer service. Happy to have found someone with so much attention to detail and passionate for her job!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Delia Maria A.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Carolyna was amazing! She made me feel so comfortable and walked me thru each step of my facial which I loved. Very nice and friendly as well, thank you for the fantastic service, definitely will be coming back."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jazmine V.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Encantada con el servicio, Carolyna me comprendió perfectamente lo que quería con mis cejas, y el resultado fue exacto lo que le pedí, bellas!!! Súper recomendable!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Claudia M.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 15 reseñas en Booksy" data-en="Read all 15 reviews on Booksy">Read all 15 reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''
block('<!-- OPINIONES -->', '<!-- UBICACION -->', new_opiniones, 'opiniones')
print('opiniones OK')

# ============================================================
# 15. UBICACION
# ============================================================
new_ubicacion = '''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">3721 NW 7th St, Suite 39 (My Suite Beauty Square), Miami, FL 33126</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(168,87,74,0.4)]" href="https://www.google.com/maps?q=3721+NW+7th+St,+Suite+39,+Miami,+FL+33126" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Martes a sábado, 10:00 am a 6:00 pm." data-en="Tuesday to Saturday, 10:00 am to 6:00 pm.">Tuesday to Saturday, 10:00 am to 6:00 pm.</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(168,87,74,0.4)]" href="https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los trabajos más recientes de Carolyna y escribe por DM cualquier duda antes de tu cita." data-en="See Carolyna's latest work and DM any questions before your appointment.">See Carolyna's latest work and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(168,87,74,0.4)]" href="https://www.instagram.com/carolynawanderley/" target="_blank" rel="noopener">@carolynawanderley</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Beauty Spa Carolyna Wanderley, 3721 NW 7th St, Suite 39, Miami FL"
          src="https://www.google.com/maps?q=3721+NW+7th+St,+Suite+39,+Miami,+FL+33126&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
  </section>

  '''
block('<!-- UBICACION -->', '<!-- CTA FINAL -->', new_ubicacion, 'ubicacion')
print('ubicacion OK')

# ============================================================
# 16. CTA FINAL
# ============================================================
new_cta = '''<!-- CTA FINAL -->
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #2a1a12 0%, #1f120c 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Piel radiante, cejas perfectas, un estudio de confianza." data-en="Glowing skin, perfect brows, one trusted studio.">Glowing skin, perfect brows, one trusted studio.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima" data-en="Your next">Your next</span> <span class="text-shine" data-es="transformación te espera" data-en="glow-up is waiting">glow-up is waiting</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva tu facial, laminado de cejas o set de pestañas en línea en segundos, o el retoque que ya te toca." data-en="Book your facial, brow lamination or lash set online in seconds, or the fill and touch-up you are due for.">Book your facial, brow lamination or lash set online in seconds, or the fill and touch-up you are due for.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
        <a href="https://www.instagram.com/carolynawanderley/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>
      </div>
    </div>
  </section>

  '''
block('<!-- CTA FINAL -->', '<!-- FOOTER -->', new_cta, 'cta_final')
print('cta_final OK')

# ============================================================
# 17. FOOTER
# ============================================================
new_footer = '''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#1c120c]">
    <span class="foot-mark" aria-hidden="true">Carolyna Wanderley</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="Beauty Spa Carolyna Wanderley" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(243,211,191,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Carolyna Wanderley</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de faciales, cejas y pestañas dentro de My Suite Beauty Square, Flagami, Miami FL. Solo con cita previa." data-en="Facial, brow and lash studio inside My Suite Beauty Square, Flagami, Miami FL. By appointment only.">Facial, brow and lash studio inside My Suite Beauty Square, Flagami, Miami FL. By appointment only.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>3721 NW 7th St, Suite 39, Miami, FL 33126</p>
        <p><a href="https://booksy.com/en-us/1477645_beauty-spa-carolyna-wanderley_brows-lashes_15889_miami" target="_blank" rel="noopener" class="hover:text-[#f3d3bf]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="https://www.instagram.com/carolynawanderley/" target="_blank" rel="noopener" class="hover:text-[#f3d3bf]">Instagram · @carolynawanderley</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Beauty Spa Carolyna Wanderley.</p>
        <a href="https://merktop.com" target="_blank" rel="noopener" class="merktop-badge">
          <span class="merktop-dot"></span>
          <span class="text-xs text-[#f4eee2]">Powered by <span class="font-semibold">Merktop</span></span>
        </a>
      </div>
    </div>
  </footer>

  '''
block('<!-- FOOTER -->', '<!-- Boton flotante de reserva -->', new_footer, 'footer')
print('footer OK')

# ============================================================
# 18. Boton flotante + aria-label
# ============================================================
rep('aria-label="Reservar cita online"', 'aria-label="Reservar cita online"')  # sin cambios, ya generico

open(OUT, 'w', encoding='utf-8').write(h)
print('checkpoint FINAL escrito')
