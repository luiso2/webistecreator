import re

h = open('output/superiorsoftwashmiramar/index.html', encoding='utf-8').read()


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c >= n, f'NO (found {c}, need {n}): {a[:120]}'
    h = h.replace(a, b, n)


# ---------------------------------------------------------------------------
# SERVICIOS: grid entero por regex (4 cards, card 2 destacada, sin precios)
# ---------------------------------------------------------------------------
services_re = re.compile(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    flags=re.S
)
assert services_re.search(h), 'no se encontro el grid de servicios'

new_services = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Seguro para el techo" data-en="Roof safe">Roof safe</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Roof Soft Washing" data-en="Roof Soft Washing">Roof Soft Washing</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Química de baja presión que elimina estrías negras, algas y liquen de techos de teja o shingle sin dañar el material, a diferencia de la presión alta." data-en="Low-pressure, roof-safe chemicals that remove black streaks, algae and lichen from tile and shingle roofs without damaging the material the way high pressure can.">Low-pressure, roof-safe chemicals that remove black streaks, algae and lichen from tile and shingle roofs without damaging the material the way high pressure can.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Cotización según el techo" data-en="Priced per roof">Priced per roof</p>
            <a href="tel:+19548822870" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(31,107,115,0.4); box-shadow: 0 18px 50px rgba(27,44,46,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="El más pedido" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="House &amp; Exterior Wash" data-en="House &amp; Exterior Wash">House &amp; Exterior Wash</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Soft wash completo de estuco, siding y ventanas: fuera el moho, el mildew y la suciedad acumulada sin forzar la pintura ni el sellador." data-en="Full soft wash of stucco, siding and windows: mold, mildew and built-up grime gone without stressing paint or sealant.">Full soft wash of stucco, siding and windows: mold, mildew and built-up grime gone without stressing paint or sealant.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Cotización según la casa" data-en="Priced per home">Priced per home</p>
            <a href="tel:+19548822870" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Concreto y pavers" data-en="Concrete &amp; pavers">Concrete &amp; pavers</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Driveway &amp; Paver Cleaning" data-en="Driveway &amp; Paver Cleaning">Driveway &amp; Paver Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Limpieza a presión de entradas, caminos y pavers: fuera las manchas negras y el musgo para dejar el concreto como nuevo." data-en="Pressure cleaning for driveways, walkways and pavers: black stains and moss gone, concrete looking new again.">Pressure cleaning for driveways, walkways and pavers: black stains and moss gone, concrete looking new again.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Cotización según el área" data-en="Priced per area">Priced per area</p>
            <a href="tel:+19548822870" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Zona de descanso" data-en="Outdoor living">Outdoor living</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Pool Deck &amp; Patio Cleaning" data-en="Pool Deck &amp; Patio Cleaning">Pool Deck &amp; Patio Cleaning</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Terrazas, patios y áreas de piscina sin resbalones ni manchas de algas, con presión ajustada a cada material." data-en="Pool decks, patios and lanai floors free of algae film and stains, with pressure matched to each material.">Pool decks, patios and lanai floors free of algae film and stains, with pressure matched to each material.</p>
          <div class="mt-auto">
            <p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide mb-5" data-es="Cotización según el patio" data-en="Priced per patio">Priced per patio</p>
            <a href="tel:+19548822870" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      '''
h = services_re.sub(new_services, h, count=1)

rep('data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    'data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Techo, casa y" data-en="Roof, home and">Roof, home and</span> <span class="text-shine" data-es="propiedad" data-en="property">property</span></h2>')

rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Cada trabajo se cotiza según el tamaño y el estado de la superficie. Llámanos y te damos un precio real." data-en="Every job is priced based on size and surface condition. Call us and we will quote it for real.">Every job is priced based on size and surface condition. Call us and we will quote it for real.</p>')

note_re = re.compile(r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)', flags=re.S)
assert note_re.search(h), 'no se encontro la nota de servicios'
h = note_re.sub(lambda m: m.group(1) + '<span data-es="Sin listas de precios fijos: cada trabajo se cotiza. Escríbenos por Instagram o llama al (954) 882-2870." data-en="No fixed price list: every job is quoted. Message us on Instagram or call (954) 882-2870.">No fixed price list: every job is quoted. Message us on Instagram or call (954) 882-2870.</span>' + m.group(2), h, count=1)

# ---------------------------------------------------------------------------
# GALERIA: grid entero por regex, fotos curadas reales
# ---------------------------------------------------------------------------
gallery_re = re.compile(
    r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
    flags=re.S
)
assert gallery_re.search(h), 'no se encontro el grid de galeria'

new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Tratamiento soft wash en techo" data-en="Roof soft wash treatment">Roof soft wash treatment</span><img src="assets/raw/gal-wide.jpg" alt="Roof soft wash chemical treatment mid-application on a shingle roof" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Terraza de piscina" data-en="Pool deck pavers">Pool deck pavers</span><img src="assets/raw/gal-2.jpg" alt="Pressure-cleaned travertine pool deck pavers" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Entrada después de limpiar" data-en="Driveway, after">Driveway, after</span><img src="assets/raw/gal-3.jpg" alt="Clean concrete driveway after pressure washing" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Lanai y piscina" data-en="Screened pool lanai">Screened pool lanai</span><img src="assets/raw/gal-4.jpg" alt="Screened pool lanai and paver deck after cleaning" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Fachada antes de limpiar" data-en="Exterior wall, before">Exterior wall, before</span><img src="assets/raw/gal-5.jpg" alt="Algae and mildew stains on an exterior wall before soft washing" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Camino de pavers" data-en="Paver walkway">Paver walkway</span><img src="assets/raw/gal-6.jpg" alt="Paver walkway before pressure cleaning" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = gallery_re.sub(new_gallery, h, count=1)

rep('<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
    '<span data-es="Trabajos" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span>')

# ---------------------------------------------------------------------------
# IMAGENES: hero + experiencia (la galeria ya quedo con sus fotos arriba)
# ---------------------------------------------------------------------------
rep('<img src="assets/raw/bk-6.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/hero-1.jpg" alt="Freshly soft-washed tile roof under a clear Broward County sky" class="blur-up w-full h-full object-cover" />')

rep('<img src="assets/raw/hero-1.jpg" alt="El suite de Lash Bloom con su letrero neon rosa" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/about-1.jpg" alt="Superior Soft Wash truck and pressure washing equipment on site" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/about-2.jpg" alt="Rincon del estudio con letrero neon y repisas rosas" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/about-2.jpg" alt="Surface cleaner attachment mid-job on a paver patio at night" class="blur-up w-full h-full object-cover" loading="lazy" />')

print('OK: servicios/galeria/imagenes hero+about')
open('output/superiorsoftwashmiramar/index.html', 'w', encoding='utf-8').write(h)
