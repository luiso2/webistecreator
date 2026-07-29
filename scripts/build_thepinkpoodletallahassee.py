import re
import shutil

SLUG = "the-pink-poodle-tallahassee"
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
# 2. Paleta: plum-pink (lashbloom) -> raspberry/berry pink (The Pink Poodle)
# ---------------------------------------------------------------------------
HEX_PALETTE = [
    ("#a04a72", "#c22a72"),  # accent-deep
    ("#5c2140", "#6e1240"),  # btn-3d sole darkest
    ("#f0bed7", "#f6c3dc"),  # dark-band shine/orb/stars accent
    ("#faf2f6", "#fdf1f6"),  # bg
    ("#c47a9c", "#e0568f"),  # accent-mid
    ("#8a5573", "#96225c"),  # dark-band btn shadow deep
    ("#f3e0ea", "#f9dceb"),  # bg-2 / accent-soft
    ("#d9a8c2", "#edb0cf"),  # orb-b
    ("#7d3457", "#96124f"),  # dark mid
    ("#5f2c48", "#7a1245"),  # step-num gradient end
    ("#33222c", "#2e1b26"),  # ink
    ("#fbf3f8", "#fdf3f8"),  # tile-cap text near-white
    ("#fbeff5", "#fdf1f7"),  # dark-band btn-3d gradient start lightest
    ("#f8dfeb", "#fbdcec"),  # dark-band shimmer 3rd stop
    ("#f6f1ea", "#fbeef4"),  # theme-color meta
    ("#f2d5e3", "#f8d3e6"),  # orb-a
    ("#f2cfe0", "#f8cfe3"),  # dark-band shimmer last stop
    ("#efd0e0", "#f5cfe3"),  # dark-band btn-3d gradient mid
    ("#e5c1d4", "#f0c2dc"),  # orb-c pale
    ("#dc9dbe", "#ea6ea3"),  # scroll-progress end stop
    ("#d3a2bc", "#e6a0c4"),  # dark-band btn-3d gradient end light
    ("#c9789f", "#de5992"),  # shimmer stop
    ("#b25a85", "#c62d74"),  # shimmer stop
    ("#2a1722", "#33101f"),  # cta-final bg gradient start
    ("#1f0f18", "#240a14"),  # cta-final bg gradient end
    ("#1c0f16", "#200b12"),  # footer bg
]
for old, new in HEX_PALETTE:
    c = h.count(old)
    assert c > 0, "hex not found: " + old
    h = h.replace(old, new)

RGBA_PALETTE = [
    ("rgba(160,74,114", "rgba(194,42,114"),    # accent-deep alpha
    ("rgba(51,34,44", "rgba(46,27,38"),        # ink alpha
    ("rgba(240,190,215", "rgba(246,195,220"),  # dark-band light accent alpha
    ("rgba(70,25,50", "rgba(74,14,44"),        # btn-3d darkest inset shadow
    ("rgba(250,242,246", "rgba(253,241,246"),  # bg alpha (nav scrolled)
    ("rgba(125,52,87", "rgba(150,18,79"),      # dark mid alpha
    ("rgba(253,246,250", "rgba(254,242,248"),  # surface alpha
    ("rgba(40,16,30", "rgba(46,10,28"),        # tile-cap gradient dark
    ("rgba(233,205,186", "rgba(240,201,217"),  # dark-band accent-ghost
    ("rgba(185,138,128", "rgba(185,103,143"),  # dark-band orb-b
]
for old, new in RGBA_PALETTE:
    c = h.count(old)
    assert c > 0, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)
print("PALETTE done")

# ---------------------------------------------------------------------------
# 3. Globales: no hay booking platform -> tel: + maps. IG.
# ---------------------------------------------------------------------------
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_TEL = "tel:+18506923979"
c = h.count(OLD_BOOK)
assert c >= 10, c
h = h.replace(OLD_BOOK, NEW_TEL)

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
NEW_IG_URL = "https://www.instagram.com/pink_poodle_tally/"
c = h.count(OLD_IG_URL)
assert c >= 3, c
h = h.replace(OLD_IG_URL, NEW_IG_URL)

OLD_IG_HANDLE = "@_lashbloom"
NEW_IG_HANDLE = "@pink_poodle_tally"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, NEW_IG_HANDLE)
print("GLOBALS done")

NEW_MAPS = "https://www.google.com/maps?q=3048+W+Tharpe+St+%237,+Tallahassee,+FL+32303"

# ---------------------------------------------------------------------------
# 4. HEAD: title, meta, og, favicon, JSON-LD
# ---------------------------------------------------------------------------
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>The Pink Poodle · Dog &amp; Cat Grooming in Tallahassee, FL | 4.7 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="The Pink Poodle, Tallahassee FL: full-service dog and cat grooming with Keili, Bailie and the team. 4.7 stars across 69 Google reviews. Call to book." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="The Pink Poodle · Dog &amp; Cat Grooming in Tallahassee, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Full-service dog and cat grooming. 4.7 on Google with 69 reviews. Call to book." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/gallery-02-pomeranian.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/gallery-02-pomeranian.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "PetGroomer",
    "name": "The Pink Poodle",
    "description": "Full-service pet grooming salon in Tallahassee, FL for dogs and cats of every breed and size: bath and brush, full groom, nail trim, ear cleaning and de-shedding treatments.",
    "address": { "@type": "PostalAddress", "streetAddress": "3048 W Tharpe St #7", "addressLocality": "Tallahassee", "addressRegion": "FL", "postalCode": "32303", "addressCountry": "US" },
    "telephone": "+1-850-692-3979",
    "sameAs": ["https://www.instagram.com/pink_poodle_tally/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "69", "bestRating": "5" },
    "openingHoursSpecification": { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "18:00" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Grooming services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bath &amp; Brush" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Full Service Groom" } },
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
# El esqueleto ya trae <html lang="en"> y applyLang(lang === 'en' ? 'en' : 'es')
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done (ya en default)")

# ---------------------------------------------------------------------------
# 6. NAV (logo monograma + wordmark + preloader)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,42,114,0.35)]" />',
    '<img src="assets/gallery-02-pomeranian.jpg" alt="The Pink Poodle" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,42,114,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">The <span class="text-[color:var(--accent-deep)]">Pink Poodle</span></span>')
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">PP</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">The Pink Poodle</span>')
print("NAV done")

# NAV CTA (Reservar cita -> tel) x2 (desktop + mobile), texto igual, solo href ya cambio via OLD_BOOK global.
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
    'data-es="Pretty on the outside, loved on the inside." data-en="Pretty on the outside, loved on the inside.">Pretty on the outside, loved on the inside.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Grooming your pet will" data-en="Grooming your pet will">Grooming your pet will</span><br /><span data-es="actually " data-en="actually ">actually </span><span class="text-shine" data-es="enjoy" data-en="enjoy">enjoy</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Bath, full grooms, nail trims and de-shedding for dogs and cats of every breed, in a calm pink studio on Tharpe Street. Keili, Bailie and the team have been making Tallahassee pets beautiful for years, at prices neighbors keep coming back for." data-en="Bath, full grooms, nail trims and de-shedding for dogs and cats of every breed, in a calm pink studio on Tharpe Street. Keili, Bailie and the team have been making Tallahassee pets beautiful for years, at prices neighbors keep coming back for.">Bath, full grooms, nail trims and de-shedding for dogs and cats of every breed, in a calm pink studio on Tharpe Street. Keili, Bailie and the team have been making Tallahassee pets beautiful for years, at prices neighbors keep coming back for.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.7 · 69 reviews on Google" data-en="4.7 · 69 reviews on Google">4.7 · 69 reviews on Google</span>')
rep('''<a href="''' + NEW_TEL + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            ''' + NEW_IG_HANDLE + '''
          </a>''',
    '''<a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Call (850) 692-3979" data-en="Call (850) 692-3979">Call (850) 692-3979</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <span data-es="Get directions" data-en="Get directions">Get directions</span>
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/hero-poodle.jpg" alt="Freshly groomed poodle mix relaxing on a pink backdrop at The Pink Poodle" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Open today" data-en="Open today">Open today</p>
            <p class="font-display text-lg">8am - 6pm</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Mon-Sat · Walk-ins welcome" data-en="Mon-Sat · Walk-ins welcome">Mon-Sat · Walk-ins welcome</p>''')
print("HERO done")

# ---------------------------------------------------------------------------
# 8. STRIP DE CONFIANZA
# ---------------------------------------------------------------------------
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="69">69</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl" data-es="Dogs" data-en="Dogs">Dogs</span> <span class="text-shine">&amp;</span> <span data-es="Cats" data-en="Cats">Cats</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="All breeds, all sizes" data-en="All breeds, all sizes">All breeds, all sizes</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">Keili <span class="text-shine">&amp;</span> Bailie</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Meet your groomers" data-en="Meet your groomers">Meet your groomers</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Tallahassee</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">W Tharpe St #7</p></div>')
print("STRIP done")

# ---------------------------------------------------------------------------
# 9. MARQUEE (x2, cada palabra aparece x4)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ("Classic Set", "Bath &amp; Brush"),
    ("Hybrid Set", "Full Groom"),
    ("Volume Set", "Nail Trim"),
    ("Mega Volume", "De-shedding"),
    ("Bottom Lashes", "Ear Cleaning"),
    ("West Palm Beach, FL", "Tallahassee, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ---------------------------------------------------------------------------
# 10. LA EXPERIENCIA
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-01-goldendoodle.jpg" alt="Goldendoodle freshly groomed and sitting on the table at The Pink Poodle" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/about-02-blackpoodle.jpg" alt="Curly black poodle mix on the grooming table at The Pink Poodle" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="A pink studio" data-en="A pink studio">A pink studio</span><br /><span class="text-shine" data-es="your pet will love" data-en="your pet will love">your pet will love</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="The Pink Poodle is a full-service grooming salon on W Tharpe Street, run by a team that includes Keili and Bailie. Dogs and cats of every breed and size come through their pink-walled studio for a bath, a full groom, or just a nail trim, always with patience for the nervous ones." data-en="The Pink Poodle is a full-service grooming salon on W Tharpe Street, run by a team that includes Keili and Bailie. Dogs and cats of every breed and size come through their pink-walled studio for a bath, a full groom, or just a nail trim, always with patience for the nervous ones.">The Pink Poodle is a full-service grooming salon on W Tharpe Street, run by a team that includes Keili and Bailie. Dogs and cats of every breed and size come through their pink-walled studio for a bath, a full groom, or just a nail trim, always with patience for the nervous ones.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="The result: 4.7 stars across 69 reviews on Google, and owners who keep coming back because the prices are fair and their pets actually leave happy." data-en="The result: 4.7 stars across 69 reviews on Google, and owners who keep coming back because the prices are fair and their pets actually leave happy.">The result: 4.7 stars across 69 reviews on Google, and owners who keep coming back because the prices are fair and their pets actually leave happy.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="69">69</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reviews" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine" data-es="Mon-Sat" data-en="Mon-Sat">Mon-Sat</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="8am to 6pm" data-en="8am to 6pm">8am to 6pm</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,42,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/gallery-02-pomeranian.jpg" alt="The Pink Poodle" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(194,42,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Keili &amp; Bailie · <span class="text-[color:var(--ink-40)]" data-es="Groomers" data-en="Groomers">Groomers</span></span>')
print("EXPERIENCIA done")

# ---------------------------------------------------------------------------
# 11. EL METODO
# ---------------------------------------------------------------------------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Your visit, step" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="by step" data-en="by step">by step</span>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Call to book" data-en="Call to book">Call to book</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Call or stop by W Tharpe Street to pick a time that works, walk-ins welcome when there is room." data-en="Call or stop by W Tharpe Street to pick a time that works, walk-ins welcome when there is room.">Call or stop by W Tharpe Street to pick a time that works, walk-ins welcome when there is room.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Check-in &amp; assessment" data-en="Check-in &amp; assessment">Check-in &amp; assessment</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Coat, skin and temperament get a quick look before choosing the shampoo, the cut and the pace your pet needs." data-en="Coat, skin and temperament get a quick look before choosing the shampoo, the cut and the pace your pet needs.">Coat, skin and temperament get a quick look before choosing the shampoo, the cut and the pace your pet needs.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Bath &amp; groom" data-en="Bath &amp; groom">Bath &amp; groom</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="A gentle bath, blow-dry, breed-appropriate haircut, ear cleaning and a nail trim, at a pace that keeps nervous pets calm." data-en="A gentle bath, blow-dry, breed-appropriate haircut, ear cleaning and a nail trim, at a pace that keeps nervous pets calm.">A gentle bath, blow-dry, breed-appropriate haircut, ear cleaning and a nail trim, at a pace that keeps nervous pets calm.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Ready for pickup" data-en="Ready for pickup">Ready for pickup</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Your pet goes home looking (and smelling) brand new, hot mess to gorgeous, just like the reviews describe." data-en="Your pet goes home looking (and smelling) brand new, hot mess to gorgeous, just like the reviews describe.">Your pet goes home looking (and smelling) brand new, hot mess to gorgeous, just like the reviews describe.</p>''')
print("METODO done")

# ---------------------------------------------------------------------------
# 12. SERVICIOS (header + grid completo por regex; solo nombres, sin precios inventados)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Services for" data-en="Services for">Services for</span> <span class="text-shine">dogs &amp; cats</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Full menu and current pricing available by phone. Every groom is tailored to your pet\'s breed, coat and temperament." data-en="Full menu and current pricing available by phone. Every groom is tailored to your pet\'s breed, coat and temperament.">Full menu and current pricing available by phone. Every groom is tailored to your pet\'s breed, coat and temperament.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Everyday care" data-en="Everyday care">Everyday care</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Bath &amp; Brush" data-en="Bath &amp; Brush">Bath &amp; Brush</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Warm bubble bath, blow dry and full coat brushing, plus nail trim and ear cleaning to keep coats fresh between full grooms." data-en="Warm bubble bath, blow dry and full coat brushing, plus nail trim and ear cleaning to keep coats fresh between full grooms.">Warm bubble bath, blow dry and full coat brushing, plus nail trim and ear cleaning to keep coats fresh between full grooms.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(194,42,114,0.4); box-shadow: 0 18px 50px rgba(46,27,38,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Service Groom" data-en="Full Service Groom">Full Service Groom</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Bath, blow dry, breed-appropriate haircut or style, sanitary trim, paw pad clean-up, ear cleaning and nail trim, start to finish." data-en="Bath, blow dry, breed-appropriate haircut or style, sanitary trim, paw pad clean-up, ear cleaning and nail trim, start to finish.">Bath, blow dry, breed-appropriate haircut or style, sanitary trim, paw pad clean-up, ear cleaning and nail trim, start to finish.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Quick visit" data-en="Quick visit">Quick visit</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Nail Trim &amp; Ear Care" data-en="Nail Trim &amp; Ear Care">Nail Trim &amp; Ear Care</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Nail trimming or grinding plus ear cleaning, a quick in-and-out for pets that just need their paws and ears looked after." data-en="Nail trimming or grinding plus ear cleaning, a quick in-and-out for pets that just need their paws and ears looked after.">Nail trimming or grinding plus ear cleaning, a quick in-and-out for pets that just need their paws and ears looked after.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Call for pricing" data-en="Call for pricing">Call for pricing</p></div>
            <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Call" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Coat &amp; dental" data-en="Coat &amp; dental">Coat &amp; dental</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="De-shedding &amp; Teeth Cleaning" data-en="De-shedding &amp; Teeth Cleaning">De-shedding &amp; Teeth Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="De-shedding treatment to cut down on loose fur at home, plus teeth cleaning and flea &amp; tick treatment when your pet needs it." data-en="De-shedding treatment to cut down on loose fur at home, plus teeth cleaning and flea &amp; tick treatment when your pet needs it.">De-shedding treatment to cut down on loose fur at home, plus teeth cleaning and flea &amp; tick treatment when your pet needs it.</p>
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
            <li class="flex items-center gap-2" data-es="Warm bubble bath" data-en="Warm bubble bath">Warm bubble bath</li>
            <li class="flex items-center gap-2" data-es="Blow dry &amp; coat brushing" data-en="Blow dry &amp; coat brushing">Blow dry &amp; coat brushing</li>
            <li class="flex items-center gap-2" data-es="Nail trim or grind" data-en="Nail trim or grind">Nail trim or grind</li>
            <li class="flex items-center gap-2" data-es="Ear plucking &amp; cleaning" data-en="Ear plucking &amp; cleaning">Ear plucking &amp; cleaning</li>
            <li class="flex items-center gap-2" data-es="Cologne &amp; bandana" data-en="Cologne &amp; bandana">Cologne &amp; bandana</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Haircut &amp; Style" data-en="Haircut &amp; Style">Haircut &amp; Style</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Breed standard haircut" data-en="Breed standard haircut">Breed standard haircut</li>
            <li class="flex items-center gap-2" data-es="All-over style haircut" data-en="All-over style haircut">All-over style haircut</li>
            <li class="flex items-center gap-2" data-es="Sanitary trim" data-en="Sanitary trim">Sanitary trim</li>
            <li class="flex items-center gap-2" data-es="Paw pad hair removal" data-en="Paw pad hair removal">Paw pad hair removal</li>
            <li class="flex items-center gap-2" data-es="Face, feet &amp; tail trim" data-en="Face, feet &amp; tail trim">Face, feet &amp; tail trim</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Extra Care" data-en="Extra Care">Extra Care</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="De-shedding treatment" data-en="De-shedding treatment">De-shedding treatment</li>
            <li class="flex items-center gap-2" data-es="Teeth cleaning" data-en="Teeth cleaning">Teeth cleaning</li>
            <li class="flex items-center gap-2" data-es="Flea &amp; tick treatment" data-en="Flea &amp; tick treatment">Flea &amp; tick treatment</li>
            <li class="flex items-center gap-2" data-es="Cat grooming" data-en="Cat grooming">Cat grooming</li>
            <li class="flex items-center gap-2" data-es="Express grooming (extra fee)" data-en="Express grooming (extra fee)">Express grooming (extra fee)</li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Pricing depends on breed, size and coat condition. Call (850) 692-3979 for an exact quote." data-en="Pricing depends on breed, size and coat condition. Call (850) 692-3979 for an exact quote.">Pricing depends on breed, size and coat condition. Call (850) 692-3979 for an exact quote.</span></p>')
print("SERVICIOS done")

# ---------------------------------------------------------------------------
# 13. GALERIA (header + grid completo por regex, solo 3 fotos reales curadas)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Happy" data-en="Happy">Happy</span> <span class="text-shine" data-es="pets" data-en="pets">pets</span>')
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

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[21/9] img-reveal"><span class="tile-cap" data-es="Two happy clients, bows included" data-en="Two happy clients, bows included">Two happy clients, bows included</span><img src="assets/gallery-01-two-dogs.jpg" alt="Two small dogs freshly groomed with bows, sitting together after their visit to The Pink Poodle" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="All smiles after the bath" data-en="All smiles after the bath">All smiles after the bath</span><img src="assets/gallery-02-pomeranian.jpg" alt="Pomeranian smiling after grooming at The Pink Poodle" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-square img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Sharp, clean lines" data-en="Sharp, clean lines">Sharp, clean lines</span><img src="assets/gallery-03-yorkie.jpg" alt="Yorkie with a neat breed haircut at The Pink Poodle" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. MARQUEE 2 (reverse) ya cubierto por MARQUEE_WORDS (rep_all, x8 total incl. este bloque)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 15. OPINIONES
# ---------------------------------------------------------------------------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What pet owners" data-en="What pet owners">What pet owners</span> <span class="text-shine" data-es="are saying" data-en="are saying">are saying</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★☆</span> &nbsp;<span data-es="4.7 out of 5 · 69 reviews on Google" data-en="4.7 out of 5 · 69 reviews on Google">4.7 out of 5 · 69 reviews on Google</span>')
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
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Claire may go in as a hot mess but, when she leaves, Keili and Bailie have made her beautiful! They\'re the best!"</blockquote>
          <figcaption class="text-sm"><span class="text-[color:var(--ink-40)]" data-es="Google review" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"My pup, Sadie, loves the ladies at Pink Poodle! She\'s always super nervous about getting her nails trimmed, but the groomers always make her feel comfortable."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Megan G.</span> <span class="text-[color:var(--ink-40)]">· Yelp</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Pink poodle is great been going there for years and best prices around."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">D.</span> <span class="text-[color:var(--ink-40)]">· Google</span></figcaption>
        </figure>''')
rep('<a href="' + NEW_TEL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="https://www.google.com/search?q=The+Pink+Poodle+Tallahassee+reviews" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 69 reviews on Google" data-en="Read all 69 reviews on Google">Read all 69 reviews on Google</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 16. UBICACION
# ---------------------------------------------------------------------------
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visit us in" data-en="Visit us in">Visit us in</span> <span class="text-shine">Tallahassee</span></h2>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,42,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Address" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">3048 W Tharpe St #7, Tallahassee, FL 32303</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,42,114,0.4)]" href="''' + NEW_MAPS + '''" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,42,114,0.4)]" href="tel:+18506923979" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Monday to Saturday, 8:00 AM to 6:00 PM. Closed Sunday. Walk-ins welcome when there is room." data-en="Monday to Saturday, 8:00 AM to 6:00 PM. Closed Sunday. Walk-ins welcome when there is room.">Monday to Saturday, 8:00 AM to 6:00 PM. Closed Sunday. Walk-ins welcome when there is room.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,42,114,0.4)]" href="tel:+18506923979" data-es="Call (850) 692-3979" data-en="Call (850) 692-3979">Call (850) 692-3979</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,42,114,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
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
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See the latest grooms from Keili, Bailie and the team, and DM any questions before your visit." data-en="See the latest grooms from Keili, Bailie and the team, and DM any questions before your visit.">See the latest grooms from Keili, Bailie and the team, and DM any questions before your visit.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(194,42,114,0.4)]" href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener">''' + NEW_IG_HANDLE + '''</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: The Pink Poodle, 3048 W Tharpe St #7, Tallahassee FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ---------------------------------------------------------------------------
# 17. CTA FINAL
# ---------------------------------------------------------------------------
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pretty on the outside, loved on the inside." data-en="Pretty on the outside, loved on the inside.">Pretty on the outside, loved on the inside.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Your pet\'s next groom" data-en="Your pet\'s next groom">Your pet\'s next groom</span> <span class="text-shine" data-es="is one call away" data-en="is one call away">is one call away</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Call (850) 692-3979 to grab a spot with Keili, Bailie and the team, Monday to Saturday, 8am to 6pm." data-en="Call (850) 692-3979 to grab a spot with Keili, Bailie and the team, Monday to Saturday, 8am to 6pm.">Call (850) 692-3979 to grab a spot with Keili, Bailie and the team, Monday to Saturday, 8am to 6pm.</p>')
rep('''<a href="tel:+18506923979" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="tel:+18506923979" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Call (850) 692-3979" data-en="Call (850) 692-3979">Call (850) 692-3979</a>
        <a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Follow on Instagram" data-en="Follow on Instagram">Follow on Instagram</a>''')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 18. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Pink Poodle</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(246,195,220,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/gallery-02-pomeranian.jpg" alt="The Pink Poodle" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(246,195,220,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">The Pink Poodle</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Dog &amp; cat grooming in Tallahassee, FL. Walk-ins welcome when there is room." data-en="Dog &amp; cat grooming in Tallahassee, FL. Walk-ins welcome when there is room.">Dog &amp; cat grooming in Tallahassee, FL. Walk-ins welcome when there is room.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="tel:+18506923979" target="_blank" rel="noopener" class="hover:text-[#f6c3dc]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>3048 W Tharpe St #7, Tallahassee, FL 32303</p>
        <p><a href="tel:+18506923979" class="hover:text-[#f6c3dc]" data-es="Call (850) 692-3979" data-en="Call (850) 692-3979">Call (850) 692-3979</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f6c3dc]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_IG_URL + '''" target="_blank" rel="noopener" class="hover:text-[#f6c3dc]">Instagram · ''' + NEW_IG_HANDLE + '''</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 The Pink Poodle.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 19. Boton flotante: llamar
# ---------------------------------------------------------------------------
rep('<a href="tel:+18506923979" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    '<a href="tel:+18506923979" class="book-float" aria-label="Call The Pink Poodle">')
print("BOOK-FLOAT done")

# ---------------------------------------------------------------------------
# 20. Limpieza: tel: links no necesitan target=_blank/rel=noopener (heredado
#     del replace global de OLD_BOOK). Quitarlo donde haya quedado.
# ---------------------------------------------------------------------------
h = h.replace('href="tel:+18506923979" target="_blank" rel="noopener"', 'href="tel:+18506923979"')
print("CLEANUP tel links done")


# ---------------------------------------------------------------------------
# 21. Traduccion ES real para todos los textos NUEVOS (bilingue obligatorio):
#     el esqueleto trae data-es=data-en identicos en el contenido que reescribi,
#     aqui se rellena data-es con espanol real, preservando data-en como esta.
# ---------------------------------------------------------------------------
T = {
    "4.7 out of 5 · 69 reviews on Google": "4.7 de 5 · 69 reseñas en Google",
    "4.7 · 69 reviews on Google": "4.7 · 69 reseñas en Google",
    "8am to 6pm": "8am a 6pm",
    "A gentle bath, blow-dry, breed-appropriate haircut, ear cleaning and a nail trim, at a pace that keeps nervous pets calm.":
        "Un baño suave, secado, corte según la raza, limpieza de oídos y corte de uñas, con calma para las mascotas más nerviosas.",
    "A pink studio": "Un estudio rosa",
    "Address": "Dirección",
    "All breeds, all sizes": "Todas las razas y tamaños",
    "All smiles after the bath": "Puras sonrisas después del baño",
    "All-over style haircut": "Corte de estilo completo",
    "Bath &amp; Brush": "Bath &amp; Brush",
    "Bath &amp; Care": "Baño y Cuidado",
    "Bath &amp; groom": "Baño y grooming",
    "Bath, blow dry, breed-appropriate haircut or style, sanitary trim, paw pad clean-up, ear cleaning and nail trim, start to finish.":
        "Baño, secado, corte según la raza o estilo, recorte sanitario, limpieza de almohadillas, limpieza de oídos y corte de uñas, de principio a fin.",
    "Bath, full grooms, nail trims and de-shedding for dogs and cats of every breed, in a calm pink studio on Tharpe Street. Keili, Bailie and the team have been making Tallahassee pets beautiful for years, at prices neighbors keep coming back for.":
        "Baño, grooming completo, corte de uñas y tratamiento antipelusa para perros y gatos de cualquier raza, en un estudio rosa y tranquilo en Tharpe Street. Keili, Bailie y el equipo llevan años embelleciendo a las mascotas de Tallahassee, con precios por los que los vecinos siguen volviendo.",
    "Blow dry &amp; coat brushing": "Secado y cepillado de pelaje",
    "Breed standard haircut": "Corte estándar de raza",
    "Call": "Llamar",
    "Call (850) 692-3979": "Llama al (850) 692-3979",
    "Call (850) 692-3979 to grab a spot with Keili, Bailie and the team, Monday to Saturday, 8am to 6pm.":
        "Llama al (850) 692-3979 para reservar tu espacio con Keili, Bailie y el equipo, de lunes a sábado, de 8am a 6pm.",
    "Call for pricing": "Llama para precios",
    "Call or stop by W Tharpe Street to pick a time that works, walk-ins welcome when there is room.":
        "Llama o pasa por W Tharpe Street para elegir un horario, se aceptan visitas sin cita cuando hay espacio.",
    "Call to book": "Llama para reservar",
    "Cat grooming": "Grooming para gatos",
    "Cats": "Gatos",
    "Check-in &amp; assessment": "Bienvenida y diagnóstico",
    "Coat &amp; dental": "Pelaje y dental",
    "Coat, skin and temperament get a quick look before choosing the shampoo, the cut and the pace your pet needs.":
        "Se revisa el pelaje, la piel y el temperamento antes de elegir el champú, el corte y el ritmo que tu mascota necesita.",
    "Cologne &amp; bandana": "Perfume y bandana",
    "Contact": "Contacto",
    "De-shedding &amp; Teeth Cleaning": "Antipelusa y Limpieza Dental",
    "De-shedding treatment": "Tratamiento antipelusa",
    "De-shedding treatment to cut down on loose fur at home, plus teeth cleaning and flea &amp; tick treatment when your pet needs it.":
        "Tratamiento antipelusa para reducir el pelo suelto en casa, además de limpieza dental y tratamiento contra pulgas y garrapatas cuando tu mascota lo necesite.",
    "Dog &amp; cat grooming in Tallahassee, FL. Walk-ins welcome when there is room.":
        "Grooming para perros y gatos en Tallahassee, FL. Se aceptan visitas sin cita cuando hay espacio.",
    "Dogs": "Perros",
    "Ear plucking &amp; cleaning": "Depilado y limpieza de oídos",
    "Everyday care": "Cuidado diario",
    "Express grooming (extra fee)": "Grooming exprés (costo extra)",
    "Extra Care": "Cuidados Extra",
    "Face, feet &amp; tail trim": "Recorte de cara, patas y cola",
    "Flea &amp; tick treatment": "Tratamiento contra pulgas y garrapatas",
    "Follow": "Síguenos",
    "Follow on Instagram": "Seguir en Instagram",
    "Full Service Groom": "Full Service Groom",
    "Full menu and current pricing available by phone. Every groom is tailored to your pet's breed, coat and temperament.":
        "Menú completo y precios actuales disponibles por teléfono. Cada grooming se adapta a la raza, el pelaje y el temperamento de tu mascota.",
    "Get directions": "Cómo llegar",
    "Google review": "Reseña de Google",
    "Groomers": "Groomers",
    "Grooming your pet will": "Un grooming que tu mascota",
    "Haircut &amp; Style": "Corte y Estilo",
    "Happy": "Mascotas",
    "Hours": "Horario",
    "Meet your groomers": "Conoce a tus groomers",
    "Mon-Sat": "Lun-Sáb",
    "Mon-Sat · Walk-ins welcome": "Lun-Sáb · Sin cita bienvenida",
    "Monday to Saturday, 8:00 AM to 6:00 PM. Closed Sunday. Walk-ins welcome when there is room.":
        "Lunes a sábado, de 8:00 AM a 6:00 PM. Cerrado los domingos. Se aceptan visitas sin cita cuando hay espacio.",
    "Most requested": "Lo más solicitado",
    "Nail Trim &amp; Ear Care": "Uñas y Cuidado de Oídos",
    "Nail trim or grind": "Corte o limado de uñas",
    "Nail trimming or grinding plus ear cleaning, a quick in-and-out for pets that just need their paws and ears looked after.":
        "Corte o limado de uñas más limpieza de oídos, una visita rápida para mascotas que solo necesitan atención en patas y oídos.",
    "Open today": "Abierto hoy",
    "Paw pad hair removal": "Depilado de almohadillas",
    "Pretty on the outside, loved on the inside.": "Hermosos por fuera, consentidos por dentro.",
    "Pricing depends on breed, size and coat condition. Call (850) 692-3979 for an exact quote.":
        "El precio depende de la raza, el tamaño y el estado del pelaje. Llama al (850) 692-3979 para una cotización exacta.",
    "Quick visit": "Visita rápida",
    "Read all 69 reviews on Google": "Lee las 69 reseñas en Google",
    "Ready for pickup": "Listo para recoger",
    "Reviews": "Reseñas",
    "Sanitary trim": "Recorte sanitario",
    "See the latest grooms from Keili, Bailie and the team, and DM any questions before your visit.":
        "Mira los últimos grooming de Keili, Bailie y el equipo, y escribe por DM cualquier duda antes de tu visita.",
    "Services for": "Servicios para",
    "Sharp, clean lines": "Líneas limpias y precisas",
    "Tallahassee, FL · Dog &amp; Cat Grooming": "Tallahassee, FL · Grooming Canino y Felino",
    "Teeth cleaning": "Limpieza dental",
    "The Pink Poodle is a full-service grooming salon on W Tharpe Street, run by a team that includes Keili and Bailie. Dogs and cats of every breed and size come through their pink-walled studio for a bath, a full groom, or just a nail trim, always with patience for the nervous ones.":
        "The Pink Poodle es un salón de grooming completo en W Tharpe Street, dirigido por un equipo que incluye a Keili y Bailie. Perros y gatos de cualquier raza y tamaño pasan por su estudio de paredes rosas para un baño, un grooming completo o solo un corte de uñas, siempre con paciencia para los más nerviosos.",
    "The result: 4.7 stars across 69 reviews on Google, and owners who keep coming back because the prices are fair and their pets actually leave happy.":
        "El resultado: 4.7 estrellas en 69 reseñas de Google, y dueños que siguen volviendo porque los precios son justos y sus mascotas de verdad salen felices.",
    "Two happy clients, bows included": "Dos clientas felices, con moños incluidos",
    "Visit us in": "Visítanos en",
    "Warm bubble bath": "Baño de burbujas tibio",
    "Warm bubble bath, blow dry and full coat brushing, plus nail trim and ear cleaning to keep coats fresh between full grooms.":
        "Baño de burbujas tibio, secado y cepillado completo del pelaje, más corte de uñas y limpieza de oídos para mantener el pelaje fresco entre grooming completos.",
    "What pet owners": "Lo que dicen los",
    "Your pet goes home looking (and smelling) brand new, hot mess to gorgeous, just like the reviews describe.":
        "Tu mascota vuelve a casa luciendo (y oliendo) como nueva, de un desastre a hermosa, tal como cuentan las reseñas.",
    "Your pet's next groom": "El próximo grooming de tu mascota",
    "Your visit, step": "Tu visita, paso",
    "actually ": "de verdad ",
    "are saying": "dueños de mascotas",
    "by step": "a paso",
    "enjoy": "disfrutará",
    "is one call away": "está a una llamada",
    "pets": "felices",
    "reviews on Google": "reseñas en Google",
    "your pet will love": "que tu mascota amará",
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
