import re

h = open('output/vivianatales/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- OPINIONES ----------
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 35 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 35 verified reviews on Booksy">5.0 de 5 · 35 reseñas verificadas en Booksy</span>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"The absolute best!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Camila</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Stefany</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Me encantaron"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Liz</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 35 reseñas en Booksy" data-en="Read all 35 reviews on Booksy">Leer las 35 reseñas en Booksy</a>')

# ---------- UBICACION ----------
rep('<span data-es="Visítanos" data-en="Visit us">Visítanos</p>' if False else 'data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    'data-es="Visítanos" data-en="Visit us">Visítanos</p>')
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Doral</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">10640 NW 27th St, Doral, FL 33172</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=10640+NW+27th+St,+Doral,+FL+33172"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los últimos looks de Viviana y escribe por DM cualquier duda antes de tu cita." data-en="See Viviana\'s latest looks and DM any questions before your appointment.">Mira los últimos looks de Viviana y escribe por DM cualquier duda antes de tu cita.</p>')
rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    '<iframe title="Mapa: Viviana Tales Lash Studio, 10640 NW 27th St, Doral FL"\n          src="https://www.google.com/maps?q=10640+NW+27th+St,+Doral,+FL+33172&output=embed"')

# ---------- CTA FINAL ----------
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu mirada nueva" data-en="Your new lashes">Tu mirada nueva</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">te está esperando</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu set clásico, de volumen suave o wispy, o el relleno que ya te toca." data-en="Book online in seconds: your classic, soft volume or wispy set, or the fill you are due for.">Reserva online en segundos: tu set clásico, de volumen suave o wispy, o el relleno que ya te toca.</p>')
rep('data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="https://www.instagram.com/vivianataleslashstudio/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
    'data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>\n        <a href="https://www.instagram.com/vivianataleslashstudio/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>')

# ---------- FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">Viviana Tales</span>')
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(227,176,168,0.37)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<img src="assets/raw/bk-2.jpg" alt="Viviana Tales Lash Studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(227,176,168,0.37)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Viviana Tales Lash Studio</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de pestañas en Doral, FL. Atención con cita previa." data-en="Lash studio in Doral, FL. By appointment only.">Estudio de pestañas en Doral, FL. Atención con cita previa.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>10640 NW 27th St, Doral, FL 33172</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Viviana Tales Lash Studio.</p>')

open('output/vivianatales/index.html', 'w').write(h)
print('opiniones + ubicacion + cta + footer OK')
