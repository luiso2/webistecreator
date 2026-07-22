import re

h = open('output/nailsbyyaima/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- EXPERIENCIA ----------
# bk-2.jpg aqui era una FOTO (no el logo); se reemplaza por el retrato profesional real bk-1.jpg
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Yaima Perdomo, master nail technician, in her Tampa studio" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-13.jpg" alt="Pink gel manicure result from Nails by Yaima" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Una técnica," data-en="One nail tech,">One nail tech,</span><br /><span class="text-shine" data-es="en la que Tampa confía" data-en="Tampa trusts">Tampa trusts</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="Nails by Yaima es el estudio privado de Yaima Perdomo, técnica maestra de uñas en Tampa. Manicura clásica y de spa, gel ruso, overlay y extensiones en builder gel, todo formado y pintado a mano, en inglés o español." data-en="Nails by Yaima is the private studio of Yaima Perdomo, a master nail technician in Tampa. Classic and luxury spa manicures, Russian gel, builder gel overlays and nail extensions, all shaped and finished by hand, in English or Spanish.">Nails by Yaima is the private studio of Yaima Perdomo, a master nail technician in Tampa. Classic and luxury spa manicures, Russian gel, builder gel overlays and nail extensions, all shaped and finished by hand, in English or Spanish.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="El resultado: 5.0 perfecto en 159 reseñas verificadas en Booksy, y clientas que vuelven cita tras cita por el mismo cuidado en cada detalle." data-en="The result: a perfect 5.0 across 159 verified Booksy reviews, and clients who come back appointment after appointment for the same attention to detail.">The result: a perfect 5.0 across 159 verified Booksy reviews, and clients who come back appointment after appointment for the same attention to detail.</p>')
rep('<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>',
    '<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="159">159</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,191,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/raw/bk-2.jpg" alt="Nails by Yaima logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,191,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yaima · <span class="text-[color:var(--ink-40)]" data-es="Técnica maestra de uñas" data-en="Master Nail Technician">Master Nail Technician</span></span>')

# ---------- METODO ----------
rep('data-es="Así se trabaja" data-en="How it works">How it works</span>',
    'data-es="Así se trabaja" data-en="How it works">How it works</span>')
rep('data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: manicura, gel ruso, builder gel o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: manicure, Russian gel, builder gel or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: manicure, Russian gel, builder gel or extensions, and confirm instantly.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de uñas" data-en="Nail consult">Nail consult</h3>')
rep('data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    'data-es="Forma, largo y el acabado que buscas (gel, gel ruso o builder gel) se deciden juntas antes de empezar." data-en="Shape, length and the finish you want (gel, Russian gel or builder gel) get decided together before anything touches your nails.">Shape, length and the finish you want (gel, Russian gel or builder gel) get decided together before anything touches your nails.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="La aplicación" data-en="The application">The application</h3>')
rep('data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    'data-es="De una remoción de esmalte de 15 minutos a un set de extensiones en builder gel de 1h 45min, cada servicio recibe el tiempo que necesita." data-en="From a 15-minute polish removal to a 1h 45min builder gel extension set, every service gets the time it needs.">From a 15-minute polish removal to a 1h 45min builder gel extension set, every service gets the time it needs.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="El acabado" data-en="The finish">The finish</h3>')
rep('data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    'data-es="Sales con un set limpio y duradero, y tu próximo relleno o remoción ya agendados." data-en="You leave with a clean, long-lasting set and your next fill or removal already on the calendar.">You leave with a clean, long-lasting set and your next fill or removal already on the calendar.</p>')

open('output/nailsbyyaima/index.html', 'w').write(h)
print('experiencia + metodo OK')
