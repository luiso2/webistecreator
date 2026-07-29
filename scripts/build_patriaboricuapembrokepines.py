import re
import shutil

SLUG = "patria-boricua-pembroke-pines"
PATH = f"output/{SLUG}/index.html"
shutil.copy("templates/dark-v2/index.html", PATH)
h = open(PATH, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:200]
    c = h.count(a)
    assert c == n, f"count {c} != expected {n} for " + a[:120]
    h = h.replace(a, b, n)


def rep_all(a, b, expect=None):
    global h
    c = h.count(a)
    assert c > 0, "NO ANCHOR: " + a[:200]
    if expect is not None:
        assert c == expect, f"count {c} != expected {expect} for " + a[:80]
    h = h.replace(a, b)


TEL = "tel:+19549996839"
IG_URL = "https://www.instagram.com/_patriaboricua/"
IG_HANDLE = "@_patriaboricua"
MAPS = "https://www.google.com/maps?q=Patria+Boricua,+10255+Pines+Blvd,+Pembroke+Pines,+FL+33026"
MAPS_EMBED = "https://www.google.com/maps?q=10255+Pines+Blvd,+Pembroke+Pines,+FL+33026&output=embed"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: gold pureartistry -> "bandera" (rojo boricua + ambar tropical)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#0f0b07", "#140d0c"),   # bg
    ("#171207", "#1e1310"),   # bg-2
    ("#f5efe3", "#f6ece2"),   # ink
    ("#d4a84b", "#b81f34"),   # accent-deep
    ("#b8934a", "#e0a23f"),   # accent-mid
    ("#241c0e", "#2b1a14"),   # accent-soft
    ("#f0dc9e", "#f2b34a"),   # shimmer light stop
    ("#9a7431", "#7a1522"),   # shimmer dark stop / step-num
    ("#e5c374", "#e0a23f"),   # shimmer/step-num light gold
    ("#e8c476", "#f0b25a"),   # btn-3d top
    ("#c9a04a", "#d9772f"),   # btn-3d mid
    ("#96742c", "#7a1f1f"),   # btn-3d bottom
    ("#6b5222", "#5c1420"),   # btn-3d/book-float sole shadow
    ("#e8cf96", "#eb8f6a"),   # dark-band shimmer light/accent bright
    ("#f8eed3", "#fbe4c9"),   # dark-band shimmer 30%
    ("#bfa060", "#c97850"),   # dark-band shimmer 52%
    ("#f0dcae", "#f2c98f"),   # dark-band shimmer 100%
    ("#e9c3ab", "#eb9a86"),   # dark-band stars
    ("#ecd9a8", "#f0b26a"),   # dark-band btn-3d mid
    ("#faf1dc", "#fce9d6"),   # dark-band btn-3d top
    ("#c9ab6b", "#d99a5a"),   # dark-band btn-3d bottom
    ("#8a744a", "#7a3a28"),   # dark-band btn-3d sole
    ("#0c0905", "#150d0c"),   # footer bg
    ("#100c05", "#150d0c"),   # cta-final gradient end
    ("#191307", "#241512"),   # cta-final gradient start
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(110,85,35,0.35)", "rgba(120,40,20,0.35)"),
    ("rgba(110,85,35,0.4)", "rgba(120,40,20,0.4)"),
    ("rgba(122,90,30,0.28)", "rgba(107,20,26,0.28)"),
    ("rgba(15,11,7,0.85)", "rgba(20,13,12,0.85)"),
    ("rgba(180,140,60,0.18)", "rgba(224,162,63,0.18)"),
    ("rgba(185,138,128,0.14)", "rgba(210,90,70,0.16)"),
    ("rgba(212,168,75,0.08)", "rgba(184,31,52,0.08)"),
    ("rgba(212,168,75,0.16)", "rgba(184,31,52,0.16)"),
    ("rgba(212,168,75,0.2)", "rgba(184,31,52,0.2)"),
    ("rgba(212,168,75,0.25)", "rgba(184,31,52,0.25)"),
    ("rgba(212,168,75,0.3)", "rgba(184,31,52,0.3)"),
    ("rgba(212,168,75,0.32)", "rgba(184,31,52,0.32)"),
    ("rgba(212,168,75,0.35)", "rgba(184,31,52,0.35)"),
    ("rgba(212,168,75,0.4)", "rgba(184,31,52,0.4)"),
    ("rgba(212,168,75,0.45)", "rgba(184,31,52,0.45)"),
    ("rgba(212,168,75,0.5)", "rgba(184,31,52,0.5)"),
    ("rgba(212,168,75,0.7)", "rgba(184,31,52,0.7)"),
    ("rgba(232,207,150,0.08)", "rgba(235,143,106,0.08)"),
    ("rgba(232,207,150,0.09)", "rgba(235,143,106,0.09)"),
    ("rgba(232,207,150,0.14)", "rgba(235,143,106,0.14)"),
    ("rgba(232,207,150,0.16)", "rgba(235,143,106,0.16)"),
    ("rgba(232,207,150,0.18)", "rgba(235,143,106,0.18)"),
    ("rgba(232,207,150,0.35)", "rgba(235,143,106,0.35)"),
    ("rgba(232,207,150,0.4)", "rgba(235,143,106,0.4)"),
    ("rgba(232,207,150,0.7)", "rgba(235,143,106,0.7)"),
    ("rgba(232,210,160,0.16)", "rgba(235,143,106,0.16)"),
    ("rgba(245,239,227,0.42)", "rgba(246,236,226,0.42)"),
    ("rgba(245,239,227,0.45)", "rgba(246,236,226,0.45)"),
    ("rgba(245,239,227,0.62)", "rgba(246,236,226,0.62)"),
    ("rgba(245,239,227,0.65)", "rgba(246,236,226,0.65)"),
    ("rgba(54,42,38,0.14)", "rgba(46,20,18,0.16)"),
    ("rgba(80,58,18,0.4)", "rgba(100,30,15,0.4)"),
    ("rgba(80,58,18,0.45)", "rgba(100,30,15,0.45)"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: reemplazar TODAS las URLs de Booksy por tel:/maps, IG url/handle
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, TEL)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, IG_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, IG_HANDLE)
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, theme-color, JSON-LD
# ---------------------------------------------------------------------------
rep('<meta name="theme-color" content="#140d0c" />',
    '<meta name="theme-color" content="#140d0c" />')  # ya migrado por la paleta; no-op de verificacion
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Patria Boricua · Food Truck Puertorriqueño en Pembroke Pines, FL | 4.9 en Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Patria Boricua, Pembroke Pines FL: mofongo, alcapurrias, pasteles y pinchos 100% puertorriqueños. 4.9 estrellas en 265 reseñas de Google. Abierto viernes a domingo." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Patria Boricua · Food Truck Puertorriqueño en Pembroke Pines, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Mofongo, alcapurrias, pasteles y pinchos boricuas. 4.9 en Google con 265 reseñas. Viernes a domingo." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-mofongo.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/logo.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FoodEstablishment",
    "name": "Patria Boricua",
    "description": "Food truck puertorriqueño instalado en Pembroke Pines, FL: mofongo, alcapurrias, pasteles, pinchos y chicharrones, cocinados por el chef Orlando con receta boricua tradicional.",
    "servesCuisine": "Puerto Rican",
    "address": { "@type": "PostalAddress", "streetAddress": "10255 Pines Blvd", "addressLocality": "Pembroke Pines", "addressRegion": "FL", "postalCode": "33026", "addressCountry": "US" },
    "telephone": "+19549996839",
    "priceRange": "$$",
    "sameAs": ["https://www.instagram.com/_patriaboricua/", "https://www.facebook.com/p/Patria-boricua-100071431339204/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "265", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "17:00", "closes": "23:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "14:00", "closes": "23:30" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "14:00", "closes": "21:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Menú de Patria Boricua", "itemListElement": [
      { "@type": "Offer", "price": "22.00", "priceCurrency": "USD", "itemOffered": { "@type": "MenuItem", "name": "El Jibarito" } },
      { "@type": "Offer", "price": "21.00", "priceCurrency": "USD", "itemOffered": { "@type": "MenuItem", "name": "Mofongo de Pollo" } },
      { "@type": "Offer", "price": "35.75", "priceCurrency": "USD", "itemOffered": { "@type": "MenuItem", "name": "Picadera" } },
      { "@type": "Offer", "price": "13.50", "priceCurrency": "USD", "itemOffered": { "@type": "MenuItem", "name": "Chicharrones de Cerdo" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio ES -> html lang=es, default de applyLang = es
# ---------------------------------------------------------------------------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")
print("IDIOMA done")

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,31,52,0.35)]" />',
    '<img src="assets/logo.jpg" alt="Patria Boricua" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,31,52,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Patria <span class="text-[color:var(--accent-deep)]">Boricua</span></span>')
rep('<a class="nav-link" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>',
    '<a class="nav-link" href="#metodo" data-es="Cómo Pedir" data-en="How to Order">Cómo Pedir</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="El Método" data-en="The Method">El Método</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#metodo" data-es="Cómo Pedir" data-en="How to Order">Cómo Pedir</a>')
rep('<a class="nav-link" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>',
    '<a class="nav-link" href="#servicios" data-es="Menú" data-en="Menu">Menú</a>')
rep('<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Servicios" data-en="Services">Servicios</a>',
    '<a class="py-3 px-3 border-b border-[color:var(--accent-ghost)]" href="#servicios" data-es="Menú" data-en="Menu">Menú</a>')
rep('''<button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Cambiar idioma">EN</button>
        <a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>''',
    '''<button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs" aria-label="Cambiar idioma">EN</button>
        <a href="''' + TEL + '''" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <span data-es="Llamar para pedir" data-en="Call to order">Llamar para pedir</span>
        </a>''')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llamar para pedir" data-en="Call to order">Llamar para pedir</a>''')
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">PB</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Patria Boricua</span>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Pembroke Pines, FL · Food Truck Boricua" data-en="Pembroke Pines, FL · Puerto Rican Food Truck">Pembroke Pines, FL · Food Truck Boricua</p>')
rep('<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Cocinando con la bendición de Dios." data-en="Cooking with God&#39;s blessing.">Cocinando con la bendición de Dios.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Sabor de Puerto Rico," data-en="The taste of Puerto Rico,">Sabor de Puerto Rico,</span><br /><span data-es="hecho con " data-en="made with ">hecho con </span><span class="text-shine" data-es="cariño boricua" data-en="boricua love">cariño boricua</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Food truck 100% puertorriqueño en Pembroke Pines: mofongo, alcapurrias, pasteles y pinchos hechos con la receta de siempre. Abierto viernes, sábado y domingo, con 4.9 estrellas en 265 reseñas de Google." data-en="A 100% Puerto Rican food truck in Pembroke Pines: mofongo, alcapurrias, pasteles and pinchos made the old-fashioned way. Open Friday through Sunday, with a 4.9 rating across 265 Google reviews.">Food truck 100% puertorriqueño en Pembroke Pines: mofongo, alcapurrias, pasteles y pinchos hechos con la receta de siempre. Abierto viernes, sábado y domingo, con 4.9 estrellas en 265 reseñas de Google.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.9 · 265 reseñas en Google" data-en="4.9 · 265 reviews on Google">4.9 · 265 reseñas en Google</span>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + IG_HANDLE + '''
          </a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llamar para pedir" data-en="Call to order">Llamar para pedir</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-mofongo.jpg" alt="Mofongo con chicharrón de cerdo servido en Patria Boricua, Pembroke Pines" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Más pedido" data-en="Most ordered">Más pedido</p>
            <p class="font-display text-lg">Mofongo de Pollo</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$21.00 · Plato insignia" data-en="$21.00 · Signature dish">$21.00 · Plato insignia</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="265">265</span> <span data-es="reseñas en Google" data-en="reviews on Google">reseñas en Google</span></p></div>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Mofongo <span class="text-shine">&amp;</span> Pernil</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Alcapurrias · Pasteles · Pinchos" data-en="Alcapurrias · Pasteles · Pinchos">Alcapurrias · Pasteles · Pinchos</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">Catering <span class="text-shine">&amp;</span> Eventos</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Empresariales · Cumpleaños" data-en="Corporate · Birthdays">Empresariales · Cumpleaños</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Pembroke Pines</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">10255 Pines Blvd</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Silk Press", "Mofongo"),
    ("Loc Retwist", "Alcapurrias"),
    ("Knotless Braids", "Pasteles"),
    ("K-Tip Extensions", "Pinchos"),
    ("Keratin", "Chicharrones"),
    ("Orlando, FL", "Pembroke Pines, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-01-picadera.jpg" alt="Picadera de Patria Boricua: alcapurrias, tostones, chicharrones y empanadillas para compartir" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-02-menu-coco.jpg" alt="Preparando una bebida frente al menú de neón del food truck Patria Boricua" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Comida boricua," data-en="Puerto Rican food,">Puerto Rican food,</span><br /><span class="text-shine" data-es="hecha con bendición" data-en="made with blessing">made with blessing</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Patria Boricua es el food truck de Orlando, chef profesional que cocina la comida típica boricua tal como la aprendió en casa. Está instalado de forma fija en el parqueo de una gasolinera sobre Pines Blvd, con mesas cubiertas al aire libre donde hasta se juega dominó mientras se espera el plato." data-en="Patria Boricua is Orlando&#39;s food truck: a professional chef cooking classic Puerto Rican food exactly the way he grew up eating it. It sits parked in a gas station lot on Pines Blvd, with covered outdoor seating where regulars even play dominoes while they wait for their plate.">Patria Boricua es el food truck de Orlando, chef profesional que cocina la comida típica boricua tal como la aprendió en casa. Está instalado de forma fija en el parqueo de una gasolinera sobre Pines Blvd, con mesas cubiertas al aire libre donde hasta se juega dominó mientras se espera el plato.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="El resultado: 4.9 estrellas casi perfectas en 265 reseñas de Google, porciones generosas y una espera que, según sus clientes, siempre vale la pena." data-en="The result: a near-perfect 4.9 across 265 Google reviews, generous portions, and a wait that customers say is always worth it.">El resultado: 4.9 estrellas casi perfectas en 265 reseñas de Google, porciones generosas y una espera que, según sus clientes, siempre vale la pena.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="265">265</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">100%</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Boricua" data-en="Puerto Rican">Boricua</p></div>''')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,31,52,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>''',
    '''<img src="assets/logo.jpg" alt="Patria Boricua" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(184,31,52,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Orlando · <span class="text-[color:var(--ink-40)]" data-es="Chef y dueño" data-en="Chef &amp; owner">Chef y dueño</span></span>''')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. COMO PEDIR (antes "El Método")
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Así se pide aquí" data-en="How to order here">Así se pide aquí</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se" data-en="How it">How it</span> <span class="text-shine" data-es="pide y se disfruta" data-en="works here">works here</span></h2>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Ven o llama" data-en="Come or call">Ven o llama</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nos encuentras en el parqueo de la gasolinera de Pines Blvd, o llamas al (954) 999-6839 para preguntar el menú del día." data-en="Find us in the gas station parking lot on Pines Blvd, or call (954) 999-6839 to ask about today&#39;s menu.">Nos encuentras en el parqueo de la gasolinera de Pines Blvd, o llamas al (954) 999-6839 para preguntar el menú del día.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Elige tu plato" data-en="Choose your dish">Elige tu plato</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del mofongo con chicharrón a las alcapurrias y pasteles: pides en la ventanilla, para comer ahí en las mesas cubiertas o para llevar." data-en="From mofongo with chicharrón to alcapurrias and pasteles: order at the window, to eat at the covered tables or to go.">Del mofongo con chicharrón a las alcapurrias y pasteles: pides en la ventanilla, para comer ahí en las mesas cubiertas o para llevar.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Espera con buena compañía" data-en="Wait in good company">Espera con buena compañía</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Los fines de semana hay cola, pero también hay dominó y buena música mientras Orlando cocina tu plato desde cero." data-en="Weekends get busy, but there is dominoes and good music while Orlando cooks your plate from scratch.">Los fines de semana hay cola, pero también hay dominó y buena música mientras Orlando cocina tu plato desde cero.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Disfruta o pide para llevar" data-en="Enjoy it or order to-go">Disfruta o pide para llevar</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el plato recién hecho, o lo pides para catering en tu próximo evento familiar o de oficina." data-en="Leave with a freshly made plate, or book it for catering at your next family or office event.">Sales con el plato recién hecho, o lo pides para catering en tu próximo evento familiar o de oficina.</p>''')
print("COMO PEDIR done")

# ---------------------------------------------------------------------------
# 12. MENU (antes "Servicios"): header + grid de destacados + categorias
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Nuestro" data-en="Our">Nuestro</span> <span class="text-shine">menú</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios reales del menú de pedidos de Patria Boricua. Llama para confirmar disponibilidad del día." data-en="Real prices from Patria Boricua&#39;s order menu. Call to confirm the day&#39;s availability.">Precios reales del menú de pedidos de Patria Boricua. Llama para confirmar disponibilidad del día.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "menu grid not found"

NEW_MENU_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Más pedido" data-en="Most ordered">Más pedido</p>
          <h3 class="font-display text-2xl leading-snug mb-3">El Jibarito</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Carne de cerdo o pollo prensada entre dos tostones de plátano verde en lugar de pan, al estilo boricua." data-en="Pulled pork or chicken pressed between two fried green plantains instead of bread, Puerto Rican jíbaro style.">Carne de cerdo o pollo prensada entre dos tostones de plátano verde en lugar de pan, al estilo boricua.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$22.00</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir" data-en="Order">Pedir</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(184,31,52,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Plato insignia" data-en="Signature dish">Plato insignia</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Mofongo de Pollo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Plátano verde majado con pollo, la receta que nuestros clientes describen como &quot;to die for&quot;." data-en="Mashed green plantain with chicken, the dish our customers describe as &quot;to die for&quot;.">Plátano verde majado con pollo, la receta que nuestros clientes describen como &quot;to die for&quot;.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$21.00</p></div>
            <a href="''' + TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir" data-en="Order">Pedir</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Para compartir" data-en="To share">Para compartir</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Picadera</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Sorullitos, alcapurrias, chicharrones de cerdo y empanadillas, todo junto para compartir en la mesa." data-en="Sorullitos, alcapurrias, pork cracklings and empanadillas, all together to share at the table.">Sorullitos, alcapurrias, chicharrones de cerdo y empanadillas, todo junto para compartir en la mesa.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$35.75</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir" data-en="Order">Pedir</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Fritura fresca" data-en="Freshly fried">Fritura fresca</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Chicharrones de Cerdo" data-en="Pork Cracklings">Chicharrones de Cerdo</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Chicharrón de cerdo recién frito, crocante por fuera y jugoso por dentro." data-en="Freshly fried pork cracklings, crisp outside and juicy inside.">Chicharrón de cerdo recién frito, crocante por fuera y jugoso por dentro.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$13.50</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Pedir" data-en="Order">Pedir</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Pa&#39; Empezar" data-en="Appetizers">Pa&#39; Empezar</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-2"><span data-es="Sorullitos de Maíz Rellenos de Queso (x3)" data-en="Corn Sorullitos Stuffed with Cheese (x3)">Sorullitos de Maíz Rellenos de Queso (x3)</span><span class="text-[color:var(--ink-40)]">$11.00</span></li>
            <li class="flex items-center justify-between gap-2"><span>Alcapurria</span><span class="text-[color:var(--ink-40)]">$4.75</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Empanadilla de Pizza" data-en="Pizza Empanadilla">Empanadilla de Pizza</span><span class="text-[color:var(--ink-40)]">$4.00</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Queso Frito con Salsa de Guayaba" data-en="Fried Cheese with Guava Sauce">Queso Frito con Salsa de Guayaba</span><span class="text-[color:var(--ink-40)]">$10.50</span></li>
            <li class="flex items-center justify-between gap-2"><span>Pasteles (2)</span><span class="text-[color:var(--ink-40)]">$11.00</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Pincho de Pollo o Cerdo" data-en="Chicken or Pork Skewer">Pincho de Pollo o Cerdo</span><span class="text-[color:var(--ink-40)]">$6.50</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Empanadilla de Carne, Pollo o Camarones con Queso" data-en="Beef, Chicken or Shrimp Empanadilla with Cheese">Empanadilla de Carne, Pollo o Camarones con Queso</span><span class="text-[color:var(--ink-40)]">$5.00-$6.00</span></li>
            <li class="flex items-center justify-between gap-2"><span>Cheesedog</span><span class="text-[color:var(--ink-40)]">$3.50</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4">Mofongos</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-2"><span data-es="Mofongo de Chicharrones de Pollo" data-en="Mofongo with Chicken Cracklings">Mofongo de Chicharrones de Pollo</span><span class="text-[color:var(--ink-40)]">$18.50</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Mofongo de Pescado" data-en="Mofongo with Fish">Mofongo de Pescado</span><span class="text-[color:var(--ink-40)]">$19.00</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Mofongo de Carne Frita" data-en="Mofongo with Fried Pork">Mofongo de Carne Frita</span><span class="text-[color:var(--ink-40)]">$21.50</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Mofongo de Chicharrones de Cerdo" data-en="Mofongo with Pork Cracklings">Mofongo de Chicharrones de Cerdo</span><span class="text-[color:var(--ink-40)]">$22.00</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Mofongo de Churrasco (Angus Steak)" data-en="Mofongo with Churrasco (Angus Steak)">Mofongo de Churrasco (Angus Steak)</span><span class="text-[color:var(--ink-40)]">$28.50</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="También en la Parrilla" data-en="Also on the Menu">También en la Parrilla</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-2"><span>Pernil</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Arroz con Gandules" data-en="Rice with Pigeon Peas">Arroz con Gandules</span></li>
            <li class="flex items-center justify-between gap-2"><span>Bacalaítos</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Tostones Rellenos" data-en="Stuffed Tostones">Tostones Rellenos</span></li>
            <li class="flex items-center justify-between gap-2"><span>Coquito</span></li>
            <li class="flex items-center justify-between gap-2"><span>Tembleque</span></li>
            <li class="flex items-center justify-between gap-2"><span data-es="Piña Colada" data-en="Piña Colada">Piña Colada</span></li>
          </ul>
          <p class="text-xs text-[color:var(--ink-40)] font-light mt-4" data-es="Disponibilidad y precio varían por fin de semana. Pregunta en el food truck." data-en="Availability and price vary by weekend. Ask us at the truck.">Disponibilidad y precio varían por fin de semana. Pregunta en el food truck.</p>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_MENU_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Catering para eventos empresariales y cumpleaños. Llama para el menú completo y disponibilidad del fin de semana." data-en="Catering for corporate events and birthdays. Call for the full menu and weekend availability.">Catering para eventos empresariales y cumpleaños. Llama para el menú completo y disponibilidad del fin de semana.</span></p>')
print("MENU done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex, 3 fotos reales)
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Comida" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="food">food</span>')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Pasteles en hoja" data-en="Banana-leaf pasteles">Pasteles en hoja</span><img src="assets/gallery-01-pasteles.jpg" alt="Pasteles boricuas envueltos en hoja, servidos con salsa en Patria Boricua" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Pescado frito" data-en="Fried fish">Pescado frito</span><img src="assets/gallery-02-pescado-frito.jpg" alt="Filetes de pescado frito, recien hechos en Patria Boricua" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Mofongo con chicharrón" data-en="Mofongo with chicharrón">Mofongo con chicharrón</span><img src="assets/gallery-03-mofongo-chicharron.jpg" alt="Mofongo con chicharrón de cerdo, plato insignia de Patria Boricua" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="Lo que dicen" data-en="What our">Lo que dicen</span> <span class="text-shine" data-es="nuestros clientes" data-en="customers say">nuestros clientes</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 265 reseñas verificadas en Google" data-en="4.9 out of 5 · 265 verified reviews on Google">4.9 de 5 · 265 reseñas verificadas en Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Wepaaaaa… La comida está espectacular, la comida única más rica que comida aquí en Miami y tremendo servicio. Que Dios los bendiga a todos. Un aplauso para el chef."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sharon P.</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Esta gente es un 10/10. No pensé que iba recibir tan buen servicio, y que la comida estuviera al 100. Tal cual la quería. Estoy demasiado satisfecha, espero volver! El Mofongo estaba en su punto! Vayan, no se van a arrepentir."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Yavialys Saldana</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"We tried the Bifongo with Churrasco and it was delicious. We also ordered some sorullitos and taste just like the ones in Puerto Rico! I definitely recommend Patria Boricua"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">E. Fuentes</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>''')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="' + MAPS + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 265 reseñas en Google" data-en="Read all 265 reviews on Google">Leer las 265 reseñas en Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Pembroke Pines</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,31,52,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">10255 Pines Blvd, Pembroke Pines, FL 33026 <span data-es="(parqueo de la gasolinera)" data-en="(gas station parking lot)">(parqueo de la gasolinera)</span></p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,31,52,0.4)]" href="''' + MAPS + '''" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,31,52,0.4)]" href="''' + TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Horario</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Viernes 5:00pm-11:30pm · Sábado 2:00pm-11:30pm · Domingo 2:00pm-9:00pm. Cerrado lunes a jueves." data-en="Friday 5:00pm-11:30pm · Saturday 2:00pm-11:30pm · Sunday 2:00pm-9:00pm. Closed Monday through Thursday.">Viernes 5:00pm-11:30pm · Sábado 2:00pm-11:30pm · Domingo 2:00pm-9:00pm. Cerrado lunes a jueves.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,31,52,0.4)]" href="''' + TEL + '''" data-es="Llamar para confirmar" data-en="Call to confirm">Llamar para confirmar</a>
            </div>''')
rep('''<p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,31,52,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">''' + IG_HANDLE + '''</a>''',
    '''<p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los platos más recientes y los especiales del fin de semana antes de venir." data-en="See the latest dishes and weekend specials before you visit.">Mira los platos más recientes y los especiales del fin de semana antes de venir.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(184,31,52,0.4)]" href="''' + IG_URL + '''" target="_blank" rel="noopener">''' + IG_HANDLE + '''</a>''')
rep('''<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"
          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"''',
    '''<iframe title="Mapa: Patria Boricua, 10255 Pines Blvd, Pembroke Pines FL"
          src="''' + MAPS_EMBED + '''"''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Cocinando con la bendición de Dios." data-en="Cooking with God&#39;s blessing.">Cocinando con la bendición de Dios.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próximo plato" data-en="Your next">Your next</span> <span class="text-shine" data-es="boricua te espera" data-en="Puerto Rican plate is waiting">Puerto Rican plate is waiting</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Llama para pedir, ven al food truck en Pines Blvd, o síguenos para saber los especiales del fin de semana." data-en="Call to order, visit the truck on Pines Blvd, or follow us to catch the weekend specials.">Llama para pedir, ven al food truck en Pines Blvd, o síguenos para saber los especiales del fin de semana.</p>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Llamar ahora" data-en="Call now">Llamar ahora</a>
        <a href="''' + MAPS + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Ver ubicación" data-en="Get directions">Ver ubicación</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">Patria Boricua</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(235,143,106,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>''',
    '''<img src="assets/logo.jpg" alt="Patria Boricua" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(235,143,106,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Patria Boricua</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Food truck puertorriqueño en Pembroke Pines, FL. Viernes a domingo." data-en="Puerto Rican food truck in Pembroke Pines, FL. Friday through Sunday.">Food truck puertorriqueño en Pembroke Pines, FL. Viernes a domingo.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
        <p><a href="''' + TEL + '''" target="_blank" rel="noopener" class="hover:text-[#eb9a86]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>10255 Pines Blvd, Pembroke Pines, FL 33026</p>
        <p><a href="''' + TEL + '''" class="hover:text-[#eb9a86]">(954) 999-6839</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#eb9a86]">Instagram · ''' + IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#eb9a86]">Instagram · ''' + IG_HANDLE + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Patria Boricua.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante de pedido (antes book-float a Booksy)
# ---------------------------------------------------------------------------
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>''',
    '''<a href="''' + TEL + '''" class="book-float" aria-label="Llamar para pedir">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>''')
print("BOOK-FLOAT done")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("WRITE done ->", PATH)
