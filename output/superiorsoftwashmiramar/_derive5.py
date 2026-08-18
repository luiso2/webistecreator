import re

h = open('output/superiorsoftwashmiramar/index.html', encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c >= n, f'NO (found {c}, need {n}): {a[:120]}'
    h = h.replace(a, b, n)


# ---------------------------------------------------------------------------
# STRIP DE CONFIANZA + contador en EXPERIENCIA (dos juegos de data-count)
# ---------------------------------------------------------------------------
rep('<span data-count="86">86</span>', '<span data-count="61">61</span>', n=2)
rep('<span data-es="reseñas en Booksy" data-en="reviews on Booksy">reseñas en Booksy</span>',
    '<span data-es="reseñas en Google" data-en="reviews on Google">reviews on Google</span>')
rep('<p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p>',
    '<p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p>')

rep('<p class="font-display text-2xl">Classic <span class="text-shine">&amp;</span> Volume</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Sets completos · Rellenos" data-en="Full sets · Fills">Full sets · Fills</p>',
    '<p class="font-display text-2xl">Roof <span class="text-shine">&amp;</span> Pressure</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Soft wash · Presión" data-en="Soft wash · Pressure clean">Soft wash · Pressure clean</p>')

rep('<p class="font-display text-2xl">+5 <span class="text-shine" data-es="años" data-en="years">years</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Clientas fieles por años" data-en="Clients who stay for years">Clients who stay for years</p>',
    '<p class="font-display text-2xl">Open <span class="text-shine" data-es="24h" data-en="24/7">24/7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Disponibles cuando nos necesites" data-en="Available when you need us">Available when you need us</p>')

rep('<p class="font-display text-2xl">West Palm Beach</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">4580 Cresthaven Blvd</p>',
    '<p class="font-display text-2xl">Broward County</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Techos · Casas · Pisos" data-en="Roofs · Homes · Hardscape">Roofs · Homes · Hardscape</p>')

# ---------------------------------------------------------------------------
# MARQUEE (x2, cada palabra aparece 4 veces en total)
# ---------------------------------------------------------------------------
MARQUEE_WORDS = [
    ('Classic Set', 'Roof Soft Wash'),
    ('Hybrid Set', 'House Wash'),
    ('Volume Set', 'Driveway Cleaning'),
    ('Mega Volume', 'Pool Deck Cleaning'),
    ('Bottom Lashes', 'Gutter Cleaning'),
    ('West Palm Beach, FL', 'Broward County, FL'),
]
for old, new in MARQUEE_WORDS:
    tag_old = f'<span class="marquee-word">{old}</span>'
    tag_new = f'<span class="marquee-word">{new}</span>'
    assert h.count(tag_old) == 4, f'{old}: se esperaban 4, hay {h.count(tag_old)}'
    h = h.replace(tag_old, tag_new)

# ---------------------------------------------------------------------------
# LA EXPERIENCIA (texto; las imagenes se cambian en el paso de imagenes)
# ---------------------------------------------------------------------------
rep('data-es="La experiencia" data-en="The experience">La experiencia</p>',
    'data-es="La experiencia" data-en="The experience">La experiencia</p>')  # sin cambios, generico

rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Un equipo local" data-en="A local crew">A local crew</span><br /><span class="text-shine" data-es="que deja resultados" data-en="that gets it done">that gets it done</span>')

rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Superior Soft Wash es un equipo de limpieza a presión y soft wash con base en Broward County. Trabajamos techos, fachadas, entradas, patios y terrazas con equipo propio: presión baja y química segura para techos de teja o shingle, y presión alta donde el concreto y los pavers la necesitan." data-en="Superior Soft Wash is a pressure washing and soft wash crew based in Broward County. We work roofs, exteriors, driveways, patios and pool decks with our own equipment: low pressure and roof-safe chemicals for tile and shingle, and higher pressure where concrete and pavers need it.">Superior Soft Wash is a pressure washing and soft wash crew based in Broward County. We work roofs, exteriors, driveways, patios and pool decks with our own equipment: low pressure and roof-safe chemicals for tile and shingle, and higher pressure where concrete and pavers need it.</p>')

rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado se ve en cada techo, entrada y patio que dejamos atrás: 5.0 perfecto en 61 reseñas verificadas en Google, sin quejas de daños por presión. Llama, mándanos fotos por Instagram y te damos un precio real para tu propiedad." data-en="The result shows on every roof, driveway and patio we leave behind: a perfect 5.0 across 61 verified Google reviews, with no pressure-damage complaints. Call us or send photos on Instagram and we will quote your property for real.">The result shows on every roof, driveway and patio we leave behind: a perfect 5.0 across 61 verified Google reviews, with no pressure-damage complaints. Call us or send photos on Instagram and we will quote your property for real.</p>')

rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">24/7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Disponibilidad" data-en="Availability">Availability</p></div>')

rep('<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<span class="text-sm font-light">Superior Soft Wash · <span class="text-[color:var(--ink-40)]" data-es="Equipo de soft wash" data-en="Soft wash crew">Soft wash crew</span></span>')

# ---------------------------------------------------------------------------
# EL METODO
# ---------------------------------------------------------------------------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Cómo trabajamos" data-en="How it works">Cómo trabajamos</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="De tu llamada" data-en="From your call">From your call</span> <span class="text-shine" data-es="a un trabajo terminado" data-en="to a finished job">to a finished job</span>')

rep('data-es="Reserva online" data-en="Book online">Book online</h3>',
    'data-es="Llama o escribe" data-en="Call or text">Call or text</h3>')
rep('data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Nos llamas o escribes por Instagram y nos cuentas qué necesitas: techo, casa, entrada o patio." data-en="You call or DM us on Instagram and tell us what you need: roof, house, driveway or patio.">You call or DM us on Instagram and tell us what you need: roof, house, driveway or patio.</p>')

rep('data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>',
    'data-es="Cotización" data-en="Free quote">Free quote</h3>')
rep('data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    'data-es="Con fotos o una visita rápida vemos la superficie y te damos un precio real antes de empezar." data-en="With photos or a quick visit we look at the surface and give you a real price before we start.">With photos or a quick visit we look at the surface and give you a real price before we start.</p>')

rep('data-es="Aplicación zen" data-en="The zen part">The zen part</h3>',
    'data-es="Limpieza segura" data-en="The safe clean">The safe clean</h3>')
rep('data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    'data-es="Química de baja presión en techos y fachadas, y presión alta donde el concreto o los pavers la piden." data-en="Low-pressure, roof-safe chemicals on roofs and exteriors, and higher pressure where concrete or pavers call for it.">Low-pressure, roof-safe chemicals on roofs and exteriors, and higher pressure where concrete or pavers call for it.</p>')

rep('data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>',
    'data-es="Revisión final" data-en="Final walkthrough">Final walkthrough</h3>')
rep('data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    'data-es="Revisamos el trabajo juntos antes de irnos, techo, entrada o patio, para que quedes conforme." data-en="We walk the job with you before we leave, roof, driveway or patio, so you are happy with the result.">We walk the job with you before we leave, roof, driveway or patio, so you are happy with the result.</p>')

print('OK: strip/marquee/experiencia/metodo')
open('output/superiorsoftwashmiramar/index.html', 'w', encoding='utf-8').write(h)
