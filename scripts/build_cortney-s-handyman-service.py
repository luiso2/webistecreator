import re

SLUG = "cortney-s-handyman-service"
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


PHONE_TEL = "tel:+13522865123"
MAPS_URL = "https://www.google.com/maps/place/Cortney%E2%80%99s+Handyman+Service/data=!4m7!3m6!1s0x88c2fb3a79979a93:0x167249f95de5e286!8m2!3d27.9018672!4d-82.814414!16s%2Fg%2F11lgqdgqj1!19sChIJk5qXeTr7wogRhuLlXflJchY?authuser=0&hl=en&g_ep=EgoyMDI2MTEyMy4wIJJjKgBIAVAD&rclk=1"

# ---------------------------------------------------------------------------
# 1. Globales: Booksy -> tel:, sin Instagram/Facebook (no existe canal social)
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
c = h.count(OLD_BOOK)
assert c == 13, c
h = h.replace(OLD_BOOK, PHONE_TEL)
print("BOOKSY->TEL done", c)

# ---------------------------------------------------------------------------
# 2. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    "<title>Cortney&#39;s Handyman Service · Handyman in Largo &amp; Clearwater, FL | 5.0 on Google</title>")
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Cortney\'s Handyman Service, Largo and Clearwater FL: kitchen and bath remodeling, plumbing and leak repairs, drywall, painting and general home repairs. Perfect 5.0 across 34 Google reviews. Call for a free estimate." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Cortney\'s Handyman Service · Handyman in Largo &amp; Clearwater, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Kitchen remodels, plumbing repairs, drywall and painting. 5.0 on Google with 34 reviews. Call for a free estimate." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-7.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/gmaps-7.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Cortney\\u2019s Handyman Service",
    "description": "Handyman service serving Largo, Clearwater and Pinellas County, FL: kitchen and bathroom remodeling, plumbing and leak repairs, drywall, painting, flooring and general home repairs.",
    "areaServed": [{ "@type": "City", "name": "Largo" }, { "@type": "City", "name": "Clearwater" }, { "@type": "AdministrativeArea", "name": "Pinellas County" }],
    "telephone": "+1-352-286-5123",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "34", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Handyman services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "General Handyman Repairs" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Kitchen & Bath Remodeling" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plumbing & Leak Repairs" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Painting, Decks & Fencing" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 3. PRELOADER + NAV (sin logo, sin pagina de IG)
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">CH</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Cortney&#39;s Handyman</span>')

rep('''<a href="#top" class="flex items-center gap-3">
        <img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,100,160,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>
      </a>''',
    '''<a href="#top" class="flex items-center gap-3">
        <span class="font-display text-xl tracking-[0.1em] uppercase">Cortney&#39;s <span class="text-[color:var(--accent-deep)]">Handyman</span></span>
      </a>''')

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Call now</span>', n=1)
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>')
print("NAV done")

# ---------------------------------------------------------------------------
# 4. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Largo y Clearwater, FL · Servicio de Handyman" data-en="Largo &amp; Clearwater, FL · Handyman Services">Largo &amp; Clearwater, FL · Handyman Services</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Reparaciones hechas bien, a la primera." data-en="Repairs done right, the first time.">Repairs done right, the first time.</p>',
    n=2)
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Remodelaciones, reparaciones" data-en="Kitchen remodels, repairs">Kitchen remodels, repairs</span><br /><span data-es="y plomería, hechas " data-en="and plumbing fixes, done ">and plumbing fixes, done </span><span class="text-shine" data-es="bien" data-en="right">right</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Cortney y su equipo se encargan de remodelaciones de cocina y baño, reparaciones de plomería y fugas, drywall, pintura e instalaciones en Largo, Clearwater y el condado de Pinellas, con una calificación perfecta de 5.0 en Google." data-en="Cortney and the team handle kitchen and bath remodels, plumbing and leak repairs, drywall, painting and installs across Largo, Clearwater and Pinellas County, with a perfect 5.0 rating on Google.">Cortney and the team handle kitchen and bath remodels, plumbing and leak repairs, drywall, painting and installs across Largo, Clearwater and Pinellas County, with a perfect 5.0 rating on Google.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 34 reseñas en Google" data-en="5.0 · 34 reviews on Google">5.0 · 34 reviews on Google</span>')
rep('''<a href="tel:+13522865123" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @_lashbloom
          </a>''',
    '''<a href="tel:+13522865123" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <span data-es="Llamar: (352) 286-5123" data-en="Call: (352) 286-5123">Call: (352) 286-5123</span>
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-7.jpg" alt="Instalacion de puertas correderas de vidrio en una terraza frente al agua por Cortney&#39;s Handyman Service" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Llama hoy" data-en="Call today">Call today</p>
            <p class="font-display text-lg">Handyman Service</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Presupuesto gratis · Largo, FL" data-en="Free estimate · Largo, FL">Free estimate · Largo, FL</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 5. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="34">34</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Handyman <span class="text-shine">&amp;</span> Repairs</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cocina · Plomería · Más" data-en="Kitchen · Plumbing · More">Kitchen · Plumbing · More</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine" data-es="Gratis" data-en="Free">Free</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Presupuesto sin costo" data-en="No cost estimates">No cost estimates</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Largo, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">&amp; Clearwater area</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 6. MARQUEE (x2 secciones, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Kitchen Remodels"),
    ("Hybrid Set", "Leak Repairs"),
    ("Volume Set", "Drywall &amp; Paint"),
    ("Mega Volume", "Door &amp; Window Install"),
    ("Bottom Lashes", "General Repairs"),
    ("West Palm Beach, FL", "Largo &amp; Clearwater, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 7. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-1.jpg" alt="Renovacion de fachada con ventanas nuevas hecha por Cortney&#39;s Handyman Service" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/gmaps-9.jpg" alt="Bano remodelado por Cortney&#39;s Handyman Service" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un solo equipo," data-en="One team,">One team,</span><br /><span class="text-shine" data-es="toda reparación cubierta" data-en="every repair covered">every repair covered</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Cortney&#39;s Handyman Service atiende Largo, Clearwater y el condado de Pinellas: remodelaciones de cocina y baño, instalacion de pisos, reparaciones de plomería y fugas, drywall, pintura exterior, terrazas y cercas, todo a cargo del mismo equipo." data-en="Cortney&#39;s Handyman Service serves Largo, Clearwater and Pinellas County: kitchen and bath remodels, flooring installs, plumbing and leak repairs, drywall, exterior painting, decks and fencing, all handled by one crew.">Cortney&#39;s Handyman Service serves Largo, Clearwater and Pinellas County: kitchen and bath remodels, flooring installs, plumbing and leak repairs, drywall, exterior painting, decks and fencing, all handled by one crew.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: una calificación perfecta de 5.0 en 34 reseñas de Google, con clientes que destacan lo profesional, respetuoso y detallista que es Cortney en cada visita." data-en="The result: a perfect 5.0 rating across 34 Google reviews, with clients specifically praising how professional, respectful and detail oriented Cortney is on every visit.">The result: a perfect 5.0 rating across 34 Google reviews, with clients specifically praising how professional, respectful and detail oriented Cortney is on every visit.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="34">34</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Contacto directo" data-en="Direct contact">Direct contact</p></div>')
rep('''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(74,100,160,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>
          </div>''',
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full px-5 py-2.5">
            <span class="text-sm font-light">Cortney · <span class="text-[color:var(--ink-40)]" data-es="Técnico y dueño" data-en="Owner & lead technician">Owner &amp; lead technician</span></span>
          </div>''')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 8. EL METODO -> COMO TRABAJAMOS
# ---------------------------------------------------------------------------
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Como trabajamos" data-en="How it works">How it works</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="De la llamada" data-en="From the call">From the call</span> <span class="text-shine" data-es="a la reparación" data-en="to the repair">to the repair</span></h2>')
rep('<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Llama o escribe" data-en="Call or text">Call or text</h3>')
rep('data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Llámanos o escríbenos y cuéntanos qué necesitas reparar o remodelar." data-en="Call or text us and tell us what needs fixing or remodeling.">Call or text us and tell us what needs fixing or remodeling.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</h3>')
rep('data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    'data-es="Evaluamos el trabajo y te damos un presupuesto claro, sin sorpresas." data-en="We evaluate the job and give you a clear, no surprises estimate.">We evaluate the job and give you a clear, no surprises estimate.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="We get to work">We get to work</h3>')
rep('data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    'data-es="Cortney y su equipo hacen el trabajo con cuidado y atención al detalle." data-en="Cortney and the team do the work with care and attention to detail.">Cortney and the team do the work with care and attention to detail.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Listo y duradero" data-en="Job done right">Job done right</h3>')
rep('data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    'data-es="Te quedas con una reparación o remodelación bien hecha, lista para años." data-en="You are left with a repair or remodel done right, built to last.">You are left with a repair or remodel done right, built to last.</p>')
print("METODO done")

# ---------------------------------------------------------------------------
# 9. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span class="text-shine">ritual</span>', '<span class="text-shine" data-es="servicio" data-en="service">service</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Presupuesto gratis en la mayoría de trabajos. Llama y te confirmamos en el mismo día." data-en="Free estimates on most jobs. Call and we confirm the same day.">Free estimates on most jobs. Call and we confirm the same day.</p>')

OLD_SERVICES_GRID = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert OLD_SERVICES_GRID
NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Reparaciones" data-en="Home Repairs">Home Repairs</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reparaciones Generales" data-en="General Handyman Repairs">General Handyman Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Drywall, puertas, repisas de closet, instalaciones y los arreglos del dia a dia que necesita una casa." data-en="Drywall, doors, closet shelving, fixture installs and the everyday fixes a home needs.">Drywall, doors, closet shelving, fixture installs and the everyday fixes a home needs.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Cotizacion gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="tel:+13522865123" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(74,100,160,0.4); box-shadow: 0 18px 50px rgba(38,43,56,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo mas pedido" data-en="Most Requested">Most Requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Remodelacion de Cocina y Bano" data-en="Kitchen &amp; Bath Remodeling">Kitchen &amp; Bath Remodeling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Remodelaciones completas de cocina, instalacion de pisos y trabajo en banos, de principio a fin." data-en="Full kitchen remodels, flooring installs and bathroom work, start to finish.">Full kitchen remodels, flooring installs and bathroom work, start to finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Cotizacion gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="tel:+13522865123" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Plomeria" data-en="Plumbing">Plumbing</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Plomeria y Reparacion de Fugas" data-en="Plumbing &amp; Leak Repairs">Plumbing &amp; Leak Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Fugas bajo el lavabo, tuberia PVC de bombas de piscina y las reparaciones de plomeria que surgen en casa." data-en="Leaks under the vanity, pool pump PVC plumbing and the plumbing repairs that come up around the house.">Leaks under the vanity, pool pump PVC plumbing and the plumbing repairs that come up around the house.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Cotizacion gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="tel:+13522865123" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Exteriores" data-en="Exterior Work">Exterior Work</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pintura, Terrazas y Cercas" data-en="Painting, Decks &amp; Fencing">Painting, Decks &amp; Fencing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pintura exterior, construccion de terrazas nuevas y reparacion de cercas y portones." data-en="Exterior painting, new deck builds and fence or gate repair.">Exterior painting, new deck builds and fence or gate repair.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine" data-es="Cotizacion gratis" data-en="Free estimate">Free estimate</p></div>
            <a href="tel:+13522865123" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:OLD_SERVICES_GRID.start()] + NEW_SERVICES_GRID + h[OLD_SERVICES_GRID.end():]

OLD_NOTE = re.search(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', h, flags=re.S)
assert OLD_NOTE
h = h[:OLD_NOTE.start()] + OLD_NOTE.group(1) + '<span data-es="Presupuesto gratis en la mayoria de trabajos. Llama para agendar una visita." data-en="Free estimates on most jobs. Call to schedule a visit.">Free estimates on most jobs. Call to schedule a visit.</span>' + OLD_NOTE.group(2) + h[OLD_NOTE.end():]
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 10. GALERIA (solo 4 fotos curadas: 1 ancha + 3)
# ---------------------------------------------------------------------------
rep('<p class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>'.replace('<p class', '<h2 class'),
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajos" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="work">work</span></h2>')
OLD_IG_GALLERY_LINK = '''<a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @_lashbloom
        </a>'''
assert OLD_IG_GALLERY_LINK in h
h = h.replace(OLD_IG_GALLERY_LINK, '', 1)

OLD_GALLERY_GRID = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert OLD_GALLERY_GRID
NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Terraza y puerta nuevas" data-en="New deck &amp; door install">New deck &amp; door install</span><img src="assets/raw/gmaps-8.jpg" alt="Terraza de madera nueva y puerta corrediza instalada por Cortney&#39;s Handyman Service" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Pintura exterior" data-en="Exterior painting">Exterior painting</span><img src="assets/raw/gmaps-4.jpg" alt="Pintura de fachada de estuco terminada" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Puerta nueva instalada" data-en="New door install">New door install</span><img src="assets/raw/gmaps-5.jpg" alt="Puerta corrediza de vidrio recien instalada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Instalacion de piso" data-en="Flooring install">Flooring install</span><img src="assets/raw/gmaps-10.jpg" alt="Cortney instalando piso de vinilo de lujo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:OLD_GALLERY_GRID.start()] + NEW_GALLERY_GRID + h[OLD_GALLERY_GRID.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 11. OPINIONES
# ---------------------------------------------------------------------------
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 34 reseñas verificadas en Google" data-en="5.0 out of 5 · 34 verified reviews on Google">5.0 out of 5 · 34 verified reviews on Google</span></p>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Cortney has been my handyman for several years now and has done general home repairs for me and also renovated my whole kitchen. He does amazing work and makes sure everything is up to your standards!"</blockquote>')
rep('<figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<figcaption class="text-sm"><span class="font-medium">Sara Weedin</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We recently had Cortney come by to fix two water leaks under our bathroom vanity, and he did an absolutely fantastic job. He was professional, humble, and very respectful throughout the entire visit. His pricing was fair, his workmanship..."</blockquote>')
rep('<figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<figcaption class="text-sm"><span class="font-medium">Tony Petrasso</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I called lots of big companies and smaller handyman people to help me repair a pool pump PVC plumbing pipe I busted. Cortney said he would come today on his way home from another job and he did everything PERFECTLY and for a lot less than others..."</blockquote>')
rep('<figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<figcaption class="text-sm"><span class="font-medium">Hank Valencia</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<a href="tel:+13522865123" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    f'<a href="{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 34 reseñas en Google" data-en="Read all 34 reviews on Google">Read all 34 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 12. UBICACION -> "Service area" (sin direccion exacta ni mapa, negocio movil)
# ---------------------------------------------------------------------------
OLD_UBICACION = re.search(r'<section id="ubicacion".*?</section>', h, flags=re.S)
assert OLD_UBICACION
NEW_UBICACION = '''<section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8 grid lg:grid-cols-2 gap-12 items-stretch">
      <div>
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Zona de servicio" data-en="Service area">Service area</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Atendemos" data-en="Serving">Serving</span> <span class="text-shine">Largo &amp; Clearwater</span></h2>
        <div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Zona de servicio" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Largo, Clearwater y el condado de Pinellas, FL. Trabajamos directamente en tu propiedad." data-en="Largo, Clearwater and Pinellas County, FL. We work directly at your property.">Largo, Clearwater and Pinellas County, FL. We work directly at your property.</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Llamanos" data-en="Call us">Call us</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Llama o escribe para un presupuesto gratis. Respondemos rapido." data-en="Call or text for a free estimate. We respond fast.">Call or text for a free estimate. We respond fast.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,100,160,0.4)]" href="tel:+13522865123">(352) 286-5123</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm1 15h-2v-2h2Zm0-4h-2V7h2Z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Calificacion en Google" data-en="Google rating">Google rating</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="5.0 de 5 estrellas en 34 reseñas verificadas de clientes reales." data-en="5.0 out of 5 stars across 34 verified reviews from real clients.">5.0 out of 5 stars across 34 verified reviews from real clients.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,100,160,0.4)]" href="''' + MAPS_URL + '''" target="_blank" rel="noopener" data-es="Ver en Google Maps" data-en="View on Google Maps">View on Google Maps</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame zoomable reveal min-h-[380px]" style="transition-delay:180ms">
        <img src="assets/raw/gmaps-8.jpg" alt="Terraza y puerta corrediza instaladas por Cortney&#39;s Handyman Service" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>
    </div>
  </section>'''
h = h[:OLD_UBICACION.start()] + NEW_UBICACION + h[OLD_UBICACION.end():]
print("UBICACION done")

# ---------------------------------------------------------------------------
# 13. CTA FINAL (sin boton secundario de Instagram)
# ---------------------------------------------------------------------------
rep('''<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Reparaciones hechas bien, a la primera." data-en="Repairs done right, the first time.">Repairs done right, the first time.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="tel:+13522865123" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>
      </div>''',
    '''<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Reparaciones hechas bien, a la primera." data-en="Repairs done right, the first time.">Repairs done right, the first time.</p>
      <h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu proxima reparacion," data-en="Your next repair,">Your next repair,</span> <span class="text-shine" data-es="bien hecha" data-en="done right">done right</span></h2>
      <p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Llama ahora para un presupuesto gratis en tu proxima reparacion o remodelacion en Largo y Clearwater." data-en="Call now for a free estimate on your next repair or remodel in Largo and Clearwater.">Call now for a free estimate on your next repair or remodel in Largo and Clearwater.</p>
      <div class="reveal flex flex-wrap justify-center gap-4" style="transition-delay:260ms">
        <a href="tel:+13522865123" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar: (352) 286-5123" data-en="Call: (352) 286-5123">Call: (352) 286-5123</a>
      </div>''')
print("CTA done")

# ---------------------------------------------------------------------------
# 14. FOOTER (sin logo, sin Instagram; columna de resenas en vez de "Siguenos")
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Cortney\'s Handyman</span>')
rep('''<div class="flex items-center gap-3 mb-4">
          <img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(190,207,240,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>''',
    '''<div class="flex items-center gap-3 mb-4">
          <span class="font-display text-lg tracking-[0.1em] uppercase">Cortney&#39;s Handyman</span>
        </div>''')
rep('<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Servicio de handyman en Largo, Clearwater y el condado de Pinellas, FL. Presupuestos gratis." data-en="Handyman service in Largo, Clearwater and Pinellas County, FL. Free estimates.">Handyman service in Largo, Clearwater and Pinellas County, FL. Free estimates.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>Largo &amp; Clearwater, FL</p>')
rep('<p><a href="tel:+13522865123" target="_blank" rel="noopener" class="hover:text-[#becff0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="tel:+13522865123" class="hover:text-[#becff0]">(352) 286-5123</a></p>')
rep('''<div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/_lashbloom/" target="_blank" rel="noopener" class="hover:text-[#becff0]">Instagram · @_lashbloom</a></p>
      </div>''',
    '''<div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reseñas" data-en="Reviews">Reviews</p>
        <p><a href="''' + MAPS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#becff0]">5.0 on Google &middot; 34 reviews</a></p>
      </div>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">&copy; 2026 Cortney&#39;s Handyman Service.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 15. BOOK-FLOAT (boton flotante -> llamar)
# ---------------------------------------------------------------------------
rep('''<a href="tel:+13522865123" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f2f5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>''',
    '''<a href="tel:+13522865123" class="book-float" aria-label="Call now">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f2f5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>''')
print("BOOK-FLOAT done")

open(PATH, "w", encoding="utf-8").write(h)
print("ALL WRITTEN OK")
