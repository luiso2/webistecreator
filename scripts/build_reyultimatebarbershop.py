import re
import colorsys

PATH = "output/reyultimatebarbershop/index.html"
h = open(PATH).read()

BOOKSY = "https://booksy.com/en-us/277397_rey-ultimate-barbershop_barber-shop_15889_miami"
IG_URL = "https://instagram.com/renato_dbarber"
IG_HANDLE = "@renato_dbarber"
ADDR = "14265 SW 42nd St, Miami, FL 33175"
ADDR_MAPQ = "14265+SW+42nd+St,+Miami,+FL+33175"


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:160]
    h = h.replace(a, b, n)


def block(start, end, new_content):
    """Replace text from `start` (inclusive) up to `end` (exclusive), asserting exactly one match."""
    global h
    pattern = re.escape(start) + r".*?(?=" + re.escape(end) + r")"
    matches = re.findall(pattern, h, flags=re.S)
    assert len(matches) == 1, "anchor count %d for start=%r" % (len(matches), start[:60])
    h = re.sub(pattern, lambda m: new_content.replace("\\", "\\\\"), h, count=1, flags=re.S)


# ---------- 1. Proteger el badge Merktop ----------
m = re.search(r"\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n", h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ================================================================
# 2. HEAD: title, meta, JSON-LD
# ================================================================
block(
    '  <title>Pure Artistry',
    '  <link rel="preconnect" href="https://fonts.googleapis.com" />',
    '''  <title>Ultimate Barbershop · Barbershop in Miami, FL | Fades, Beards &amp; Kids Cuts | 5.0 on Booksy</title>
  <meta name="description" content="Ultimate Barbershop, Miami FL: skin fades, beard lineups, kids cuts and the Full Groom by master barber Renato. 5.0 with 190 reviews on Booksy. Book online." />
  <meta property="og:title" content="Ultimate Barbershop · Barbershop in Miami, FL" />
  <meta property="og:description" content="Skin fades, beard lineups and kids cuts by master barber Renato. 5.0 on Booksy. Book online." />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="assets/raw/bk-4.jpg" />
  <link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Ultimate Barbershop",
    "alternateName": "Rey / Ultimate Barbershop",
    "description": "Barbershop in Miami, FL: skin fades, beard lineups, kids cuts and full grooming services by master barber Renato Sotomayor.",
    "address": { "@type": "PostalAddress", "streetAddress": "14265 SW 42nd St", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33175", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.73006728897618, "longitude": -80.42504330802639 },
    "sameAs": ["''' + BOOKSY + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "190", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Tuesday", "opens": "13:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Wednesday", "opens": "11:30", "closes": "21:05" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Thursday", "opens": "11:30", "closes": "21:15" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "11:30", "closes": "21:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "11:30", "closes": "18:30" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Barbershop services", "itemListElement": [
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Signature grooming service" } },
      { "@type": "Offer", "price": "36", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Complete grooming service" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "The Full Groom" } },
      { "@type": "Offer", "price": "36", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Kids haircut" } },
      { "@type": "Offer", "price": "18", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Beard trim+lineup" } }
    ] }
  }
  </script>
'''
)

# ================================================================
# 3. PRELOADER
# ================================================================
block(
    '<!-- PRELOADER DE MARCA -->',
    '<!-- BARRA DE PROGRESO DE SCROLL -->',
    '''<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">UB</span>
    <span class="pre-word">Ultimate Barbershop</span>
    <span class="pre-line"></span>
  </div>

  '''
)

# ================================================================
# 4. NAV
# ================================================================
block(
    '<!-- NAV -->',
    '<!-- HERO -->',
    '''<!-- NAV -->
  <header id="nav" class="fixed top-0 inset-x-0 z-50">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 h-[72px] flex items-center justify-between">
      <a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/bk-2.jpg" alt="Ultimate Barbershop" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Ultimate <span class="text-[color:var(--accent-deep)]">Barbershop</span></span>
      </a>
      <nav class="hidden md:flex items-center gap-7 text-sm font-light">
        <a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">The Experience</a>
        <a class="nav-link" href="#metodo" data-es="El Método" data-en="The Method">The Method</a>
        <a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Services</a>
        <a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>
        <a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>
        <a class="nav-link" href="#ubicacion" data-es="Ubicación" data-en="Location">Location</a>
      </nav>
      <div class="flex items-center gap-3">
        <button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Cambiar idioma">ES</button>
        <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Book now</span>
        </a>
        <button id="menuBtn" class="md:hidden w-10 h-10 flex flex-col items-center justify-center gap-[5px]" aria-label="Abrir menú">
          <span class="w-6 h-px bg-[color:var(--ink)]"></span>
          <span class="w-6 h-px bg-[color:var(--ink)]"></span>
          <span class="w-4 h-px bg-[color:var(--accent-deep)] self-end mr-2"></span>
        </button>
      </div>
    </div>
    <div id="mobileMenu" class="md:hidden hidden glass mx-4 mt-1 rounded-2xl overflow-hidden">
      <nav class="flex flex-col p-4 text-sm">
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="La Experiencia" data-en="The Experience">The Experience</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Method">The Method</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Services</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Gallery</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Reviews</a>
        <a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Location</a>
        <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Book now</a>
      </nav>
    </div>
  </header>

  '''
)

# ================================================================
# 5. HERO
# ================================================================
block(
    '<!-- HERO -->',
    '<!-- STRIP DE CONFIANZA -->',
    '''<!-- HERO -->
  <section id="top" class="relative min-h-screen flex items-center grain overflow-hidden pt-28 pb-16">
    <div class="glow-bg"><div class="orb orb-a" data-parallax="0.14"></div><div class="orb orb-b" data-parallax="0.09"></div><div class="orb orb-c" data-parallax="0.2"></div></div>
    <div id="heroInner" class="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Miami, FL · Barbería" data-en="Miami, FL · Barbershop">Miami, FL · Barbershop</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Cortes con precisión, sin prisa." data-en="Precision cuts, no rush.">Precision cuts, no rush.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Fades, delineado de barba" data-en="Skin fades, beard lineups">Skin fades, beard lineups</span><br /><span data-es="y grooming, hechos " data-en="and grooming, done ">and grooming, done </span><span class="text-shine" data-es="bien" data-en="right">right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Fades de precisión, delineado de barba nítido y servicios completos de grooming en Miami, FL. Renato perfecciona cortes desde el 2012, con un 5.0 perfecto en 190 reseñas en Booksy." data-en="Precision skin fades, sharp beard lineups and full grooming services in Miami, FL. Renato has been perfecting cuts since 2012, with a perfect 5.0 across 190 reviews on Booksy.">Precision skin fades, sharp beard lineups and full grooming services in Miami, FL. Renato has been perfecting cuts since 2012, with a perfect 5.0 across 190 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 190 reseñas en Booksy" data-en="5.0 · 190 reviews on Booksy">5.0 · 190 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + IG_HANDLE + '''
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-4.jpg" alt="Renato finishing a sharp beard lineup and skin fade on a client, profile view" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">The Full Groom</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $80 · 1h" data-en="From $80 · 1h">From $80 · 1h</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''
)

# ================================================================
# 6. STRIP DE CONFIANZA
# ================================================================
block(
    '<!-- STRIP DE CONFIANZA -->',
    '<!-- MARQUEE -->',
    '''<!-- STRIP DE CONFIANZA -->
  <section class="relative border-y border-[color:var(--accent-ghost)] bg-[color:var(--bg-2)]">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="190">190</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Skin Fades <span class="text-shine">&amp;</span> Beards</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Delineado de precisión" data-en="Precision lineups">Precision lineups</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Kids <span class="text-shine">&amp;</span> Grooming</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cortes pacientes y nítidos" data-en="Patient, sharp cuts">Patient, sharp cuts</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">SW 42nd St</p></div>
    </div>
  </section>

  '''
)

# ================================================================
# 7. MARQUEE #1
# ================================================================
MARQUEE_SEQ = '''<div class="marquee-seq">
        <span class="marquee-word">Skin Fades</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Beard Lineups</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Signature Grooming</span><span class="marquee-star">✦</span>
        <span class="marquee-word">The Full Groom</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Kids Cuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Miami, FL</span><span class="marquee-star">✦</span>
      </div>'''

block(
    '<!-- MARQUEE -->',
    '<!-- LA EXPERIENCIA -->',
    '''<!-- MARQUEE -->
  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">
      ''' + MARQUEE_SEQ + '''
      ''' + MARQUEE_SEQ + '''
    </div>
  </div>

  '''
)

# ================================================================
# 8. LA EXPERIENCIA
# ================================================================
block(
    '<!-- LA EXPERIENCIA -->',
    '<!-- EL METODO -->',
    '''<!-- LA EXPERIENCIA -->
  <section id="experiencia" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">01</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-14 items-center">
      <div class="frame zoomable aspect-[3/4] img-reveal max-w-md mx-auto lg:mx-0">
        <img src="assets/raw/bk-5.jpg" alt="Renato blending a skin fade with clippers and a comb, close-up of the cut in progress" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un barbero," data-en="One barber,">One barber,</span><br /><span class="text-shine" data-es="una década de confianza" data-en="a decade of trust">a decade of trust</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Ultimate Barbershop es la silla de Renato en Miami, FL: fades de precisión, delineado de barba nítido y grooming a la antigua, un cliente a la vez." data-en="Ultimate Barbershop is Renato's chair in Miami, FL: precision fades, sharp beard lineups and grooming done the old-school way, one client at a time.">Ultimate Barbershop is Renato's chair in Miami, FL: precision fades, sharp beard lineups and grooming done the old-school way, one client at a time.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientes lo dicen mejor que nadie: una reseña lo llama simplemente el mejor barbero de todo Miami, cortando el cabello de la misma familia por más de 10 años. Un 5.0 perfecto en 190 reseñas verificadas de Booksy." data-en="His clients say it best: one review calls him simply the best barber in all of Miami, cutting the same family's hair for over 10 years. A perfect 5.0 across 190 verified Booksy reviews.">His clients say it best: one review calls him simply the best barber in all of Miami, cutting the same family's hair for over 10 years. A perfect 5.0 across 190 verified Booksy reviews.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="190">190</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2012</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Barbero maestro desde" data-en="Master barber since">Master barber since</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="Ultimate Barbershop" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Ultimate Barbershop · <span class="text-[color:var(--ink-40)]" data-es="Barbero Maestro" data-en="Master Barber">Master Barber</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''
)

# ================================================================
# 9. EL METODO
# ================================================================
block(
    '<!-- EL METODO -->',
    '<!-- SERVICIOS -->',
    '''<!-- EL METODO -->
  <section id="metodo" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">02</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: fade, barba o el Full Groom, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: a fade, a beard lineup or the Full Groom, and confirm instantly.">Pick your service on Booksy with clear price and duration: a fade, a beard lineup or the Full Groom, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta" data-en="Consult">Consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Estilo, largo de guarda y forma de la barba: unos minutos para definir exactamente el corte que buscas." data-en="Style, guard length and beard shape: a few minutes to define exactly the cut you are after.">Style, guard length and beard shape: a few minutes to define exactly the cut you are after.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="El corte" data-en="The cut">The cut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Fade a máquina con mezcla de precisión y delineado de barba a navaja: cada detalle con su tiempo completo." data-en="Precision clipper work and a razor-sharp beard lineup: every detail gets its full time, no rushing.">Precision clipper work and a razor-sharp beard lineup: every detail gets its full time, no rushing.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el fade limpio, la barba nivelada y tu próxima cita lista para agendar en Booksy." data-en="You leave with a clean fade, a leveled beard and your next visit ready to book on Booksy.">You leave with a clean fade, a leveled beard and your next visit ready to book on Booksy.</p>
        </div>
      </div>
    </div>
  </section>

  '''
)

# ================================================================
# 10. SERVICIOS (5 cards, real data)
# ================================================================
block(
    '<!-- SERVICIOS -->',
    '<!-- GALERIA -->',
    '''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Services</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="corte" data-en="cut">cut</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Ultimate Barbershop en Booksy. La reserva confirma al instante." data-en="Prices and durations as published by Ultimate Barbershop on Booksy. Booking confirms instantly.">Prices and durations as published by Ultimate Barbershop on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Paquete insignia" data-en="Signature package">Signature package</p>
          <h3 class="font-display text-2xl leading-snug mb-3">The Full Groom</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La experiencia completa de Ultimate Barbershop: corte de precisión, esculpido de barba y delineado nítido, todo en una hora sin prisa con Renato." data-en="The complete Ultimate Barbershop experience: precision haircut, beard sculpting and a sharp lineup, all in one relaxed hour with Renato.">The complete Ultimate Barbershop experience: precision haircut, beard sculpting and a sharp lineup, all in one relaxed hour with Renato.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Corte insignia" data-en="Signature cut">Signature cut</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Signature Grooming Service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El fade o corte degradado insignia de Renato, terminado con un delineado limpio y nítido." data-en="Renato's signature fade or tapered cut, finished with a clean, sharp lineup.">Renato's signature fade or tapered cut, finished with a clean, sharp lineup.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Servicio completo" data-en="Full service">Full service</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Complete Grooming Service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte completo y arreglo de barba en una sola visita, rápido y nítido." data-en="A full haircut and beard tidy-up in one visit, fast and sharp.">A full haircut and beard tidy-up in one visit, fast and sharp.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$36</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">35min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para los más pequeños" data-en="For the little ones">For the little ones</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Kids Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un corte paciente y preciso para los clientes más jóvenes, fades y diseños bienvenidos." data-en="A patient, precise cut for the youngest clients, fades and designs welcome.">A patient, precise cut for the youngest clients, fades and designs welcome.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$36</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">35min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Retoque rápido" data-en="Quick touch-up">Quick touch-up</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Beard Trim + Lineup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un recorte y delineado de barba rápido y nítido para mantener tu forma fresca entre cortes completos." data-en="A quick, sharp beard trim and lineup to keep your shape fresh between full cuts.">A quick, sharp beard trim and lineup to keep your shape fresh between full cuts.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$18</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">20min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 5 servicios con sus precios y duraciones exactos publicados en Booksy." data-en="All 5 services with their exact prices and durations as published on Booksy.">All 5 services with their exact prices and durations as published on Booksy.</span></p>
    </div>
  </section>

  '''
)

# ================================================================
# 11. GALERIA (4 real photos: 1 wide + 3 tiles)
# ================================================================
block(
    '<!-- GALERIA -->',
    '<div class="marquee marquee-reverse"',
    '''<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Gallery</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span></h2>
        </div>
        <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + IG_HANDLE + '''
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Barba completa + fade fresco" data-en="Full beard + fresh fade">Full beard + fresh fade</span><img src="assets/raw/bk-7.jpg" alt="Client with a full beard, sharp neckline and a fresh fade, shown from behind" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Skin fade limpio" data-en="Clean skin fade">Clean skin fade</span><img src="assets/raw/bk-3.jpg" alt="Kid's clean skin fade with a sharp part line, side profile" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Fade con textura arriba" data-en="Textured top fade">Textured top fade</span><img src="assets/raw/bk-6.jpg" alt="Fade with a spiked, textured top, side view" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Fade + línea de diseño" data-en="Fade + hard part">Fade + hard part</span><img src="assets/raw/bk-8.jpg" alt="Fade with a textured top and a hard part design line" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''
)

# ================================================================
# 12. MARQUEE #2 (reverse)
# ================================================================
block(
    '<div class="marquee marquee-reverse" aria-hidden="true">',
    '<!-- OPINIONES -->',
    '''<div class="marquee marquee-reverse" aria-hidden="true">
    <div class="marquee-track">
      ''' + MARQUEE_SEQ + '''
      ''' + MARQUEE_SEQ + '''
    </div>
  </div>

  '''
)

# ================================================================
# 13. OPINIONES (3 real verbatim reviews)
# ================================================================
block(
    '<!-- OPINIONES -->',
    '<!-- UBICACION -->',
    '''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Reviews</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What his">What his</span> <span class="text-shine" data-es="sus clientes" data-en="clients say">clients say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 190 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 190 verified reviews on Booksy">5.0 out of 5 · 190 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great service, really nice cut, will come again"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">santiago c…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great service"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Miguelito</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing haircuts!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jennifer A…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 190 reseñas en Booksy" data-en="Read all 190 reviews on Booksy">Read all 190 reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''
)

# ================================================================
# 14. UBICACION (real address, real hours, Booksy, IG)
# ================================================================
block(
    '<!-- UBICACION -->',
    '<!-- CTA FINAL -->',
    '''<!-- UBICACION -->
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
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.google.com/maps?q=''' + ADDR_MAPQ + '''" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:180ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Tue 1:00 – 8:00 PM · Wed 11:30 AM – 9:05 PM</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Thu 11:30 AM – 9:15 PM · Fri 11:30 AM – 9:00 PM</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Sat 11:30 AM – 6:30 PM</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:220ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + BOOKSY + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los cortes más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest cuts and DM any questions before your visit.">See the latest cuts and DM any questions before your visit.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">''' + IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Ultimate Barbershop, 14265 SW 42nd St, Miami FL"
          src="https://www.google.com/maps?q=''' + ADDR_MAPQ + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
  </section>

  '''
)

# ================================================================
# 15. CTA FINAL
# ================================================================
block(
    '<!-- CTA FINAL -->',
    '<!-- FOOTER -->',
    '''<!-- CTA FINAL -->
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #191307 0%, #100c05 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Cortes con precisión, sin prisa." data-en="Precision cuts, no rush.">Precision cuts, no rush.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te espera" data-en="is waiting">is waiting</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu fade, tu delineado de barba, o el Full Groom que has querido probar." data-en="Book online in seconds: your fade, your beard lineup, or the Full Groom you have been meaning to try.">Book online in seconds: your fade, your beard lineup, or the Full Groom you have been meaning to try.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
        <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>
      </div>
    </div>
  </section>

  '''
)

# ================================================================
# 16. FOOTER
# ================================================================
block(
    '<!-- FOOTER -->',
    '<!-- Boton flotante de reserva -->',
    '''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#0c0905]">
    <span class="foot-mark" aria-hidden="true">Ultimate Barbershop</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="Ultimate Barbershop" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Ultimate Barbershop</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Barbería en Miami, FL. Con cita a través de Booksy." data-en="Barbershop in Miami, FL. By appointment via Booksy.">Barbershop in Miami, FL. By appointment via Booksy.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>''' + ADDR + '''</p>
        <p><a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · ''' + IG_HANDLE + '''</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 Ultimate Barbershop.</p>
        <a href="https://merktop.com" target="_blank" rel="noopener" class="merktop-badge">
          <span class="merktop-dot"></span>
          <span class="text-xs text-[#f4eee2]">Powered by <span class="font-semibold">Merktop</span></span>
        </a>
      </div>
    </div>
  </footer>

  '''
)

# ================================================================
# 17. BOTON FLOTANTE
# ================================================================
rep(
    '<a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + BOOKSY + '" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">'
)

# ================================================================
# 18. Palette: rotacion de matiz uniforme (gold amber #d4a84b -> steel-blue-slate)
# ================================================================
HUE_SHIFT = 170.0  # grados: gold ~40 -> ~210, masculine steel-blue-slate (distinto de los demas dark-v2 en curso)


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
    hexcode = mo.group(1)
    return '#' + shift_hex(hexcode)


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

open(PATH, 'w').write(h)
print('build OK: reyultimatebarbershop (HUE_SHIFT=%s)' % HUE_SHIFT)
