import re
import shutil

SLUG = "sky-s-the-limit-handyman-services"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/dark-v2/index.html", PATH)
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


MAPS_URL = "https://www.google.com/maps/place/Sky's+The+Limit+Handyman+Services/"
TEL = "tel:+18133130379"

# 1. Globales: sin booking -> tel:, sin FB/IG -> se quita boton secundario
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
rep_all(OLD_BOOK, TEL, expect=13)
print("GLOBALS done")

# 2. HEAD
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    "<title>Sky's The Limit Handyman Services · Tampa, FL | TV Mounting &amp; Repairs | 4.9 on Google</title>")
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    "<meta name=\"description\" content=\"Sky's The Limit Handyman Services, Tampa FL: TV mounting, plumbing fixture installs and general home repairs for homeowners and rental properties. 4.9 stars across 13 Google reviews.\" />")
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    "<meta property=\"og:title\" content=\"Sky's The Limit Handyman Services · Tampa, FL\" />")
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="TV mounting, plumbing fixtures and general repairs in Tampa. 4.9 on Google with 13 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-3.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/gmaps-3.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Sky's The Limit Handyman Services",
    "description": "Handyman company serving Tampa, FL: TV mounting, plumbing fixture installs and general home repairs for homeowners, landlords and rental properties.",
    "areaServed": { "@type": "City", "name": "Tampa" },
    "telephone": "+1-813-313-0379",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "13", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Handyman services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "TV Mounting" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plumbing Fixture Installs" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Rental Property Maintenance" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "General Handyman Repairs" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# 3. PRELOADER + NAV
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">SL</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Sky\'s The Limit</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
    '<img src="assets/raw/gmaps-3.jpg" alt="Sky\'s The Limit Handyman Services" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Sky\'s <span class="text-[color:var(--accent-deep)]">The Limit</span></span>')
rep('<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '', n=1)
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '', n=1)
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Call now</span>', n=1)
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>')
print("NAV done")

# 4. HERO
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Tampa, FL · Handyman" data-en="Tampa, FL · Handyman">Tampa, FL · Handyman</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Disponible cuando lo necesitas, de verdad." data-en="Available when you need it, really.">Available when you need it, really.</p>',
    n=2)
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Montaje de TV," data-en="TV mounting,">TV mounting,</span><br /><span data-es="plomeria y reparaciones " data-en="plumbing and repairs ">plumbing and repairs </span><span class="text-shine" data-es="24/7" data-en="24/7">24/7</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Sky atiende Tampa las 24 horas: montaje de TV, instalacion de artefactos de plomeria y mantenimiento general para propietarios y administradores de propiedades de alquiler, con 4.9 estrellas en 13 reseñas de Google." data-en="Sky serves Tampa around the clock: TV mounting, plumbing fixture installs and general upkeep for homeowners and rental property managers, with 4.9 stars across 13 Google reviews.">Sky serves Tampa around the clock: TV mounting, plumbing fixture installs and general upkeep for homeowners and rental property managers, with 4.9 stars across 13 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.9 · 13 reseñas en Google" data-en="4.9 · 13 reviews on Google">4.9 · 13 reviews on Google</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Llamar al (813) 313-0379" data-en="Call (813) 313-0379">Call (813) 313-0379</span>', n=1)
rep('''          <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @pure.artistrysk
          </a>
''', '')
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>\n          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Resenas reales en Google" data-en="Real Google reviews">Real Google reviews</span>\n          <span data-es="Presupuesto gratis" data-en="Free estimates">Free estimates</span>\n          <span data-es="Disponible 24/7" data-en="Available 24/7">Available 24/7</span>')
rep('aria-label="Lo que encontrará el cliente"', 'aria-label="What you get"')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-3.jpg" alt="Reparacion de techo y canaleta hecha por Skys The Limit" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Llama hoy" data-en="Call today">Call today</p>
            <p class="font-display text-lg">TV Mounting</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Presupuesto gratis · Tampa" data-en="Free estimate · Tampa">Free estimate · Tampa</p>''')
print("HERO done")
open(PATH, "w", encoding="utf-8").write(h)
print("WROTE PARTIAL1")
h = open(PATH, encoding="utf-8").read()

# 5. STRIP
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="13">13</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">TV <span class="text-shine">&amp;</span> Plumbing</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Montaje e instalaciones" data-en="Mounting & installs">Mounting & installs</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">24<span class="text-shine">/</span>7</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Siempre disponible" data-en="Always available">Always available</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Tampa, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="&amp; alrededores" data-en="&amp; surrounding area">&amp; surrounding area</p></div>')
print("STRIP done")

# 6. MARQUEE
MARQUEE_WORDS = [
    ("Silk Press", "TV Mounting"),
    ("Loc Retwist", "Plumbing Fixtures"),
    ("Knotless Braids", "Rental Maintenance"),
    ("K-Tip Extensions", "General Repairs"),
    ("Keratin", "Free Estimates"),
    ("Orlando, FL", "Tampa, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# 7. EXPERIENCIA (solo 2 fotos reales: una sola imagen grande, no grid de 2)
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="frame zoomable aspect-[4/5] img-reveal">
        <img src="assets/raw/gmaps-1.jpg" alt="Instalacion de artefacto de plomeria hecha por Sky's The Limit" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Un solo contacto," data-en="One point of contact,">One point of contact,</span><br /><span class="text-shine" data-es="disponible 24/7" data-en="available around the clock">available around the clock</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Sky atiende el mismo el telefono y el trabajo: montaje de TV, instalaciones de plomeria y mantenimiento general para casas y propiedades de alquiler en Tampa, con trato directo de principio a fin." data-en="Sky answers the phone and does the work himself: TV mounting, plumbing installs and general upkeep for homes and rental properties across Tampa, with direct, personal service start to finish.">Sky answers the phone and does the work himself: TV mounting, plumbing installs and general upkeep for homes and rental properties across Tampa, with direct, personal service start to finish.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="El resultado: 4.9 de calificacion en 13 reseñas de Google, con clientes que destacan lo profesional y confiable que es para manejar propiedades a distancia." data-en="The result: a 4.9 rating across 13 Google reviews, with clients praising how professional and trustworthy he is for managing a property remotely.">The result: a 4.9 rating across 13 Google reviews, with clients praising how professional and trustworthy he is for managing a property remotely.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="13">13</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Resenas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atencion personal" data-en="Personal care">Personal care</p></div>''')
rep('''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>
          </div>''',
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/gmaps-3.jpg" alt="Sky's The Limit Handyman Services" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Sky's The Limit · <span class="text-[color:var(--ink-40)]" data-es="Handyman" data-en="Handyman">Handyman</span></span>
          </div>''')
rep('<p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>')
print("EXPERIENCIA done")

# 8. METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu proyecto, paso a paso" data-en="Your project, step by step">Tu proyecto, paso a paso</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Asi se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span></h2>')
rep('<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Llama o escribe" data-en="Call or text">Call or text</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cuentale a Sky que necesitas: montaje, plomeria o una reparacion general, a cualquier hora." data-en="Tell Sky what you need: mounting, plumbing or a general repair, any time of day.">Tell Sky what you need: mounting, plumbing or a general repair, any time of day.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sky revisa el trabajo y te deja un precio claro antes de empezar, de los mejores precios de la zona." data-en="Sky reviews the job and leaves you a clear price before starting, some of the best prices in town.">Sky reviews the job and leaves you a clear price before starting, some of the best prices in town.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De un montaje de TV a un proyecto completo en una propiedad de alquiler, Sky conoce el trabajo bien." data-en="From a single TV mount to a full job on a rental property, Sky knows the work well.">From a single TV mount to a full job on a rental property, Sky knows the work well.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Trabajo terminado" data-en="Finished right">Finished right</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Trabajo prolijo y confiable, tal como lo describen sus clientes de propiedades de alquiler en Google." data-en="Clean, trustworthy work, exactly as his rental property clients describe it on Google.">Clean, trustworthy work, exactly as his rental property clients describe it on Google.</p>')
print("METODO done")
open(PATH, "w", encoding="utf-8").write(h)
print("WROTE PARTIAL2")
h = open(PATH, encoding="utf-8").read()

# 9. SERVICIOS
rep('data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que" data-en="What we">Lo que</span> <span class="text-shine" data-es="hacemos" data-en="do">do</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Cada trabajo se cotiza segun el alcance real. Presupuesto gratis, sin compromiso." data-en="Every job is quoted based on its real scope. Free estimate, no obligation.">Every job is quoted based on its real scope. Free estimate, no obligation.</p>')

OLD_SERVICES_GRID = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert OLD_SERVICES_GRID
NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo mas pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Montaje de TV" data-en="TV Mounting">TV Mounting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Instalacion profesional y segura, con los mejores precios de la zona segun sus clientes." data-en="Safe, professional installs, with some of the best prices in town according to his clients.">Safe, professional installs, with some of the best prices in town according to his clients.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Cotizacion" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18133130379" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Bano y cocina" data-en="Bath & Kitchen">Bath & Kitchen</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Instalacion de plomeria" data-en="Plumbing Fixture Installs">Plumbing Fixture Installs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Inodoros, lavamanos y grifos instalados correctamente desde la primera vez." data-en="Toilets, sinks and faucets installed right the first time.">Toilets, sinks and faucets installed right the first time.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Cotizacion" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18133130379" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Propietarios" data-en="Landlords">Landlords</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Mantenimiento de alquileres" data-en="Rental Property Maintenance">Rental Property Maintenance</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Confiable para administradores que manejan propiedades a distancia: profesional y de confianza." data-en="Trusted by property managers handling things remotely: professional and reliable.">Trusted by property managers handling things remotely: professional and reliable.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Cotizacion" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18133130379" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="General" data-en="General">General</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reparaciones generales" data-en="General Handyman Repairs">General Handyman Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Reparacion de techos, canaletas y todo lo que tu casa o propiedad necesite." data-en="Roof and gutter repair, and whatever else your home or property needs.">Roof and gutter repair, and whatever else your home or property needs.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Cotizacion" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18133130379" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:OLD_SERVICES_GRID.start()] + NEW_SERVICES_GRID + h[OLD_SERVICES_GRID.end():]

OLD_SERVICES_NOTE = re.search(r'<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">.*?</p>', h, flags=re.S)
assert OLD_SERVICES_NOTE
NEW_SERVICES_NOTE = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: montaje de muebles, instalaciones y reparaciones varias. Llama para contarnos tu proyecto." data-en="Also: furniture assembly, installations and miscellaneous repairs. Call to tell us about your project.">Also: furniture assembly, installations and miscellaneous repairs. Call to tell us about your project.</span></p>'
h = h[:OLD_SERVICES_NOTE.start()] + NEW_SERVICES_NOTE + h[OLD_SERVICES_NOTE.end():]
print("SERVICIOS done")

# 10. GALERIA: se ELIMINA la seccion completa (solo 2 fotos reales, ya usadas
#     en hero/experiencia; no hay suficiente para un grid sin repetir/rellenar).
OLD_GALLERY_SECTION = re.search(r'\s*<!-- GALERIA -->\s*<section id="galeria".*?</section>', h, flags=re.S)
assert OLD_GALLERY_SECTION
h = h[:OLD_GALLERY_SECTION.start()] + h[OLD_GALLERY_SECTION.end():]
print("GALERIA (removida) done")

# 11. OPINIONES
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 13 resenas verificadas en Google" data-en="4.9 out of 5 · 13 verified reviews on Google">4.9 out of 5 · 13 verified reviews on Google</span></p>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"From a contractor standpoint, trust and professionalism are everything, especially when you are managing a property remotely."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Alexander Yassein</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I have worked with Sky on multiple projects across both my rental property and my personal home, and I cannot recommend him highly enough."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Michael Guzzo</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Sky came out today for a TV mounting and he was great! Best prices in town, very knowledgeable, great work. Highly recommended!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">apt vids</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<a href="tel:+18133130379" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    f'<a href="{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 13 resenas en Google" data-en="Read all 13 reviews on Google">Read all 13 reviews on Google</a>')
print("OPINIONES done")
open(PATH, "w", encoding="utf-8").write(h)
print("WROTE PARTIAL3")
h = open(PATH, encoding="utf-8").read()

# 12. UBICACION -> service area
OLD_UBICACION = re.search(r'<section id="ubicacion".*?</section>', h, flags=re.S)
assert OLD_UBICACION
NEW_UBICACION = '''<section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-5xl mx-auto px-5 sm:px-8">
      <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Area de servicio" data-en="Service area">Service area</p>
      <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Trabajamos en" data-en="We work across">We work across</span> <span class="text-shine">Tampa</span></h2>
      <div class="grid sm:grid-cols-2 gap-5">
        <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
          <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
          <div>
            <p class="font-medium mb-1" data-es="Donde trabajamos" data-en="Where we work">Where we work</p>
            <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Tampa y alrededores, casas y propiedades de alquiler. Servicio a domicilio." data-en="Tampa and the surrounding area, homes and rental properties. We come to you.">Tampa and the surrounding area, homes and rental properties. We come to you.</p>
          </div>
        </div>
        <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
          <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <div>
            <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
            <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Disponible 24/7. Llama para tu presupuesto gratis o una reparacion urgente." data-en="Available 24/7. Call for your free estimate or an urgent repair.">Available 24/7. Call for your free estimate or an urgent repair.</p>
            <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="tel:+18133130379" data-es="Llamar al (813) 313-0379" data-en="Call (813) 313-0379">Call (813) 313-0379</a>
          </div>
        </div>
      </div>
    </div>
  </section>'''
h = h[:OLD_UBICACION.start()] + NEW_UBICACION + h[OLD_UBICACION.end():]
print("UBICACION done")

# 13. CTA FINAL
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu proyecto" data-en="Your project">Your project</span> <span class="text-shine" data-es="puede empezar hoy" data-en="can start today">can start today</span></h2>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Llama ahora, a cualquier hora, para un presupuesto gratis o una reparacion urgente." data-en="Call now, any time of day, for a free estimate or an urgent repair.">Call now, any time of day, for a free estimate or an urgent repair.</p>')
rep('<a href="tel:+18133130379" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="tel:+18133130379" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (813) 313-0379" data-en="Call (813) 313-0379">Call (813) 313-0379</a>')
print("CTA FINAL done")

# 14. FOOTER
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Sky\'s The Limit</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>''',
    '''<img src="assets/raw/gmaps-3.jpg" alt="Sky's The Limit Handyman" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Sky's The Limit</span>''')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Handyman en Tampa, FL. Servicio a domicilio, disponible 24/7." data-en="Handyman serving Tampa, FL. We come to you, available 24/7.">Handyman serving Tampa, FL. We come to you, available 24/7.</p>')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="tel:+18133130379" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>Tampa &amp; surrounding area, FL</p>
        <p><a href="tel:+18133130379" class="hover:text-[#e9c3ab]">(813) 313-0379</a></p>''')
OLD_FOOTER_FOLLOW = re.search(r'<div class="text-sm font-light text-\[color:var\(--ink-60\)\] space-y-2">\s*<p class="text-xs tracking-\[0\.3em\] uppercase text-\[color:var\(--ink-40\)\] mb-3" data-es="Síguenos".*?</div>', h, flags=re.S)
assert OLD_FOOTER_FOLLOW
NEW_FOOTER_FOLLOW = '''<div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Resenas" data-en="Reviews">Reviews</p>
        <p><a href="''' + MAPS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Google · 4.9 (13)</a></p>
      </div>'''
h = h[:OLD_FOOTER_FOLLOW.start()] + NEW_FOOTER_FOLLOW + h[OLD_FOOTER_FOLLOW.end():]
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    "<p class=\"text-xs text-[color:var(--ink-40)]\">&copy; 2026 Sky's The Limit Handyman Services.</p>")
print("FOOTER done")

# 15. Boton flotante
rep('<a href="tel:+18133130379" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="tel:+18133130379" class="book-float" aria-label="Llamar ahora">')
rep('<span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span class="book-float-label" data-es="Llamar ahora" data-en="Call now">Call now</span>')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 16. PALETA (al final: evita anclas rotas por recolor previo). Gold -> amber/copper.
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

HEX_PALETTE = [
    ("#d4a84b", "#a66a35"),
    ("#b8934a", "#b8813f"),
    ("#f0dc9e", "#e3c08f"),
    ("#9a7431", "#6e4a1f"),
    ("#e5c374", "#c99356"),
    ("#e8c476", "#cb9759"),
    ("#c9a04a", "#b07a3e"),
    ("#96742c", "#6e4a1f"),
    ("#e8cf96", "#dcb989"),
    ("#f8eed3", "#f1e2cc"),
    ("#bfa060", "#a97a46"),
    ("#ecd9a8", "#dfc49c"),
    ("#f0dcae", "#e3c6a1"),
    ("#e9c3ab", "#dcb79c"),
    ("#6b5222", "#4d3416"),
    ("#1c1408", "#17100a"),
    ("#8a744a", "#8a5e38"),
    ("#faf1dc", "#f4e6d2"),
    ("#c9ab6b", "#b88a53"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(166,106,53"),
    ("rgba(122,90,30", "rgba(110,74,31"),
    ("rgba(180,140,60", "rgba(176,122,62"),
    ("rgba(232,207,150", "rgba(220,185,137"),
    ("rgba(232,210,160", "rgba(223,196,156"),
    ("rgba(185,138,128", "rgba(180,146,120"),
    ("rgba(110,85,35", "rgba(109,74,31"),
    ("rgba(80,58,18", "rgba(77,52,22"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

open(PATH, "w", encoding="utf-8").write(h)
print("WROTE", PATH)
