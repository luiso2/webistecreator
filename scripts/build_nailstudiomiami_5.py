import re

h = open('output/nailstudiomiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- OPINIONES ----------
rep('<span data-es="Lo que dicen" data-en="What her">Lo que dicen</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">sus clientas</span>',
    '<span data-es="Lo que dicen" data-en="What her">What her</span> <span class="text-shine" data-es="sus clientas" data-en="clients say">clients say</span>')
rep('<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 234 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 234 verified reviews on Booksy">5.0 out of 5 · 234 verified reviews on Booksy</span>',
    '<span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 52 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 52 verified reviews on Booksy">5.0 out of 5 · 52 verified reviews on Booksy</span>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"I absolutely love my hair! What impressed me most was how well it held up in the Orlando heat: my silk press lasted a full TWO WEEKS, which is almost unheard of for me!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Chianita</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Loi\'s work is absolutely amazing! The attention to detail is incredible. The atmosphere is so relaxing. Everything made for an amazing experience. I\'m in love with my nails. They\'re simply gorgeous! Highly recommend!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Katia</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Very pleasant, great job energy, good communication"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Rue</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Best nail tech hands down!"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Alexandria</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Always does a great job."</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Joel</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>',
    '<blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"Love her work"</blockquote>\n          <figcaption class="text-sm"><span class="font-medium">Carmen</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>')
rep('data-es="Leer las 234 reseñas en Booksy" data-en="Read all 234 reviews on Booksy">Read all 234 reviews on Booksy</a>',
    'data-es="Leer las 52 reseñas en Booksy" data-en="Read all 52 reviews on Booksy">Read all 52 reviews on Booksy</a>')

# ---------- UBICACION ----------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Miami</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">8944 SW 152nd Path, Miami, FL 33196</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,114,173,0.4)]" href="https://www.google.com/maps?q=8944+SW+152nd+Path,+Miami,+FL+33196" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://booksy.com/en-us/418314_the-nail-studio-miami_nail-salon_15889_miami" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,114,173,0.4)]" href="https://booksy.com/en-us/418314_the-nail-studio-miami_nail-salon_15889_miami" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>')
rep('data-es="Mira los estilos más recientes y escribe por DM cualquier duda antes de tu cita." data-en="See the latest styles and DM any questions before your appointment.">See the latest styles and DM any questions before your appointment.</p>',
    'data-es="Mira los últimos sets de Loi y escribe por DM cualquier duda antes de tu cita." data-en="See Loi\'s latest sets and DM any questions before your appointment.">See Loi\'s latest sets and DM any questions before your appointment.</p>')
rep('<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="https://www.instagram.com/thenailstudiomiami/" target="_blank" rel="noopener">@thenailstudiomiami</a>',
    '<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(74,114,173,0.4)]" href="https://www.instagram.com/thenailstudiomiami/" target="_blank" rel="noopener">@thenailstudiomiami</a>')
rep('<iframe title="Mapa: Pure Artistry, 80 W Grant St, Orlando FL"\n          src="https://www.google.com/maps?q=80+W+Grant+St,+Orlando,+FL+32806&output=embed"',
    '<iframe title="Mapa: The Nail Studio Miami, 8944 SW 152nd Path, Miami FL"\n          src="https://www.google.com/maps?q=8944+SW+152nd+Path,+Miami,+FL+33196&output=embed"')

# ---------- CTA FINAL ----------
rep('style="background: linear-gradient(180deg, #191307 0%, #100c05 100%);"',
    'style="background: linear-gradient(180deg, #0f1723 0%, #0a0f18 100%);"')
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Tu próximo set" data-en="Your next set">Your next set</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.</p>',
    'data-es="Reserva online en segundos: tu set en gel o acrílico, tu pedicura, o el relleno que ya te toca." data-en="Book online in seconds: your gel or acrylic set, your pedicure, or the fill you are due for.">Book online in seconds: your gel or acrylic set, your pedicure, or the fill you are due for.</p>')

# ---------- FOOTER ----------
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">The Nail Studio</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(140,175,220,0.4)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<img src="assets/raw/bk-2.jpg" alt="The Nail Studio Miami" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(140,175,220,0.4)]" loading="lazy" />\n          <span class="font-display text-lg tracking-[0.1em] uppercase">The Nail Studio Miami</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.</p>',
    'data-es="Salón de uñas en Miami, FL. Atención con cita previa." data-en="Nail salon in Miami, FL. By appointment only.">Nail salon in Miami, FL. By appointment only.</p>')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', '<p>8944 SW 152nd Path, Miami, FL 33196</p>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 The Nail Studio Miami.</p>')

open('output/nailstudiomiami/index.html', 'w').write(h)
print('opiniones + ubicacion + cta + footer OK')
