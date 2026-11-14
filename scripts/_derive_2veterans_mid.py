import re
SLUG = 'output/2-veterans-handyman-service/index.html'
h = open(SLUG, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    cnt = h.count(a)
    assert cnt == n, f'NO (found {cnt}, need {n}): {a[:140]!r}'
    h = h.replace(a, b, n)

PHONE_TEL = '+17542667735'

# ---------- STRIP DE CONFIANZA ----------
old_strip = '''      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="234">234</span> <span data-es="reseñas en Booksy" data-en="reviews on Booksy">reviews on Booksy</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Locs <span class="text-shine">&amp;</span> Braids</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Retwist · Interlock · Knotless" data-en="Retwist · Interlock · Knotless">Retwist · Interlock · Knotless</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">K-Tip <span class="text-shine">&amp;</span> Links</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Extensiones premium" data-en="Premium extensions">Premium extensions</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Orlando</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1">80 W Grant St</p></div>'''
new_strip = '''      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1"><span data-count="55">55</span> <span data-es="resenas en Google" data-en="reviews on Google">reviews on Google</span></p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl">Drywall <span class="text-shine">&amp;</span> Remodel</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Cocinas · Banos · Reparaciones" data-en="Kitchens · Baths · Repairs">Kitchens · Baths · Repairs</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl" data-es="Veterano" data-en="Veteran-Owned">Veteran-Owned</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Licenciado y asegurado" data-en="Licensed &amp; insured">Licensed &amp; insured</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Cape Coral</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="22nd Terrace, FL" data-en="22nd Terrace, FL">22nd Terrace, FL</p></div>'''
rep(old_strip, new_strip)

# ---------- MARQUEE (both copies, 2 blocks) ----------
old_marquee_block = '''        <span class="marquee-word">Silk Press</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Loc Retwist</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Knotless Braids</span><span class="marquee-star">✦</span>
        <span class="marquee-word">K-Tip Extensions</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Keratin</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Orlando, FL</span><span class="marquee-star">✦</span>'''
new_marquee_block = '''        <span class="marquee-word">Drywall Repair</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Kitchen Remodel</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Bathroom Remodel</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Installations</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Home Repairs</span><span class="marquee-star">✦</span>
        <span class="marquee-word">Cape Coral, FL</span><span class="marquee-star">✦</span>'''
cnt = h.count(old_marquee_block)
assert cnt == 4, f'expected 4 marquee blocks, found {cnt}'
h = h.replace(old_marquee_block, new_marquee_block)

# ---------- EXPERIENCIA ----------
old_exp_imgs = '''      <div class="grid grid-cols-2 gap-5">
        <div class="frame zoomable aspect-[3/4] img-reveal">
          <img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
        <div class="frame zoomable aspect-[3/4] mt-10 img-reveal" style="transition-delay:140ms">
          <img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>'''
new_exp_imgs = '''      <div class="grid grid-cols-1 gap-5">
        <div class="frame zoomable aspect-[4/3] img-reveal">
          <img src="assets/about-drywall-patch.jpg" alt="Drywall patch and repair in progress by 2 Veterans Handyman Service in a Cape Coral home" class="blur-up w-full h-full object-cover" loading="lazy" />
        </div>
      </div>'''
rep(old_exp_imgs, new_exp_imgs)

rep(
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>',
'<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="La experiencia" data-en="The experience">La experiencia</p>'
)
rep(
'''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span></h2>''',
'''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-7" style="transition-delay:80ms"><span data-es="Un equipo," data-en="One crew,">One crew,</span><br /><span class="text-shine" data-es="dos veteranos" data-en="two veterans">two veterans</span></h2>'''
)
rep(
'''<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.</p>''',
'''<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es="2 Veterans Handyman Service es el negocio veterano de Todd Williams y su equipo en Cape Coral. Drywall, remodelacion de cocinas y banos, instalaciones y reparaciones generales, con tecnicos licenciados y asegurados." data-en="2 Veterans Handyman Service is Todd Williams and his crew's veteran-owned business in Cape Coral. Drywall, kitchen and bathroom remodeling, installs and general repairs, with licensed and insured technicians.">2 Veterans Handyman Service is Todd Williams and his crew's veteran-owned business in Cape Coral. Drywall, kitchen and bathroom remodeling, installs and general repairs, with licensed and insured technicians.</p>'''
)
rep(
'''<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.</p>''',
'''<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es="Sus clientes lo confirman: pidieron una cita un viernes y el trabajo se hizo el lunes siguiente. 4.7 estrellas en 55 resenas verificadas de Google." data-en="Their customers confirm it: one asked for an appointment on a Friday and had the job done the following Monday. A 4.7 rating across 55 verified Google reviews.">Their customers confirm it: one asked for an appointment on a Friday and had the job done the following Monday. A 4.7 rating across 55 verified Google reviews.</p>'''
)
rep(
'''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="5.0" data-decimals="1">5.0</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Booksy</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="234">234</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención personal" data-en="Personal care">Personal care</p></div>''',
'''<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="4.7" data-decimals="1">4.7</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1">Google</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="55">55</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Reseñas" data-en="Reviews">Reviews</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">24/7</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Emergencias" data-en="Emergency calls">Emergency calls</p></div>'''
)
rep(
'''<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(63,152,103,0.3)]" loading="lazy" />
            <span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>''',
'''<img src="assets/hero-chandelier-install.jpg" alt="2 Veterans Handyman Service" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(63,152,103,0.3)]" loading="lazy" />
            <span class="text-sm font-light">2 Veterans Handyman · <span class="text-[color:var(--ink-40)]" data-es="Veterano, equipo de 2" data-en="Veteran-owned crew">Veteran-owned crew</span></span>'''
)

# ---------- EL METODO ----------
rep(
'''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span></h2>''',
'''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Asi se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aqui" data-en="here">here</span></h2>'''
)
rep(
'''        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Reserva online" data-en="Book online">Book online</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Manos a la obra" data-en="The work">The work</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="El toque final" data-en="The finish">The finish</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.</p>
        </div>''',
f'''        <div class="glass glass-hover rounded-3xl p-7 reveal">
          <p class="step-num text-5xl mb-5">01</p>
          <h3 class="font-display text-xl mb-3" data-es="Llama y cuenta" data-en="Call it in">Call it in</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Llama o escribe con el trabajo que necesitas, desde un socket suelto hasta una remodelacion de bano." data-en="Call or text with the job you need, from a loose outlet to a full bathroom remodel.">Call or text with the job you need, from a loose outlet to a full bathroom remodel.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="step-num text-5xl mb-5">02</p>
          <h3 class="font-display text-xl mb-3" data-es="Cotizacion gratis" data-en="Free estimate">Free estimate</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El equipo revisa el trabajo y da una cotizacion gratis y honesta antes de empezar cualquier reparacion." data-en="The crew looks at the job and gives a free, honest estimate before any repair starts.">The crew looks at the job and gives a free, honest estimate before any repair starts.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="step-num text-5xl mb-5">03</p>
          <h3 class="font-display text-xl mb-3" data-es="Agenda rapida" data-en="Fast scheduling">Fast scheduling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Clientes piden el viernes y consiguen el trabajo el lunes: el equipo se mueve rapido por Cape Coral." data-en="Customers ask on a Friday and get the job done Monday: the crew moves fast across Cape Coral.">Customers ask on a Friday and get the job done Monday: the crew moves fast across Cape Coral.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 reveal" style="transition-delay:330ms">
          <p class="step-num text-5xl mb-5">04</p>
          <h3 class="font-display text-xl mb-3" data-es="Entrega limpia" data-en="Clean handoff">Clean handoff</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="El trabajo se termina, se limpia el area y se deja la propiedad mejor de como se encontro." data-en="The job gets finished, the area gets cleaned up, and the property is left better than it was found.">The job gets finished, the area gets cleaned up, and the property is left better than it was found.</p>
        </div>'''
)

open(SLUG, 'w', encoding='utf-8').write(h)
print('STRIP+MARQUEE+EXP+METODO OK, length', len(h))
