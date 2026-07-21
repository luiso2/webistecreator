import re

h = open('output/vivianatales/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- EXPERIENCIA ----------
rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-1.jpg" alt="Interior del suite de Viviana Tales Lash Studio en Doral" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-8.jpg" alt="Viviana Tales, artista de pestañas, retrato" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
    '<span data-es="Una sola artista," data-en="One artist,">Una sola artista,</span><br /><span class="text-shine" data-es="manos de confianza" data-en="trusted hands">manos de confianza</span>')
rep('data-es="Lash Bloom es el estudio de una sola artista licenciada y certificada: Yesi. Cada set se diseña sobre tu ojo, pestaña por pestaña, en un suite que sus clientas describen como zen y relajante, con luz neon rosa y calma de verdad." data-en="Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.">Lash Bloom is the studio of one licensed, certified artist: Yesi. Every set is designed around your eye, lash by lash, in a suite her clients describe as zen and relaxing, pink neon glow included.</p>',
    'data-es="Viviana Tales Lash Studio es el suite de una sola artista, Viviana, en Doral. Cada set se diseña sobre tu ojo, pestaña por pestaña, desde el clásico hasta el mega volumen, además de laminado de cejas y henna." data-en="Viviana Tales Lash Studio is the suite of one artist, Viviana, in Doral. Every set is designed around your eye, lash by lash, from classic to mega volume, plus brow lamination and henna.">Viviana Tales Lash Studio es el suite de una sola artista, Viviana, en Doral. Cada set se diseña sobre tu ojo, pestaña por pestaña, desde el clásico hasta el mega volumen, además de laminado de cejas y henna.</p>')
rep('data-es="El resultado: 5.0 perfecto en 86 reseñas verificadas, un programa de lealtad para clientas frecuentes, y mujeres que llevan más de cinco años sin dejarse pestañas con nadie más." data-en="The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.">The result: a perfect 5.0 across 86 verified reviews, a loyalty program for regulars, and women who have not trusted their lashes to anyone else in over five years.</p>',
    'data-es="El resultado: 5.0 perfecto en 35 reseñas verificadas de Booksy, y clientas que confían en ella para sus cejas y pestañas cita tras cita." data-en="The result: a perfect 5.0 across 35 verified Booksy reviews, and clients who trust her with their brows and lashes appointment after appointment.">El resultado: 5.0 perfecto en 35 reseñas verificadas de Booksy, y clientas que confían en ella para sus cejas y pestañas cita tras cita.</p>')
rep('<span data-count="86">86</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<span data-count="35">35</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(140,63,82,0.32)]" loading="lazy" />\n            <span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
    '<img src="assets/raw/bk-2.jpg" alt="Viviana Tales Lash Studio" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(140,63,82,0.32)]" loading="lazy" />\n            <span class="text-sm font-light">Viviana Tales · <span class="text-[color:var(--ink-40)]" data-es="Artista de pestañas" data-en="Lash artist">Artista de pestañas</span></span>')

# ---------- METODO ----------
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>',
    'data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso</p>')
rep('<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
    '<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Tu cita, pestaña</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">por pestaña</span>')
rep('data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Pick your set or fill on Booksy with clear price and duration, and confirm instantly.</p>',
    'data-es="Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante." data-en="Pick your set or fill on Booksy with clear price and duration, and confirm instantly.">Eliges tu set o tu relleno en Booksy con precio y duración claros, y confirmas al instante.</p>')
rep('data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, híbrido o volumen." data-en="Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.">Eye shape, natural lash and the effect you want: that is where the classic, hybrid or volume design comes from.</p>',
    'data-es="Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, volumen suave o wispy." data-en="Eye shape, natural lash and the effect you want: that is where the classic, soft volume or wispy design comes from.">Forma del ojo, pestaña natural y el efecto que buscas: de ahí sale el diseño clásico, volumen suave o wispy.</p>')
rep('data-es="Te recuestas, cierras los ojos y Yesi hace lo suyo: hasta 1h 50min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.">You lie back, close your eyes and Yesi does her thing: up to 1h 50min of unhurried, lash-by-lash application.</p>',
    'data-es="Te recuestas, cierras los ojos y Viviana hace lo suyo: hasta 1h 40min de aplicación tranquila, pestaña por pestaña." data-en="You lie back, close your eyes and Viviana does her thing: up to 1h 40min of unhurried, lash-by-lash application.">Te recuestas, cierras los ojos y Viviana hace lo suyo: hasta 1h 40min de aplicación tranquila, pestaña por pestaña.</p>')
rep('data-es="Sales con tu relleno de 2 o 3 semanas agendado y acumulando puntos del programa de lealtad." data-en="You leave with your 2 or 3 week fill booked and loyalty points adding up.">You leave with your 2 or 3 week fill booked and loyalty points adding up.</p>',
    'data-es="Sales con tu mirada nueva y tu próximo relleno ya agendado." data-en="You leave with your new look and your next fill already booked.">Sales con tu mirada nueva y tu próximo relleno ya agendado.</p>')

open('output/vivianatales/index.html', 'w').write(h)
print('experiencia + metodo OK')
