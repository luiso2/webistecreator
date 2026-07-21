import re

h = open('output/nailsbynicky/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/421799_nails-by-nicky_nail-salon_15886_hialeah'

# ---------- SERVICIOS: grid completo reemplazado ----------
services_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', re.S)
m = services_re.search(h)
assert m, 'grid servicios no encontrado'
new_services = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(212,75,98,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">House signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Russian Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura rusa con sistemas luminary de larga duración, la técnica de precision que distingue el estudio. 2 horas dedicadas." data-en="Russian manicure with long-lasting luminary systems, the precision technique that sets the studio apart. A dedicated 2 hours.">Russian manicure with long-lasting luminary systems, the precision technique that sets the studio apart. A dedicated 2 hours.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">2h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Set &amp; Pedicura" data-en="Full Set &amp; Pedicure">Full Set &amp; Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Full set de Apres Gel X más pedicura clásica $100 (2h 15min), o con pedicura en gel $110. El set solo, $65 (1h 30min)." data-en="Apres Gel X full set plus a classic pedicure $100 (2h 15min), or with a gel pedicure $110. The set alone, $65 (1h 30min).">Apres Gel X full set plus a classic pedicure $100 (2h 15min), or with a gel pedicure $110. The set alone, $65 (1h 30min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min+</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Luminary Gel" data-en="Luminary Gel">Luminary Gel</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura &amp; Pedicura" data-en="Manicure &amp; Pedicure">Manicure &amp; Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura luminary gel $75 combinada con pedicura regular ($110 en total) o pedicura en gel ($120 en total)." data-en="Luminary gel manicure $75 paired with a regular pedicure ($110 total) or a gel pedicure ($120 total).">Luminary gel manicure $75 paired with a regular pedicure ($110 total) or a gel pedicure ($120 total).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$110+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">3h 30min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Add-ons">Add-ons</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Nail Art &amp; Cristales" data-en="Nail Art &amp; Crystals">Nail Art &amp; Crystals</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Nail art desde $5 (2 uñas) hasta $15 (10 uñas), cristales Swarovski desde $5 cada 2 uñas, frances desde $10 y quitado de apres $8." data-en="Nail art from $5 (2 nails) up to $15 (10 nails), Swarovski crystals from $5 per 2 nails, French from $10 and Apres removal $8.">Nail art from $5 (2 nails) up to $15 (10 nails), Swarovski crystals from $5 per 2 nails, French from $10 and Apres removal $8.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$5+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">5min+</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_services + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="16 servicios en el menú. Lista completa y disponibilidad en Booksy." data-en="16 services on the menu. Full list and availability on Booksy.">16 services on the menu. Full list and availability on Booksy.</span></p>')

rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Nails By Nicky en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Nails By Nicky on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Nails By Nicky en Booksy. Reserva con confirmación inmediata.</p>')

# ---------- GALERIA: grid completo reemplazado (5 fotos reales: bk-1,4,5,7,8; se reduce de 6 a 5 tiles, sin rellenar con thumbnails 100x100) ----------
gallery_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', re.S)
mg = gallery_re.search(h)
assert mg, 'grid galeria no encontrado'
new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Frances minimalista" data-en="Minimalist French">Minimalist French</span><img src="assets/raw/bk-4.jpg" alt="Minimalist nude French manicure with a tiny evil eye accent at Nails By Nicky" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Rojo brillante" data-en="Glossy red">Glossy red</span><img src="assets/raw/bk-1.jpg" alt="Glossy red gel manicure with a fine dot accent" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Detalle de ojo turco" data-en="Evil eye detail">Evil eye detail</span><img src="assets/raw/bk-5.jpg" alt="Closeup of nude gel nails with an evil eye accent nail" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Arte de temporada" data-en="Seasonal art">Seasonal art</span><img src="assets/raw/bk-7.jpg" alt="Neon green and black ghost nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Rosa con brillo" data-en="Pink with sparkle">Pink with sparkle</span><img src="assets/raw/bk-8.jpg" alt="Soft pink gel manicure with a glitter accent nail" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:mg.start()] + new_gallery + h[mg.end():]

rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nails">nails</span></h2>')

open('output/nailsbynicky/index.html', 'w').write(h)
print('servicios + galeria OK')
