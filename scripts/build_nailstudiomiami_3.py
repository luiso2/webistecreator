import re

h = open('output/nailstudiomiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- EXPERIENCIA ----------
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Nude gel manicure resting on a car steering wheel" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Black and white marble nail art at The Nail Studio Miami" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Una técnica," data-en="One nail tech,">One nail tech,</span><br /><span class="text-shine" data-es="manos firmes" data-en="steady hands">steady hands</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="The Nail Studio Miami es el suite de una sola técnica, Loi, en West Kendall. Cada set se moldea y termina a mano, desde un cambio de esmalte hasta un set completo en gel o acrílico, en un ambiente que sus clientas describen como relajante." data-en="The Nail Studio Miami is the suite of one nail tech, Loi, in West Kendall. Every set is shaped and finished by hand, from a quick polish change to a full gel or acrylic set, in an atmosphere her clients call relaxing.">The Nail Studio Miami is the suite of one nail tech, Loi, in West Kendall. Every set is shaped and finished by hand, from a quick polish change to a full gel or acrylic set, in an atmosphere her clients call relaxing.</p>')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="El resultado: 5.0 perfecto en 52 reseñas verificadas, y clientas que le confían sus manicuras desde hace casi dos décadas." data-en="The result: a perfect 5.0 across 52 verified reviews, and clients who have trusted her with their manicures for close to two decades.">The result: a perfect 5.0 across 52 verified reviews, and clients who have trusted her with their manicures for close to two decades.</p>')
rep('<span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<span data-count="52">52</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/raw/bk-2.jpg" alt="The Nail Studio Miami logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(120,160,210,0.35)]" loading="lazy" />\n            <span class="text-sm font-light">Loi · <span class="text-[color:var(--ink-40)]" data-es="Técnica de uñas" data-en="Nail Artist">Nail Artist</span></span>')

# ---------- METODO ----------
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>')
rep('data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy con precio y duración claros: manicura, pedicura, set completo o cera, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: manicure, pedicure, full set or wax, and confirm instantly.">Pick your service on Booksy with clear price and duration: manicure, pedicure, full set or wax, and confirm instantly.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta de uñas" data-en="Nail consult">Nail consult</h3>')
rep('data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    'data-es="Forma, largo y color o arte en uñas se deciden juntas antes de empezar." data-en="Shape, length and color or nail art get decided together before anything touches your nails.">Shape, length and color or nail art get decided together before anything touches your nails.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="La aplicación" data-en="The application">The application</h3>')
rep('data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    'data-es="De un cambio de esmalte de 30 minutos a un set en gel o acrílico de 2 horas, cada servicio recibe el tiempo que necesita, sin apuros." data-en="From a 30-minute polish change to a 2-hour gel or acrylic set, every service gets the time it needs, no rush.">From a 30-minute polish change to a 2-hour gel or acrylic set, every service gets the time it needs, no rush.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="El acabado" data-en="The finish">The finish</h3>')
rep('data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    'data-es="Sales con un acabado limpio y duradero, y tu próximo relleno o pedicura ya agendados." data-en="You leave with a clean, long-lasting finish and your next fill or pedicure already on the calendar.">You leave with a clean, long-lasting finish and your next fill or pedicure already on the calendar.</p>')

open('output/nailstudiomiami/index.html', 'w').write(h)
print('experiencia + metodo OK')
