import re

h = open('output/superiorsoftwashmiramar/index.html', encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c >= n, f'NO (found {c}, need {n}): {a[:100]}'
    h = h.replace(a, b, n)


PHONE_DISPLAY = '(954) 882-2870'
PHONE_TEL = 'tel:+19548822870'
IG_URL = 'https://www.instagram.com/superior_services_sofla/'
IG_HANDLE = '@superior_services_sofla'

# ---------------------------------------------------------------------------
# 3. Globales: quitar Booksy/IG viejos, avatares (no hay logo real: monograma)
# ---------------------------------------------------------------------------
BOOKSY_A = 'href="https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach" target="_blank" rel="noopener"'
rep(BOOKSY_A, f'href="{PHONE_TEL}"', n=h.count(BOOKSY_A))

rep_ig_count = h.count('https://www.instagram.com/_lashbloom/')
for _ in range(rep_ig_count):
    rep('https://www.instagram.com/_lashbloom/', IG_URL)

rep('@_lashbloom', IG_HANDLE, n=h.count('@_lashbloom'))

# Avatares: no hay logo descargable real (solo fotos de Google Maps) -> monograma "SS"
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,107,115,0.35)]" />',
    '<span class="w-10 h-10 rounded-full ring-1 ring-[rgba(31,107,115,0.35)] bg-[color:var(--accent-deep)] text-white flex items-center justify-center font-display text-sm tracking-wide">SS</span>'
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(31,107,115,0.3)]" loading="lazy" />',
    '<span class="w-10 h-10 rounded-full ring-1 ring-[rgba(31,107,115,0.3)] bg-[color:var(--accent-deep)] text-white flex items-center justify-center font-display text-sm tracking-wide">SS</span>'
)
rep(
    '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(143,227,234,0.35)]" loading="lazy" />',
    '<span class="w-9 h-9 rounded-full ring-1 ring-[rgba(143,227,234,0.35)] bg-[color:var(--accent-mid)] text-[#0b1e20] flex items-center justify-center font-display text-xs tracking-wide">SS</span>'
)

# Favicon: sin logo real, usamos la foto de la camioneta rotulada (marca real visible)
rep('<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/about-1.jpg" />')

print('OK: paso 3 globales')
open('output/superiorsoftwashmiramar/index.html', 'w', encoding='utf-8').write(h)
