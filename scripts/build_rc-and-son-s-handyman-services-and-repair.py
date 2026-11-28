import re
import shutil

SLUG = "rc-and-son-s-handyman-services-and-repair"
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


# 1. Proteger el badge Merktop
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# 2. Paleta: gold -> verde bosque oscuro
HEX_PALETTE = [
    ("#d4a84b", "#3f8a5e"),
    ("#b8934a", "#4d9d6e"),
    ("#f0dc9e", "#aedcc0"),
    ("#9a7431", "#28673f"),
    ("#e5c374", "#6bab82"),
    ("#e8c476", "#70ad87"),
    ("#c9a04a", "#4a9768"),
    ("#96742c", "#28673f"),
    ("#e8cf96", "#b9e0c9"),
    ("#f8eed3", "#eef8f1"),
    ("#bfa060", "#5ca378"),
    ("#ecd9a8", "#c4e6d3"),
    ("#f0dcae", "#cdeadb"),
    ("#e9c3ab", "#c9e7d5"),
    ("#6b5222", "#1d4d30"),
    ("#1c1408", "#0c2014"),
    ("#8a744a", "#3f8060"),
    ("#faf1dc", "#eef8f2"),
    ("#c9ab6b", "#6fb391"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(63,138,94"),
    ("rgba(122,90,30", "rgba(40,99,63"),
    ("rgba(180,140,60", "rgba(91,163,138"),
    ("rgba(232,207,150", "rgba(185,224,201"),
    ("rgba(232,210,160", "rgba(196,230,211"),
    ("rgba(185,138,128", "rgba(145,194,178"),
    ("rgba(110,85,35", "rgba(44,99,78"),
    ("rgba(80,58,18", "rgba(29,77,48"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# 3. Globales: sin booking -> tel:
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+19043395630"
rep_all(OLD_BOOK, NEW_TEL, expect=13)
print("GLOBALS done")

MAPS_URL = "https://www.google.com/maps/place/RC+%26+Son's+Handyman+Services+%26+Repair/"

# 4. HEAD
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    "<title>RC &amp; Son's Handyman Services &amp; Repair · Jacksonville, FL | Emergency &amp; General Repairs | 4.5 on Google</title>")
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="RC &amp; Son\'s Handyman Services &amp; Repair, Jacksonville FL: emergency repairs, kitchen and bathroom remodeling, storm damage and general handyman work. 4.5 stars across 35 Google reviews. Call for a free estimate." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    "<meta property=\"og:title\" content=\"RC &amp; Son's Handyman Services &amp; Repair · Jacksonville, FL\" />")
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Emergency repairs, remodeling and general handyman work in Jacksonville. 4.5 on Google with 35 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-10.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/gmaps-10.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "RC & Son's Handyman Services & Repair",
    "description": "Handyman and repair company serving Jacksonville, FL: emergency repairs, kitchen and bathroom remodeling, storm and accident damage repair, and general home repairs.",
    "areaServed": { "@type": "City", "name": "Jacksonville" },
    "telephone": "+1-904-339-5630",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.5", "reviewCount": "35", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Handyman & repair services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Emergency & Same-Day Repairs" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Kitchen & Bathroom Remodeling" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Storm & Accident Damage Repair" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "General Handyman Repairs" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# 6. PRELOADER + NAV
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">RC</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">RC &amp; Son\'s</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(63,138,94,0.35)]" />',
    '<img src="assets/raw/gmaps-10.jpg" alt="RC &amp; Son\'s Handyman Services" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(63,138,94,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">RC &amp; <span class="text-[color:var(--accent-deep)]">Son\'s</span></span>')
rep('<a class="nav-link" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '', n=1)
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#galeria" data-es="Galería" data-en="Gallery">Galería</a>\n        ', '', n=1)
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Call now</span>', n=1)
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>')
print("NAV done")

# 7. HERO
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Jacksonville, FL · Handyman" data-en="Jacksonville, FL · Handyman">Jacksonville, FL · Handyman</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Reparaciones rapidas, trabajo que dura." data-en="Fast repairs, work that lasts.">Fast repairs, work that lasts.</p>',
    n=2)
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Reparaciones de emergencia" data-en="Emergency repairs">Emergency repairs</span><br /><span data-es="y remodelacion " data-en="and remodeling ">and remodeling </span><span class="text-shine" data-es="hechas bien" data-en="done right">done right</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="RC &amp; Son\'s responde el mismo dia a reparaciones de emergencia (desde un choque contra una vidriera hasta un ventilador de techo suelto en plena tormenta), ademas de remodelaciones completas de cocina y bano en Jacksonville, con 4.5 estrellas en 35 reseñas de Google." data-en="RC &amp; Son\'s shows up same-day for emergency repairs (from a car crashing into a storefront to a ceiling fan coming loose mid-storm), plus full kitchen and bathroom remodels across Jacksonville, with 4.5 stars across 35 Google reviews.">RC &amp; Son\'s shows up same-day for emergency repairs (from a car crashing into a storefront to a ceiling fan coming loose mid-storm), plus full kitchen and bathroom remodels across Jacksonville, with 4.5 stars across 35 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.5 · 35 reseñas en Google" data-en="4.5 · 35 reviews on Google">4.5 · 35 reviews on Google</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Llamar al (904) 339-5630" data-en="Call (904) 339-5630">Call (904) 339-5630</span>', n=1)
rep('''          <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @pure.artistrysk
          </a>
''', '')
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>\n          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Resenas reales en Google" data-en="Real Google reviews">Real Google reviews</span>\n          <span data-es="Presupuesto gratis" data-en="Free estimates">Free estimates</span>\n          <span data-es="Respuesta el mismo dia" data-en="Same-day response">Same-day response</span>')
rep('aria-label="Lo que encontrará el cliente"', 'aria-label="What you get"')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-10.jpg" alt="Cocina remodelada por RC and Sons en Jacksonville" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Llama hoy" data-en="Call today">Call today</p>
            <p class="font-display text-lg">Emergency Repairs</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Presupuesto gratis · Jacksonville" data-en="Free estimate · Jacksonville">Free estimate · Jacksonville</p>''')
print("HERO done")
open(PATH, "w", encoding="utf-8").write(h)
print("WROTE PARTIAL (hero) - continuing in part2")
h = open(PATH, encoding="utf-8").read()

# 8. STRIP
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="35">35</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Kitchen <span class="text-shine">&amp;</span> Bath</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Remodelacion completa" data-en="Full remodeling">Full remodeling</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl"><span data-es="Mismo" data-en="Same">Same</span> <span class="text-shine" data-es="dia" data-en="day">day</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Emergencias y reparaciones" data-en="Emergencies & repairs">Emergencies & repairs</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Jacksonville</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="&amp; alrededores" data-en="&amp; surrounding areas">&amp; surrounding areas</p></div>')
print("STRIP done")

# 9. MARQUEE
MARQUEE_WORDS = [
    ("Silk Press", "Emergency Repairs"),
    ("Loc Retwist", "Kitchen Remodels"),
    ("Knotless Braids", "Bathroom Remodels"),
    ("K-Tip Extensions", "Storm Damage Repair"),
    ("Keratin", "Free Estimates"),
    ("Orlando, FL", "Jacksonville, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# 10. EXPERIENCIA
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/gmaps-7.jpg" alt="Bano remodelado con ducha de bloques de vidrio" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/gmaps-8.jpg" alt="Cocina con gabinetes pintados de blanco" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Padre e hijo," data-en="Father and son,">Father and son,</span><br /><span class="text-shine" data-es="listos cuando los necesitas" data-en="ready when you need them">ready when you need them</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="RC &amp; Son\'s es un equipo familiar que atiende Jacksonville para lo urgente y lo planeado por igual: desde un local con la vidriera rota que necesitaba arreglo el mismo dia, hasta remodelaciones completas de cocina y bano hechas con calma y buen acabado." data-en="RC &amp; Son\'s is a family team serving Jacksonville for both the urgent and the planned: from a storefront with a broken window that needed same-day fixing, to full kitchen and bathroom remodels done with care and a clean finish.">RC &amp; Son\'s is a family team serving Jacksonville for both the urgent and the planned: from a storefront with a broken window that needed same-day fixing, to full kitchen and bathroom remodels done with care and a clean finish.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="El resultado: 4.5 de calificacion en 35 reseñas de Google, con clientes que destacan lo rapido que llegan en una emergencia y lo bien que queda el trabajo terminado." data-en="The result: a 4.5 rating across 35 Google reviews, with clients praising how fast they show up for an emergency and how clean the finished work looks.">The result: a 4.5 rating across 35 Google reviews, with clients praising how fast they show up for an emergency and how clean the finished work looks.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="35">35</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Resenas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Mismo" data-en="Same">Same</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="dia" data-en="day">day</p></div>''')
rep('<p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<p class="font-display text-xl text-shine"><span data-count="4.5" data-decimals="1">4.5</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>')
rep('''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(63,138,94,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>
          </div>''',
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/gmaps-10.jpg" alt="RC and Sons Handyman Services" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(63,138,94,0.3)]" loading="lazy" />
            <span class="text-sm font-light">RC &amp; Son's · <span class="text-[color:var(--ink-40)]" data-es="Handyman familiar" data-en="Family handyman">Family handyman</span></span>
          </div>''')
print("EXPERIENCIA done")

# 11. METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu proyecto, paso a paso" data-en="Your project, step by step">Tu proyecto, paso a paso</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Asi se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span></h2>')
rep('<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Llama ahora" data-en="Call now">Call now</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cuentanos si es una emergencia o un proyecto planeado: respondemos el mismo dia para lo urgente." data-en="Tell us if it is an emergency or a planned project: we respond the same day for anything urgent.">Tell us if it is an emergency or a planned project: we respond the same day for anything urgent.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Presupuesto gratis" data-en="Free estimate">Free estimate</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Revisamos el alcance real del trabajo y te dejamos un precio claro antes de empezar, sin sorpresas." data-en="We review the real scope of the job and leave you a clear price before starting, no surprises.">We review the real scope of the job and leave you a clear price before starting, no surprises.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Desde un ventilador de techo roto en plena tormenta hasta una cocina completa: cada trabajo recibe la misma atencion al detalle." data-en="From a ceiling fan broken mid-storm to a full kitchen: every job gets the same attention to detail.">From a ceiling fan broken mid-storm to a full kitchen: every job gets the same attention to detail.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Trabajo terminado" data-en="Finished right">Finished right</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Limpiamos despues de cada trabajo y dejamos un acabado que se nota, tal como lo describen las reseñas de Google." data-en="We clean up after every job and leave a finish that shows, exactly as Google reviews describe it.">We clean up after every job and leave a finish that shows, exactly as Google reviews describe it.</p>')
print("METODO done")
open(PATH, "w", encoding="utf-8").write(h)
print("WROTE PARTIAL2")
h = open(PATH, encoding="utf-8").read()

# 12. SERVICIOS
rep('data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que" data-en="What we">Lo que</span> <span class="text-shine" data-es="hacemos" data-en="do">do</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Cada trabajo se cotiza segun el alcance real. Presupuesto gratis, sin compromiso." data-en="Every job is quoted based on its real scope. Free estimate, no obligation.">Every job is quoted based on its real scope. Free estimate, no obligation.</p>')

OLD_SERVICES_GRID = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert OLD_SERVICES_GRID
NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(63,138,94,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Respuesta rapida" data-en="Fast response">Fast response</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reparaciones de emergencia" data-en="Emergency Repairs">Emergency Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Vidrieras rotas, techos sueltos, puertas de tormenta: respuesta el mismo dia cuando algo se rompe sin avisar." data-en="Broken storefronts, loose fans, storm doors: same-day response when something breaks without warning.">Broken storefronts, loose fans, storm doors: same-day response when something breaks without warning.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Cotizacion" data-en="Estimate">Estimate</p></div>
            <a href="tel:+19043395630" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cocina y bano" data-en="Kitchen & Bath">Kitchen & Bath</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Remodelacion completa" data-en="Full Remodeling">Full Remodeling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Gabinetes, electrodomesticos, duchas de bloques de vidrio y acabados nuevos, de principio a fin." data-en="Cabinets, appliances, glass-block showers and new finishes, start to finish.">Cabinets, appliances, glass-block showers and new finishes, start to finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Cotizacion" data-en="Estimate">Estimate</p></div>
            <a href="tel:+19043395630" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Carpinteria" data-en="Carpentry">Carpentry</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Muebles a medida" data-en="Custom Built-Ins">Custom Built-Ins</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Libreros, estantes y muebles empotrados hechos a la medida de tu espacio." data-en="Bookshelves, shelving and built-ins made to fit your space.">Bookshelves, shelving and built-ins made to fit your space.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Cotizacion" data-en="Estimate">Estimate</p></div>
            <a href="tel:+19043395630" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="General" data-en="General">General</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reparaciones generales" data-en="General Handyman Repairs">General Handyman Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Drywall, pintura, instalaciones y todo lo que tu casa o tu negocio necesiten." data-en="Drywall, paint, installations and whatever your home or business needs.">Drywall, paint, installations and whatever your home or business needs.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Cotizacion" data-en="Estimate">Estimate</p></div>
            <a href="tel:+19043395630" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:OLD_SERVICES_GRID.start()] + NEW_SERVICES_GRID + h[OLD_SERVICES_GRID.end():]

OLD_SERVICES_NOTE = re.search(r'<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">.*?</p>', h, flags=re.S)
assert OLD_SERVICES_NOTE
NEW_SERVICES_NOTE = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: instalaciones, montaje de muebles y reparaciones comerciales. Llama para contarnos tu proyecto." data-en="Also: installations, furniture assembly and commercial repairs. Call to tell us about your project.">Also: installations, furniture assembly and commercial repairs. Call to tell us about your project.</span></p>'
h = h[:OLD_SERVICES_NOTE.start()] + NEW_SERVICES_NOTE + h[OLD_SERVICES_NOTE.end():]
print("SERVICIOS done")

# 13. GALERIA
OLD_GALLERY_GRID = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert OLD_GALLERY_GRID
NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Reparacion de emergencia" data-en="Emergency repair">Emergency repair</span><img src="assets/raw/gmaps-9.jpg" alt="Instalacion de piso en local comercial tras reparacion de emergencia" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Bano remodelado" data-en="Remodeled bathroom">Remodeled bathroom</span><img src="assets/raw/gmaps-7.jpg" alt="Ducha de bloques de vidrio en bano remodelado" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Muebles a medida" data-en="Custom built-ins">Custom built-ins</span><img src="assets/raw/gmaps-5.jpg" alt="Libreros empotrados hechos a la medida" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Cocina terminada" data-en="Finished kitchen">Finished kitchen</span><img src="assets/raw/gmaps-10.jpg" alt="Cocina con electrodomesticos nuevos instalados" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Porche techado" data-en="Covered porch">Covered porch</span><img src="assets/raw/gmaps-4.jpg" alt="Porche con pergola de madera construida" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:OLD_GALLERY_GRID.start()] + NEW_GALLERY_GRID + h[OLD_GALLERY_GRID.end():]
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>\n        </div>\n        <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">\n          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>\n          @pure.artistrysk\n        </a>\n      </div>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galeria" data-en="Gallery">Gallery</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="work">work</span></h2>\n        </div>\n      </div>')
print("GALERIA done")

# 14. OPINIONES
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.5 de 5 · 35 resenas verificadas en Google" data-en="4.5 out of 5 · 35 verified reviews on Google">4.5 out of 5 · 35 verified reviews on Google</span></p>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"In October 2020, a car drove into our store front. That same day, RC &amp; Son\'s had a temporary store front up in less than 6 hours! I would highly recommend them!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Armando DiBenedetto</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"It was storming and my ceiling fan came undone, gave him a call. He came the same day, fixed my ceiling fan and went about his day! I will go with RC and Sons if I need anything else when it comes to needing a handyman."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Hazel Bolduc</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"RC came over on short notice to redo the installation of my storm door after a relative botched the job terribly. The door was reinstalled in a short time and it turned out excellently. I\'m forever grateful to them for helping me."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Susan Maynard</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>')
rep('<a href="tel:+19043395630" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    f'<a href="{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 35 resenas en Google" data-en="Read all 35 reviews on Google">Read all 35 reviews on Google</a>')
print("OPINIONES done")
open(PATH, "w", encoding="utf-8").write(h)
print("WROTE PARTIAL3")
h = open(PATH, encoding="utf-8").read()

# 15. UBICACION -> service area (direccion de Maps es residencial)
OLD_UBICACION = re.search(r'<section id="ubicacion".*?</section>', h, flags=re.S)
assert OLD_UBICACION
NEW_UBICACION = '''<section id="ubicacion" class="relative py-24 sm:py-32 bg-[color:var(--bg-2)] border-y border-[color:var(--accent-ghost)] grain">
    <span class="sec-num" aria-hidden="true">06</span>
    <div class="max-w-5xl mx-auto px-5 sm:px-8">
      <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Area de servicio" data-en="Service area">Service area</p>
      <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Trabajamos en" data-en="We work across">We work across</span> <span class="text-shine">Jacksonville</span></h2>
      <div class="grid sm:grid-cols-2 gap-5">
        <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
          <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
          <div>
            <p class="font-medium mb-1" data-es="Donde trabajamos" data-en="Where we work">Where we work</p>
            <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Jacksonville y alrededores, hogares y negocios. Servicio a domicilio, sin oficina para visitar." data-en="Jacksonville and surrounding areas, homes and businesses. We come to you, no storefront to visit.">Jacksonville and surrounding areas, homes and businesses. We come to you, no storefront to visit.</p>
          </div>
        </div>
        <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
          <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <div>
            <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
            <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sabado, 8am a 5pm. Llama para emergencias o para agendar tu presupuesto gratis." data-en="Monday to Saturday, 8am to 5pm. Call for emergencies or to schedule your free estimate.">Monday to Saturday, 8am to 5pm. Call for emergencies or to schedule your free estimate.</p>
            <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(63,138,94,0.4)]" href="tel:+19043395630" data-es="Llamar al (904) 339-5630" data-en="Call (904) 339-5630">Call (904) 339-5630</a>
          </div>
        </div>
      </div>
    </div>
  </section>'''
h = h[:OLD_UBICACION.start()] + NEW_UBICACION + h[OLD_UBICACION.end():]
print("UBICACION done")

# 16. CTA FINAL
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu proyecto" data-en="Your project">Your project</span> <span class="text-shine" data-es="puede empezar hoy" data-en="can start today">can start today</span></h2>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Llama ahora para un presupuesto gratis, o para una reparacion de emergencia el mismo dia." data-en="Call now for a free estimate, or for a same-day emergency repair.">Call now for a free estimate, or for a same-day emergency repair.</p>')
rep('<a href="tel:+19043395630" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="tel:+19043395630" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (904) 339-5630" data-en="Call (904) 339-5630">Call (904) 339-5630</a>')
print("CTA FINAL done")

# 17. FOOTER
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">RC and Sons</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(185,224,201,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>''',
    '''<img src="assets/raw/gmaps-10.jpg" alt="RC and Sons Handyman" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(185,224,201,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">RC &amp; Son's</span>''')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Handyman familiar en Jacksonville, FL. Servicio a domicilio, emergencias el mismo dia." data-en="Family handyman serving Jacksonville, FL. We come to you, same-day emergencies.">Family handyman serving Jacksonville, FL. We come to you, same-day emergencies.</p>')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="tel:+19043395630" target="_blank" rel="noopener" class="hover:text-[#c9e7d5]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>Jacksonville &amp; surrounding areas, FL</p>
        <p><a href="tel:+19043395630" class="hover:text-[#c9e7d5]">(904) 339-5630</a></p>''')
OLD_FOOTER_FOLLOW = re.search(r'<div class="text-sm font-light text-\[color:var\(--ink-60\)\] space-y-2">\s*<p class="text-xs tracking-\[0\.3em\] uppercase text-\[color:var\(--ink-40\)\] mb-3" data-es="Síguenos".*?</div>', h, flags=re.S)
assert OLD_FOOTER_FOLLOW
NEW_FOOTER_FOLLOW = '''<div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Resenas" data-en="Reviews">Reviews</p>
        <p><a href="''' + MAPS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#c9e7d5]">Google · 4.5 (35)</a></p>
      </div>'''
h = h[:OLD_FOOTER_FOLLOW.start()] + NEW_FOOTER_FOLLOW + h[OLD_FOOTER_FOLLOW.end():]
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    "<p class=\"text-xs text-[color:var(--ink-40)]\">&copy; 2026 RC &amp; Son's Handyman Services &amp; Repair.</p>")
print("FOOTER done")

# 18. Boton flotante
rep('<a href="tel:+19043395630" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="tel:+19043395630" class="book-float" aria-label="Llamar ahora">')
rep('<span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span class="book-float-label" data-es="Llamar ahora" data-en="Call now">Call now</span>')
print("BOOK-FLOAT done")

open(PATH, "w", encoding="utf-8").write(h)
print("WROTE", PATH)
