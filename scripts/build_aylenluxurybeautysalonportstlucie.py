import re
import os
import shutil

SLUG = "aylen-luxury-beauty-salon-port-st-lucie"
os.makedirs(f"output/{SLUG}/assets", exist_ok=True)
shutil.copyfile("templates/light-v2/index.html", f"output/{SLUG}/index.html")
h = open(f"output/{SLUG}/index.html", encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:200]
    h = h.replace(a, b, n)


BOOKSY = "https://booksy.com/en-us/1429982_aylen-luxury-beauty-salon_nail-salon_16074_fort-pierce"
IG_URL = "https://www.instagram.com/aylen_luxury_beauty_salon/"
IG_HANDLE = "@aylen_luxury_beauty_salon"

# ---------- 1. Proteger el badge Merktop ----------
badge_m = re.search(r"\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n", h, flags=re.S)
assert badge_m
badge_block = badge_m.group(0)
h = h.replace(badge_block, "@@BADGE@@", 1)

# ---------- 2. Paleta: plum-pink -> burdeos + dorado rosado ----------
HEX_PAIRS = [
    ("a04a72", "6d1b30"),  # accent-deep -> deep burgundy wine
    ("c47a9c", "a8536a"),  # accent-mid -> dusty rose-wine
    ("5c2140", "431022"),  # shadow/suela 3d -> near-black wine
    ("7d3457", "551a30"),  # btn-3d bottom stop
    ("5f2c48", "3d0f1e"),  # text-shine mid-dark stop
    ("c9789f", "b06478"),  # text-shine stop2
    ("b25a85", "8a3552"),  # text-shine stop5
    ("faf2f6", "faf3ee"),  # bg
    ("f3e0ea", "f1ddd6"),  # bg-2
    ("33222c", "2d1f1a"),  # ink
    ("f6f1ea", "f5ede3"),  # theme-color meta
    ("fbf3f8", "faf1e9"),  # tile-cap text tint
    ("f2d5e3", "f0ddd2"),  # orb-a light
    ("d9a8c2", "caa393"),  # orb-b / dark-band shine stop3 (reused)
    ("e5c1d4", "e0cabd"),  # orb-c light
    ("dc9dbe", "b97a6a"),  # scroll-progress end stop
    ("f0bed7", "e8bf95"),  # dark-band main light accent (rose gold)
    ("f8dfeb", "f3ddb9"),  # dark-band shine stop2
    ("f2cfe0", "eed0a0"),  # dark-band shine stop5
    ("fbeff5", "faf1e2"),  # dark-band btn top stop
    ("efd0e0", "e8c894"),  # dark-band btn mid stop
    ("d3a2bc", "c9a06e"),  # dark-band btn bottom stop
    ("8a5573", "8a6238"),  # dark-band btn suela (bronze-gold)
    ("2a1722", "20100f"),  # CTA final bg top
    ("1f0f18", "160b0a"),  # CTA final bg bottom
    ("1c0f16", "190d0c"),  # footer bg
]
for old, new in HEX_PAIRS:
    assert h.count("#" + old) >= 1, "hex not found: " + old
    h = h.replace("#" + old, "#" + new)

RGBA_PAIRS = [
    ("160,74,114", "109,27,48"),      # accent-deep
    ("51,34,44", "45,31,26"),         # ink
    ("70,25,50", "67,16,34"),         # deep shadow family
    ("240,190,215", "232,191,149"),   # dark-band accent (rose gold)
    ("125,52,87", "85,26,48"),        # btn-3d bottom
    ("253,246,250", "253,247,241"),   # light surface
    ("250,242,246", "250,243,238"),   # nav scrolled bg
    ("233,205,186", "232,191,149"),   # dark-band ghost base
    ("185,138,128", "202,163,147"),   # dark-band orb-b
    ("40,16,30", "32,16,15"),         # tile-cap dark overlay
]
for old, new in RGBA_PAIRS:
    assert old in h, "rgba not found: " + old
    h = h.replace(old, new)

h = h.replace("@@BADGE@@", badge_block, 1)

# ---------- 3. Globales: Booksy / Instagram / logo ----------
rep(
    'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
    BOOKSY,
    n=h.count('https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach'),
)
rep('https://www.instagram.com/_lashbloom/', IG_URL, n=h.count('https://www.instagram.com/_lashbloom/'))
rep('@_lashbloom', IG_HANDLE, n=h.count('@_lashbloom'))

# ---------- 4. HEAD ----------
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Aylen Luxury Beauty Salon · Salon de Unas y Cejas en Port St. Lucie, FL | 5.0 en Booksy</title>',
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Aylen Luxury Beauty Salon, Port St. Lucie FL: unas acrilicas, polygel, pedicura de lujo, y cejas con henna y laminado. 5.0 perfecto en 49 resenas de Booksy. Reserva online." />',
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Aylen Luxury Beauty Salon · Salon de Belleza en Port St. Lucie, FL" />',
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Unas de lujo, pedicura y cejas con henna. 5.0 en Booksy. Reserva online." />',
)
rep(
    '<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-11.jpg" />',
)

ld_old_m = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S)
assert ld_old_m
ld_new = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": "Aylen Luxury Beauty Salon",
    "description": "Salon de belleza boutique en Port St. Lucie, FL, dentro de Mia Salon Suite: unas acrilicas, en gel y polygel, pedicura de lujo, depilacion y laminado de cejas con henna.",
    "address": { "@type": "PostalAddress", "streetAddress": "1763 St Lucie West Blvd, Suite 212", "addressLocality": "Port St. Lucie", "addressRegion": "FL", "postalCode": "34986", "addressCountry": "US" },
    "geo": { "@type": "GeoCoordinates", "latitude": 27.31641, "longitude": -80.39629 },
    "sameAs": ["''' + BOOKSY + '''", "''' + IG_URL + '''"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "49", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Servicios de unas y cejas", "itemListElement": [
      { "@type": "Offer", "price": "45", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Gel Manicure" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Acrylic Full Set - XL" } },
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Luxury Spa Pedicure" } },
      { "@type": "Offer", "price": "80", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Brow Lamination + Henna & Wax" } }
    ] }
  }
  </script>'''
h = h[: ld_old_m.start()] + ld_new + h[ld_old_m.end():]

# ---------- 5. Idioma: ES por defecto ----------
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep(
    "applyLang(lang === 'es' ? 'es' : 'en');",
    "applyLang(lang === 'en' ? 'en' : 'es');",
)

# ---------- 6. PRELOADER ----------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">AL</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Aylen Luxury</span>')

# ---------- 7. NAV ----------
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(109,27,48,0.35)]" />',
    '<img src="assets/raw/logo.jpg" alt="Aylen Luxury Beauty Salon" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(109,27,48,0.35)]" />',
)
rep(
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Aylen <span class="text-[color:var(--accent-deep)]">Luxury</span></span>',
)

# ---------- 8. HERO ----------
rep(
    'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Port St. Lucie, FL · Salon de Unas y Cejas" data-en="Port St. Lucie, FL · Nail &amp; Brow Salon">Port St. Lucie, FL · Salon de Unas y Cejas</p>',
)
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Belleza de lujo, uña por uña." data-en="Luxury beauty, nail by nail.">Belleza de lujo, uña por uña.</p>',
)
rep(
    '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Uñas de lujo y cejas" data-en="Luxury nails and brows">Luxury nails and brows</span><br /><span data-es="perfectas, hechas para " data-en="made to ">made to </span><span class="text-shine" data-es="brillar" data-en="shine">shine</span>',
)
rep(
    'data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Manicura en gel y acrílico, pedicura de lujo, y cejas con henna y laminado en un suite boutique dentro de Mia Salon Suite. Arlet diseña cada set a mano, con un 5.0 perfecto en 49 reseñas de Booksy." data-en="Gel and acrylic manicures, luxury pedicures, and henna brow treatments with lamination in a boutique suite inside Mia Salon Suite. Arlet hand-designs every set, with a perfect 5.0 across 49 Booksy reviews.">Manicura en gel y acrílico, pedicura de lujo, y cejas con henna y laminado en un suite boutique dentro de Mia Salon Suite. Arlet diseña cada set a mano, con un 5.0 perfecto en 49 reseñas de Booksy.</p>',
)
rep(
    'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 49 reseñas en Booksy" data-en="5.0 · 49 reviews on Booksy">5.0 · 49 reseñas en Booksy</span>',
)
rep(
    'data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    'data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
)
rep(
    '<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-11.jpg" alt="Diseño de uñas estilo sirena con conchas doradas hecho a mano en Aylen Luxury Beauty Salon" class="blur-up w-full h-full object-cover" />',
)
rep(
    'data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Volume Full Set</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    'data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Gel Manicure</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$45 · 1h" data-en="$45 · 1h">$45 · 1h</p>',
)

# ---------- 9. STRIP DE CONFIANZA ----------
rep(
    '<span data-count="86">86</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-count="49">49</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
)
rep(
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Uñas <span class="text-shine">&amp;</span> Cejas</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Gel · Acrílico · Henna" data-en="Gel · Acrylic · Henna">Gel · Acrílico · Henna</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">16 <span class="text-shine" data-es="servicios" data-en="services">services</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Uñas, pedicura y cejas" data-en="Nails, pedicure &amp; brows">Uñas, pedicura y cejas</p></div>',
)
rep(
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Port St. Lucie</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">1763 St Lucie West Blvd</p></div>',
)

# ---------- 10. MARQUEE (x2 marquees, cada palabra aparece 4 veces) ----------
MARQUEE_WORDS = [
    ("Classic Set", "Gel Manicure"),
    ("Hybrid Set", "Acrylic Nails"),
    ("Volume Set", "Luxury Pedicure"),
    ("Mega Volume", "Brow Lamination"),
    ("Bottom Lashes", "Henna Brows"),
    ("West Palm Beach, FL", "Port St. Lucie, FL"),
]
for old, new in MARQUEE_WORDS:
    old_tag = f'<span class="marquee-word">{old}</span>'
    new_tag = f'<span class="marquee-word">{new}</span>'
    cnt = h.count(old_tag)
    assert cnt == 4, f"{old!r} aparece {cnt} veces, se esperaban 4"
    h = h.replace(old_tag, new_tag)

# ---------- 11. LA EXPERIENCIA ----------
rep(
    '<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Arlet en el interior de Aylen Luxury Beauty Salon junto al letrero dorado de la marca" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Manicura francesa azul con flores en 3D hecha en Aylen Luxury Beauty Salon" class="blur-up w-full h-full object-cover" loading="lazy" />',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un suite boutique" data-en="A boutique suite">A boutique suite</span><br /><span class="text-shine" data-es="para sentirte única" data-en="to feel one of a kind">to feel one of a kind</span></h2>',
)
rep(
    'data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Aylen Luxury Beauty Salon es el estudio de Arlet Leon dentro de Mia Salon Suite, en St. Lucie West. Cada set de uñas y cada ceja se diseña a mano, servicio por servicio, en un ambiente íntimo pensado para una clienta a la vez." data-en="Aylen Luxury Beauty Salon is Arlet Leon&#39;s studio inside Mia Salon Suite, in St. Lucie West. Every nail set and every brow is designed by hand, one service at a time, in an intimate space built for one client at a time.">Aylen Luxury Beauty Salon es el estudio de Arlet Leon dentro de Mia Salon Suite, en St. Lucie West. Cada set de uñas y cada ceja se diseña a mano, servicio por servicio, en un ambiente íntimo pensado para una clienta a la vez.</p>',
)
rep(
    'data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: un 5.0 perfecto en 49 reseñas verificadas en Booksy, clientas que piden a Arlet por nombre, y un menú que va de manicura en gel a laminado de cejas con henna, todo bajo el mismo techo." data-en="The result: a perfect 5.0 across 49 verified Booksy reviews, clients who ask for Arlet by name, and a menu that ranges from gel manicures to henna brow lamination, all under one roof.">El resultado: un 5.0 perfecto en 49 reseñas verificadas en Booksy, clientas que piden a Arlet por nombre, y un menú que va de manicura en gel a laminado de cejas con henna, todo bajo el mismo techo.</p>',
)
rep(
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="49">49</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(109,27,48,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/logo.jpg" alt="Aylen Luxury Beauty Salon" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(109,27,48,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Arlet · <span class="text-[color:var(--ink-40)]" data-es="Estilista de uñas y cejas" data-en="Nail &amp; brow artist">Nail &amp; brow artist</span></span>',
)

# ---------- 12. EL METODO ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tu cita, uña" data-en="Your visit, nail">Your visit, nail</span> <span class="text-shine" data-es="por uña" data-en="by nail">by nail</span></h2>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration, and confirm instantly.">Eliges tu servicio en Booksy con precio y duración claros, y confirmas al instante.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de diseño" data-en="Design consult">Design consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Forma de mano, largo deseado y el estilo que buscas: de ahí sale el acrílico, polygel o gel que mejor te queda." data-en="Hand shape, desired length and the look you want: that is where the acrylic, polygel or gel that suits you best comes from.">Forma de mano, largo deseado y el estilo que buscas: de ahí sale el acrílico, polygel o gel que mejor te queda.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Manos de Arlet" data-en="Arlet&#39;s hands">Arlet&#39;s hands</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Te relajas mientras Arlet trabaja cada detalle a mano, desde la base hasta el último diseño en 3D." data-en="You relax while Arlet works every detail by hand, from the base to the last 3D design.">Te relajas mientras Arlet trabaja cada detalle a mano, desde la base hasta el último diseño en 3D.</p>',
)
rep(
    '<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    '<h3 class="font-display text-xl mb-3" data-es="Sales lista" data-en="Ready to go">Ready to go</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con tus uñas o cejas terminadas y tu próxima cita agendada si la quieres." data-en="You leave with your nails or brows finished, and your next visit booked if you want it.">Sales con tus uñas o cejas terminadas y tu próxima cita agendada si la quieres.</p>',
)

# ---------- 13. SERVICIOS: intro ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
)
rep(
    'data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones reales publicados por Aylen Luxury Beauty Salon en Booksy. Reserva con confirmación inmediata." data-en="Real prices and durations as listed by Aylen Luxury Beauty Salon on Booksy. Booking confirms instantly.">Precios y duraciones reales publicados por Aylen Luxury Beauty Salon en Booksy. Reserva con confirmación inmediata.</p>',
)

# ---------- 14. SERVICIOS: grid de destacados (regex, bloque completo) ----------
highlight_pat = re.compile(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    flags=re.S,
)
assert highlight_pat.search(h), "no se encontro el grid de destacados"

highlight_new = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Manicura clásica" data-en="Classic manicure">Classic manicure</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura completa en gel con acabado brillante de larga duración, la base perfecta antes de cualquier diseño." data-en="A full gel manicure with a long-lasting glossy finish, the perfect base before any design.">Manicura completa en gel con acabado brillante de larga duración, la base perfecta antes de cualquier diseño.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$45</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(109,27,48,0.4); box-shadow: 0 18px 50px rgba(45,31,26,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del salón" data-en="Salon favorite">Salon favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic Full Set &ndash; XL</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de uñas acrílicas extra largas, esculpidas a mano por Arlet con el largo y la forma que elijas." data-en="A full set of extra-long acrylic nails, hand-sculpted by Arlet to the length and shape you choose.">Set completo de uñas acrílicas extra largas, esculpidas a mano por Arlet con el largo y la forma que elijas.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h 30min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Ritual de pies" data-en="Foot ritual">Foot ritual</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Luxury Spa Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicura de lujo con exfoliación, masaje y esmaltado en gel, para unos pies renovados de principio a fin." data-en="A luxury pedicure with exfoliation, massage and gel polish, for renewed feet from tip to toe.">Pedicura de lujo con exfoliación, masaje y esmaltado en gel, para unos pies renovados de principio a fin.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$90</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas con carácter" data-en="Brows with character">Brows with character</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Brow Lamination + Henna &amp; Wax" data-en="Brow Lamination + Henna &amp; Wax">Brow Lamination + Henna &amp; Wax</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Laminado de cejas con tinte de henna y depilación con cera: cejas llenas, definidas y perfectamente peinadas por semanas." data-en="Brow lamination with henna tint and wax shaping: full, defined brows perfectly styled for weeks.">Laminado de cejas con tinte de henna y depilación con cera: cejas llenas, definidas y perfectamente peinadas por semanas.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = highlight_pat.sub(highlight_new.replace("\\", "\\\\"), h, count=1)

# ---------- 15. SERVICIOS: nota + menú completo por categoría ----------


def menu_block(cat_es, cat_en, delay, rows):
    rows_html = "\n".join(
        f'<div class="flex items-center justify-between gap-3 py-2 border-b border-[color:var(--accent-ghost)] text-sm"><span class="font-light text-[color:var(--ink-60)]">{name}</span><span class="font-medium shrink-0 ml-3">{price}</span></div>'
        for name, price in rows
    )
    return f'''<div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:{delay}ms">
          <h3 class="font-display text-xl mb-4" data-es="{cat_es}" data-en="{cat_en}">{cat_en}</h3>
          <div class="space-y-0.5">
{rows_html}
          </div>
        </div>'''


menu_manicura = menu_block("Manicura y Gel", "Manicure &amp; Gel", 0, [
    ("Gel Manicure", "$45 &middot; 1h"),
    ("Rubber base", "$70"),
    ("Builder Gel Overlay", "$80"),
    ("Aprés Soft Gel Extensions", "$90"),
])
menu_acrilico = menu_block("Acrílico y Polygel", "Acrylic &amp; Polygel", 90, [
    ("Acrylic Full Set &ndash; Medium/Long", "$80"),
    ("Acrylic Fill", "$70"),
    ("Acrylic Full Set &ndash; XL", "$100 &middot; 2h 30min"),
    ("Acrylic Fill &ndash; XL", "$80"),
    ("Acrylic Removal", "$20 &middot; 20min"),
    ("Polygel Full Set", "$80"),
    ("Polygel Fill", "$70"),
])
menu_pedicura = menu_block("Pedicura", "Pedicure", 0, [
    ("Gel Pedicure", "$50 &middot; 1h 15min"),
    ("Luxury Spa Pedicure", "$90"),
])
menu_cejas = menu_block("Cejas", "Brows", 90, [
    ("Brow Waxing", "$20 &middot; 20min"),
    ("Henna Brows + Wax", "$35 &middot; 30min"),
    ("Brow Lamination + Henna &amp; Wax", "$80"),
])

note_and_menu_pat = re.compile(
    r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">.*?</p>)\s*</div>\s*</section>',
    flags=re.S,
)
assert note_and_menu_pat.search(h), "no se encontro la nota de servicios"

note_new = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Uñas en acrílico, polygel y gel, pedicura de lujo, y cejas con henna y laminado, todo en un mismo suite. Menú completo y disponibilidad en Booksy." data-en="Acrylic, polygel and gel nails, luxury pedicures, and henna brow treatments with lamination, all in one suite. Full menu and availability on Booksy.">Uñas en acrílico, polygel y gel, pedicura de lujo, y cejas con henna y laminado, todo en un mismo suite. Menú completo y disponibilidad en Booksy.</span></p>\n      <p class="reveal text-center text-sm text-[color:var(--ink-60)] font-light mt-16 mb-8" data-es="El menú completo, por categoría" data-en="The full menu, by category">El menú completo, por categoría</p>\n      <div class="grid sm:grid-cols-2 gap-5 mt-14">\n        ' + menu_manicura + "\n        " + menu_acrilico + "\n        " + menu_pedicura + "\n        " + menu_cejas + "\n      </div>\n    </div>\n  </section>"

h = note_and_menu_pat.sub(note_new.replace("\\", "\\\\"), h, count=1)

# ---------- 16. GALERIA ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span></h2>',
)

gallery_pat = re.compile(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    flags=re.S,
)
assert gallery_pat.search(h), "no se encontro el grid de galeria"

gallery_new = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Verde jade, acabado en gel" data-en="Jade green, gel finish">Jade green, gel finish</span><img src="assets/raw/bk-6.jpg" alt="Manicura en gel color verde jade degradado hecha en Aylen Luxury Beauty Salon" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Coral con flores 3D" data-en="Coral with 3D flowers">Coral with 3D flowers</span><img src="assets/raw/bk-3.jpg" alt="Uñas acrílicas color coral con flores en 3D y detalles dorados" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Borgoña con flor blanca" data-en="Burgundy with white flower">Burgundy with white flower</span><img src="assets/raw/bk-4.jpg" alt="Manicura borgoña brillante con acento floral blanco" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Nude con lazo dorado" data-en="Nude with gold bow">Nude with gold bow</span><img src="assets/raw/bk-12.jpg" alt="Manicura nude con acento de lazo dorado hecho a mano" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="French nude y dorado" data-en="Nude &amp; gold french">Nude &amp; gold french</span><img src="assets/raw/bk-7.jpg" alt="Manicura estilo french en tonos nude con línea dorada" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Verde lima brillante" data-en="Bright lime green">Bright lime green</span><img src="assets/raw/bk-8.jpg" alt="Manicura en gel verde lima con diseño floral blanco" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = gallery_pat.sub(gallery_new.replace("\\", "\\\\"), h, count=1)

# ---------- 17. OPINIONES ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span></h2>',
)
rep(
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 49 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 49 verified reviews on Booksy">5.0 de 5 · 49 reseñas verificadas en Booksy</span>',
)
rep(
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I love my nails! Thank you for your patience and for doing such a beautiful job. You listened to what I wanted, and I couldn&rsquo;t be happier with the results. I&rsquo;ll definitely be back!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Nicky P.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
)
rep(
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Maravillosa experiencia hacerme mis uñitas contigo. Muy buen carisma, ambiente acogedor y sobre todo excelente trabajo."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Claudia</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
)
rep(
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"La mejor! Siempre salgo encantada con mis uñas. Es muy profesional, detallista y hace un trabajo hermoso. La recomiendo al 100%."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Leyana S.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
)
rep(
    'data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 49 reseñas en Booksy" data-en="Read all 49 reviews on Booksy">Leer las 49 reseñas en Booksy</a>',
)

# ---------- 18. UBICACION ----------
rep(
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Port St. Lucie</span></h2>',
)
rep(
    '<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(109,27,48,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">1763 St Lucie West Blvd, Suite 212 (Mia Salon Suite), Port St. Lucie, FL 34986</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(109,27,48,0.4)]" href="https://www.google.com/maps?q=1763+St+Lucie+West+Blvd+Suite+212,+Port+St.+Lucie,+FL+34986" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
)
rep(
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
)
rep(
    "data-es=\"Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita.\" data-en=\"See Yesi's latest sets and DM any questions before your appointment.\">See Yesi's latest sets and DM any questions before your appointment.</p>",
    'data-es="Mira los últimos diseños de Arlet y escribe por DM cualquier duda antes de tu cita." data-en="See Arlet&#39;s latest designs and DM any questions before your appointment.">Mira los últimos diseños de Arlet y escribe por DM cualquier duda antes de tu cita.</p>',
)
rep(
    'title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'title="Mapa: Aylen Luxury Beauty Salon, 1763 St Lucie West Blvd Suite 212, Port St. Lucie FL"\n          src="https://www.google.com/maps?q=1763+St+Lucie+West+Blvd+Suite+212,+Port+St.+Lucie,+FL+34986&output=embed"',
)

# ---------- 19. CTA FINAL ----------
rep(
    'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Belleza de lujo, uña por uña." data-en="Luxury beauty, nail by nail.">Belleza de lujo, uña por uña.</p>',
)
rep(
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-6xl leading-tight mb-8" style="transition-delay:100ms"><span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span></h2>',
)
rep(
    'data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu manicura, tu pedicura de lujo o el laminado de cejas que ya te toca." data-en="Book online in seconds: your manicure, your luxury pedicure, or the brow lamination you are due for.">Reserva online en segundos: tu manicura, tu pedicura de lujo o el laminado de cejas que ya te toca.</p>',
)

# ---------- 20. FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Aylen Luxury</span>')
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,191,149,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<img src="assets/raw/logo.jpg" alt="Aylen Luxury Beauty Salon" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,191,149,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Aylen Luxury</span>',
)
rep(
    'data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Salón de belleza boutique en Port St. Lucie, FL. Atención con cita previa." data-en="Boutique beauty salon in Port St. Lucie, FL. By appointment only.">Salón de belleza boutique en Port St. Lucie, FL. Atención con cita previa.</p>',
)
rep(
    '<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>',
    '<p>1763 St Lucie West Blvd, Suite 212, Port St. Lucie, FL 34986</p>',
)
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Aylen Luxury Beauty Salon.</p>')

# ---------- 21. Sanity: no deben quedar rastros del esqueleto ----------
for leftover in ["Lash Bloom", "Yesi", "West Palm Beach", "Cresthaven", "519855", "_lashbloom", "pestañ", "lash set", "eyelash"]:
    assert leftover not in h, "LEFTOVER: " + leftover

os.makedirs(f"output/{SLUG}/assets/raw", exist_ok=True)
open(f"output/{SLUG}/index.html", "w", encoding="utf-8").write(h)
print("BUILD OK:", f"output/{SLUG}/index.html", len(h), "bytes")
