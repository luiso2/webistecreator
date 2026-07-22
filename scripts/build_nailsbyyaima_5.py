import re

h = open('output/nailsbyyaima/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/1019645_nails-by-yaima_nail-salon_15761_tampa'

# ---------- OPINIONES ----------
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 159 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 159 verified reviews on Booksy">5.0 out of 5 · 159 verified reviews on Booksy</span>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Yaima is amazing! She took real care if my cuticles… like TRANSFORMED my hands. She is very professional and her client education is top notch. I truly enjoyed this service. I cannot wait to show my nails off in Croatia"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Fara J.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"She is amazing on all levels!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Christina B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Love them so much"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Amy</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    'data-es="Leer las 159 reseñas en Booksy" data-en="Read all 159 reviews on Booksy">Read all 159 reviews on Booksy</a>')

# ---------- UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Tampa</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">7340 Ponderosa Dr, Tampa, FL 33637</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,191,75,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,191,75,0.4)]" href="https://www.google.com/maps?q=7340+Ponderosa+Dr,+Tampa,+FL+33637" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>')
rep(f'<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,191,75,0.4)]" href="{BOOKSY}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    f'<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,191,75,0.4)]" href="{BOOKSY}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="Mira los últimos sets de Yaima y escribe por DM cualquier duda antes de tu cita." data-en="See Yaima\'s latest sets and DM any questions before your appointment.">See Yaima\'s latest sets and DM any questions before your appointment.</p>')
rep('<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Mapa: Nails by Yaima, 7340 Ponderosa Dr, Tampa FL"\n          src="https://www.google.com/maps?q=7340+Ponderosa+Dr,+Tampa,+FL+33637&output=embed"')

# Insertar fila de telefono (dato real, encontrado y corroborado por busqueda web) tras la fila de direccion
old_address_block = '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Dirección</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">7340 Ponderosa Dr, Tampa, FL 33637</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,191,75,0.4)]" href="https://www.google.com/maps?q=7340+Ponderosa+Dr,+Tampa,+FL+33637" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>
          </div>'''
assert old_address_block in h
new_address_block = old_address_block + '''
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:170ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Teléfono" data-en="Phone">Teléfono</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">(813) 493-7405</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,191,75,0.4)]" href="tel:+18134937405" data-es="Llamar" data-en="Call now">Call now</a>
            </div>
          </div>'''
h = h.replace(old_address_block, new_address_block, 1)

# ---------- CTA FINAL ----------
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Tu próximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva online en segundos: tu manicura de gel ruso, tu set de builder gel, o el relleno que ya te toca." data-en="Book online in seconds: your Russian gel manicure, your builder gel set, or the fill you are due for.">Book online in seconds: your Russian gel manicure, your builder gel set, or the fill you are due for.</p>')

# ---------- FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Nails by Yaima</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,221,150,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<img src="assets/raw/bk-2.jpg" alt="Nails by Yaima" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,221,150,0.35)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Nails by Yaima</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Tampa, FL. Atención únicamente con cita previa." data-en="Nail salon in Tampa, FL. By appointment only.">Nail salon in Tampa, FL. By appointment only.</p>')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', '<p>7340 Ponderosa Dr, Tampa, FL 33637</p>')
rep(f'<p><a href="{BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#e9cdab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    f'<p><a href="{BOOKSY}" target="_blank" rel="noopener" class="hover:text-[#e9cdab]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>\n        <p><a href="tel:+18134937405" class="hover:text-[#e9cdab]">(813) 493-7405</a></p>')
rep('<p><a href="https://www.instagram.com/nailsbyyaima/" target="_blank" rel="noopener" class="hover:text-[#e9cdab]">Instagram · @nailsbyyaima</a></p>',
    '<p><a href="https://www.instagram.com/nailsbyyaima/" target="_blank" rel="noopener" class="hover:text-[#e9cdab]">Instagram · @nailsbyyaima</a></p>\n        <p><a href="https://www.facebook.com/nailsbyyaima/" target="_blank" rel="noopener" class="hover:text-[#e9cdab]">Facebook · Nails by Yaima</a></p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Nails by Yaima.</p>')

open('output/nailsbyyaima/index.html', 'w').write(h)
print('opiniones + ubicacion + cta + footer OK')
