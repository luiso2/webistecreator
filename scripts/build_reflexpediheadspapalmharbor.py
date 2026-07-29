import re
import shutil

SLUG = "reflexpedi-headspa-palm-harbor"
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


# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop antes de tocar la paleta
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> teal + coral "wellness clinic"
#    (derivada de los colores reales configurados por Renee en su propia
#    pagina de GlossGenius: brand_color_override_primary #3E8D9A -> #ED8277)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#2d6f78"),  # accent-deep
    ("#5c2140", "#163c40"),  # btn-3d sole darkest
    ("#f0bed7", "#f4c9a8"),  # dark-band shine/orb/stars accent
    ("#faf2f6", "#f7f3ec"),  # bg
    ("#c47a9c", "#d9806c"),  # accent-mid
    ("#8a5573", "#1d4b50"),  # dark-band btn shadow deep
    ("#f3e0ea", "#f2e3da"),  # bg-2 / accent-soft
    ("#d9a8c2", "#e8b49a"),  # orb-b
    ("#7d3457", "#1a4448"),  # dark mid
    ("#5f2c48", "#163c40"),  # step-num gradient end
    ("#33222c", "#24312f"),  # ink
    ("#fbf3f8", "#faf6f0"),  # tile-cap text near-white
    ("#fbeff5", "#f7ece0"),  # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#f0d9c4"),  # dark-band shimmer 3rd stop
    ("#f6f1ea", "#f3ede2"),  # theme-color meta
    ("#f2d5e3", "#f0ded0"),  # orb-a
    ("#f2cfe0", "#ecd2b8"),  # dark-band shimmer last stop
    ("#efd0e0", "#ecd2b8"),  # dark-band btn-3d gradient mid
    ("#e5c1d4", "#e8b49a"),  # orb-c pale
    ("#dc9dbe", "#cc6f52"),  # scroll-progress end stop
    ("#d3a2bc", "#ddab8c"),  # dark-band btn-3d gradient end light
    ("#c9789f", "#cc6f52"),  # shimmer stop
    ("#b25a85", "#4a8e94"),  # shimmer stop
    ("#2a1722", "#0f2b2d"),  # cta-final bg gradient start
    ("#1f0f18", "#0a1f21"),  # cta-final bg gradient end
    ("#1c0f16", "#0c2224"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(45,111,120"),   # accent-deep alpha
    ("rgba(51,34,44", "rgba(36,49,47"),       # ink alpha
    ("rgba(240,190,215", "rgba(244,201,168"),  # dark-band light accent alpha
    ("rgba(70,25,50", "rgba(22,60,64"),       # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(247,243,236"),  # bg alpha (nav scrolled)
    ("rgba(125,52,87", "rgba(26,68,72"),      # dark mid alpha
    ("rgba(253,246,250", "rgba(250,246,240"),  # surface alpha
    ("rgba(40,16,30", "rgba(15,43,45"),       # tile-cap gradient dark
    ("rgba(233,205,186", "rgba(244,201,168"),  # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(232,180,154"),  # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: booking (GlossGenius), Instagram, telefono
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_BOOK = "https://reflexpedi.glossgenius.com/"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_BOOK)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/reflexpedibyrenee/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@reflexpedibyrenee"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_TEL = "tel:+17274806447"
NEW_MAPS = "https://www.google.com/maps?q=3235+Tampa+Rd+Room8,+Palm+Harbor,+FL+34684"
NEW_MAPS_EMBED = "https://www.google.com/maps?q=3235+Tampa+Rd+Room8,+Palm+Harbor,+FL+34684&output=embed"

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>ReflexPedi &amp; HeadSpa · Head Spa &amp; Reflexology in Palm Harbor, FL | 5.0 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="ReflexPedi &amp; HeadSpa, Palm Harbor FL: private one-on-one head spa and reflexology pedicure with Renee Lee. 5.0 stars across 188 Google reviews. Book online." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="ReflexPedi &amp; HeadSpa · Head Spa &amp; Reflexology in Palm Harbor, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Private, one-on-one head spa and reflexology pedicure. 5.0 on Google with 188 reviews. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-relax.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/owner-renee.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "name": "ReflexPedi &amp; HeadSpa",
    "description": "Private, one-on-one head spa and reflexology pedicure studio in Palm Harbor, FL, run by Renee Lee inside Salon Lofts.",
    "address": { "@type": "PostalAddress", "streetAddress": "3235 Tampa Rd Room#8", "addressLocality": "Palm Harbor", "addressRegion": "FL", "postalCode": "34684", "addressCountry": "US" },
    "telephone": "+1-727-480-6447",
    "email": "reflexpedi34684@gmail.com",
    "url": "https://reflexpedi.glossgenius.com/",
    "sameAs": ["https://www.instagram.com/reflexpedibyrenee/", "https://www.facebook.com/reflexpedi/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "188", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Thursday"], "opens": "08:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday", "Friday", "Saturday"], "opens": "09:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "10:00", "closes": "18:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Head spa and reflexology services", "itemListElement": [
      { "@type": "Offer", "price": "199", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Ultimate HeadSpa Treatment" } },
      { "@type": "Offer", "price": "250", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pedicure &amp; HeadSpa Package" } },
      { "@type": "Offer", "price": "168", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Migraine/Psoriasis Relief Treatment" } },
      { "@type": "Offer", "price": "155", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Unwind HeadSpa Treatment" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: negocio EN -> se queda en EN (ya es el default del esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. NAV (logo monograma + wordmark + preloader)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(45,111,120,0.35)]" />',
    '<img src="assets/owner-renee.jpg" alt="ReflexPedi &amp; HeadSpa" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(45,111,120,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Reflex<span class="text-[color:var(--accent-deep)]">Pedi</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">RP</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">ReflexPedi</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Book now" data-en="Book now">Book now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Book now" data-en="Book now">Book now</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Palm Harbor, FL · Head Spa &amp; Reflexology" data-en="Palm Harbor, FL · Head Spa &amp; Reflexology">Palm Harbor, FL · Head Spa &amp; Reflexology</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="A private sanctuary, just for you." data-en="A private sanctuary, just for you.">A private sanctuary, just for you.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="One client at a time," data-en="One client at a time,">One client at a time,</span><br /><span data-es="a ritual made to help you " data-en="a ritual made to help you ">a ritual made to help you </span><span class="text-shine" data-es="unwind" data-en="unwind">unwind</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Renee Lee sees one client at a time, so every session is unhurried and tailored to you: scalp treatments, reflexology pedicures and facials in a private Salon Lofts suite in Palm Harbor." data-en="Renee Lee sees one client at a time, so every session is unhurried and tailored to you: scalp treatments, reflexology pedicures and facials in a private Salon Lofts suite in Palm Harbor.">Renee Lee sees one client at a time, so every session is unhurried and tailored to you: scalp treatments, reflexology pedicures and facials in a private Salon Lofts suite in Palm Harbor.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 188 reviews on Google" data-en="5.0 · 188 reviews on Google">5.0 · 188 reviews on Google</span>')
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
          <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            (727) 480-6447
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-relax.jpg" alt="A client fully relaxed during a head spa treatment at ReflexPedi &amp; HeadSpa" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Book online" data-en="Book online">Book online</p>
            <p class="font-display text-lg">Ultimate HeadSpa</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$199 · 100min" data-en="$199 · 100min">$199 · 100min</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="188">188</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">HeadSpa <span class="text-shine">&amp;</span> Reflexology</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="24 servicios reales" data-en="24 real services">24 real services</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">1:1 <span class="text-shine" data-es="siempre" data-en="always">always</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="One client at a time, no exceptions" data-en="One client at a time, no exceptions">One client at a time, no exceptions</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Palm Harbor</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Salon Lofts · Tampa Rd" data-en="Salon Lofts · Tampa Rd">Salon Lofts · Tampa Rd</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Head Spa"),
    ("Hybrid Set", "Reflexology"),
    ("Volume Set", "Pedicure"),
    ("Mega Volume", "Scalp Massage"),
    ("Bottom Lashes", "Facial Lift"),
    ("West Palm Beach, FL", "Palm Harbor, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-scalp-massage.jpg" alt="Hands massaging a client&#39;s scalp during a head spa treatment" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-renee-treatment.jpg" alt="Renee Lee performing a scalp treatment on a client in her Palm Harbor suite" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="A private suite," data-en="A private suite,">A private suite,</span><br /><span class="text-shine" data-es="made just for you" data-en="made just for you">made just for you</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Welcome to ReflexPedi &amp; HeadSpa, a private, one-on-one wellness sanctuary. Because Renee works with only one client at a time, your session is never rushed and completely tailored to your needs. Experience the luxury of undivided attention in a peaceful suite designed solely for your relaxation." data-en="Welcome to ReflexPedi &amp; HeadSpa, a private, one-on-one wellness sanctuary. Because Renee works with only one client at a time, your session is never rushed and completely tailored to your needs. Experience the luxury of undivided attention in a peaceful suite designed solely for your relaxation.">Welcome to ReflexPedi &amp; HeadSpa, a private, one-on-one wellness sanctuary. Because Renee works with only one client at a time, your session is never rushed and completely tailored to your needs. Experience the luxury of undivided attention in a peaceful suite designed solely for your relaxation.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a perfect 5.0 across 188 Google reviews, and clients who describe the reflexology and head spa combination as unlike anything else in Tampa Bay." data-en="The result: a perfect 5.0 across 188 Google reviews, and clients who describe the reflexology and head spa combination as unlike anything else in Tampa Bay.">The result: a perfect 5.0 across 188 Google reviews, and clients who describe the reflexology and head spa combination as unlike anything else in Tampa Bay.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="188">188</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(45,111,120,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/owner-renee.jpg" alt="Renee Lee" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(45,111,120,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Renee Lee · <span class="text-[color:var(--ink-40)]" data-es="Owner &amp; specialist" data-en="Owner &amp; specialist">Owner &amp; specialist</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your visit, step" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="by step" data-en="by step">by step</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Book online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Pick your treatment on GlossGenius with clear price and duration, and confirm instantly." data-en="Pick your treatment on GlossGenius with clear price and duration, and confirm instantly.">Pick your treatment on GlossGenius with clear price and duration, and confirm instantly.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Scalp analysis" data-en="Scalp analysis">Scalp analysis</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Renee looks at your scalp and feet to tailor the herbal infusion, oils and pressure to what you actually need." data-en="Renee looks at your scalp and feet to tailor the herbal infusion, oils and pressure to what you actually need.">Renee looks at your scalp and feet to tailor the herbal infusion, oils and pressure to what you actually need.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The ritual" data-en="The ritual">The ritual</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Herbal infusion, scalp and shoulder massage, hair care and reflexology, up to 150 unhurried minutes, one on one." data-en="Herbal infusion, scalp and shoulder massage, hair care and reflexology, up to 150 unhurried minutes, one on one.">Herbal infusion, scalp and shoulder massage, hair care and reflexology, up to 150 unhurried minutes, one on one.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Leave renewed" data-en="Leave renewed">Leave renewed</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Hair washed and dried, skin hydrated, feet cared for, and your next visit booked before you walk out." data-en="Hair washed and dried, skin hydrated, feet cared for, and your next visit booked before you walk out.">Hair washed and dried, skin hydrated, feet cared for, and your next visit booked before you walk out.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex; 24 servicios reales)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Choose your" data-en="Choose your">Choose your</span> <span class="text-shine">ritual</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Prices and durations as published by ReflexPedi &amp; HeadSpa on GlossGenius. Booking confirms instantly." data-en="Prices and durations as published by ReflexPedi &amp; HeadSpa on GlossGenius. Booking confirms instantly.">Prices and durations as published by ReflexPedi &amp; HeadSpa on GlossGenius. Booking confirms instantly.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"


def card(eyebrow, name, desc, price, dur, featured=False):
    btn_cls = "btn-3d" if featured else "btn-ghost"
    style = ' style="transition-delay:110ms; border-color: rgba(45,111,120,0.4); box-shadow: 0 18px 50px rgba(36,49,47,0.14);"' if featured else ""
    return f'''        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal"{style}>
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="{eyebrow}" data-en="{eyebrow}">{eyebrow}</p>
          <h3 class="font-display text-2xl leading-snug mb-3">{name}</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="{desc}" data-en="{desc}">{desc}</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">${price}</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">{dur}min</p></div>
            <a href="''' + NEW_BOOK + f'''" target="_blank" rel="noopener" class="{btn_cls} rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Book" data-en="Book">Book</a>
          </div>
        </div>
'''


FEATURED_HTML = (
    card("Signature ritual", "Ultimate HeadSpa Treatment",
         "Herbal infusion, scalp analysis, shampoo and hair care, mini facial, plus reflexology and a paraffin treatment.",
         199, 100, featured=True)
    + card("Most complete", "Pedicure &amp; HeadSpa Package",
           "Scalp analysis, essential oil treatment, mini facial, shampoo and blow-dry, plus a gel pedicure with paraffin.",
           250, 150)
    + card("Specialty relief", "Migraine/Psoriasis Relief Treatment",
           "Essential oil therapy with GuoSha technique, herbal infusion, scalp analysis and a mini facial.",
           168, 90)
    + card("Best for first visits", "Unwind HeadSpa Treatment",
           "Herbal infusion, scalp analysis, a rejuvenating scalp, neck, shoulder and hand treatment, hair care and a mini facial.",
           155, 90)
)
NEW_SERVICES_GRID = '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">\n' + FEATURED_HTML + '''      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Head Spa Rituals" data-en="Head Spa Rituals">Head Spa Rituals</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-3"><span>Luxury Essential Oils HeadSpa <span class="text-[color:var(--ink-40)]">120min</span></span><span class="font-medium text-[color:var(--ink)]">$250</span></li>
            <li class="flex items-center justify-between gap-3"><span>Castor Oil HeadSpa <span class="text-[color:var(--ink-40)]">80min</span></span><span class="font-medium text-[color:var(--ink)]">$138</span></li>
            <li class="flex items-center justify-between gap-3"><span>Signature HeadSpa <span class="text-[color:var(--ink-40)]">70min</span></span><span class="font-medium text-[color:var(--ink)]">$125</span></li>
            <li class="flex items-center justify-between gap-3"><span>Herbal Soup HeadSpa <span class="text-[color:var(--ink-40)]">60min</span></span><span class="font-medium text-[color:var(--ink)]">$99</span></li>
            <li class="flex items-center justify-between gap-3"><span>Dry Essential Oils HeadSpa <span class="text-[color:var(--ink-40)]">50min</span></span><span class="font-medium text-[color:var(--ink)]">$89</span></li>
            <li class="flex items-center justify-between gap-3"><span>Dry Organic Castor Oil HeadSpa <span class="text-[color:var(--ink-40)]">45min</span></span><span class="font-medium text-[color:var(--ink)]">$69</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Reflexology &amp; Pedicure" data-en="Reflexology &amp; Pedicure">Reflexology &amp; Pedicure</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-3"><span>Volcano Pedicure <span class="text-[color:var(--ink-40)]">85min</span></span><span class="font-medium text-[color:var(--ink)]">$90</span></li>
            <li class="flex items-center justify-between gap-3"><span>Deluxe Retreat 2 <span class="text-[color:var(--ink-40)]">75min</span></span><span class="font-medium text-[color:var(--ink)]">$85</span></li>
            <li class="flex items-center justify-between gap-3"><span>Reflex Pedi 2 <span class="text-[color:var(--ink-40)]">65min</span></span><span class="font-medium text-[color:var(--ink)]">$65</span></li>
            <li class="flex items-center justify-between gap-3"><span>Deluxe Pedicure 1 <span class="text-[color:var(--ink-40)]">60min</span></span><span class="font-medium text-[color:var(--ink)]">$65</span></li>
            <li class="flex items-center justify-between gap-3"><span>Reflex Pedicure 1 <span class="text-[color:var(--ink-40)]">45min</span></span><span class="font-medium text-[color:var(--ink)]">$50</span></li>
            <li class="flex items-center justify-between gap-3"><span>Gel Polish On Toe <span class="text-[color:var(--ink-40)]">20min</span></span><span class="font-medium text-[color:var(--ink)]">$15</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Facial &amp; Finishing Touches" data-en="Facial &amp; Finishing Touches">Facial &amp; Finishing Touches</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-3"><span>Facial Lift Rejuvenation <span class="text-[color:var(--ink-40)]">60min</span></span><span class="font-medium text-[color:var(--ink)]">$110</span></li>
            <li class="flex items-center justify-between gap-3"><span>Add 30 Mins Extra Treatment <span class="text-[color:var(--ink-40)]">30min</span></span><span class="font-medium text-[color:var(--ink)]">$60</span></li>
            <li class="flex items-center justify-between gap-3"><span>Cupping Rejuvenating <span class="text-[color:var(--ink-40)]">30min</span></span><span class="font-medium text-[color:var(--ink)]">$50</span></li>
            <li class="flex items-center justify-between gap-3"><span>Manicure <span class="text-[color:var(--ink-40)]">40min</span></span><span class="font-medium text-[color:var(--ink)]">$30</span></li>
            <li class="flex items-center justify-between gap-3"><span>Add 15 Mins Extra Treatment <span class="text-[color:var(--ink-40)]">10min</span></span><span class="font-medium text-[color:var(--ink)]">$30</span></li>
            <li class="flex items-center justify-between gap-3"><span>Eyebrows / Chin Wax <span class="text-[color:var(--ink-40)]">10min</span></span><span class="font-medium text-[color:var(--ink)]">$15</span></li>
            <li class="flex items-center justify-between gap-3"><span>Lip Wax <span class="text-[color:var(--ink-40)]">10min</span></span><span class="font-medium text-[color:var(--ink)]">$10</span></li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="All 24 services shown above with real prices and durations. Book directly on GlossGenius." data-en="All 24 services shown above with real prices and durations. Book directly on GlossGenius.">All 24 services shown above with real prices and durations. Book directly on GlossGenius.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex; 7 fotos reales curadas)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Inside the" data-en="Inside the">Inside the</span> <span class="text-shine" data-es="ritual" data-en="ritual">ritual</span>')
rep('''<a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_IG_HANDLE + '''
        </a>''',
    '''<a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_IG_HANDLE + '''
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Masaje de reflexologia en los pies" data-en="Reflexology foot massage">Reflexology foot massage</span><img src="assets/gallery-reflexology-feet.jpg" alt="A reflexology foot massage in progress at ReflexPedi &amp; HeadSpa" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Mascarilla capilar herbal" data-en="Herbal scalp mask">Herbal scalp mask</span><img src="assets/gallery-headspa-mask.jpg" alt="A client receiving an herbal scalp mask treatment" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Lavado ritual" data-en="Ritual hair rinse">Ritual hair rinse</span><img src="assets/gallery-headspa-green.jpg" alt="A client&#39;s hair being rinsed during a head spa ritual" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Ambiente relajante" data-en="A calming setting">A calming setting</span><img src="assets/gallery-headspa-purple.jpg" alt="A head spa treatment under a soft purple ambient light" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Ritual completo" data-en="The full ritual">The full ritual</span><img src="assets/gallery-headspa-blue.jpg" alt="A client fully relaxed during the head spa ritual" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Cuidado del cabello" data-en="Hair care">Hair care</span><img src="assets/gallery-hair-rinse.jpg" alt="Hair being cared for during a head spa rinse" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 15. OPINIONES (2 testimonios reales con nombre, de Salon Lofts)
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What her" data-en="What her">What her</span> <span class="text-shine" data-es="clients say" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 out of 5 · 188 reviews on Google" data-en="5.0 out of 5 · 188 reviews on Google">5.0 out of 5 · 188 reviews on Google</span>')

OLD_REVIEWS_GRID = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
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
        </figure>
      </div>'''
assert OLD_REVIEWS_GRID in h
NEW_REVIEWS_GRID = '''<div class="grid sm:grid-cols-2 gap-5 items-stretch max-w-4xl mx-auto">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I am the privileged first client of Renee&#39;s unique headspa. She has brought amazing equipment and products that relaxed my neck, shoulders and head. It&#39;s a gotta try it to really understand it. She has amazing techniques."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Kathy C.</span> <span class="text-[color:var(--ink-40)]" data-es="Testimonio verificado" data-en="Verified testimonial">Verified testimonial</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"This morning I pulled the trigger and went to one of those headspa places, the ones you see on TikTok. I was there for a little over an hour and I HIGHLY recommend doing it even if it&#39;s just once! Treat yourself."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Meaghan B.</span> <span class="text-[color:var(--ink-40)]" data-es="Testimonio verificado" data-en="Verified testimonial">Verified testimonial</span></figcaption>
        </figure>
      </div>'''
h = h.replace(OLD_REVIEWS_GRID, NEW_REVIEWS_GRID, 1)

rep('<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_MAPS + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="See all 188 reviews on Google" data-en="See all 188 reviews on Google">See all 188 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visit us in" data-en="Visit us in">Visit us in</span> <span class="text-shine">Palm Harbor</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(45,111,120,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">3235 Tampa Rd Room#8 (inside Salon Lofts), Palm Harbor, FL 34684</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(45,111,120,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(45,111,120,0.4)]" href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mon, Thu 8am-8pm · Wed, Fri, Sat 9am-8pm · Sun 10am-6pm · Closed Tuesdays." data-en="Mon, Thu 8am-8pm · Wed, Fri, Sat 9am-8pm · Sun 10am-6pm · Closed Tuesdays.">Mon, Thu 8am-8pm &middot; Wed, Fri, Sat 9am-8pm &middot; Sun 10am-6pm &middot; Closed Tuesdays.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(45,111,120,0.4)]" href="''' + NEW_BOOK + '''" target="_blank" rel="noopener" data-es="Book on GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(45,111,120,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See Renee&#39;s latest treatments and DM any questions before your appointment." data-en="See Renee&#39;s latest treatments and DM any questions before your appointment.">See Renee&#39;s latest treatments and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(45,111,120,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>''')
rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Map: ReflexPedi &amp; HeadSpa, 3235 Tampa Rd Room#8, Palm Harbor FL"\n          src="' + NEW_MAPS_EMBED + '"')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="A private sanctuary, just for you." data-en="A private sanctuary, just for you.">A private sanctuary, just for you.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your unwind" data-en="Your unwind">Your unwind</span> <span class="text-shine" data-es="is waiting" data-en="is waiting">is waiting</span></h2>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Book online in seconds: your head spa ritual, reflexology pedicure, or the combo package, one on one with Renee." data-en="Book online in seconds: your head spa ritual, reflexology pedicure, or the combo package, one on one with Renee.">Book online in seconds: your head spa ritual, reflexology pedicure, or the combo package, one on one with Renee.</p>')
rep('<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Book on GlossGenius" data-en="Book on GlossGenius">Book on GlossGenius</a>')
rep('<a href="' + NEW_IG_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="' + NEW_IG_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Follow on Instagram" data-en="Follow on Instagram">Follow on Instagram</a>')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">ReflexPedi</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(244,201,168,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>''',
    '''<img src="assets/owner-renee.jpg" alt="ReflexPedi &amp; HeadSpa" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(244,201,168,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">ReflexPedi</span>''')
rep('<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    '<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Head spa &amp; reflexology pedicure in Palm Harbor, FL. By appointment only." data-en="Head spa &amp; reflexology pedicure in Palm Harbor, FL. By appointment only.">Head spa &amp; reflexology pedicure in Palm Harbor, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>3235 Tampa Rd Room#8, Palm Harbor, FL 34684</p>')
rep('<p><a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="hover:text-[#f4c9a8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    '<p><a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="hover:text-[#f4c9a8]" data-es="Online booking · GlossGenius" data-en="Online booking · GlossGenius">Online booking &middot; GlossGenius</a></p>\n        <p><a href="tel:+17274806447" class="hover:text-[#f4c9a8]">(727) 480-6447</a></p>\n        <p><a href="mailto:reflexpedi34684@gmail.com" class="hover:text-[#f4c9a8]">reflexpedi34684@gmail.com</a></p>')
rep('<p><a href="' + NEW_IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f4c9a8]">Instagram · ' + NEW_IG_HANDLE + '</a></p>',
    '<p><a href="' + NEW_IG_URL + '" target="_blank" rel="noopener" class="hover:text-[#f4c9a8]">Instagram &middot; ' + NEW_IG_HANDLE + '</a></p>\n        <p><a href="https://www.facebook.com/reflexpedi/" target="_blank" rel="noopener" class="hover:text-[#f4c9a8]">Facebook &middot; ReflexPedi by Renee</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">&copy; 2026 ReflexPedi &amp; HeadSpa.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante de reserva
# ---------------------------------------------------------------------------
rep('<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="' + NEW_BOOK + '" target="_blank" rel="noopener" class="book-float" aria-label="Book an appointment online">')
print("BOOK-FLOAT done")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("WROTE", PATH, len(h), "bytes")
