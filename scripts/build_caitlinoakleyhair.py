import re, os, shutil

SLUG = "caitlinoakleyhair"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/dark-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b):
    global h
    assert a in h, "NO ANCHOR: " + a[:90]
    h = h.replace(a, b, 1)


# 1. Protect merktop badge block (dark-v2 badge gold == accent-deep hex, must NOT rotate)
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m, "badge block not found"
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# 2. Palette: hue-rotated steel-teal pairs (delta +145.3 from original gold family)
PALETTE = [
    ("#0f0b07", "#070f0e"), ("#171207", "#071517"),
    ("#d4a84b", "#4bc6d4"), ("#b8934a", "#4aafb8"),
    ("#f0dc9e", "#9ee1f0"), ("#9a7431", "#31949a"), ("#e5c374", "#74d7e5"),
    ("#e8c476", "#76dce8"), ("#c9a04a", "#4abcc9"), ("#96742c", "#2c8b96"),
    ("#6b5222", "#22656b"), ("#e8cf96", "#96dee8"), ("#f8eed3", "#d3f2f8"),
    ("#bfa060", "#60b6bf"), ("#f0dcae", "#aee8f0"), ("#faf1dc", "#dcf6fa"),
    ("#ecd9a8", "#a8e2ec"), ("#c9ab6b", "#6bbfc9"), ("#8a744a", "#4a858a"),
    ("#e9c3ab", "#abe9dd"), ("#191307", "#071719"), ("#100c05", "#050f10"),
    ("#0c0905", "#050c0c"),
]
for old, new in PALETTE:
    h = h.replace(old, new)

RGBA_PAIRS = [
    ("rgba(122,90,30", "rgba(30,115,122"),
    ("rgba(180,140,60", "rgba(60,169,180"),
    ("rgba(80,58,18", "rgba(18,76,80"),
    ("rgba(232,210,160", "rgba(160,224,232"),
    ("rgba(110,85,35", "rgba(35,103,110"),
    ("rgba(232,207,150", "rgba(150,222,232"),
    ("rgba(54,42,38", "rgba(38,54,49"),
]
for old, new in RGBA_PAIRS:
    h = h.replace(old, new)

# rgba(212,168,75 = accent, used OUTSIDE the badge too (btn-3d hover glow, stars shadow, glass border etc): rotate
h = h.replace("rgba(212,168,75", "rgba(75,198,212")
# rgba(185,138,128 dark-band orb-b: keep as-is (neutral warm counter-glow, not in accent family, harmless either theme)

# restore badge (still gold, protected)
h = h.replace("@@BADGE@@", badge_block, 1)

# meta theme-color (not covered by PALETTE since original was exact bg hex already rotated above)
print("PALETTE done")

# 3. Globals: booking URL, IG url/handle
old_booksy = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
assert old_booksy in h
h = h.replace(old_booksy, 'https://caitlinoakleyhair.glossgenius.com')
old_ig = 'https://www.instagram.com/pure.artistrysk/'
assert old_ig in h
h = h.replace(old_ig, 'https://www.instagram.com/caitlinoakleyhair/')
assert '@pure.artistrysk' in h
h = h.replace('@pure.artistrysk', '@caitlinoakleyhair')

# 4. HEAD: title, meta, JSON-LD
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Caitlin Oakley Hair · Hair Studio in Miami, FL | Book Online</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Caitlin Oakley Hair, Miami FL: cuts, color, balayage, K-Tip and tape-in extensions, keratin treatments. Real menu, real photos. Book online." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Caitlin Oakley Hair · Hair Studio in Miami, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Cuts, color, balayage and extensions, healthy hair first. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />', '<meta property="og:image" content="assets/raw/bk-13.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />', '<link rel="icon" type="image/jpeg" href="assets/raw/bk-3.jpg" />')

old_jsonld = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_jsonld = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Caitlin Oakley Hair",
    "description": "Hair studio in Miami, FL: cuts, color, balayage, K-Tip and tape-in extensions, keratin smoothing treatments and loc maintenance.",
    "address": { "@type": "PostalAddress", "streetAddress": "218 NW 8th St", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33136", "addressCountry": "US" },
    "telephone": "+13052094441",
    "sameAs": ["https://caitlinoakleyhair.glossgenius.com", "https://www.instagram.com/caitlinoakleyhair/"],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Hair services", "itemListElement": [
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Long Cut" } },
      { "@type": "Offer", "price": "370", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Balayage" } },
      { "@type": "Offer", "price": "550", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "K-Tip Extensions" } },
      { "@type": "Offer", "price": "450", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Keratin Smoothing Treatment" } }
    ] }
  }
  </script>'''
h = h.replace(old_jsonld, new_jsonld, 1)

print("HEAD done")

# 5. Preloader
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">CO</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Caitlin Oakley Hair</span>')

# 6. NAV brand + logo
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,198,212,0.35)]" />',
    '<img src="assets/raw/bk-3.jpg" alt="Caitlin Oakley Hair" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,198,212,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Caitlin <span class="text-[color:var(--accent-deep)]">Oakley</span></span>')

# rename "Opiniones/Reviews" nav label -> "Por qué/Why us" (section becomes especialidades, href/id stay #opiniones)
rep('<a class="nav-link" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="nav-link" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#opiniones" data-es="Por qué" data-en="Why us">Why us</a>')

print("NAV done")

# 7. HERO
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Miami, FL · Hair Studio" data-en="Miami, FL · Hair Studio">Miami, FL · Hair Studio</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>\n        <h1',
    'data-es="Cabello sano primero." data-en="Healthy hair first.">Healthy hair first.</p>\n        <h1')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Cortes, color y" data-en="Cuts, color and">Cuts, color and</span><br /><span data-es="extensiones hechas " data-en="extensions built ">extensions built </span><span class="text-shine" data-es="para tu cabello" data-en="around your hair">around your hair</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="De balayage y color de raiz a extensiones K-Tip, silk press y mantenimiento de locs, cada servicio empieza por la salud de tu cabello. Una estilista, una silla, en el corazon de Miami." data-en="From balayage and root color to K-Tip extensions, silk press and loc maintenance, every service starts with the health of your hair. One stylist, one chair, in the heart of Miami.">From balayage and root color to K-Tip extensions, silk press and loc maintenance, every service starts with the health of your hair. One stylist, one chair, in the heart of Miami.</p>')
rep('''        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>
        </div>
''', '')
rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Reservar cita" data-en="Book online">Book online</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-13.jpg" alt="Short pixie haircut with dramatic studio lighting, Caitlin Oakley Hair" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg">Balayage</p>')
rep('data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="$370 · 3h 30min" data-en="$370 · 3h 30min">$370 · 3h 30min</p>')

# 8. STRIP DE CONFIANZA (no ratings, real specialties + address)
rep('<div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<div class="reveal"><p class="font-display text-2xl">Cuts <span class="text-shine">&amp;</span> Color</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Menu completo, precios reales" data-en="Full menu, real prices">Full menu, real prices</p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Tape-In</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Especialista en extensiones" data-en="Extension specialist">Extension specialist</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">By <span class="text-shine" data-es="cita" data-en="appt">appt</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Atención uno a uno" data-en="One-on-one care">One-on-one care</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">218 NW 8th St</p></div>')

# 9. MARQUEE (x2, appears 4 times each word)
for old, new in [
    ('Silk Press', 'Cuts'),
    ('Loc Retwist', 'Color'),
    ('Knotless Braids', 'Extensions'),
    ('K-Tip Extensions', 'Keratin Care'),
    ('Keratin', 'Locs'),
    ('Orlando, FL', 'Miami, FL'),
]:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(tag_old)
    assert cnt == 4, f"{old}: expected 4 got {cnt}"
    h = h.replace(tag_old, tag_new)

print("HERO+STRIP+MARQUEE done")

# 10. EXPERIENCIA
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-12.jpg" alt="Long sleek straight hair color result" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-16.jpg" alt="Long dark wavy hair, back view" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>', 'data-es="La experiencia" data-en="The experience">The experience</p>')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="cabello sano primero" data-en="healthy hair first">healthy hair first</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Caitlin Oakley Hair es un estudio privado en Miami enfocado primero en la salud de tu cabello, desde color y cortes hasta extensiones K-Tip y mantenimiento de locs." data-en="Caitlin Oakley Hair is a private studio in Miami focused on the health of your hair first, from color and cuts to K-Tip extensions and loc maintenance.">Caitlin Oakley Hair is a private studio in Miami focused on the health of your hair first, from color and cuts to K-Tip extensions and loc maintenance.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Cada cita empieza con una consulta, para que la tecnica, de una correccion de color completa a un corte simple, se construya alrededor de lo que tu cabello realmente necesita." data-en="Every appointment starts with a consultation, so the technique, from a full color correction to a simple trim, is built around what your hair actually needs.">Every appointment starts with a consultation, so the technique, from a full color correction to a simple trim, is built around what your hair actually needs.</p>')
rep('''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Color</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Especialidad" data-en="Specialty">Specialty</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">Miami</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Ubicación" data-en="Location">Location</p></div>''')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,198,212,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Caitlin Oakley Hair, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,198,212,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="text-sm font-light">Caitlin · <span class="text-[color:var(--ink-40)]" data-es="Estilista de cabello" data-en="Hair stylist">Hair stylist</span></span>')

print("EXPERIENCIA done")

# 11. EL METODO
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio con precio y duración claros: corte, color o extensiones, y confirmas al instante." data-en="Pick your service with clear price and duration: cut, color or extensions, and confirm instantly.">Pick your service with clear price and duration: cut, color or extensions, and confirm instantly.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el look que buscas definen la tecnica y los productos que se usan." data-en="Your hair type, its health and the look you want define the technique and the products used.">Your hair type, its health and the look you want define the technique and the products used.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De un tratamiento de 20 minutos a una correccion de color de varias horas: cada servicio recibe su tiempo completo." data-en="From a 20-minute treatment to a multi-hour color correction, every service gets its full time.">From a 20-minute treatment to a multi-hour color correction, every service gets its full time.</p>''')
rep('''          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con un acabado hecho para durar y las indicaciones para cuidarlo en casa." data-en="You leave with a finish built to last and the guidance to care for it at home.">You leave with a finish built to last and the guidance to care for it at home.</p>''')

print("METODO done")

# 12. SERVICIOS (regex-replace whole grid + note)
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Caitlin Oakley Hair. Reserva con confirmación inmediata." data-en="Prices and durations as published by Caitlin Oakley Hair. Booking confirms instantly.">Prices and durations as published by Caitlin Oakley Hair. Booking confirms instantly.</p>')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="servicio" data-en="service">service</span>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid, "services grid not found"
NEW_SERVICES = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cortes" data-en="Cuts">Cuts</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Corte a tu medida" data-en="Cut to fit you">Cut to fit you</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Long Cut $100 (1h), Short Cut $55 (45min), Curly Cut $100 (1h), Pixie Cut $100 (1h) y mas." data-en="Long Cut $100 (1h), Short Cut $55 (45min), Curly Cut $100 (1h), Pixie Cut $100 (1h) and more.">Long Cut $100 (1h), Short Cut $55 (45min), Curly Cut $100 (1h), Pixie Cut $100 (1h) and more.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $35" data-en="From $35">From $35</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">15min+</p></div>
            <a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(75,198,212,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Color" data-en="Color">Color</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Balayage</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Balayage $370 (3h 30min), Full Highlight $360 (3h), Root To End Colour $210 (2h), correccion de color desde $560." data-en="Balayage $370 (3h 30min), Full Highlight $360 (3h), Root To End Colour $210 (2h), color correction from $560.">Balayage $370 (3h 30min), Full Highlight $360 (3h), Root To End Colour $210 (2h), color correction from $560.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $210" data-en="From $210">From $210</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h+</p></div>
            <a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extensiones" data-en="Extensions">Extensions</p>
          <h3 class="font-display text-2xl leading-snug mb-3">K-Tip &amp; Tape-In</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="K-Tip $550 (2h 30min), Tape-In $350 (1h 30min), Clip-In $150 (1h), extensiones weft desde $450." data-en="K-Tip $550 (2h 30min), Tape-In $350 (1h 30min), Clip-In $150 (1h), weft extensions from $450.">K-Tip $550 (2h 30min), Tape-In $350 (1h 30min), Clip-In $150 (1h), weft extensions from $450.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $150" data-en="From $150">From $150</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h+</p></div>
            <a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Tratamientos" data-en="Treatments">Treatments</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Keratina y mas" data-en="Keratin &amp; more">Keratin &amp; more</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Keratin Smoothing $450 (3h), Olaplex $30 (20min), Deep Conditioning $30 (30min), Silk Press $95 (1h 30min)." data-en="Keratin Smoothing $450 (3h), Olaplex $30 (20min), Deep Conditioning $30 (30min), Silk Press $95 (1h 30min).">Keratin Smoothing $450 (3h), Olaplex $30 (20min), Deep Conditioning $30 (30min), Silk Press $95 (1h 30min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine" data-es="Desde $30" data-en="From $30">From $30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">20min+</p></div>
            <a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Tambien: buzz cuts, blowouts, updos, retwist y color de locs, y camo color para hombre. Menu completo y disponibilidad en el sitio de reservas." data-en="Also available: buzz cuts, blowouts, updos, loc retwist and color, and men\'s camo color. Full menu and availability on the booking site.">Also available: buzz cuts, blowouts, updos, loc retwist and color, and men\'s camo color. Full menu and availability on the booking site.</span></p>')

print("SERVICIOS done")

# 13. GALERIA
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid, "gallery grid not found"
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Editorial en movimiento" data-en="Editorial motion">Editorial motion</span><img src="assets/raw/bk-8.jpg" alt="Long wavy dark hair, editorial black and white photo" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Color turquesa" data-en="Teal color">Teal color</span><img src="assets/raw/bk-14.jpg" alt="Wavy hair dyed a vivid teal blue" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Rizos naturales" data-en="Natural curls">Natural curls</span><img src="assets/raw/bk-1.jpg" alt="Natural curly hair portrait" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Rizos al viento" data-en="Windswept curls">Windswept curls</span><img src="assets/raw/bk-9.jpg" alt="Curly blonde hair, windswept close-up" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Bob rubio" data-en="Blonde bob">Blonde bob</span><img src="assets/raw/bk-6.jpg" alt="Blonde bob haircut, side profile" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Reflejos iridiscentes" data-en="Iridescent tones">Iridescent tones</span><img src="assets/raw/bk-15.jpg" alt="Close-up of hair strands with iridescent color tones" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]

print("GALERIA done")

# 14. OPINIONES -> ESPECIALIDADES ("Por que Caitlin Oakley Hair", sin-testimonios)
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Opiniones" data-en="Reviews">Opiniones</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="El estudio" data-en="The studio">The studio</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Por qué" data-en="Why">Why</span> <span class="text-shine" data-es="Caitlin Oakley Hair" data-en="Caitlin Oakley Hair">Caitlin Oakley Hair</span></h2>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Cortes, color y extensiones para todo tipo de cabello, siempre empezando por lo que es sano para tu cabello." data-en="Cuts, color and extensions for every hair type, with healthy hair always the starting point.">Cuts, color and extensions for every hair type, with healthy hair always the starting point.</p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid, "reviews grid not found"
NEW_WHY = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="font-display text-2xl text-shine mb-3" data-es="Cabello sano primero" data-en="Healthy hair first">Healthy hair first</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Cada servicio de color y extensiones empieza por lo que realmente es sano para tu cabello, no solo por el look." data-en="Every color and extension service starts with what is actually healthy for your hair, not just the look.">Every color and extension service starts with what is actually healthy for your hair, not just the look.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Una estilista, una silla" data-en="One stylist, one chair">One stylist, one chair</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sin cambios de cuarto entre servicios. La misma estilista consulta, colorea y termina tu look." data-en="No handoffs between rooms. The same stylist consults, colors and finishes your look.">No handoffs between rooms. The same stylist consults, colors and finishes your look.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="font-display text-2xl text-shine mb-3" data-es="Todo tipo de cabello" data-en="Every hair type">Every hair type</p>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De cortes rizados y locs a silk press y K-Tips, el menu cubre cabello natural, relajado y con color por igual." data-en="From curly cuts and locs to silk press and K-Tips, the menu covers natural, relaxed and colored hair alike.">From curly cuts and locs to silk press and K-Tips, the menu covers natural, relaxed and colored hair alike.</p>
        </div>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_WHY + h[reviews_grid.end():]

rep('<a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver el menu completo y reservar" data-en="See the full menu and book">See the full menu and book</a>')

print("ESPECIALIDADES done")

# 15. UBICACION
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">218 NW 8th St, Miami, FL 33136</p>')
rep('href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806"',
    'href="https://www.google.com/maps?q=218+NW+8th+St,+Miami,+FL+33136"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
    'data-es="Con cita previa en linea: eliges servicio, dia y hora, y la confirmacion es inmediata." data-en="By appointment online: pick the service, day and time, and the confirmation is instant.">By appointment online: pick the service, day and time, and the confirmation is instant.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,198,212,0.4)]" href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,198,212,0.4)]" href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="Mira los estilos mas recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>')
rep('title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"',
    'title="Mapa: Caitlin Oakley Hair, 218 NW 8th St, Miami FL"')
rep('src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    'src="https://www.google.com/maps?q=218+NW+8th+St,+Miami,+FL+33136&output=embed"')

print("UBICACION done")

# 16. CTA FINAL
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>\n      <h2',
    'data-es="Cabello sano primero." data-en="Healthy hair first.">Healthy hair first.</p>\n      <h2')
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Tu proximo look" data-en="Your next look">Your next look</span> <span class="text-shine" data-es="esta a un toque" data-en="is one tap away">is one tap away</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva en linea en segundos: tu corte, tu color, o esas extensiones que llevas planeando." data-en="Book online in seconds: your cut, your color, or the extensions you have been planning.">Book online in seconds: your cut, your color, or the extensions you have been planning.</p>')
rep('<a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar cita" data-en="Book online">Book online</a>')
rep('data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Seguir en Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')

print("CTA FINAL done")

# 17. FOOTER
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Caitlin Oakley Hair</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(150,222,232,0.35)]" loading="lazy" />',
    '<img src="assets/raw/bk-3.jpg" alt="Caitlin Oakley Hair" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(150,222,232,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">Caitlin Oakley Hair</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Estudio de cabello en Miami, FL. Atencion con cita previa." data-en="Hair studio in Miami, FL. By appointment only.">Hair studio in Miami, FL. By appointment only.</p>')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', '<p>218 NW 8th St, Miami, FL 33136</p>')
rep('<p><a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#abe9dd]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="hover:text-[#abe9dd]" data-es="Reservas en linea" data-en="Online booking">Online booking</a></p>')
rep('<p><a href="https://www.instagram.com/caitlinoakleyhair/" target="_blank" rel="noopener" class="hover:text-[#abe9dd]">Instagram · @caitlinoakleyhair</a></p>',
    '<p><a href="https://www.instagram.com/caitlinoakleyhair/" target="_blank" rel="noopener" class="hover:text-[#abe9dd]">Instagram · @caitlinoakleyhair</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Caitlin Oakley Hair.</p>')

print("FOOTER done")

# 18. book-float button (svg stroke color 1c1408 unrelated to accent palette, keep)
rep('<a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="https://caitlinoakleyhair.glossgenius.com" target="_blank" rel="noopener" class="book-float" aria-label="Book online">')

print("ALL SECTIONS done")
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print(len(h), "chars written (checkpoint 7, final)")
