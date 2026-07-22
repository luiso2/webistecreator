import re

PATH = "output/slicker-barbershop-miami/index.html"
h = open(PATH).read()

BOOKSY = "https://booksy.com/en-us/1341780_slicker-barbershop_barber-shop_15889_miami"
BOOKSY_OLD = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
IG_URL_OLD = "https://www.instagram.com/pure.artistrysk/"
IG_URL = "https://www.instagram.com/herrera_barbero/"
IG_HANDLE_OLD = "@pure.artistrysk"
IG_HANDLE = "@herrera_barbero"
NAME = "Slicker Barbershop"
ADDR = "108 SW 9th St, Suite 32, Miami, FL 33130"
ADDR_MAPQ = "108+SW+9th+St,+Miami,+FL+33130"


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:160]
    h = h.replace(a, b, n)


def repall(a, b):
    global h
    assert a in h, "NO: " + a[:200]
    h = h.replace(a, b)


# ---------- 1. Proteger el badge Merktop ----------
m = re.search(r"\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n", h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------- 2. HEAD ----------
rep(
    '<meta name="theme-color" content="#0f0b07" />',
    '<meta name="theme-color" content="#0f0d17" />',
)
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    f'<title>{NAME} · Barbershop in Miami, FL | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    f'<meta name="description" content="{NAME}, Miami FL: precision fades, haircuts and beard trims by Juan Herrera in a private Brickell studio. 5.0 with 197 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    f'<meta property="og:title" content="{NAME} · Barbershop in Miami, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Precision fades, haircuts and beard trims. 5.0 on Booksy. Book online." />',
)
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />', '<meta property="og:image" content="assets/raw/bk-9.jpg" />')

# ---------- 3. JSON-LD ----------
OLD_LD_START = '  <script type="application/ld+json">'
m2 = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m2, "no se encontro JSON-LD"
NEW_LD = f"""<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "{NAME}",
    "description": "Barbershop in Miami, FL: precision fades, haircuts and beard trims in a private Brickell-area studio.",
    "address": {{ "@type": "PostalAddress", "streetAddress": "108 SW 9th St, Suite 32", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33130", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 25.7650985, "longitude": -80.1962608 }},
    "sameAs": ["{BOOKSY}", "{IG_URL}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "197", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "22:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday"], "opens": "09:00", "closes": "20:00" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Barbershop services", "itemListElement": [
      {{ "@type": "Offer", "price": "108", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "The OMBR Experience" }} }},
      {{ "@type": "Offer", "price": "64", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Haircut &amp; Beard" }} }},
      {{ "@type": "Offer", "price": "48", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Haircut (All ages)" }} }},
      {{ "@type": "Offer", "price": "28", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Beard Trim" }} }}
    ] }}
  }}
  </script>"""
h = h[: m2.start()] + NEW_LD + h[m2.end():]

repall(BOOKSY_OLD, BOOKSY)
repall(IG_URL_OLD, IG_URL)
repall(IG_HANDLE_OLD, IG_HANDLE)

# ---------- 4. Preloader ----------
rep('<span class="pre-word">Pure Artistry</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 5. NAV ----------
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
    f'<img src="assets/raw/bk-10.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Slicker <span class="text-[color:var(--accent-deep)]">Barbershop</span></span>',
)

# ---------- 6. HERO ----------
rep(
    'data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Miami, FL · Barbershop" data-en="Miami, FL · Barbershop">Miami, FL · Barbershop</p>',
)
rep(
    'data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Cortes con precisión de verdad." data-en="Cuts with real precision.">Cuts with real precision.</p>',
    n=2,
)
rep(
    '<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Fades y cortes con" data-en="Fades and cuts with">Fades and cuts with</span><br /><span data-es="atención al detalle " data-en="attention to detail, ">attention to detail, </span><span class="text-shine" data-es="total" data-en="every time">every time</span>',
)
rep(
    'data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    f'data-es="Cortes, fades y arreglo de barba en un estudio privado de Miami. Juan Herrera se toma su tiempo con cada cliente, con un 5.0 perfecto en 197 reseñas de Booksy." data-en="Haircuts, fades and beard grooming in a private Miami studio. Juan Herrera takes his time with every client, with a perfect 5.0 across 197 Booksy reviews.">Haircuts, fades and beard grooming in a private Miami studio. Juan Herrera takes his time with every client, with a perfect 5.0 across 197 Booksy reviews.</p>',
)
rep(
    'data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 197 reseñas en Booksy" data-en="5.0 · 197 reviews on Booksy">5.0 · 197 reviews on Booksy</span>',
)
rep(
    '<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-9.jpg" alt="Clean profile fade haircut" class="blur-up w-full h-full object-cover" />',
)
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg">The OMBR Experience</p>')
rep(
    'data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="$108 · 1h 30min" data-en="$108 · 1h 30min">$108 · 1h 30min</p>',
)

# ---------- 7. STRIP ----------
rep(
    '<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
    '<span data-count="197">197</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fades <span class="text-shine">&amp;</span> Beards</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cortes · Barba · Diseño" data-en="Haircuts · Beard · Design">Haircuts · Beard · Design</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Private <span class="text-shine">&amp;</span> 1:1</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Estudio privado" data-en="Private studio">Private studio</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">108 SW 9th St</p></div>',
)

# ---------- 8. MARQUEE (2 secuencias, cada palabra aparece 4 veces) ----------
MQ = [
    ("Silk Press", "The OMBR Experience"),
    ("Loc Retwist", "Haircut &amp; Beard"),
    ("Knotless Braids", "Haircut All Ages"),
    ("K-Tip Extensions", "Beard Trim"),
    ("Keratin", "Fades"),
    ("Orlando, FL", "Miami, FL"),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f"marquee count != 4 para {old}: {h.count(old_span)}"
    h = h.replace(old_span, new_span)

# ---------- 9. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Slicker Barbershop private studio interior" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Juan Herrera cutting a client\'s hair" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un barbero," data-en="One barber,">One barber,</span><br /><span class="text-shine" data-es="clientes de por vida" data-en="clients for life">clients for life</span></h2>',
)
rep(
    'data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    f'data-es="{NAME} es el estudio privado de Juan Herrera en Miami. Cortes, fades y arreglo de barba en una experiencia 1 a 1, sin apuros, con la conversacion y el detalle que sus clientes describen una y otra vez." data-en="{NAME} is Juan Herrera\'s private studio in Miami. Haircuts, fades and beard grooming in a one-on-one experience, unhurried, with the conversation and attention to detail his clients describe again and again.">{NAME} is Juan Herrera\'s private studio in Miami. Haircuts, fades and beard grooming in a one-on-one experience, unhurried, with the conversation and attention to detail his clients describe again and again.</p>',
)
rep(
    'data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus clientes lo confirman: algunos llevan mas de tres anos sin cortarse con nadie mas. 5.0 perfecto en 197 resenas verificadas de Booksy." data-en="His clients confirm it: some have not had a haircut from anyone else in over three years. A perfect 5.0 across 197 verified Booksy reviews.">His clients confirm it: some have not had a haircut from anyone else in over three years. A perfect 5.0 across 197 verified Booksy reviews.</p>',
)
rep(
    '<span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<span data-count="197">197</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
)
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    f'<img src="assets/raw/bk-11.jpg" alt="Juan Herrera, barber" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Juan Herrera · <span class="text-[color:var(--ink-40)]" data-es="Barbero" data-en="Barber">Barber</span></span>',
)

# ---------- 10. EL METODO ----------
rep(
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: corte, barba o el combo completo, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: haircut, beard or the full combo, and confirm instantly.">Pick your service on Booksy with clear price and duration: haircut, beard or the full combo, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta rapida" data-en="Quick consult">Quick consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma de la cara, largo actual y el estilo que buscas: de ahi sale el fade o el diseno exacto." data-en="Face shape, current length and the look you want: that is where the exact fade or design comes from.">Face shape, current length and the look you want: that is where the exact fade or design comes from.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De la Ombr Experience de 1h 30 al corte rapido de 1 hora: cada servicio recibe su tiempo completo, sin apuros." data-en="From the 1h 30min OMBR Experience to the 1-hour haircut: every service gets its full time, no rushing.">From the 1h 30min OMBR Experience to the 1-hour haircut: every service gets its full time, no rushing.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con la linea limpia y la barba perfilada, tal como cuentan sus resenas de Booksy. Tu proxima cita queda agendada." data-en="You leave with a clean line and a sharp beard, just as his Booksy reviews describe. Next visit booked before you go.">You leave with a clean line and a sharp beard, just as his Booksy reviews describe. Next visit booked before you go.</p>',
)

# ---------- 11. SERVICIOS ----------
OLD_SERV_GRID = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h,
    flags=re.S,
)
assert OLD_SERV_GRID, "no se encontro grid de servicios"

NEW_SERV_GRID = f"""<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">The OMBR Experience</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio completo de la casa: corte, diseno y arreglo de barba en una sola sesion extendida." data-en="The full house service: haircut, design and beard grooming in one extended session.">The full house service: haircut, design and beard grooming in one extended session.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$108</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito" data-en="Most booked">Most booked</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Haircut &amp; Beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte a tu medida mas arreglo de barba, el combo que mas reservan sus clientes." data-en="A custom haircut plus a beard trim, the combo his clients book most.">A custom haircut plus a beard trim, the combo his clients book most.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$64</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 20min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para todas las edades" data-en="All ages">All ages</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Haircut (All Ages)</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte clasico con linea limpia, para cualquier edad." data-en="A classic haircut with a clean line, for any age.">A classic haircut with a clean line, for any age.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$48</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Barba" data-en="Beard">Beard</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Beard Trim</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Perfilado y arreglo de barba con navaja, para un acabado limpio." data-en="Beard shaping and lineup with a razor, for a clean finish.">Beard shaping and lineup with a razor, for a clean finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$28</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">35min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      """
h = h[: OLD_SERV_GRID.start()] + NEW_SERV_GRID + h[OLD_SERV_GRID.end():]

rep(
    'data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    f'data-es="Precios y duraciones publicados por {NAME} en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.">Prices and durations as published by {NAME} on Booksy. Booking confirms instantly.</p>',
)
rep(
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Disponibilidad y precios exactos en tiempo real en Booksy." data-en="Exact prices and real time availability on Booksy.">Exact prices and real time availability on Booksy.</span></p>',
)

# ---------- 12. GALERIA ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="cuts">cuts</span></h2>',
)

OLD_GAL_GRID = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h,
    flags=re.S,
)
assert OLD_GAL_GRID, "no se encontro grid de galeria"

NEW_GAL_GRID = """<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Fade limpio" data-en="Clean fade">Clean fade</span><img src="assets/raw/bk-8.jpg" alt="Overhead view of a clean skin fade haircut" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Perfil terminado" data-en="Finished profile">Finished profile</span><img src="assets/raw/bk-9.jpg" alt="Side profile of a precision fade haircut" class="blur-up w-full h-full object-cover" /></div>
      </div>
    </div>
  </section>"""
h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end():]

# ---------- 13. OPINIONES ----------
rep(
    '<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 197 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 197 verified reviews on Booksy">5.0 out of 5 · 197 verified reviews on Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente servicio!!!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Arturo Lirio P…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excellent Service, professional barbershop, good customer service and a private location experience. Good conversation, Juan makes you feel comfortable all the time and the work is exceptional."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Guillermo V…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Juan is the most outstanding barber in town! I've been coming to Juan for the better part of 3 years now and I am always happy with his work. He has a customer for life!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mitchel L…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    'data-es="Leer las 197 reseñas en Booksy" data-en="Read all 197 reviews on Booksy">Read all 197 reviews on Booksy</a>',
)

# ---------- 14. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Miami, FL</span></h2>',
)
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', f'<p class="text-sm text-[color:var(--ink-60)] font-light">{ADDR}</p>')
rep(
    'href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    f'href="https://www.google.com/maps?q={ADDR_MAPQ}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
)
rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata. Abierto martes, jueves, viernes y sábado de 9:00 am a 10:00 pm, y miércoles de 9:00 am a 8:00 pm." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Tuesday, Thursday, Friday and Saturday 9:00 am to 10:00 pm, and Wednesday 9:00 am to 8:00 pm.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant. Open Tuesday, Thursday, Friday and Saturday 9:00 am to 10:00 pm, and Wednesday 9:00 am to 8:00 pm.</p>',
)
rep(
    'data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="Mira los cortes más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest cuts and DM any questions before your appointment.">See the latest cuts and DM any questions before your appointment.</p>',
)
rep(
    'title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    f'title="Map: {NAME}, {ADDR}"\n          src="https://www.google.com/maps?q={ADDR_MAPQ}&output=embed"',
)

# ---------- 15. CTA FINAL ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu corte" data-en="Your next cut">Your next cut</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva online en segundos: tu corte, tu barba o la OMBR Experience completa." data-en="Book online in seconds: your haircut, your beard trim, or the full OMBR Experience.">Book online in seconds: your haircut, your beard trim, or the full OMBR Experience.</p>',
)

# ---------- 16. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    f'<img src="assets/raw/bk-10.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Barbershop en Miami, FL. Atención con cita previa." data-en="Barbershop in Miami, FL. By appointment only.">Barbershop in Miami, FL. By appointment only.</p>',
)
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', f'<p>{ADDR}</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ================================================================
# 19. Paleta: gold -> deep indigo-violet (accent-deep #4d3f7a, accent-mid #786bb5)
#     Proteger merktop-badge ya hecho en el paso 1 (placeholder @@BADGE@@)
# ================================================================
HEX_PAIRS = [
    ('#d4a84b', '#4d3f7a'),
    ('#b8934a', '#786bb5'),
    ('#f0dc9e', '#c7bee6'),
    ('#9a7431', '#332a5c'),
    ('#e5c374', '#a89bd6'),
    ('#e8c476', '#ab9ed8'),
    ('#c9a04a', '#786bb5'),
    ('#96742c', '#372c68'),
    ('#6b5222', '#241d40'),
    ('#1c1408', '#120f1e'),
    ('#e9c3ab', '#c3b9e2'),
    ('#8a744a', '#4d3f7a'),
    ('#e8cf96', '#b0a4dc'),
    ('#f8eed3', '#e5e1f5'),
    ('#bfa060', '#6a5a9c'),
    ('#f0dcae', '#c9c0ea'),
    ('#faf1dc', '#e9e6f7'),
    ('#ecd9a8', '#b7ace0'),
    ('#c9ab6b', '#786bb5'),
    ('#241c0e', '#181430'),
]
for old, new in HEX_PAIRS:
    assert old in h, "paleta hex no encontrado: " + old
    h = h.replace(old, new)

RGB_PAIRS = [
    ('212,168,75', '77,63,122'),
    ('232,207,150', '176,164,220'),
    ('232,210,160', '178,168,222'),
    ('80,58,18', '36,29,64'),
    ('110,85,35', '44,35,80'),
    ('122,90,30', '55,44,104'),
    ('180,140,60', '110,96,172'),
    ('185,138,128', '150,138,190'),
    ('54,42,38', '38,32,54'),
]
for old, new in RGB_PAIRS:
    assert old in h, "paleta rgb no encontrado: " + old
    h = h.replace(old, new)

h = h.replace('@@BADGE@@', badge_block, 1)

open(PATH, "w").write(h)
print("BUILD OK: slicker-barbershop-miami")
