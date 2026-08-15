import re

SLUG = "progressiveelectrical"
PATH = f"output/{SLUG}/index.html"
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


TEL = "tel:+17279399473"
FB_URL = "https://www.facebook.com/rsgnic/"
MAPS_Q = "https://www.google.com/maps?q=40351+US+Hwy+19+N+%23304,+Tarpon+Springs,+FL+34689"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> navy blue (Progressive Electrical)
#    accent-deep #1f4e8c / accent-mid #3f7fc4 (brief), el resto de la escala
#    sigue la misma jerarquia de luminosidad ya validada por otros builds v2.
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#1f4e8c"),  # accent-deep
    ("#5c2140", "#0c2038"),  # btn-3d sole darkest
    ("#f0bed7", "#a9c1de"),  # dark-band shine/orb/stars accent
    ("#faf2f6", "#f2f5f8"),  # bg
    ("#c47a9c", "#3f7fc4"),  # accent-mid
    ("#8a5573", "#1c3c63"),  # dark-band btn shadow deep
    ("#f3e0ea", "#dce5ef"),  # bg-2 / accent-soft
    ("#d9a8c2", "#7899c2"),  # orb-b
    ("#7d3457", "#163255"),  # dark mid / step-num gradient end
    ("#5f2c48", "#0e2847"),  # shimmer stop / step-num gradient start
    ("#33222c", "#1c232b"),  # ink
    ("#fbf3f8", "#f2f6fb"),  # tile-cap text near-white
    ("#fbeff5", "#eaf1fa"),  # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#cddcee"),  # dark-band shimmer 3rd stop
    ("#f6f1ea", "#eaeff6"),  # theme-color meta
    ("#f2d5e3", "#cddbec"),  # orb-a
    ("#f2cfe0", "#c2d4e9"),  # dark-band shimmer last stop
    ("#efd0e0", "#c8d8eb"),  # dark-band btn-3d gradient mid
    ("#e5c1d4", "#a9c1de"),  # orb-c pale
    ("#dc9dbe", "#5780b3"),  # scroll-progress end stop
    ("#d3a2bc", "#8eaacd"),  # dark-band btn-3d gradient end light
    ("#c9789f", "#3d689c"),  # shimmer stop
    ("#b25a85", "#1f497d"),  # shimmer stop
    ("#2a1722", "#0b1a2c"),  # cta-final bg gradient start
    ("#1f0f18", "#07111e"),  # cta-final bg gradient end
    ("#1c0f16", "#08111d"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(31,78,140"),    # accent-deep alpha
    ("rgba(51,34,44", "rgba(28,35,43"),       # ink alpha
    ("rgba(240,190,215", "rgba(169,193,222"),  # dark-band light accent alpha
    ("rgba(70,25,50", "rgba(12,32,56"),       # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(242,245,248"),  # bg alpha (nav scrolled)
    ("rgba(125,52,87", "rgba(22,50,85"),      # dark mid alpha
    ("rgba(253,246,250", "rgba(242,246,251"),  # surface alpha
    ("rgba(40,16,30", "rgba(11,26,44"),       # tile-cap gradient dark
    ("rgba(233,205,186", "rgba(169,193,222"),  # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(63,108,163"),  # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: sin booking platform -> tel:. Facebook real en vez de IG (no hay IG verificado).
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, FB_URL)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Progressive Electrical Services, Inc. · Electrical Contractor in Tarpon Springs, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Progressive Electrical Services, Inc., Tarpon Springs FL: licensed electrical contractor since 1987. Residential, commercial and industrial work with 24-hour emergency service. 5.0 stars on Google. Call (727) 939-9473." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Progressive Electrical Services, Inc. · Electrical Contractor in Tarpon Springs, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Licensed electrical contractor since 1987. Residential, commercial and industrial work, 24-hour emergency service. Call (727) 939-9473." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-8.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/gmaps-8.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Electrician",
    "name": "Progressive Electrical Services, Inc.",
    "slogan": "Licensed electrical contractor serving Tampa Bay since 1987",
    "description": "Electrical contractor in Tarpon Springs, FL providing residential, commercial and industrial electrical services since 1987: panels, generators, architectural and landscape lighting, new construction and 24-hour emergency service.",
    "address": { "@type": "PostalAddress", "streetAddress": "40351 US Hwy 19 N #304", "addressLocality": "Tarpon Springs", "addressRegion": "FL", "postalCode": "34689", "addressCountry": "US" },
    "areaServed": "Pinellas, Pasco and Hillsborough Counties, FL",
    "telephone": "+1-727-939-9473",
    "email": "randy@rsgnic.com",
    "foundingDate": "1987",
    "image": "assets/raw/gmaps-8.jpg",
    "sameAs": ["https://www.facebook.com/rsgnic/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "40", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Electrical services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Commercial &amp; Industrial Electrical" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Residential Electrical &amp; Emergency Service" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Architectural &amp; Landscape Lighting" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "New Construction &amp; Electrical Installations" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN -> se queda en EN (default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. NAV (monograma texto en vez de logo.jpg -> no hay logo real; wordmark; preloader)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,78,140,0.35)]" />',
    '<span class="w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(31,78,140,0.35)] bg-[rgba(31,78,140,0.1)] text-[color:var(--accent-deep)]">PE</span>')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Progressive <span class="text-[color:var(--accent-deep)]">Electrical</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">PE</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Progressive Electrical</span>')
print("NAV done")

for old, new in [
    ('data-es="La Experiencia" data-en="The Experience">La Experiencia</a>',
     'data-es="Nosotros" data-en="About Us">About Us</a>'),
    ('data-es="El Método" data-en="The Method">El Método</a>',
     'data-es="Cómo Trabajamos" data-en="How We Work">How We Work</a>'),
    ('data-es="Servicios" data-en="Services">Servicios</a>',
     'data-es="Servicios" data-en="Services">Services</a>'),
    ('data-es="Galería" data-en="Gallery">Galería</a>',
     'data-es="Galería" data-en="Gallery">Gallery</a>'),
    ('data-es="Opiniones" data-en="Reviews">Opiniones</a>',
     'data-es="Por Qué Progressive" data-en="Why Progressive">Why Progressive</a>'),
    ('data-es="Ubicación" data-en="Location">Ubicación</a>',
     'data-es="Contacto" data-en="Contact">Contact</a>'),
]:
    rep_all(old, new, expect=2)
print("NAV LINKS done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar Ahora" data-en="Call Now">Call Now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar Ahora" data-en="Call Now">Call Now</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tarpon Springs, FL · Contratista Eléctrico" data-en="Tarpon Springs, FL · Electrical Contractor">Tarpon Springs, FL · Electrical Contractor</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Dando energía a Tampa Bay desde 1987." data-en="Powering Tampa Bay since 1987.">Powering Tampa Bay since 1987.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Electricistas con licencia," data-en="Licensed electricians,">Licensed electricians,</span><br /><span data-es="al servicio de Tampa Bay " data-en="serving Tampa Bay ">serving Tampa Bay </span><span class="text-shine" data-es="desde 1987" data-en="since 1987">since 1987</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Progressive Electrical Services realiza trabajos eléctricos residenciales, comerciales e industriales en los condados de Pinellas, Pasco y Hillsborough desde hace casi cuatro décadas, con electricistas con licencia y servicio de emergencia las 24 horas cuando algo no puede esperar." data-en="Progressive Electrical Services has handled residential, commercial and industrial electrical work across Pinellas, Pasco and Hillsborough counties for nearly four decades, with licensed crews and 24-hour emergency service when something cannot wait.">Progressive Electrical Services has handled residential, commercial and industrial electrical work across Pinellas, Pasco and Hillsborough counties for nearly four decades, with licensed crews and 24-hour emergency service when something cannot wait.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 40 reseñas en Google" data-en="5.0 · 40 reviews on Google">5.0 · 40 reviews on Google</span>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + FB_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @_lashbloom
          </a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llamar (727) 939-9473" data-en="Call (727) 939-9473">Call (727) 939-9473</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + FB_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
            <span data-es="Facebook" data-en="Facebook">Facebook</span>
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-8.jpg" alt="Landscape and architectural lighting installed by Progressive Electrical Services at a Tampa Bay area home" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Siempre Disponibles" data-en="Always On Call">Always On Call</p>
            <p class="font-display text-lg" data-es="Servicio 24 Horas" data-en="24-Hour Service">24-Hour Service</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Residencial · Comercial · Industrial" data-en="Residential · Commercial · Industrial">Residential · Commercial · Industrial</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="40">40</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl"><span data-es="Desde" data-en="Est.">Est.</span> <span class="text-shine">1987</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="39 años en Tampa Bay" data-en="39 years in Tampa Bay">39 years in Tampa Bay</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span data-es="Licencia" data-en="FL Lic.">FL Lic.</span> <span class="text-shine">EC0001666</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Contratista eléctrico certificado" data-en="Certified Electrical Contractor">Certified Electrical Contractor</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Tarpon Springs</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Pinellas, Pasco y Hillsborough" data-en="Pinellas, Pasco &amp; Hillsborough">Pinellas, Pasco &amp; Hillsborough</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Commercial Electrical"),
    ("Hybrid Set", "Residential Electrical"),
    ("Volume Set", "Industrial Installations"),
    ("Mega Volume", "Architectural Lighting"),
    ("Bottom Lashes", "24-Hour Emergency Service"),
    ("West Palm Beach, FL", "Tarpon Springs, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (Nosotros)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-7.jpg" alt="Progressive Electrical Services crew wiring a boat lift on a Tampa Bay dock" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-1.jpg" alt="Progressive Electrical Services technician working on commercial switchgear and generator equipment" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="Nosotros" data-en="About Us">About Us</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Cuatro décadas" data-en="Four decades">Four decades</span><br /><span class="text-shine" data-es="de trabajo con licencia" data-en="of licensed electrical work">of licensed electrical work</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Progressive Electrical Services, Inc. es el contratista eléctrico de Tarpon Springs desde 1987, dirigido por el presidente Randall S. Graber bajo la licencia de Contratista Eléctrico Certificado de Florida EC0001666. El equipo se encarga de todo, desde paneles de servicio y generadores hasta iluminación de paisaje y construcción nueva, para propietarios y negocios de toda el área de Tampa Bay." data-en="Progressive Electrical Services, Inc. has been Tarpon Springs&#39; electrical contractor since 1987, led by president Randall S. Graber under Florida Certified Electrical Contractor license EC0001666. The crew handles everything from service panels and generators to landscape lighting and new construction, for homeowners and businesses across the Tampa Bay area.">Progressive Electrical Services, Inc. has been Tarpon Springs&#39; electrical contractor since 1987, led by president Randall S. Graber under Florida Certified Electrical Contractor license EC0001666. The crew handles everything from service panels and generators to landscape lighting and new construction, for homeowners and businesses across the Tampa Bay area.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Cada trabajo, grande o pequeño, lo hacen electricistas con licencia que llegan, lo hacen bien y responden por su trabajo. Ese enfoque ha mantenido a los clientes llamando de vuelta para proyectos residenciales, comerciales e industriales en los condados de Pinellas, Pasco y Hillsborough durante casi 40 años." data-en="Every job, big or small, is done by licensed electricians who show up, do the work right, and stand behind it. That approach has kept clients calling back for residential, commercial and industrial projects across Pinellas, Pasco and Hillsborough counties for nearly 40 years.">Every job, big or small, is done by licensed electricians who show up, do the work right, and stand behind it. That approach has kept clients calling back for residential, commercial and industrial projects across Pinellas, Pasco and Hillsborough counties for nearly 40 years.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="40">40</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">A+</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Calificación BBB" data-en="BBB Rating">BBB Rating</p></div>''')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,78,140,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>''',
    '''<span class="blur-up loaded w-10 h-10 rounded-full flex items-center justify-center font-display text-sm ring-1 ring-[rgba(31,78,140,0.3)] bg-[rgba(31,78,140,0.1)] text-[color:var(--accent-deep)]">PE</span>
            <span class="text-sm font-light">Randall S. Graber · <span class="text-[color:var(--ink-40)]" data-es="Presidente" data-en="President">President</span></span>''')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO -> COMO TRABAJAMOS
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Cómo trabajamos, paso a paso" data-en="How we work, step by step">How we work, step by step</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="El trabajo," data-en="The job,">The job,</span> <span class="text-shine" data-es="hecho con cuidado" data-en="done with care">done with care</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Llama o pide servicio" data-en="Call or Request Service">Call or Request Service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llama al (727) 939-9473 y describe lo que necesitas, desde un breaker disparado hasta una actualización de panel completa. La oficina te conecta con un electricista con licencia." data-en="Call (727) 939-9473 and describe what needs attention, from a tripped breaker to a full panel upgrade. The office connects you with a licensed electrician.">Call (727) 939-9473 and describe what needs attention, from a tripped breaker to a full panel upgrade. The office connects you with a licensed electrician.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Evaluación en el sitio" data-en="On-Site Evaluation">On-Site Evaluation</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Un técnico de Progressive Electrical inspecciona el trabajo en persona y explica lo que se necesita para hacerlo con seguridad y conforme al código antes de empezar." data-en="A Progressive Electrical technician inspects the job in person and explains what it takes to do it safely and up to code before any work begins.">A Progressive Electrical technician inspects the job in person and explains what it takes to do it safely and up to code before any work begins.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Trabajo con licencia, conforme al código" data-en="Licensed, Code-Compliant Work">Licensed, Code-Compliant Work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El trabajo se realiza bajo la licencia de Contratista Eléctrico Certificado de Florida EC0001666, ya sea un panel de servicio, una conexión de generador o una instalación de iluminación." data-en="Work is carried out under Florida Certified Electrical Contractor license EC0001666, whether it is a service panel, generator hookup or lighting install.">Work is carried out under Florida Certified Electrical Contractor license EC0001666, whether it is a service panel, generator hookup or lighting install.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Soporte de emergencia 24 horas" data-en="24-Hour Emergency Support">24-Hour Emergency Support</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Clientes residenciales, comerciales e industriales pueden contactar al equipo a cualquier hora cuando un problema eléctrico no puede esperar al horario regular." data-en="Residential, commercial and industrial clients can reach the team around the clock when an electrical issue cannot wait for regular hours.">Residential, commercial and industrial clients can reach the team around the clock when an electrical issue cannot wait for regular hours.</p>''')
print("METODO done")

open(PATH, "w", encoding="utf-8").write(h)
print("PART 1 WRITTEN")
