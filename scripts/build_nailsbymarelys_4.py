import re

h = open('output/nailsbymarelys/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/608679_nails-by-marelys_nail-salon_15886_hialeah'

# ---------- SERVICIOS: grid completo reemplazado ----------
services_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', re.S)
m = services_re.search(h)
assert m, 'grid servicios no encontrado'
new_services = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Uso diario" data-en="Everyday">Everyday</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Manicure &amp; Pedicure Regular</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El combo clásico de manicura y pedicura regular. Por separado, manicura regular $20 o pedicura regular $35." data-en="The classic regular manicure and pedicure combo. Individually, regular manicure $20 or regular pedicure $35.">The classic regular manicure and pedicure combo. Individually, regular manicure $20 or regular pedicure $35.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,100,74,0.4); box-shadow: 0 18px 50px rgba(51,34,44,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Gel Manicure &amp; Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Esmalte en gel de larga duración en manos y pies. Gel manicura sola $45, gel pedicura sola $45, o ambas en gel por $80." data-en="Long-lasting gel polish on hands and feet. Gel manicure alone $45, gel pedicure alone $45, or both in gel for $80.">Long-lasting gel polish on hands and feet. Gel manicure alone $45, gel pedicure alone $45, or both in gel for $80.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$70</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Dip y acrílico" data-en="Dip &amp; Acrylic">Dip &amp; Acrylic</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Full Sets" data-en="Full Sets">Full Sets</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicure dip powder más pedicura en gel $90 (2h), o un full set en acrílico desde $65 (1h 30min). Hard gel también disponible desde $65." data-en="Dip powder manicure plus gel pedicure $90 (2h), or a full acrylic set from $65 (1h 30min). Hard gel also available from $65.">Dip powder manicure plus gel pedicure $90 (2h), or a full acrylic set from $65 (1h 30min). Hard gel also available from $65.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min+</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Extras" data-en="Add-ons">Add-ons</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Frances, Diseños y Cera" data-en="French, Art &amp; Wax">French, Art &amp; Wax</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Frances dip o gel $10, frances en pedicura $5, diseños desde $5, cera de cejas $10 y cera de bozo $10." data-en="French dip or gel $10, French pedicure $5, nail designs from $5, eyebrow wax $10 and lip wax $10.">French dip or gel $10, French pedicure $5, nail designs from $5, eyebrow wax $10 and lip wax $10.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$5+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">10min+</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_services + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="24 servicios en el menú. Lista completa y disponibilidad en Booksy." data-en="24 services on the menu. Full list and availability on Booksy.">24 services on the menu. Full list and availability on Booksy.</span></p>')

rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por Nails by Marelys en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Nails by Marelys on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Nails by Marelys en Booksy. Reserva con confirmación inmediata.</p>')

# ---------- GALERIA: grid completo reemplazado ----------
gallery_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', re.S)
mg = gallery_re.search(h)
assert mg, 'grid galeria no encontrado'
new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Acento en hoja de oro" data-en="Gold leaf accent">Gold leaf accent</span><img src="assets/raw/bk-6.jpg" alt="Nude gel manicure with a gold foil accent nail at Nails by Marelys" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Natural en el auto" data-en="Natural, on the go">Natural, on the go</span><img src="assets/raw/bk-1.jpg" alt="Nude manicure resting on a car dashboard" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Manos entrelazadas" data-en="Hands together">Hands together</span><img src="assets/raw/bk-3.jpg" alt="Nude gel manicure closeup with hands clasped together" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Sobre ruedas" data-en="On the go">On the go</span><img src="assets/raw/bk-4.jpg" alt="Nude manicure resting on a car steering wheel" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Blanco brillante" data-en="Glossy white">Glossy white</span><img src="assets/raw/bk-7.jpg" alt="Glossy white gel manicure at Nails by Marelys" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Frances iridiscente" data-en="Iridescent French">Iridescent French</span><img src="assets/raw/bk-5.jpg" alt="Iridescent French shimmer manicure at Nails by Marelys" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:mg.start()] + new_gallery + h[mg.end():]

rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Uñas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="nails">nails</span></h2>')

open('output/nailsbymarelys/index.html', 'w').write(h)
print('servicios + galeria OK')
