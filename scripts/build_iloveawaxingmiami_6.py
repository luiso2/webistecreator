import re

h = open('output/iloveawaxingmiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/1037088_i-love-waxing-miami_hair-removal_15889_miami'
MAPQ = 'https://www.google.com/maps?q=2915+Biscayne+Blvd,+Suite+200-75,+Miami,+FL+33137'

# ---------- OPINIONES (reseñas reales verbatim de data.json, named_reviews) ----------
rep('<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 111 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 111 verified reviews on Booksy">5.0 out of 5 · 111 verified reviews on Booksy</span>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"10/10 customer service is awesome and I love my lash set!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Emily</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente todo!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Daniela R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yesi is very pleasant and professional! She does a beautiful job and I always enjoy her company!!! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Suzanne</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"She’s been servicing me over 10 years. I absolutely love her work, I even travel to come to every appointment!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Cee R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always professional and a perfectionist. I’ve been with Lash Bloom for over 5 years now and absolutely love her!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Tara</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Amazing!!!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Olivia D.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    'data-es="Leer las 111 reseñas en Booksy" data-en="Read all 111 reviews on Booksy">Read all 111 reviews on Booksy</a>')

# ---------- UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">2915 Biscayne Blvd, Suite 200-75, Miami, FL 33137</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,92,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    f'<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,92,0.4)]" href="{MAPQ}" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>')

# Nueva tarjeta de horario, insertada entre Direccion y Reservas
rep('''            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>''',
    '''            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:170ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15.5 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario" data-en="Hours">Hours</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Dom 9am-2pm · Lun 9am-12pm · Mar/Mié/Vie 9am-3pm · Jue 11am-5pm · Sáb cerrado" data-en="Sun 9am-2pm · Mon 9am-12pm · Tue/Wed/Fri 9am-3pm · Thu 11am-5pm · Sat closed">Sun 9am-2pm · Mon 9am-12pm · Tue/Wed/Fri 9am-3pm · Thu 11am-5pm · Sat closed</p>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Reservas" data-en="Bookings">Reservas</p>''')

rep(f'<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,92,0.4)]" href="{BOOKSY}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    f'<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(160,74,92,0.4)]" href="{BOOKSY}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira el estudio y escribe por DM cualquier duda antes de tu cita." data-en="See the studio and DM any questions before your appointment.">See the studio and DM any questions before your appointment.</p>')
rep('<iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"\n          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    f'<iframe title="Mapa: I Love Waxing Miami, 2915 Biscayne Blvd, Miami FL"\n          src="{MAPQ}&output=embed"')

# ---------- CTA FINAL ----------
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu piel suave" data-en="Your smooth skin">Your smooth skin</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva online en segundos: tu bikini brasileño, tus cejas, o el paquete completo que ya te toca." data-en="Book online in seconds: your Brazilian bikini, your brows, or the full package you are due for.">Book online in seconds: your Brazilian bikini, your brows, or the full package you are due for.</p>')

# ---------- FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">I Love Waxing</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,202,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<img src="assets/raw/bk-2.jpg" alt="I Love Waxing Miami" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,202,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">I Love Waxing</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de depilación con cera en Miami, FL. Atención con cita previa." data-en="Waxing studio in Miami, FL. By appointment only.">Waxing studio in Miami, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>2915 Biscayne Blvd, Suite 200-75, Miami, FL 33137</p>')
rep(f'<p><a href="{BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#f0beca]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    f'<p><a href="{BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#f0beca]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>')
rep('<p><a href="https://www.instagram.com/ilovewaxingmiami/" target="_blank" rel="noopener" class="hover:text-[#f0beca]">Instagram · @ilovewaxingmiami</a></p>',
    '<p><a href="https://www.instagram.com/ilovewaxingmiami/" target="_blank" rel="noopener" class="hover:text-[#f0beca]">Instagram · @ilovewaxingmiami</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 I Love Waxing Miami.</p>')

open('output/iloveawaxingmiami/index.html', 'w').write(h)
print('opiniones + ubicacion + cta + footer OK')
