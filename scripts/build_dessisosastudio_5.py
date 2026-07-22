import re

h = open('output/dessisosastudio/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:220]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/57332_dessisosa-studio_nail-salon_15761_tampa'

# ================= GALERIA: encabezado =================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Trabajo</span> <span class="text-shine" data-es="real" data-en="work">real</span></h2>')

# ================= GALERIA: grid completo (curaduria real: solo resultados limpios, sin selfies ni texto encima) =================
gal_pattern = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', flags=re.S)
m = gal_pattern.search(h)
assert m, 'grid galeria no encontrado'

new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Nuestro espacio" data-en="Our space">Nuestro espacio</span><img src="assets/raw/bk-1.jpg" alt="Interior del estudio DessiSosa Studio en Tampa, con flores frescas en el mostrador" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Manicura terminada" data-en="Finished manicure">Manicura terminada</span><img src="assets/raw/bk-11.jpg" alt="Manicura terminada con diseño en blanco y rosa en DessiSosa Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:m.start()] + new_gallery + h[m.end():]

# ================= OPINIONES =================
rep('data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>',
    'data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span></h2>')
rep('<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span data-es="5.0 de 5 · 46 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 46 verified reviews on Booksy">5.0 de 5 · 46 reseñas verificadas en Booksy</span>')

rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Dessi Sosa Studio it\'s the best nail studio in the area ❤️"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Adriana R.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')

rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Execente como siempre las uñas me quedaron perfectas 100 puntos"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Racsy M.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')

rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Excelente servicio"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Lubismar B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')

rep('data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    'data-es="Leer las 46 reseñas en Booksy" data-en="Read all 46 reviews on Booksy">Leer las 46 reseñas en Booksy</a>')

# ================= UBICACION =================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight mb-9" style="transition-delay:80ms"><span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Tampa</span></h2>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,98,212,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">7208 North Armenia Avenue, Suite B, Tampa, FL 33604</p>\n              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(75,98,212,0.4)]" href="https://www.google.com/maps?q=7208+North+Armenia+Avenue,+Suite+B,+Tampa,+FL+33604" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>')
rep('<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Mapa: DessiSosa Studio, 7208 North Armenia Avenue, Tampa FL"\n          src="https://www.google.com/maps?q=7208+North+Armenia+Avenue,+Suite+B,+Tampa,+FL+33604&output=embed"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata.</p>',
    'data-es="Lunes a viernes de 8am a 7pm y sábados de 10am a 7pm, con cita previa vía Booksy." data-en="Monday to Friday 8am to 7pm and Saturdays 10am to 7pm, by appointment via Booksy.">Lunes a viernes de 8am a 7pm y sábados de 10am a 7pm, con cita previa vía Booksy.</p>')
rep('data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="Mira los trabajos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest work and DM any questions before your appointment.">Mira los trabajos más recientes y escribe por DM cualquier duda antes de tu cita.</p>')

# ================= CTA FINAL =================
rep('data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    'data-es="Tu cita" data-en="Your appointment">Tu cita</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva online en segundos: tu manicura, tu pedicure o ese set de pestañas que llevas planeando." data-en="Book online in seconds: your manicure, your pedicure, or that lash set you have been planning.">Reserva online en segundos: tu manicura, tu pedicure o ese set de pestañas que llevas planeando.</p>')

# ================= FOOTER =================
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
    '<span class="foot-mark" aria-hidden="true">DessiSosa Studio</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(150,163,232,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<img src="assets/raw/bk-2.jpg" alt="DessiSosa Studio" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(150,163,232,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">DessiSosa Studio</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Nail salon y lash studio en el norte de Tampa, FL. Atención con cita previa." data-en="Nail salon and lash studio in North Tampa, FL. By appointment only.">Nail salon y lash studio en el norte de Tampa, FL. Atención con cita previa.</p>')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p>7208 North Armenia Avenue, Suite B, Tampa, FL 33604</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 DessiSosa Studio.</p>')

open('output/dessisosastudio/index.html', 'w').write(h)
print('galeria+opiniones+ubicacion+cta+footer OK')
