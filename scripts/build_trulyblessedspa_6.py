import re

h = open('output/trulyblessedspa/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/1780520_truly-blessed-spa-boutique-llc_wellness-day-spa_15746_brandon'

# ---------- OPINIONES ----------
rep('<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>',
    '<span data-es="Lo que dicen" data-en="What">What</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="4.9 de 5 · 30 reseñas verificadas en Booksy" data-en="4.9 out of 5 · 30 verified reviews on Booksy">4.9 out of 5 · 30 verified reviews on Booksy</span>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I found the experience very customer centric. I will definitely be back."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">James M.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Great experience!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Marizol G.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Janaira is so sweet! I never had a lymphatic massage before. I recently had lipo 360 and after the massage, my swelling went down soooo much. She applied perfect pressure. Her suite is so cute and relaxing. I’ve been recommending everyone to her. Seriously the best!!!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Anna</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 30 reseñas en Booksy" data-en="Read all 30 reviews on Booksy">Read all 30 reviews on Booksy</a>')

# ---------- UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Brandon</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">873 E Bloomingdale Ave, 7A, Brandon, FL 33511</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(139,74,160,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(139,74,160,0.4)]" href="https://www.google.com/maps?q=873+E+Bloomingdale+Ave+7A,+Brandon,+FL+33511" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los últimos trabajos de Shekila y Janaira y escribe por DM cualquier duda antes de tu cita." data-en="See Shekila and Janaira\'s latest work and DM any questions before your appointment.">See Shekila and Janaira\'s latest work and DM any questions before your appointment.</p>')
rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Truly Blessed Spa &amp; Boutique, 873 E Bloomingdale Ave, Brandon FL"\n          src="https://www.google.com/maps?q=873+E+Bloomingdale+Ave+7A,+Brandon,+FL+33511&output=embed"')

# ---------- CTA FINAL ----------
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu próxima cita" data-en="Your next appointment">Your next appointment</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tus uñas, tu pedicura, tu facial o tu sesión de contorno corporal." data-en="Book online in seconds: your nails, your pedicure, your facial or your body contouring session.">Book online in seconds: your nails, your pedicure, your facial or your body contouring session.</p>')

# ---------- FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Truly Blessed</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(226,190,240,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<img src="assets/raw/bk-2.jpg" alt="Truly Blessed Spa &amp; Boutique" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(226,190,240,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Truly Blessed</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Day spa y estudio de uñas en Brandon, FL. Atención con cita previa." data-en="Day spa and nail studio in Brandon, FL. By appointment only.">Day spa and nail studio in Brandon, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>873 E Bloomingdale Ave, 7A, Brandon, FL 33511</p>')
rep(f'<p><a href="{BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#e2bef0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    f'<p><a href="{BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#e2bef0]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Truly Blessed Spa &amp; Boutique LLC.</p>')

open('output/trulyblessedspa/index.html', 'w').write(h)
print('opiniones + ubicacion + cta + footer OK')
