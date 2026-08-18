import re

h = open('output/superiorsoftwashmiramar/index.html', encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c >= n, f'NO (found {c}, need {n}): {a[:120]}'
    h = h.replace(a, b, n)


# ---------------------------------------------------------------------------
# PRELOADER
# ---------------------------------------------------------------------------
rep('<span class="pre-mono">LB</span>', '<span class="pre-mono">SS</span>')
rep('<span class="pre-word">Lash Bloom</span>', '<span class="pre-word">Superior Soft Wash</span>')

# ---------------------------------------------------------------------------
# NAV: marca, "Opiniones" -> "Por Que Nosotros", CTA a llamar
# ---------------------------------------------------------------------------
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
    '<span class="font-display text-xl tracking-[0.1em] uppercase">Superior <span class="text-[color:var(--accent-deep)]">Soft Wash</span></span>')

rep('href="#opiniones" data-es="Opiniones" data-en="Reviews">Opiniones</a>',
    'href="#porque" data-es="Por Qué Nosotros" data-en="Why Us">Por Qué Nosotros</a>', n=2)
rep('<section id="opiniones" class="relative py-24 sm:py-32 grain">',
    '<section id="porque" class="relative py-24 sm:py-32 grain">')

rep('data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    'data-es="Llamar ahora" data-en="Call now">Llamar ahora</span>')
rep('data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'data-es="Llamar ahora" data-en="Call now">Llamar ahora</a>')

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
rep('data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio</p>',
    'data-es="Broward County, FL · Roof &amp; Pressure Cleaning" data-en="Broward County, FL · Roof &amp; Pressure Cleaning">Broward County, FL · Roof &amp; Pressure Cleaning</p>')

rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
    'data-es="Su casa, su techo, su propiedad: limpios de verdad." data-en="Your home, your roof, your property, actually clean.">Your home, your roof, your property, actually clean.</p>', n=2)

rep('<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
    '<span data-es="Roof soft washing y" data-en="Roof soft washing and">Roof soft washing and</span><br /><span data-es="limpieza a presión que " data-en="pressure cleaning that ">pressure cleaning that </span><span class="text-shine" data-es="se nota" data-en="shows">shows</span>')

rep('data-es="Sets completos clásicos, híbridos, volumen y mega volumen, con rellenos de 2 y 3 semanas para mantener la mirada perfecta. Una artista licenciada, un suite zen y clientas que llevan más de 5 años con ella." data-en="Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.">Full classic, hybrid, volume and mega volume sets, with 2 and 3 week fills to keep the look perfect. One licensed artist, a zen suite, and clients who have stayed with her for over 5 years.</p>',
    'data-es="Roof soft washing, lavado de casas y limpieza a presión de entradas, patios y terrazas en Broward County. Sistema de baja presión seguro para techos de tejas y shingles, y equipo propio para cada trabajo." data-en="Roof soft washing, house washing, and pressure cleaning for driveways, patios and pool decks across Broward County. Low-pressure system that is safe on tile and shingle roofs, with our own equipment on every job.">Roof soft washing, house washing, and pressure cleaning for driveways, patios and pool decks across Broward County. Low-pressure system that is safe on tile and shingle roofs, with our own equipment on every job.</p>')

rep('data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy</span>',
    'data-es="5.0 · 61 reseñas en Google" data-en="5.0 · 61 reviews on Google">5.0 · 61 reviews on Google</span>')

rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Llamar ahora" data-en="Call now">Call now</span>', n=1)
rep('data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    'data-es="Llamar ahora" data-en="Call now">Call now</a>', n=2)

rep('<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Volume Full Set</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
    '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Cotización gratis" data-en="Free quote">Free quote</p>\n            <p class="font-display text-lg" data-es="Techo, casa o piso" data-en="Roof, house or hardscape">Roof, house or hardscape</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="Llama y te decimos el precio" data-en="Call and we quote it">Call and we quote it</p>')

print('OK: preloader/nav/hero')
open('output/superiorsoftwashmiramar/index.html', 'w', encoding='utf-8').write(h)
