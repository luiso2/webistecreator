import re

h = open('output/trulyblessedspa/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Shekila Vann, owner of Truly Blessed Spa &amp; Boutique, in her Brandon suite" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-16.jpg" alt="Cavitation and lymphatic massage treatment at Truly Blessed Spa &amp; Boutique" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="One boutique suite," data-en="One boutique suite,">One boutique suite,</span><br /><span class="text-shine" data-es="every service under one roof" data-en="every service under one roof">every service under one roof</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Truly Blessed Spa &amp; Boutique es el suite de Shekila Vann en Brandon, con Janaira a cargo del contorno corporal y el masaje linfático. Del Gel-X y el Ombré a la cera, el facial y la cavitación, cada cita se trata con el mismo cuidado personal." data-en="Truly Blessed Spa &amp; Boutique is Shekila Vann’s suite in Brandon, with Janaira leading body contouring and lymphatic massage. From Gel-X and Ombré to waxing, facials and cavitation, every appointment gets the same one-on-one care.">Truly Blessed Spa &amp; Boutique is Shekila Vann\'s suite in Brandon, with Janaira leading body contouring and lymphatic massage. From Gel-X and Ombré to waxing, facials and cavitation, every appointment gets the same one-on-one care.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 4.9 en 30 reseñas verificadas de Booksy, con clientas que hablan de un servicio centrado en ellas y de un alívio real después de su primer masaje linfático." data-en="The result: a 4.9 rating across 30 verified Booksy reviews, with clients describing customer-centric service and real relief after their first lymphatic massage.">The result: a 4.9 rating across 30 verified Booksy reviews, with clients describing customer-centric service and real relief after their first lymphatic massage.</p>')
rep('<span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<span data-count="30">30</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>')
rep('<img src="assets/raw/bk-2.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(139,74,160,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/bk-2.jpg" alt="Truly Blessed Spa &amp; Boutique logo" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(139,74,160,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Shekila &amp; Janaira · <span class="text-[color:var(--ink-40)]" data-es="Owners" data-en="Owners">Owners</span></span>')

# ---------- METODO ----------
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, paso" data-en="Your visit, step">Your visit, step</span> <span class="text-shine" data-es="a paso" data-en="by step">by step</span>')
rep('data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu servicio en Booksy, de manicura a contorno corporal, con precio y duración claros, y confirmas al instante." data-en="Pick your service on Booksy, from a manicure to body contouring, with clear price and duration, and confirm instantly.">Pick your service on Booksy, from a manicure to body contouring, with clear price and duration, and confirm instantly.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="Consulta" data-en="Consult">Consult</h3>')
rep('data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    'data-es="Antes de empezar, Shekila o Janaira revisan lo que buscas: forma, largo y acabado en uñas, o la zona a tratar en el contorno corporal." data-en="Before anything starts, Shekila or Janaira review what you want: shape, length and finish for nails, or the area to treat for body contouring.">Before anything starts, Shekila or Janaira review what you want: shape, length and finish for nails, or the area to treat for body contouring.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Aplicación zen" data-en="The zen part">The zen part</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="El tratamiento" data-en="The treatment">The treatment</h3>')
rep('data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    'data-es="Te recuestas y te dejas cuidar: desde un full set de Gel-X hasta una sesión de cavitación con masaje linfático, con calma y sin prisa." data-en="You settle in and let them take care of it: from a Gel-X full set to a cavitation session with lymphatic massage, unhurried and relaxed.">You settle in and let them take care of it: from a Gel-X full set to a cavitation session with lymphatic massage, unhurried and relaxed.</p>')
rep('<h3 class="font-display text-xl mb-3" data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>',
    '<h3 class="font-display text-xl mb-3" data-es="El resultado" data-en="The result">The result</h3>')
rep('data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    'data-es="Sales con un acabado impecable y, si lo necesitas, tu próxima cita o relleno ya agendados." data-en="You leave with a flawless finish and, if you need it, your next appointment or fill already booked.">You leave with a flawless finish and, if you need it, your next appointment or fill already booked.</p>')

open('output/trulyblessedspa/index.html', 'w').write(h)
print('experiencia + metodo OK')
