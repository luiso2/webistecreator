import re
import shutil

SLUG = "caninodogllc"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/light-v2/index.html", PATH)
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


TEL = "tel:+17543148614"
TEL_DISPLAY = "(754) 314-8614"
IG_URL = "https://www.instagram.com/caninodoggroming/"
IG_HANDLE = "@caninodoggroming"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> lagoon teal + aqua (marca real: van turquesa,
#    letrero neon "CaninoDog" teal dentro del van). No repite ninguna paleta de
#    DESIGN.md ni la naranja/teal ya usada en a-labor-of-love-dog-grooming-kendall.
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#0e8f93"),  # accent-deep
    ("#c47a9c", "#3dbdc2"),  # accent-mid
    ("#7d3457", "#0a5a5e"),  # dark mid -> deep lagoon teal
    ("#5c2140", "#073d3f"),  # btn-3d sole darkest
    ("#5f2c48", "#0d4f52"),  # step-num gradient end
    ("#b25a85", "#2fa7ac"),  # shimmer stop
    ("#c9789f", "#4bbfc4"),  # shimmer stop
    ("#d9a8c2", "#a9dcdc"),  # orb-b -> soft aqua
    ("#d3a2bc", "#bfe8e6"),  # dark-band btn-3d gradient end (light)
    ("#efd0e0", "#e3f5f3"),  # dark-band btn-3d gradient mid
    ("#fbeff5", "#f6fcfb"),  # dark-band btn-3d gradient start (lightest)
    ("#f0bed7", "#9fe0de"),  # dark-band shine/orb/stars light accent
    ("#f2cfe0", "#cdeeec"),  # shimmer dark-band last stop
    ("#f8dfeb", "#e8f7f5"),  # shimmer dark-band 3rd stop
    ("#dc9dbe", "#2fb8bd"),  # scroll-progress end stop
    ("#8a5573", "#0a4446"),  # dark-band btn shadow deep
    ("#e5c1d4", "#d7f0ee"),  # orb-c -> pale mint
    ("#f2d5e3", "#eafaf8"),  # orb-a -> very pale aqua
    ("#faf2f6", "#fbf8f2"),  # bg
    ("#f3e0ea", "#e8f5f3"),  # bg-2 / accent-soft
    ("#f6f1ea", "#fbf8f2"),  # theme-color meta
    ("#fbf3f8", "#f7fdfc"),  # tile-cap text near-white
    ("#33222c", "#1d3334"),  # ink
    ("#2a1722", "#0b2626"),  # cta-final bg gradient start
    ("#1f0f18", "#071a1a"),  # cta-final bg gradient end
    ("#1c0f16", "#081d1d"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(14,143,147"),   # accent-deep alpha
    ("rgba(51,34,44", "rgba(29,51,52"),       # ink alpha
    ("rgba(125,52,87", "rgba(10,90,94"),      # dark mid alpha
    ("rgba(240,190,215", "rgba(159,224,222"), # light accent on dark-band alpha
    ("rgba(70,25,50", "rgba(7,61,63"),        # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(251,248,242"), # bg alpha (nav scrolled / dark-band ink)
    ("rgba(253,246,250", "rgba(247,253,252"), # surface glass alpha
    ("rgba(233,205,186", "rgba(159,224,222"), # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(90,190,188"),  # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: Booksy -> telefono real; Instagram real
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, TEL)
c2 = h.count(f'href="{TEL}" target="_blank" rel="noopener"')
assert c2 >= 10, c2
h = h.replace(f'href="{TEL}" target="_blank" rel="noopener"', f'href="{TEL}"')

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, IG_URL)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Canino Dog · Mobile Pet Grooming in Pembroke Pines, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Canino Dog, mobile pet grooming in Pembroke Pines, FL: gentle, patient grooming at your door, even for anxious and senior dogs. 4.9 stars across 83 Google reviews. Call to book." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Canino Dog · Mobile Pet Grooming in Pembroke Pines, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Gentle mobile dog grooming at your door. 4.9 stars on Google. Call to book." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-maltese-groom.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Canino Dog Mobile Pet Grooming",
    "description": "Mobile dog grooming serving Pembroke Pines, FL and nearby areas. Gentle, patient grooming at the client's door, by appointment, no fixed storefront.",
    "telephone": "+1-754-314-8614",
    "areaServed": { "@type": "City", "name": "Pembroke Pines, FL" },
    "address": { "@type": "PostalAddress", "addressLocality": "Pembroke Pines", "addressRegion": "FL", "addressCountry": "US" },
    "sameAs": ["https://www.instagram.com/caninodoggroming/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "83", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "18:00" }
    ]
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: light-v2 ya viene EN default (idioma principal del negocio) -> sin cambios
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 6. NAV (header + mobile menu)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(14,143,147,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Canino Dog mobile pet grooming" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(14,143,147,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Canino <span class="text-[color:var(--accent-deep)]">Dog</span></span>')

NAV_LINKS = [
    ('#experiencia', 'La Experiencia', 'The Experience', 'El Equipo', 'The Team'),
    ('#metodo', 'El Método', 'The Method', 'Cómo Funciona', 'How It Works'),
    ('#servicios', 'Servicios', 'Services', 'Servicios', 'Services'),
    ('#galeria', 'Galería', 'Gallery', 'Galería', 'Gallery'),
    ('#opiniones', 'Opiniones', 'Reviews', 'Opiniones', 'Reviews'),
    ('#ubicacion', 'Ubicación', 'Location', 'Zona de Servicio', 'Service Area'),
]
for anchor, old_es, old_en, new_es, new_en in NAV_LINKS:
    rep_all(f'data-es="{old_es}" data-en="{old_en}">{old_es}</a>', f'data-es="{new_es}" data-en="{new_en}">{new_en}</a>', expect=2)

rep('<button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Cambiar idioma">EN</button>',
    '<button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Change language">EN</button>')

CALL_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'

rep(f'''<a href="{TEL}" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>''',
    f'''<a href="{TEL}" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          {CALL_ICON}
          <span data-es="Llamar ahora" data-en="Call now">Call now</span>
        </a>''')

rep(f'''<a href="{TEL}" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>''',
    f'''<a href="{TEL}" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>''')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. PRELOADER
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">CD</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Canino Dog</span>')
print("PRELOADER done")

# ---------------------------------------------------------------------------
# 8. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Pembroke Pines, FL · Mobile Pet Grooming" data-en="Pembroke Pines, FL · Mobile Pet Grooming">Pembroke Pines, FL · Mobile Pet Grooming</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Grooming que llega a tu puerta." data-en="Grooming that comes to your door.">Grooming that comes to your door.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Un spa de grooming completo," data-en="A full grooming spa,">A full grooming spa,</span><br /><span data-es="rodando hasta tu " data-en="parked right at your ">parked right at your </span><span class="text-shine" data-es="puerta" data-en="door">door</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Un van totalmente equipado llega a tu casa en Pembroke Pines con bañera, mesa y todas las herramientas de un salón real. Edgar, tu groomer, es paciente con perros ansiosos, mayores y dificiles, sin jaulas ni esperas en un lobby." data-en="A fully equipped van pulls up at your home in Pembroke Pines with a real tub, table and every tool of a true salon. Edgar, your groomer, is patient with anxious, senior and difficult dogs, no cages and no waiting around in a lobby.">A fully equipped van pulls up at your home in Pembroke Pines with a real tub, table and every tool of a true salon. Edgar, your groomer, is patient with anxious, senior and difficult dogs, no cages and no waiting around in a lobby.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 83 reseñas en Google" data-en="4.9 · 83 reviews on Google">4.9 · 83 reviews on Google</span>')
rep(f'''<a href="{TEL}" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @_lashbloom
          </a>''',
    f'''<a href="{TEL}" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llamar para reservar" data-en="Call to book">Call to book</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{IG_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            {IG_HANDLE}
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-maltese-groom.jpg" alt="Freshly groomed bichon smiling next to the CaninoDog neon sign inside the mobile grooming van" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Servicio" data-en="Service">Service</p>
            <p class="font-display text-lg" data-es="100% movil" data-en="100% mobile">100% mobile</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Rodamos hasta tu puerta" data-en="We drive right to your door">We drive right to your door</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 9. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="83">83</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Gentle <span class="text-shine">&amp;</span> Patient</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Con perros ansiosos y mayores" data-en="With anxious &amp; senior dogs">With anxious &amp; senior dogs</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl" data-es="100%" data-en="100%">100%</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Movil, sin jaulas ni traslados" data-en="Mobile, no cages or car rides">Mobile, no cages or car rides</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Pembroke Pines</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Zona de servicio" data-en="Service area">Service area</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 10. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Mobile Grooming"),
    ("Hybrid Set", "Breed Haircuts"),
    ("Volume Set", "Bath &amp; Brush-Out"),
    ("Mega Volume", "Nail Trims"),
    ("Bottom Lashes", "Gentle Handling"),
    ("West Palm Beach, FL", "Pembroke Pines, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 11. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-sheepdog-table.jpg" alt="Sheepdog mix freshly groomed with a bandana on the grooming table inside the Canino Dog van" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-van-interior.jpg" alt="Inside the Canino Dog mobile grooming van, with the grooming table and neon sign visible through the open door" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="El equipo" data-en="The team">The team</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un salon real," data-en="A real salon,">A real salon,</span><br /><span class="text-shine" data-es="sobre ruedas" data-en="on wheels">on wheels</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    "data-es=\"Canino Dog es el van de grooming movil de Edgar en Pembroke Pines: una bañera profesional, mesa de corte y todas las herramientas de un salón, dentro de un vehiculo equipado que se estaciona frente a tu casa.\" data-en=\"Canino Dog is Edgar's mobile grooming van serving Pembroke Pines: a professional tub, a grooming table and every tool of a real salon, inside one fully equipped vehicle that parks right outside your home.\">Canino Dog is Edgar's mobile grooming van serving Pembroke Pines: a professional tub, a grooming table and every tool of a real salon, inside one fully equipped vehicle that parks right outside your home.</p>")
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Las reseñas repiten lo mismo: puntualidad, horarios flexibles y un trato paciente con perros ansiosos, que salen del van con menos estres que en un salón tradicional, sin jaula y sin esperar en un lobby." data-en="Reviews keep pointing to the same thing: punctuality, flexible scheduling and patient handling of anxious dogs, who come out of the van less stressed than at a traditional salon, with no cage and no lobby wait.">Reviews keep pointing to the same thing: punctuality, flexible scheduling and patient handling of anxious dogs, who come out of the van less stressed than at a traditional salon, with no cage and no lobby wait.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="83">83</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(14,143,147,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="Canino Dog mobile pet grooming" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(14,143,147,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Edgar · <span class="text-[color:var(--ink-40)]" data-es="Groomer movil" data-en="Mobile groomer">Mobile groomer</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 12. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, sin salir" data-en="Your visit, without">Your visit, without</span> <span class="text-shine" data-es="de casa" data-en="leaving home">leaving home</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Llama o escribe" data-en="Call or text">Call or text</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llama al (754) 314-8614 y cuentale a Edgar la raza, el pelaje y el temperamento de tu perro para encontrar un horario." data-en="Call (754) 314-8614 and tell Edgar your dog's breed, coat and temperament so he can find a time that works for you.">Call (754) 314-8614 and tell Edgar your dog's breed, coat and temperament so he can find a time that works for you.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="El van llega" data-en="The van arrives">The van arrives</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Edgar estaciona el van frente a tu casa en Pembroke Pines, puntual, con la bañera y la mesa ya listas." data-en="Edgar parks the fully equipped van right outside your home in Pembroke Pines, on time, with the tub and table already set up.">Edgar parks the fully equipped van right outside your home in Pembroke Pines, on time, with the tub and table already set up.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="El grooming" data-en="The groom">The groom</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Baño, corte segun la raza y uñas, dentro del van, con el trato paciente que piden perros ansiosos o mayores." data-en="A bath, a breed-appropriate haircut and a nail trim, all inside the van, with the patient handling anxious or senior dogs need.">A bath, a breed-appropriate haircut and a nail trim, all inside the van, with the patient handling anxious or senior dogs need.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Entrega" data-en="Pickup">Pickup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu perro vuelve a casa limpio y relajado, sin el estres de un traslado, tal como describen las reseñas en Google." data-en="Your dog comes back inside clean and relaxed, with none of the stress of a car ride, exactly as the Google reviews describe.">Your dog comes back inside clean and relaxed, with none of the stress of a car ride, exactly as the Google reviews describe.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 13. SERVICIOS (header + grid completo por regex + menu categorizado)
# ---------------------------------------------------------------------------
rep('data-es="Servicios" data-en="Services">Servicios</p>',
    'data-es="Servicios" data-en="Services">Services</p>', n=1)
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Grooming," data-en="Grooming,">Grooming,</span> <span class="text-shine" data-es="a domicilio" data-en="at your door">at your door</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Sin lista de precios publicada: cada perro, raza y pelaje es distinto. Llama al (754) 314-8614 para una cotización real." data-en="No published price list, every dog, breed and coat is different. Call (754) 314-8614 for a real quote.">No published price list, every dog, breed and coat is different. Call (754) 314-8614 for a real quote.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Servicio completo" data-en="Full service">Full service</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Baño y Corte Movil" data-en="Mobile Bath &amp; Haircut">Mobile Bath &amp; Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Baño completo y corte segun la raza, dentro del van totalmente equipado, estacionado frente a tu casa." data-en="A full bath and a breed-appropriate haircut, inside the fully equipped van, parked right outside your home.">A full bath and a breed-appropriate haircut, inside the fully equipped van, parked right outside your home.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Precio por consulta" data-en="Call for pricing">Call for pricing</p>
            <a href="{TEL}" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(14,143,147,0.4); box-shadow: 0 18px 50px rgba(29,51,52,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo más pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Perros Ansiosos y Mayores" data-en="Anxious &amp; Senior Dogs">Anxious &amp; Senior Dogs</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trato calmado y paciente para perros nerviosos, mayores o dificiles, sin jaula y sin la espera de un salon tradicional." data-en="Calm, patient handling for nervous, senior or difficult dogs, no cage and none of the wait of a traditional salon.">Calm, patient handling for nervous, senior or difficult dogs, no cage and none of the wait of a traditional salon.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Precio por consulta" data-en="Call for pricing">Call for pricing</p>
            <a href="{TEL}" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar para reservar" data-en="Call to book">Call to book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Toque final" data-en="Finishing touch">Finishing touch</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Uñas y Detalles" data-en="Nail Trim &amp; Finishing">Nail Trim &amp; Finishing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte de uñas y los ultimos detalles del arreglo, parte de cada visita del van de Canino Dog." data-en="Nail trimming and the last finishing touches, part of every Canino Dog van visit.">Nail trimming and the last finishing touches, part of every Canino Dog van visit.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Precio por consulta" data-en="Call for pricing">Call for pricing</p>
            <a href="{TEL}" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Puntualidad" data-en="On time, every time">On time, every time</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Horarios Flexibles" data-en="Flexible Scheduling">Flexible Scheduling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Edgar coordina el horario contigo y llega puntual, segun confirman las reseñas en Google." data-en="Edgar works the schedule around you and shows up on time, exactly as the Google reviews confirm.">Edgar works the schedule around you and shows up on time, exactly as the Google reviews confirm.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Precio por consulta" data-en="Call for pricing">Call for pricing</p>
            <a href="{TEL}" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Grooming basico" data-en="Grooming basics">Grooming basics</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Baño completo" data-en="Full bath">Full bath</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Corte segun la raza" data-en="Breed-appropriate haircut">Breed-appropriate haircut</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Corte de uñas" data-en="Nail trim">Nail trim</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Comodidad" data-en="Comfort &amp; care">Comfort &amp; care</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Sin jaulas ni traslados" data-en="No cages, no car rides">No cages, no car rides</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Atencion 1:1 en cada visita" data-en="1:1 attention every visit">1:1 attention every visit</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Por que eligen a Edgar" data-en="Why owners choose Edgar">Why owners choose Edgar</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="4.9 estrellas, 83 reseñas en Google" data-en="4.9 stars, 83 Google reviews">4.9 stars, 83 Google reviews</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Puntual y de confianza" data-en="Punctual &amp; reliable">Punctual &amp; reliable</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Paciente con perros ansiosos y mayores" data-en="Gentle with anxious &amp; senior dogs">Gentle with anxious &amp; senior dogs</span></li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Sin lista de precios en línea. Llama al (754) 314-8614 para una cotización." data-en="No online price list. Call (754) 314-8614 for a quote.">No online price list. Call (754) 314-8614 for a quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 14. GALERIA (header + grid completo por regex)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Perros" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="dogs">dogs</span>')
rep(f'''<a href="{IG_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @_lashbloom
        </a>''',
    f'''<a href="{IG_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          {IG_HANDLE}
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Fresca del baño y feliz" data-en="Fresh-groomed and happy">Fresh-groomed and happy</span><img src="assets/gallery-01-poodle-couch.jpg" alt="Freshly groomed toy poodle standing proudly on the couch at home after a Canino Dog visit" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Lista con su moño" data-en="Bow-ready">Bow-ready</span><img src="assets/gallery-02-schnauzer-bow.jpg" alt="Schnauzer puppy with a pink flower collar after grooming" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Celebrando en grande" data-en="Birthday pup">Birthday pup</span><img src="assets/gallery-03-birthday-cupcake.jpg" alt="Freshly groomed white dog wearing a birthday crown in front of a small cupcake" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Listas para pasear" data-en="Walk-ready duo">Walk-ready duo</span><img src="assets/gallery-04-two-shihtzus.jpg" alt="Two freshly groomed small dogs walking together at home after grooming" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="El spa movil" data-en="The mobile spa">The mobile spa</span><img src="assets/gallery-05-van-front.jpg" alt="The Canino Dog mobile grooming van parked with its side door open, showing the grooming table inside" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. MARQUEE 2 (reverse) ya cubierto por el replace_all de MARQUEE_WORDS arriba
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 16. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="Lo que dicen" data-en="What pet">What pet</span> <span class="text-shine" data-es="sus clientes" data-en="owners say">owners say</span>')
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 83 reseñas verificadas en Google" data-en="4.9 out of 5 · 83 verified reviews on Google">4.9 out of 5 · 83 verified reviews on Google</span></p>')
rep('''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>''',
    '''<figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The best of the best. Reliable and efficient groomer. Edgar has been taking care of my girls for years and I couldn't be happier. He takes care of them like his own. Gives the best haircuts. My girls always come out looking and smelling great."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Gigi De La Rosa</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Edgar from Canino Dog is incredible! My dog has anxiety and usually gets nervous during grooming, but Edgar's calm and gentle approach completely put her at ease. She looked beautiful, smelled amazing, and came home relaxed and happy."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Barbara Galizia</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I'm so happy with the service at Canino Dog! They're reliable, professional, and truly care about the dogs. My pups always come back looking amazing and well-groomed. Highly recommend to anyone looking for a trustworthy grooming service."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Janet Nieman</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>''')
rep(f'<a href="{TEL}" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    f'<a href="https://www.google.com/maps/place/?q=place_id:ChIJ93alNU2n2YgR6X8RoEbUy_c" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 83 reseñas en Google" data-en="Read all 83 reviews on Google">Read all 83 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 17. UBICACION -> ZONA DE SERVICIO (negocio movil, sin local fijo: sin mapa,
#     foto real del van en vez de iframe, per PIPELINE Fase 3.5 variante adaptada)
# ---------------------------------------------------------------------------
rep('data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    'data-es="Zona de servicio" data-en="Service area">Service area</p>')
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Rodamos por" data-en="We roll through">We roll through</span> <span class="text-shine">Pembroke Pines</span>')
rep('''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(14,143,147,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>
          </div>''',
    '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Sin local fijo" data-en="No storefront">No storefront</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Canino Dog es 100% movil: no hay tienda que visitar. El van llega a tu casa en Pembroke Pines y alrededores." data-en="Canino Dog is 100% mobile: there is no shop to visit. The van comes to your home in Pembroke Pines and nearby areas.">Canino Dog is 100% mobile: there is no shop to visit. The van comes to your home in Pembroke Pines and nearby areas.</p>
            </div>
          </div>''')
rep('''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(14,143,147,0.4)]" href="{TEL}" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>
          </div>'''.replace("{TEL}", TEL),
    f'''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Bookings</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Por cita, llamando directo. Edgar confirma dia, hora y la direccion donde estacionar el van." data-en="By appointment, just call. Edgar confirms the day, time and where to park the van.">By appointment, just call. Edgar confirms the day, time and where to park the van.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(14,143,147,0.4)]" href="{TEL}" data-es="Llamar para reservar" data-en="Call to book">Call to book</a>
            </div>
          </div>''')
rep(f'''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(14,143,147,0.4)]" href="{IG_URL}" target="_blank" rel="noopener">@_lashbloom</a>
            </div>
          </div>''',
    f'''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los perros groomeados mas recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest groomed pups and DM any questions before your appointment.">See the latest groomed pups and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(14,143,147,0.4)]" href="{IG_URL}" target="_blank" rel="noopener">{IG_HANDLE}</a>
            </div>
          </div>''')

# Mapa -> foto real del van (negocio movil sin local fijo)
rep('''<div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div class="frame reveal min-h-[380px] img-reveal" style="transition-delay:180ms">
        <img src="assets/gallery-05-van-front.jpg" alt="The Canino Dog mobile grooming van, fully equipped, ready to park outside a client's home in Pembroke Pines" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 18. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Grooming que llega a tu puerta." data-en="Grooming that comes to your door.">Grooming that comes to your door.</p>')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu perro, fresco" data-en="Your dog, fresh">Your dog, fresh</span> <span class="text-shine" data-es="sin salir de casa" data-en="without leaving home">without leaving home</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Llama o escribe al (754) 314-8614 y coordina el dia que Edgar estaciona el van frente a tu casa en Pembroke Pines." data-en="Call or text (754) 314-8614 and set the day Edgar parks the van right outside your home in Pembroke Pines.">Call or text (754) 314-8614 and set the day Edgar parks the van right outside your home in Pembroke Pines.</p>')
rep(f'''<a href="{TEL}" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="{IG_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    f'''<a href="{TEL}" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar para reservar" data-en="Call to book">Call to book</a>
        <a href="{IG_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 19. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Canino Dog</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(159,224,222,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>''',
    '''<img src="assets/logo.jpg" alt="Canino Dog mobile pet grooming" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(159,224,222,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Canino Dog</span>''')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Mobile dog grooming en Pembroke Pines, FL. Con cita previa, nosotros llegamos a ti." data-en="Mobile dog grooming in Pembroke Pines, FL. By appointment, we come to you.">Mobile dog grooming in Pembroke Pines, FL. By appointment, we come to you.</p>')
rep(f'''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="{TEL}" class="hover:text-[#9fe0de]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    f'''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contact</p>
        <p>{TEL_DISPLAY}</p>
        <p><a href="{TEL}" class="hover:text-[#9fe0de]" data-es="Pembroke Pines y alrededores" data-en="Pembroke Pines &amp; nearby">Pembroke Pines &amp; nearby</a></p>''')
rep(f'<p><a href="{IG_URL}" target="_blank" rel="noopener" class="hover:text-[#9fe0de]">Instagram · @_lashbloom</a></p>',
    f'<p><a href="{IG_URL}" target="_blank" rel="noopener" class="hover:text-[#9fe0de]">Instagram · {IG_HANDLE}</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Canino Dog.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 20. Boton flotante de reserva (ya cubierto por OLD_BOOK -> TEL global)
# ---------------------------------------------------------------------------
rep('<a href="' + TEL + '" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + TEL + '" class="book-float" aria-label="Call to book">')

open(PATH, "w", encoding="utf-8").write(h)
print("WROTE", PATH, len(h), "bytes")
