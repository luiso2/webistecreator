import re
import colorsys
import json

h = open('output/salondiane/index.html').read()


def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)


# ---------- 3. Globales: Booksy URL, quitar Instagram ----------
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
NEW_BOOKSY = 'https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami'
assert h.count(OLD_BOOKSY) == 13
h = h.replace(OLD_BOOKSY, NEW_BOOKSY)

# ---------- 4. HEAD ----------
# (theme-color hex ya fue rotado por el paso de paleta global, arriba)
rep(
    '<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Salon Diane · Hair Salon en West Miami, FL | Silk Press, Color y Cirujia Capilar | 5.0 en Booksy</title>'
)
rep(
    '<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Salon Diane, West Miami FL: silk press, color completo, toner, keratina y cirujia capilar. 5.0 con 49 resenas en Booksy. Reserva en linea." />'
)
rep(
    '<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Salon Diane · Hair Salon en West Miami, FL" />'
)
rep(
    '<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Silk press, color, toner y cirujia capilar. 5.0 en Booksy. Reserva en linea." />'
)
rep(
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />'
)
rep(
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/bk-6.jpg" />'
)

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert old_jsonld
new_jsonld_obj = {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Salon Diane",
    "description": "Salon de belleza en West Miami, FL: silk press, color completo, toner, keratina y tratamiento de cirujia capilar.",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "1076 SW 67th Ave, Suite 100",
        "addressLocality": "Miami",
        "addressRegion": "FL",
        "postalCode": "33144",
        "addressCountry": "US"
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 25.76007849, "longitude": -80.30501302},
    "sameAs": ["https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami"],
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "49", "bestRating": "5"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:30"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "16:00"}
    ],
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Servicios de cabello", "itemListElement": [
        {"@type": "Offer", "price": "180", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "Silk press"}},
        {"@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "All over color"}},
        {"@type": "Offer", "price": "68", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "Cirujia Capilar"}},
        {"@type": "Offer", "price": "50", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "Haircut"}}
    ]}
}
new_jsonld = '<script type="application/ld+json">\n  ' + json.dumps(new_jsonld_obj, ensure_ascii=False, indent=2) + '\n  </script>'
h = h[:old_jsonld.start()] + new_jsonld + h[old_jsonld.end():]

# ---------- 5. Idioma: ya default 'es' en <html lang> y applyLang; el esqueleto viene en 'en' ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------- 5b. PRELOADER ----------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">SD</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Salon Diane</span>')

# ---------- 6. NAV ----------
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
    '<img src="assets/raw/bk-6.jpg" alt="Salon Diane" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />'
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Salon <span class="text-[color:var(--accent-deep)]">Diane</span></span>'
)

# ---------- 7. HERO ----------
rep(
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    '<p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="West Miami, FL · Salon de Belleza" data-en="West Miami, FL · Hair Salon">West Miami, FL · Salon de Belleza</p>'
)
rep(
    '<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Silk press, color y" data-en="Silk press, color and">Silk press, color and</span><br /><span data-es="tratamientos con " data-en="treatments with ">treatments with </span><span class="text-shine" data-es="resultados reales" data-en="real results">real results</span>'
)
rep(
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    '<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Silk press que dura semanas, color a la medida y tratamientos de recuperacion capilar en West Miami. Un salon de confianza con calificacion perfecta de 5.0 en 49 reseñas de Booksy." data-en="Silk presses that last for weeks, custom color and hair-repair treatments in West Miami. A trusted salon with a perfect 5.0 rating across 49 Booksy reviews.">Silk presses that last for weeks, custom color and hair-repair treatments in West Miami. A trusted salon with a perfect 5.0 rating across 49 Booksy reviews.</p>'
)
rep(
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    '<span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 49 reseñas en Booksy" data-en="5.0 · 49 reviews on Booksy">5.0 · 49 reviews on Booksy</span>'
)
rep(
    '''<a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @pure.artistrysk
          </a>''',
    '''<a href="#servicios" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
            <span data-es="Ver servicios" data-en="See services">Ver servicios</span>
          </a>'''
)
rep(
    '<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-6.jpg" alt="Cabello rubio liso y brillante recien peinado en Salon Diane" class="blur-up w-full h-full object-cover" />'
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    '<p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $180 · 3h 30min" data-en="From $180 · 3h 30min">From $180 · 3h 30min</p>'
)

# ---------- 8. STRIP DE CONFIANZA ----------
rep(
    '<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
    '<span data-count="49">49</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>'
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Color <span class="text-shine">&amp;</span> Toner</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Balayage · Keratina" data-en="Balayage · Keratin">Balayage · Keratin</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Silk <span class="text-shine">&amp;</span> Press</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Liso que dura semanas" data-en="Sleek finish that lasts weeks">Sleek finish that lasts weeks</p></div>'
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1076 SW 67th Ave</p></div>'
)

# ---------- 9. MARQUEE (x4 cada palabra) ----------
marquee_pairs = [
    ('Loc Retwist', 'Color a la Medida'),
    ('Knotless Braids', 'Cirujia Capilar'),
    ('K-Tip Extensions', 'Toner &amp; Keratina'),
    ('Keratin', 'Deep Conditioning'),
    ('Orlando, FL', 'West Miami, FL'),
]
for old_w, new_w in marquee_pairs:
    old_span = '<span class="marquee-word">' + old_w + '</span>'
    new_span = '<span class="marquee-word">' + new_w + '</span>'
    assert h.count(old_span) == 4, f'{old_w}: {h.count(old_span)}'
    h = h.replace(old_span, new_span)

# ---------- 10. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Cabello castaño con ondas trabajado en Salon Diane" class="blur-up w-full h-full object-cover" loading="lazy" />'
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Cabello liso oscuro con brillo, trabajo terminado en Salon Diane" class="blur-up w-full h-full object-cover" loading="lazy" />'
)
rep(
    '<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="de toda confianza" data-en="you can trust">you can trust</span>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Salon Diane es el salon de barrio de West Miami donde Dianeli atiende cita por cita: silk press, color a la medida y tratamientos de recuperacion capilar como la cirujia capilar. Trabajo detallado y sin prisas en el 1076 SW 67th Ave." data-en="Salon Diane is the neighborhood salon in West Miami where Dianeli works one appointment at a time: silk press, custom color and hair-repair treatments like the cirujia capilar. Careful, unhurried work at 1076 SW 67th Ave.">Salon Diane is the neighborhood salon in West Miami where Dianeli works one appointment at a time: silk press, custom color and hair-repair treatments like the cirujia capilar. Careful, unhurried work at 1076 SW 67th Ave.</p>'
)
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas lo confirman con una calificacion perfecta de 5.0 en 49 reseñas verificadas de Booksy, en español y en ingles." data-en="Her clients confirm it with a perfect 5.0 rating across 49 verified Booksy reviews, in Spanish and English.">Her clients confirm it with a perfect 5.0 rating across 49 verified Booksy reviews, in Spanish and English.</p>'
)
rep(
    '<span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<span data-count="49">49</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>'
)
rep(
    '''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>''',
    '''<img src="assets/raw/bk-1.jpg" alt="Dianeli, estilista de Salon Diane" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Salon Diane · <span class="text-[color:var(--ink-40)]" data-es="Estilista" data-en="Stylist">Stylist</span></span>'''
)

# ---------- 11. EL METODO ----------
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, color, toner o cirujia capilar, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, color, toner or cirujia capilar, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, color, toner or cirujia capilar, and confirm instantly.</p>'
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 3h 30min al toner de 30 minutos: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 3h 30min silk press to the 30-minute toner: every service gets its full time, no double booking, no rushing.">From the 3h 30min silk press to the 30-minute toner: every service gets its full time, no double booking, no rushing.</p>'
)

rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Salon Diane en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Salon Diane on Booksy. Booking confirms instantly.">Prices and durations as published by Salon Diane on Booksy. Booking confirms instantly.</p>'
)

# ---------- 12. SERVICIOS: grid de 4 cards ----------
old_services_grid = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Silk Press</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El silk press que las reseñas describen aguantando DOS semanas en el calor de Orlando. Desde $90, 2 horas dedicadas." data-en="The silk press her reviews describe lasting a full TWO weeks in the Orlando heat. From $90, a dedicated 2 hours.">The silk press her reviews describe lasting a full TWO weeks in the Orlando heat. From $90, a dedicated 2 hours.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3">Locs</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Retwist &amp; Interlock" data-en="Retwist &amp; Interlock">Retwist &amp; Interlock</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full-head loc retwist desde $100 (1h 30min), interlock desde $135 (2h) y extensiones de locs custom desde $450." data-en="Full-head loc retwist from $100 (1h 30min), interlock from $135 (2h) and custom loc extensions from $450.">Full-head loc retwist from $100 (1h 30min), interlock from $135 (2h) and custom loc extensions from $450.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min+</p></div>
            <a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Trenzas" data-en="Braids">Braids</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Knotless &amp; Box</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Small knotless braids desde $400 (7h) y medium box braids desde $300 (6h 30min): protectoras, limpias y sin tensión." data-en="Small knotless braids from $400 (7h) and medium box braids from $300 (6h 30min): protective, clean and tension-free.">Small knotless braids from $400 (7h) and medium box braids from $300 (6h 30min): protective, clean and tension-free.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$300+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">6h 30min+</p></div>
            <a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extensiones" data-en="Extensions">Extensions</p>
          <h3 class="font-display text-2xl leading-snug mb-3">K-Tips &amp; MicroLinks</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La especialidad de la casa: K-Tip extensions desde $750 (8h) y microlinks desde $250. También keratina desde $225 y updos desde $125." data-en="The house specialty: K-Tip extensions from $750 (8h) and microlinks from $250. Plus keratin from $225 and updos from $125.">The house specialty: K-Tip extensions from $750 (8h) and microlinks from $250. Plus keratin from $225 and updos from $125.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$250+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min+</p></div>
            <a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>'''

new_services_grid = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">Firma de la casa</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Silk Press</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El silk press insignia de Salon Diane: liso que dura semanas, hecho a mano por Dianeli en West Miami. Desde $180, 3 horas y media dedicadas." data-en="Salon Diane's signature silk press: a sleek finish that lasts for weeks, done by hand by Dianeli in West Miami. From $180, a dedicated 3.5 hours.">Salon Diane's signature silk press: a sleek finish that lasts for weeks, done by hand by Dianeli in West Miami. From $180, a dedicated 3.5 hours.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$180+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h 30min</p></div>
            <a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Color" data-en="Color">Color</p>
          <h3 class="font-display text-2xl leading-snug mb-3">All Over Color</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Color completo de raiz a puntas, aplicado y procesado con cuidado por Dianeli. Desde $90, 2 horas de servicio." data-en="Full root-to-tip color, applied and processed with care by Dianeli. From $90, a 2-hour service.">Full root-to-tip color, applied and processed with care by Dianeli. From $90, a 2-hour service.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tratamiento" data-en="Treatment">Tratamiento</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Cirujia Capilar</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El tratamiento de recuperacion capilar de la casa: nutre e hidrata el cabello dañado en una sesion de una hora. Desde $68." data-en="The house's deep hair-repair treatment: nourishes and hydrates damaged hair in a one-hour session. From $68.">The house's deep hair-repair treatment: nourishes and hydrates damaged hair in a one-hour session. From $68.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$68</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Corte" data-en="Cut">Corte</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte de cabello con Dianeli; el 'Female haircut' tiene el mismo precio. Desde $50." data-en="Haircut with Dianeli; the 'Female haircut' is the same price. From $50.">Haircut with Dianeli; the 'Female haircut' is the same price. From $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p></div>
            <a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>'''

assert old_services_grid in h
h = h.replace(old_services_grid, new_services_grid, 1)

# ---------- 13. Nota de servicios -> bloque de menu completo (sin acordeon) ----------
old_note = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>'
new_menu_block = '''<div class="reveal glass rounded-3xl p-7 sm:p-9 mt-10" style="transition-delay:60ms">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Menú completo" data-en="Full menu">Menú completo</p>
        <div class="grid sm:grid-cols-2 gap-x-10 gap-y-3 text-sm">
          <div class="flex items-baseline justify-between gap-4 border-b border-[color:var(--accent-ghost)] pb-2"><span class="text-[color:var(--ink-60)] font-light">Hair wash</span><span class="font-medium">$23</span></div>
          <div class="flex items-baseline justify-between gap-4 border-b border-[color:var(--accent-ghost)] pb-2"><span class="text-[color:var(--ink-60)] font-light">Female haircut</span><span class="font-medium">$50</span></div>
          <div class="flex items-baseline justify-between gap-4 border-b border-[color:var(--accent-ghost)] pb-2"><span class="text-[color:var(--ink-60)] font-light">Bang trim <span class="text-[color:var(--ink-40)]">· 15min</span></span><span class="font-medium">$14</span></div>
          <div class="flex items-baseline justify-between gap-4 border-b border-[color:var(--accent-ghost)] pb-2"><span class="text-[color:var(--ink-60)] font-light">Hair toner</span><span class="font-medium">$41</span></div>
          <div class="flex items-baseline justify-between gap-4 border-b border-[color:var(--accent-ghost)] pb-2"><span class="text-[color:var(--ink-60)] font-light">Toner <span class="text-[color:var(--ink-40)]">· 30min</span></span><span class="font-medium">$32</span></div>
          <div class="flex items-baseline justify-between gap-4 border-b border-[color:var(--accent-ghost)] pb-2"><span class="text-[color:var(--ink-60)] font-light" data-es="Deep conditioning treatment" data-en="Deep conditioning treatment">Deep conditioning treatment <span class="text-[color:var(--ink-40)]">· 30min</span></span><span class="font-medium">$32</span></div>
        </div>
        <p class="text-xs text-[color:var(--ink-40)] font-light mt-6" data-es="Precios y duraciones publicados por Salon Diane en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Salon Diane on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Salon Diane en Booksy. Reserva con confirmación inmediata.</p>
      </div>'''
rep(old_note, new_menu_block)

# ---------- 14. GALERIA ----------
rep(
    '<div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Twists definidos" data-en="Defined twists">Defined twists</span><img src="assets/raw/bk-13.jpg" alt="Twists largos y definidos hechos en Pure Artistry" class="blur-up w-full h-full object-cover" /></div>',
    '<div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Color con brillo" data-en="Color, glass shine">Color, glass shine</span><img src="assets/raw/bk-3.jpg" alt="Corte con color terminado, vista trasera dentro del salon con espejo y productos visibles" class="blur-up w-full h-full object-cover" /></div>'
)
rep(
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Ondas plateadas" data-en="Silver waves">Silver waves</span><img src="assets/raw/bk-12.jpg" alt="Cabello con ondas y reflejos plateados" class="blur-up w-full h-full object-cover" /></div>',
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Ondas rubias" data-en="Blonde waves">Blonde waves</span><img src="assets/raw/bk-2.jpg" alt="Ondas rubias largas y definidas, vista trasera en el salon" class="blur-up w-full h-full object-cover" /></div>'
)
rep(
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cornrows con diseño" data-en="Design cornrows">Design cornrows</span><img src="assets/raw/bk-7.jpg" alt="Cornrows con diseño geometrico" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Morena con ondas" data-en="Wavy brunette">Wavy brunette</span><img src="assets/raw/bk-4.jpg" alt="Cabello castaño oscuro con ondas sueltas, vista trasera" class="blur-up w-full h-full object-cover" loading="lazy" /></div>'
)
rep(
    '<div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Silk press con capas" data-en="Layered silk press">Layered silk press</span><img src="assets/raw/bk-3.jpg" alt="Silk press con capas y movimiento" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
    '<div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Balayage cálido" data-en="Warm balayage">Warm balayage</span><img src="assets/raw/bk-5.jpg" alt="Balayage con reflejos calidos sobre cabello castaño, vista trasera" class="blur-up w-full h-full object-cover" loading="lazy" /></div>'
)
rep(
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Locs con color" data-en="Colored locs">Colored locs</span><img src="assets/raw/bk-10.jpg" alt="Locs con puntas de color" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
    '<div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Liso rubio" data-en="Sleek blonde">Sleek blonde</span><img src="assets/raw/bk-6.jpg" alt="Cabello rubio liso y brillante, vista trasera en silla del salon" class="blur-up w-full h-full object-cover" loading="lazy" /></div>'
)
rep(
    '<div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Rizos grises" data-en="Silver curls">Silver curls</span><img src="assets/raw/bk-5.jpg" alt="Rizos definidos en tono gris plata" class="blur-up w-full h-full object-cover" loading="lazy" /></div>',
    '<div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Liso negro" data-en="Sleek black">Sleek black</span><img src="assets/raw/bk-7.jpg" alt="Cabello negro liso y brillante, vista trasera junto al espejo" class="blur-up w-full h-full object-cover" loading="lazy" /></div>'
)

rep(
    '''<a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @pure.artistrysk
        </a>''',
    '''<a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
        </a>'''
)

# ---------- 15. OPINIONES ----------
rep(
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 49 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 49 verified reviews on Booksy">5.0 out of 5 · 49 verified reviews on Booksy</span></p>'
)
old_reviews = '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>'''
new_reviews = '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I had a amazing service!! My hair came out amazing, definitely coming back again!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Dayana L…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Agradecido y muy satisfecho con el trabajo hecho a mi novia.. la dejo más bella aún..la chica muy profesional 100% recomendada"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Javier G…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Super buena atención y excelente trabajo mi esposa quedó pa novela preciosa muy agradecido 🙏🏻🙏🏻🙏🏻"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Mario H…</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>'''
rep(old_reviews, new_reviews)
rep(
    '<a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 49 reseñas en Booksy" data-en="Read all 49 reviews on Booksy">Leer las 49 reseñas en Booksy</a>'
)

# ---------- 16. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">West Miami</span></h2>'
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1076 SW 67th Ave, Suite 100, Miami, FL 33144</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.google.com/maps?q=1076+SW+67th+Ave,+Miami,+FL+33144" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>'
)
old_ig_block = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener">@pure.artistrysk</a>
            </div>
          </div>'''
new_hours_block = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Horario</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a viernes de 9:00 am a 5:30 pm. Sábados de 9:00 am a 4:00 pm." data-en="Monday to Friday, 9:00 am to 5:30 pm. Saturdays, 9:00 am to 4:00 pm.">Monday to Friday, 9:00 am to 5:30 pm. Saturdays, 9:00 am to 4:00 pm.</p>
            </div>
          </div>'''
rep(old_ig_block, new_hours_block)
rep(
    '<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Mapa: Salon Diane, 1076 SW 67th Ave, Miami FL"\n          src="https://www.google.com/maps?q=1076+SW+67th+Ave,+Miami,+FL+33144&output=embed"'
)

# ---------- 17. CTA FINAL ----------
rep(
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu color o esa cirujia capilar que llevas planeando." data-en="Book online in seconds: your silk press, your color, or that cirujia capilar you have been planning.">Book online in seconds: your silk press, your color, or that cirujia capilar you have been planning.</p>'
)
rep(
    '''<a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="https://booksy.com/en-us/1779012_salon-diane_hair-salon_15889_miami" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>'''
)

# ---------- 18. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Salon Diane</span>')
rep(
    '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<img src="assets/raw/bk-6.jpg" alt="Salon Diane" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Salon Diane</span>'
)
rep(
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Salón de belleza en West Miami, FL. Atención con cita previa." data-en="Hair salon in West Miami, FL. By appointment only.">Hair salon in West Miami, FL. By appointment only.</p>'
)
rep(
    '<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p>1076 SW 67th Ave, Suite 100, Miami, FL 33144</p>'
)
old_footer_ig_col = '''<div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · @pure.artistrysk</a></p>
      </div>'''
new_footer_hours_col = '''<div class="text-sm font-light text-[color:var(--ink-60)] space-y-2">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Horario" data-en="Hours">Horario</p>
        <p data-es="Lun - Vie: 9:00 am - 5:30 pm" data-en="Mon - Fri: 9:00 am - 5:30 pm">Lun - Vie: 9:00 am - 5:30 pm</p>
        <p data-es="Sáb: 9:00 am - 4:00 pm" data-en="Sat: 9:00 am - 4:00 pm">Sáb: 9:00 am - 4:00 pm</p>
      </div>'''
rep(old_footer_ig_col, new_footer_hours_col)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Salon Diane.</p>')

# ---------- 19. Verificacion final de restos (contenido, previo a la paleta) ----------
for leftover in ['Pure Artistry', 'pure.artistrysk', 'Orlando', '121705', 'K-Tip', 'Knotless', 'Locs', 'Loc Retwist',
                  'hair studio', '80 W Grant St', 'Instagram', 'instagram.com']:
    assert leftover not in h, 'LEFTOVER: ' + leftover

# ---------- 20. Proteger el badge Merktop ----------
m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m
badge_block = m.group(0)
h = h.replace(badge_block, '@@BADGE@@', 1)

# ---------- 21. Paleta: rotacion de matiz uniforme (misma tecnica que build_nailsbyyaima.py) ----------
# dark-v2 base = gold amber (~hue 40). HUE_SHIFT 250 -> ~hue 290: plum/magenta-bronze.
# Distinto del original y de los hermanos en construccion paralela (nails 42, brows 135, spa 310, barbershop dark 170).
HUE_SHIFT = 250.0


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
    return '#' + shift_hex(mo.group(1))


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

open('output/salondiane/index.html', 'w').write(h)
print('build OK')
