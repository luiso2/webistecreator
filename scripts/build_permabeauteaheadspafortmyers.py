import re
import shutil

SLUG = "permabeautea-head-spa-fort-myers"
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


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta (SIEMPRE dorado)
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: gold dark original (Pure Artistry) -> "tsuki" (luna) copper-rose
#    sobre indigo profundo. Rotacion de hue matematica preservando
#    luminosidad/saturacion: familia acento (oro ~40deg -> cobre-terracota
#    ~14deg, delta -26), familia fondo (marron-negro casi neutro -> indigo
#    profundo hue 258deg, +0.12 saturacion) para el ambiente nocturno/luna
#    real del negocio (luz neon morada, arco de cobre, decoracion de luna,
#    ver fotos reales bk-1/gg-2/gg-6). Distinta de mizu/amani/mare/alea/pausa
#    (DESIGN.md) y de coral fairy, caramelo, esmeralda, teal acero,
#    violeta dark, rosa dark, gold dark original (SKELETONS-V2.md).
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    # familia acento (oro -> cobre-terracota, delta hue -26)
    ("d4a84b", "d46d4b"),
    ("b8934a", "b8634a"),
    ("e9c3ab", "e9abae"),
    ("8a744a", "8a584a"),
    ("f0dc9e", "f0b89e"),
    ("e8cf96", "e8ab96"),
    ("e8c476", "e89376"),
    ("e5c374", "e59274"),
    ("c9a04a", "c9694a"),
    ("9a7431", "9a4631"),
    ("96742c", "96462c"),
    ("fbf6ea", "fbefea"),
    ("faf1dc", "fae4dc"),
    ("f8eed3", "f8ded3"),
    ("f0dcae", "f0bfae"),
    ("ecd9a8", "ecbca8"),
    ("c9ab6b", "c9826b"),
    ("bfa060", "bf7760"),
    ("6b5222", "6b3222"),
    ("1c1408", "1c0b08"),
    # familia fondo (casi-negro marron -> indigo profundo, hue 258deg)
    ("0f0b07", "090610"),
    ("171207", "0b0519"),
    ("100c05", "080411"),
    ("191307", "0c051b"),
    ("0c0905", "07040d"),
    ("241c0e", "130b27"),
]
for old, new in HEX_PALETTE:
    old_hex, new_hex = "#" + old, "#" + new
    c = h.count(old_hex)
    assert c > 0, "hex not found: " + old_hex
    h = h.replace(old_hex, new_hex)

RGBA_PALETTE = [
    ("rgba(212,168,75", "rgba(212,109,75"),    # accent-deep alpha (accent-ghost, borders, glows)
    ("rgba(232,207,150", "rgba(232,171,150"),  # dark-band accent tint
    ("rgba(80,58,18", "rgba(80,31,18"),        # btn-3d darkest inset shadow
    ("rgba(110,85,35", "rgba(110,52,35"),      # dark-band btn shadow
    ("rgba(232,210,160", "rgba(232,179,160"),  # accent-ghost variant (dark-band)
    ("rgba(185,138,128", "rgba(185,128,143"),  # dark-band orb-b
    ("rgba(180,140,60", "rgba(180,88,60"),     # orb-c pale
    ("rgba(122,90,30", "rgba(122,50,30"),      # orb-b
    ("rgba(15,11,7", "rgba(9,6,16"),           # bg alpha (nav scrolled)
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: booking = GlossGenius (no hay Booksy), IG real
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando"
NEW_BOOK = "https://permabeauteahs.glossgenius.com"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_BOOK)

OLD_IG_URL = "https://www.instagram.com/pure.artistrysk/"
NEW_IG_URL = "https://www.instagram.com/permabeautea.hs/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@pure.artistrysk"
NEW_IG_HANDLE = "@permabeautea.hs"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_TEL = "tel:+12392337569"
NEW_MAPS = "https://www.google.com/maps?q=2741+1st+St,+Fort+Myers,+FL+33916"

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>PermabeauTea Head Spa · Japanese Head Spa in Fort Myers, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="PermabeauTea Head Spa, Fort Myers FL: Japanese-rooted scalp massage, gua sha lifting facial, nourishing hair treatments and a 21-herb foot detox, finished with homemade tea. 5.0 stars, 24 Google reviews. Book online." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="PermabeauTea Head Spa · Japanese Head Spa in Fort Myers, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Japanese-rooted scalp massage, gua sha facial and herbal foot detox, finished with tea. 5.0 on Google with 24 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-mist.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-mist.jpg" />')
rep('<meta name="theme-color" content="#090610" />',
    '<meta name="theme-color" content="#0b0519" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "PermabeauTea Head Spa",
    "description": "Japanese-rooted head spa in Fort Myers, FL: scalp massage, hair nourishing treatments, gua sha lifting facial, back scrub and a 21-herb foot detox, finished with homemade tea.",
    "address": { "@type": "PostalAddress", "streetAddress": "2741 1st St, Unit 110", "addressLocality": "Fort Myers", "addressRegion": "FL", "postalCode": "33916", "addressCountry": "US" },
    "telephone": "+1-239-233-7569",
    "email": "permabeauteahs@gmail.com",
    "sameAs": ["https://permabeauteahs.glossgenius.com", "https://www.instagram.com/permabeautea.hs/", "https://facebook.com/61559729461625"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "24", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Thursday"], "opens": "08:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday", "Friday", "Saturday"], "opens": "09:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "10:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Head spa services", "itemListElement": [
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Head Spa - Xpress" } },
      { "@type": "Offer", "price": "125", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Nourishing Treatments" } },
      { "@type": "Offer", "price": "175", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Refreshing Head Spa" } },
      { "@type": "Offer", "price": "225", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Head Spa - The Experiences" } },
      { "@type": "Offer", "price": "295", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Invitation to Dream" } },
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Back Scrub (Add-on)" } },
      { "@type": "Offer", "price": "95", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Foot Spa - Herbal Detox" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN -> se queda en EN (default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. NAV (sin logo real -> monograma de texto en vez de <img>)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,109,75,0.35)]" />',
    '<span class="w-10 h-10 rounded-full ring-1 ring-[rgba(212,109,75,0.35)] bg-[rgba(212,109,75,0.12)] flex items-center justify-center font-display text-sm tracking-wide text-[color:var(--accent-deep)]" aria-hidden="true">PT</span>')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Permabeau<span class="text-[color:var(--accent-deep)]">Tea</span></span>')
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">PT</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">PermabeauTea</span>')
print("NAV done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Fort Myers, FL · Japanese Head Spa" data-en="Fort Myers, FL · Japanese Head Spa">Fort Myers, FL · Japanese Head Spa</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Slow down. Steep in it." data-en="Slow down. Steep in it.">Slow down. Steep in it.</p>')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Japanese head spa," data-en="Japanese head spa,">Japanese head spa,</span><br /><span data-es="steeped in " data-en="steeped in ">steeped in </span><span class="text-shine" data-es="stillness" data-en="stillness">stillness</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Scalp massage, gua sha lifting facial, nourishing hair treatments and a 21-herb foot detox in a candlelit, moonlit suite in Fort Myers. Every ritual, from the Xpress to the Invitation to Dream, ends the same way: your own cup of homemade tea." data-en="Scalp massage, gua sha lifting facial, nourishing hair treatments and a 21-herb foot detox in a candlelit, moonlit suite in Fort Myers. Every ritual, from the Xpress to the Invitation to Dream, ends the same way: your own cup of homemade tea.">Scalp massage, gua sha lifting facial, nourishing hair treatments and a 21-herb foot detox in a candlelit, moonlit suite in Fort Myers. Every ritual, from the Xpress to the Invitation to Dream, ends the same way: your own cup of homemade tea.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="5.0 · 24 reviews on Google" data-en="5.0 · 24 reviews on Google">5.0 · 24 reviews on Google</span>')
rep('''<a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Book on GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-mist.jpg" alt="Warm herbal steam ritual under the copper misting arch at PermabeauTea Head Spa" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Book online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Head Spa - Xpress</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$90 · 55 min" data-en="$90 · 55 min">$90 · 55 min</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="24">24</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<p class="font-display text-2xl">Scalp <span class="text-shine">&amp;</span> Gua Sha</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Massage · Detox · Ritual" data-en="Massage · Detox · Ritual">Massage · Detox · Ritual</p></div>')
rep('<p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<p class="font-display text-2xl">From <span class="text-shine">$90</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Head Spa - Xpress, 55 min" data-en="Head Spa - Xpress, 55 min">Head Spa - Xpress, 55 min</p></div>')
rep('<p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<p class="font-display text-2xl">Fort Myers</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">2741 1st St</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Silk Press", "Head Spa Xpress"),
    ("Loc Retwist", "Nourishing Treatment"),
    ("Knotless Braids", "Refreshing Head Spa"),
    ("K-Tip Extensions", "Gua Sha Facial"),
    ("Keratin", "Herbal Foot Detox"),
    ("Orlando, FL", "Fort Myers, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-room.jpg" alt="The candlelit PermabeauTea Head Spa treatment suite, with its crescent moon light and reading nook" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-moon.jpg" alt="The copper misting arch glowing under the moon and stars projection at PermabeauTea Head Spa" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="One ritual," data-en="One ritual,">One ritual,</span><br /><span class="text-shine" data-es="rooted in stillness" data-en="rooted in stillness">rooted in stillness</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="PermabeauTea Head Spa is a Japanese-rooted head spa suite in Fort Myers: scalp massage, hair nourishing treatments, gua sha lifting facial and back scrub, plus a foot detox soak with 21 kinds of herbs. Every visit happens one-on-one, by appointment, under soft candlelight and a projected moon and stars." data-en="PermabeauTea Head Spa is a Japanese-rooted head spa suite in Fort Myers: scalp massage, hair nourishing treatments, gua sha lifting facial and back scrub, plus a foot detox soak with 21 kinds of herbs. Every visit happens one-on-one, by appointment, under soft candlelight and a projected moon and stars.">PermabeauTea Head Spa is a Japanese-rooted head spa suite in Fort Myers: scalp massage, hair nourishing treatments, gua sha lifting facial and back scrub, plus a foot detox soak with 21 kinds of herbs. Every visit happens one-on-one, by appointment, under soft candlelight and a projected moon and stars.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Clients confirm it: a perfect 5.0 across 24 Google reviews, praising the attention to detail and how relaxed they feel by the time their tea is poured." data-en="Clients confirm it: a perfect 5.0 across 24 Google reviews, praising the attention to detail and how relaxed they feel by the time their tea is poured.">Clients confirm it: a perfect 5.0 across 24 Google reviews, praising the attention to detail and how relaxed they feel by the time their tea is poured.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="24">24</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">21</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Herbs in the foot detox" data-en="Herbs in the foot detox">Herbs in the foot detox</p></div>''')
rep('''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,109,75,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>
          </div>''',
    '''<div class="flex items-center gap-3 glass glass-hover rounded-full pr-5 pl-1.5 py-1.5">
            <span class="w-10 h-10 rounded-full ring-1 ring-[rgba(212,109,75,0.3)] bg-[rgba(212,109,75,0.12)] flex items-center justify-center font-display text-xs tracking-wide text-[color:var(--accent-deep)]" aria-hidden="true">PT</span>
            <span class="text-sm font-light">PermabeauTea Head Spa · <span class="text-[color:var(--ink-40)]" data-es="Est. 2024" data-en="Est. 2024">Est. 2024</span></span>
          </div>''')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO -> EL RITUAL
# ---------------------------------------------------------------------------
rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Your visit, step by step" data-en="Your visit, step by step">Your visit, step by step</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="The ritual," data-en="The ritual,">The ritual,</span> <span class="text-shine" data-es="step by step" data-en="step by step">step by step</span></h2>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Book online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Pick your ritual on GlossGenius, from the 55-minute Xpress to the full Invitation to Dream, with clear price and duration, and confirm instantly." data-en="Pick your ritual on GlossGenius, from the 55-minute Xpress to the full Invitation to Dream, with clear price and duration, and confirm instantly.">Pick your ritual on GlossGenius, from the 55-minute Xpress to the full Invitation to Dream, with clear price and duration, and confirm instantly.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Steam &amp; cleanse" data-en="Steam &amp; cleanse">Steam &amp; cleanse</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A warm herbal steam opens the scalp under the copper misting arch, ready for a deep cleanse before any product goes on." data-en="A warm herbal steam opens the scalp under the copper misting arch, ready for a deep cleanse before any product goes on.">A warm herbal steam opens the scalp under the copper misting arch, ready for a deep cleanse before any product goes on.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Scalp ritual" data-en="Scalp ritual">Scalp ritual</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Gua sha lifting facial, nourishing hair treatment and a slow scalp massage, each gets its full time, no rushing." data-en="Gua sha lifting facial, nourishing hair treatment and a slow scalp massage, each gets its full time, no rushing.">Gua sha lifting facial, nourishing hair treatment and a slow scalp massage, each gets its full time, no rushing.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Tea &amp; tranquility" data-en="Tea &amp; tranquility">Tea &amp; tranquility</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Add a back scrub or herbal foot detox if you like, then every visit ends the same way: your own cup of homemade tea." data-en="Add a back scrub or herbal foot detox if you like, then every visit ends the same way: your own cup of homemade tea.">Add a back scrub or herbal foot detox if you like, then every visit ends the same way: your own cup of homemade tea.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex; 7 servicios reales)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Choose your" data-en="Choose your">Choose your</span> <span class="text-shine">ritual</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Prices and durations as published by PermabeauTea Head Spa on GlossGenius. Booking confirms instantly." data-en="Prices and durations as published by PermabeauTea Head Spa on GlossGenius. Booking confirms instantly.">Prices and durations as published by PermabeauTea Head Spa on GlossGenius. Booking confirms instantly.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Quick daily reset" data-en="Quick daily reset">Quick daily reset</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Head Spa - Xpress</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A shorter scalp ritual for when time is tight: steam, cleanse and massage, without the extras." data-en="A shorter scalp ritual for when time is tight: steam, cleanse and massage, without the extras.">A shorter scalp ritual for when time is tight: steam, cleanse and massage, without the extras.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">55 min</p></div>
            <a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Book" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(212,109,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Refreshing Head Spa</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="The full scalp and hair ritual, with the gua sha lifting facial worked into a longer, unhurried visit." data-en="The full scalp and hair ritual, with the gua sha lifting facial worked into a longer, unhurried visit.">The full scalp and hair ritual, with the gua sha lifting facial worked into a longer, unhurried visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$175</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">105 min</p></div>
            <a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Book" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Signature" data-en="Signature">Signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Head Spa - The Experiences" data-en="Head Spa - The Experiences">Head Spa - The Experiences</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Neck, arm and shoulder massage combined with mindfulness techniques, on top of the full scalp and hair ritual." data-en="Neck, arm and shoulder massage combined with mindfulness techniques, on top of the full scalp and hair ritual.">Neck, arm and shoulder massage combined with mindfulness techniques, on top of the full scalp and hair ritual.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$225</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">135 min</p></div>
            <a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Book" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="The ultimate ritual" data-en="The ultimate ritual">The ultimate ritual</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Invitation to Dream" data-en="Invitation to Dream">Invitation to Dream</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="The longest ritual PermabeauTea offers: scalp, hair, facial and massage together, unhurried, finished with tea." data-en="The longest ritual PermabeauTea offers: scalp, hair, facial and massage together, unhurried, finished with tea.">The longest ritual PermabeauTea offers: scalp, hair, facial and massage together, unhurried, finished with tea.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$295</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">195 min</p></div>
            <a href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Book" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Hair &amp; Scalp" data-en="Hair &amp; Scalp">Hair &amp; Scalp</p>
          <div class="flex items-baseline justify-between gap-3 text-sm text-[color:var(--ink-60)] font-light">
            <span data-es="Nourishing Treatments" data-en="Nourishing Treatments">Nourishing Treatments</span>
            <span class="text-[color:var(--accent-deep)] whitespace-nowrap">$125 · 70 min</span>
          </div>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Foot Ritual" data-en="Foot Ritual">Foot Ritual</p>
          <div class="flex items-baseline justify-between gap-3 text-sm text-[color:var(--ink-60)] font-light">
            <span data-es="Foot Spa - Herbal Detox" data-en="Foot Spa - Herbal Detox">Foot Spa - Herbal Detox</span>
            <span class="text-[color:var(--accent-deep)] whitespace-nowrap">$95 · 60 min</span>
          </div>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Add-on" data-en="Add-on">Add-on</p>
          <div class="flex items-baseline justify-between gap-3 text-sm text-[color:var(--ink-60)] font-light">
            <span data-es="Back Scrub" data-en="Back Scrub">Back Scrub</span>
            <span class="text-[color:var(--accent-deep)] whitespace-nowrap">$45 · 20 min</span>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="All 7 services shown above, exactly as priced on GlossGenius. No accounts, no surprises." data-en="All 7 services shown above, exactly as priced on GlossGenius. No accounts, no surprises.">All 7 services shown above, exactly as priced on GlossGenius. No accounts, no surprises.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex; 3 fotos reales curadas)
# ---------------------------------------------------------------------------
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="moments" data-en="moments">moments</span>')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Nourishing scalp wash" data-en="Nourishing scalp wash">Nourishing scalp wash</span><img src="assets/gallery-wash.jpg" alt="A nourishing scalp wash under purple ambient light at PermabeauTea Head Spa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Hair treatment under the arch" data-en="Hair treatment under the arch">Hair treatment under the arch</span><img src="assets/gallery-color.jpg" alt="A hair treatment applied under the copper misting arch at PermabeauTea Head Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="21-herb foot detox" data-en="21-herb foot detox">21-herb foot detox</span><img src="assets/gallery-foot-detox.jpg" alt="Feet soaking in the 21-herb foot detox tub at PermabeauTea Head Spa" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="What her" data-en="What her">What her</span> <span class="text-shine" data-es="clients say" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 24 reviews on Google" data-en="5.0 out of 5 · 24 reviews on Google">5.0 out of 5 · 24 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Phenomenal services. Fully relaxing and therapeutic. Very much want to book another session."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">David Walper</span> <span class="text-[color:var(--ink-40)]" data-es="Google review" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Had an amazing experience. Very relaxing and refreshing, would totally recommend her to anyone."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Jessica</span> <span class="text-[color:var(--ink-40)]" data-es="Google review" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I thoroughly enjoyed the experience. The attention to detail and professional atmosphere was amazing. I will return."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Katie W</span> <span class="text-[color:var(--ink-40)]" data-es="Google review" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=PermabeauTea+Head+Spa+Fort+Myers+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 24 reviews on Google" data-en="Read all 24 reviews on Google">Read all 24 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visit us in" data-en="Visit us in">Visit us in</span> <span class="text-shine">Fort Myers</span></h2>')
rep('''<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,109,75,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>''',
    '''<p class="text-sm text-[color:var(--ink-60)] font-light">2741 1st St, Unit 110, Fort Myers, FL 33916</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,109,75,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>''')
rep('''<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,109,75,0.4)]" href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>''',
    '''<p class="text-sm text-[color:var(--ink-60)] font-light" data-es="By appointment via GlossGenius: Monday, Wednesday to Saturday 8am/9am to 8pm, Sunday 10am to 6pm. Closed Tuesdays." data-en="By appointment via GlossGenius: Monday, Wednesday to Saturday 8am/9am to 8pm, Sunday 10am to 6pm. Closed Tuesdays.">By appointment via GlossGenius: Monday, Wednesday to Saturday 8am/9am to 8pm, Sunday 10am to 6pm. Closed Tuesdays.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,109,75,0.4)]" href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" data-es="Book on GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>''')
rep('data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="See the treatment suite and DM any questions before your visit." data-en="See the treatment suite and DM any questions before your visit.">See the treatment suite and DM any questions before your visit.</p>')
rep('''<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"
          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"''',
    '''<iframe title="Map: PermabeauTea Head Spa, 2741 1st St, Fort Myers FL"
          src="''' + NEW_MAPS + '''&output=embed"''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Slow down. Steep in it." data-en="Slow down. Steep in it.">Slow down. Steep in it.</p>')
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Your ritual" data-en="Your ritual">Your ritual</span> <span class="text-shine" data-es="is waiting" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Book online in seconds: your scalp ritual, your foot detox, or the tea waiting at the end of it." data-en="Book online in seconds: your scalp ritual, your foot detox, or the tea waiting at the end of it.">Book online in seconds: your scalp ritual, your foot detox, or the tea waiting at the end of it.</p>')
rep('<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Book on GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>')
print("CTA done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">PermabeauTea</span>')
rep('''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,171,150,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>''',
    '''<span class="w-9 h-9 rounded-full ring-1 ring-[rgba(232,171,150,0.35)] bg-[rgba(212,109,75,0.14)] flex items-center justify-center font-display text-xs tracking-wide text-[color:var(--accent-deep)]" aria-hidden="true">PT</span>
          <span class="font-display text-lg tracking-[0.1em] uppercase">PermabeauTea</span>''')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Japanese head spa in Fort Myers, FL. By appointment only." data-en="Japanese head spa in Fort Myers, FL. By appointment only.">Japanese head spa in Fort Myers, FL. By appointment only.</p>')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p>2741 1st St, Unit 110, Fort Myers, FL 33916</p>')
rep('<p><a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="hover:text-[#e9abae]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="hover:text-[#e9abae]" data-es="Online booking · GlossGenius" data-en="Online booking · GlossGenius">Online booking · GlossGenius</a></p>')
rep('<p><a href="mailto:permabeauteahs@gmail.com" class="hover:text-[#e9abae]">permabeauteahs@gmail.com</a></p>',
    '<p><a href="mailto:permabeauteahs@gmail.com" class="hover:text-[#e9abae]">permabeauteahs@gmail.com</a></p>') if 'mailto:permabeauteahs@gmail.com' in h else None
rep('<p><a href="' + NEW_IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#e9abae]">Instagram · ' + NEW_IG_HANDLE + '</a></p>',
    '<p><a href="' + NEW_IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#e9abae]">Instagram · ' + NEW_IG_HANDLE + '</a></p>\n        <p><a href="mailto:permabeauteahs@gmail.com" class="hover:text-[#e9abae]">permabeauteahs@gmail.com</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 PermabeauTea Head Spa.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. Boton flotante de reserva
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="book-float" aria-label="Book appointment online">')
print("BOOK-FLOAT done")

open(PATH, "w", encoding="utf-8").write(h)
print("WROTE", PATH, len(h), "bytes")
