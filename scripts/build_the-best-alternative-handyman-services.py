import re
import shutil

SLUG = "the-best-alternative-handyman-services"
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


badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

HEX_PALETTE = [
    ("#d4a84b", "#51a37d"), ("#b8934a", "#53886f"), ("#f0dc9e", "#87ccab"), ("#9a7431", "#3e6f58"),
    ("#e5c374", "#6abb95"), ("#e8c476", "#6bbe98"), ("#c9a04a", "#529877"), ("#96742c", "#3a6b54"),
    ("#e8cf96", "#82c3a5"), ("#f8eed3", "#abdbc5"), ("#bfa060", "#5d977c"), ("#ecd9a8", "#8ec9ae"),
    ("#f0dcae", "#92ceb2"), ("#e9c3ab", "#91c6ad"), ("#6b5222", "#2b4d3d"), ("#1c1408", "#0b1410"),
    ("#8a744a", "#4b695b"), ("#faf1dc", "#b1dfc9"), ("#c9ab6b", "#63a385"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(81,163,125"), ("rgba(122,90,30", "rgba(43,86,66"),
    ("rgba(180,140,60", "rgba(74,130,104"), ("rgba(232,207,150", "rgba(130,195,165"),
    ("rgba(232,210,160", "rgba(137,196,169"), ("rgba(185,138,128", "rgba(114,152,134"),
    ("rgba(110,85,35", "rgba(44,79,63"), ("rgba(80,58,18", "rgba(27,56,43"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_TEL = "tel:+18633983165"
c = h.count(OLD_BOOK)
assert c > 0, c
h = h.replace(OLD_BOOK, NEW_TEL)
print(f"GLOBALS done ({c} Booksy->tel)")

MAPS_URL = "https://www.google.com/maps/place/The+Best+Alternative+Handyman+Services/data=!4m7!3m6!1s0xaad5e35b9ff54795:0x58c82a39e031449e!8m2!3d27.9671276!4d-82.418873!16s%2Fg%2F11v0f7y21t!19sChIJlUf1n1vj1aoRnkQx4DkqyFg?authuser=0&hl=en&g_ep=EgoyMDI2MTEyMy4wIJJjKgBIAVAD&rclk=1"

rep(f'href="{NEW_TEL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    f'href="{MAPS_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 11 reseñas en Google" data-en="Read all 11 reviews on Google">Read all 11 reviews on Google</a>')
print("REVIEWS LINK fixed")

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"

rep(f'''<a href="{OLD_IG_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @pure.artistrysk
          </a>''', '', n=1)

rep(f'''<a href="{OLD_IG_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @pure.artistrysk
        </a>''', '', n=1)

rep(f'<a href="{OLD_IG_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>', '', n=1)
print("SOCIAL BUTTONS removed (no verified FB/IG)")

rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>The Best Alternative Handyman Services · Handyman in Brandon, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="The Best Alternative Handyman Services, Brandon FL: cabinet and closet installs, and quick home repairs. 5.0 stars across 11 Google reviews. Family owned, se habla espanol." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="The Best Alternative Handyman Services · Handyman in Brandon, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Cabinet and closet installs, quick home repairs. 5.0 on Google with 11 reviews. Family owned, se habla espanol." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/gmaps-2.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/gmaps-1.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "The Best Alternative Handyman Services",
    "description": "Family owned handyman service serving Brandon, FL and the surrounding area: cabinet and closet installation, plumbing fixes and general home repairs.",
    "areaServed": [{ "@type": "City", "name": "Brandon" }, { "@type": "AdministrativeArea", "name": "Hillsborough County" }],
    "telephone": "+1-863-398-3165",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "11", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Handyman services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Cabinet & Closet Installation" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Plumbing Fixes" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "General Home Repairs" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">BA</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Best Alternative</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(81,163,125,0.35)]" />',
    '<img src="assets/raw/gmaps-1.jpg" alt="The Best Alternative Handyman Services" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(81,163,125,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Best <span class="text-[color:var(--accent-deep)]">Alternative</span></span>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Call now</span>', n=1)
rep(f'href="{NEW_TEL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    f'href="{NEW_TEL}" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>')
print("NAV done")

rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Brandon, FL · Handyman" data-en="Brandon, FL · Handyman">Brandon, FL · Handyman</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Instalaciones y reparaciones, bien hechas." data-en="Installs and repairs, done right.">Installs and repairs, done right.</p>',
    n=2)
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Gabinetes, closets" data-en="Cabinets, closets">Cabinets, closets</span><br /><span data-es="y reparaciones rapidas, " data-en="and quick repairs, ">and quick repairs, </span><span class="text-shine" data-es="bien hechos" data-en="done right">done right</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="The Best Alternative Handyman Services es un negocio familiar en Brandon que instala gabinetes y closets, y resuelve reparaciones de plomeria y de la casa con estimados rapidos. Ed y su esposa hablan ingles y espanol, con 5.0 perfecto en 11 reseñas de Google." data-en="The Best Alternative Handyman Services is a family owned business in Brandon installing cabinets and closets, and handling plumbing and household repairs with fast estimates. Ed and his wife speak English and Spanish, with a perfect 5.0 across 11 Google reviews.">The Best Alternative Handyman Services is a family owned business in Brandon installing cabinets and closets, and handling plumbing and household repairs with fast estimates. Ed and his wife speak English and Spanish, with a perfect 5.0 across 11 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 11 reseñas en Google" data-en="5.0 · 11 reviews on Google">5.0 · 11 reviews on Google</span>')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Llamar al (863) 398-3165" data-en="Call (863) 398-3165">Call (863) 398-3165</span>', n=1)
rep('data-es="Fotos reales" data-en="Real work">Fotos reales</span>\n          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>\n          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>',
    'data-es="Reseñas reales en Google" data-en="Real Google reviews">Real Google reviews</span>\n          <span data-es="Presupuesto gratis" data-en="Free estimates">Free estimates</span>\n          <span data-es="Se habla espanol" data-en="Se habla espanol">Se habla espanol</span>')
rep('aria-label="Lo que encontrará el cliente"', 'aria-label="What you get"')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/gmaps-2.jpg" alt="Finished kitchen cabinet install by The Best Alternative Handyman Services in Brandon, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Llama hoy" data-en="Call today">Call today</p>
            <p class="font-display text-lg">Free Estimate</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Brandon, FL" data-en="Brandon, FL">Brandon, FL</p>''')
print("HERO done")

rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="11">11</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Cabinets <span class="text-shine">&amp;</span> Closets</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Instalacion - Plomeria" data-en="Installation - Plumbing">Installation - Plumbing</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl"><span data-es="Abierto" data-en="Open">Open</span> 6</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Dias a la semana, domingo cerrado" data-en="Days a week, closed Sundays">Days a week, closed Sundays</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Brandon</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">&amp; Hillsborough County</p></div>')
print("STRIP done")

MARQUEE_WORDS = [
    ("Silk Press", "Cabinet Installs"),
    ("Loc Retwist", "Closet Shelving"),
    ("Knotless Braids", "Plumbing Fixes"),
    ("K-Tip Extensions", "Free Estimates"),
    ("Keratin", "Se Habla Espanol"),
    ("Orlando, FL", "Brandon, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="frame zoomable aspect-[4/5] img-reveal">
        <img src="assets/raw/gmaps-1.jpg" alt="Plumbing repair tools used by The Best Alternative Handyman Services" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Un negocio," data-en="One family,">One family,</span><br /><span class="text-shine" data-es="trabajo hecho con cuidado" data-en="work done with care">work done with care</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="The Best Alternative Handyman Services es un negocio familiar en Brandon: Ed y su esposa instalan gabinetes y closets, y resuelven reparaciones de plomeria y de la casa, hablando ingles y espanol con cada cliente." data-en="The Best Alternative Handyman Services is a family business in Brandon: Ed and his wife install cabinets and closets, and handle plumbing and household repairs, speaking English and Spanish with every customer.">The Best Alternative Handyman Services is a family business in Brandon: Ed and his wife install cabinets and closets, and handle plumbing and household repairs, speaking English and Spanish with every customer.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus clientes lo confirman: estimados rapidos, mismo dia de instalacion cuando se necesita, y precios razonables. 5.0 perfecto en 11 reseñas verificadas de Google." data-en="Customers confirm it: fast estimates, same-day installation when needed, and reasonable pricing. A perfect 5.0 across 11 verified Google reviews.">Customers confirm it: fast estimates, same-day installation when needed, and reasonable pricing. A perfect 5.0 across 11 verified Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="11">11</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Rapido" data-en="Fast">Fast</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Mismo dia" data-en="Same-day service">Same-day service</p></div>''')
rep('''<p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p>''',
    '''<p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(81,163,125,0.3)]" loading="lazy" />',
    '<img src="assets/raw/gmaps-1.jpg" alt="The Best Alternative Handyman Services team" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(81,163,125,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="text-sm font-light">Best Alternative · <span class="text-[color:var(--ink-40)]" data-es="Negocio familiar" data-en="Family owned">Family owned</span></span>')
print("EXPERIENCIA done")

rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Como trabajamos" data-en="How we work">How we work</p>')
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="De la llamada" data-en="From the call">From the call</span> <span class="text-shine" data-es="al trabajo terminado" data-en="to the finished job">to the finished job</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Llama o escribe" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nos cuentas lo que necesitas instalar o reparar y te damos un estimado rapido, a veces el mismo dia." data-en="Tell us what needs installing or fixing and we give you a fast estimate, sometimes the same day.">Tell us what needs installing or fixing and we give you a fast estimate, sometimes the same day.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Visita al lugar" data-en="On-site visit">On-site visit</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Vemos el espacio o el problema en persona antes de empezar, para un precio justo y sin sorpresas." data-en="We look at the space or the problem in person before starting, for a fair price with no surprises.">We look at the space or the problem in person before starting, for a fair price with no surprises.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="El trabajo se hace" data-en="The work gets done">The work gets done</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Instalacion de gabinetes y closets, o la reparacion que necesites, con limpieza al terminar." data-en="Cabinet and closet installation, or the repair you need, with cleanup when the job is done.">Cabinet and closet installation, or the repair you need, with cleanup when the job is done.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Revision final" data-en="Final walkthrough">Final walkthrough</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Revisamos el trabajo juntos antes de irnos. Si algo no te convence, lo corregimos ahi mismo." data-en="We walk through the finished work together before we leave. If something is not right, we fix it on the spot.">We walk through the finished work together before we leave. If something is not right, we fix it on the spot.</p>''')
print("METODO done")

rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Estimado rapido en cada trabajo, a veces el mismo dia." data-en="Fast estimate on every job, sometimes same day.">Fast estimate on every job, sometimes same day.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Lo que" data-en="What we">What we</span> <span class="text-shine" data-es="hacemos" data-en="do">do</span>')

OLD_SERVICES = re.search(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', h, flags=re.S)
assert OLD_SERVICES
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(81,163,125,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Especialidad" data-en="Specialty">Specialty</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Gabinetes y closets" data-en="Cabinet &amp; Closet Installs">Cabinet &amp; Closet Installs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Instalacion prolija de gabinetes de cocina y estantes de closet, con estimados rapidos y servicio el mismo dia cuando se necesita." data-en="Clean installation of kitchen cabinets and closet shelving, with fast estimates and same-day service when needed.">Clean installation of kitchen cabinets and closet shelving, with fast estimates and same-day service when needed.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Presupuesto" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18633983165" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Plomeria" data-en="Plumbing">Plumbing</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reparaciones de plomeria" data-en="Plumbing Fixes">Plumbing Fixes</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Fugas de llave y otros problemas de plomeria resueltos rapido, con precios razonables." data-en="Faucet leaks and other plumbing issues fixed fast, at a reasonable price.">Faucet leaks and other plumbing issues fixed fast, at a reasonable price.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Presupuesto" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18633983165" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="General" data-en="General">General</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reparaciones generales" data-en="General Repairs">General Repairs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Lo que la casa necesite arreglar, con atencion al detalle y buena comunicacion." data-en="Whatever the house needs fixed, with attention to detail and clear communication.">Whatever the house needs fixed, with attention to detail and clear communication.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Presupuesto" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18633983165" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Familiar" data-en="Family">Family</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Se habla espanol" data-en="Se Habla Espanol">Se Habla Espanol</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Negocio familiar, bilingue, atencion directa con Ed y su esposa en cada trabajo." data-en="A bilingual, family owned business, with Ed and his wife directly involved in every job.">A bilingual, family owned business, with Ed and his wife directly involved in every job.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Gratis" data-en="Free">Free</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Presupuesto" data-en="Estimate">Estimate</p></div>
            <a href="tel:+18633983165" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
'''
h = h[:OLD_SERVICES.start()] + NEW_SERVICES + h[OLD_SERVICES.end():]

OLD_NOTE = re.search(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', h, flags=re.S)
assert OLD_NOTE
h = h[:OLD_NOTE.start()] + OLD_NOTE.group(1) + '<span data-es="No ves tu proyecto en la lista? Llama y te damos un presupuesto gratis." data-en="Do not see your project listed? Call and we will give you a free estimate.">Do not see your project listed? Call and we will give you a free estimate.</span>' + OLD_NOTE.group(2) + h[OLD_NOTE.end():]
print("SERVICIOS done")

rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="results">results</span>')

OLD_GAL_LINK = re.search(r'<a href="tel:\+18633983165" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">.*?</a>\s*', h, flags=re.S)
if OLD_GAL_LINK:
    h = h[:OLD_GAL_LINK.start()] + h[OLD_GAL_LINK.end():]

OLD_GALLERY = re.search(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert OLD_GALLERY
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Gabinetes instalados" data-en="Installed cabinets">Installed cabinets</span><img src="assets/raw/gmaps-3.jpg" alt="Gabinetes de cocina instalados por The Best Alternative Handyman Services" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Detalle de acabado" data-en="Finish detail">Finish detail</span><img src="assets/raw/gmaps-4.jpg" alt="Detalle de molduras de gabinetes instalados" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:OLD_GALLERY.start()] + NEW_GALLERY + h[OLD_GALLERY.end():]
print("GALERIA done")

rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="nuestros clientes" data-en="customers say">nuestros clientes</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 11 reseñas verificadas en Google" data-en="5.0 out of 5 · 11 verified reviews on Google">5.0 out of 5 · 11 verified reviews on Google</span>')

OLD_T1 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>'''
NEW_T1 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Ed did an awesome job installing our cabinets. Family owned and operated. Ed and his wife speak English and Spanish."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ramon Arguinzoni</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>'''
rep(OLD_T1, NEW_T1)

OLD_T2 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>'''
NEW_T2 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Ed was professional, courteous, and installed my closet shelving with the utmost care. His estimate process was fast and thorough, he even offered same day installation service."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tessha Parran</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>'''
rep(OLD_T2, NEW_T2)

OLD_T3 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>'''
NEW_T3 = '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We had a bathroom tub faucet issue, and he fixed it within 30 minutes and gave us a very reasonable price. He was very quick to respond and came out within a day to fix our problem."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Amy Chesnut</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>'''
rep(OLD_T3, NEW_T3)
print("OPINIONES done")

rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Area de servicio en" data-en="Serving">Serving</span> <span class="text-shine" data-es="Brandon" data-en="Brandon">Brandon</span>')

OLD_LOC_CARDS = re.search(r'<div class="space-y-4">.*?</div>\s*</div>\s*<div class="frame map-frame reveal min-h-\[380px\]".*?</div>\s*</div>\s*</section>', h, flags=re.S)
assert OLD_LOC_CARDS
NEW_LOC = '''<div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Area de servicio" data-en="Service area">Service area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Brandon y el resto del condado de Hillsborough." data-en="Brandon and the rest of Hillsborough County.">Brandon and the rest of Hillsborough County.</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Llama o escribe" data-en="Call or text">Call or text</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Estimado rapido por telefono, a veces servicio el mismo dia." data-en="Fast estimate over the phone, sometimes same-day service.">Fast estimate over the phone, sometimes same-day service.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(81,163,125,0.4)]" href="tel:+18633983165" data-es="(863) 398-3165" data-en="(863) 398-3165">(863) 398-3165</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a sabado, 5am a 11pm. Domingo cerrado." data-en="Monday to Saturday, 5am to 11pm. Closed Sundays.">Monday to Saturday, 5am to 11pm. Closed Sundays.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="frame reveal min-h-[380px]" style="transition-delay:180ms">
        <img src="assets/raw/gmaps-3.jpg" alt="Gabinetes terminados por The Best Alternative Handyman Services" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>
    </div>
  </section>'''
h = h[:OLD_LOC_CARDS.start()] + NEW_LOC + h[OLD_LOC_CARDS.end():]
print("UBICACION done")

rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Una instalacion bien hecha" data-en="A job done right">A job done right</span> <span class="text-shine" data-es="esta a una llamada" data-en="is one call away">is one call away</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Estimado rapido, a veces el mismo dia. Gabinetes, closets, plomeria o esa reparacion pendiente en la casa." data-en="Fast estimate, sometimes same day. Cabinets, closets, plumbing or that repair you have been putting off.">Fast estimate, sometimes same day. Cabinets, closets, plumbing or that repair you have been putting off.</p>')
rep('<a href="tel:+18633983165" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="tel:+18633983165" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (863) 398-3165" data-en="Call (863) 398-3165">Call (863) 398-3165</a>')
print("CTA FINAL done")

rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Best Alternative</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(130,195,165,0.35)]" loading="lazy" />',
    '<img src="assets/raw/gmaps-1.jpg" alt="The Best Alternative Handyman Services" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(130,195,165,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">The Best Alternative Handyman Services</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Negocio familiar de handyman en Brandon, FL. Presupuesto gratis por telefono." data-en="Family owned handyman business serving Brandon, FL. Free estimates by phone.">Family owned handyman business serving Brandon, FL. Free estimates by phone.</p>')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="tel:+18633983165" target="_blank" rel="noopener" class="hover:text-[#91c6ad]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>Brandon, FL</p>
        <p><a href="tel:+18633983165" class="hover:text-[#91c6ad]">(863) 398-3165</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="hover:text-[#91c6ad]">Instagram · @pure.artistrysk</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Horario" data-en="Hours">Hours</p>
        <p data-es="Lun-Sab: 5am-11pm" data-en="Mon-Sat: 5am-11pm">Mon-Sat: 5am-11pm</p>
        <p data-es="Domingo: cerrado" data-en="Sunday: closed">Sunday: closed</p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 The Best Alternative Handyman Services.</p>')
print("FOOTER done")

rep('<span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span class="book-float-label" data-es="Llamar" data-en="Call now">Call now</span>')
rep('aria-label="Reservar cita online"', 'aria-label="Call The Best Alternative Handyman Services"')

open(PATH, "w", encoding="utf-8").write(h)
print("WRITTEN", PATH)
