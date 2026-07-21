import re

h = open('output/nailsbymarelys/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Glossy white gel manicure at Nails by Marelys, Hialeah" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-5.jpg" alt="Iridescent French shimmer manicure at Nails by Marelys, Hialeah" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Una técnica," data-en="One nail tech,">One nail tech,</span><br /><span class="text-shine" data-es="manos de confianza" data-en="hands you trust">hands you trust</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Nails by Marelys es el suite de Marelys Pacheco en Hialeah. Cada set se forma y pinta a mano, desde una manicura regular hasta un full set en acrílico o dip powder, con el mismo cuidado en cada cita." data-en="Nails by Marelys is Marelys Pacheco\'s suite in Hialeah. Every set is shaped and painted by hand, from a regular manicure to a full acrylic or dip powder set, with the same care every visit.">Nails by Marelys is Marelys Pacheco\'s suite in Hialeah. Every set is shaped and painted by hand, from a regular manicure to a full acrylic or dip powder set, with the same care every visit.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 89 reseñas verificadas en Booksy, y clientas que vuelven cita tras cita por la misma atención al detalle." data-en="The result: a perfect 5.0 across 89 verified Booksy reviews, and clients who come back visit after visit for the same attention to detail.">The result: a perfect 5.0 across 89 verified Booksy reviews, and clients who come back visit after visit for the same attention to detail.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="89">89</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<img src="assets/raw/bk-2.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,100,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/bk-2.jpg" alt="Nails by Marelys logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,100,74,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Marelys · <span class="text-[color:var(--ink-40)]" data-es="Técnica de uñas" data-en="Nail Artist">Nail Artist</span></span>')

# ---------- METODO ----------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, paso" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="a paso" data-en="by step">by step</span>')
rep('data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: manicura, pedicura, dip o acrílico, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: manicure, pedicure, dip or acrylic, and confirm instantly.">Pick your service on Booksy with clear price and duration: manicure, pedicure, dip or acrylic, and confirm instantly.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de uñas" data-en="Nail consult">Nail consult</h3>')
rep('data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    'data-es="Forma, largo y el acabado que buscas (gel, dip o acrílico) se deciden juntas antes de empezar." data-en="Shape, length and the finish you want (gel, dip or acrylic) get decided together before anything touches your nails.">Shape, length and the finish you want (gel, dip or acrylic) get decided together before anything touches your nails.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="La aplicación" data-en="The application">The application</h3>')
rep('data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    'data-es="De una manicura regular de 40 minutos a un full set de gel o acrílico de casi 2 horas, cada servicio recibe el tiempo que necesita." data-en="From a 40-minute regular manicure to a nearly 2-hour gel or acrylic full set, every service gets the time it needs.">From a 40-minute regular manicure to a nearly 2-hour gel or acrylic full set, every service gets the time it needs.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="El acabado" data-en="The finish">The finish</h3>')
rep('data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    'data-es="Sales con un acabado limpio y duradero, y tu próximo relleno o pedicura ya agendados." data-en="You leave with a clean, long-lasting finish and your next fill or pedicure already on the calendar.">You leave with a clean, long-lasting finish and your next fill or pedicure already on the calendar.</p>')

open('output/nailsbymarelys/index.html', 'w').write(h)
print('experiencia + metodo OK')
