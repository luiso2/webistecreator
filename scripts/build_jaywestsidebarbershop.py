import re

PATH = "output/jaywestsidebarbershop/index.html"
h = open(PATH).read()

BOOKSY_OLD = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
BOOKSY = "https://booksy.com/en-us/1723181_jay-westside-barbershop_barber-shop_15761_tampa"
IG_URL_OLD = "https://www.instagram.com/pure.artistrysk/"
IG_URL = "https://www.instagram.com/jadielcutzpr/"
IG_HANDLE_OLD = "@pure.artistrysk"
IG_HANDLE = "@jadielcutzpr"
NAME = "Jay @Westside Barbershop"
ADDR = "2800 N Mac Dill Ave, Tampa, FL 33607"
ADDR_MAPQ = "2800+N+Mac+Dill+Ave,+Tampa,+FL+33607"


def rep(a, b, n=1):
    global h
    assert a in h, "NO: " + a[:200]
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
    '<meta name="theme-color" content="#0a1018" />',
)
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    f'<title>{NAME} · Barbershop in Tampa, FL | 5.0 on Booksy</title>',
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    f'<meta name="description" content="{NAME}, Tampa FL: signature fades, haircuts, beard sculpting and kids cuts by Jadiel. Walk-ins welcome. 5.0 with 69 reviews on Booksy. Book online." />',
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    f'<meta property="og:title" content="{NAME} · Barbershop in Tampa, FL" />',
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Signature fades, haircuts and beard sculpting. 5.0 on Booksy. Book online." />',
)
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />', '<meta property="og:image" content="assets/raw/bk-7.jpg" />')
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-10.jpg" />',
)

# ---------- 3. JSON-LD ----------
m2 = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert m2, "no se encontro JSON-LD"
NEW_LD = f"""<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "{NAME}",
    "description": "Barbershop in Tampa, FL: signature fades, haircuts, beard sculpting and kids cuts by Jadiel. Walk-ins welcome.",
    "address": {{ "@type": "PostalAddress", "streetAddress": "2800 N Mac Dill Ave", "addressLocality": "Tampa", "addressRegion": "FL", "postalCode": "33607", "addressCountry": "US" }},
    "geo": {{ "@type": "GeoCoordinates", "latitude": 27.96596473348429, "longitude": -82.49372840285535 }},
    "sameAs": ["{BOOKSY}", "{IG_URL}"],
    "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "69", "bestRating": "5" }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "09:00", "closes": "17:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday"], "opens": "10:00", "closes": "19:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "19:00" }}
    ],
    "hasOfferCatalog": {{ "@type": "OfferCatalog", "name": "Barbershop services", "itemListElement": [
      {{ "@type": "Offer", "price": "54", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "VIP Barber Experience" }} }},
      {{ "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Signature Haircut & Beard" }} }},
      {{ "@type": "Offer", "price": "36", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Signature Haircut" }} }},
      {{ "@type": "Offer", "price": "27", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Beard Sculpt & Lineup" }} }},
      {{ "@type": "Offer", "price": "32", "priceCurrency": "USD", "itemOffered": {{ "@type": "Service", "name": "Kids Premium Cut" }} }}
    ] }}
  }}
  </script>"""
h = h[: m2.start()] + NEW_LD + h[m2.end():]

repall(BOOKSY_OLD, BOOKSY)
repall(IG_URL_OLD, IG_URL)
repall(IG_HANDLE_OLD, IG_HANDLE)

# ---------- 4. Preloader ----------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">JW</span>')
rep('<span class="pre-word">Pure Artistry</span>', f'<span class="pre-word">{NAME}</span>')

# ---------- 5. NAV ----------
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
    f'<img src="assets/raw/bk-10.jpg" alt="{NAME}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Jay <span class="text-[color:var(--accent-deep)]">Westside</span></span>',
)

# ---------- 6. HERO ----------
rep(
    'data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Tampa, FL · Barbershop" data-en="Tampa, FL · Barbershop">Tampa, FL · Barbershop</p>',
)
rep(
    'data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Cortes frescos, líneas nítidas, cuidado real." data-en="Fresh fades, sharp lines, real care.">Fresh fades, sharp lines, real care.</p>',
    n=2,
)
rep(
    '<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Fades de firma y" data-en="Signature fades and">Signature fades and</span><br /><span data-es="líneas nítidas, hechas " data-en="clean lineups, done ">clean lineups, done </span><span class="text-shine" data-es="bien siempre" data-en="right every time">right every time</span>',
)
rep(
    'data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    f'data-es="Fades de precisión, cortes de firma y arreglo de barba por Jadiel en West Tampa. Se aceptan walk-ins, con un 5.0 perfecto en 69 reseñas de Booksy." data-en="Precision fades, signature haircuts and beard sculpting by Jadiel in West Tampa. Walk-ins welcome, with a perfect 5.0 across 69 reviews on Booksy.">Precision fades, signature haircuts and beard sculpting by Jadiel in West Tampa. Walk-ins welcome, with a perfect 5.0 across 69 reviews on Booksy.</p>',
)
rep(
    'data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 69 reseñas en Booksy" data-en="5.0 · 69 reviews on Booksy">5.0 · 69 reviews on Booksy</span>',
)
rep(
    '<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    f'<img src="assets/raw/bk-7.jpg" alt="Finished two-tone blonde fade haircut at {NAME}" class="blur-up w-full h-full object-cover" />',
)
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg">VIP Barber Experience</p>')
rep(
    'data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="$54 · 1h" data-en="$54 · 1h">$54 · 1h</p>',
)

# ---------- 7. STRIP ----------
rep(
    '<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
    '<span data-count="69">69</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Fades <span class="text-shine">&amp;</span> Beards</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cortes · Barba · Diseño" data-en="Haircuts · Beard · Design">Haircuts · Beard · Design</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Walk-Ins <span class="text-shine">&amp;</span> Booksy</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Reserva o pasa directo" data-en="Book or walk right in">Book or walk right in</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Tampa, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">2800 N Mac Dill Ave</p></div>',
)

# ---------- 8. MARQUEE (2 secuencias, cada palabra aparece 4 veces) ----------
MQ = [
    ("Silk Press", "Signature Fades"),
    ("Loc Retwist", "Beard Sculpt"),
    ("Knotless Braids", "VIP Experience"),
    ("K-Tip Extensions", "Kids Cuts"),
    ("Keratin", "Walk-Ins Welcome"),
    ("Orlando, FL", "Tampa, FL"),
]
for old, new in MQ:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f"marquee count != 4 para {old}: {h.count(old_span)}"
    h = h.replace(old_span, new_span)

# ---------- 9. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    f'<img src="assets/raw/bk-9.jpg" alt="{NAME} interior with barber chairs, pool table and lounge area" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    f"<img src=\"assets/raw/bk-3.jpg\" alt=\"Barber trimming a client's hairline in a reclined chair at {NAME}\" class=\"blur-up w-full h-full object-cover\" loading=\"lazy\" />",
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un barbero," data-en="One barber,">One barber,</span><br /><span class="text-shine" data-es="siempre al detalle" data-en="always on point">always on point</span></h2>',
)
rep(
    'data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    f'data-es="{NAME} es la base de Jadiel en West Tampa. Fades de firma, líneas nítidas y arreglo de barba, todo de un barbero al que sus clientes describen como detallista y fácil de tratar." data-en="{NAME} is Jadiel\'s home base in West Tampa. Signature fades, clean lineups and beard sculpting, all from a barber his clients describe as detail oriented and easy to talk to.">{NAME} is Jadiel\'s home base in West Tampa. Signature fades, clean lineups and beard sculpting, all from a barber his clients describe as detail oriented and easy to talk to.</p>',
)
rep(
    'data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus clientes lo confirman: reseñas que lo describen como el mejor barbero del Westside. 5.0 perfecto en 69 reseñas verificadas de Booksy." data-en="His clients confirm it: reviews that call him the best barber on the Westside. A perfect 5.0 across 69 verified Booksy reviews.">His clients confirm it: reviews that call him the best barber on the Westside. A perfect 5.0 across 69 verified Booksy reviews.</p>',
)
rep(
    '<span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<span data-count="69">69</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
)
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/raw/bk-11.jpg" alt="Jadiel, barber" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Jadiel · <span class="text-[color:var(--ink-40)]" data-es="Barbero" data-en="Barber">Barber</span></span>',
)

# ---------- 10. EL METODO ----------
rep(
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: corte, barba o la VIP Experience completa, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: haircut, beard, or the full VIP Experience, and confirm instantly.">Pick your service on Booksy with clear price and duration: haircut, beard, or the full VIP Experience, and confirm instantly.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta rápida" data-en="Quick consult">Quick consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma de la cara, largo actual y el fade que buscas: de ahí sale la línea y el degradado exactos." data-en="Face shape, current length and the fade you want: that is where the exact line and taper come from.">Face shape, current length and the fade you want: that is where the exact line and taper come from.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del arreglo de barba de 30 minutos a la VIP Barber Experience de 1 hora: cada servicio recibe su tiempo completo, sin apuros." data-en="From the 30-minute beard sculpt to the 1-hour VIP Barber Experience: every service gets its full time, no rushing.">From the 30-minute beard sculpt to the 1-hour VIP Barber Experience: every service gets its full time, no rushing.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el fade limpio y la línea nítida, tal como cuentan sus reseñas de Booksy. Tu próxima cita queda agendada." data-en="You leave with a clean fade and a sharp lineup, just as his Booksy reviews describe. Next visit booked before you go.">You leave with a clean fade and a sharp lineup, just as his Booksy reviews describe. Next visit booked before you go.</p>',
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
          <h3 class="font-display text-2xl leading-snug mb-3">👑VIP BARBER EXPERIENCE</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El servicio completo de la casa: corte, diseño y arreglo de barba en una sola sesión extendida con Jadiel." data-en="The full house service: haircut, design and beard grooming in one extended session with Jadiel.">The full house service: haircut, design and beard grooming in one extended session with Jadiel.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$54</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito" data-en="Most booked">Most booked</p>
          <h3 class="font-display text-2xl leading-snug mb-3">💈Signature Haircut &amp; Beard</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte a tu medida más arreglo de barba, el combo que más reservan sus clientes." data-en="A custom haircut plus beard grooming, the combo his clients book most.">A custom haircut plus beard grooming, the combo his clients book most.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">55min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Clásico" data-en="Classic">Classic</p>
          <h3 class="font-display text-2xl leading-snug mb-3">🔥Signature Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El fade de firma de la casa con línea nítida, listo en menos de una hora." data-en="The house signature fade with a clean lineup, ready in under an hour.">The house signature fade with a clean lineup, ready in under an hour.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$36</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">45min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Barba" data-en="Beard">Beard</p>
          <h3 class="font-display text-2xl leading-snug mb-3">🪒 Beard Sculpt &amp; Lineup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Perfilado y arreglo de barba con navaja, para un acabado limpio." data-en="Beard shaping and lineup with a razor, for a clean finish.">Beard shaping and lineup with a razor, for a clean finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$27</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30min</p></div>
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
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: 👦 Kids Premium Cut desde $32 (40min). Menú completo y disponibilidad en Booksy." data-en="Also: 👦 Kids Premium Cut from $32 (40min). Full menu and availability on Booksy.">Also: 👦 Kids Premium Cut from $32 (40min). Full menu and availability on Booksy.</span></p>',
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

NEW_GAL_GRID = f"""<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Precisión en acción" data-en="Precision in progress">Precision in progress</span><img src="assets/raw/bk-1.jpg" alt="Barber cutting a client's hair under ring lights at {NAME}" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Línea de fade nítida" data-en="Sharp taper line">Sharp taper line</span><img src="assets/raw/bk-4.jpg" alt="Close-up of a fresh taper fade line at {NAME}" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Acabado engominado" data-en="Slick finish">Slick finish</span><img src="assets/raw/bk-5.jpg" alt="Slicked back finished haircut styled at {NAME}" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Fade limpio, barba perfilada" data-en="Clean fade, sharp beard">Clean fade, sharp beard</span><img src="assets/raw/bk-6.jpg" alt="Clean fade and beard finish, back view, at {NAME}" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Corte fresco, vista del local" data-en="Fresh cut, full shop view">Fresh cut, full shop view</span><img src="assets/raw/bk-8.jpg" alt="Side profile of a fresh taper fade with beard at {NAME}" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>"""
h = h[: OLD_GAL_GRID.start()] + NEW_GAL_GRID + h[OLD_GAL_GRID.end():]

# ---------- 13. OPINIONES ----------
rep(
    '<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 69 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 69 verified reviews on Booksy">5.0 out of 5 · 69 verified reviews on Booksy</span>',
)

OLD_REVIEWS = '<div class="grid sm:grid-cols-3 gap-5 items-stretch">\n        <figure class="glass glass-hover rounded-3xl p-8 reveal">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">\n          <p class="stars text-sm mb-4">★★★★★</p>\n          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>\n        </figure>\n      </div>'

NEW_REVIEWS = """<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Jadiel best barber in the WestSide Barbershop."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">John</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Good service and cut"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Alexander R…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Really good service, very detailed oriented. Also, really friendly had a great conversation. Will be back soon!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joshuan S…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>"""
rep(OLD_REVIEWS, NEW_REVIEWS)

rep(
    'data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    'data-es="Leer las 69 reseñas en Booksy" data-en="Read all 69 reviews on Booksy">Read all 69 reviews on Booksy</a>',
)

# ---------- 14. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Tampa, FL</span></h2>',
)
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', f'<p class="text-sm text-[color:var(--ink-60)] font-light">{ADDR}</p>')
rep(
    'href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    f'href="https://www.google.com/maps?q={ADDR_MAPQ}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
)
rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
    'data-es="Reserva por Booksy o pasa directo: eliges servicio, día y hora, y la confirmación es inmediata. Walk-ins bienvenidos según disponibilidad. Abierto domingo de 9:00 am a 5:00 pm, lunes a miércoles de 10:00 am a 7:00 pm, y jueves a sábado de 8:00 am a 7:00 pm." data-en="By appointment via Booksy or walk right in: pick the service, day and time, and the confirmation is instant. Walk-ins welcome based on availability. Open Sunday 9:00 am to 5:00 pm, Monday to Wednesday 10:00 am to 7:00 pm, and Thursday to Saturday 8:00 am to 7:00 pm.">By appointment via Booksy or walk right in: pick the service, day and time, and the confirmation is instant. Walk-ins welcome based on availability. Open Sunday 9:00 am to 5:00 pm, Monday to Wednesday 10:00 am to 7:00 pm, and Thursday to Saturday 8:00 am to 7:00 pm.</p>',
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
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo corte" data-en="Your next cut">Your next cut</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva online en segundos: tu fade, tu arreglo de barba o la VIP Barber Experience completa." data-en="Book online in seconds: your fade, your beard trim, or the full VIP Barber Experience.">Book online in seconds: your fade, your beard trim, or the full VIP Barber Experience.</p>',
)

# ---------- 16. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', f'<span class="foot-mark" aria-hidden="true">{NAME}</span>')
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    f'<img src="assets/raw/bk-10.jpg" alt="{NAME}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">{NAME}</span>',
)
rep(
    'data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Barbershop en Tampa, FL. Walk-ins bienvenidos, citas por Booksy." data-en="Barbershop in Tampa, FL. Walk-ins welcome, appointments via Booksy.">Barbershop in Tampa, FL. Walk-ins welcome, appointments via Booksy.</p>',
)
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', f'<p>{ADDR}</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {NAME}.</p>')

# ================================================================
# 17. Paleta: gold -> steel navy (accent-deep #3a5a78, accent-mid #6f93ad)
#     Proteger merktop-badge ya hecho en el paso 1 (placeholder @@BADGE@@)
# ================================================================
HEX_PAIRS = [
    ('#d4a84b', '#3a5a78'),
    ('#b8934a', '#6f93ad'),
    ('#f0dc9e', '#cfe2ee'),
    ('#9a7431', '#1f3547'),
    ('#e5c374', '#a9c8dd'),
    ('#e8c476', '#bcd8e8'),
    ('#c9a04a', '#4a7396'),
    ('#96742c', '#26445c'),
    ('#6b5222', '#17293a'),
    ('#1c1408', '#0b141c'),
    ('#e9c3ab', '#a9c8dd'),
    ('#8a744a', '#2c4a63'),
    ('#e8cf96', '#bcd8e8'),
    ('#f8eed3', '#eaf4fa'),
    ('#bfa060', '#6f93ad'),
    ('#f0dcae', '#cfe2ee'),
    ('#faf1dc', '#eaf4fa'),
    ('#ecd9a8', '#bcd8e8'),
    ('#c9ab6b', '#6f93ad'),
    ('#241c0e', '#16222c'),
]
for old, new in HEX_PAIRS:
    assert old in h, "paleta hex no encontrado: " + old
    h = h.replace(old, new)

RGB_PAIRS = [
    ('212,168,75', '58,90,120'),
    ('232,207,150', '188,216,232'),
    ('232,210,160', '207,226,238'),
    ('80,58,18', '23,41,58'),
    ('110,85,35', '44,74,99'),
    ('122,90,30', '31,53,71'),
    ('180,140,60', '74,115,150'),
    ('185,138,128', '122,147,173'),
    ('54,42,38', '28,38,48'),
]
for old, new in RGB_PAIRS:
    assert old in h, "paleta rgb no encontrado: " + old
    h = h.replace(old, new)

h = h.replace('@@BADGE@@', badge_block, 1)

open(PATH, "w").write(h)
print("BUILD OK: jaywestsidebarbershop")
