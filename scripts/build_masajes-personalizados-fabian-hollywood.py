import re

SLUG = "masajes-personalizados-fabian-hollywood"
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


TEL = "tel:+19542003387"
PHONE_DISPLAY = "(954) 200-3387"
REVIEWS_URL = "https://www.google.com/search?q=Masajes+Personalizados+By+Fabian+Hollywood+FL+reviews"
REVIEWS_LABEL_ES = "Resenas de Google"
REVIEWS_LABEL_EN = "Google Reviews"
ADDR = "2750 N 29th Ave #313, Hollywood, FL 33020"
MAPS = "https://www.google.com/maps?q=2750+N+29th+Ave+%23313,+Hollywood,+FL+33020"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: gold (Pure Artistry) -> sage green (zen studio real: paredes verdes + salt lamp)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#d4a84b", "#5f8057"),
    ("#b8934a", "#8aa67a"),
    ("#f0dc9e", "#d9e6ce"),
    ("#9a7431", "#3f5a39"),
    ("#e5c374", "#b9cf9e"),
    ("#241c0e", "#16201a"),
    ("#0f0b07", "#0c100d"),
    ("#171207", "#141a15"),
    ("#e8c476", "#9fc08c"),
    ("#c9a04a", "#6f9a5e"),
    ("#96742c", "#3f5a39"),
    ("#6b5222", "#35492f"),
    ("#1c1408", "#12170f"),
    ("#e8cf96", "#b9cf9e"),
    ("#f8eed3", "#eaf2e2"),
    ("#bfa060", "#7a9a68"),
    ("#f0dcae", "#cfe0bd"),
    ("#faf1dc", "#e4edd9"),
    ("#ecd9a8", "#c3d9b3"),
    ("#c9ab6b", "#8fae7c"),
    ("#8a744a", "#5c7850"),
    ("#e9c3ab", "#b9cf9e"),
    ("#191307", "#11160f"),
    ("#100c05", "#0b0f0b"),
    ("#0c0905", "#0a0f0a"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(138,166,122"),
    ("rgba(232,207,150", "rgba(185,207,158"),
    ("rgba(122,90,30", "rgba(74,107,63"),
    ("rgba(180,140,60", "rgba(138,166,122"),
    ("rgba(185,138,128", "rgba(122,150,110"),
    ("rgba(110,85,35", "rgba(70,95,60"),
    ("rgba(80,58,18", "rgba(50,70,42"),
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
assert c >= 10, c
h = h.replace(OLD_BOOK, TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, REVIEWS_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, REVIEWS_LABEL_EN)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Masajes Personalizados By Fabian · Massage Therapist in Hollywood, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Masajes Personalizados By Fabian, Hollywood FL: therapeutic, deep tissue and Thai massage. 5.0 stars across 15 Google reviews. Call to book a personalized session." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Masajes Personalizados By Fabian · Massage Therapist in Hollywood, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Therapeutic, deep tissue and Thai massage. 5.0 on Google with 15 reviews. Call to book." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-room.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/avatar-fabian.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "Masajes Personalizados By Fabian",
    "description": "Personalized massage therapy studio in Hollywood, FL: therapeutic, deep tissue and Thai massage focused on back, shoulder and sciatic pain relief.",
    "address": { "@type": "PostalAddress", "streetAddress": "2750 N 29th Ave #313", "addressLocality": "Hollywood", "addressRegion": "FL", "postalCode": "33020", "addressCountry": "US" },
    "telephone": "+1-954-200-3387",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "15", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"], "opens": "09:00", "closes": "23:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday"], "opens": "00:00", "closes": "23:59" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "10:00", "closes": "23:59" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Massage services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Therapeutic Massage" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Deep Tissue Massage" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Thai Massage" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Personalized Session" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: ES default (branding propio del negocio es en espanol)
# ---------------------------------------------------------------------------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'es' ? 'en' : 'es');")
print("IDIOMA done")

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(138,166,122,0.35)]" />',
    '<img src="assets/avatar-fabian.jpg" alt="Masajes Personalizados By Fabian" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(138,166,122,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Fabian <span class="text-[color:var(--accent-deep)]">Masajes</span></span>')
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">MF</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Fabian Masajes</span>')
print("NAV done")

rep('class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">\n          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>\n        </a>',
    'class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">\n          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>\n          <span data-es="Llamar ahora" data-en="Call now">Llamar ahora</span>\n        </a>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Llamar ahora</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Hollywood, FL · Masajes Personalizados" data-en="Hollywood, FL · Personalized Massage">Hollywood, FL · Personalized Massage</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Manos que sanan de verdad." data-en="Hands that truly heal.">Hands that truly heal.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Masaje personalizado" data-en="Personalized massage">Personalized massage</span><br /><span data-es="para aliviar el dolor " data-en="to relieve pain, ">to relieve pain, </span><span class="text-shine" data-es="de verdad" data-en="for real">for real</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Masaje terapeutico, de tejido profundo y Thai, enfocado en aliviar dolor de espalda, hombros y ciatica. Fabian atiende sesiones personalizadas en su propio estudio en Hollywood, con 5.0 perfecto en 15 reseñas de Google." data-en="Therapeutic, deep tissue and Thai massage, focused on relieving back, shoulder and sciatic pain. Fabian runs personalized sessions out of his own studio in Hollywood, with a perfect 5.0 across 15 Google reviews.">Therapeutic, deep tissue and Thai massage, focused on relieving back, shoulder and sciatic pain. Fabian runs personalized sessions out of his own studio in Hollywood, with a perfect 5.0 across 15 Google reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    f'data-es="5.0 · 15 reseñas en Google" data-en="5.0 · 15 reviews on Google">5.0 · 15 reviews on Google</span>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + REVIEWS_LABEL_EN + '''
          </a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llamar al (954) 200-3387" data-en="Call (954) 200-3387">Call (954) 200-3387</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + REVIEWS_LABEL_EN + '''
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-room.jpg" alt="Sala de masajes de Masajes Personalizados By Fabian en Hollywood, FL" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Abierto" data-en="Open">Abierto</p>
            <p class="font-display text-lg" data-es="Hasta medianoche sabados" data-en="Until midnight Saturdays">Until midnight Saturdays</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Lun 24h · Mar-Dom 9am-11pm" data-en="Mon 24h · Tue-Sun 9am-11pm">Mon 24h · Tue-Sun 9am-11pm</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="15">15</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="15">15</span>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="15">15</span>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl" data-es="Se habla" data-en="We speak">We speak</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Espanol e Ingles" data-en="Spanish &amp; English">Spanish &amp; English</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">Dolor <span class="text-shine">&amp;</span> Ciatica</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Alivio comprobado" data-en="Proven relief">Proven relief</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hollywood</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sur de Florida" data-en="South Florida">South Florida</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Silk Press", "Therapeutic Massage"),
    ("Loc Retwist", "Deep Tissue"),
    ("Knotless Braids", "Thai Massage"),
    ("K-Tip Extensions", "Personalized Session"),
    ("Keratin", "Pain Relief"),
    ("Orlando, FL", "Hollywood, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (un solo About, + avatar en vez de dos fotos)
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
          <img src="assets/about-room.jpg" alt="Sala de masajes con decoracion zen de Masajes Personalizados By Fabian" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Un terapeuta," data-en="One therapist,">One therapist,</span><br /><span class="text-shine" data-es="manos que sanan" data-en="hands that heal">hands that heal</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Masajes Personalizados By Fabian es el estudio privado de Fabian en Hollywood, FL. Masaje terapeutico, tejido profundo y Thai, cada sesion ajustada a tu dolor y tu presion ideal, en un cuarto tranquilo pensado para desconectar." data-en="Masajes Personalizados By Fabian is Fabian\'s private studio in Hollywood, FL. Therapeutic, deep tissue and Thai massage, every session tailored to your pain and your ideal pressure, in a calm room built to help you unwind.">Masajes Personalizados By Fabian is Fabian\'s private studio in Hollywood, FL. Therapeutic, deep tissue and Thai massage, every session tailored to your pain and your ideal pressure, in a calm room built to help you unwind.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus clientes lo confirman: alivio real de dolor de espalda, hombros y ciatica, con un trato calido y profesional. 5.0 perfecto en 15 reseñas verificadas de Google." data-en="His clients confirm it: real relief from back, shoulder and sciatic pain, with a warm, professional touch. A perfect 5.0 across 15 verified Google reviews.">His clients confirm it: real relief from back, shoulder and sciatic pain, with a warm, professional touch. A perfect 5.0 across 15 verified Google reviews.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="15">15</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(138,166,122,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/avatar-fabian.jpg" alt="Fabian, terapeuta de masajes" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(138,166,122,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Fabian · <span class="text-[color:var(--ink-40)]" data-es="Masajista" data-en="Massage Therapist">Massage Therapist</span></span>')
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
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llamas al (954) 200-3387, cuentas que te molesta y Fabian te da un horario el mismo dia o para esta semana." data-en="Call (954) 200-3387, tell Fabian what is bothering you, and he finds you a slot the same day or this week.">Call (954) 200-3387, tell Fabian what is bothering you, and he finds you a slot the same day or this week.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Cuentas tu dolor" data-en="You describe the pain">You describe the pain</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Espalda, hombros, ciatica o solo tension acumulada: Fabian ajusta la tecnica y la presion a lo que necesitas ese dia." data-en="Back, shoulders, sciatica or just built-up tension: Fabian adjusts the technique and pressure to what you need that day.">Back, shoulders, sciatica or just built-up tension: Fabian adjusts the technique and pressure to what you need that day.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Sesion personalizada" data-en="Personalized session">Personalized session</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Masaje terapeutico, tejido profundo o Thai, en un cuarto tranquilo, sin apuros y sin otra cita encima de la tuya." data-en="Therapeutic, deep tissue or Thai massage, in a calm room, no rushing and no other appointment stacked on top of yours.">Therapeutic, deep tissue or Thai massage, in a calm room, no rushing and no other appointment stacked on top of yours.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Sales renovado" data-en="You leave renewed">You leave renewed</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con menos dolor y, si quieres, tu proxima visita mensual ya acordada por telefono." data-en="You leave with less pain and, if you want, your next monthly visit already set up by phone.">You leave with less pain and, if you want, your next monthly visit already set up by phone.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Tu sesion" data-en="Your">Your</span> <span class="text-shine" data-es="a tu medida" data-en="session, your way">session, your way</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Cada sesion se ajusta a tu dolor y tu presion ideal. Llama al (954) 200-3387 para cotizar y agendar." data-en="Every session is tailored to your pain and your ideal pressure. Call (954) 200-3387 for pricing and to book.">Every session is tailored to your pain and your ideal pressure. Call (954) 200-3387 for pricing and to book.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(138,166,122,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo mas pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Masaje Terapeutico" data-en="Therapeutic Massage">Therapeutic Massage</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El masaje que mas piden los clientes de Fabian: alivio dirigido de dolor de espalda baja, hombros y ciatica." data-en="The massage Fabian's clients ask for most: targeted relief for lower back, shoulder and sciatic pain.">The massage Fabian's clients ask for most: targeted relief for lower back, shoulder and sciatic pain.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Presion firme" data-en="Firm pressure">Firm pressure</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tejido Profundo" data-en="Deep Tissue">Deep Tissue</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trabajo mas intenso sobre nudos y tension acumulada, con la presion exacta que necesitas." data-en="More intense work on knots and built-up tension, with exactly the pressure you need.">More intense work on knots and built-up tension, with exactly the pressure you need.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Estilo tradicional" data-en="Traditional style">Traditional style</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Masaje Thai" data-en="Thai Massage">Thai Massage</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Estiramientos asistidos y presion con las manos para recuperar movilidad en hombros y espalda." data-en="Assisted stretching and hand pressure to help you get back range of motion in your shoulders and back.">Assisted stretching and hand pressure to help you get back range of motion in your shoulders and back.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="A tu medida" data-en="Tailored to you">Tailored to you</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Sesion Personalizada" data-en="Personalized Session">Personalized Session</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Le cuentas a Fabian que te molesta y el combina tecnicas para esa sesion especifica." data-en="You tell Fabian what is bothering you and he blends techniques for that specific session.">You tell Fabian what is bothering you and he blends techniques for that specific session.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Abierto lunes las 24 horas y hasta la medianoche los sabados. Llama al (954) 200-3387." data-en="Open 24 hours on Mondays and until midnight on Saturdays. Call (954) 200-3387.">Open 24 hours on Mondays and until midnight on Saturdays. Call (954) 200-3387.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (una sola foto honesta en vez de 6: curaduria estricta del estudio personal)
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="El" data-en="The">The</span> <span class="text-shine" data-es="estudio" data-en="studio">studio</span>')
rep('''<a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + REVIEWS_LABEL_EN + '''
        </a>''',
    '''<a href="''' + TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (954) 200-3387
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-1 gap-4 sm:gap-5">
        <div class="frame zoomable aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Rincon zen del estudio" data-en="The studio's zen corner">The studio's zen corner</span><img src="assets/gallery-detail.jpg" alt="Decoracion zen del estudio de Masajes Personalizados By Fabian en Hollywood, FL" class="blur-up w-full h-full object-cover" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES (verbatim reales de Google)
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="Lo que dicen" data-en="What his">Lo que dicen</span> <span class="text-shine" data-es="sus clientes" data-en="clients say">sus clientes</span>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 15 reseñas verificadas en Google" data-en="5.0 out of 5 · 15 verified reviews on Google">5.0 out of 5 · 15 verified reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Had a wonderful experience. Was a Mother's Day gift from my son and daughter in law. Didn't know what to expect since I suffer from lower back sciatic pain and Alex has healing hand. Left with no sciatic pain. Definitely coming back for healing. Thank you!!!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ana Llerena</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Highly recommended. From a warm and friendly greeting. Alex does amazing work. Came in with lower back pain and shoulder pain. I walked out feeling great. Very professional and attentive. Makes sure pressure is just right."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">James Schrader</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Fabian is an excellent massage therapist. My monthly visits to him have produced more range of motion in my arms and has relieved much of my lower back pain."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Ric Bonilla</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 15 reseñas en Google" data-en="Read all 15 reviews on Google">Read all 15 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visitanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Hollywood</span></h2>')
rep('''<p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,166,122,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''<p class="font-medium mb-1" data-es="Direccion" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,166,122,0.4)]" href="''' + MAPS + '''" target="_blank" rel="noopener" data-es="Como llegar" data-en="Get directions">Get directions</a>''')
rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,166,122,0.4)]" href="''' + TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes abierto las 24 horas. Martes a domingo, de 9am a 11pm, y sabados hasta la medianoche." data-en="Open 24 hours on Mondays. Tuesday through Sunday, 9am to 11pm, and until midnight on Saturdays.">Open 24 hours on Mondays. Tuesday through Sunday, 9am to 11pm, and until midnight on Saturdays.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,166,122,0.4)]" href="''' + TEL + '''" data-es="Llamar al (954) 200-3387" data-en="Call (954) 200-3387">Call (954) 200-3387</a>''')
rep('''<p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,166,122,0.4)]" href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener">''' + REVIEWS_LABEL_EN + '''</a>
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
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="5.0 estrellas en 15 reseñas verificadas de Google." data-en="5.0 stars across 15 verified Google reviews.">5.0 stars across 15 verified Google reviews.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,166,122,0.4)]" href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener">''' + REVIEWS_LABEL_EN + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Masajes Personalizados By Fabian, 2750 N 29th Ave, Hollywood FL"
          src="''' + MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Manos que sanan de verdad." data-en="Hands that truly heal.">Hands that truly heal.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Una llamada" data-en="One call">One call</span> <span class="text-shine" data-es="te puede aliviar" data-en="could ease it all">could ease it all</span></h2>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Llama al (954) 200-3387 y cuenta que te molesta. Fabian te consigue un horario el mismo dia o para esta semana." data-en="Call (954) 200-3387 and tell Fabian what is bothering you. He will find you a slot the same day or this week.">Call (954) 200-3387 and tell Fabian what is bothering you. He will find you a slot the same day or this week.</p>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (954) 200-3387" data-en="Call (954) 200-3387">Call (954) 200-3387</a>
        <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Leer reseñas en Google" data-en="Read Google reviews">Read Google reviews</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Fabian Masajes</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(185,207,158,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/avatar-fabian.jpg" alt="Masajes Personalizados By Fabian" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(185,207,158,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase" data-es="Fabian Masajes" data-en="Fabian Masajes">Fabian Masajes</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Masajes personalizados en Hollywood, FL. Atencion con cita previa por telefono." data-en="Personalized massage in Hollywood, FL. By appointment only, over the phone.">Personalized massage in Hollywood, FL. By appointment only, over the phone.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + TEL + '''" target="_blank" rel="noopener" class="hover:text-[#b9cf9e]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>''' + ADDR + '''</p>
        <p><a href="''' + TEL + '''" class="hover:text-[#b9cf9e]" data-es="Llamar al (954) 200-3387" data-en="Call (954) 200-3387">Call (954) 200-3387</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#b9cf9e]">Instagram · ''' + REVIEWS_LABEL_EN + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Reseñas" data-en="Reviews">Reviews</p>
        <p><a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#b9cf9e]">5.0 · ''' + REVIEWS_LABEL_EN + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Masajes Personalizados By Fabian.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + TEL + '" class="book-float" aria-label="Call Masajes Personalizados By Fabian">')
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
