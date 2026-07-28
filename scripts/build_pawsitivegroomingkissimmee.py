import re
import shutil

SLUG = "pawsitive-grooming-kissimmee"
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
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> tangerine / warm amber (Pawsitive)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#c2660f"),  # accent-deep
    ("#5c2140", "#7a3d08"),  # btn-3d sole darkest
    ("#f0bed7", "#f6d9a0"),  # dark-band shine/orb/stars accent
    ("#faf2f6", "#fbf5ec"),  # bg
    ("#c47a9c", "#e79a4a"),  # accent-mid
    ("#8a5573", "#8a5a1e"),  # dark-band btn shadow deep
    ("#f3e0ea", "#f3e6d4"),  # bg-2 / accent-soft
    ("#d9a8c2", "#f0d9b8"),  # orb-b
    ("#7d3457", "#9c520f"),  # dark mid
    ("#5f2c48", "#7d4a12"),  # step-num gradient end
    ("#33222c", "#2e2115"),  # ink
    ("#fbf3f8", "#fdf6ea"),  # tile-cap text near-white
    ("#fbeff5", "#fffaf0"),  # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#fbedd2"),  # dark-band shimmer 3rd stop
    ("#f6f1ea", "#fbf5ec"),  # theme-color meta
    ("#f2d5e3", "#f6ddb8"),  # orb-a
    ("#f2cfe0", "#f8e0b0"),  # dark-band shimmer last stop
    ("#efd0e0", "#fbead0"),  # dark-band btn-3d gradient mid
    ("#e5c1d4", "#f2dca0"),  # orb-c pale gold
    ("#dc9dbe", "#e8a75a"),  # scroll-progress end stop
    ("#d3a2bc", "#f4d9a8"),  # dark-band btn-3d gradient end light
    ("#c9789f", "#eb9d4c"),  # shimmer stop
    ("#b25a85", "#d98a35"),  # shimmer stop
    ("#2a1722", "#241a10"),  # cta-final bg gradient start
    ("#1f0f18", "#1a1109"),  # cta-final bg gradient end
    ("#1c0f16", "#19110a"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(194,102,15"),   # accent-deep alpha
    ("rgba(51,34,44", "rgba(46,33,21"),       # ink alpha
    ("rgba(240,190,215", "rgba(246,217,160"), # dark-band light accent alpha
    ("rgba(70,25,50", "rgba(74,38,10"),       # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(251,245,236"), # bg alpha (nav scrolled)
    ("rgba(125,52,87", "rgba(156,82,15"),     # dark mid alpha
    ("rgba(253,246,250", "rgba(253,248,236"), # surface alpha
    ("rgba(40,16,30", "rgba(38,22,10"),       # tile-cap gradient dark
    ("rgba(233,205,186", "rgba(242,203,150"), # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(198,138,70"),  # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: URL de Booksy, IG
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_BOOK = "https://booksy.com/en-us/1002877_pawsitive-grooming-salon-spa-llc_pet-services_134766_kissimmee"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_BOOK)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/pawsitivepetsgrooming/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@pawsitivepetsgrooming"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Pawsitive Grooming Salon & Spa · Grooming Canino y Felino en Kissimmee, FL | 5.0 en Booksy</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Pawsitive Grooming Salon & Spa en Kissimmee (Poinciana), FL: baño, corte y spa para perros y gatos de todas las razas, con Stephanie Samalot. 5.0 estrellas en 182 reseñas en Booksy. Reserva online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Pawsitive Grooming Salon & Spa · Grooming en Kissimmee, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Baño, corte y spa para perros y gatos. 5.0 en Booksy con 182 reseñas. Reserva online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/gallery-01-before-after.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Pawsitive Grooming Salon & Spa",
    "description": "Salon de grooming para perros y gatos en Kissimmee (Poinciana), FL: bano, ozone spa, corte segun raza, limpieza dental sin anestesia y grooming creativo, con Stephanie Samalot.",
    "address": { "@type": "PostalAddress", "streetAddress": "427 Arkansas Ct", "addressLocality": "Kissimmee", "addressRegion": "FL", "postalCode": "34759", "addressCountry": "US" },
    "telephone": "+1-407-655-9400",
    "sameAs": ["https://booksy.com/en-us/1002877_pawsitive-grooming-salon-spa-llc_pet-services_134766_kissimmee", "https://www.instagram.com/pawsitivepetsgrooming/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "182", "bestRating": "5" },
    "openingHoursSpecification": { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "10:00", "closes": "17:00" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de grooming", "itemListElement": [
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luxury Ozone Spa Therapy" } },
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full Grooming (Medium Size)" } },
      { "@type": "Offer", "price": "20", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pawdicure Deluxe" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Limpieza dental profunda" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio ES -> html lang=es, default de applyLang = es
# ---------------------------------------------------------------------------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")
print("IDIOMA done")

# ---------------------------------------------------------------------------
# 6. NAV (logo + wordmark + preloader)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,102,15,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Pawsitive Grooming Salon &amp; Spa" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,102,15,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Pawsitive <span class="text-[color:var(--accent-deep)]">Grooming</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">PG</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Pawsitive Grooming</span>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Kissimmee, FL · Grooming Canino y Felino" data-en="Kissimmee, FL · Dog &amp; Cat Grooming">Kissimmee, FL · Grooming Canino y Felino</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Cada cita, con mucho cariño." data-en="Every visit, with lots of love.">Cada cita, con mucho cariño.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Grooming profesional," data-en="Professional grooming,">Grooming profesional,</span><br /><span data-es="con la calma que " data-en="with the calm your ">con la calma que </span><span class="text-shine" data-es="tu mascota merece" data-en="pet deserves">tu mascota merece</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Baño, corte y spa para perros y gatos de todas las razas y tamaños, con Stephanie Samalot y su equipo en Kissimmee. Ozone spa, limpieza dental sin anestesia y grooming creativo, todo agendado por Booksy." data-en="Bath, haircut and spa for dogs and cats of every breed and size, with Stephanie Samalot and her team in Kissimmee. Ozone spa therapy, anesthesia-free dental cleaning and creative grooming, all booked through Booksy.">Bath, haircut and spa for dogs and cats of every breed and size, with Stephanie Samalot and her team in Kissimmee. Ozone spa therapy, anesthesia-free dental cleaning and creative grooming, all booked through Booksy.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 182 reseñas en Booksy" data-en="5.0 · 182 reviews on Booksy">5.0 · 182 reseñas en Booksy</span>')
rep('''<a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-poodle.jpg" alt="Caniche gigante recien peinado con collar de flores en Pawsitive Grooming Salon &amp; Spa" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Más popular" data-en="Most popular">Más popular</p>
            <p class="font-display text-lg">Ozone Spa Therapy</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$65 · Solo baño" data-en="$65 · Bath only">$65 · Solo baño</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="182">182</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl" data-es="Perros" data-en="Dogs">Perros</span> <span class="text-shine">&amp;</span> <span data-es="Gatos" data-en="Cats">Gatos</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Todas las razas y tamaños" data-en="Every breed and size">Todas las razas y tamaños</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl" data-es="Bilingüe" data-en="Bilingual">Bilingüe</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención en español e inglés" data-en="Service in Spanish &amp; English">Atención en español e inglés</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Kissimmee</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">427 Arkansas Ct</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Full Grooming"),
    ("Hybrid Set", "Ozone Spa"),
    ("Volume Set", "Pawdicure Deluxe"),
    ("Mega Volume", "Grooming Creativo"),
    ("Bottom Lashes", "Limpieza Dental"),
    ("West Palm Beach, FL", "Kissimmee, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-01-schnauzer.jpg" alt="Schnauzer recien bañado en la mesa de grooming de Pawsitive, con decoracion de huellitas en la pared" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-02-doodle.jpg" alt="Goldendoodle feliz con la lengua afuera en la mesa de grooming de Pawsitive" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="La experiencia" data-en="The experience">La experiencia</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Manos con" data-en="Hands with">Manos con</span><br /><span class="text-shine" data-es="paciencia real" data-en="real patience">paciencia real</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Pawsitive Grooming Salon &amp; Spa es el espacio de Stephanie Samalot en Kissimmee: grooming profesional para perros y gatos de todas las razas, desde el mini groom de un chihuahua hasta el full groom de un perro grande. Cada cita empieza con un ozone spa o un baño con champú a la medida del pelaje." data-en="Pawsitive Grooming Salon &amp; Spa is Stephanie Samalot\'s space in Kissimmee: professional grooming for dogs and cats of every breed, from a chihuahua\'s mini groom to a large dog\'s full groom. Every visit starts with an ozone spa or a bath with shampoo matched to the coat.">Pawsitive Grooming Salon &amp; Spa is Stephanie Samalot\'s space in Kissimmee: professional grooming for dogs and cats of every breed, from a chihuahua\'s mini groom to a large dog\'s full groom. Every visit starts with an ozone spa or a bath with shampoo matched to the coat.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 182 reseñas verificadas en Booksy, con dueños que repiten porque confían en Stephanie con perros ansiosos y gatos difíciles por igual, y un servicio bilingüe para toda la comunidad de Poinciana y Kissimmee." data-en="The result: a perfect 5.0 across 182 verified reviews on Booksy, with owners who keep coming back because they trust Stephanie with anxious dogs and difficult cats alike, and a bilingual service for the whole Poinciana and Kissimmee community.">The result: a perfect 5.0 across 182 verified reviews on Booksy, with owners who keep coming back because they trust Stephanie with anxious dogs and difficult cats alike, and a bilingual service for the whole Poinciana and Kissimmee community.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="182">182</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Atención personal</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,102,15,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Pawsitive Grooming Salon &amp; Spa" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,102,15,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Stephanie Samalot · <span class="text-[color:var(--ink-40)]" data-es="Groomer profesional" data-en="Professional groomer">Groomer profesional</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu visita, paso" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="a paso" data-en="by step">by step</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Reserva en Booksy" data-en="Book on Booksy">Reserva en Booksy</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges el servicio para tu perro o gato, con precio y duración claros, y confirmas al instante." data-en="Pick the service for your dog or cat, with clear price and duration, and confirm instantly.">Eliges el servicio para tu perro o gato, con precio y duración claros, y confirmas al instante.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Bienvenida y diagnóstico" data-en="Check-in &amp; assessment">Bienvenida y diagnóstico</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Stephanie revisa el pelaje, la piel y el temperamento de tu mascota antes de elegir el champú y el corte." data-en="Stephanie checks your pet\'s coat, skin and temperament before choosing the shampoo and cut.">Stephanie revisa el pelaje, la piel y el temperamento de tu mascota antes de elegir el champú y el corte.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Baño y grooming" data-en="Bath &amp; groom">Baño y grooming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Ozone spa o baño con champú natural, secado, corte según la raza, limpieza de oídos y corte de uñas, con calma y sin prisa." data-en="Ozone spa or a natural shampoo bath, blow-dry, breed-appropriate haircut, ear cleaning and a nail trim, unhurried.">Ozone spa o baño con champú natural, secado, corte según la raza, limpieza de oídos y corte de uñas, con calma y sin prisa.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Perfume y despedida" data-en="Perfume &amp; pickup">Perfume y despedida</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu mascota sale perfumada, con su bandana y lista para la foto, tal como cuentan las reseñas." data-en="Your pet leaves perfumed, wearing a bandana and ready for a photo, just like the reviews describe.">Tu mascota sale perfumada, con su bandana y lista para la foto, tal como cuentan las reseñas.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex + menu categorizado)
# ---------------------------------------------------------------------------
rep('data-es="Servicios" data-en="Services">Servicios</p>',
    'data-es="Servicios" data-en="Services">Servicios</p>', n=1)
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Grooming," data-en="Grooming,">Grooming,</span> <span class="text-shine" data-es="hecho con calma" data-en="done gently">hecho con calma</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Pawsitive Grooming en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pawsitive Grooming on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pawsitive Grooming en Booksy. Reserva con confirmación inmediata.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Más popular" data-en="Most popular">Más popular</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Ozone Spa Therapy</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Baño en spa con ozono para desinfectar, hidratar la piel y dejar el pelaje suave (solo baño, sin corte)." data-en="An ozone spa bath to disinfect, hydrate the skin and leave the coat soft (bath only, haircut not included).">Baño en spa con ozono para desinfectar, hidratar la piel y dejar el pelaje suave (solo baño, sin corte).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Solo baño" data-en="Bath only">Solo baño</p></div>
            <a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(194,102,15,0.4); box-shadow: 0 18px 50px rgba(46,33,21,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo más solicitado" data-en="Most requested">Lo más solicitado</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Full Grooming</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Baño, secado, corte según la raza, limpieza de oídos y corte y limado de uñas. Precio según el tamaño de tu perro, de $65 a $100." data-en="Bath, blow-dry, breed haircut, ear cleaning, and nail trim and filing. Priced by your dog\'s size, from $65 to $100.">Baño, secado, corte según la raza, limpieza de oídos y corte y limado de uñas. Precio según el tamaño de tu perro, de $65 a $100.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65-$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Bundle de uñas" data-en="Nail bundle">Bundle de uñas</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Pawdicure Deluxe</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte y limado de uñas, más limpieza de oídos e hidratación de almohadillas, para patas sanas entre baños." data-en="Nail trim and filing, plus ear cleaning and paw pad hydration, for healthy paws between baths.">Corte y limado de uñas, más limpieza de oídos e hidratación de almohadillas, para patas sanas entre baños.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$20</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Bundle" data-en="Bundle">Bundle</p></div>
            <a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Nuevo · Sin anestesia" data-en="New · Anesthesia-free">Nuevo · Sin anestesia</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Limpieza Dental Profunda" data-en="Deep Dental Cleaning">Limpieza Dental Profunda</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Profilaxis dental sin anestesia: elimina el sarro y el mal aliento, previene enfermedades y mejora la calidad de vida de tu mascota." data-en="Anesthesia-free dental prophylaxis: removes tartar and bad breath, prevents disease and improves your pet\'s quality of life.">Profilaxis dental sin anestesia: elimina el sarro y el mal aliento, previene enfermedades y mejora la calidad de vida de tu mascota.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Profilaxis" data-en="Prophylaxis">Profilaxis</p></div>
            <a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Baño y Spa" data-en="Bath &amp; Spa">Baño y Spa</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-2"><span data-es="Baño Small Dog" data-en="Bath, Small Dog">Baño Small Dog</span><span class="text-[color:var(--ink-40)]">$25</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Baño Medium Dog" data-en="Bath, Medium Dog">Baño Medium Dog</span><span class="text-[color:var(--ink-40)]">$35</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Baño Large Dog" data-en="Bath, Large Dog">Baño Large Dog</span><span class="text-[color:var(--ink-40)]">$45</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Baño XL Dog" data-en="Bath, XL Dog">Baño XL Dog</span><span class="text-[color:var(--ink-40)]">$55</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Medicated Shampoo" data-en="Medicated Shampoo">Medicated Shampoo</span><span class="text-[color:var(--ink-40)]">$15</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Herbal Flea &amp; Tick Treatment" data-en="Herbal Flea &amp; Tick Treatment">Herbal Flea &amp; Tick Treatment</span><span class="text-[color:var(--ink-40)]">$12</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Grooming Completo" data-en="Full Grooming">Grooming Completo</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-2"><span data-es="Full Grooming Small Dog" data-en="Full Grooming, Small Dog">Full Grooming Small Dog</span><span class="text-[color:var(--ink-40)]">$65</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Full Grooming Medium Dog" data-en="Full Grooming, Medium Dog">Full Grooming Medium Dog</span><span class="text-[color:var(--ink-40)]">$75</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Full Grooming Large Dog" data-en="Full Grooming, Large Dog">Full Grooming Large Dog</span><span class="text-[color:var(--ink-40)]">$90</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Full Grooming XL Dog" data-en="Full Grooming, XL Dog">Full Grooming XL Dog</span><span class="text-[color:var(--ink-40)]">$100</span></li>
            <li class="flex items-center justify-between gap-2"><span>Poodle &amp; Doodles</span><span class="text-[color:var(--ink-40)]">$70</span></li>
            <li class="flex items-center justify-between gap-2"><span>Puppy Cut</span><span class="text-[color:var(--ink-40)]">$55</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Tratamiento Deshedding" data-en="Deshedding Treatment">Tratamiento Deshedding</span><span class="text-[color:var(--ink-40)]">$50</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Full Grooming Gato" data-en="Full Grooming, Cat">Full Grooming Gato</span><span class="text-[color:var(--ink-40)]">$60-$70</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Uñas, Oídos y Extras" data-en="Nails, Ears &amp; Extras">Uñas, Oídos y Extras</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-2"><span data-es="Corte de uñas" data-en="Nail Trimming">Corte de uñas</span><span class="text-[color:var(--ink-40)]">$15</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Pintado de uñas" data-en="Nail Polish">Pintado de uñas</span><span class="text-[color:var(--ink-40)]">$10</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Limpieza de oídos" data-en="Ear Cleaning">Limpieza de oídos</span><span class="text-[color:var(--ink-40)]">$12</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Cepillado dental" data-en="Teeth Brushing">Cepillado dental</span><span class="text-[color:var(--ink-40)]">$15</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Recorte de cara" data-en="Face Trim">Recorte de cara</span><span class="text-[color:var(--ink-40)]">$8</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Grooming creativo" data-en="Creative Grooming">Grooming creativo</span><span class="text-[color:var(--ink-40)]">$5</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Tinte orejas y cola" data-en="Hair Dye, Ears &amp; Tail">Tinte orejas y cola</span><span class="text-[color:var(--ink-40)]">$20</span></li>
            <li class="flex items-center justify-between gap-2"><span>Perfume VIP Cologne</span><span class="text-[color:var(--ink-40)]">$25</span></li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Se habla español. Más de 40 servicios, menú completo y disponibilidad en Booksy." data-en="English &amp; Spanish spoken. 40+ services, full menu and availability on Booksy.">Se habla español. Más de 40 servicios, menú completo y disponibilidad en Booksy.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span>')
rep('''<a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_IG_HANDLE + '''
        </a>''',
    '''<a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_IG_HANDLE + '''
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Antes y después" data-en="Before and after">Antes y después</span><img src="assets/gallery-01-before-after.jpg" alt="Dos schnauzers antes y despues del grooming completo en Pawsitive" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Pawdicure con estilo" data-en="Pawdicure with style">Pawdicure con estilo</span><img src="assets/gallery-02-nails.jpg" alt="Pata de perro con uñas pintadas de colores tras un pawdicure en Pawsitive" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Baño con cariño" data-en="Bath time, gentle hands">Baño con cariño</span><img src="assets/gallery-03-cat-bath.jpg" alt="Gato recibiendo un baño con manos cuidadosas en Pawsitive Grooming" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Recién bañado" data-en="Fresh from the bath">Recién bañado</span><img src="assets/gallery-04-kitten-towel.jpg" alt="Gatito envuelto en toalla despues del baño en Pawsitive Grooming" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Grooming creativo" data-en="Creative grooming">Grooming creativo</span><img src="assets/gallery-05-rainbow-tail.jpg" alt="Cola de perro tenida en colores de arcoiris, servicio de grooming creativo en Pawsitive" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Uñas al detalle" data-en="Nails, done right">Uñas al detalle</span><img src="assets/gallery-06-paw-detail.jpg" alt="Detalle de corte de uñas de perro en Pawsitive Grooming" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="Lo que dicen" data-en="What their">What their</span> <span class="text-shine" data-es="sus clientes" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 182 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 182 verified reviews on Booksy">5.0 de 5 · 182 reseñas verificadas en Booksy</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Mi chica quedó de show. Muy profesional y muy amable, lo recomendaría, quedè encantada. Gracias"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Silvia R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente servicio siempre"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yomaira G.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Definitivamente es la mejor"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Midori</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 182 reseñas en Booksy" data-en="Read all 182 reviews on Booksy">Leer las 182 reseñas en Booksy</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Kissimmee</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,102,15,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">427 Arkansas Ct, Kissimmee, FL 34759</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,102,15,0.4)]" href="https://www.google.com/maps?q=427+Arkansas+Ct,+Kissimmee,+FL+34759" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,102,15,0.4)]" href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,102,15,0.4)]" href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,102,15,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los grooms más recientes de Stephanie y escribe por DM cualquier duda antes de tu cita." data-en="See Stephanie\'s latest grooms and DM any questions before your appointment.">Mira los grooms más recientes de Stephanie y escribe por DM cualquier duda antes de tu cita.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,102,15,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21l1.65-3.8a9 9 0 1 1 3.4 3.16L3 21"/><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0v1a5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"/></svg>
            <div>
              <p class="font-medium mb-1">WhatsApp</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Escríbenos directo para dudas rápidas o cambios de última hora." data-en="Message us directly for quick questions or last-minute changes.">Escríbenos directo para dudas rápidas o cambios de última hora.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,102,15,0.4)]" href="https://wa.me/14076559400" target="_blank" rel="noopener">(407) 655-9400</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Pawsitive Grooming Salon &amp; Spa, 427 Arkansas Ct, Kissimmee FL"
          src="https://www.google.com/maps?q=427+Arkansas+Ct,+Kissimmee,+FL+34759&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Cada cita, con mucho cariño." data-en="Every visit, with lots of love.">Cada cita, con mucho cariño.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Reserva el próximo" data-en="Book your pet\'s next">Book your pet\'s next</span> <span class="text-shine" data-es="grooming de tu mascota" data-en="grooming appointment">grooming appointment</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: un baño, el full grooming o el bundle de uñas que le toca a tu perro o gato." data-en="Book online in seconds: a bath, full grooming, or the nail bundle your dog or cat is due for.">Reserva online en segundos: un baño, el full grooming o el bundle de uñas que le toca a tu perro o gato.</p>')
rep('''<a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Pawsitive</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(246,217,160,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Pawsitive Grooming Salon &amp; Spa" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(246,217,160,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pawsitive Grooming</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Grooming para perros y gatos en Kissimmee, FL. Atención con cita previa." data-en="Dog &amp; cat grooming in Kissimmee, FL. By appointment only.">Grooming para perros y gatos en Kissimmee, FL. Atención con cita previa.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="hover:text-[#f6d9a0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>427 Arkansas Ct, Kissimmee, FL 34759</p>
        <p><a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="hover:text-[#f6d9a0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f6d9a0]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f6d9a0]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pawsitive Grooming Salon &amp; Spa.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Verificar que no quedo #f6d9a0 mal usado, dark-band hover ya cubierto por RGBA_PALETTE global (rgba(240,190,215->246,217,160)) asi que footer hover ya estaba en hex #f0bed7 -> #f6d9a0 por HEX_PALETTE. OK.
# ---------------------------------------------------------------------------

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("WRITE done ->", PATH)
