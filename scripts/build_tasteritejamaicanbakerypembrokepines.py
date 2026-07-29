import re
import shutil

SLUG = "taste-rite-jamaican-bakery-pembroke-pines"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/light-v2/index.html", PATH)
h = open(PATH, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:200]
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None):
    global h
    c = h.count(a)
    assert c > 0, "NO ANCHOR: " + a[:200]
    if expect is not None:
        assert c == expect, f"count {c} != expected {expect} for " + a[:80]
    h = h.replace(a, b)


# ---------------------------------------------------------------------------
# Constantes de contacto reales
# ---------------------------------------------------------------------------
TEL = "tel:+19549986298"
PHONE_DISPLAY = "(954) 998-6298"
ADDRESS_LINE = "9924 Pines Blvd, Pembroke Pines, FL 33024"
MAPS_DIR = "https://www.google.com/maps?q=9924+Pines+Blvd,+Pembroke+Pines,+FL+33024"
MAPS_EMBED = "https://www.google.com/maps?q=9924+Pines+Blvd,+Pembroke+Pines,+FL+33024&output=embed"
GOOGLE_REVIEWS_URL = "https://www.google.com/maps/search/?api=1&query=Taste+Rite+Jamaican+Bakery+9924+Pines+Blvd+Pembroke+Pines+FL"
IG_URL = "https://www.instagram.com/tasteritebakery/"
IG_HANDLE = "@tasteritebakery"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> golden wheat / Jamaican gold (Taste Rite)
#    Derivada del logo real (medallon dorado/rojo sobre fondo amarillo) y de
#    los patties dorados en las fotos. Fondo claro tipo pan/masa horneada.
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#b8860a"),  # accent-deep (goldenrod)
    ("#5c2140", "#6b4a06"),  # btn-3d sole darkest
    ("#f0bed7", "#f2d98a"),  # dark-band shine/orb/stars accent (soft gold)
    ("#faf2f6", "#faf6ec"),  # bg (warm cream)
    ("#c47a9c", "#d1a237"),  # accent-mid (honey gold)
    ("#8a5573", "#8a6416"),  # dark-band btn shadow deep
    ("#f3e0ea", "#f5ecd8"),  # bg-2 / accent-soft (pale wheat)
    ("#d9a8c2", "#e6c877"),  # orb-b (warm gold)
    ("#7d3457", "#7a5710"),  # dark mid
    ("#5f2c48", "#5c3f0c"),  # step-num gradient end
    ("#33222c", "#2e2013"),  # ink (coffee brown)
    ("#fbf3f8", "#fdf8ec"),  # tile-cap text near-white
    ("#fbeff5", "#faf0d2"),  # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#f3e0a8"),  # dark-band shimmer 3rd stop
    ("#f6f1ea", "#faf6ec"),  # theme-color meta
    ("#f2d5e3", "#f2dfa0"),  # orb-a
    ("#f2cfe0", "#eed48a"),  # dark-band shimmer last stop
    ("#efd0e0", "#f0dca0"),  # dark-band btn-3d gradient mid
    ("#e5c1d4", "#e9cf8c"),  # orb-c
    ("#dc9dbe", "#e0b23a"),  # scroll-progress end stop
    ("#d3a2bc", "#dbb658"),  # dark-band btn-3d gradient end light
    ("#c9789f", "#d9ad34"),  # shimmer stop
    ("#b25a85", "#a8790f"),  # shimmer stop
    ("#2a1722", "#2b2013"),  # cta-final bg gradient start (coffee brown)
    ("#1f0f18", "#1c140b"),  # cta-final bg gradient end
    ("#1c0f16", "#19130b"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(184,134,10"),    # accent-deep alpha
    ("rgba(51,34,44", "rgba(46,32,19"),        # ink alpha
    ("rgba(240,190,215", "rgba(242,217,138"),  # dark-band light accent alpha
    ("rgba(70,25,50", "rgba(74,50,6"),         # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(250,246,236"),  # bg alpha (nav scrolled)
    ("rgba(125,52,87", "rgba(122,87,16"),      # dark mid alpha
    ("rgba(253,246,250", "rgba(253,248,236"),  # surface alpha
    ("rgba(40,16,30", "rgba(38,26,10"),        # tile-cap gradient dark
    ("rgba(233,205,186", "rgba(242,223,160"),  # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(230,200,119"),  # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: quitar Booksy (no aplica, es panaderia sin reservas), IG
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, TEL)  # fallback global; los CTAs especificos se re-escriben abajo con su propio texto

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, IG_HANDLE)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Taste Rite Jamaican Bakery · Patties &amp; Baked Goods in Pembroke Pines, FL | 4.5 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Taste Rite Jamaican Bakery, Pembroke Pines FL: fresh beef, chicken and vegetable patties, coco bread and Jamaican baked goods. 4.5 stars from 484 Google reviews. Call (954) 998-6298." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Taste Rite Jamaican Bakery · Pembroke Pines, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Fresh Jamaican patties and baked goods. 4.5 on Google with 484 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-patties-box.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Bakery",
    "name": "Taste Rite Jamaican Bakery",
    "description": "Jamaican bakery in Pembroke Pines, FL serving fresh beef, chicken and vegetable patties, coco bread, bulla bread and traditional Jamaican baked goods.",
    "address": { "@type": "PostalAddress", "streetAddress": "9924 Pines Blvd", "addressLocality": "Pembroke Pines", "addressRegion": "FL", "postalCode": "33024", "addressCountry": "US" },
    "telephone": "+1-954-998-6298",
    "sameAs": ["https://www.instagram.com/tasteritebakery/", "https://www.facebook.com/tasteritebakery/", "https://www.yelp.com/biz/taste-rite-jamaican-bakery-pembroke-pines"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.5", "reviewCount": "484", "bestRating": "5" },
    "openingHoursSpecification": { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:30", "closes": "18:00" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Menu", "itemListElement": [
      { "@type": "Offer", "price": "1.90", "priceCurrency": "USD", "itemOffered": { "@type": "Product", "name": "Beef Patty" } },
      { "@type": "Offer", "price": "2.00", "priceCurrency": "USD", "itemOffered": { "@type": "Product", "name": "Chicken Patty" } },
      { "@type": "Offer", "price": "1.50", "priceCurrency": "USD", "itemOffered": { "@type": "Product", "name": "Vegetable Patty" } },
      { "@type": "Offer", "price": "0.90", "priceCurrency": "USD", "itemOffered": { "@type": "Product", "name": "Coco Bread" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN, el esqueleto ya es EN por defecto -> sin cambios
# ---------------------------------------------------------------------------
assert 'applyLang(lang === \'es\' ? \'es\' : \'en\');' in h
print("IDIOMA ok (default en)")

# ---------------------------------------------------------------------------
# 6. NAV (logo + wordmark + preloader + links)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,134,10,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Taste Rite Jamaican Bakery" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,134,10,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Taste <span class="text-[color:var(--accent-deep)]">Rite</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">TR</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Taste Rite</span>')

rep_all('href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>',
        'href="#experiencia" data-es="Nuestra Historia" data-en="Our Story">Our Story</a>', expect=2)
rep_all('href="#metodo" data-es="El Método" data-en="The Method">El Método</a>',
        'href="#metodo" data-es="Fresco Cada Día" data-en="Fresh Daily">Fresh Daily</a>', expect=2)
rep_all('href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>',
        'href="#servicios" data-es="Menú" data-en="Menu">Menu</a>', expect=2)
rep_all('href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>',
        'href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>', expect=2)
rep_all('href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
        'href="#opiniones" data-es="Reseñas" data-en="Reviews">Reviews</a>', expect=2)
rep_all('href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>',
        'href="#ubicacion" data-es="Ubicación" data-en="Location">Location</a>', expect=2)

CALL_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'

rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          ''' + CALL_ICON + '''
          <span data-es="Llamar para Pedir" data-en="Call to Order">Call to Order</span>
        </a>''')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    '<a href="' + TEL + '" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar para Pedir" data-en="Call to Order">Call to Order</a>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Pembroke Pines, FL · Panadería Jamaiquina" data-en="Pembroke Pines, FL · Jamaican Bakery">Pembroke Pines, FL · Jamaican Bakery</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Horneado fresco, hojaldre a hojaldre." data-en="Baked fresh, patty by patty.">Baked fresh, patty by patty.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Hojaldres dorados y crujientes," data-en="Golden, flaky patties,">Golden, flaky patties,</span><br /><span data-es="horneados frescos " data-en="baked fresh ">baked fresh </span><span class="text-shine" data-es="cada día" data-en="every day">every day</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Patties de res, pollo y vegetales doblados a mano y horneados frescos en nuestra tienda de Pines Blvd, junto con coco bread, bulla bread y otros clásicos jamaiquinos. Pasa cualquier día menos domingo por un patty caliente." data-en="Beef, chicken and vegetable patties hand-folded and baked fresh at our Pines Blvd shop, along with coco bread, bulla bread and other Jamaican classics. Walk in any day but Sunday for a hot patty.">Beef, chicken and vegetable patties hand-folded and baked fresh at our Pines Blvd shop, along with coco bread, bulla bread and other Jamaican classics. Walk in any day but Sunday for a hot patty.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.5 · 484 reseñas en Google" data-en="4.5 · 484 reviews on Google">4.5 · 484 reviews on Google</span>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + IG_HANDLE + '''
          </a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llamar para Pedir" data-en="Call to Order">Call to Order</span>
            ''' + CALL_ICON + '''
          </a>
          <a href="''' + MAPS_DIR + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <span data-es="Cómo Llegar" data-en="Get Directions">Get Directions</span>
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-patties-box.jpg" alt="Box of golden Jamaican beef patties fresh from the oven at Taste Rite Jamaican Bakery" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Más Vendido" data-en="Best Seller">Best Seller</p>
            <p class="font-display text-lg">Beef Patty</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$1.90 · Horneado fresco" data-en="$1.90 · Baked fresh daily">$1.90 · Baked fresh daily</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.5" data-decimals="1">4.5</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="484">484</span> <span data-es="reseñas en Google" data-en="reviews on Google">reseñas en Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Patties <span class="text-shine">&amp;</span> Breads</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Doblados a mano, horneados frescos" data-en="Hand-folded, baked fresh">Hand-folded, baked fresh</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">10K+ <span class="text-shine" data-es="seguidores" data-en="followers">followers</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Comunidad fiel en Instagram" data-en="Loyal Instagram community">Loyal Instagram community</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Pembroke Pines</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">9924 Pines Blvd</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Beef Patty"),
    ("Hybrid Set", "Chicken Patty"),
    ("Volume Set", "Vegetable Patty"),
    ("Mega Volume", "Coco Bread"),
    ("Bottom Lashes", "Bulla Bread"),
    ("West Palm Beach, FL", "Pembroke Pines, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (Nuestra Historia / Our Story)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-01-bread-rolls.jpg" alt="Tray of fresh Jamaican bread rolls baked at Taste Rite" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-02-patties-tray.jpg" alt="Rows of hand-folded patties on a baking tray at Taste Rite Jamaican Bakery" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="Nuestra historia" data-en="Our story">Our story</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Patties de verdad," data-en="Real patties,">Real patties,</span><br /><span class="text-shine" data-es="hechos como se debe" data-en="made the honest way">made the honest way</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Taste Rite Jamaican Bakery hornea los mismos patties dorados y crujientes en sus tiendas del sur de la Florida, y la ubicación de Pines Blvd en Pembroke Pines es donde los vecinos pasan por un patty caliente de res, pollo o vegetales cualquier día de la semana." data-en="Taste Rite Jamaican Bakery bakes the same golden, flaky patties across its South Florida shops, and the Pines Blvd location in Pembroke Pines is where neighbors stop for a hot beef, chicken or vegetable patty any day of the week.">Taste Rite Jamaican Bakery bakes the same golden, flaky patties across its South Florida shops, and the Pines Blvd location in Pembroke Pines is where neighbors stop for a hot beef, chicken or vegetable patty any day of the week.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 4.5 de calificación en 484 reseñas de Google, clientes frecuentes que piden por nombre el patty de jerk chicken y el de callaloo, y más de 10,000 seguidores en Instagram pendientes de cada nueva tanda recién horneada." data-en="The result: a 4.5 rating across 484 Google reviews, regulars who call out the jerk chicken and callaloo patties by name, and a following of over 10,000 on Instagram watching for the next batch out of the oven.">The result: a 4.5 rating across 484 Google reviews, regulars who call out the jerk chicken and callaloo patties by name, and a following of over 10,000 on Instagram watching for the next batch out of the oven.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.5" data-decimals="1">4.5</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="484">484</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">10K+</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Instagram</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,134,10,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Taste Rite Jamaican Bakery" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,134,10,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Taste Rite <span class="text-[color:var(--ink-40)]" data-es="· Tienda de Pembroke Pines" data-en="· Pembroke Pines shop">· Pembroke Pines shop</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO (Fresco Cada Dia / Fresh Every Day)
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Fresco cada día" data-en="Fresh every day">Fresh every day</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Del horno" data-en="From the oven">From the oven</span> <span class="text-shine" data-es="a tus manos" data-en="to your hands">to your hands</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Masa fresca" data-en="Dough made fresh">Dough made fresh</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nuestra masa de hojaldre con cúrcuma se mezcla y estira fresca en la tienda, igual cada mañana." data-en="Our turmeric pastry dough is mixed and rolled fresh at the shop, the same way every morning.">Our turmeric pastry dough is mixed and rolled fresh at the shop, the same way every morning.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Doblados a mano" data-en="Hand-folded patties">Hand-folded patties</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Res, pollo, vegetales y más se rellenan y sellan a mano, patty por patty." data-en="Beef, chicken, vegetable and more get filled and crimped by hand, patty by patty.">Beef, chicken, vegetable and more get filled and crimped by hand, patty by patty.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Horneados dorados" data-en="Baked golden">Baked golden</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cada patty va al horno hasta que la masa queda dorada y crujiente, nunca se queda fría esperando." data-en="Every patty goes into the oven until the crust is flaky and golden, never sitting around cold.">Every patty goes into the oven until the crust is flaky and golden, never sitting around cold.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Entra, sin espera" data-en="Walk in, no wait">Walk in, no wait</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="No necesitas cita. Entra de lunes a sábado y llévate un patty caliente." data-en="No appointment needed. Walk in Monday through Saturday and grab a hot patty to go.">No appointment needed. Walk in Monday through Saturday and grab a hot patty to go.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS -> MENU (header + grid completo por regex + menu categorizado)
# ---------------------------------------------------------------------------
rep('data-es="Servicios" data-en="Services">Servicios</p>',
    'data-es="Menú" data-en="Menu">Menu</p>', n=1)
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Horneado" data-en="Baked">Baked</span> <span class="text-shine" data-es="fresco cada día" data-en="fresh daily">fresh daily</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios publicados para la ubicación de Pembroke Pines. Llama con anticipación para conocer la selección completa del día." data-en="Prices as published for the Pembroke Pines location. Call ahead for today\'s full selection.">Prices as published for the Pembroke Pines location. Call ahead for today\'s full selection.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Distintivo" data-en="Signature">Signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Beef Patty</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Res sazonada envuelta en una masa hojaldrada con cúrcuma, doblada a mano y horneada fresca. El clásico patty jamaiquino." data-en="Seasoned ground beef wrapped in a flaky turmeric pastry, hand-folded and baked fresh. Jamaica's classic hand pie.">Seasoned ground beef wrapped in a flaky turmeric pastry, hand-folded and baked fresh. Jamaica's classic hand pie.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$1.90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Horneado fresco" data-en="Baked fresh daily">Baked fresh daily</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar para Pedir" data-en="Call to Order">Call to Order</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(184,134,10,0.4); box-shadow: 0 18px 50px rgba(46,32,19,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo más pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Chicken Patty</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pollo sazonado en la misma masa dorada con cúrcuma. El favorito de los clientes junto al de res, según las reseñas." data-en="Seasoned chicken in the same golden turmeric crust. A customer favorite right alongside the beef, reviews say.">Seasoned chicken in the same golden turmeric crust. A customer favorite right alongside the beef, reviews say.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$2.00</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Horneado fresco" data-en="Baked fresh daily">Baked fresh daily</p></div>
            <a href="''' + TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar para Pedir" data-en="Call to Order">Call to Order</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Vegetariano" data-en="Vegetarian">Vegetarian</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Vegetable Patty</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Vegetales sazonados y horneados a la perfección en una masa suave y hojaldrada. Opción vegetariana de todos los días." data-en="Seasoned vegetables baked to perfection in a soft, flaky crust. The everyday vegetarian option.">Seasoned vegetables baked to perfection in a soft, flaky crust. The everyday vegetarian option.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$1.50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Horneado fresco" data-en="Baked fresh daily">Baked fresh daily</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar para Pedir" data-en="Call to Order">Call to Order</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Recién horneado" data-en="Fresh baked">Fresh baked</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Coco Bread" data-en="Coco Bread">Coco Bread</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pan suave de leche de coco, el envoltorio clásico para meter un patty caliente adentro." data-en="Soft coconut-milk bread, the classic wrap for tucking a hot patty inside.">Soft coconut-milk bread, the classic wrap for tucking a hot patty inside.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$0.90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Horneado fresco" data-en="Baked fresh daily">Baked fresh daily</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar para Pedir" data-en="Call to Order">Call to Order</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Patties" data-en="Patties">Patties</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-2"><span>Beef Patty</span><span class="text-[color:var(--ink-40)]">$1.90</span></li>
            <li class="flex items-center justify-between gap-2"><span>Chicken Patty</span><span class="text-[color:var(--ink-40)]">$2.00</span></li>
            <li class="flex items-center justify-between gap-2"><span>Vegetable Patty</span><span class="text-[color:var(--ink-40)]">$1.50</span></li>
            <li class="flex items-center gap-2 pt-1" style="border-top:1px solid var(--accent-ghost)"><span data-es="+ Jerk Chicken, Cheesy Beef, Callaloo, Ackee &amp; Saltfish, Fish, Shrimp y Meatloaf Patty: pregunta en tienda por los sabores del día." data-en="+ Jerk Chicken, Cheesy Beef, Callaloo, Ackee &amp; Saltfish, Fish, Shrimp and Meatloaf Patty: ask in store for today's flavors.">+ Jerk Chicken, Cheesy Beef, Callaloo, Ackee &amp; Saltfish, Fish, Shrimp and Meatloaf Patty: ask in store for today's flavors.</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Panes y Sweet Tings" data-en="Breads &amp; Sweet Tings">Breads &amp; Sweet Tings</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-2"><span>Coco Bread</span><span class="text-[color:var(--ink-40)]">$0.90</span></li>
            <li class="flex items-center justify-between gap-2"><span>Corn Bread</span><span class="text-[color:var(--ink-40)]">$1.75</span></li>
            <li class="flex items-center justify-between gap-2"><span>Bulla Bread</span><span class="text-[color:var(--ink-40)]">$2.00</span></li>
            <li class="flex items-center justify-between gap-2"><span>Gizzada</span><span class="text-[color:var(--ink-40)]">$1.25</span></li>
            <li class="flex items-center justify-between gap-2"><span>Sugar Bun</span><span class="text-[color:var(--ink-40)]">$1.50</span></li>
            <li class="flex items-center justify-between gap-2"><span>Banana Bread</span><span class="text-[color:var(--ink-40)]">$1.75</span></li>
            <li class="flex items-center justify-between gap-2"><span>Toto</span><span class="text-[color:var(--ink-40)]">$1.50</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Bebidas y Más" data-en="Drinks &amp; More">Drinks &amp; More</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2"><span data-es="Sodas jamaiquinas D&amp;G" data-en="D&amp;G Jamaican Sodas">D&amp;G Jamaican Sodas</span></li>
            <li class="flex items-center gap-2"><span>Ting</span></li>
            <li class="flex items-center gap-2"><span>Malta</span></li>
            <li class="flex items-center gap-2"><span data-es="Agua de coco" data-en="Coconut Water">Coconut Water</span></li>
            <li class="flex items-center gap-2"><span data-es="Budín de papa" data-en="Potato Pudding">Potato Pudding</span></li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="El menú y la disponibilidad pueden variar según el día. Llama a la tienda para confirmar los sabores de hoy." data-en="Menu and availability may vary by day. Call the shop to confirm today\'s flavors.">Menu and availability may vary by day. Call the shop to confirm today\'s flavors.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Fresco," data-en="Fresh,">Fresh,</span> <span class="text-shine" data-es="cada tanda" data-en="every batch">every batch</span>')
rep('''<a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + IG_HANDLE + '''
        </a>''',
    '''<a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + IG_HANDLE + '''
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Recién salidos de la caja" data-en="Hot out the box">Hot out the box</span><img src="assets/hero-patties-box.jpg" alt="Box of golden Jamaican patties fresh from the oven at Taste Rite" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Doblado a mano, siempre" data-en="Hand-folded, always">Hand-folded, always</span><img src="assets/gallery-01-hand-patty.jpg" alt="Hand holding a golden Jamaican patty at Taste Rite Jamaican Bakery" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="También los Sweet Tings" data-en="Sweet Tings too">Sweet Tings too</span><img src="assets/gallery-02-sweet-bread.jpg" alt="Hand holding a sweet Jamaican pastry with red filling from Taste Rite" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Esa masa crujiente" data-en="That flaky crust">That flaky crust</span><img src="assets/gallery-03-patty-bite.jpg" alt="Bitten Jamaican beef patty showing the flaky crust and filling at Taste Rite" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Bebidas naturales también" data-en="Fresh juices too">Fresh juices too</span><img src="assets/gallery-04-juices.jpg" alt="Three bottled all-natural juice drinks held in hand at Taste Rite Jamaican Bakery" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Tanda fresca, lista para llevar" data-en="Fresh batch, boxed up">Fresh batch, boxed up</span><img src="assets/gallery-05-patties-box2.jpg" alt="Another box of fresh Jamaican patties ready to go at Taste Rite" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="los clientes" data-en="customers say">customers say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.5 de 5 · 484 reseñas en Google" data-en="4.5 out of 5 · 484 reviews on Google">4.5 out of 5 · 484 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I stumbled upon this gem of a spot that has some amazing Jamaican patties. They have a jerk chicken which I never seen before, they are delicious."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Maurice R.</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Imo best jamaican patties in south florida. I've been to the sunrise location and this one is just as good."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Nathan D.</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Hands down, the BEST patties in all of South Florida! Lots of variety too. Beef, jerk chicken, fish, ackee &amp; saltfish, to name a few."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Suzanne G.</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>''')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + GOOGLE_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 484 reseñas en Google" data-en="Read all 484 reviews on Google">Read all 484 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Encuéntranos en" data-en="Find us in">Find us in</span> <span class="text-shine">Pembroke Pines</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,134,10,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + ADDRESS_LINE + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,134,10,0.4)]" href="''' + MAPS_DIR + '''" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>''')
rep('<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n            <div>\n              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>',
    '<svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n            <div>\n              <p class="font-medium mb-1" data-es="Pedidos" data-en="Order">Order</p>')

rep('''<div>
              <p class="font-medium mb-1" data-es="Pedidos" data-en="Order">Order</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,134,10,0.4)]" href="''' + TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Pedidos" data-en="Order">Order</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Llama con anticipación o pasa de lunes a sábado, de 9:30am a 6:00pm. Cerrado los domingos." data-en="Call ahead or walk in Monday through Saturday, 9:30am to 6:00pm. Closed Sundays.">Call ahead or walk in Monday through Saturday, 9:30am to 6:00pm. Closed Sundays.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,134,10,0.4)]" href="''' + TEL + '''" data-es="Llamar (954) 998-6298" data-en="Call (954) 998-6298">Call (954) 998-6298</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,134,10,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">''' + IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira las últimas tandas frescas y escribe por DM si tienes dudas." data-en="See the latest fresh batches and DM with any questions.">See the latest fresh batches and DM with any questions.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,134,10,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">''' + IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Taste Rite Jamaican Bakery, 9924 Pines Blvd, Pembroke Pines FL"
          src="''' + MAPS_EMBED + '''"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Horneado fresco, hojaldre a hojaldre." data-en="Baked fresh, patty by patty.">Baked fresh, patty by patty.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Pasa por un" data-en="Stop by for a">Stop by for a</span> <span class="text-shine" data-es="patty caliente hoy" data-en="hot patty today">hot patty today</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Llama con anticipación o simplemente entra, de lunes a sábado. Pines Blvd, Pembroke Pines." data-en="Call ahead or just walk in, Monday through Saturday. Pines Blvd, Pembroke Pines.">Call ahead or just walk in, Monday through Saturday. Pines Blvd, Pembroke Pines.</p>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar para Pedir" data-en="Call to Order">Call to Order</a>
        <a href="''' + MAPS_DIR + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Cómo Llegar" data-en="Get Directions">Get Directions</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Taste Rite</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(242,217,138,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Taste Rite Jamaican Bakery" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(242,217,138,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Taste Rite</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Panadería jamaiquina en Pembroke Pines, FL. Caminantes bienvenidos, de lunes a sábado." data-en="Jamaican bakery in Pembroke Pines, FL. Walk-ins welcome, Monday through Saturday.">Jamaican bakery in Pembroke Pines, FL. Walk-ins welcome, Monday through Saturday.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + TEL + '''" target="_blank" rel="noopener" class="hover:text-[#f2d98a]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>''' + ADDRESS_LINE + '''</p>
        <p><a href="''' + TEL + '''" class="hover:text-[#f2d98a]" data-es="Llamar · (954) 998-6298" data-en="Call · (954) 998-6298">Call &middot; (954) 998-6298</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f2d98a]">Instagram · ''' + IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f2d98a]">Instagram &middot; ''' + IG_HANDLE + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Taste Rite Jamaican Bakery.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante (llamar) + aria-labels
# ---------------------------------------------------------------------------
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf6ec" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>''',
    '''<a href="''' + TEL + '''" class="book-float" aria-label="Call to order">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf6ec" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>''')
print("BOOK-FLOAT done")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("WRITE done ->", PATH)
