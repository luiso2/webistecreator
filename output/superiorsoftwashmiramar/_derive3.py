import re, json

h = open('output/superiorsoftwashmiramar/index.html', encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c >= n, f'NO (found {c}, need {n}): {a[:100]}'
    h = h.replace(a, b, n)


# ---------------------------------------------------------------------------
# 4. Head: title, meta description, og:*, JSON-LD
# ---------------------------------------------------------------------------
rep(
    '<title>Lash Bloom · Lash Studio in West Palm Beach, FL | 5.0 on Booksy</title>',
    '<title>Superior Soft Wash · Roof &amp; Pressure Cleaning in Broward County, FL | 5.0 on Google</title>'
)
rep(
    '<meta name="description" content="Lash Bloom LLC, West Palm Beach FL: classic, hybrid, volume and mega volume lash extensions with a perfect 5.0 across 86 Booksy reviews. Book online." />',
    '<meta name="description" content="Superior Soft Wash Roof Cleaning and Pressure Cleaning, Broward County FL: roof soft washing, house washing, driveway and pool deck cleaning with a perfect 5.0 rating across 61 Google reviews. Call for a free quote." />'
)
rep(
    '<meta property="og:title" content="Lash Bloom · Lash Studio in West Palm Beach, FL" />',
    '<meta property="og:title" content="Superior Soft Wash · Roof &amp; Pressure Cleaning in Broward County, FL" />'
)
rep(
    '<meta property="og:description" content="Classic, hybrid and volume lashes. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Roof soft washing, house washing, driveway and pool deck cleaning. 5.0 on Google. Call for a free quote." />'
)
rep('<meta property="og:image" content="assets/raw/bk-6.jpg" />',
    '<meta property="og:image" content="assets/raw/hero-1.jpg" />')

ld_pattern = re.compile(r'<script type="application/ld\+json">.*?</script>', flags=re.S)
old_ld = ld_pattern.search(h)
assert old_ld, 'no se encontro el bloque JSON-LD'

ld_obj = {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Superior Soft Wash Roof Cleaning and Pressure Cleaning",
    "description": "Roof soft washing, house washing, and driveway, paver and pool deck pressure cleaning serving Broward County, FL.",
    "telephone": "+1-954-882-2870",
    "areaServed": {"@type": "AdministrativeArea", "name": "Broward County, FL"},
    "sameAs": ["https://www.instagram.com/superior_services_sofla/"],
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "61", "bestRating": "5"}
}
new_ld = '<script type="application/ld+json">\n  ' + json.dumps(ld_obj, indent=2) + '\n  </script>'
h = ld_pattern.sub(new_ld, h, count=1)

print('OK: paso 4 head/json-ld')
open('output/superiorsoftwashmiramar/index.html', 'w', encoding='utf-8').write(h)
