import re
import shutil

SLUG = "lakeside-grooming-tallahassee"
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
# 2. Paleta: plum-pink (lashbloom) -> lake-teal (Lakeside Grooming)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#146b74"),  # accent-deep
    ("#5c2140", "#0c3438"),  # btn-3d sole darkest
    ("#f0bed7", "#a9dedd"),  # dark-band shine/orb/stars accent
    ("#faf2f6", "#f2f8f6"),  # bg
    ("#c47a9c", "#3f9aa3"),  # accent-mid
    ("#8a5573", "#1c5e63"),  # dark-band btn shadow deep
    ("#f3e0ea", "#dcefec"),  # bg-2 / accent-soft
    ("#d9a8c2", "#78c2c1"),  # orb-b
    ("#7d3457", "#164f55"),  # dark mid
    ("#5f2c48", "#0e4247"),  # step-num gradient end
    ("#33222c", "#1c2b2a"),  # ink
    ("#fbf3f8", "#f2fbfa"),  # tile-cap text near-white
    ("#fbeff5", "#eafaf8"),  # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#cdeeec"),  # dark-band shimmer 3rd stop
    ("#f6f1ea", "#eaf6f4"),  # theme-color meta
    ("#f2d5e3", "#cdece9"),  # orb-a
    ("#f2cfe0", "#c2e9e6"),  # dark-band shimmer last stop
    ("#efd0e0", "#c8ebe8"),  # dark-band btn-3d gradient mid
    ("#e5c1d4", "#a9dedb"),  # orb-c pale
    ("#dc9dbe", "#57b3b2"),  # scroll-progress end stop
    ("#d3a2bc", "#8ecdc9"),  # dark-band btn-3d gradient end light
    ("#c9789f", "#3d9a9c"),  # shimmer stop
    ("#b25a85", "#1f7a7d"),  # shimmer stop
    ("#2a1722", "#0b2b2c"),  # cta-final bg gradient start
    ("#1f0f18", "#071d1e"),  # cta-final bg gradient end
    ("#1c0f16", "#081c1d"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(20,107,116"),    # accent-deep alpha
    ("rgba(51,34,44", "rgba(28,43,42"),        # ink alpha
    ("rgba(240,190,215", "rgba(169,222,221"),  # dark-band light accent alpha
    ("rgba(70,25,50", "rgba(12,52,56"),        # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(242,248,246"),  # bg alpha (nav scrolled)
    ("rgba(125,52,87", "rgba(22,79,85"),       # dark mid alpha
    ("rgba(253,246,250", "rgba(240,251,250"),  # surface alpha
    ("rgba(40,16,30", "rgba(11,31,32"),        # tile-cap gradient dark
    ("rgba(233,205,186", "rgba(169,222,221"),  # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(70,158,163"),   # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform -> tel: + maps. Sin IG (ver data.json).
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+18502964443"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_FB_URL = "https://www.facebook.com/LakesideofTallahasee/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_FB_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_FB_HANDLE = "Facebook"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_FB_HANDLE)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=3976+N+Monroe+St,+Tallahassee,+FL+32303"

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Lakeside Grooming · Dog &amp; Cat Grooming in Tallahassee, FL | 4.6 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Lakeside Grooming, Tallahassee FL: full-service dog and cat grooming with Chantal, Tori, Robin and Tyler. 4.6 stars across 106 Google reviews. Call to book." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Lakeside Grooming · Dog &amp; Cat Grooming in Tallahassee, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Full-service dog and cat grooming since 1993. 4.6 on Google with 106 reviews. Call to book." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/hero-amelia.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-amelia.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "PetGroomer",
    "name": "Lakeside Grooming",
    "description": "Full-service pet grooming salon in Tallahassee, FL for dogs and cats of every breed and size, grooming since 1993: bath and brush, full service haircut, nail trim, ear cleaning, de-shedding and teeth cleaning.",
    "address": { "@type": "PostalAddress", "streetAddress": "3976 N Monroe St", "addressLocality": "Tallahassee", "addressRegion": "FL", "postalCode": "32303", "addressCountry": "US" },
    "telephone": "+1-850-296-4443",
    "sameAs": ["https://www.facebook.com/LakesideofTallahasee/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "106", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "06:30", "closes": "16:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "06:30", "closes": "13:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Grooming services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bath &amp; Brush" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Full Service Haircut" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Nail Trim" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "De-shedding Treatment" } }
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
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,107,116,0.35)]" />',
    '<img src="assets/hero-amelia.jpg" alt="Lakeside Grooming" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,107,116,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lakeside <span class="text-[color:var(--accent-deep)]">Grooming</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">LG</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Lakeside Grooming</span>')
print("NAV done")

rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Call to book" data-en="Call to book">Call to book</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Call to book" data-en="Call to book">Call to book</a>')
print("NAV CTA done")

# ---------------------------------------------------------------------------
# 7. HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Tallahassee, FL · Dog &amp; Cat Grooming" data-en="Tallahassee, FL · Dog &amp; Cat Grooming">Tallahassee, FL · Dog &amp; Cat Grooming</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Calm hands. Happy tails." data-en="Calm hands. Happy tails.">Calm hands. Happy tails.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="A groom as calm as" data-en="A groom as calm as">A groom as calm as</span><br /><span data-es="a morning " data-en="a morning ">a morning </span><span class="text-shine" data-es="by the lake" data-en="by the lake">by the lake</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Owner Chantal Celske has been grooming pets since 1993, and her team, including Tori, Robin and Tyler, brings that same patient, unhurried care to every dog and cat that comes through the door on N Monroe Street, no matter how nervous they start out." data-en="Owner Chantal Celske has been grooming pets since 1993, and her team, including Tori, Robin and Tyler, brings that same patient, unhurried care to every dog and cat that comes through the door on N Monroe Street, no matter how nervous they start out.">Owner Chantal Celske has been grooming pets since 1993, and her team, including Tori, Robin and Tyler, brings that same patient, unhurried care to every dog and cat that comes through the door on N Monroe Street, no matter how nervous they start out.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.6 · 106 reviews on Google" data-en="4.6 · 106 reviews on Google">4.6 · 106 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_FB_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (850) 296-4443" data-en="Call (850) 296-4443">Call (850) 296-4443</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <span data-es="Get directions" data-en="Get directions">Get directions</span>
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-amelia.jpg" alt="Amelia, a small groomed dog, relaxing after her visit to Lakeside Grooming" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open" data-en="Open">Open</p>
            <p class="font-display text-lg">6:30am - 4pm</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Mon-Fri · Sat until 1pm" data-en="Mon-Fri · Sat until 1pm">Mon-Fri · Sat until 1pm</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="106">106</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl"><span data-es="Desde" data-en="Since">Since</span> <span class="text-shine">1993</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Chantal grooming Tallahassee pets" data-en="Chantal grooming Tallahassee pets">Chantal grooming Tallahassee pets</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">Chantal, Tori <span class="text-shine">&amp;</span> Robin</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Meet the team" data-en="Meet the team">Meet the team</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Tallahassee</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">N Monroe St</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Bath &amp; Brush"),
    ("Hybrid Set", "Full Service Haircut"),
    ("Volume Set", "Nail Trim"),
    ("Mega Volume", "De-shedding Treatment"),
    ("Bottom Lashes", "Teeth Cleaning"),
    ("West Palm Beach, FL", "Tallahassee, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-annie.jpg" alt="Annie, a groomed spaniel-type dog, after her visit to Lakeside Grooming" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-storefront-sign.jpg" alt="The real Lakeside Grooming sign outside the salon on N Monroe Street" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Three decades of" data-en="Three decades of">Three decades of</span><br /><span class="text-shine" data-es="patient hands" data-en="patient hands">patient hands</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Chantal Celske opened Lakeside Grooming after starting her career in 1993, and the salon on N Monroe Street has been a fixture for Tallahassee pet owners ever since. Stylists Tori and Robin, along with groomer Tyler, handle everything from a quick bath to a full breed-standard haircut, always at the unhurried pace nervous dogs and cats need." data-en="Chantal Celske opened Lakeside Grooming after starting her career in 1993, and the salon on N Monroe Street has been a fixture for Tallahassee pet owners ever since. Stylists Tori and Robin, along with groomer Tyler, handle everything from a quick bath to a full breed-standard haircut, always at the unhurried pace nervous dogs and cats need.">Chantal Celske opened Lakeside Grooming after starting her career in 1993, and the salon on N Monroe Street has been a fixture for Tallahassee pet owners ever since. Stylists Tori and Robin, along with groomer Tyler, handle everything from a quick bath to a full breed-standard haircut, always at the unhurried pace nervous dogs and cats need.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: a 4.6-star rating across 106 Google reviews, a Community\'s Choice Award for Best Pet Grooming Company in Tallahassee, and pet owners who come back because the team is kind, communicates well, and keeps prices fair." data-en="The result: a 4.6-star rating across 106 Google reviews, a Community\'s Choice Award for Best Pet Grooming Company in Tallahassee, and pet owners who come back because the team is kind, communicates well, and keeps prices fair.">The result: a 4.6-star rating across 106 Google reviews, a Community\'s Choice Award for Best Pet Grooming Company in Tallahassee, and pet owners who come back because the team is kind, communicates well, and keeps prices fair.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.6" data-decimals="1">4.6</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="106">106</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1993</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Grooming since" data-en="Grooming since">Grooming since</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,107,116,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/hero-amelia.jpg" alt="Lakeside Grooming" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(20,107,116,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Chantal, Tori &amp; Robin · <span class="text-[color:var(--ink-40)]" data-es="Groomers" data-en="Groomers">Groomers</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your visit, start" data-en="Your visit, start">Your visit, start</span> <span class="text-shine" data-es="to finish" data-en="to finish">to finish</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Give us a call" data-en="Give us a call">Give us a call</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call (850) 296-4443 or stop by N Monroe Street to find a time that works, walk-ins welcome when the schedule allows." data-en="Call (850) 296-4443 or stop by N Monroe Street to find a time that works, walk-ins welcome when the schedule allows.">Call (850) 296-4443 or stop by N Monroe Street to find a time that works, walk-ins welcome when the schedule allows.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Meet &amp; greet" data-en="Meet &amp; greet">Meet &amp; greet</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Every pet gets a calm hello first, so the team can check coat, skin and temperament before choosing the right approach." data-en="Every pet gets a calm hello first, so the team can check coat, skin and temperament before choosing the right approach.">Every pet gets a calm hello first, so the team can check coat, skin and temperament before choosing the right approach.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Bath &amp; style" data-en="Bath &amp; style">Bath &amp; style</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A gentle bath, blow-dry and the haircut or trim you asked for, done at a pace that keeps nervous pets relaxed." data-en="A gentle bath, blow-dry and the haircut or trim you asked for, done at a pace that keeps nervous pets relaxed.">A gentle bath, blow-dry and the haircut or trim you asked for, done at a pace that keeps nervous pets relaxed.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Tails wagging home" data-en="Tails wagging home">Tails wagging home</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Nails trimmed, ears cleaned, and a pet that goes home looking, and feeling, like new, just like the reviews describe." data-en="Nails trimmed, ears cleaned, and a pet that goes home looking, and feeling, like new, just like the reviews describe.">Nails trimmed, ears cleaned, and a pet that goes home looking, and feeling, like new, just like the reviews describe.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex; solo nombres, sin precios inventados)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine">every pet</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Full menu and current pricing available by phone. Every groom is tailored to your pet\'s breed, coat and temperament." data-en="Full menu and current pricing available by phone. Every groom is tailored to your pet\'s breed, coat and temperament.">Full menu and current pricing available by phone. Every groom is tailored to your pet\'s breed, coat and temperament.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Everyday care" data-en="Everyday care">Everyday care</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Bath &amp; Brush" data-en="Bath &amp; Brush">Bath &amp; Brush</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A full bath, blow-dry and brush-out to keep your pet's coat fresh and clean between full grooms, plus a quick nail trim." data-en="A full bath, blow-dry and brush-out to keep your pet's coat fresh and clean between full grooms, plus a quick nail trim.">A full bath, blow-dry and brush-out to keep your pet's coat fresh and clean between full grooms, plus a quick nail trim.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(20,107,116,0.4); box-shadow: 0 18px 50px rgba(28,43,42,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Service Haircut" data-en="Full Service Haircut">Full Service Haircut</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Bath, blow-dry, a breed-standard or custom haircut, sanitary trim, nail trim and ear cleaning, done start to finish by the team." data-en="Bath, blow-dry, a breed-standard or custom haircut, sanitary trim, nail trim and ear cleaning, done start to finish by the team.">Bath, blow-dry, a breed-standard or custom haircut, sanitary trim, nail trim and ear cleaning, done start to finish by the team.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Quick visit" data-en="Quick visit">Quick visit</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Nail Trim &amp; Ear Cleaning" data-en="Nail Trim &amp; Ear Cleaning">Nail Trim &amp; Ear Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A fast in-and-out for pets that just need their nails trimmed and ears cleaned between full grooming appointments." data-en="A fast in-and-out for pets that just need their nails trimmed and ears cleaned between full grooming appointments.">A fast in-and-out for pets that just need their nails trimmed and ears cleaned between full grooming appointments.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Coat &amp; dental" data-en="Coat &amp; dental">Coat &amp; dental</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="De-shedding &amp; Teeth Cleaning" data-en="De-shedding &amp; Teeth Cleaning">De-shedding &amp; Teeth Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="A de-shedding treatment to cut down on loose fur at home, plus teeth cleaning and flea and tick treatment when your pet needs it." data-en="A de-shedding treatment to cut down on loose fur at home, plus teeth cleaning and flea and tick treatment when your pet needs it.">A de-shedding treatment to cut down on loose fur at home, plus teeth cleaning and flea and tick treatment when your pet needs it.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Bath &amp; Care" data-en="Bath &amp; Care">Bath &amp; Care</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Full bath &amp; blow-dry" data-en="Full bath &amp; blow-dry">Full bath &amp; blow-dry</li>
            <li class="flex items-center gap-2" data-es="Brush-out" data-en="Brush-out">Brush-out</li>
            <li class="flex items-center gap-2" data-es="Nail trim or grind" data-en="Nail trim or grind">Nail trim or grind</li>
            <li class="flex items-center gap-2" data-es="Ear cleaning" data-en="Ear cleaning">Ear cleaning</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Haircut &amp; Style" data-en="Haircut &amp; Style">Haircut &amp; Style</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Breed-standard haircut" data-en="Breed-standard haircut">Breed-standard haircut</li>
            <li class="flex items-center gap-2" data-es="Custom style trim" data-en="Custom style trim">Custom style trim</li>
            <li class="flex items-center gap-2" data-es="Sanitary trim" data-en="Sanitary trim">Sanitary trim</li>
            <li class="flex items-center gap-2" data-es="Paw pad clean-up" data-en="Paw pad clean-up">Paw pad clean-up</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Extra Care" data-en="Extra Care">Extra Care</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="De-shedding treatment" data-en="De-shedding treatment">De-shedding treatment</li>
            <li class="flex items-center gap-2" data-es="Teeth cleaning" data-en="Teeth cleaning">Teeth cleaning</li>
            <li class="flex items-center gap-2" data-es="Flea &amp; tick treatment" data-en="Flea &amp; tick treatment">Flea &amp; tick treatment</li>
            <li class="flex items-center gap-2" data-es="Cat grooming" data-en="Cat grooming">Cat grooming</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on breed, size and coat condition. Call (850) 296-4443 for an exact quote." data-en="Pricing depends on breed, size and coat condition. Call (850) 296-4443 for an exact quote.">Pricing depends on breed, size and coat condition. Call (850) 296-4443 for an exact quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex, 5 fotos reales curadas)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Happy" data-en="Happy">Happy</span> <span class="text-shine" data-es="pets" data-en="pets">pets</span>')
rep('''<a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_FB_HANDLE + '''
        </a>''',
    '''<a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          ''' + NEW_FB_HANDLE + '''
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[21/9] img-reveal"><span class="tile-cap" data-es="Blossom, tranquila y lista para la foto" data-en="A calm, camera-ready poodle">A calm, camera-ready poodle</span><img src="assets/gallery-blossom.jpg" alt="Blossom, a groomed standard poodle, standing calmly after her visit to Lakeside Grooming" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Recien peinada y lista" data-en="Freshly groomed and picture-ready">Freshly groomed and picture-ready</span><img src="assets/gallery-tilly.jpg" alt="Tilly, a groomed Pomeranian, after her visit to Lakeside Grooming" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Moños bien puestos" data-en="Bows done just right">Bows done just right</span><img src="assets/gallery-patriotic-poodle.jpg" alt="A groomed standard poodle wearing bow clips after a visit to Lakeside Grooming" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Dulce y recien banada" data-en="Sweet, soft and freshly washed">Sweet, soft and freshly washed</span><img src="assets/gallery-yorkie.jpg" alt="A groomed Yorkie with a bow, resting after a visit to Lakeside Grooming" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:270ms"><span class="tile-cap" data-es="Tranquila tras el grooming" data-en="Calm after a full groom">Calm after a full groom</span><img src="assets/gallery-cavalier-mix.jpg" alt="A groomed spaniel-mix dog lying calmly after a visit to Lakeside Grooming" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. MARQUEE 2 (reverse) ya cubierto por MARQUEE_WORDS (rep_all)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What pet owners" data-en="What pet owners">What pet owners</span> <span class="text-shine" data-es="are saying" data-en="are saying">are saying</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★☆</span> &nbsp;<span data-es="4.6 out of 5 · 106 reviews on Google" data-en="4.6 out of 5 · 106 reviews on Google">4.6 out of 5 · 106 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Lakeside grooming did an amazing job on my mini Goldendoodle! They are so kind, communicate well and very affordable."</blockquote>
          <figcaption class="text-sm"><span class="text-[color:var(--ink-40)]" data-es="Google review" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Tyler did a phenomenal job on my double doodle! Halloween just around the corner and we are going to show off."</blockquote>
          <figcaption class="text-sm"><span class="text-[color:var(--ink-40)]" data-es="Google review" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing! They were extremely patient with my dog, who has so many issues he should have a magazine track for himself."</blockquote>
          <figcaption class="text-sm"><span class="text-[color:var(--ink-40)]" data-es="Google review" data-en="Google review">Google review</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=Lakeside+Grooming+Tallahassee+FL+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 106 reviews on Google" data-en="Read all 106 reviews on Google">Read all 106 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visit us in" data-en="Visit us in">Visit us in</span> <span class="text-shine">Tallahassee</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,116,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">3976 N Monroe St, Tallahassee, FL 32303</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,116,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,116,0.4)]" href="tel:+18502964443" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Friday, 6:30 AM to 4:00 PM. Saturday 6:30 AM to 1:00 PM. Closed Sunday." data-en="Monday to Friday, 6:30 AM to 4:00 PM. Saturday 6:30 AM to 1:00 PM. Closed Sunday.">Monday to Friday, 6:30 AM to 4:00 PM. Saturday 6:30 AM to 1:00 PM. Closed Sunday.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,116,0.4)]" href="tel:+18502964443" data-es="Call (850) 296-4443" data-en="Call (850) 296-4443">Call (850) 296-4443</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,116,0.4)]" href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener">''' + NEW_FB_HANDLE + '''</a>
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
              <p class="font-medium mb-1">Facebook</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See the latest grooms and Reels from the team, and message any questions before your visit." data-en="See the latest grooms and Reels from the team, and message any questions before your visit.">See the latest grooms and Reels from the team, and message any questions before your visit.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(20,107,116,0.4)]" href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener">Facebook</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Lakeside Grooming, 3976 N Monroe St, Tallahassee FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Calm hands. Happy tails." data-en="Calm hands. Happy tails.">Calm hands. Happy tails.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One call books" data-en="One call books">One call books</span> <span class="text-shine" data-es="a calmer groom" data-en="a calmer groom">a calmer groom</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (850) 296-4443 to find a time with Chantal, Tori, Robin or Tyler, Monday to Friday 6:30 AM to 4 PM, or Saturday 6:30 AM to 1 PM." data-en="Call (850) 296-4443 to find a time with Chantal, Tori, Robin or Tyler, Monday to Friday 6:30 AM to 4 PM, or Saturday 6:30 AM to 1 PM.">Call (850) 296-4443 to find a time with Chantal, Tori, Robin or Tyler, Monday to Friday 6:30 AM to 4 PM, or Saturday 6:30 AM to 1 PM.</p>')
rep('''<a href="tel:+18502964443" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="tel:+18502964443" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (850) 296-4443" data-en="Call (850) 296-4443">Call (850) 296-4443</a>
        <a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Get directions" data-en="Get directions">Get directions</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Lakeside</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(169,222,221,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/hero-amelia.jpg" alt="Lakeside Grooming" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(169,222,221,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lakeside Grooming</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Dog &amp; cat grooming in Tallahassee, FL. Walk-ins welcome when the schedule allows." data-en="Dog &amp; cat grooming in Tallahassee, FL. Walk-ins welcome when the schedule allows.">Dog &amp; cat grooming in Tallahassee, FL. Walk-ins welcome when the schedule allows.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="tel:+18502964443" target="_blank" rel="noopener" class="hover:text-[#a9dedd]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>3976 N Monroe St, Tallahassee, FL 32303</p>
        <p><a href="tel:+18502964443" class="hover:text-[#a9dedd]" data-es="Call (850) 296-4443" data-en="Call (850) 296-4443">Call (850) 296-4443</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9dedd]">Instagram · ''' + NEW_FB_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_FB_URL + '''" target="_blank" rel="noopener" class="hover:text-[#a9dedd]">Facebook · Lakeside Grooming of Tallahassee</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lakeside Grooming.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="tel:+18502964443" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="tel:+18502964443" class="book-float" aria-label="Call Lakeside Grooming">')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 20. Limpieza: tel: links no necesitan target=_blank/rel=noopener
# ---------------------------------------------------------------------------
h = h.replace('href="tel:+18502964443" target="_blank" rel="noopener"', 'href="tel:+18502964443"')
print("CLEANUP tel links done")


# ---------------------------------------------------------------------------
# 21. Traduccion ES real para todos los textos NUEVOS (bilingue obligatorio)
# ---------------------------------------------------------------------------
T = {
    "4.6 out of 5 · 106 reviews on Google": "4.6 de 5 · 106 reseñas en Google",
    "4.6 · 106 reviews on Google": "4.6 · 106 reseñas en Google",
    "A de-shedding treatment to cut down on loose fur at home, plus teeth cleaning and flea and tick treatment when your pet needs it.":
        "Un tratamiento antipelusa para reducir el pelo suelto en casa, además de limpieza dental y tratamiento contra pulgas y garrapatas cuando tu mascota lo necesite.",
    "A fast in-and-out for pets that just need their nails trimmed and ears cleaned between full grooming appointments.":
        "Una visita rápida para mascotas que solo necesitan corte de uñas y limpieza de oídos entre citas de grooming completo.",
    "A full bath, blow-dry and brush-out to keep your pet's coat fresh and clean between full grooms, plus a quick nail trim.":
        "Un baño completo, secado y cepillado para mantener el pelaje de tu mascota fresco y limpio entre grooming completos, más un corte de uñas rápido.",
    "A gentle bath, blow-dry and the haircut or trim you asked for, done at a pace that keeps nervous pets relaxed.":
        "Un baño suave, secado y el corte que pediste, a un ritmo que mantiene relajadas a las mascotas más nerviosas.",
    "A groom as calm as": "Un grooming tan tranquilo",
    "Address": "Dirección",
    "Bath &amp; Brush": "Bath &amp; Brush",
    "Bath &amp; Care": "Baño y Cuidado",
    "Bath &amp; style": "Baño y estilo",
    "Bath, blow-dry, a breed-standard or custom haircut, sanitary trim, nail trim and ear cleaning, done start to finish by the team.":
        "Baño, secado, corte según la raza o estilo personalizado, recorte sanitario, corte de uñas y limpieza de oídos, de principio a fin.",
    "Breed-standard haircut": "Corte estándar de raza",
    "Brush-out": "Cepillado",
    "Calm hands. Happy tails.": "Manos tranquilas. Colas felices.",
    "Call": "Llamar",
    "Call (850) 296-4443": "Llama al (850) 296-4443",
    "Call (850) 296-4443 or stop by N Monroe Street to find a time that works, walk-ins welcome when the schedule allows.":
        "Llama al (850) 296-4443 o pasa por N Monroe Street para encontrar un horario, se aceptan visitas sin cita cuando el horario lo permite.",
    "Call (850) 296-4443 to find a time with Chantal, Tori, Robin or Tyler, Monday to Friday 6:30 AM to 4 PM, or Saturday 6:30 AM to 1 PM.":
        "Llama al (850) 296-4443 para encontrar un horario con Chantal, Tori, Robin o Tyler, de lunes a viernes de 6:30 AM a 4 PM, o sábado de 6:30 AM a 1 PM.",
    "Call for pricing": "Llama para precios",
    "Call to book": "Llama para reservar",
    "Cat grooming": "Grooming para gatos",
    "Chantal grooming Tallahassee pets": "Chantal cuidando mascotas en Tallahassee",
    "Chantal Celske opened Lakeside Grooming after starting her career in 1993, and the salon on N Monroe Street has been a fixture for Tallahassee pet owners ever since. Stylists Tori and Robin, along with groomer Tyler, handle everything from a quick bath to a full breed-standard haircut, always at the unhurried pace nervous dogs and cats need.":
        "Chantal Celske abrió Lakeside Grooming tras comenzar su carrera en 1993, y el salón en N Monroe Street ha sido un punto de referencia para los dueños de mascotas de Tallahassee desde entonces. Las estilistas Tori y Robin, junto con el groomer Tyler, se encargan de todo, desde un baño rápido hasta un corte completo según la raza, siempre al ritmo tranquilo que necesitan los perros y gatos más nerviosos.",
    "Coat &amp; dental": "Pelaje y dental",
    "Contact": "Contacto",
    "Custom style trim": "Corte de estilo personalizado",
    "De-shedding &amp; Teeth Cleaning": "Antipelusa y Limpieza Dental",
    "De-shedding treatment": "Tratamiento antipelusa",
    "Dog &amp; cat grooming in Tallahassee, FL. Walk-ins welcome when the schedule allows.":
        "Grooming para perros y gatos en Tallahassee, FL. Se aceptan visitas sin cita cuando el horario lo permite.",
    "Ear cleaning": "Limpieza de oídos",
    "Every pet gets a calm hello first, so the team can check coat, skin and temperament before choosing the right approach.":
        "Cada mascota recibe primero un saludo tranquilo, para que el equipo pueda revisar pelaje, piel y temperamento antes de elegir el enfoque adecuado.",
    "Everyday care": "Cuidado diario",
    "Extra Care": "Cuidados Extra",
    "Flea &amp; tick treatment": "Tratamiento contra pulgas y garrapatas",
    "Follow": "Síguenos",
    "Groomers": "Estilistas",
    "Haircut &amp; Style": "Corte y Estilo",
    "Full bath &amp; blow-dry": "Baño completo y secado",
    "Full Service Haircut": "Full Service Haircut",
    "Full menu and current pricing available by phone. Every groom is tailored to your pet's breed, coat and temperament.":
        "Menú completo y precios actuales disponibles por teléfono. Cada grooming se adapta a la raza, el pelaje y el temperamento de tu mascota.",
    "Get directions": "Cómo llegar",
    "Give us a call": "Llámanos",
    "Google review": "Reseña de Google",
    "Grooming since": "Cuidando mascotas desde",
    "Happy": "Mascotas",
    "Hours": "Horario",
    "Meet &amp; greet": "Bienvenida",
    "Meet the team": "Conoce al equipo",
    "Monday to Friday, 6:30 AM to 4:00 PM. Saturday 6:30 AM to 1:00 PM. Closed Sunday.":
        "Lunes a viernes, de 6:30 AM a 4:00 PM. Sábado de 6:30 AM a 1:00 PM. Cerrado los domingos.",
    "Most requested": "Lo más solicitado",
    "Mon-Fri · Sat until 1pm": "Lun-Vie · Sáb hasta la 1pm",
    "Nail Trim &amp; Ear Cleaning": "Uñas y Limpieza de Oídos",
    "Nail trim or grind": "Corte o limado de uñas",
    "Nails trimmed, ears cleaned, and a pet that goes home looking, and feeling, like new, just like the reviews describe.":
        "Uñas cortadas, oídos limpios, y una mascota que vuelve a casa luciendo, y sintiéndose, como nueva, tal como cuentan las reseñas.",
    "One call books": "Una llamada agenda",
    "Open": "Abierto",
    "Paw pad clean-up": "Limpieza de almohadillas",
    "pets": "felices",
    "Pricing depends on breed, size and coat condition. Call (850) 296-4443 for an exact quote.":
        "El precio depende de la raza, el tamaño y el estado del pelaje. Llama al (850) 296-4443 para una cotización exacta.",
    "Quick visit": "Visita rápida",
    "Read all 106 reviews on Google": "Lee las 106 reseñas en Google",
    "reviews on Google": "reseñas en Google",
    "Sanitary trim": "Recorte sanitario",
    "See the latest grooms and Reels from the team, and message any questions before your visit.":
        "Mira los últimos grooming y Reels del equipo, y escribe cualquier duda antes de tu visita.",
    "Services for": "Servicios para",
    "Tails wagging home": "Colas felices de vuelta a casa",
    "Tallahassee, FL · Dog &amp; Cat Grooming": "Tallahassee, FL · Grooming Canino y Felino",
    "Teeth cleaning": "Limpieza dental",
    "The result: a 4.6-star rating across 106 Google reviews, a Community's Choice Award for Best Pet Grooming Company in Tallahassee, and pet owners who come back because the team is kind, communicates well, and keeps prices fair.":
        "El resultado: una calificación de 4.6 estrellas en 106 reseñas de Google, un premio Community's Choice como Mejor Empresa de Grooming de Mascotas en Tallahassee, y dueños que siguen volviendo porque el equipo es amable, comunica bien y mantiene precios justos.",
    "Three decades of": "Tres décadas de",
    "Visit us in": "Visítanos en",
    "What pet owners": "Lo que dicen los",
    "a calmer groom": "un grooming más tranquilo",
    "a morning ": "una mañana ",
    "are saying": "dueños de mascotas",
    "by the lake": "junto al lago",
    "Owner Chantal Celske has been grooming pets since 1993, and her team, including Tori, Robin and Tyler, brings that same patient, unhurried care to every dog and cat that comes through the door on N Monroe Street, no matter how nervous they start out.":
        "La dueña Chantal Celske ha estado cuidando mascotas desde 1993, y su equipo, incluyendo a Tori, Robin y Tyler, brinda ese mismo cuidado paciente y sin prisas a cada perro y gato que llega a N Monroe Street, sin importar lo nervioso que esté al principio.",
    "patient hands": "manos pacientes",
    "to finish": "hasta el final",
    "Your visit, start": "Tu visita, de inicio",
}

_missing = []
for _en, _es in T.items():
    _pat = f'data-es="{_en}" data-en="{_en}"'
    _new = f'data-es="{_es}" data-en="{_en}"'
    if _pat in h:
        h = h.replace(_pat, _new)
    else:
        _missing.append(_en)
assert not _missing, "missing ES translations for: " + repr(_missing)
print("TRANSLATE ES done,", len(T), "strings")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(h)
print("FINAL WRITE done ->", PATH)
