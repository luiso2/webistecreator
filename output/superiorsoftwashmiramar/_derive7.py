import re

h = open('output/superiorsoftwashmiramar/index.html', encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c >= n, f'NO (found {c}, need {n}): {a[:120]}'
    h = h.replace(a, b, n)


# ---------------------------------------------------------------------------
# "POR QUE NOSOTROS" (variante SIN-testimonios: sin quotes, sin stars, sin
# data-count aca; el rating real ya vive en hero/strip/experiencia)
# ---------------------------------------------------------------------------
porque_re = re.compile(r'<section id="porque" class="relative py-24 sm:py-32 grain">.*?</section>', flags=re.S)
assert porque_re.search(h), 'no se encontro la seccion porque'

new_porque = '''<section id="porque" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Por qué nosotros" data-en="Why us">Why us</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Por qué" data-en="Why">Why</span> <span class="text-shine" data-es="elegirnos" data-en="choose us">choose us</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms" data-es="5.0 en Google · 61 reseñas verificadas" data-en="5.0 on Google · 61 verified reviews">5.0 on Google · 61 verified reviews</p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-8 reveal">
          <h3 class="font-display text-xl mb-4" data-es="Método seguro para el techo" data-en="Roof-safe method">Roof-safe method</h3>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Soft wash de baja presión con química pensada para teja y shingle: quita algas y manchas sin agrietar ni desgastar el techo, algo que la presión alta sí puede hacer." data-en="Low-pressure soft wash with chemicals matched to tile and shingle: algae and stains come off without cracking or wearing down the roof the way high pressure can.">Low-pressure soft wash with chemicals matched to tile and shingle: algae and stains come off without cracking or wearing down the roof the way high pressure can.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <h3 class="font-display text-xl mb-4" data-es="Resultados reales" data-en="Real before &amp; after results">Real before &amp; after results</h3>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Lo que ves en nuestra galería es trabajo propio, no fotos de stock: cada techo, entrada y patio es un antes y después real." data-en="What you see in our gallery is our own work, not stock photos: every roof, driveway and patio is a real before and after.">What you see in our gallery is our own work, not stock photos: every roof, driveway and patio is a real before and after.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <h3 class="font-display text-xl mb-4" data-es="Locales y disponibles" data-en="Local &amp; available">Local &amp; available</h3>
          <p class="text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Equipo con base en Broward County, abierto 24/7 para cotizaciones. Llamas o escribes por Instagram y respondemos rápido." data-en="Crew based in Broward County, open 24/7 for quotes. Call or message us on Instagram and we answer fast.">Crew based in Broward County, open 24/7 for quotes. Call or message us on Instagram and we answer fast.</p>
        </div>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="tel:+19548822870" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Llamar para tu cotización" data-en="Call for a free quote">Call for a free quote</a>
      </div>
    </div>
  </section>'''
h = porque_re.sub(new_porque, h, count=1)

# ---------------------------------------------------------------------------
# UBICACION: sin direccion publica -> sin mapa, foto real + zona de servicio
# ---------------------------------------------------------------------------
rep('data-es="Visítanos" data-en="Visit us">Visítanos</p>',
    'data-es="Zona de servicio" data-en="Service area">Service area</p>')
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Trabajamos en" data-en="Serving">Serving</span> <span class="text-shine">Broward County, FL</span>')

rep('''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Dirección" data-en="Address">Address</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(31,107,115,0.4)]" href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415" target="_blank" rel="noopener" data-es="Cómo llegar" data-en="Get directions">Cómo llegar</a>
            </div>
          </div>''',
    '''<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Área" data-en="Area">Area</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Servimos Broward County, FL: techos, casas, entradas y patios en toda la zona." data-en="We serve Broward County, FL: roofs, homes, driveways and patios across the area.">We serve Broward County, FL: roofs, homes, driveways and patios across the area.</p>
            </div>
          </div>''')

rep('data-es="Reservas" data-en="Bookings">Reservas</p>',
    'data-es="Cotizaciones" data-en="Quotes">Quotes</p>')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Llama o manda un mensaje con fotos de tu techo, casa o patio: te damos un precio real, sin listas fijas." data-en="Call or send a message with photos of your roof, house or patio: we give you a real price, no fixed price lists.">Call or send a message with photos of your roof, house or patio: we give you a real price, no fixed price lists.</p>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira trabajos recientes y manda fotos de tu propiedad por DM para una cotización rápida." data-en="See recent jobs and DM us photos of your property for a fast quote.">See recent jobs and DM us photos of your property for a fast quote.</p>')

rep('''<div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">
        <iframe title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"
          src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"
          class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>''',
    '''<div class="frame img-reveal reveal min-h-[380px]" style="transition-delay:180ms">
        <img src="assets/raw/about-1.jpg" alt="Superior Soft Wash truck ready for the next job in Broward County" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>''')

# ---------------------------------------------------------------------------
# CTA FINAL: titular y parrafo
# ---------------------------------------------------------------------------
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu propiedad" data-en="Your property">Your property</span> <span class="text-shine" data-es="lista para brillar" data-en="ready to shine">ready to shine</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Llama ahora y te damos una cotización real para tu techo, casa, entrada o patio. Respondemos rápido." data-en="Call now for a real quote on your roof, house, driveway or patio. We answer fast.">Call now for a real quote on your roof, house, driveway or patio. We answer fast.</p>')

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
    '<span class="foot-mark" aria-hidden="true">Superior Soft Wash</span>')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Superior Soft Wash</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Roof soft washing y limpieza a presión en Broward County, FL." data-en="Roof soft washing and pressure cleaning across Broward County, FL.">Roof soft washing and pressure cleaning across Broward County, FL.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>Broward County, FL</p>')
rep('data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a>',
    'data-es="Llamar · (954) 882-2870" data-en="Call · (954) 882-2870">Call · (954) 882-2870</a>')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Superior Soft Wash Roof Cleaning and Pressure Cleaning.</p>')

print('OK: porque/ubicacion/cta-final/footer')
open('output/superiorsoftwashmiramar/index.html', 'w', encoding='utf-8').write(h)
