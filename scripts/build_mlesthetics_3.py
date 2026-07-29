import re

SLUG = "ml-esthetics-pompano-beach"
PATH = f"output/{SLUG}/index.html"
h = open(PATH, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:160]
    h = h.replace(a, b, n)


BOOK = "https://booksy.com/en-us/1680270_ml-esthetics_brows-lashes_15649_pompano-beach"
IG = "https://www.instagram.com/ml_esthetics1/"

# ---------------------------------------------------------------------------
# 13. GALERIA (6 tiles curados visualmente: antes/despues + resultados terminados)
# ---------------------------------------------------------------------------
rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="results">results</span>')

gallery_grid = re.search(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    h, flags=re.S)
assert gallery_grid
NEW_GALLERY = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Antes y Después · Cejas y Labios" data-en="Before &amp; After · Brows &amp; Lips">Before &amp; After · Brows &amp; Lips</span><img src="assets/raw/bk-1.jpg" alt="Before and after brow and lip blush permanent makeup result at ML Esthetics" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Retrato PMU" data-en="PMU Portrait">PMU Portrait</span><img src="assets/raw/bk-12.jpg" alt="Client portrait with finished permanent makeup brows at ML Esthetics" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Laminado de Cejas" data-en="Brow Lamination">Brow Lamination</span><img src="assets/raw/bk-13.jpg" alt="Finished brow lamination result at ML Esthetics" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Lash Lift &amp; Cejas" data-en="Lash Lift &amp; Brows">Lash Lift &amp; Brows</span><img src="assets/raw/bk-5.jpg" alt="Closeup of finished lash lift and brow lamination at ML Esthetics" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Extensiones de Pestañas" data-en="Eyelash Extensions">Eyelash Extensions</span><img src="assets/raw/bk-9.jpg" alt="Closeup of finished eyelash extensions at ML Esthetics" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Antes y Después · Lip Blush" data-en="Before &amp; After · Lip Blush">Before &amp; After · Lip Blush</span><img src="assets/raw/bk-11.jpg" alt="Before and after lip blush permanent makeup result at ML Esthetics" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:gallery_grid.start()] + NEW_GALLERY + h[gallery_grid.end():]
print("GALERIA done")

# ---------------------------------------------------------------------------
# 14. OPINIONES (3 reseñas reales verbatim de Booksy)
# ---------------------------------------------------------------------------
rep('<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 86 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 86 verified reviews on Booksy">5.0 out of 5 · 86 verified reviews on Booksy</span></p>',
    '<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms"><span class="stars">★★★★★</span> &nbsp;<span data-es="5.0 de 5 · 124 reseñas verificadas en Booksy" data-en="5.0 out of 5 · 124 verified reviews on Booksy">5.0 out of 5 · 124 verified reviews on Booksy</span></p>')

reviews_grid = re.search(
    r'<div class="grid sm:grid-cols-3 gap-5 items-stretch">.*?</div>\s*(?=<div class="text-center mt-10)',
    h, flags=re.S)
assert reviews_grid
NEW_REVIEWS = '''<div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <figure class="glass glass-hover rounded-3xl p-8 reveal flex flex-col">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Did brow lamination and lash lift and tint. They look amazing, super happy! Will defo be coming back"</blockquote>
          <figcaption class="text-sm mt-auto"><span class="font-medium">Tasmin C.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal flex flex-col" style="transition-delay:110ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Monica did a beautiful job shaping and defining my eyebrows. The result is a soft straight brow that looks clean, modern, and flattering for my face shape. The strokes are even and well-placed, giving a natural look without appearing too heavy."</blockquote>
          <figcaption class="text-sm mt-auto"><span class="font-medium">Akram B.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
        <figure class="glass glass-hover rounded-3xl p-8 reveal flex flex-col" style="transition-delay:220ms">
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5 text-sm">"Amazing lash lift ❤️ and so quick"</blockquote>
          <figcaption class="text-sm mt-auto"><span class="font-medium">jasmine m.</span> <span class="text-[color:var(--ink-40)]">· Booksy</span></figcaption>
        </figure>
      </div>
      '''
h = h[:reviews_grid.start()] + NEW_REVIEWS + h[reviews_grid.end():]

rep(f'<a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 86 reseñas en Booksy" data-en="Read all 86 reviews on Booksy">Read all 86 reviews on Booksy</a>',
    f'<a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Leer las 124 reseñas en Booksy" data-en="Read all 124 reviews on Booksy">Read all 124 reviews on Booksy</a>')
print("OPINIONES done")

# ---------------------------------------------------------------------------
# 15. UBICACION
# ---------------------------------------------------------------------------
rep('<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
    '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">Pompano Beach</span>')
rep('<p class="text-sm text-[color:var(--ink-60)] font-light">4580 Cresthaven Blvd (inside Lux Stitch Embroidery), West Palm Beach, FL 33415</p>',
    '<p class="text-sm text-[color:var(--ink-60)] font-light">575 S Cypress Rd, Pompano Beach, FL 33060</p>')
rep('href="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415"',
    'href="https://www.google.com/maps?q=575+S+Cypress+Rd,+Pompano+Beach,+FL+33060"')
rep('data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>',
    'data-es="Con cita previa vía Booksy: eliges servicio, día y hora, y la confirmación es inmediata." data-en="By appointment via Booksy: pick the service, day and time, and the confirmation is instant.">By appointment via Booksy: pick the service, day and time, and the confirmation is instant.</p>')
rep(f'<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,74,82,0.4)]" href="{BOOK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    f'<a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,74,82,0.4)]" href="{BOOK}" target="_blank" rel="noopener" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>')
rep('data-es="Mira los sets más recientes de Yesi y escribe por DM cualquier duda antes de tu cita." data-en="See Yesi\'s latest sets and DM any questions before your appointment.">See Yesi\'s latest sets and DM any questions before your appointment.</p>',
    'data-es="Mira los resultados más recientes de Monica y escribe por DM cualquier duda antes de tu cita." data-en="See Monica\'s latest work and DM any questions before your appointment.">See Monica\'s latest work and DM any questions before your appointment.</p>')
rep('title="Mapa: Lash Bloom, 4580 Cresthaven Blvd, West Palm Beach FL"',
    'title="Map: ML Esthetics, 575 S Cypress Rd, Pompano Beach FL"')
rep('src="https://www.google.com/maps?q=4580+Cresthaven+Blvd,+West+Palm+Beach,+FL+33415&output=embed"',
    'src="https://www.google.com/maps?q=575+S+Cypress+Rd,+Pompano+Beach,+FL+33060&output=embed"')

# Bloque adicional: Horario y Telefono, insertado tras el bloque de Instagram
ig_block_anchor = f'''          <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los resultados más recientes de Monica y escribe por DM cualquier duda antes de tu cita." data-en="See Monica's latest work and DM any questions before your appointment.">See Monica's latest work and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,74,82,0.4)]" href="{IG}" target="_blank" rel="noopener">@ml_esthetics1</a>
            </div>
          </div>
        </div>'''
assert ig_block_anchor in h, "NO ANCHOR: ig_block_anchor"
HOURS_BLOCK = f'''          <div>
              <p class="font-medium mb-1">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Mira los resultados más recientes de Monica y escribe por DM cualquier duda antes de tu cita." data-en="See Monica's latest work and DM any questions before your appointment.">See Monica's latest work and DM any questions before your appointment.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,74,82,0.4)]" href="{IG}" target="_blank" rel="noopener">@ml_esthetics1</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:320ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Horario y Teléfono" data-en="Hours &amp; Phone">Hours &amp; Phone</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Lunes a viernes 9am-7pm · Sábado 9am-9pm" data-en="Mon-Fri 9am-7pm · Sat 9am-9pm">Mon-Fri 9am-7pm · Sat 9am-9pm</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(138,74,82,0.4)]" href="tel:+13057206197">(305) 720-6197</a>
            </div>
        </div>'''
h = h.replace(ig_block_anchor, HOURS_BLOCK, 1)
print("UBICACION done")

# ---------------------------------------------------------------------------
# 16. CTA FINAL
# ---------------------------------------------------------------------------
rep('data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n      <h2',
    'data-es="Belleza que dura, hecha a tu medida." data-en="Beauty that lasts, made just for you.">Beauty that lasts, made just for you.</p>\n      <h2')
rep('<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
    '<span data-es="Tu nueva mirada" data-en="Your new look">Your new look</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>')
rep('data-es="Reserva online en segundos: tu set clásico, híbrido o de volumen, o el relleno que ya te toca." data-en="Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.">Book online in seconds: your classic, hybrid or volume set, or the fill you are due for.</p>',
    'data-es="Reserva en Booksy en segundos: tu microblading, lip blush, lash lift o el facial que ya te toca." data-en="Book on Booksy in seconds: your microblading, lip blush, lash lift, or the facial you are due for.">Book on Booksy in seconds: your microblading, lip blush, lash lift, or the facial you are due for.</p>')
rep(f'<a href="{BOOK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    f'<a href="{BOOK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Book on Booksy</a>')
print("CTA FINAL done")

# ---------------------------------------------------------------------------
# 17. FOOTER
# ---------------------------------------------------------------------------
rep('<span class="foot-mark" aria-hidden="true">Lash Bloom</span>', '<span class="foot-mark" aria-hidden="true">ML Esthetics</span>')
MONO_FOOT = '<span class="w-9 h-9 rounded-full ring-1 ring-[rgba(232,184,168,0.35)] bg-white/5 flex items-center justify-center font-display text-sm" aria-hidden="true">ML</span>'
rep('<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,184,168,0.35)]" loading="lazy" />',
    MONO_FOOT)
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>', '<span class="font-display text-lg tracking-[0.1em] uppercase">ML Esthetics</span>')
rep('data-es="Lash studio en West Palm Beach, FL. Atención con cita previa." data-en="Lash studio in West Palm Beach, FL. By appointment only.">Lash studio in West Palm Beach, FL. By appointment only.</p>',
    'data-es="Estudio de PMU, pestañas y cejas en Pompano Beach, FL. Atención con cita previa." data-en="Permanent makeup, lash &amp; brow studio in Pompano Beach, FL. By appointment only.">Permanent makeup, lash &amp; brow studio in Pompano Beach, FL. By appointment only.</p>')
rep('<p>4580 Cresthaven Blvd, West Palm Beach, FL 33415</p>', '<p>575 S Cypress Rd, Pompano Beach, FL 33060</p>')
rep(f'<p><a href="{BOOK}" target="_blank" rel="noopener" class="hover:text-[#e8b8a8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy</a></p>',
    f'''<p><a href="{BOOK}" target="_blank" rel="noopener" class="hover:text-[#e8b8a8]" data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Online booking · Booksy</a></p>
        <p><a href="tel:+13057206197" class="hover:text-[#e8b8a8]">(305) 720-6197</a></p>''')
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Lash Bloom.</p>', '<p class="text-xs text-[color:var(--ink-40)]">© 2026 ML Esthetics.</p>')
print("FOOTER done")

# ---------------------------------------------------------------------------
# 18. book-float
# ---------------------------------------------------------------------------
rep(f'<a href="{BOOK}" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">',
    f'<a href="{BOOK}" target="_blank" rel="noopener" class="book-float" aria-label="Book online">')

print("ALL DONE")
open(PATH, "w", encoding="utf-8").write(h)
print(len(h))
