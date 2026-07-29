#!/usr/bin/env python3
"""Derivacion anclada de CONTENIDO (paleta ya rotada previamente):
output/fivestarsdominicansalon/index.html (copia paletizada de templates/dark-v2)
-> output/fivestarsdominicansalon/index.html (contenido real de 5 Stars Dominican
Beauty Salon & Barbershop, North Miami / Miami FL). NO se toca ningun color/hex/rgba,
NO se toca el merktop-badge (se reutiliza intacto).
"""
import re

SRC = 'output/fivestarsdominicansalon/index.html'
DST = 'output/fivestarsdominicansalon/index.html'

h = open(SRC, encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'ANCLA ROTA: ' + a[:160]
    h = h.replace(a, b, n)


BK = 'https://booksy.com/en-us/443207_5starsdominican-beauty-salon-barbershop_hair-salon_15889_miami'
IG = 'https://www.instagram.com/5_stars_dominican_beauty_salon/'
IG_HANDLE = '@5_stars_dominican_beauty_salon'
BRAND = '5 Stars Dominican Beauty Salon &amp; Barbershop'
BRAND_PLAIN = '5 Stars Dominican Beauty Salon & Barbershop'

# ============================================================
# 1. HEAD: title, meta, og, JSON-LD (paleta/badge NO se tocan)
# ============================================================
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    f'<title>{BRAND} · Hair Salon &amp; Barbershop in Miami, FL | Hair Botox, Keratin &amp; Cuts | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    f'<meta name="description" content="{BRAND_PLAIN}, Miami FL: hair botox, keratin treatments, silk-smooth blowouts, curly cuts and men\'s cuts with stylist Johanne Vital. 5.0 with 74 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    f'<meta property="og:title" content="{BRAND} · Hair Salon &amp; Barbershop in Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Hair botox, keratin, blowouts and cuts for women and men. 5.0 on Booksy. Book online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-9.jpg" />',
)
# favicon ya es assets/raw/bk-2.jpg (logo real del negocio): se deja intacto.

m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m, 'no se encontro JSON-LD'
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "5 Stars Dominican Beauty Salon & Barbershop",
    "description": "Hair salon and barbershop in North Miami, FL: hair botox, keratin treatments, silk-smooth blowouts and curly cuts for women, plus cuts and grooming for men, with stylist Johanne Vital.",
    "address": { "@type": "PostalAddress", "streetAddress": "631 NE 125th St", "addressLocality": "North Miami", "addressRegion": "FL", "postalCode": "33161", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 25.89057, "longitude": -80.18551 },
    "sameAs": ["https://booksy.com/en-us/443207_5starsdominican-beauty-salon-barbershop_hair-salon_15889_miami", "https://www.instagram.com/5_stars_dominican_beauty_salon/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "74", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:55", "closes": "18:55" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:55", "closes": "19:10" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Hair services", "itemListElement": [
      { "@type": "Offer", "price": "60", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Female Haircut" } },
      { "@type": "Offer", "price": "176", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Hair Botox" } },
      { "@type": "Offer", "price": "72", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Curly Hair Cut" } },
      { "@type": "Offer", "price": "200", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Keratin Hair Treatment" } }
    ] }
  }
  </script>'''
h = h[:m.start()] + NEW_JSONLD + h[m.end():]

print('OK: head + JSON-LD')

# ============================================================
# 2. IDIOMA: dark-v2 ya es EN default -> sin cambios (solo se verifica)
# ============================================================
assert "applyLang(lang === 'es' ? 'es' : 'en')" in h
assert '<html lang="en"' in h

# ============================================================
# 3. SEGMENTACION POR MARCADORES DE COMENTARIO
# ============================================================
def idx(marker, start=0):
    i = h.find(marker, start)
    assert i != -1, 'MARCADOR NO ENCONTRADO: ' + marker
    return i


i_preloader = idx('<!-- PRELOADER DE MARCA -->')
i_scroll = idx('<!-- BARRA DE PROGRESO DE SCROLL -->')
i_nav = idx('<!-- NAV -->')
i_hero = idx('<!-- HERO -->')
i_strip = idx('<!-- STRIP DE CONFIANZA -->')
i_marquee1 = idx('<!-- MARQUEE -->')
i_experiencia = idx('<!-- LA EXPERIENCIA -->')
i_metodo = idx('<!-- EL METODO -->')
i_servicios = idx('<!-- SERVICIOS -->')
i_galeria = idx('<!-- GALERIA -->')
i_marquee2 = idx('<!-- MARQUEE -->', i_experiencia)
i_opiniones = idx('<!-- OPINIONES -->')
i_ubicacion = idx('<!-- UBICACION -->')
i_cta = idx('<!-- CTA FINAL -->')
i_footer = idx('<!-- FOOTER -->')
i_bookfloat = idx('<!-- Boton flotante de reserva -->')
i_cursorring = idx('<div id="cursorRing"')

seg_head = h[:i_preloader]
seg_scroll = h[i_scroll:i_nav]
seg_footer_orig = h[i_footer:i_bookfloat]
seg_tail = h[i_cursorring:]

print('OK: segmentacion por anclas de comentario')

# ============================================================
# PRELOADER
# ============================================================
NEW_PRELOADER = '''<!-- PRELOADER DE MARCA -->
  <div id="preloader" aria-hidden="true">
    <span class="pre-mono">5S</span>
    <span class="pre-word">5 Stars Dominican</span>
    <span class="pre-line"></span>
  </div>

  '''

# ============================================================
# NAV
# ============================================================
NEW_NAV = f'''<!-- NAV -->
  <header id="nav" class="fixed top-0 inset-x-0 z-50">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 h-[72px] flex items-center justify-between">
      <a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/bk-2.jpg" alt="5 Stars Dominican Beauty Salon &amp; Barbershop logo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(213,60,85,0.35)] bg-white" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">5 Stars <span class="text-[color:var(--accent-deep)]">Dominican</span></span>
      </a>
      <nav class="hidden md:flex items-center gap-7 text-sm font-light">
        <a class="nav-link" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>
        <a class="nav-link" href="#metodo" data-es="El Método" data-en="The Process">El Método</a>
        <a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>
        <a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>
        <a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>
        <a class="nav-link" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>
      </nav>
      <div class="flex items-center gap-3">
        <button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Change language">EN</button>
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>
        <button id="menuBtn" class="md:hidden w-10 h-10 flex flex-col items-center justify-center gap-[5px]" aria-label="Open menu">
          <span class="w-6 h-px bg-[color:var(--ink)]"></span>
          <span class="w-6 h-px bg-[color:var(--ink)]"></span>
          <span class="w-4 h-px bg-[color:var(--accent-deep)] self-end mr-2"></span>
        </button>
      </div>
    </div>
    <div id="mobileMenu" class="md:hidden hidden glass mx-4 mt-1 rounded-2xl overflow-hidden">
      <nav class="flex flex-col p-4 text-sm">
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#experiencia" data-es="La Experiencia" data-en="The Experience">La Experiencia</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Process">El Método</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>
        <a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>
        <a class="py-3 px-3" href="#ubicacion" data-es="Ubicación" data-en="Location">Ubicación</a>
        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>
      </nav>
    </div>
  </header>

  '''

print('OK: preloader + nav definidos')

# ============================================================
# HERO
# ============================================================
NEW_HERO = f'''<!-- HERO -->
  <section id="top" class="relative min-h-screen flex items-center grain overflow-hidden pt-28 pb-16">
    <div class="glow-bg"><div class="orb orb-a" data-parallax="0.14"></div><div class="orb orb-b" data-parallax="0.09"></div><div class="orb orb-c" data-parallax="0.2"></div></div>
    <div id="heroInner" class="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Miami, FL · Salón y Barbería" data-en="Miami, FL · Salon &amp; Barbershop">Miami, FL · Salon &amp; Barbershop</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Belleza y estilo, para todos." data-en="Beauty and style, for everyone.">Beauty and style, for everyone.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Botox capilar, keratina y" data-en="Hair botox, keratin and">Hair botox, keratin and</span><br /><span data-es="cortes para " data-en="cuts for ">cuts for </span><span class="text-shine" data-es="todos" data-en="everyone">everyone</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Botox capilar, tratamientos de keratina, blowouts lisos y brillantes y cortes de precisión de manos de la estilista Johanne Vital, para mujeres y hombres. Un salón y barbería cinco estrellas en Miami, FL con una calificación perfecta de 5.0 en 74 reseñas." data-en="Hair botox, keratin treatments, silk-smooth blowouts and precision cuts from stylist Johanne Vital, for women and men alike. A five-star salon and barbershop in Miami, FL with a perfect 5.0 rating across 74 reviews.">Hair botox, keratin treatments, silk-smooth blowouts and precision cuts from stylist Johanne Vital, for women and men alike. A five-star salon and barbershop in Miami, FL with a perfect 5.0 rating across 74 reviews.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 74 reseñas en Booksy" data-en="5.0 · 74 reviews on Booksy">5.0 · 74 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            {IG_HANDLE}
          </a>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-9.jpg" alt="Silk-smooth, shiny blowout finished at 5 Stars Dominican Beauty Salon, back view" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Hair Botox</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$176 · 2h" data-en="$176 · 2h">$176 · 2h</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# STRIP DE CONFIANZA
# ============================================================
NEW_STRIP = '''<!-- STRIP DE CONFIANZA -->
  <section class="relative border-y border-[color:var(--accent-ghost)] bg-[color:var(--bg-2)]">
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="74">74</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl" data-es="Salón" data-en="Salon">Salon</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Mujeres y hombres" data-en="Women &amp; men welcome">Women &amp; men welcome</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Botox <span class="text-shine">&amp;</span> Keratin</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Tratamientos insignia" data-en="Signature treatments">Signature treatments</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">North Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">631 NE 125th St</p></div>
    </div>
  </section>

  '''

print('OK: hero + strip definidos')

# ============================================================
# MARQUEE (misma secuencia en los dos marquees)
# ============================================================
MARQUEE_SEQ = '''      <div class="marquee-seq">
        <span class="marquee-word">Hair Botox</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Keratin Treatment</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Silk-Smooth Blowouts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Curly Cuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Men&#8217;s Cuts</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Miami, FL</span><span class="marquee-star">✦</span>
      </div>
'''
NEW_MARQUEE1 = '''<!-- MARQUEE -->
  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">
''' + MARQUEE_SEQ + MARQUEE_SEQ + '''    </div>
  </div>

  '''
NEW_MARQUEE2 = '''<!-- MARQUEE -->
  <div class="marquee marquee-reverse" aria-hidden="true">
    <div class="marquee-track">
''' + MARQUEE_SEQ + MARQUEE_SEQ + '''    </div>
  </div>

  '''

# ============================================================
# LA EXPERIENCIA
# ============================================================
NEW_EXPERIENCIA = '''<!-- LA EXPERIENCIA -->
  <section id="experiencia" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">01</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-14 items-center">
      <div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-1.jpg" alt="Client getting a fresh finish inside 5 Stars Dominican Beauty Salon, back view of the interior" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-7.jpg" alt="Interior of 5 Stars Dominican Beauty Salon &amp; Barbershop" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un salón," data-en="One salon,">One salon,</span><br /><span class="text-shine" data-es="resultados sin límite" data-en="endless finishes">endless finishes</span></h2>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="5 Stars Dominican Beauty Salon &amp; Barbershop es el estudio de la estilista Johanne Vital en North Miami: botox capilar, tratamientos de keratina, blowouts lisos y brillantes y cortes de rizos para mujeres, además de cortes y arreglos para hombres, todo bajo un mismo techo." data-en="5 Stars Dominican Beauty Salon &amp; Barbershop is stylist Johanne Vital&#8217;s studio in North Miami: hair botox, keratin treatments, silk-smooth blowouts and curly cuts for women, plus cuts and grooming for men, all under one roof.">5 Stars Dominican Beauty Salon &amp; Barbershop is stylist Johanne Vital&#8217;s studio in North Miami: hair botox, keratin treatments, silk-smooth blowouts and curly cuts for women, plus cuts and grooming for men, all under one roof.</p>
        <p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientes vuelven por la misma razón: resultados sanos y definidos cada vez, ya sea un corte de rizos o un botox capilar completo. Un 5.0 perfecto en 74 reseñas verificadas de Booksy." data-en="Clients keep coming back for the same reason: healthy, defined results every time, whether it&#8217;s a curly cut or a full hair botox treatment. A perfect 5.0 across 74 verified reviews on Booksy.">Clients keep coming back for the same reason: healthy, defined results every time, whether it&#8217;s a curly cut or a full hair botox treatment. A perfect 5.0 across 74 verified reviews on Booksy.</p>
        <div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="74">74</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Salón + Barbería" data-en="Salon + Barber">Salon + Barber</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Para toda la familia" data-en="For the whole family">For the whole family</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="5 Stars Dominican Beauty Salon &amp; Barbershop logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(213,60,85,0.3)] bg-white" loading="lazy" />
            <span class="text-sm font-light">Johanne Vital · <span class="text-[color:var(--ink-40)]" data-es="Estilista principal" data-en="Lead Stylist">Lead Stylist</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''

print('OK: marquee x2 + experiencia definidos')

# ============================================================
# EL METODO
# ============================================================
NEW_METODO = '''<!-- EL METODO -->
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Elige tu servicio en Booksy con precio y duración claros: botox capilar, keratina, un blowout o un corte para ella o él, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: hair botox, keratin, a blowout, or a cut for her or him, and confirm instantly.">Pick your service on Booksy with clear price and duration: hair botox, keratin, a blowout, or a cut for her or him, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su textura y el estilo que buscas definen la técnica: un corte de rizos o un fade nítido empiezan con una idea clara." data-en="Your hair type, texture and the look you want set the technique: a curly cut or a sharp fade both start with a clear plan.">Your hair type, texture and the look you want set the technique: a curly cut or a sharp fade both start with a clear plan.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The service">The service</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Desde un corte de 40 minutos hasta un botox capilar de 2 horas o una keratina de 2h 30min: cada cliente recibe atención completa, sin apuros." data-en="From a 40-minute haircut to a 2-hour hair botox or a 2h 30min keratin treatment: every client gets full, unhurried attention.">From a 40-minute haircut to a 2-hour hair botox or a 2h 30min keratin treatment: every client gets full, unhurried attention.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un acabado definido y consejos para cuidarlo en casa. Tu próxima cita queda agendada antes de irte." data-en="You leave with a defined, healthy finish and tips to maintain it at home. Your next appointment gets booked before you go.">You leave with a defined, healthy finish and tips to maintain it at home. Your next appointment gets booked before you go.</p>
        </div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# SERVICIOS (4 cards, card 2 = destacada/favorita con btn-3d)
# ============================================================
NEW_SERVICIOS = f'''<!-- SERVICIOS -->
  <section id="servicios" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">03</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Servicios" data-en="Services">Servicios</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="tratamiento" data-en="treatment">treatment</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por 5 Stars Dominican Beauty Salon &amp; Barbershop en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by 5 Stars Dominican Beauty Salon &amp; Barbershop on Booksy. Booking confirms instantly.">Prices and durations as published by 5 Stars Dominican Beauty Salon &amp; Barbershop on Booksy. Booking confirms instantly.</p>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Corte" data-en="Haircut">Haircut</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Female Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un corte de precisión, lavado y terminado en una sola visita rápida." data-en="A precision haircut, washed and finished in one quick visit.">A precision haircut, washed and finished in one quick visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">40min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(213,60,85,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito de la casa" data-en="House favorite">House favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Hair Botox</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El tratamiento insignia que deja el cabello más suave, brillante y manejable, dos horas dedicadas por completo a tu cabello." data-en="The signature treatment that leaves hair smoother, shinier and easier to manage, two hours dedicated entirely to your hair.">The signature treatment that leaves hair smoother, shinier and easier to manage, two hours dedicated entirely to your hair.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$176</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especialidad en rizos" data-en="Curly specialist">Curly specialist</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Curly Hair Cut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un corte pensado para dar forma y realzar el rizo natural, resaltando su volumen y definición." data-en="A cut designed to shape and enhance your natural curls, bringing out their bounce and definition.">A cut designed to shape and enhance your natural curls, bringing out their bounce and definition.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$72</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tratamiento profundo" data-en="Deep treatment">Deep treatment</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Keratin Hair Treatment" data-en="Keratin Hair Treatment">Keratin Hair Treatment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un tratamiento completo de keratina para un cabello más liso, sin frizz y con resultados duraderos." data-en="A full keratin treatment for smoother, frizz-free hair with results that last.">A full keratin treatment for smoother, frizz-free hair with results that last.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$200</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También en el menú: Corte para hombre $28 (40min), Color $96 (1h), Full Highlights $224 (2h 30min), Shampoo y Style $112 (1h 30min), Extensiones de cinta $168 (3h) y Manicura y Pedicura en Gel $52 (1h 30min). Precios exactos y disponibilidad real en Booksy." data-en="Also on the menu: Male Haircut $28 (40min), Color $96 (1h), Full Highlights $224 (2h 30min), Shampoo and Style $112 (1h 30min), Tape Hair Extensions $168 (3h) and Manicure &amp; Pedicure Gel $52 (1h 30min). Exact prices and real time availability on Booksy.">Also on the menu: Male Haircut $28 (40min), Color $96 (1h), Full Highlights $224 (2h 30min), Shampoo and Style $112 (1h 30min), Tape Hair Extensions $168 (3h) and Manicure &amp; Pedicure Gel $52 (1h 30min). Exact prices and real time availability on Booksy.</span></p>
    </div>
  </section>

  '''

print('OK: metodo + servicios definidos')

# ============================================================
# GALERIA (1 tile ancho 16/9 + 5 tiles 3/4)
# ============================================================
NEW_GALERIA = f'''<!-- GALERIA -->
  <section id="galeria" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">04</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="flex flex-wrap items-end justify-between gap-6 mb-14">
        <div>
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>
          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span></h2>
        </div>
        <a href="{IG}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          {IG_HANDLE}
        </a>
      </div>
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Dentro del salón" data-en="Inside the salon">Inside the salon</span><img src="assets/raw/bk-4.jpg" alt="Wide view of the 5 Stars Dominican Beauty Salon &amp; Barbershop interior with styling chairs" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Acabado liso y brillante" data-en="Sleek, shiny finish">Sleek, shiny finish</span><img src="assets/raw/bk-3.jpg" alt="Sleek, shiny black hair finished at the salon, back view" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Color rubio miel" data-en="Honey blonde color">Honey blonde color</span><img src="assets/raw/bk-10.jpg" alt="Honey blonde hair color, profile view" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Updo con corona de flores" data-en="Updo with a flower crown">Updo with a flower crown</span><img src="assets/raw/bk-11.jpg" alt="Festive updo styled with a flower crown" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Blowout liso, vista de espaldas" data-en="Smooth blowout, back view">Smooth blowout, back view</span><img src="assets/raw/bk-12.jpg" alt="Smooth, straight black hair finished in the styling chair, back view" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Un acabado fresco en la silla" data-en="A fresh finish in the chair">A fresh finish in the chair</span><img src="assets/raw/bk-1.jpg" alt="Client getting a fresh finish inside 5 Stars Dominican Beauty Salon" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>

  '''

# ============================================================
# OPINIONES (3 resenas reales verbatim, sin em-dash)
# ============================================================
NEW_OPINIONES = f'''<!-- OPINIONES -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What clients">What clients</span> <span class="text-shine" data-es="los clientes" data-en="say">say</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 74 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 74 verified reviews on Booksy">5.0 out of 5 · 74 verified reviews on Booksy</span></p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very good cut and calm environment."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Malachi .&#8230;</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I came in just for a curly cut, and I'm so happy with the results! The stylist really understood how to shape my curls to bring out their natural bounce and volume. They took their time making sure everything was even and flattering for my face shape. Even without a wash or style, my curls look so much healthier and more defined. I love the shape and how lightweight my hair feels now. I'll definitely be coming back!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mia. Y&#8230;</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing experience. Great Botox treatment and silk press."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Amy L&#8230;</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{BK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 74 reseñas en Booksy" data-en="Read all 74 reviews on Booksy">Read all 74 reviews on Booksy</a>
      </div>
    </div>
  </section>

  '''

print('OK: galeria + opiniones definidos')

# ============================================================
# UBICACION
# ============================================================
MAPS_Q = '631+NE+125th+St,+North+Miami,+FL+33161'
NEW_UBICACION = f'''<!-- UBICACION -->
  <section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Visítanos" data-en="Visit us">Visit us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">North Miami</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">631 NE 125th St, North Miami, FL 33161</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(213,60,85,0.4)]" href="https://www.google.com/maps?q={MAPS_Q}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a viernes, 9:55am a 6:55pm. Sábado, 9:55am a 7:10pm." data-en="Monday to Friday, 9:55am to 6:55pm. Saturday, 9:55am to 7:10pm.">Monday to Friday, 9:55am to 6:55pm. Saturday, 9:55am to 7:10pm.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(213,60,85,0.4)]" href="{BK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los resultados más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest results and DM any questions before your appointment.">See the latest results and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(213,60,85,0.4)]" href="{IG}" target="_blank" rel="noopener">{IG_HANDLE}</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: 5 Stars Dominican Beauty Salon &amp; Barbershop, 631 NE 125th St, North Miami FL"
          src="https://www.google.com/maps?q={MAPS_Q}&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
  </section>

  '''

# ============================================================
# CTA FINAL
# ============================================================
NEW_CTA = '''<!-- CTA FINAL -->
  <section id="cta-final" class="dark-band relative py-28 sm:py-36 overflow-hidden grain border-t border-[color:var(--accent-ghost)]" style="background: linear-gradient(180deg, #180609 0%, #0f0407 100%);">
    <div class="glow-bg"><div class="orb orb-a" style="opacity:0.7"></div><div class="orb orb-b" style="opacity:0.7"></div></div>
    <div id="ctaGlow" class="cursor-glow" aria-hidden="true"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-5 sm:px-8 text-center">
      <p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Belleza y estilo, para todos." data-en="Beauty and style, for everyone.">Beauty and style, for everyone.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="empieza aquí" data-en="starts here">starts here</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva en línea en segundos: tu botox capilar, tu keratina, o ese corte de rizos que has estado planeando." data-en="Book online in seconds: your hair botox, your keratin treatment, or that curly cut you have been planning.">Book online in seconds: your hair botox, your keratin treatment, or that curly cut you have been planning.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
'''
NEW_CTA += f'''        <a href="{BK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>
        <a href="{IG}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>
      </div>
    </div>
  </section>

  '''

print('OK: ubicacion + cta final definidos')

# ============================================================
# FOOTER (el merktop-badge original se reutiliza intacto)
# ============================================================
m_badge_footer = re.search(r'<a href="https://merktop\.com".*?</a>', seg_footer_orig, flags=re.S)
assert m_badge_footer, 'no se encontro merktop-badge en footer original'
MERKTOP_BADGE_HTML = m_badge_footer.group(0)

NEW_FOOTER = f'''<!-- FOOTER -->
  <footer class="dark-band relative overflow-hidden border-t border-[color:var(--accent-ghost)] bg-[#0c0506]">
    <span class="foot-mark" aria-hidden="true">5 Stars Dominican</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 py-14 grid sm:grid-cols-3 gap-10">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/bk-2.jpg" alt="5 Stars Dominican Beauty Salon &amp; Barbershop logo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(231,132,147,0.35)] bg-white" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">5 Stars Dominican</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Salón y barbería en North Miami, FL. Atención con cita previa vía Booksy." data-en="Salon &amp; barbershop in North Miami, FL. By appointment via Booksy.">Salon &amp; barbershop in North Miami, FL. By appointment via Booksy.</p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>631 NE 125th St, North Miami, FL 33161</p>
        <p><a href="{BK}" target="_blank" rel="noopener" class="hover:text-[#e799bd]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
      </div>
      <div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Follow</p>
        <p><a href="{IG}" target="_blank" rel="noopener" class="hover:text-[#e799bd]">Instagram · {IG_HANDLE}</a></p>
      </div>
    </div>
    <div class="border-t border-[color:var(--accent-ghost)]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-xs text-[color:var(--ink-40)]">© 2026 5 Stars Dominican Beauty Salon &amp; Barbershop.</p>
        {MERKTOP_BADGE_HTML}
      </div>
    </div>
  </footer>

  '''

# ============================================================
# BOTON FLOTANTE (misma marca, solo booksy url + aria-label EN)
# ============================================================
NEW_BOOKFLOAT = f'''<!-- Boton flotante de reserva -->
  <a href="{BK}" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1b070c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>

  '''

# ============================================================
# TAIL: cursorRing + back-top + script (aria-label back-top a EN)
# ============================================================
new_seg_tail = seg_tail.replace('aria-label="Volver arriba"', 'aria-label="Back to top"')
assert new_seg_tail != seg_tail, 'no se pudo traducir aria-label de back-top'
seg_tail = new_seg_tail

print('OK: footer + book-float + tail definidos')

# ============================================================
# 4. ENSAMBLADO FINAL
# ============================================================
h_final = (
    seg_head
    + NEW_PRELOADER
    + seg_scroll
    + NEW_NAV
    + NEW_HERO
    + NEW_STRIP
    + NEW_MARQUEE1
    + NEW_EXPERIENCIA
    + NEW_METODO
    + NEW_SERVICIOS
    + NEW_GALERIA
    + NEW_MARQUEE2
    + NEW_OPINIONES
    + NEW_UBICACION
    + NEW_CTA
    + NEW_FOOTER
    + NEW_BOOKFLOAT
    + seg_tail
)

# sanity: los 6 marquee-word deben aparecer exactamente 4 veces cada uno
for word in ['Hair Botox', 'Keratin Treatment', 'Silk-Smooth Blowouts', 'Curly Cuts', 'Men&#8217;s Cuts', 'Miami, FL']:
    c = h_final.count(f'<span class="marquee-word">{word}</span>')
    assert c == 4, f'marquee-word "{word}" x{c}, esperaba 4'

assert h_final.count('—') == 0, 'hay em-dash en el HTML final'

import os
os.makedirs('output/fivestarsdominicansalon', exist_ok=True)
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h_final)
print('OK: escrito', DST, 'len=', len(h_final))
