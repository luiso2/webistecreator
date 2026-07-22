import re

h = open('output/dessisosastudio/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:220]
    h = h.replace(a, b, n)

# ================= LA EXPERIENCIA =================
# Imagenes: de 2 fotos apiladas a 1 sola foto grande (pool real limitado, bk-6 interior/proceso)
rep('''<div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>''',
    '''<div class="frame zoomable aspect-[4/5] img-reveal">
        <img src="assets/raw/bk-6.jpg" alt="Interior del estudio DessiSosa Studio en Tampa, servicio de pedicure en proceso" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>''')

rep('data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    'data-es="Tres técnicas," data-en="Three technicians,">Three technicians,</span><br /><span class="text-shine" data-es="un solo estándar" data-en="one single standard">one single standard</span>')

rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>',
    'data-es="DessiSosa Studio es un estudio de uñas y pestañas en el norte de Tampa, fundado por Dessi Sosa junto a Meybis Suarez y Nehiva Gomez. Manicura en gel y acrílico, pedicure y extensión de pestañas, en un espacio pequeño donde cada clienta recibe el tiempo completo de su cita." data-en="DessiSosa Studio is a nail and lash studio in North Tampa, founded by Dessi Sosa alongside Meybis Suarez and Nehiva Gomez. Gel and acrylic manicures, pedicures and lash extensions, in a small space where every client gets the full time of her appointment.">DessiSosa Studio es un estudio de uñas y pestañas en el norte de Tampa, fundado por Dessi Sosa junto a Meybis Suarez y Nehiva Gomez. Manicura en gel y acrílico, pedicure y extensión de pestañas, en un espacio pequeño donde cada clienta recibe el tiempo completo de su cita.</p>')

rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>',
    'data-es="Sus clientas lo confirman en cada reseña: trato excelente y trabajo prolijo, cita tras cita. 5.0 perfecto en 46 reseñas verificadas de Booksy." data-en="Her clients confirm it in every review: excellent treatment and careful work, visit after visit. A perfect 5.0 across 46 verified Booksy reviews.">Sus clientas lo confirman en cada reseña: trato excelente y trabajo prolijo, cita tras cita. 5.0 perfecto en 46 reseñas verificadas de Booksy.</p>')

rep('<span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p>',
    '<span data-count="46">46</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reseñas</p>')

rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,98,212,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<img src="assets/raw/bk-4.jpg" alt="Dessi Sosa, fundadora de DessiSosa Studio" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(75,98,212,0.3)]" loading="lazy" />\n            <span class="text-sm font-light">Dessi Sosa · <span class="text-[color:var(--ink-40)]" data-es="Fundadora" data-en="Founder">Fundadora</span></span>')

# ================= EL METODO =================
rep('data-es="Reserva online" data-en="Book online">Book online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>',
    'data-es="Reserva online" data-en="Book online">Reserva online</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: uñas, pedicure o pestañas, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: nails, pedicure or lashes, and confirm instantly.">Eliges tu servicio en Booksy con precio y duración claros: uñas, pedicure o pestañas, y confirmas al instante.</p>')

rep('data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>',
    'data-es="Diseño y color" data-en="Design and color">Diseño y color</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges forma, largo y color de uñas, o el estilo de pestañas que buscas: clásico, híbrido o volumen." data-en="You choose nail shape, length and color, or the lash style you want: classic, hybrid or volume.">Eliges forma, largo y color de uñas, o el estilo de pestañas que buscas: clásico, híbrido o volumen.</p>')

rep('data-es="Manos a la obra" data-en="The work">The work</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>',
    'data-es="El servicio" data-en="The service">El servicio</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="De los 15 minutos de una depilación de cejas a la 1h 45min de un set de pestañas completo: cada cita recibe su tiempo dedicado." data-en="From the 15 minutes of an eyebrow wax to the 1h 45min of a full lash set: every appointment gets its dedicated time.">De los 15 minutos de una depilación de cejas a la 1h 45min de un set de pestañas completo: cada cita recibe su tiempo dedicado.</p>')

rep('data-es="El toque final" data-en="The finish">The finish</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>',
    'data-es="El toque final" data-en="The finish">El toque final</h3>\n          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Top coat, indicaciones de cuidado y la fecha de tu retoque, ya sea de uñas o de pestañas, agendada antes de salir." data-en="Top coat, care guidance and your fill date, whether for nails or lashes, booked before you leave.">Top coat, indicaciones de cuidado y la fecha de tu retoque, ya sea de uñas o de pestañas, agendada antes de salir.</p>')

open('output/dessisosastudio/index.html', 'w').write(h)
print('experiencia + metodo OK')
