import re
import shutil

SLUG = "a-labor-of-love-dog-grooming-kendall"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/light-v2/index.html", PATH)
h = open(PATH, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:160]
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None):
    global h
    c = h.count(a)
    assert c > 0, "NO ANCHOR: " + a[:160]
    if expect is not None:
        assert c == expect, f"count {c} != expected {expect} for " + a[:80]
    h = h.replace(a, b)


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> pumpkin orange + brand teal (mascot)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#d9720f"),  # accent-deep
    ("#c47a9c", "#e6a23c"),  # accent-mid
    ("#7d3457", "#a8500a"),  # dark mauve mid -> deep burnt orange
    ("#5c2140", "#7a3d08"),  # btn-3d sole darkest
    ("#5f2c48", "#7d4a12"),  # step-num gradient end
    ("#b25a85", "#c9852a"),  # shimmer stop
    ("#c9789f", "#e0954a"),  # shimmer stop
    ("#d9a8c2", "#a9d6c9"),  # orb-b -> soft mint
    ("#d3a2bc", "#f0c98a"),  # dark-band btn-3d gradient end (light)
    ("#efd0e0", "#f6deb0"),  # dark-band btn-3d gradient mid
    ("#fbeff5", "#fcf3e4"),  # dark-band btn-3d gradient start (lightest)
    ("#f0bed7", "#f2c98a"),  # dark-band shine/orb/stars light accent
    ("#f2cfe0", "#f5d9a0"),  # shimmer dark-band last stop
    ("#f8dfeb", "#fae7c4"),  # shimmer dark-band 3rd stop
    ("#dc9dbe", "#e8973e"),  # scroll-progress end stop
    ("#8a5573", "#8a5a1e"),  # dark-band btn shadow deep
    ("#e5c1d4", "#f2dfa0"),  # orb-c -> pale gold
    ("#f2d5e3", "#f6dcc0"),  # orb-a -> peach
    ("#faf2f6", "#fbf7ec"),  # bg
    ("#f3e0ea", "#eaf2ed"),  # bg-2 / accent-soft
    ("#f6f1ea", "#fbf7ec"),  # theme-color meta
    ("#fbf3f8", "#fcf8ef"),  # tile-cap text near-white
    ("#33222c", "#2e2115"),  # ink
    ("#2a1722", "#241a10"),  # cta-final bg gradient start
    ("#1f0f18", "#1a1109"),  # cta-final bg gradient end
    ("#1c0f16", "#19110a"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(217,114,15"),   # accent-deep alpha
    ("rgba(51,34,44", "rgba(46,33,21"),       # ink alpha
    ("rgba(125,52,87", "rgba(168,80,10"),     # dark mid alpha
    ("rgba(240,190,215", "rgba(242,201,138"), # light accent on dark-band alpha
    ("rgba(70,25,50", "rgba(74,38,10"),       # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(251,247,236"), # bg alpha (nav scrolled / dark-band ink)
    ("rgba(253,246,250", "rgba(253,249,240"), # surface glass alpha
    ("rgba(233,205,186", "rgba(242,203,150"), # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(120,190,170"), # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: quitar canal Booksy/Instagram inexistentes -> telefono real
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
TEL = "tel:+17867902025"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, TEL)
# tel: links no necesitan target=_blank/rel=noopener (eran para el booking externo)
c2 = h.count('href="tel:+17867902025" target="_blank" rel="noopener"')
assert c2 >= 10, c2
h = h.replace('href="tel:+17867902025" target="_blank" rel="noopener"', 'href="tel:+17867902025"')

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
YELP_URL = "https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, YELP_URL)
# El texto/icono "@_lashbloom" + icono IG se ajusta seccion por seccion mas abajo
# (evita copy incorrecto tipo "Instagram . See on Yelp" en footer/ubicacion).
print("GLOBALS done")

YELP_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>A Labor of Love · Dog Grooming Salon in Kendall, Miami FL | 4.6 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="A Labor of Love Dog Grooming Salon in Kendall, Miami FL: family-run since 2004, gentle with anxious and senior dogs, natural shampoos. 4.6 stars on Google. Call to book." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="A Labor of Love · Dog Grooming Salon in Kendall, Miami FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Family-run dog grooming since 2004. Gentle with anxious and senior dogs. 4.6 stars on Google. Call to book." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/gallery-01-fresh.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "A Labor of Love Dog Grooming Salon",
    "description": "Family-run dog grooming salon in Kendall, Miami FL, grooming dogs of all breeds and sizes since 2004, by appointment.",
    "address": { "@type": "PostalAddress", "streetAddress": "10864 SW 104th St", "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33176", "addressCountry": "US" },
    "telephone": "+1-786-790-2025",
    "sameAs": ["https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3", "https://www.google.com/maps/place/?q=place_id:ChIJM33al9zA2YgR52_G-UDiGIY"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "167", "bestRating": "5" },
    "openingHoursSpecification": { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "16:00" }
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
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(217,114,15,0.35)]" />',
    '<img src="assets/logo.jpg" alt="A Labor of Love Dog Grooming Salon" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(217,114,15,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">A Labor <span class="text-[color:var(--accent-deep)]">of Love</span></span>')

NAV_LINKS = [
    ('#experiencia', 'La Experiencia', 'The Experience', 'El Salón', 'The Salon'),
    ('#metodo', 'El Método', 'The Method', 'Cómo Funciona', 'How It Works'),
    ('#servicios', 'Servicios', 'Services', 'Servicios', 'Services'),
    ('#galeria', 'Galería', 'Gallery', 'Galería', 'Gallery'),
    ('#opiniones', 'Opiniones', 'Reviews', 'Opiniones', 'Reviews'),
    ('#ubicacion', 'Ubicación', 'Location', 'Ubicación', 'Location'),
]
for anchor, old_es, old_en, new_es, new_en in NAV_LINKS:
    rep_all(f'data-es="{old_es}" data-en="{old_en}">{old_es}</a>', f'data-es="{new_es}" data-en="{new_en}">{new_en}</a>', expect=2)

rep('<button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Cambiar idioma">EN</button>',
    '<button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Change language">EN</button>')

CALL_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'

rep('''<a href="tel:+17867902025" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>''',
    f'''<a href="tel:+17867902025" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          {CALL_ICON}
          <span data-es="Llamar ahora" data-en="Call now">Call now</span>
        </a>''')

rep('''<a href="tel:+17867902025" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>''',
    '''<a href="tel:+17867902025" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar ahora" data-en="Call now">Call now</a>''')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. PRELOADER
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">ALL</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">A Labor of Love</span>')
print("PRELOADER done")

# ---------------------------------------------------------------------------
# 8. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Miami, FL · Salón de Grooming Canino" data-en="Miami, FL · Dog Grooming Salon">Miami, FL · Dog Grooming Salon</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Cada baño y corte, con mucho cariño." data-en="Every groom, a labor of love.">Every groom, a labor of love.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Grooming con cariño," data-en="Gentle grooming,">Gentle grooming,</span><br /><span data-es="respaldado por 20 años de " data-en="backed by 20 years of ">backed by 20 years of </span><span class="text-shine" data-es="confianza" data-en="trust">trust</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Un salón de grooming familiar en Kendall, de confianza para perros ansiosos, mayores y difíciles desde 2004. Manejo paciente, champús naturales y orgánicos, y una pañoleta o moño de regalo en cada baño." data-en="A family-run grooming salon in Kendall trusted with anxious, senior and difficult dogs since 2004. Patient handling, natural and organic shampoos, and a free bandana or bow with every groom.">A family-run grooming salon in Kendall trusted with anxious, senior and difficult dogs since 2004. Patient handling, natural and organic shampoos, and a free bandana or bow with every groom.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.6 · 167 reseñas en Google" data-en="4.6 · 167 reviews on Google">4.6 · 167 reviews on Google</span>')
rep('''<a href="tel:+17867902025" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @_lashbloom
          </a>''',
    f'''<a href="tel:+17867902025" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llamar para reservar" data-en="Call to book">Call to book</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.google.com/maps?q=10864+SW+104th+St,+Miami,+FL+33176" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <span data-es="Cómo llegar" data-en="Get directions">Get directions</span>
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/gallery-01-fresh.jpg" alt="Freshly groomed puppy on the grooming table at A Labor of Love Dog Grooming Salon" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Familiar desde" data-en="Family-run since">Family-run since</p>
            <p class="font-display text-lg">2004</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="20+ años de grooming en Kendall" data-en="20+ years grooming in Kendall">20+ years grooming in Kendall</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 9. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="167">167</span> <span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Natural <span class="text-shine">&amp;</span> Organic</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Champús suaves para piel sensible" data-en="Gentle shampoos for sensitive skin">Gentle shampoos for sensitive skin</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">20+ <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Familiar en Kendall desde 2004" data-en="Family-run in Kendall since 2004">Family-run in Kendall since 2004</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Kendall</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">10864 SW 104th St</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 10. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Bath &amp; Haircut"),
    ("Hybrid Set", "Nail Trimming"),
    ("Volume Set", "Ear Cleaning"),
    ("Mega Volume", "Paw Treatments"),
    ("Bottom Lashes", "Teeth Cleaning"),
    ("West Palm Beach, FL", "Kendall, Miami FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 11. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-01-pom.jpg" alt="Pomeranian mix with a bow, freshly groomed on the table at A Labor of Love" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-02-walk.jpg" alt="Two freshly groomed small dogs on leashes outside A Labor of Love" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="El salón" data-en="The salon">The salon</p>')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Dos décadas de" data-en="Two decades of">Two decades of</span><br /><span class="text-shine" data-es="manos pacientes" data-en="gentle hands">gentle hands</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="A Labor of Love Dog Grooming Salon lleva bañando y cortando perros en la SW 104th Street de Kendall desde 2004: dos décadas con el mismo trato familiar, donde cada perro es parte de la familia y el equipo conoce a tu mascota por su nombre." data-en="A Labor of Love Dog Grooming Salon has been grooming dogs on SW 104th Street in Kendall since 2004: two decades of the same family-run approach, where every dog is treated like part of the family and the team knows your pet by name.">A Labor of Love Dog Grooming Salon has been grooming dogs on SW 104th Street in Kendall since 2004: two decades of the same family-run approach, where every dog is treated like part of the family and the team knows your pet by name.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Las reseñas siempre dicen lo mismo: paciencia con perros ansiosos, mayores y difíciles, una instalación realmente limpia, y un equipo que sigue exactamente tus instrucciones, con una pañoleta o moño de regalo al terminar." data-en="Reviews consistently point to the same thing: patience with anxious, senior and difficult dogs, a genuinely clean facility, and a team that follows exactly what you ask for, finished off with a free bandana or bow.">Reviews consistently point to the same thing: patience with anxious, senior and difficult dogs, a genuinely clean facility, and a team that follows exactly what you ask for, finished off with a free bandana or bow.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="167">167</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">2004</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Año de fundación" data-en="Est. year">Est. year</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(217,114,15,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/logo.jpg" alt="A Labor of Love Dog Grooming Salon" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(217,114,15,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">A Labor of Love · <span class="text-[color:var(--ink-40)]" data-es="Salón familiar" data-en="Family-run salon">Family-run salon</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 12. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, de principio" data-en="Your visit, start">Your visit, start</span> <span class="text-shine" data-es="a fin" data-en="to finish">to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Llama para reservar" data-en="Call to book">Call to book</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sin reservas en línea: llama al (786) 790-2025 y cuéntanos la raza, el pelaje y el temperamento de tu perro para buscar un horario." data-en="No online booking, just call (786) 790-2025 and tell us your dog's breed, coat and temperament so we can find a time that works.">No online booking, just call (786) 790-2025 and tell us your dog's breed, coat and temperament so we can find a time that works.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Recibimiento" data-en="Drop-off">Drop-off</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Trae a tu perro a la SW 104th Street en Kendall. El equipo evalúa temperamento y pelaje antes de empezar el baño." data-en="Bring your dog to 10864 SW 104th St in Kendall. The team gets a quick read on temperament and coat before the groom starts.">Bring your dog to 10864 SW 104th St in Kendall. The team gets a quick read on temperament and coat before the groom starts.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="El baño y corte" data-en="The groom">The groom</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Baño con champú natural y suave, corte según la raza, limpieza de oídos y corte de uñas, con la paciencia que necesitan los perros ansiosos y mayores." data-en="A bath with natural, mild shampoo, a breed-appropriate haircut, ear cleaning and a nail trim, handled with the patience anxious and senior dogs need.">A bath with natural, mild shampoo, a breed-appropriate haircut, ear cleaning and a nail trim, handled with the patience anxious and senior dogs need.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Recogida" data-en="Pickup">Pickup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu perro se va limpio, cómodo y con una pañoleta o moño de regalo, tal como lo han hecho las familias que regresan desde hace más de 20 años." data-en="Your dog goes home clean, comfortable and wearing a free bandana or bow, just like the families who have kept coming back for over 20 years.">Your dog goes home clean, comfortable and wearing a free bandana or bow, just like the families who have kept coming back for over 20 years.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 13. SERVICIOS (header + grid completo por regex + menu categorizado)
# ---------------------------------------------------------------------------
rep('data-es="Servicios" data-en="Services">Servicios</p>',
    'data-es="Servicios" data-en="Services">Services</p>', n=1)
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Grooming," data-en="Grooming,">Grooming,</span> <span class="text-shine" data-es="hecho con calma" data-en="done gently">done gently</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Sin lista de precios publicada: cada raza, pelaje y temperamento es distinto. Llama para una cotización real." data-en="No published price list, every breed, coat and temperament is different. Call for a real quote.">No published price list, every breed, coat and temperament is different. Call for a real quote.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Servicio completo" data-en="Full service">Full service</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Baño y Corte" data-en="Bath &amp; Haircut">Bath &amp; Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Baño completo con champú natural y suave, secado y corte según la raza, gentil incluso con perros ansiosos y mayores." data-en="A full bath with natural, mild shampoo, blow-dry and breed-appropriate haircut, gentle enough for anxious and senior dogs.">A full bath with natural, mild shampoo, blow-dry and breed-appropriate haircut, gentle enough for anxious and senior dogs.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Precio por consulta" data-en="Call for pricing">Call for pricing</p>
            <a href="tel:+17867902025" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(217,114,15,0.4); box-shadow: 0 18px 50px rgba(46,33,21,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo más solicitado" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Uñas y Oídos" data-en="Nail Trim &amp; Ear Cleaning">Nail Trim &amp; Ear Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Corte de uñas y limpieza de oídos, como parte del baño completo o como visita rápida por separado." data-en="Quick nail trims and ear cleaning, offered as part of a full groom or as a fast standalone visit.">Quick nail trims and ear cleaning, offered as part of a full groom or as a fast standalone visit.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Precio por consulta" data-en="Call for pricing">Call for pricing</p>
            <a href="tel:+17867902025" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar para reservar" data-en="Call to book">Call to book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cuidado extra" data-en="Comfort care">Comfort care</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Tratamiento de Patas" data-en="Paw Treatments">Paw Treatments</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Tratamiento de patas para mantener las almohadillas suaves y cómodas entre baños, ideal para perros mayores." data-en="A paw treatment to keep pads soft and comfortable between grooms, especially for older dogs.">A paw treatment to keep pads soft and comfortable between grooms, especially for older dogs.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Precio por consulta" data-en="Call for pricing">Call for pricing</p>
            <a href="tel:+17867902025" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Aliento fresco" data-en="Fresh breath">Fresh breath</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Limpieza Dental" data-en="Teeth Cleaning">Teeth Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Un extra de limpieza dental suave para mantener el aliento fresco entre visitas al veterinario." data-en="A gentle teeth cleaning add-on to keep breath fresh between vet visits.">A gentle teeth cleaning add-on to keep breath fresh between vet visits.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Precio por consulta" data-en="Call for pricing">Call for pricing</p>
            <a href="tel:+17867902025" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Grooming básico" data-en="Grooming basics">Grooming basics</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Baño" data-en="Bathing">Bathing</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Corte según la raza" data-en="Breed haircut">Breed haircut</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Limpieza de oídos" data-en="Ear cleaning">Ear cleaning</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Corte de uñas" data-en="Nail trimming">Nail trimming</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Extras y bienestar" data-en="Add-ons &amp; wellness">Add-ons &amp; wellness</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Tratamiento de patas" data-en="Paw treatments">Paw treatments</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Limpieza dental" data-en="Teeth cleaning">Teeth cleaning</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Por qué se quedan" data-en="Why owners stay">Why owners stay</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Champús naturales y orgánicos" data-en="Natural &amp; organic shampoos">Natural &amp; organic shampoos</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Pañoleta o moño de regalo" data-en="Free bandana or bow">Free bandana or bow</span></li>
            <li class="flex items-center gap-2"><span class="text-[color:var(--accent-mid)]">✦</span><span data-es="Paciencia con perros ansiosos y mayores" data-en="Gentle with anxious &amp; senior dogs">Gentle with anxious &amp; senior dogs</span></li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Sin lista de precios en línea. Llama al (786) 790-2025 para una cotización." data-en="No online price list. Call (786) 790-2025 for a quote.">No online price list. Call (786) 790-2025 for a quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 14. GALERIA (header + grid completo por regex)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Perros" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="dogs">dogs</span>')
rep('''<a href="https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @_lashbloom
        </a>''',
    f'''<a href="https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          {YELP_ICON}
          <span data-es="Ver en Yelp" data-en="See on Yelp">See on Yelp</span>
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Recién bañado y feliz" data-en="Fresh-groomed and happy">Fresh-groomed and happy</span><img src="assets/gallery-01-fresh.jpg" alt="Freshly groomed doodle puppy on the grooming table at A Labor of Love Dog Grooming Salon" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Lista para su moño" data-en="Bow-ready">Bow-ready</span><img src="assets/gallery-02-bow.jpg" alt="Yorkie with a bow, freshly groomed on the salon table" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Razas grandes bienvenidas" data-en="Big-breed pups welcome">Big-breed pups welcome</span><img src="assets/gallery-03-gsd.jpg" alt="German Shepherd puppy on the grooming table at A Labor of Love" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Esponjoso y cómodo" data-en="Fluffy and comfortable">Fluffy and comfortable</span><img src="assets/gallery-04-fluffy.jpg" alt="Fluffy grey and white dog freshly groomed on the salon table" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Acabado con tijera" data-en="Scissor-finished">Scissor-finished</span><img src="assets/gallery-05-scissor.jpg" alt="Papillon-type dog freshly groomed with scissors visible on the table" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Lista para recoger" data-en="Ready for pickup">Ready for pickup</span><img src="assets/gallery-06-pickup.jpg" alt="Small white puppy freshly groomed, ready for pickup" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="Lo que dicen" data-en="What pet">What pet</span> <span class="text-shine" data-es="sus clientas" data-en="parents say">parents say</span>')
rep('''<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>''',
    '''<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="4.6 de 5 · 167 reseñas en Google" data-en="4.6 out of 5 · 167 reviews on Google">4.6 out of 5 · 167 reviews on Google</span></p>''')

rep('''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''',
    '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The BEST! My dog is a little difficult, and they take such good care of him and do an excellent job!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jacqueline S.</span> <span class="text-[color:var(--ink-40)]">· Google via Birdeye</span></figcaption>''')
rep('''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''',
    '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I'm a loyal customer to Labor of Love since the day that they opened. They are always friendly, very professional."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Litsseny C.</span> <span class="text-[color:var(--ink-40)]">· Google via Birdeye</span></figcaption>''')
rep('''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>''',
    '''<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I've been having Freddy, my poodle, groomed at a Labor of Love Dog Grooming Salon for the past ten years."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Freddy's owner</span> <span class="text-[color:var(--ink-40)]">· Google via Birdeye</span></figcaption>''')
rep('''<a href="tel:+17867902025" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>''',
    '''<a href="https://www.google.com/maps/place/?q=place_id:ChIJM33al9zA2YgR52_G-UDiGIY" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver las reseñas en Google" data-en="Read reviews on Google">Read reviews on Google</a>''')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION
# ---------------------------------------------------------------------------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Kendall</span>')
rep('''<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,114,15,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''<p class="text-sm text-[color:var(--ink-60)] font-light">10864 SW 104th St, Miami, FL 33176</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,114,15,0.4)]" href="https://www.google.com/maps?q=10864+SW+104th+St,+Miami,+FL+33176" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Get directions</a>''')
rep('''<p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,114,15,0.4)]" href="tel:+17867902025" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="font-medium mb-1" data-es="Reservas" data-en="Appointments">Appointments</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa, de lunes a sábado de 9am a 4pm. Sin reservas en línea: llama para agendar." data-en="By appointment only, Monday through Saturday, 9am to 4pm. There is no online booking, call to schedule.">By appointment only, Monday through Saturday, 9am to 4pm. There is no online booking, call to schedule.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,114,15,0.4)]" href="tel:+17867902025" data-es="Llamar al (786) 790-2025" data-en="Call (786) 790-2025">Call (786) 790-2025</a>''')
rep('''<p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,114,15,0.4)]" href="https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3" target="_blank" rel="noopener">@_lashbloom</a>''',
    '''<p class="font-medium mb-1" data-es="Encuéntranos" data-en="Find us online">Find us online</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lee más reseñas reales en Yelp o revisa la ficha de Google antes de tu primera visita." data-en="Read more real reviews on Yelp or check the Google listing before your first visit.">Read more real reviews on Yelp or check the Google listing before your first visit.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(217,114,15,0.4)]" href="https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3" target="_blank" rel="noopener">Yelp &amp; Google reviews</a>''')
rep('''<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"''',
    '''<iframe title="Map: A Labor of Love Dog Grooming Salon, 10864 SW 104th St, Miami FL"
          src="https://www.google.com/maps?q=10864+SW+104th+St,+Miami,+FL+33176&output=embed"''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Cada baño y corte, con mucho cariño." data-en="Every groom, a labor of love.">Every groom, a labor of love.</p>')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '''<span data-es="El próximo baño de tu perro" data-en="Your dog's next groom">Your dog's next groom</span> <span class="text-shine" data-es="está a una llamada" data-en="is one call away">is one call away</span>''')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '''data-es="Con cita previa, de lunes a sábado. Llama y buscamos un horario que funcione para la raza, el pelaje y el temperamento de tu perro." data-en="By appointment, Monday through Saturday. Call and we will find a time that works for your dog's breed, coat and temperament.">By appointment, Monday through Saturday. Call and we will find a time that works for your dog's breed, coat and temperament.</p>''')
rep('''<a href="tel:+17867902025" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="tel:+17867902025" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar al (786) 790-2025" data-en="Call (786) 790-2025">Call (786) 790-2025</a>
        <a href="https://www.google.com/maps?q=10864+SW+104th+St,+Miami,+FL+33176" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Cómo llegar" data-en="Get directions">Get directions</a>''')
print("CTA done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">A Labor of Love</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(242,201,138,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>''',
    '''<img src="assets/logo.jpg" alt="A Labor of Love Dog Grooming Salon" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(242,201,138,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">A Labor of Love</span>''')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de grooming familiar en Kendall, Miami FL. Atención con cita previa." data-en="Family-run dog grooming salon in Kendall, Miami FL. By appointment only.">Family-run dog grooming salon in Kendall, Miami FL. By appointment only.</p>')
rep('''<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="tel:+17867902025" class="hover:text-[#f2c98a]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p>10864 SW 104th St, Miami, FL 33176</p>
        <p><a href="tel:+17867902025" class="hover:text-[#f2c98a]">(786) 790-2025</a></p>''')
rep('''<p><a href="https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3" target="_blank" rel="noopener" class="hover:text-[#f2c98a]">Instagram · @_lashbloom</a></p>''',
    '''<p><a href="https://www.yelp.com/biz/a-labor-of-love-dog-grooming-salon-miami-3" target="_blank" rel="noopener" class="hover:text-[#f2c98a]">Yelp</a></p>
        <p><a href="https://www.google.com/maps/place/?q=place_id:ChIJM33al9zA2YgR52_G-UDiGIY" target="_blank" rel="noopener" class="hover:text-[#f2c98a]" data-es="Reseñas en Google" data-en="Reviews on Google">Reviews on Google</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 A Labor of Love Dog Grooming Salon.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. BOOK-FLOAT
# ---------------------------------------------------------------------------
rep('''<a href="tel:+17867902025" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fbf7ec" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
  </a>''',
    '''<a href="tel:+17867902025" class="book-float" aria-label="Call to book a groom">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fbf7ec" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>''')
print("BOOKFLOAT done")

open(PATH, "w", encoding="utf-8").write(h)
print("BUILD DONE, len", len(h))
