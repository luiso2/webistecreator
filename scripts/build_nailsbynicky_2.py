import re

h = open('output/nailsbynicky/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/421799_nails-by-nicky_nail-salon_15886_hialeah'
OLD_BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'
assert h.count(OLD_BOOKSY) >= 1
h = h.replace(OLD_BOOKSY, BOOKSY)

OLD_IG_URL = 'https://www.instagram.com/pure.artistrysk/'
NEW_IG_URL = 'https://www.instagram.com/nailsbynicky111/'
h = h.replace(OLD_IG_URL, NEW_IG_URL)
h = h.replace('@pure.artistrysk', '@nailsbynicky111')

# ---------- HEAD ----------
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Nails By Nicky · Nail Salon in Hialeah, FL | 4.9 on Booksy</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Nails By Nicky, Hialeah FL: Russian manicure, Apres Gel X full sets, dip powder and nail art, with a 4.9 rating across 71 Booksy reviews. Book online." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Nails By Nicky · Nail Salon in Hialeah, FL" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Russian manicure, Apres Gel X and nail art. 4.9 on Booksy. Book online." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-1.jpg" />')

old_ldjson = re.search(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S).group(0)
new_ldjson = '''<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NailSalon",
    "name": "Nails By Nicky",
    "description": "Nail salon in Hialeah, FL: Russian manicure, Apres Gel X full sets, dip powder, acrylic and nail art.",
    "address": { "@type": "PostalAddress", "streetAddress": "5775 W 20th Ave", "addressLocality": "Hialeah", "addressRegion": "FL", "postalCode": "33012", "addressCountry": "US" },
    "sameAs": ["''' + BOOKSY + '''", "https://www.instagram.com/nailsbynicky111/"],
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "71", "bestRating": "5" },
    "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Nail services", "itemListElement": [
      { "@type": "Offer", "price": "75", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Russian Manicure & Luminary Systems" } },
      { "@type": "Offer", "price": "65", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres Gel X Full Set" } },
      { "@type": "Offer", "price": "100", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Apres Gel X Full Set &amp; Pedicure" } },
      { "@type": "Offer", "price": "10", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "French Nails" } }
    ] }
  }
  </script>'''
assert old_ldjson in h
h = h.replace(old_ldjson, new_ldjson, 1)

# ---------- PRELOADER ----------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">NN</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Nails By Nicky</span>')

# ---------- NAV ----------
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Nails By <span class="text-[color:var(--accent-deep)]">Nicky</span></span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,75,98,0.35)]" />',
    '<img src="assets/raw/bk-2.jpg" alt="Nails By Nicky" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,75,98,0.35)]" />')

open('output/nailsbynicky/index.html', 'w').write(h)
print('head+preloader+nav OK')
