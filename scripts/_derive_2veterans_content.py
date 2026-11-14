import re

SLUG = 'output/2-veterans-handyman-service/index.html'
h = open(SLUG, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    cnt = h.count(a)
    assert cnt == n, f'NO (found {cnt}, need {n}): {a[:110]!r}'
    h = h.replace(a, b, n)

PHONE_DISPLAY = '(754) 266-7735'
PHONE_TEL = '+17542667735'
FB_URL = 'https://www.facebook.com/2veteranshandymanservice/'
GREV_URL = 'https://www.google.com/search?q=2+Veterans+Handyman+Service+Cape+Coral+FL+reviews'
MAPS_URL = 'https://www.google.com/maps?q=1806+Southwest+22nd+Terrace,+Cape+Coral,+FL+33991'
MAPS_EMBED = 'https://www.google.com/maps?q=1806+Southwest+22nd+Terrace,+Cape+Coral,+FL+33991&output=embed'

# ---------- HEAD ----------
rep(
'<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
'<title>2 Veterans Handyman Service · Handyman in Cape Coral, FL | Drywall &amp; Remodeling | 4.7 on Google</title>'
)
rep(
'<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
'<meta name="description" content="2 Veterans Handyman Service, Cape Coral FL: drywall repair, kitchen and bathroom remodeling, installs and home repairs. Veteran-owned, licensed and insured. 4.7 stars across 55 Google reviews." />'
)
rep(
'<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
'<meta property="og:title" content="2 Veterans Handyman Service · Handyman in Cape Coral, FL" />'
)
rep(
'<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
'<meta property="og:description" content="Drywall, remodeling, installs and home repairs. Veteran-owned. 4.7 stars across 55 Google reviews." />'
)
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/hero-chandelier-install.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/hero-chandelier-install.jpg" />')

old_jsonld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Pure Artistry",
    "description": "Hair studio in Orlando, FL: silk press, loc retwists and interlocks, knotless braids, K-Tip and microlink extensions, keratin treatments.",
    "address": { "@type": "PostalAddress", "streetAddress": "80 W Grant St, Suite 111, Studio 156", "addressLocality": "Orlando", "addressRegion": "FL", "postalCode": "32806", "addressCountry": "US" },
    "sameAs": ["https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando", "https://www.instagram.com/pure.artistrysk/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "234", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Hair services", "itemListElement": [
      { "@type": "Offer", "price": "90", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Silk Press" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Full-head Loc Retwist" } },
      { "@type": "Offer", "price": "400", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Small Knotless Braids" } },
      { "@type": "Offer", "price": "750", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "K-Tip Extensions" } }
    ] }
  }
  </script>'''
new_jsonld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "2 Veterans Handyman Service",
    "description": "Veteran-owned handyman company in Cape Coral, FL: drywall repair and installation, kitchen and bathroom remodeling, TV mounts, ceiling fans, light fixtures and general home repairs.",
    "address": { "@type": "PostalAddress", "streetAddress": "1806 Southwest 22nd Terrace", "addressLocality": "Cape Coral", "addressRegion": "FL", "postalCode": "33991", "addressCountry": "US" },
    "telephone": "+1-754-266-7735",
    "sameAs": ["https://www.facebook.com/2veteranshandymanservice/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "55", "bestRating": "5" },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "00:00", "closes": "23:59" }
    ],
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Handyman services", "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Drywall Repair & Installation" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Kitchen & Bathroom Remodeling" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Installations & Fixtures" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Home Repairs & Maintenance" } }
    ] }
  }
  </script>'''
rep(old_jsonld, new_jsonld)

open(SLUG, 'w', encoding='utf-8').write(h)
print('HEAD OK, length', len(h))
