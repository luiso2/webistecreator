import re
import shutil

SLUG = "dog-city-pompano-beach"
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


TEL = "tel:+19549460001"
MAPS_URL = "https://www.google.com/maps?q=3951+N+Federal+Hwy,+Pompano+Beach,+FL+33064"
MAPS_EMBED = "https://www.google.com/maps?q=3951+N+Federal+Hwy,+Pompano+Beach,+FL+33064&output=embed"
REVIEWS_URL = "https://www.google.com/search?q=Dog+City+Pompano+Beach+FL+reviews"
ADDR = "3951 N Federal Hwy, Pompano Beach, FL 33064"

# ---------------------------------------------------------------------------
# 1. Proteger el badge Merktop
# ---------------------------------------------------------------------------
badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------------------------------------------------------------------------
# 2. Paleta: plum-pink (lashbloom) -> teal/aqua playful (Dog City)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#2f7d8a"),
    ("#5c2140", "#163f46"),
    ("#f0bed7", "#a8e0d9"),
    ("#faf2f6", "#f5faf9"),
    ("#c47a9c", "#4fa8ac"),
    ("#8a5573", "#3c7d82"),
    ("#f3e0ea", "#dff0ee"),
    ("#d9a8c2", "#a3d4d1"),
    ("#7d3457", "#1f5a60"),
    ("#5f2c48", "#234a4f"),
    ("#33222c", "#20302f"),
    ("#fbf3f8", "#eafbfa"),
    ("#fbeff5", "#e3f7f6"),
    ("#f8dfeb", "#cdeeec"),
    ("#f6f1ea", "#eef8f7"),
    ("#f2d5e3", "#cfeeeb"),
    ("#f2cfe0", "#c7ece9"),
    ("#efd0e0", "#d7f0ee"),
    ("#e5c1d4", "#bfe9e6"),
    ("#dc9dbe", "#8dd0cc"),
    ("#d3a2bc", "#9ad6d2"),
    ("#c9789f", "#4fa3a7"),
    ("#b25a85", "#2f7a80"),
    ("#2a1722", "#12272a"),
    ("#1f0f18", "#0d1d1f"),
    ("#1c0f16", "#0b1a1c"),
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(47,125,138"),
    ("rgba(51,34,44", "rgba(32,48,47"),
    ("rgba(240,190,215", "rgba(168,224,217"),
    ("rgba(70,25,50", "rgba(22,63,70"),
    ("rgba(250,242,246", "rgba(245,250,249"),
    ("rgba(125,52,87", "rgba(31,90,96"),
    ("rgba(253,246,250", "rgba(234,251,250"),
    ("rgba(233,205,186", "rgba(163,212,209"),
    ("rgba(185,138,128", "rgba(108,186,181"),
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: sin booking platform ni IG -> tel: + reseñas de Google
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, REVIEWS_URL)

OLD_IG_HANDLE = "@_lashbloom"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, "Google Reviews")
print("GLOBALS done")

# ---------------------------------------------------------------------------
# 4. HEAD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Dog City · Dog Grooming in Pompano Beach, FL | 4.9 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Dog City, Pompano Beach FL: full-service dog grooming with baths, breed-specific cuts, nail trims and de-shedding. 4.9 stars across 91 Google reviews. Call for an appointment." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Dog City · Dog Grooming in Pompano Beach, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Full-service dog grooming: baths, cuts, nail trims and de-shedding. 4.9 on Google with 91 reviews." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/groom-pom-mickey.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/groom-closeup-finished.jpg" />')
assert '<meta name="theme-color" content="#eef8f7" />' in h

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Dog City",
    "description": "Full-service dog grooming salon in Pompano Beach, FL: baths, breed-specific haircuts, nail trims, de-shedding and more for all breeds and sizes.",
    "address": { "@type": "PostalAddress", "streetAddress": "3951 N Federal Hwy", "addressLocality": "Pompano Beach", "addressRegion": "FL", "postalCode": "33064", "addressCountry": "US" },
    "telephone": "+1-954-946-0001",
    "sameAs": ["https://www.google.com/maps/place/Dog+City/@26.2802879,-80.0975787,17z"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "91", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "08:00", "closes": "16:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Dog grooming services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Full Groom" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bath &amp; Brush" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Breed-Specific Haircut" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Nail Trim &amp; De-Shed" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ---------------------------------------------------------------------------
# 5. Idioma: EN default (ya lo es en el esqueleto)
# ---------------------------------------------------------------------------
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ---------------------------------------------------------------------------
# 6. NAV
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,125,138,0.35)]" />',
    '<img src="assets/raw/groom-closeup-finished.jpg" alt="Dog City groomed dog" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,125,138,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Dog <span class="text-[color:var(--accent-deep)]">City</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">DC</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Dog City</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call now" data-en="Call now">Call now</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call now" data-en="Call now">Call now</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Pompano Beach, FL · Dog Grooming" data-en="Pompano Beach, FL · Dog Grooming">Pompano Beach, FL · Dog Grooming</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Loved by Pompano Beach dogs since day one." data-en="Loved by Pompano Beach dogs since day one.">Loved by Pompano Beach dogs since day one.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Baths, cuts and brushouts" data-en="Baths, cuts and brushouts">Baths, cuts and brushouts</span><br /><span data-es="that leave tails " data-en="that leave tails ">that leave tails </span><span class="text-shine" data-es="wagging" data-en="wagging">wagging</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Dog City has been grooming Pompano Beach dogs of every breed and size with full baths, breed-specific haircuts, nail trims and de-shedding treatments. Certified groomers, a calm touch, and a 4.9 rating across 91 Google reviews." data-en="Dog City has been grooming Pompano Beach dogs of every breed and size with full baths, breed-specific haircuts, nail trims and de-shedding treatments. Certified groomers, a calm touch, and a 4.9 rating across 91 Google reviews.">Dog City has been grooming Pompano Beach dogs of every breed and size with full baths, breed-specific haircuts, nail trims and de-shedding treatments. Certified groomers, a calm touch, and a 4.9 rating across 91 Google reviews.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.9 · 91 reviews on Google" data-en="4.9 · 91 reviews on Google">4.9 · 91 reviews on Google</span>')
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            Google Reviews
          </a>''',
    '''<a href="''' + TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (954) 946-0001" data-en="Call (954) 946-0001">Call (954) 946-0001</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            Google Reviews
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/groom-pom-mickey.jpg" alt="A freshly groomed Pomeranian wearing a Mickey Mouse bandana at Dog City" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">Tue&ndash;Fri 8&ndash;5</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Sat 8-4 · Closed Sun &amp; Mon" data-en="Sat 8-4 · Closed Sun &amp; Mon">Sat 8-4 · Closed Sun &amp; Mon</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="91">91</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Full <span class="text-shine">Groom</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Bath · Cut · Nails" data-en="Bath · Cut · Nails">Bath · Cut · Nails</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl"><span class="text-shine">Tue-Fri</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="8am to 5pm" data-en="8am to 5pm">8am to 5pm</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Pompano Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">N Federal Hwy</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Full Groom"),
    ("Hybrid Set", "Breed Cuts"),
    ("Volume Set", "Nail Trim"),
    ("Mega Volume", "De-Shedding"),
    ("Bottom Lashes", "Teeth Brushing"),
    ("West Palm Beach, FL", "Pompano Beach, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA (imagen unica, como a1stump)
# ---------------------------------------------------------------------------
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="grid grid-cols-1 gap-5">
        <div class="frame zoomable aspect-[4/3] img-reveal">
          <img src="assets/raw/groom-schnauzer-salon.jpg" alt="A groomed schnauzer in the Dog City salon, with grooming certificates on the wall" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="A team dogs" data-en="A team dogs">A team dogs</span><br /><span class="text-shine" data-es="actually like" data-en="actually like">actually like</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Dog City has been a fixture on North Federal Highway in Pompano Beach, grooming dogs of every breed and size with a full menu of baths, haircuts, nail trims and de-shedding treatments. The team is certified through the National Dog Groomers Association of America, and it shows in the finish." data-en="Dog City has been a fixture on North Federal Highway in Pompano Beach, grooming dogs of every breed and size with a full menu of baths, haircuts, nail trims and de-shedding treatments. The team is certified through the National Dog Groomers Association of America, and it shows in the finish.">Dog City has been a fixture on North Federal Highway in Pompano Beach, grooming dogs of every breed and size with a full menu of baths, haircuts, nail trims and de-shedding treatments. The team is certified through the National Dog Groomers Association of America, and it shows in the finish.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Customers keep coming back for the same reasons: dogs that come home relaxed and happy, a gentle touch with nervous or senior pets, and fair pricing with no surprises. That consistency is why Dog City holds a 4.9-star rating across 91 Google reviews." data-en="Customers keep coming back for the same reasons: dogs that come home relaxed and happy, a gentle touch with nervous or senior pets, and fair pricing with no surprises. That consistency is why Dog City holds a 4.9-star rating across 91 Google reviews.">Customers keep coming back for the same reasons: dogs that come home relaxed and happy, a gentle touch with nervous or senior pets, and fair pricing with no surprises. That consistency is why Dog City holds a 4.9-star rating across 91 Google reviews.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.9" data-decimals="1">4.9</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="91">91</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">All</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Breeds welcome" data-en="Breeds welcome">Breeds welcome</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,125,138,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/groom-closeup-finished.jpg" alt="Dog City" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(47,125,138,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Dog City · <span class="text-[color:var(--ink-40)]" data-es="Certified groomers" data-en="Certified groomers">Certified groomers</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your dog&#39;s visit," data-en="Your dog&#39;s visit,">Your dog&#39;s visit,</span> <span class="text-shine" data-es="step by step" data-en="step by step">step by step</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Check-in" data-en="Check-in">Check-in</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tell the team about your dog&#39;s coat, any sensitive spots, and the cut you have in mind." data-en="Tell the team about your dog&#39;s coat, any sensitive spots, and the cut you have in mind.">Tell the team about your dog&#39;s coat, any sensitive spots, and the cut you have in mind.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Bath &amp; blow-dry" data-en="Bath &amp; blow-dry">Bath &amp; blow-dry</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A full bath with the right shampoo for your dog&#39;s coat, followed by a gentle blow-dry and brush-out." data-en="A full bath with the right shampoo for your dog&#39;s coat, followed by a gentle blow-dry and brush-out.">A full bath with the right shampoo for your dog&#39;s coat, followed by a gentle blow-dry and brush-out.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="The cut" data-en="The cut">The cut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Breed-standard or your own style, trimmed by hand with a steady, calm approach." data-en="Breed-standard or your own style, trimmed by hand with a steady, calm approach.">Breed-standard or your own style, trimmed by hand with a steady, calm approach.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Finishing touches" data-en="Finishing touches">Finishing touches</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nails trimmed, ears cleaned, and a bandana or bow for the ride home." data-en="Nails trimmed, ears cleaned, and a bandana or bow for the ride home.">Nails trimmed, ears cleaned, and a bandana or bow for the ride home.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Grooming for" data-en="Grooming for">Grooming for</span> <span class="text-shine" data-es="every dog" data-en="every dog">every dog</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Pricing depends on your dog&#39;s breed, coat and size, so every visit starts with a quick, honest quote." data-en="Pricing depends on your dog&#39;s breed, coat and size, so every visit starts with a quick, honest quote.">Pricing depends on your dog&#39;s breed, coat and size, so every visit starts with a quick, honest quote.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(47,125,138,0.4); box-shadow: 0 18px 50px rgba(32,48,47,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Groom" data-en="Full Groom">Full Groom</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Bath, blow-dry, haircut, nail trim and ear cleaning, finished with a bandana or bow." data-en="Bath, blow-dry, haircut, nail trim and ear cleaning, finished with a bandana or bow.">Bath, blow-dry, haircut, nail trim and ear cleaning, finished with a bandana or bow.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Quick refresh" data-en="Quick refresh">Quick refresh</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Bath &amp; Brush" data-en="Bath &amp; Brush">Bath &amp; Brush</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A full bath with blow-dry and brush-out, a light trim where needed, and a fresh smell." data-en="A full bath with blow-dry and brush-out, a light trim where needed, and a fresh smell.">A full bath with blow-dry and brush-out, a light trim where needed, and a fresh smell.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Styled to order" data-en="Styled to order">Styled to order</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Breed-Specific Haircut" data-en="Breed-Specific Haircut">Breed-Specific Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Scissored or clipped to breed standard, or your own look, with calm, steady hands." data-en="Scissored or clipped to breed standard, or your own look, with calm, steady hands.">Scissored or clipped to breed standard, or your own look, with calm, steady hands.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Add-on favorites" data-en="Add-on favorites">Add-on favorites</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Nail Trim &amp; De-Shed" data-en="Nail Trim &amp; De-Shed">Nail Trim &amp; De-Shed</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A quick nail trim and grind, or a full de-shedding treatment for heavy shedders." data-en="A quick nail trim and grind, or a full de-shedding treatment for heavy shedders.">A quick nail trim and grind, or a full de-shedding treatment for heavy shedders.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Bath &amp; Spa" data-en="Bath &amp; Spa">Bath &amp; Spa</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Full bath &amp; blow-dry" data-en="Full bath &amp; blow-dry">Full bath &amp; blow-dry</li>
            <li class="flex items-center gap-2" data-es="De-shedding treatment" data-en="De-shedding treatment">De-shedding treatment</li>
            <li class="flex items-center gap-2" data-es="Flea &amp; tick shampoo" data-en="Flea &amp; tick shampoo">Flea &amp; tick shampoo</li>
            <li class="flex items-center gap-2" data-es="Brush-out" data-en="Brush-out">Brush-out</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Styling" data-en="Styling">Styling</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Breed-standard cuts" data-en="Breed-standard cuts">Breed-standard cuts</li>
            <li class="flex items-center gap-2" data-es="Custom styling" data-en="Custom styling">Custom styling</li>
            <li class="flex items-center gap-2" data-es="Hand-scissoring" data-en="Hand-scissoring">Hand-scissoring</li>
            <li class="flex items-center gap-2" data-es="Sanitary trim" data-en="Sanitary trim">Sanitary trim</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Finishing Touches" data-en="Finishing Touches">Finishing Touches</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Nail trim &amp; grind" data-en="Nail trim &amp; grind">Nail trim &amp; grind</li>
            <li class="flex items-center gap-2" data-es="Ear cleaning" data-en="Ear cleaning">Ear cleaning</li>
            <li class="flex items-center gap-2" data-es="Teeth brushing" data-en="Teeth brushing">Teeth brushing</li>
            <li class="flex items-center gap-2" data-es="Bandana or bow" data-en="Bandana or bow">Bandana or bow</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on breed, coat and size. Call (954) 946-0001 for a quote." data-en="Pricing depends on breed, coat and size. Call (954) 946-0001 for a quote.">Pricing depends on breed, coat and size. Call (954) 946-0001 for a quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real" data-en="Real">Real</span> <span class="text-shine" data-es="results" data-en="results">results</span>')
rep('''<a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          Google Reviews
        </a>''',
    '''<a href="''' + TEL + '''" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call (954) 946-0001
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Corte fresco, cachorro feliz" data-en="Fresh trim, happy pup">Fresh trim, happy pup</span><img src="assets/raw/groom-pom-mickey.jpg" alt="A freshly groomed Pomeranian with a Mickey Mouse bandana at Dog City" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Antes y después real" data-en="Real before &amp; after">Real before &amp; after</span><img src="assets/raw/before-after-yorkie.jpg" alt="A Yorkie before and after a full groom at Dog City" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Estilo con pañoleta" data-en="Styled &amp; bandana ready">Styled &amp; bandana ready</span><img src="assets/raw/groom-shihtzu-bandana.jpg" alt="A groomed black Shih Tzu wearing a bandana at Dog City" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Limpio y en casa" data-en="Clean, soft and home">Clean, soft and home</span><img src="assets/raw/client-maltese-home.jpg" alt="A clean, freshly groomed Maltese at home after a Dog City visit" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Todas las razas, bienvenidas" data-en="All breeds welcome">All breeds welcome</span><img src="assets/raw/client-goldendoodle-home.jpg" alt="A happy, well-groomed Goldendoodle client at home" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:330ms"><span class="tile-cap" data-es="Listo para salir" data-en="Finished and ready to go">Finished and ready to go</span><img src="assets/raw/groom-schnauzer-standing.jpg" alt="A freshly groomed schnauzer standing on the table at Dog City" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. MARQUEE reverse: ya cubierto arriba por rep_all (x4 total, 2 por bloque)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Pompano Beach" data-en="What Pompano Beach">What Pompano Beach</span> <span class="text-shine" data-es="owners say" data-en="owners say">owners say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 out of 5 · 91 reviews on Google" data-en="4.9 out of 5 · 91 reviews on Google">4.9 out of 5 · 91 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I love this place! They are great with my dog, sweet when she comes in. Do an amazing job. Price is great. This is only place I'll take my dog from now on."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Francesca Padron</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Best grooming ever!! The shampoo used is not overpowering, it smells clean and very lightly scented. The haircut is perfect. Blu gets compliments everywhere he goes!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Chrissy Oliver</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I take my golden retriever and French bulldog to Dog City Grooming and they always do the best job! They are so soft and happy right now. The staff is so kind as well. Thanks for caring for my babies!"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Brianna Sledge</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 91 reviews on Google" data-en="Read all 91 reviews on Google">Read all 91 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visit us in" data-en="Visit us in">Visit us in</span> <span class="text-shine">Pompano Beach</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,125,138,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">''' + ADDR + '''</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,125,138,0.4)]" href="''' + MAPS_URL + '''" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,125,138,0.4)]" href="''' + TEL + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Tue-Fri 8am to 5pm, Sat 8am to 4pm. Closed Sunday and Monday." data-en="Tue-Fri 8am to 5pm, Sat 8am to 4pm. Closed Sunday and Monday.">Tue-Fri 8am to 5pm, Sat 8am to 4pm. Closed Sunday and Monday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,125,138,0.4)]" href="''' + TEL + '''" data-es="Call (954) 946-0001" data-en="Call (954) 946-0001">Call (954) 946-0001</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,125,138,0.4)]" href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener">Google Reviews</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Phone" data-en="Phone">Phone</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Give the team a call to check availability or ask about your dog&#39;s cut." data-en="Give the team a call to check availability or ask about your dog&#39;s cut.">Give the team a call to check availability or ask about your dog&#39;s cut.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(47,125,138,0.4)]" href="''' + TEL + '''">(954) 946-0001</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Dog City, 3951 N Federal Hwy, Pompano Beach FL"
          src="''' + MAPS_EMBED + '''"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Loved by Pompano Beach dogs since day one." data-en="Loved by Pompano Beach dogs since day one.">Loved by Pompano Beach dogs since day one.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your dog&#39;s next groom" data-en="Your dog&#39;s next groom">Your dog&#39;s next groom</span> <span class="text-shine" data-es="is waiting" data-en="is waiting">is waiting</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call Dog City to book a bath, a full groom or a breed-specific cut, and give your dog the spa day the reviews talk about." data-en="Call Dog City to book a bath, a full groom or a breed-specific cut, and give your dog the spa day the reviews talk about.">Call Dog City to book a bath, a full groom or a breed-specific cut, and give your dog the spa day the reviews talk about.</p>')
rep('<a href="' + TEL + '" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="' + REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    '<a href="' + TEL + '" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (954) 946-0001" data-en="Call (954) 946-0001">Call (954) 946-0001</a>\n        <a href="' + REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Read reviews" data-en="Read reviews">Read reviews</a>')
print("CTA done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Dog City</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(168,224,217,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/raw/groom-closeup-finished.jpg" alt="Dog City" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(168,224,217,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Dog City</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Dog grooming salon in Pompano Beach, FL. Walk-ins and appointments welcome." data-en="Dog grooming salon in Pompano Beach, FL. Walk-ins and appointments welcome.">Dog grooming salon in Pompano Beach, FL. Walk-ins and appointments welcome.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + TEL + '''" target="_blank" rel="noopener" class="hover:text-[#a8e0d9]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + ADDR + '''</p>
        <p><a href="''' + TEL + '''" class="hover:text-[#a8e0d9]">(954) 946-0001</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + REVIEWS_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a8e0d9]">Instagram · Google Reviews</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Hours" data-en="Hours">Hours</p>
        <p data-es="Tue-Fri 8am-5pm" data-en="Tue-Fri 8am-5pm">Tue-Fri 8am-5pm</p>
        <p data-es="Sat 8am-4pm · Closed Sun &amp; Mon" data-en="Sat 8am-4pm · Closed Sun &amp; Mon">Sat 8am-4pm · Closed Sun &amp; Mon</p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Dog City.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. BOTON FLOTANTE
# ---------------------------------------------------------------------------
rep('''<a href="''' + TEL + '''" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f5faf9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
  </a>''',
    '''<a href="''' + TEL + '''" class="book-float" aria-label="Call Dog City">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f5faf9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>''')
print("BOOK-FLOAT done")

open(PATH, "w", encoding="utf-8").write(h)
print("WRITTEN", PATH)
