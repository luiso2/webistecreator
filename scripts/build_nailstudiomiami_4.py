import re

h = open('output/nailstudiomiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- SERVICIOS: grid completo reemplazado ----------
services_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', re.S)
m = services_re.search(h)
assert m, 'grid servicios no encontrado'
BOOKSY = 'https://booksy.com/en-us/418314_the-nail-studio-miami_nail-salon_15889_miami'
new_services = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Uso diario" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Regular Manicure &amp; Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo clásico: manicura regular y pedicura regular, con esmalte incluido. Por separado, manicura $30 o pedicura $30." data-en="The classic combo: regular manicure and regular pedicure, polish included. Individually, manicure $30 or pedicure $30.">The classic combo: regular manicure and regular pedicure, polish included. Individually, manicure $30 or pedicure $30.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$55</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(74,114,173,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel Manicure &amp; Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Esmalte en gel de larga duración en manos y pies, el set que más reservan las clientas. Manicura en gel sola $40, pedicura en gel sola $40." data-en="Long-lasting gel polish on hands and feet, the set most clients book. Gel manicure alone $40, gel pedicure alone $40.">Long-lasting gel polish on hands and feet, the set most clients book. Gel manicure alone $40, gel pedicure alone $40.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Acrílico y Apres" data-en="Acrylic &amp; Apres">Acrylic &amp; Apres</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Sets" data-en="Full Sets">Full Sets</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Rellenos de acrílico con esmalte en gel más pedicura en gel desde $85, o un set completo de Apres Gel X desde $60 (1h 30min)." data-en="Acrylic refills with gel polish plus gel pedicure from $85, or a full Apres Gel X set from $60 (1h 30min).">Acrylic refills with gel polish plus gel pedicure from $85, or a full Apres Gel X set from $60 (1h 30min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$85+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min+</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Add-ons">Add-ons</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cera y Retoques" data-en="Wax &amp; Touch-ups">Wax &amp; Touch-ups</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura y pedicura para hombres $50, cera de labio $8, cera de cejas $10, cambio de esmalte en gel $20, retiro de acrílico $20." data-en="Men's manicure &amp; pedicure $50, lip wax $8, eyebrow wax $10, gel polish change $20, acrylic soak off $20.">Men's manicure &amp; pedicure $50, lip wax $8, eyebrow wax $10, gel polish change $20, acrylic soak off $20.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$20+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">15min+</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_services + h[m.end():]

# Nota de servicios
rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="19 servicios en el menú. Lista completa y disponibilidad en Booksy." data-en="19 services on the menu. Full list and availability on Booksy.">19 services on the menu. Full list and availability on Booksy.</span></p>')

rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por The Nail Studio Miami en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by The Nail Studio Miami on Booksy. Booking confirms instantly.">Prices and durations as published by The Nail Studio Miami on Booksy. Booking confirms instantly.</p>')

# ---------- GALERIA: grid completo reemplazado ----------
gallery_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', re.S)
mg = gallery_re.search(h)
assert mg, 'grid galeria no encontrado'
new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Set nuevo, clienta feliz" data-en="Fresh set, happy client">Fresh set, happy client</span><img src="assets/raw/bk-6.jpg" alt="Pink ombre gel manicure with a gold ring at The Nail Studio Miami" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Azul clásico" data-en="Classic blue">Classic blue</span><img src="assets/raw/bk-16.jpg" alt="Classic blue gel manicure" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Negro con actitud" data-en="Bold black">Bold black</span><img src="assets/raw/bk-9.jpg" alt="Bold black gel manicure closeup" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Arte pintado a mano" data-en="Hand-painted art">Hand-painted art</span><img src="assets/raw/bk-14.jpg" alt="Pink hand-painted floral nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Sobre ruedas" data-en="On the go">On the go</span><img src="assets/raw/bk-10.jpg" alt="Blue gel manicure resting on a car steering wheel" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Uñas con carácter" data-en="Statement nails">Statement nails</span><img src="assets/raw/bk-8.jpg" alt="Black nails with a bold orange accent nail" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:mg.start()] + new_gallery + h[mg.end():]

rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nails">nails</span></h2>')

open('output/nailstudiomiami/index.html', 'w').write(h)
print('servicios + galeria OK')
