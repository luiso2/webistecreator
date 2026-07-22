import re

PATH = "output/heights-barbershop-chris/index.html"
h = open(PATH).read()

BOOKSY = "https://booksy.com/en-us/425212_the-heights-barbershop-chris_barber-shop_15761_tampa"
IG_URL = "https://www.instagram.com/theheightsbarbershop/"
IG_HANDLE = "@theheightsbarbershop"
ADDR = "6500 N Florida Ave, Tampa, FL 33604"
ADDR_MAPQ = "6500+N+Florida+Ave,+Tampa,+FL+33604"


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
    '''  <title>The Heights Barbershop &middot; Barbershop in Tampa, FL | Fades, Beard Trims &amp; Haircuts | 5.0 on Booksy</title>
  <meta name="description" content="The Heights Barbershop, Tampa FL: bald fades, beard trims, haircuts and senior cuts by Chris Copeland and Dakota. 5.0 with 301 reviews on Booksy. Book online." />
  <meta property="og:title" content="The Heights Barbershop &middot; Barbershop in Tampa, FL" />
  <meta property="og:description" content="Bald fades, beard trims and honest haircuts in Tampa, FL. 5.0 on Booksy. Book online." />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="assets/raw/bk-16.jpg" />
  <link rel="icon" type="image/jpeg" href="assets/raw/bk-13.jpg" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "The Heights Barbershop",
    "description": "Barbershop in Tampa, FL: bald fades, beard trims, haircuts and senior cuts by Chris Copeland and Dakota.",
    "address": { "@type": "PostalAddress", "streetAddress": "6500 N Florida Ave", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33604", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.00684, "longitude": -82.45967 },
    "sameAs": ["''' + BOOKSY + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "301", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "10:00", "closes": "12:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Friday"], "opens": "10:00", "closes": "13:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Tuesday", "opens": "14:30", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Wednesday", "opens": "14:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Thursday", "opens": "09:30", "closes": "13:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Thursday", "opens": "14:00", "closes": "15:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "14:00", "closes": "16:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:30", "closes": "15:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Barbershop services", "itemListElement": [
      { "@type": "Offer", "price": "31", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut" } },
      { "@type": "Offer", "price": "36", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Bald fade" } },
      { "@type": "Offer", "price": "38", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Haircut & Beard trim" } },
      { "@type": "Offer", "price": "15", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Beard trim" } },
      { "@type": "Offer", "price": "40", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Bald Fade & Beard Trim" } },
      { "@type": "Offer", "price": "25", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Senior citizen cut" } }
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
    <span class="pre-mono">HB</span>
    <span class="pre-word">The Heights Barbershop</span>
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
        <img src="assets/raw/bk-13.jpg" alt="The Heights Barbershop" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">The Heights <span class="text-[color:var(--accent-deep)]">Barbershop</span></span>
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
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Tampa, FL · Barbería" data-en="Tampa, FL · Barbershop">Tampa, FL · Barbershop</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Fades nítidos, buena conversación." data-en="Sharp fades, real conversation.">Sharp fades, real conversation.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Fades, arreglo de barba" data-en="Fades, beard trims">Fades, beard trims</span><br /><span data-es="y cortes, hechos " data-en="and haircuts, done ">and haircuts, done </span><span class="text-shine" data-es="bien" data-en="right">right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Bald fades de precisión, arreglo de barba nítido y cortes honestos en Tampa, FL. Chris Copeland y Dakota mantienen las sillas ocupadas con buen ambiente de garage y un 5.0 perfecto en 301 reseñas en Booksy." data-en="Precision bald fades, sharp beard trims and honest haircuts in Tampa, FL. Chris Copeland and Dakota keep the chairs busy with a cool garage vibe and a perfect 5.0 across 301 reviews on Booksy.">Precision bald fades, sharp beard trims and honest haircuts in Tampa, FL. Chris Copeland and Dakota keep the chairs busy with a cool garage vibe and a perfect 5.0 across 301 reviews on Booksy.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 301 reseñas en Booksy" data-en="5.0 · 301 reviews on Booksy">5.0 · 301 reviews on Booksy</span>
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
            <img src="assets/raw/bk-16.jpg" alt="Freshly finished bald fade on a client at The Heights Barbershop, shown from behind" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Bald Fade</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $36 · 45min" data-en="From $36 · 45min">From $36 · 45min</p>
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
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="301">301</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fades <span class="text-shine">&amp;</span> Beards</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Nítidos, siempre" data-en="Sharp, every time">Sharp, every time</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">All <span class="text-shine">Ages</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="De niños a mayores" data-en="Kids to seniors welcome">Kids to seniors welcome</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">N Florida Ave</p></div>
    </div>
  </section>

  '''
)

# ================================================================
# 7. MARQUEE #1
# ================================================================
MARQUEE_SEQ = '''<div class="marquee-seq">
        <span class="marquee-word">Bald Fades</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Beard Trims</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Haircuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Senior Cuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Garage Vibe</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Tampa Heights, FL</span><span class="marquee-star">✦</span>
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
      <div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-1.jpg" alt="Shop interior at The Heights Barbershop, with barber chairs and retro wall decor" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-11.jpg" alt="Barber cutting a client's hair mid-service, cape draped over the client" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">The experience</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Dos barberos," data-en="Two barbers,">Two barbers,</span><br /><span class="text-shine" data-es="un solo ambiente de garage" data-en="one cool Tampa vibe">one cool Tampa vibe</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="The Heights Barbershop es la barbería de Dakota y Chris Copeland en Tampa, FL: bald fades de precisión, arreglo de barba nítido y cortes honestos, dentro de un espacio estilo garage que se siente como la casa de un amigo, no una cadena." data-en="The Heights Barbershop is Dakota and Chris Copeland's shop in Tampa, FL: precision bald fades, sharp beard trims and honest haircuts, inside a garage-style space that feels like a friend's place, not a chain.">The Heights Barbershop is Dakota and Chris Copeland's shop in Tampa, FL: precision bald fades, sharp beard trims and honest haircuts, inside a garage-style space that feels like a friend's place, not a chain.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Los clientes vuelven tanto por la conversación como por el corte. Una reseña lo describe simplemente como un ambiente de garage genial con barberos simpáticos y divertidos. Un 5.0 perfecto en 301 reseñas verificadas de Booksy." data-en="Clients keep coming back for the conversation as much as the cut. One review calls it simply a cool garage vibe with engaging and funny barbers. A perfect 5.0 across 301 verified Booksy reviews.">Clients keep coming back for the conversation as much as the cut. One review calls it simply a cool garage vibe with engaging and funny barbers. A perfect 5.0 across 301 verified Booksy reviews.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="301">301</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Barberos en silla" data-en="Barbers on the chair">Barbers on the chair</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-13.jpg" alt="The Heights Barbershop" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">The Heights Barbershop · <span class="text-[color:var(--ink-40)]" data-es="Chris &amp; Dakota" data-en="Chris &amp; Dakota">Chris &amp; Dakota</span></span>
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: corte, bald fade o arreglo de barba, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: a haircut, a bald fade or a beard trim, and confirm instantly.">Pick your service on Booksy with clear price and duration: a haircut, a bald fade or a beard trim, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta" data-en="Consult">Consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Altura del fade, largo de guarda y forma de la barba: unos minutos para definir exactamente el corte que buscas." data-en="Fade height, guard length and beard shape: a few minutes to define exactly the cut you are after.">Fade height, guard length and beard shape: a few minutes to define exactly the cut you are after.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="El corte" data-en="The cut">The cut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Fade a máquina con mezcla de precisión y arreglo de barba nítido: cada detalle con su tiempo completo, sin apuros." data-en="Precision clipper fade work and a sharp beard trim: every detail gets its full time, no rushing.">Precision clipper fade work and a sharp beard trim: every detail gets its full time, no rushing.</p>
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
# 10. SERVICIOS (4 cards, real data, 6 services covered)
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
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por The Heights Barbershop en Booksy. La reserva confirma al instante." data-en="Prices and durations as published by The Heights Barbershop on Booksy. Booking confirms instantly.">Prices and durations as published by The Heights Barbershop on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="El clásico" data-en="The classic">The classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un corte honesto y prolijo, tijera y máquina, para salir listo en 30 minutos." data-en="An honest, clean haircut with shears and clippers, in and out in 30 minutes.">An honest, clean haircut with shears and clippers, in and out in 30 minutes.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$31</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35); transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="El más pedido" data-en="Most booked">Most booked</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Bald Fade</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El bald fade insignia de la casa: piel limpia, mezcla perfecta y una línea nítida de principio a fin." data-en="The house signature bald fade: skin-clean blend and a sharp line from start to finish.">The house signature bald fade: skin-clean blend and a sharp line from start to finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$36</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">45min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Combos de corte y barba" data-en="Cut + beard combos">Cut + beard combos</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte &amp; Arreglo de Barba" data-en="Haircut &amp; Beard Combos">Haircut &amp; Beard Combos</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Haircut &amp; Beard trim por $38 (40min), o llévalo al máximo con Bald Fade &amp; Beard Trim por $40 (45min)." data-en="Haircut &amp; Beard trim for $38 (40min), or go all in with Bald Fade &amp; Beard Trim for $40 (45min).">Haircut &amp; Beard trim for $38 (40min), or go all in with Bald Fade &amp; Beard Trim for $40 (45min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$38+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min+</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Barba y descuentos" data-en="Beard &amp; senior specials">Beard &amp; senior specials</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Arreglo de Barba &amp; Corte Senior" data-en="Beard Trim &amp; Senior Cut">Beard Trim &amp; Senior Cut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un arreglo de barba rápido y nítido por $15 (20min), o un corte de precio especial para adultos mayores por $25 (30min)." data-en="A quick, sharp beard trim for $15 (20min), or a discounted haircut for senior citizens for $25 (30min).">A quick, sharp beard trim for $15 (20min), or a discounted haircut for senior citizens for $25 (30min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$15+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">20min+</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Los 6 servicios con sus precios y duraciones exactos publicados en Booksy." data-en="All 6 services with their exact prices and durations as published on Booksy.">All 6 services with their exact prices and durations as published on Booksy.</span></p>
    </div>
  </section>

  '''
)

# ================================================================
# 11. GALERIA (1 wide + 5 tiles, real curated photos)
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
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Fade fresco, acabado limpio" data-en="Fresh fade, clean finish">Fresh fade, clean finish</span><img src="assets/raw/bk-16.jpg" alt="Client's bald fade freshly blended, shown from behind, wide shot" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Fade de perfil" data-en="Side profile fade">Side profile fade</span><img src="assets/raw/bk-13.jpg" alt="Client with a slicked back fade, side profile view" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Acabado nítido" data-en="Sharp finish">Sharp finish</span><img src="assets/raw/bk-8.jpg" alt="Client wearing a mask, showing a finished fade result" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Fresco y limpio" data-en="Fresh and clean">Fresh and clean</span><img src="assets/raw/bk-14.jpg" alt="Client wearing a mask with a fresh, clean fade, side view" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="También cortes para niños" data-en="Kids cuts too">Kids cuts too</span><img src="assets/raw/bk-2.jpg" alt="Young client's mohawk haircut, showing the shop cuts kids too" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Look completo, bien hecho" data-en="Full look, done right">Full look, done right</span><img src="assets/raw/bk-6.jpg" alt="Bearded client's finished portrait after a haircut and beard trim" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
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
# 13. OPINIONES (3 real verbatim named reviews)
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
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What our">What our</span> <span class="text-shine" data-es="nuestros clientes" data-en="clients say">clients say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 301 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 301 verified reviews on Booksy">5.0 out of 5 · 301 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Cool garage vibe, engaging and funny barbers topped with an excellent haircut/beard trim."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Dan M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great cut and great guy!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Shawn H…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Best in the game, always on point…"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Bernie M…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 301 reseñas en Booksy" data-en="Read all 301 reviews on Booksy">Read all 301 reviews on Booksy</a>
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
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Tampa</span></h2>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light">Mon 10:00 AM &ndash; 12:00 PM · Tue, Wed, Fri 10:00 AM &ndash; 1:00 PM</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Tue 2:30 &ndash; 6:00 PM · Wed 2:00 &ndash; 6:00 PM · Thu 9:30 AM &ndash; 1:00 PM &amp; 2:00 &ndash; 3:00 PM</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">Fri 2:00 &ndash; 4:30 PM · Sat 9:30 AM &ndash; 3:00 PM</p>
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
        <iframe title="Map: The Heights Barbershop, 6500 N Florida Ave, Tampa FL"
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
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Fades nítidos, buena conversación." data-en="Sharp fades, real conversation.">Sharp fades, real conversation.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te espera" data-en="is waiting">is waiting</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu bald fade, tu arreglo de barba, o el combo de corte y barba que has querido probar." data-en="Book online in seconds: your bald fade, your beard trim, or the haircut and beard combo you have been meaning to try.">Book online in seconds: your bald fade, your beard trim, or the haircut and beard combo you have been meaning to try.</p>
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
    <span class="foot-mark" aria-hidden="true">The Heights Barbershop</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-13.jpg" alt="The Heights Barbershop" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">The Heights Barbershop</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Barbería en Tampa, FL. Con cita a través de Booksy." data-en="Barbershop in Tampa, FL. By appointment via Booksy.">Barbershop in Tampa, FL. By appointment via Booksy.</p>
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
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 The Heights Barbershop.</p>
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
# 18. Idioma por defecto: EN (dark-v2 ya es EN-default de fabrica: <html lang="en">
#     y applyLang(lang === 'es' ? 'es' : 'en') ya cae a 'en' salvo navigator.language 'es'.
#     Se verifican ambas anclas tal cual, sin invertir la ternaria.)
# ================================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h

# ================================================================
# 19. Paleta: gold -> steel/denim blue (accent-deep #3f6b8a, accent-mid #6a94ad)
#     Proteger merktop-badge ya hecho en el paso 1 (placeholder @@BADGE@@)
# ================================================================
HEX_PAIRS = [
    ('#d4a84b', '#3f6b8a'),  # accent-deep
    ('#b8934a', '#6a94ad'),  # accent-mid
    ('#f0dc9e', '#aad0ec'),  # shimmer light stop
    ('#9a7431', '#2c4a61'),  # shimmer/step-num dark stop
    ('#e5c374', '#82b4d8'),  # shimmer light-mid stop
    ('#e8c476', '#86b8dc'),  # btn-3d top gradient
    ('#c9a04a', '#6a94ad'),  # btn-3d mid gradient (reuse accent-mid)
    ('#96742c', '#2a4d68'),  # btn-3d/scroll-progress dark stop
    ('#6b5222', '#1f3a4d'),  # btn-3d/book-float shadow base
    ('#1c1408', '#0d1720'),  # btn-3d text/icon color
    ('#e9c3ab', '#a8c9dc'),  # dark-band stars / footer hover text
    ('#8a744a', '#3f6b8a'),  # dark-band btn-3d shadow base (reuse accent-deep)
    ('#e8cf96', '#a0c8e0'),  # dark-band text-shine / orb / cursor-glow light stop
    ('#f8eed3', '#dcebf5'),  # dark-band text-shine very light stop
    ('#bfa060', '#5f89a8'),  # dark-band text-shine mid-dark stop
    ('#f0dcae', '#b7d6ec'),  # dark-band text-shine last stop
    ('#faf1dc', '#e0ecf5'),  # dark-band btn-3d top gradient
    ('#ecd9a8', '#a9cfe6'),  # dark-band btn-3d mid gradient
    ('#c9ab6b', '#6a94ad'),  # dark-band btn-3d bottom gradient (reuse accent-mid)
    ('#241c0e', '#101a24'),  # accent-soft variable
]
for old, new in HEX_PAIRS:
    assert old in h, "paleta hex no encontrado: " + old
    h = h.replace(old, new)

RGB_PAIRS = [
    ('212,168,75', '63,107,138'),   # accent-deep rgb (rgba usages, all alphas)
    ('232,207,150', '160,200,224'),  # e8cf96 rgb (dark-band / cursor-glow)
    ('232,210,160', '162,202,225'),  # dark-band accent-ghost rgb
    ('80,58,18', '24,40,54'),        # btn-3d inset shadow
    ('110,85,35', '28,48,64'),       # dark-band btn-3d inset shadow
    ('122,90,30', '30,55,75'),       # orb-b background
    ('180,140,60', '90,130,160'),    # orb-c background
    ('185,138,128', '120,150,175'),  # dark-band orb-b background
    ('54,42,38', '30,38,46'),        # btn-ghost hover shadow
]
for old, new in RGB_PAIRS:
    assert old in h, "paleta rgb no encontrado: " + old
    h = h.replace(old, new)

h = h.replace('@@BADGE@@', badge_block, 1)

open(PATH, 'w').write(h)
print('build OK: heights-barbershop-chris')
