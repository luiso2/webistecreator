import re
SLUG = 'output/2-veterans-handyman-service/index.html'
h = open(SLUG, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    cnt = h.count(a)
    assert cnt == n, f'NO (found {cnt}, need {n}): {a[:140]!r}'
    h = h.replace(a, b, n)

PHONE_TEL = '+17542667735'
FB_URL = 'https://www.facebook.com/2veteranshandymanservice/'

# ---------- SERVICIOS header ----------
rep(
'''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>''',
'''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo del hogar para" data-en="Home work for">Home work for</span> <span class="text-shine" data-es="cada necesidad" data-en="every need">every need</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Cada trabajo recibe su propia cotizacion gratis por telefono antes de que empiece cualquier reparacion." data-en="Every job gets its own free quote by phone before any repair starts.">Every job gets its own free quote by phone before any repair starts.</p>'''
)

# ---------- SERVICIOS grid (4 cards) ----------
old_grid = re.search(r'(      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\n      </div>\n)(      <p class="reveal text-center text-xs)', h, flags=re.S)
assert old_grid, 'services grid not found'
new_grid = f'''      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(63,152,103,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Lo mas solicitado" data-en="Most requested">Most requested</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reparacion de Drywall" data-en="Drywall Repair">Drywall Repair</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Parches, textura knockdown e instalacion de drywall. El trabajo que las resenas destacan como el mas recomendado del equipo." data-en="Patching, knockdown texture blending and drywall installation. The work customer reviews call out most when recommending the crew.">Patching, knockdown texture blending and drywall installation. The work customer reviews call out most when recommending the crew.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for a quote">Call for a quote</p></div>
            <a href="tel:{PHONE_TEL}" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cocinas y banos" data-en="Kitchens &amp; baths">Kitchens &amp; baths</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Remodelacion de Cocina y Bano" data-en="Kitchen &amp; Bathroom Remodeling">Kitchen &amp; Bathroom Remodeling</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Remodelacion de cocinas y banos, cabinetes construidos e instalados, y acabados que dejan el espacio como nuevo." data-en="Kitchen and bathroom remodeling, custom-built and installed cabinets, and finishes that leave the space looking new.">Kitchen and bathroom remodeling, custom-built and installed cabinets, and finishes that leave the space looking new.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for a quote">Call for a quote</p></div>
            <a href="tel:{PHONE_TEL}" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Montajes y accesorios" data-en="Installs &amp; fixtures">Installs &amp; fixtures</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Instalaciones y Montajes" data-en="Installations &amp; Fixtures">Installations &amp; Fixtures</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Montaje de TV con cables ocultos, ventiladores de techo, luces, puertas para mascotas y cerraduras." data-en="Wall-mounted TVs with hidden wires, ceiling fans, light fixtures, dog doors and door and lock repairs.">Wall-mounted TVs with hidden wires, ceiling fans, light fixtures, dog doors and door and lock repairs.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for a quote">Call for a quote</p></div>
            <a href="tel:{PHONE_TEL}" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Mantenimiento general" data-en="General upkeep">General upkeep</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Reparaciones del Hogar" data-en="Home Repairs &amp; Maintenance">Home Repairs &amp; Maintenance</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Reparacion de buzones, cercas, puertas y fascias danadas por tormenta, mas servicio disponible las 24 horas para emergencias." data-en="Mailbox, fence, door and storm-damaged fascia repairs, plus availability around the clock for emergency calls.">Mailbox, fence, door and storm-damaged fascia repairs, plus availability around the clock for emergency calls.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-lg text-shine" data-es="Llama para cotizar" data-en="Call for a quote">Call for a quote</p></div>
            <a href="tel:{PHONE_TEL}" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Llamar" data-en="Call">Call</a>
          </div>
        </div>
      </div>
      <div class="mt-14 grid sm:grid-cols-3 gap-5">
        <div class="glass rounded-3xl p-7 reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Drywall y Pintura" data-en="Drywall &amp; Paint">Drywall &amp; Paint</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Parches y reparacion de drywall" data-en="Drywall patching &amp; repair">Drywall patching &amp; repair</li>
            <li class="flex items-center gap-2" data-es="Instalacion de drywall" data-en="Drywall installation">Drywall installation</li>
            <li class="flex items-center gap-2" data-es="Textura knockdown" data-en="Knockdown texture blending">Knockdown texture blending</li>
            <li class="flex items-center gap-2" data-es="Retoques de pintura" data-en="Paint touch-ups">Paint touch-ups</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Montajes y Accesorios" data-en="Installs &amp; Fixtures">Installs &amp; Fixtures</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Montaje de TV con cables ocultos" data-en="TV mounts with hidden wires">TV mounts with hidden wires</li>
            <li class="flex items-center gap-2" data-es="Ventiladores de techo" data-en="Ceiling fan installation">Ceiling fan installation</li>
            <li class="flex items-center gap-2" data-es="Luces y accesorios" data-en="Light fixtures">Light fixtures</li>
            <li class="flex items-center gap-2" data-es="Cabinetes a medida" data-en="Custom cabinets">Custom cabinets</li>
          </ul>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Reparaciones del Hogar" data-en="Home Repairs">Home Repairs</p>
          <ul class="space-y-3 text-sm text-[color:var(--ink-60)] font-light">
            <li class="flex items-center gap-2" data-es="Puertas y cerraduras" data-en="Doors &amp; locks">Doors &amp; locks</li>
            <li class="flex items-center gap-2" data-es="Buzones y cercas" data-en="Mailbox &amp; fence repair">Mailbox &amp; fence repair</li>
            <li class="flex items-center gap-2" data-es="Reparaciones de plomeria menor" data-en="Minor plumbing fixes">Minor plumbing fixes</li>
            <li class="flex items-center gap-2" data-es="Cotizaciones gratis" data-en="Free estimates">Free estimates</li>
          </ul>
        </div>
      </div>
'''
h = h[:old_grid.start(1)] + new_grid + h[old_grid.end(1):]

rep(
'''<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>''',
'''<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="El precio depende del alcance del trabajo. Llama al (754) 266-7735 para una cotizacion gratis." data-en="Pricing depends on the scope of the job. Call (754) 266-7735 for a free quote.">Pricing depends on the scope of the job. Call (754) 266-7735 for a free quote.</span></p>'''
)

# ---------- GALERIA header + link ----------
rep(
'''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>
        </div>
        <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          @pure.artistrysk
        </a>''',
f'''<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="work">work</span></h2>
        </div>
        <a href="{FB_URL}" target="_blank" rel="noopener" class="reveal btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2" style="transition-delay:160ms">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3Z"/></svg>
          Facebook
        </a>'''
)

# ---------- GALERIA grid ----------
old_gal = '''      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Twists definidos" data-en="Defined twists">Defined twists</span><img src="assets/raw/bk-13.jpg" alt="Twists largos y definidos hechos en Pure Artistry" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Ondas plateadas" data-en="Silver waves">Silver waves</span><img src="assets/raw/bk-12.jpg" alt="Cabello con ondas y reflejos plateados" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Cornrows con diseño" data-en="Design cornrows">Design cornrows</span><img src="assets/raw/bk-7.jpg" alt="Cornrows con diseño geometrico" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Silk press con capas" data-en="Layered silk press">Layered silk press</span><img src="assets/raw/bk-3.jpg" alt="Silk press con capas y movimiento" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Locs con color" data-en="Colored locs">Colored locs</span><img src="assets/raw/bk-10.jpg" alt="Locs con puntas de color" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Rizos grises" data-en="Silver curls">Silver curls</span><img src="assets/raw/bk-5.jpg" alt="Rizos definidos en tono gris plata" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>'''
new_gal = '''      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-5">
        <div class="frame zoomable sm:col-span-2 aspect-[2/1] img-reveal"><span class="tile-cap" data-es="Remodelacion de cocina" data-en="Kitchen remodel">Kitchen remodel</span><img src="assets/gallery-kitchen-backsplash.jpg" alt="Finished kitchen remodel with new countertops and backsplash by 2 Veterans Handyman Service" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Remodelacion de bano" data-en="Bathroom vanity">Bathroom vanity</span><img src="assets/gallery-bathroom-vanity.jpg" alt="Finished bathroom vanity and toilet installation by 2 Veterans Handyman Service" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[4/3] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Espejos de bano" data-en="Bathroom mirrors">Bathroom mirrors</span><img src="assets/gallery-bathroom-mirrors.jpg" alt="Finished bathroom mirrors and corner cabinet installed by 2 Veterans Handyman Service" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>'''
rep(old_gal, new_gal)

open(SLUG, 'w', encoding='utf-8').write(h)
print('SERVICIOS+GALERIA OK, length', len(h))
