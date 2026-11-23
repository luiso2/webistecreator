import re

SLUG = "miafascia-northmiamibeach"
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


TEL = "tel:+17862381093"
PHONE_DISPLAY = "(786) 238-1093"
REVIEWS_URL = "https://www.google.com/search?q=MIAFASCIA+North+Miami+Beach+FL+reviews"
REVIEWS_LABEL = "Google Reviews"
ADDR = "3753 NE 163rd St, North Miami Beach, FL 33160"
MAPS = "https://www.google.com/maps?q=3753+NE+163rd+St,+North+Miami+Beach,+FL+33160"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: gold (Pure Artistry) -> crimson/garnet (red light therapy real: cuarto bañado
#    en luz roja, tape naranja/negra, moretones de ventosas). Brand vibe = recovery/clinical-red.
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#6b5222", "#5a1f24"),
    ("#d4a84b", "#c23b4a"),
    ("#e9c3ab", "#e3a6a0"),
    ("#8a744a", "#a65a52"),
    ("#f0dc9e", "#e8a3a8"),
    ("#e8cf96", "#eec3bd"),
    ("#e8c476", "#e7918f"),
    ("#e5c374", "#e4938a"),
    ("#c9a04a", "#b84a4f"),
    ("#9a7431", "#7a2e34"),
    ("#96742c", "#6e2630"),
    ("#0f0b07", "#110807"),
    ("#b8934a", "#9c4046"),
    ("#241c0e", "#241012"),
    ("#191307", "#1c0d0e"),
    ("#171207", "#1c0e0e"),
    ("#100c05", "#120909"),
    ("#0c0905", "#110a0a"),
    ("#bfa060", "#a85c5a"),
    ("#f0dcae", "#eec3bd"),
    ("#ecd9a8", "#c97270"),
    ("#c9ab6b", "#a85650"),
    ("#faf1dc", "#f3dcd9"),
    ("#f8eed3", "#f6e2df"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(194,59,74"),
    ("rgba(232,207,150", "rgba(238,195,189"),
    ("rgba(122,90,30", "rgba(140,45,40"),
    ("rgba(180,140,60", "rgba(190,80,70"),
    ("rgba(185,138,128", "rgba(190,90,85"),
    ("rgba(110,85,35", "rgba(100,40,40"),
    ("rgba(80,58,18", "rgba(74,28,30"),
    ("rgba(232,210,160", "rgba(238,195,189"),
    ("rgba(15,11,7", "rgba(17,8,7"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: sin booking platform, sin IG/FB, sin email -> tel: + Google reviews
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
c = h.count(OLD_BOOK)
assert c == 13, c
h = h.replace(OLD_BOOK, TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
c = h.count(OLD_IG_URL)
assert c == 6, c
h = h.replace(OLD_IG_URL, REVIEWS_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
c = h.count(OLD_IG_HANDLE)
assert c == 4, c
h = h.replace(OLD_IG_HANDLE, REVIEWS_LABEL)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>MIAFASCIA · Fascia &amp; Recovery Massage in North Miami Beach, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="MIAFASCIA, North Miami Beach FL: myofascial release, deep tissue massage, cupping and red light therapy. 5.0 stars across 30 Google reviews. Call to book a session." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="MIAFASCIA · Fascia &amp; Recovery Massage in North Miami Beach, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Myofascial release, deep tissue, cupping and red light therapy. 5.0 on Google with 30 reviews. Call to book." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-room.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/avatar-ivan.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "MIAFASCIA",
    "description": "Fascia and recovery massage studio in North Miami Beach, FL: myofascial release, deep tissue massage, cupping therapy and red light therapy with EMS.",
    "address": { "@type": "PostalAddress", "streetAddress": "3753 NE 163rd St", "addressLocality": "North Miami Beach", "addressRegion": "FL", "postalCode": "33160", "addressCountry": "US" },
    "telephone": "+1-786-238-1093",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "30", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Massage and recovery services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Myofascial Release" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Deep Tissue Massage" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Cupping Therapy" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Red Light Therapy & EMS Recovery" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: EN default (reseñas y presencia publica, todas en ingles; sin evidencia de
#    español en marca/redes). El esqueleto YA es EN-default (<html lang="en">,
#    applyLang(lang === 'es' ? 'es' : 'en')), asi que no hace falta tocar ese bloque.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,59,74,0.35)]" />',
    '<img src="assets/avatar-ivan.jpg" alt="MIAFASCIA" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,59,74,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">MIA<span class="text-[color:var(--accent-deep)]">FASCIA</span></span>')
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">MF</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">MIAFASCIA</span>')
print("NAV done")

rep('class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">\n          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n        </a>',
    'class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">\n          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n          <span data-es="Llamar ahora" data-en="Call now">Call now</span>\n        </a>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="North Miami Beach, FL · Estudio de Fascia" data-en="North Miami Beach, FL · Fascia Studio">North Miami Beach, FL · Fascia Studio</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Alivio real, no solo relajacion." data-en="Real relief, not just relaxation.">Real relief, not just relaxation.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Liberacion miofascial y" data-en="Myofascial release and">Myofascial release and</span><br /><span data-es="terapia de recuperacion, " data-en="recovery therapy, ">recovery therapy, </span><span class="text-shine" data-es="bien hecha" data-en="done right">done right</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Tejido profundo, liberacion miofascial, ventosas y terapia de luz roja enfocados en alivio real de dolor, movilidad y recuperacion. Un estudio privado en North Miami Beach con 5.0 perfecto en 30 reseñas de Google." data-en="Deep tissue, myofascial release, cupping and red light therapy focused on real pain relief, mobility and recovery. A private studio in North Miami Beach with a perfect 5.0 across 30 Google reviews.">Deep tissue, myofascial release, cupping and red light therapy focused on real pain relief, mobility and recovery. A private studio in North Miami Beach with a perfect 5.0 across 30 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 30 reseñas en Google" data-en="5.0 · 30 reviews on Google">5.0 · 30 reviews on Google</span>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + REVIEWS_LABEL + '''
          </a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llamar al (786) 238-1093" data-en="Call (786) 238-1093">Call (786) 238-1093</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + REVIEWS_LABEL + '''
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-room.jpg" alt="Treatment room at MIAFASCIA in North Miami Beach lit for red light therapy" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Abierto" data-en="Open">Open</p>
            <p class="font-display text-lg" data-es="Con cita previa" data-en="By appointment">By appointment</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Lun-Vie · 9am-5pm" data-en="Mon-Fri · 9am-5pm">Mon-Fri · 9am-5pm</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="30">30</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Myofascial <span class="text-shine">&amp;</span> Deep Tissue</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Ventosas · Luz roja · EMS" data-en="Cupping · Red light · EMS">Cupping · Red light · EMS</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">Pain <span class="text-shine">&amp;</span> Mobility</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Alivio comprobado" data-en="Proven relief">Proven relief</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">North Miami Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">3753 NE 163rd St</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Silk Press", "Myofascial Release"),
    ("Loc Retwist", "Deep Tissue"),
    ("Knotless Braids", "Cupping Therapy"),
    ("K-Tip Extensions", "Red Light Therapy"),
    ("Keratin", "Sports Massage"),
    ("Orlando, FL", "North Miami Beach, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (un solo About + avatar, igual que el patron de un solo terapeuta)
# ---------------------------------------------------------------------------
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="grid grid-cols-1 gap-5">
        <div class="frame zoomable aspect-[4/3] img-reveal">
          <img src="assets/about-device.jpg" alt="Red light therapy and EMS recovery equipment at MIAFASCIA" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Un terapeuta," data-en="One therapist,">One therapist,</span><br /><span class="text-shine" data-es="manos que conocen la fascia" data-en="hands that know fascia">hands that know fascia</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="MIAFASCIA es el estudio privado de Ivan en North Miami Beach, construido alrededor de la liberacion miofascial: tejido profundo, ventosas, terapia de luz roja y estimulacion muscular electrica combinadas sesion a sesion para tratar dolor cronico, lesiones deportivas y recuperacion." data-en="MIAFASCIA is Ivan\'s private studio in North Miami Beach, built around myofascial release: deep tissue, cupping, red light therapy and electrical muscle stimulation combined session by session to target chronic pain, sports injuries and recovery.">MIAFASCIA is Ivan\'s private studio in North Miami Beach, built around myofascial release: deep tissue, cupping, red light therapy and electrical muscle stimulation combined session by session to target chronic pain, sports injuries and recovery.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus reseñas lo confirman: los clientes describen alivio inmediato de ciatica y dolor lumbar, mas movilidad y un espacio tranquilo y profesional. 5.0 perfecto en 30 reseñas verificadas de Google." data-en="His reviews confirm it: clients describe immediate relief from sciatica and lower back pain, more mobility and a calm, professional space. A perfect 5.0 across 30 verified Google reviews.">His reviews confirm it: clients describe immediate relief from sciatica and lower back pain, more mobility and a calm, professional space. A perfect 5.0 across 30 verified Google reviews.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="30">30</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,59,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/avatar-ivan.jpg" alt="Ivan, massage therapist at MIAFASCIA" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,59,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Ivan · <span class="text-[color:var(--ink-40)]" data-es="Masajista" data-en="Massage Therapist">Massage Therapist</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu sesion, paso a paso" data-en="Your session, step by step">Your session, step by step</p>')
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="Asi se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Llamas y agendas" data-en="Call and book">Call and book</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llama al (786) 238-1093 y cuentale a Ivan que te molesta. Te consigue un horario que funcione, muchas veces esa misma semana." data-en="Call (786) 238-1093 and tell Ivan what is bothering you. He finds you a slot that works, often the same week.">Call (786) 238-1093 and tell Ivan what is bothering you. He finds you a slot that works, often the same week.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Evaluacion de movimiento" data-en="Movement assessment">Movement assessment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Ivan revisa postura, rango de movimiento y zonas problematicas antes de elegir la combinacion de tecnicas correcta para ese dia." data-en="Ivan checks posture, range of motion and problem areas before choosing the right combination of techniques for that day.">Ivan checks posture, range of motion and problem areas before choosing the right combination of techniques for that day.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="La sesion" data-en="The session">The session</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tejido profundo, liberacion miofascial, ventosas, luz roja o EMS, combinados segun tus puntos de dolor, en un cuarto privado y tranquilo." data-en="Deep tissue, myofascial release, cupping, red light therapy or EMS, blended to your pain points, in a calm private room.">Deep tissue, myofascial release, cupping, red light therapy or EMS, blended to your pain points, in a calm private room.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Sales moviendote mejor" data-en="You leave moving better">You leave moving better</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Menos tension, mas rango de movimiento, y recomendaciones para mantenerlo hasta tu proxima visita." data-en="Less tension, more range of motion, and guidance to keep it that way until your next visit.">Less tension, more range of motion, and guidance to keep it that way until your next visit.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Tratamiento," data-en="Treatment,">Treatment,</span> <span class="text-shine" data-es="hecho para ti" data-en="built around you">built around you</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Cada sesion se ajusta a tus puntos de dolor. Llama al (786) 238-1093 para cotizar y agendar." data-en="Every session is tailored to your pain points. Call (786) 238-1093 for pricing and to book.">Every session is tailored to your pain points. Call (786) 238-1093 for pricing and to book.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(194,59,74,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo mas pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Liberacion Miofascial" data-en="Myofascial Release">Myofascial Release</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La tecnica detras del nombre de MIAFASCIA: presion lenta y dirigida sobre fascia tensa para restaurar movilidad y aliviar tension cronica." data-en="The technique behind MIAFASCIA's name: slow, targeted pressure on tight fascia to restore mobility and relieve chronic tension.">The technique behind MIAFASCIA's name: slow, targeted pressure on tight fascia to restore mobility and relieve chronic tension.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Presion firme" data-en="Firm pressure">Firm pressure</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tejido Profundo" data-en="Deep Tissue Massage">Deep Tissue Massage</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Presion firme y dirigida sobre nudos y tension cronica, el masaje que mas mencionan las reseñas para dolor de espalda y hombros." data-en="Firm, focused pressure on knots and chronic tightness, the massage reviewers mention most for back and shoulder pain.">Firm, focused pressure on knots and chronic tightness, the massage reviewers mention most for back and shoulder pain.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Circulacion" data-en="Circulation">Circulation</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Terapia de Ventosas" data-en="Cupping Therapy">Cupping Therapy</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Ventosas colocadas en espalda y hombros para mejorar la circulacion y soltar la fascia antes o despues del trabajo profundo." data-en="Suction cups placed along the back and shoulders to boost circulation and loosen fascia before or after deep work.">Suction cups placed along the back and shoulders to boost circulation and loosen fascia before or after deep work.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Recuperacion" data-en="Recovery">Recovery</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Luz Roja y EMS" data-en="Red Light &amp; EMS Recovery">Red Light &amp; EMS Recovery</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Terapia de luz roja combinada con estimulacion muscular electrica, la combinacion que las reseñas destacan por el alivio rapido de ciatica y dolor lumbar." data-en="Red light therapy paired with electrical muscle stimulation, the combination reviewers credit with fast relief from sciatica and lower back pain.">Red light therapy paired with electrical muscle stimulation, the combination reviewers credit with fast relief from sciatica and lower back pain.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: masaje deportivo y sesiones de recuperacion para atletas. Llama o escribe al (786) 238-1093 por disponibilidad." data-en="Also: sports massage and recovery sessions for athletes. Call or text (786) 238-1093 for availability.">Also: sports massage and recovery sessions for athletes. Call or text (786) 238-1093 for availability.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (3 tiles reales: taping ancho + cupping + standing, curaduria estricta)
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="El" data-en="The">The</span> <span class="text-shine" data-es="estudio" data-en="studio">studio</span>')
rep('''<a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + REVIEWS_LABEL + '''
        </a>''',
    '''<a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + REVIEWS_LABEL + '''
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-1 lg:col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Vendaje y fascia" data-en="Fascia &amp; kinesio taping">Fascia &amp; kinesio taping</span><img src="assets/gallery-taping.jpg" alt="Kinesio taping treatment at MIAFASCIA studio in North Miami Beach" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Terapia de ventosas" data-en="Cupping therapy">Cupping therapy</span><img src="assets/gallery-cupping.jpg" alt="Cupping therapy session on a client's back at MIAFASCIA" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Recuperacion real, resultados visibles" data-en="Real recovery, visible results">Real recovery, visible results</span><img src="assets/gallery-standing.jpg" alt="Client after a cupping therapy session at MIAFASCIA, North Miami Beach" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES (verbatim reales de Google, truncadas tal cual las trunca Google con "…")
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="sus clientes" data-en="clients say">clients say</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 30 reseñas verificadas en Google" data-en="5.0 out of 5 · 30 verified reviews on Google">5.0 out of 5 · 30 verified reviews on Google</span>')
rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal">
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
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I'm so happy I found Ivan! He is truly gifted at what he does and has a natural ability to understand what the body needs. He's more than just a massage therapist; he's a true healer. You can tell he genuinely cares about his clients and is &hellip;"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Melanie Rosemberg</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Ivan has helped me on multiple occasions. His knowledge and ability to identify and treat problem areas are outstanding. Whether you're dealing with chronic pain, a sports-related issue, or just need recovery work, he takes the time to &hellip;"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Avi Bash</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I have been suffering from massive lower back ache and sciatica for many weeks. I Felt results immediately after Ivan's deep tissue massage, red light therapy and electrical muscle stimulation. His equipment is top-of-the-line, much better &hellip;"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">shaya770</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 30 reseñas en Google" data-en="Read all 30 reviews on Google">Read all 30 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visitanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">North Miami Beach</span></h2>')
rep('''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,74,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''<p class="font-medium mb-1" data-es="Direccion" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,74,0.4)]" href="''' + MAPS + '''" target="_blank" rel="noopener" data-es="Como llegar" data-en="Get directions">Get directions</a>''')
rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,74,0.4)]" href="''' + TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a viernes, de 9am a 5pm. Cerrado sabado y domingo." data-en="Monday through Friday, 9am to 5pm. Closed Saturday and Sunday.">Monday through Friday, 9am to 5pm. Closed Saturday and Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,74,0.4)]" href="''' + TEL + '''" data-es="Llamar al (786) 238-1093" data-en="Call (786) 238-1093">Call (786) 238-1093</a>''')
rep('''<p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,74,0.4)]" href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener">''' + REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"
          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<p class="font-medium mb-1" data-es="Reseñas" data-en="Reviews">Reviews</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="5.0 estrellas en 30 reseñas verificadas de Google." data-en="5.0 stars across 30 verified Google reviews.">5.0 stars across 30 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,59,74,0.4)]" href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener">''' + REVIEWS_LABEL + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: MIAFASCIA, 3753 NE 163rd St, North Miami Beach FL"
          src="''' + MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Alivio real, no solo relajacion." data-en="Real relief, not just relaxation.">Real relief, not just relaxation.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Una llamada" data-en="One call">One call</span> <span class="text-shine" data-es="te puede aliviar" data-en="could ease it all">could ease it all</span></h2>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Llama al (786) 238-1093 y cuentale a Ivan que te molesta. Te va a conseguir un horario que funcione, muchas veces esa misma semana." data-en="Call (786) 238-1093 and tell Ivan what is bothering you. He will find you a slot that works, often the same week.">Call (786) 238-1093 and tell Ivan what is bothering you. He will find you a slot that works, often the same week.</p>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (786) 238-1093" data-en="Call (786) 238-1093">Call (786) 238-1093</a>
        <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Leer reseñas en Google" data-en="Read Google reviews">Read Google reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">MIAFASCIA</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(238,195,189,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/avatar-ivan.jpg" alt="MIAFASCIA" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(238,195,189,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase" data-es="MIAFASCIA" data-en="MIAFASCIA">MIAFASCIA</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Estudio de masaje de fascia y recuperacion en North Miami Beach, FL. Atencion con cita previa." data-en="Fascia and recovery massage studio in North Miami Beach, FL. By appointment only.">Fascia and recovery massage studio in North Miami Beach, FL. By appointment only.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + TEL + '''" target="_blank" rel="noopener" class="hover:text-[#e3a6a0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>''' + ADDR + '''</p>
        <p><a href="''' + TEL + '''" class="hover:text-[#e3a6a0]" data-es="Llamar al (786) 238-1093" data-en="Call (786) 238-1093">Call (786) 238-1093</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e3a6a0]">Instagram · ''' + REVIEWS_LABEL + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reseñas" data-en="Reviews">Reviews</p>
        <p><a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#e3a6a0]">5.0 · ''' + REVIEWS_LABEL + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 MIAFASCIA.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + TEL + '" class="book-float" aria-label="Call MIAFASCIA">')
rep('<span class="book-float-label" data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span class="book-float-label" data-es="Llamar ahora" data-en="Call now">Call now</span>')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 19. Limpieza: tel: links no necesitan target=_blank/rel=noopener
# ---------------------------------------------------------------------------
h = h.replace(f'href="{TEL}" target="_blank" rel="noopener"', f'href="{TEL}"')
print("CLEANUP tel links done")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("FINAL WRITE done ->", PATH)
