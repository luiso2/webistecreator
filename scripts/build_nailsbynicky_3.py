import re

h = open('output/nailsbynicky/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- HERO ----------
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>',
    'data-es="Hialeah, FL · Nail Salon" data-en="Hialeah, FL · Nail Salon">Hialeah, FL · Nail Salon</p>')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Uñas con actitud y precisión." data-en="Nails with attitude and precision.">Nails with attitude and precision.</p>')
rep('''<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>''',
    '''<span data-es="Russian manicure, Apres" data-en="Russian manicure, Apres">Russian manicure, Apres</span><br /><span data-es="Gel X y nail art, hechos para " data-en="Gel X and nail art, made to ">Gel X and nail art, made to </span><span class="text-shine" data-es="brillar" data-en="turn heads">turn heads</span>''')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>',
    'data-es="Russian manicure con sistemas luminary, full sets de Apres Gel X, dip powder y nail art hecho a mano, todo con una sola técnica en Hialeah. 4.9 en 71 reseñas de Booksy." data-en="Russian manicure with luminary systems, Apres Gel X full sets, dip powder and hand-painted nail art, all from one nail tech in Hialeah. A 4.9 rating across 71 Booksy reviews.">Russian manicure with luminary systems, Apres Gel X full sets, dip powder and hand-painted nail art, all from one nail tech in Hialeah. A 4.9 rating across 71 Booksy reviews.</p>')
rep('data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>',
    'data-es="4.9 · 71 reseñas en Booksy" data-en="4.9 · 71 reviews on Booksy">4.9 · 71 reviews on Booksy</span>')
rep('<span class="stars text-lg" aria-hidden="true">★★★★★</span>',
    '<span class="stars text-lg" aria-hidden="true">★★★★★</span>')
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-1.jpg" alt="Glossy red gel manicure with a fine dot accent at Nails By Nicky, Hialeah" class="blur-up w-full h-full object-cover" />')
rep('<p class="font-display text-lg">Silk Press</p>', '<p class="font-display text-lg">Apres Gel X Full Set</p>')
rep('data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
    'data-es="$65 · 1h 30min" data-en="$65 · 1h 30min">$65 · 1h 30min</p>')

# ---------- STRIP ----------
rep('<span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>',
    '<span data-count="71">71</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span>')
rep('<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>',
    '<div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Apres <span class="text-shine">&amp;</span> Russian</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Full sets · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p></div>')
rep('<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>',
    '<div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">1:1</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Una técnica, atención de cerca" data-en="One tech, close attention">One tech, close attention</p></div>')
rep('<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>',
    '<div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Hialeah, FL</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">5775 W 20th Ave</p></div>')

# ---------- MARQUEE (x2, 4 ocurrencias por palabra) ----------
marquee_words = [
    ('Silk Press', 'Apres Gel X'),
    ('Loc Retwist', 'Russian Manicure'),
    ('Knotless Braids', 'Dip Powder'),
    ('K-Tip Extensions', 'Nail Art'),
    ('Keratin', 'Luminary Gel'),
    ('Orlando, FL', 'Hialeah, FL'),
]
for old, new in marquee_words:
    old_span = f'<span class="marquee-word">{old}</span>'
    new_span = f'<span class="marquee-word">{new}</span>'
    assert h.count(old_span) == 4, f'{old_span}: {h.count(old_span)}'
    h = h.replace(old_span, new_span)

open('output/nailsbynicky/index.html', 'w').write(h)
print('hero+strip+marquee OK')
