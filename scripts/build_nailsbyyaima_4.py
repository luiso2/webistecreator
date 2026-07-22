import re

h = open('output/nailsbyyaima/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/1019645_nails-by-yaima_nail-salon_15761_tampa'

# ---------- SERVICIOS: grid completo reemplazado ----------
services_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', re.S)
m = services_re.search(h)
assert m, 'grid servicios no encontrado'
new_services = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Uso diario" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Clásica y de Spa" data-en="Classic &amp; Spa Manicure">Classic &amp; Spa Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="La manicura clásica de siempre, o la manicura de spa de lujo con más mimo y masaje. Manicura clásica $23, manicura de spa de lujo $55 (1h)." data-en="The classic manicure regulars come back for, or the luxury spa manicure with extra pampering and a longer massage. Classic manicure $23, luxury spa manicure $55 (1h).">The classic manicure regulars come back for, or the luxury spa manicure with extra pampering and a longer massage. Classic manicure $23, luxury spa manicure $55 (1h).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$23+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Hasta 1h" data-en="Up to 1h">Up to 1h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(212,191,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma del estudio" data-en="Studio signature">Studio signature</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Russian Gel Manicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Su servicio más pedido: trabajo preciso de cutícula y un acabado duradero tipo cristal. $75, 1h 15min." data-en="Her most requested service: precise cuticle work and a long-lasting, glass-like finish. $75, 1h 15min.">Her most requested service: precise cuticle work and a long-lasting, glass-like finish. $75, 1h 15min.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$75</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 15min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Builder Gel" data-en="Builder Gel">Builder Gel</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Overlay y Extensiones" data-en="Overlay &amp; Extensions">Overlay &amp; Extensions</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Overlay de builder gel sobre uña natural desde $59, o extensiones cortas, medianas o largas desde $63 hasta $90, hasta 1h 45min de trabajo." data-en="Builder gel overlay on natural nails from $59, or short, medium and long extensions from $63 to $90, up to 1h 45min of hands-on work.">Builder gel overlay on natural nails from $59, or short, medium and long extensions from $63 to $90, up to 1h 45min of hands-on work.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$59+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Hasta 1h 45min" data-en="Up to 1h 45min">Up to 1h 45min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Rellenos y Remoción" data-en="Refills &amp; Removal">Refills &amp; Removal</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Mantenimiento" data-en="Upkeep">Upkeep</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Relleno de builder gel hasta 3 semanas $50, relleno de hard gel de 3 a 5 semanas $60, remoción de esmalte en gel $14, y remoción de hard gel/acrílico/dip powder $18." data-en="Builder gel refill up to 3 weeks $50, hard gel refill for 3 to 5 weeks of growth $60, gel polish removal $14, and hard gel/acrylic/dip powder removal $18.">Builder gel refill up to 3 weeks $50, hard gel refill for 3 to 5 weeks of growth $60, gel polish removal $14, and hard gel/acrylic/dip powder removal $18.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$14+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Desde 15min" data-en="From 15min">From 15min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_services + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="11 servicios en el menú. Lista completa y disponibilidad en Booksy." data-en="11 services on the menu. Full list and availability on Booksy.">11 services on the menu. Full list and availability on Booksy.</span></p>')

rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Nails by Yaima en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Nails by Yaima on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Nails by Yaima en Booksy. Reserva con confirmación inmediata.</p>')

# ---------- GALERIA: grid completo reemplazado ----------
gallery_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', re.S)
mg = gallery_re.search(h)
assert mg, 'grid galeria no encontrado'
new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Diseño personalizado" data-en="Custom nail art">Custom nail art</span><img src="assets/raw/bk-8.jpg" alt="Colorful floral nail art design by Nails by Yaima" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Extensiones en Builder Gel" data-en="Builder gel extensions">Builder gel extensions</span><img src="assets/raw/bk-5.jpg" alt="Nude stiletto builder gel nail extensions" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Manicura de Gel Ruso" data-en="Russian gel manicure">Russian gel manicure</span><img src="assets/raw/bk-6.jpg" alt="Nude square Russian gel manicure" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Manicura Clásica" data-en="Classic manicure">Classic manicure</span><img src="assets/raw/bk-7.jpg" alt="Soft pink round classic manicure" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Diseño Francés" data-en="French tip design">French tip design</span><img src="assets/raw/bk-9.jpg" alt="Light blue ombre nails with a gold glitter French tip" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Extensiones Largas" data-en="Long extensions">Long extensions</span><img src="assets/raw/bk-10.jpg" alt="Long nude stiletto builder gel nail extensions" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:mg.start()] + new_gallery + h[mg.end():]

rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span></h2>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nails">nails</span></h2>')

open('output/nailsbyyaima/index.html', 'w').write(h)
print('servicios + galeria OK')
