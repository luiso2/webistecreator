import re
import os
import colorsys

SLUG = "mesubbim-boca-raton"
SRC = "templates/light-v2/index.html"
DST = f"output/{SLUG}/index.html"

h = open(SRC, encoding="utf-8").read()


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


# ============================================================
# 3. Globales: canal real = Square order link (pedidos reales) + tel: + Facebook real
# ============================================================
OLD_BOOK = "https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach"
NEW_ORDER = "https://mesubbim.square.site/s/order"
c = h.count(OLD_BOOK)
assert c >= 8, c
h = h.replace(OLD_BOOK, NEW_ORDER)

NEW_TEL = "tel:+15618496153"
NEW_FB = "https://www.facebook.com/mesubbimexpress/"

OLD_IG_URL = "https://www.instagram.com/_lashbloom/"
c = h.count(OLD_IG_URL)
assert c >= 4, c
h = h.replace(OLD_IG_URL, NEW_FB)

OLD_IG_HANDLE = "@_lashbloom"
c = h.count(OLD_IG_HANDLE)
assert c >= 2, c
h = h.replace(OLD_IG_HANDLE, "Facebook")
print("GLOBALS done")

NEW_ADDR = "7160 Beracasa Way, Del Mar Village, Boca Raton, FL 33433"
NEW_MAPS = "https://www.google.com/maps?q=7160+Beracasa+Way,+Boca+Raton,+FL+33433"
NEW_REVIEWS_URL = ("https://www.google.com/maps/place/Mesubbim/data=!4m7!3m6!1s0x88d91de625163a6d:"
                    "0x30517dc60b87a16f!8m2!3d26.3512547!4d-80.1567776!16s%2Fg%2F11p0h5dv1n!"
                    "19sChIJbToWJeYd2YgRb6GHC8Z9UTA")

# ============================================================
# 4. HEAD
# ============================================================
rep('<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Mesubbim · Kosher Bakery &amp; Deli in Boca Raton, FL | ORB Certified, 4.7 on Google</title>')
rep('<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Mesubbim, Boca Raton FL: kosher bakery, deli counter and Shabbat catering at Del Mar Village. Challah, babka, bourekas, schnitzel and more. ORB certified, Pas Yisroel bakery. 4.7 stars on Google. Order online or call." />')
rep('<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Mesubbim · Kosher Bakery &amp; Deli in Boca Raton, FL" />')
rep('<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Kosher bakery, deli counter and Shabbat catering. ORB certified. 4.7 stars on Google. Order online." />')
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/schnitzel-sandwich-hero.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/schnitzel-sandwich-hero.jpg" />')

OLD_JSONLD = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert OLD_JSONLD
NEW_JSONLD = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FoodEstablishment",
    "name": "Mesubbim",
    "description": "Kosher bakery, deli counter and Shabbat/holiday catering in Boca Raton, FL: sweet bakery (Matok), savory bakery (Malohach, Pas Yisroel), prepared Israeli foods and a kosher sandwich counter. ORB certified.",
    "address": { "@type": "PostalAddress", "streetAddress": "7160 Beracasa Way", "addressLocality": "Boca Raton", "addressRegion": "FL", "postalCode": "33433", "addressCountry": "US" },
    "telephone": "+1-561-849-6153",
    "servesCuisine": ["Kosher", "Israeli", "Bakery"],
    "sameAs": ["https://mesubbim.square.site/", "https://www.facebook.com/mesubbimexpress/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "25", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "11:00", "closes": "20:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday"], "opens": "11:00", "closes": "14:00" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Bakery, deli and catering", "itemListElement": [
      { "@type": "Offer", "price": "17.50", "priceCurrency": "USD", "itemOffered": { "@type": "Product", "name": "Chicken Schnitzel (per lb)" } },
      { "@type": "Offer", "price": "7.50", "priceCurrency": "USD", "itemOffered": { "@type": "Product", "name": "Challah" } },
      { "@type": "Offer", "price": "25.00", "priceCurrency": "USD", "itemOffered": { "@type": "Product", "name": "Beef Cigar, 15 ct" } },
      { "@type": "Offer", "price": "11.99", "priceCurrency": "USD", "itemOffered": { "@type": "Product", "name": "Chocolate Babka" } }
    ] }
  }
  </script>'''
h = h[:OLD_JSONLD.start()] + NEW_JSONLD + h[OLD_JSONLD.end():]
print("HEAD done")

# ============================================================
# 5. Idioma: EN default (ya lo es en light-v2)
# ============================================================
assert '<html lang="en" class="scroll-smooth">' in h
assert "applyLang(lang === 'es' ? 'es' : 'en');" in h
print("IDIOMA done")

# ============================================================
# 6. PRELOADER + NAV
# ============================================================
rep('<span class="pre-mono">LB</span>\n    <span class="pre-word">Lash Bloom</span>',
    '<span class="pre-mono">ME</span>\n    <span class="pre-word">Mesubbim</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
    '<img src="assets/raw/logo-icon.webp" alt="Mesubbim" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)] bg-white p-0.5" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Mesub<span class="text-[color:var(--accent-deep)]">bim</span></span>')
rep('<span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<span data-es="Order Online" data-en="Order Online">Order Online</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Order Online" data-en="Order Online">Order Online</a>')
print("NAV done")

# ============================================================
# 7. HERO
# ============================================================
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Boca Raton, FL · Kosher Bakery &amp; Deli" data-en="Boca Raton, FL · Kosher Bakery &amp; Deli">Boca Raton, FL · Kosher Bakery &amp; Deli</p>')
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="A traditional kosher experience." data-en="A traditional kosher experience.">A traditional kosher experience.</p>')
rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Kosher bakery, deli" data-en="Kosher bakery, deli">Kosher bakery, deli</span><br /><span data-es="and catering, made " data-en="and catering, made ">and catering, made </span><span class="text-shine" data-es="fresh" data-en="fresh">fresh</span>')
rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Challah, babka and bourekas from the Matok and Malohach bakery counters, schnitzel sandwiches and bowls from the Express lunch counter, and full Shabbat or event catering trays, all from one ORB-certified kosher kitchen in Boca Raton&#39;s Del Mar Village." data-en="Challah, babka and bourekas from the Matok and Malohach bakery counters, schnitzel sandwiches and bowls from the Express lunch counter, and full Shabbat or event catering trays, all from one ORB-certified kosher kitchen in Boca Raton&#39;s Del Mar Village.">Challah, babka and bourekas from the Matok and Malohach bakery counters, schnitzel sandwiches and bowls from the Express lunch counter, and full Shabbat or event catering trays, all from one ORB-certified kosher kitchen in Boca Raton&#39;s Del Mar Village.</p>')
rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="4.7 · 25 reviews on Google" data-en="4.7 · 25 reviews on Google">4.7 · 25 reviews on Google</span>')
rep('''<a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_FB + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            Facebook
          </a>''',
    '''<a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Order Online" data-en="Order Online">Order Online</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <span data-es="Call (561) 849-6153" data-en="Call (561) 849-6153">Call (561) 849-6153</span>
          </a>''')
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/schnitzel-sandwich-hero.jpg" alt="Mesubbim&#39;s signature schnitzel sandwich with roasted peppers and eggplant" class="blur-up w-full h-full object-cover" />')
rep('''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Volume Full Set</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>''',
    '''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Kosher certified" data-en="Kosher certified">Kosher certified</p>
            <p class="font-display text-lg">ORB &middot; Pas Yisroel</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Bakery, deli &amp; catering" data-en="Bakery, deli &amp; catering">Bakery, deli &amp; catering</p>''')
print("HERO done")

# ============================================================
# 8. STRIP DE CONFIANZA
# ============================================================
rep('<span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span></p></div>',
    '<span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="25">25</span> <span data-es="reviews on Google" data-en="reviews on Google">reviews on Google</span></p></div>')
rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<p class="font-display text-2xl">Matok <span class="text-shine">&amp;</span> Malohach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sweet &amp; savory bakery" data-en="Sweet &amp; savory bakery">Sweet &amp; savory bakery</p></div>')
rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<p class="font-display text-2xl">ORB <span class="text-shine" data-es="Certified" data-en="Certified">Certified</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Kosher certification" data-en="Kosher certification">Kosher certification</p></div>')
rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<p class="font-display text-2xl">Boca Raton</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">Del Mar Village</p></div>')
print("STRIP done")

# ============================================================
# 9. MARQUEE (x2 widgets, cada palabra x4)
# ============================================================
MARQUEE_WORDS = [
    ("Classic Set", "Challah"),
    ("Hybrid Set", "Babka"),
    ("Volume Set", "Schnitzel"),
    ("Mega Volume", "Bourekas"),
    ("Bottom Lashes", "Shabbat Catering"),
    ("West Palm Beach, FL", "Boca Raton, FL"),
]
for old, new in MARQUEE_WORDS:
    rep_all(f'<span class="marquee-word">{old}</span>', f'<span class="marquee-word">{new}</span>', expect=4)
print("MARQUEE done")

# ============================================================
# 10. LA EXPERIENCIA
# ============================================================
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/interior-counter.jpg" alt="Dining counter and pastry case inside Mesubbim in Boca Raton, FL" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/sandwich-counter-sign.jpg" alt="A schnitzel sandwich on deli paper with the Mesubbim counter sign in the background" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One kitchen," data-en="One kitchen,">One kitchen,</span><br /><span class="text-shine" data-es="every kosher craving" data-en="every kosher craving">every kosher craving</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Mesubbim bakes and cooks everything in one ORB-certified kosher kitchen at Del Mar Village: a sweet bakery (Matok), a Pas Yisroel savory bakery (Malohach), prepared Israeli dishes, and a lunch counter serving schnitzel sandwiches and bowls." data-en="Mesubbim bakes and cooks everything in one ORB-certified kosher kitchen at Del Mar Village: a sweet bakery (Matok), a Pas Yisroel savory bakery (Malohach), prepared Israeli dishes, and a lunch counter serving schnitzel sandwiches and bowls.">Mesubbim bakes and cooks everything in one ORB-certified kosher kitchen at Del Mar Village: a sweet bakery (Matok), a Pas Yisroel savory bakery (Malohach), prepared Israeli dishes, and a lunch counter serving schnitzel sandwiches and bowls.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="Customers mention the small things: olive oil instead of seed oil, real fresh lemon juice in the tahini, and portions that make hosting easier. The result is a 4.7-star rating across 25 reviews on Google." data-en="Customers mention the small things: olive oil instead of seed oil, real fresh lemon juice in the tahini, and portions that make hosting easier. The result is a 4.7-star rating across 25 reviews on Google.">Customers mention the small things: olive oil instead of seed oil, real fresh lemon juice in the tahini, and portions that make hosting easier. The result is a 4.7-star rating across 25 reviews on Google.</p>')
rep('''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
    '''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="25">25</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">ORB</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Kosher" data-en="Kosher">Kosher</p></div>''')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/logo-icon.webp" alt="Mesubbim" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.3)] bg-white p-0.5" loading="lazy" />\n            <span class="text-sm font-light">Mesubbim · <span class="text-[color:var(--ink-40)]" data-es="Kosher bakery &amp; deli" data-en="Kosher bakery &amp; deli">Kosher bakery &amp; deli</span></span>')
print("EXPERIENCIA done")

# ============================================================
# 11. EL METODO
# ============================================================
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="From the counter" data-en="From the counter">From the counter</span> <span class="text-shine" data-es="to your table" data-en="to your table">to your table</span>')
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="How it works" data-en="How it works">How it works</p>')
rep('''<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Order online or call" data-en="Order online or call">Order online or call</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Choose from the Matok sweet bakery, the Malohach savory bakery, or the weekly prepared-foods menu, on Mesubbim&#39;s own ordering site or by phone." data-en="Choose from the Matok sweet bakery, the Malohach savory bakery, or the weekly prepared-foods menu, on Mesubbim&#39;s own ordering site or by phone.">Choose from the Matok sweet bakery, the Malohach savory bakery, or the weekly prepared-foods menu, on Mesubbim&#39;s own ordering site or by phone.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Pick your size" data-en="Pick your size">Pick your size</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Trays, by-the-pound portions and 8 to 10 inch cake rounds for a crowd; larger cakes need 72 hours notice." data-en="Trays, by-the-pound portions and 8 to 10 inch cake rounds for a crowd; larger cakes need 72 hours notice.">Trays, by-the-pound portions and 8 to 10 inch cake rounds for a crowd; larger cakes need 72 hours notice.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Kosher, every step" data-en="Kosher, every step">Kosher, every step</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="The kitchen is ORB certified, and the savory bakery is Pas Yisroel, so every order meets the same standard." data-en="The kitchen is ORB certified, and the savory bakery is Pas Yisroel, so every order meets the same standard.">The kitchen is ORB certified, and the savory bakery is Pas Yisroel, so every order meets the same standard.</p>''')
rep('''<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>''',
    '''<h3 class="font-display text-xl mb-3" data-es="Pickup, delivery or catering" data-en="Pickup, delivery or catering">Pickup, delivery or catering</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Ready for a weekday lunch, a Shabbat table or a full event tray at the Del Mar Village counter." data-en="Ready for a weekday lunch, a Shabbat table or a full event tray at the Del Mar Village counter.">Ready for a weekday lunch, a Shabbat table or a full event tray at the Del Mar Village counter.</p>''')
print("METODO done")

# ============================================================
# 12. SERVICIOS
# ============================================================
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Tastes for" data-en="Tastes for">Tastes for</span> <span class="text-shine" data-es="every table" data-en="every table">every table</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Real prices as published on Mesubbim&#39;s own ordering menu. Order online for pickup or delivery, or call for same-day questions." data-en="Real prices as published on Mesubbim&#39;s own ordering menu. Order online for pickup or delivery, or call for same-day questions.">Real prices as published on Mesubbim&#39;s own ordering menu. Order online for pickup or delivery, or call for same-day questions.</p>')

services_grid_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = services_grid_re.search(h)
assert m, "services grid not found"

NEW_SERVICES_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(160,74,114,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Most requested" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Chicken Schnitzel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Breaded and fried to order in olive oil, not seed oil: the dish Mesubbim&#39;s own reviews mention most." data-en="Breaded and fried to order in olive oil, not seed oil: the dish Mesubbim&#39;s own reviews mention most.">Breaded and fried to order in olive oil, not seed oil: the dish Mesubbim&#39;s own reviews mention most.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$17.50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="per lb" data-en="per lb">per lb</p></div>
            <a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Order" data-en="Order">Order</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Shabbat staple" data-en="Shabbat staple">Shabbat staple</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Challah</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="The weekly braided loaf (parve), plus a Wedding Challah for simchas and larger events." data-en="The weekly braided loaf (parve), plus a Wedding Challah for simchas and larger events.">The weekly braided loaf (parve), plus a Wedding Challah for simchas and larger events.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$7.50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="parve loaf" data-en="parve loaf">parve loaf</p></div>
            <a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Order" data-en="Order">Order</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Catering platter" data-en="Catering platter">Catering platter</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Beef Cigar, 15 ct</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Crisp phyllo-wrapped beef cigars served with half a pound of tahini on the side, built for a crowd." data-en="Crisp phyllo-wrapped beef cigars served with half a pound of tahini on the side, built for a crowd.">Crisp phyllo-wrapped beef cigars served with half a pound of tahini on the side, built for a crowd.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25.00</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="15 pieces" data-en="15 pieces">15 pieces</p></div>
            <a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Order" data-en="Order">Order</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Gluten-free bakery" data-en="Gluten-free bakery">Gluten-free bakery</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Chocolate Mousse Cake</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Gluten-free, available dairy or parve. 8&quot; and 10&quot; rounds need 72 hours notice." data-en="Gluten-free, available dairy or parve. 8&quot; and 10&quot; rounds need 72 hours notice.">Gluten-free, available dairy or parve. 8&quot; and 10&quot; rounds need 72 hours notice.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-2xl text-shine">$2.99-$39</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="GF, dairy or parve" data-en="GF, dairy or parve">GF, dairy or parve</p></div>
            <a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Order" data-en="Order">Order</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Sweet Bakery &middot; Matok" data-en="Sweet Bakery &middot; Matok">Sweet Bakery &middot; Matok</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-3"><span>Chocolate Babka (Parve)</span><span class="text-[color:var(--ink-40)]">$11.99</span></li>
            <li class="flex items-center justify-between gap-3"><span>NY Style Cheesecake 6&quot; (Dairy)</span><span class="text-[color:var(--ink-40)]">$29.00</span></li>
            <li class="flex items-center justify-between gap-3"><span>Cannoli Platter, 32 ct (Dairy)</span><span class="text-[color:var(--ink-40)]">$65.00</span></li>
            <li class="flex items-center justify-between gap-3"><span>Churros, 2 ct (Parve)</span><span class="text-[color:var(--ink-40)]">$7.99</span></li>
            <li class="flex items-center justify-between gap-3"><span>Wedding Challah (Parve)</span><span class="text-[color:var(--ink-40)]">$28.75</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Savory Bakery &middot; Malohach" data-en="Savory Bakery &middot; Malohach">Savory Bakery &middot; Malohach</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-3"><span>Quiche, Spinach &amp; Feta</span><span class="text-[color:var(--ink-40)]">$7.99-$36</span></li>
            <li class="flex items-center justify-between gap-3"><span>Bourekas (Dairy/Parve)</span><span class="text-[color:var(--ink-40)]">$8.99</span></li>
            <li class="flex items-center justify-between gap-3"><span>Sweet Noodle Kugel</span><span class="text-[color:var(--ink-40)]">$38.00</span></li>
            <li class="flex items-center justify-between gap-3"><span>Potato Kugel, 9x13</span><span class="text-[color:var(--ink-40)]">$45.00</span></li>
            <li class="flex items-center justify-between gap-3"><span>Pita, pack of 5</span><span class="text-[color:var(--ink-40)]">$4.99</span></li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Prepared Israeli &amp; Catering" data-en="Prepared Israeli &amp; Catering">Prepared Israeli &amp; Catering</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center justify-between gap-3"><span>Beef Kebbeh, 1 lb</span><span class="text-[color:var(--ink-40)]">$28.00</span></li>
            <li class="flex items-center justify-between gap-3"><span>Chicken Tikka Masala, 2 lb</span><span class="text-[color:var(--ink-40)]">$36.00</span></li>
            <li class="flex items-center justify-between gap-3"><span>Potato &amp; Peas Samosa, 4 ct</span><span class="text-[color:var(--ink-40)]">$12.90</span></li>
            <li class="flex items-center justify-between gap-3"><span>Garlic Naan, 2 ct</span><span class="text-[color:var(--ink-40)]">$4.99</span></li>
            <li class="flex items-center justify-between gap-3"><span data-es="Homemade Hummus" data-en="Homemade Hummus">Homemade Hummus</span><span class="text-[color:var(--ink-40)]" data-es="market price" data-en="market price">market price</span></li>
          </ul>
        </div>
      </div>
      '''
h = h[:m.start()] + NEW_SERVICES_GRID + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Hanukkah pre-order is open through Nov 29 for pickup Dec 4-12. Full menu, sizes and same-day availability at the link above or by phone." data-en="Hanukkah pre-order is open through Nov 29 for pickup Dec 4-12. Full menu, sizes and same-day availability at the link above or by phone.">Hanukkah pre-order is open through Nov 29 for pickup Dec 4-12. Full menu, sizes and same-day availability at the link above or by phone.</span></p>')
print("SERVICIOS done")

# ============================================================
# 13. GALERIA
# ============================================================
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Real food," data-en="Real food,">Real food,</span> <span class="text-shine" data-es="real counter" data-en="real counter">real counter</span>')
rep('''<a href="''' + NEW_FB + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          Facebook
        </a>''',
    '''<a href="''' + NEW_FB + '''" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
          Facebook
        </a>''')

gallery_grid_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
gm = gallery_grid_re.search(h)
assert gm, "gallery grid not found"

NEW_GALLERY_GRID = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Sandwich counter spread" data-en="Sandwich counter spread">Sandwich counter spread</span><img src="assets/raw/sandwich-spread.jpg" alt="A spread of Mesubbim&#39;s schnitzel sandwiches with fries and roasted peppers" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Schnitzel bowl" data-en="Schnitzel bowl">Schnitzel bowl</span><img src="assets/raw/schnitzel-bowl.jpg" alt="A schnitzel bowl with hummus, pickled cabbage and herbs at Mesubbim" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Fresh off the counter" data-en="Fresh off the counter">Fresh off the counter</span><img src="assets/raw/sandwich-newspaper.jpg" alt="A halved schnitzel sandwich on deli paper at Mesubbim" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="GF chocolate mousse cake" data-en="GF chocolate mousse cake">GF chocolate mousse cake</span><img src="assets/raw/gf-chocolate-mousse-cake.jpg" alt="Gluten-free chocolate mousse cake from Mesubbim&#39;s Matok bakery" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="GF almond bar" data-en="GF almond bar">GF almond bar</span><img src="assets/raw/gf-almond-bar.jpg" alt="Gluten-free almond bars dipped in chocolate from Mesubbim" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gm.start()] + NEW_GALLERY_GRID + h[gm.end():]
print("GALERIA done")

# ============================================================
# 14. OPINIONES (4 reseñas reales de Google, grid 2x4 en vez de 3)
# ============================================================
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="What Boca Raton" data-en="What Boca Raton">What Boca Raton</span> <span class="text-shine" data-es="customers say" data-en="customers say">customers say</span>')
rep('<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span data-es="4.7 out of 5 · 25 reviews on Google" data-en="4.7 out of 5 · 25 reviews on Google">4.7 out of 5 · 25 reviews on Google</span>')

reviews_grid_re = re.compile(r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)', flags=re.S)
rm = reviews_grid_re.search(h)
assert rm, "reviews grid not found"

NEW_REVIEWS_GRID = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Love ordering from Mesubbim! Great food, amazing service, and perfect portions every time. My guests are always happy and keep asking where it&#39;s from. Everything is fresh, flavorful, and beautifully presented."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">Sivan Ravit</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Tastes amazing and they use olive oil in the pargit. Not seed oil. Also they use real fresh lemon juice in the tahini. Very good service too."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">R C</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I&#39;ll start by saying they deserve 10 stars. From the moment I call to get information to the end of my son&#39;s Aliyah LaTorah, they helped to make the event a success. The food was amazing, and you get so much for what you pay."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">OHANA Locksmith &amp; Security</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:330ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Messubbim&#39;s food is absolutely delicious!! The flavors were rich, and the freshness of the ingredients stood out. The perfect choice for a festive Shabbat gathering and beyond."</blockquote>
          <figcaption class="text-sm"><span class="font-medium">E Joy B</span> <span class="text-[color:var(--ink-40)]" data-es="Reseña de Google" data-en="Google review">Google review</span></figcaption>
        </figure>'''
h = h[:rm.start()] + NEW_REVIEWS_GRID + h[rm.end():]

rep('<a href="' + NEW_ORDER + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    '<a href="' + NEW_REVIEWS_URL + '" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Read all 25 reviews on Google" data-en="Read all 25 reviews on Google">Read all 25 reviews on Google</a>')
print("OPINIONES done")

# ============================================================
# 15. UBICACION
# ============================================================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visit us in" data-en="Visit us in">Visit us in</span> <span class="text-shine">Boca Raton</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">' + NEW_ADDR + '</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="' + NEW_MAPS + '" target="_blank" rel="noopener" data-es="Get directions" data-en="Get directions">Get directions</a>')
rep('''<div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
            </div>''',
    '''<div>
              <p class="font-medium mb-1" data-es="Hours &amp; ordering" data-en="Hours &amp; ordering">Hours &amp; ordering</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Sun-Thu 11:00 AM to 8:00 PM, Fri 11:00 AM to 2:00 PM, closed Saturday for Shabbat." data-en="Sun-Thu 11:00 AM to 8:00 PM, Fri 11:00 AM to 2:00 PM, closed Saturday for Shabbat.">Sun-Thu 11:00 AM to 8:00 PM, Fri 11:00 AM to 2:00 PM, closed Saturday for Shabbat.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" data-es="Order Online" data-en="Order Online">Order Online</a>
            </div>''')
rep('''<div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi's latest sets and DM any questions before your appointment.">See Yesi's latest sets and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="''' + NEW_FB + '''" target="_blank" rel="noopener">Facebook</a>
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
              <p class="font-medium mb-1" data-es="Facebook" data-en="Facebook">Facebook</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="See counter updates and message any questions before you order." data-en="See counter updates and message any questions before you order.">See counter updates and message any questions before you order.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,114,0.4)]" href="''' + NEW_FB + '''" target="_blank" rel="noopener">Facebook</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Map: Mesubbim, 7160 Beracasa Way, Boca Raton FL"
          src="''' + NEW_MAPS + '''&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''')
print("UBICACION done")

# ============================================================
# 16. CTA FINAL
# ============================================================
rep('<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    '<p class="reveal font-script text-2xl text-[color:var(--ink-60)] mb-5" data-es="A traditional kosher experience." data-en="A traditional kosher experience.">A traditional kosher experience.</p>')
rep('<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="One order" data-en="One order">One order</span> <span class="text-shine" data-es="feeds the table" data-en="feeds the table">feeds the table</span></h2>')
rep('<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    '<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es="Order online in seconds for pickup or delivery, from a Shabbat challah to a full catering tray for your next simcha." data-en="Order online in seconds for pickup or delivery, from a Shabbat challah to a full catering tray for your next simcha.">Order online in seconds for pickup or delivery, from a Shabbat challah to a full catering tray for your next simcha.</p>')
rep('''<a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>
        <a href="''' + NEW_FB + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>''',
    '''<a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Order Online" data-en="Order Online">Order Online</a>
        <a href="''' + NEW_TEL + '''" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Call (561) 849-6153" data-en="Call (561) 849-6153">Call (561) 849-6153</a>''')
print("CTA FINAL done")

# ============================================================
# 17. FOOTER
# ============================================================
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Mesubbim</span>')
rep('''<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>''',
    '''<img src="assets/raw/logo-icon.webp" alt="Mesubbim" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)] bg-white p-0.5" loading="lazy" />
          <span class="font-display text-lg tracking-[0.1em] uppercase">Mesubbim</span>
        </div>
        <p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" data-es="Kosher bakery, deli counter and catering in Boca Raton, FL. ORB certified." data-en="Kosher bakery, deli counter and catering in Boca Raton, FL. ORB certified.">Kosher bakery, deli counter and catering in Boca Raton, FL. ORB certified.</p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contacto" data-en="Contact">Contacto</p>
        <p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>
        <p><a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="hover:text-[#f0bed7]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Contact" data-en="Contact">Contact</p>
        <p>''' + NEW_ADDR + '''</p>
        <p><a href="''' + NEW_ORDER + '''" target="_blank" rel="noopener" class="hover:text-[#f0bec5]" data-es="Order online" data-en="Order online">Order online</a></p>
        <p><a href="''' + NEW_TEL + '''" class="hover:text-[#f0bec5]" data-es="Call (561) 849-6153" data-en="Call (561) 849-6153">Call (561) 849-6153</a></p>''')
rep('''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Síguenos" data-en="Follow">Síguenos</p>
        <p><a href="''' + NEW_FB + '''" target="_blank" rel="noopener" class="hover:text-[#f0bed7]">Instagram · Facebook</a></p>''',
    '''<p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)] mb-3" data-es="Follow" data-en="Follow">Follow</p>
        <p><a href="''' + NEW_FB + '''" target="_blank" rel="noopener" class="hover:text-[#f0bec5]">Facebook · Mesubbim Express</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Mesubbim.</p>')
print("FOOTER done")

# ============================================================
# 18. Boton flotante
# ============================================================
rep('<a href="' + NEW_ORDER + '" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#faf2f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>',
    '<a href="' + NEW_ORDER + '" target="_blank" rel="noopener" class="book-float" aria-label="Order online from Mesubbim">\n    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#faf2f3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>\n    <span class="book-float-label" data-es="Order Online" data-en="Order Online">Order Online</span>\n  </a>')
print("BOOK-FLOAT done")

# ============================================================
# 19. Traduccion ES
# ============================================================
T = {
    "Boca Raton, FL · Kosher Bakery &amp; Deli": "Boca Raton, FL · Panaderia y Deli Kosher",
    "A traditional kosher experience.": "Una experiencia kosher tradicional.",
    "Kosher bakery, deli": "Panaderia y deli kosher,",
    "and catering, made ": "y catering, hechos con ",
    "fresh": "frescura",
    "Challah, babka and bourekas from the Matok and Malohach bakery counters, schnitzel sandwiches and bowls from the Express lunch counter, and full Shabbat or event catering trays, all from one ORB-certified kosher kitchen in Boca Raton&#39;s Del Mar Village.":
        "Challah, babka y bourekas de las panaderias Matok y Malohach, sandwiches de schnitzel y bowls del mostrador Express, y bandejas completas de catering para Shabat o eventos, todo desde una sola cocina kosher certificada por ORB en Del Mar Village, Boca Raton.",
    "4.7 · 25 reviews on Google": "4.7 · 25 resenas en Google",
    "Order Online": "Ordenar en linea",
    "Call (561) 849-6153": "Llama al (561) 849-6153",
    "Kosher certified": "Certificado kosher",
    "Bakery, deli &amp; catering": "Panaderia, deli y catering",
    "Sweet &amp; savory bakery": "Panaderia dulce y salada",
    "Certified": "Certificado",
    "Kosher certification": "Certificacion kosher",
    "One kitchen,": "Una sola cocina,",
    "every kosher craving": "para todo antojo kosher",
    "Mesubbim bakes and cooks everything in one ORB-certified kosher kitchen at Del Mar Village: a sweet bakery (Matok), a Pas Yisroel savory bakery (Malohach), prepared Israeli dishes, and a lunch counter serving schnitzel sandwiches and bowls.":
        "Mesubbim hornea y cocina todo en una sola cocina kosher certificada por ORB en Del Mar Village: una panaderia dulce (Matok), una panaderia salada Pas Yisroel (Malohach), platos israelies preparados, y un mostrador de almuerzo con sandwiches de schnitzel y bowls.",
    "Customers mention the small things: olive oil instead of seed oil, real fresh lemon juice in the tahini, and portions that make hosting easier. The result is a 4.7-star rating across 25 reviews on Google.":
        "Los clientes mencionan los pequenos detalles: aceite de oliva en vez de aceite de semillas, jugo de limon fresco de verdad en el tahini, y porciones que facilitan recibir invitados. El resultado es una calificacion de 4.7 estrellas en 25 resenas de Google.",
    "Kosher bakery &amp; deli": "Panaderia y deli kosher",
    "From the counter": "Del mostrador",
    "to your table": "a tu mesa",
    "How it works": "Asi se trabaja",
    "Order online or call": "Ordena en linea o llama",
    "Choose from the Matok sweet bakery, the Malohach savory bakery, or the weekly prepared-foods menu, on Mesubbim&#39;s own ordering site or by phone.":
        "Elige entre la panaderia dulce Matok, la panaderia salada Malohach, o el menu semanal de comida preparada, en la propia pagina de pedidos de Mesubbim o por telefono.",
    "Pick your size": "Elige tu tamano",
    "Trays, by-the-pound portions and 8 to 10 inch cake rounds for a crowd; larger cakes need 72 hours notice.":
        "Bandejas, porciones por libra y tortas redondas de 8 a 10 pulgadas para un grupo grande; las tortas mas grandes necesitan 72 horas de aviso.",
    "Kosher, every step": "Kosher, en cada paso",
    "The kitchen is ORB certified, and the savory bakery is Pas Yisroel, so every order meets the same standard.":
        "La cocina esta certificada por ORB, y la panaderia salada es Pas Yisroel, asi que cada pedido cumple el mismo estandar.",
    "Pickup, delivery or catering": "Pickup, entrega o catering",
    "Ready for a weekday lunch, a Shabbat table or a full event tray at the Del Mar Village counter.":
        "Listo para un almuerzo entre semana, una mesa de Shabat o una bandeja completa de evento en el mostrador de Del Mar Village.",
    "Tastes for": "Sabores para",
    "every table": "cada mesa",
    "Real prices as published on Mesubbim&#39;s own ordering menu. Order online for pickup or delivery, or call for same-day questions.":
        "Precios reales publicados en el propio menu de pedidos de Mesubbim. Ordena en linea para pickup o entrega, o llama para preguntas del mismo dia.",
    "Most requested": "Lo mas pedido",
    "Breaded and fried to order in olive oil, not seed oil: the dish Mesubbim&#39;s own reviews mention most.":
        "Empanizado y frito al momento en aceite de oliva, no de semillas: el platillo que mas mencionan las propias resenas de Mesubbim.",
    "per lb": "por libra",
    "Order": "Ordenar",
    "Shabbat staple": "Infaltable de Shabat",
    "The weekly braided loaf (parve), plus a Wedding Challah for simchas and larger events.":
        "El pan trenzado de cada semana (parve), ademas de una Challah de Boda para simchas y eventos mas grandes.",
    "parve loaf": "pan parve",
    "Catering platter": "Bandeja de catering",
    "Crisp phyllo-wrapped beef cigars served with half a pound of tahini on the side, built for a crowd.":
        "Rollitos de carne envueltos en masa filo, crujientes, servidos con media libra de tahini aparte, pensados para un grupo grande.",
    "15 pieces": "15 piezas",
    "Gluten-free bakery": "Panaderia sin gluten",
    "Gluten-free, available dairy or parve. 8&quot; and 10&quot; rounds need 72 hours notice.":
        "Sin gluten, disponible dairy o parve. Las tortas de 8&quot; y 10&quot; necesitan 72 horas de aviso.",
    "GF, dairy or parve": "Sin gluten, dairy o parve",
    "Sweet Bakery &middot; Matok": "Panaderia Dulce &middot; Matok",
    "Savory Bakery &middot; Malohach": "Panaderia Salada &middot; Malohach",
    "Prepared Israeli &amp; Catering": "Comida Israeli Preparada y Catering",
    "Homemade Hummus": "Hummus Casero",
    "market price": "precio del dia",
    "Hanukkah pre-order is open through Nov 29 for pickup Dec 4-12. Full menu, sizes and same-day availability at the link above or by phone.":
        "El pre-pedido de Hanukkah esta abierto hasta el 29 de noviembre para recoger entre el 4 y el 12 de diciembre. Menu completo, tamanos y disponibilidad del mismo dia en el enlace de arriba o por telefono.",
    "Real food,": "Comida real,",
    "real counter": "mostrador real",
    "Sandwich counter spread": "Variedad del mostrador de sandwiches",
    "Schnitzel bowl": "Bowl de schnitzel",
    "Fresh off the counter": "Recien salido del mostrador",
    "GF chocolate mousse cake": "Torta de mousse de chocolate sin gluten",
    "GF almond bar": "Barra de almendra sin gluten",
    "What Boca Raton": "Lo que dice",
    "customers say": "Boca Raton",
    "4.7 out of 5 · 25 reviews on Google": "4.7 de 5 · 25 resenas en Google",
    "Read all 25 reviews on Google": "Lee las 25 resenas en Google",
    "Visit us in": "Visitanos en",
    "Get directions": "Como llegar",
    "Hours &amp; ordering": "Horario y pedidos",
    "Sun-Thu 11:00 AM to 8:00 PM, Fri 11:00 AM to 2:00 PM, closed Saturday for Shabbat.":
        "Dom-Jue 11:00 AM a 8:00 PM, Vie 11:00 AM a 2:00 PM, cerrado los sabados por Shabat.",
    "Facebook": "Facebook",
    "See counter updates and message any questions before you order.":
        "Mira las novedades del mostrador y escribe cualquier duda antes de ordenar.",
    "One order": "Un solo pedido",
    "feeds the table": "alimenta la mesa",
    "Order online in seconds for pickup or delivery, from a Shabbat challah to a full catering tray for your next simcha.":
        "Ordena en linea en segundos para pickup o entrega, desde una challah de Shabat hasta una bandeja completa de catering para tu proxima simcha.",
    "Kosher bakery, deli counter and catering in Boca Raton, FL. ORB certified.":
        "Panaderia, deli y catering kosher en Boca Raton, FL. Certificado por ORB.",
    "Contact": "Contacto",
    "Order online": "Ordena en linea",
    "Follow": "Siguenos",
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

# ============================================================
# PALETA (al final, sobre todo el contenido ya insertado): plum-pink (lashbloom)
# -> deep wine / pomegranate red (Mesubbim). Monocromo por hue-shift, mismo
# metodo que build_tnttreeservice.py. Hue elegido a partir de los puntos rojos
# del logo real de Mesubbim. Se hace al final para que TODO el HTML ya este
# en su lugar (nav, hero, servicios, etc.) y el shift cubra cualquier hex/rgba
# que se haya reescrito con los valores originales del esqueleto.
# ============================================================
m_css = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
assert m_css
badge_css = m_css.group(0)
h = h.replace(badge_css, '@@BADGE_CSS@@', 1)

m_html = re.search(r'<a href="https://merktop\.com".*?</a>', h, flags=re.S)
assert m_html
badge_html = m_html.group(0)
h = h.replace(badge_html, '@@BADGE_HTML@@', 1)

_HEXES = ['#1c0f16', '#1f0f18', '#2a1722', '#33222c', '#5c2140', '#5f2c48', '#7d3457',
          '#8a5573', '#a04a72', '#b25a85', '#c47a9c', '#c9789f', '#d3a2bc', '#d9a8c2',
          '#dc9dbe', '#e5c1d4', '#efd0e0', '#f0bed7', '#f2cfe0', '#f2d5e3', '#f3e0ea',
          '#f6f1ea', '#f8dfeb', '#faf2f6', '#fbeff5', '#fbf3f8']
_RGBAS = [(125, 52, 87), (160, 74, 114), (185, 138, 128), (233, 205, 186), (240, 190, 215),
          (250, 242, 246), (253, 246, 250), (51, 34, 44), (70, 25, 50)]

TARGET_HUE = 352 / 360.0
SAT_MUL = 1.0


def _shift_hex(hx):
    hx = hx.lstrip('#')
    r, g, b = int(hx[0:2], 16) / 255, int(hx[2:4], 16) / 255, int(hx[4:6], 16) / 255
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(TARGET_HUE, l, min(1.0, s * SAT_MUL))
    return '#%02x%02x%02x' % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def _shift_rgb(rgb):
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(TARGET_HUE, l, min(1.0, s * SAT_MUL))
    return (round(r2 * 255), round(g2 * 255), round(b2 * 255))


PALETTE = [(hx, _shift_hex(hx)) for hx in _HEXES]
for old, new in PALETTE:
    rep_all(old, new)

RGBA_FAMILIES = [(rgb, _shift_rgb(rgb)) for rgb in _RGBAS]
for (r1, g1, b1), (r2, g2, b2) in RGBA_FAMILIES:
    pattern = re.compile(r'rgba\(' + f'{r1},{g1},{b1}' + r',([0-9.]+)\)')
    n = len(pattern.findall(h))
    assert n > 0, f'sin matches para rgba({r1},{g1},{b1},*)'
    h = pattern.sub(lambda mm: f'rgba({r2},{g2},{b2},{mm.group(1)})', h)

h = h.replace('@@BADGE_CSS@@', badge_css, 1)
h = h.replace('@@BADGE_HTML@@', badge_html, 1)
print("PALETTE done")

with open(DST, "w", encoding="utf-8") as f:
    f.write(h)
print("PART 1 WRITE done ->", DST)
