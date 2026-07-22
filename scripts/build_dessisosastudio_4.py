import re

h = open('output/dessisosastudio/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:220]
    h = h.replace(a, b, n)

# ================= SERVICIOS: encabezado =================
rep('<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>',
    '<h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine" data-es="servicio" data-en="service">servicio</span></h2>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por DessiSosa Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by DessiSosa Studio on Booksy. Booking confirms instantly.">Precios y duraciones publicados por DessiSosa Studio en Booksy. Reserva con confirmación inmediata.</p>')

BOOKSY = 'https://booksy.com/en-us/57332_dessisosa-studio_nail-salon_15761_tampa'

# ================= SERVICIOS: grid de destacados (4 cards) reemplazo completo =================
grid_pattern = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', flags=re.S)
m = grid_pattern.search(h)
assert m, 'grid destacados no encontrado'

new_highlights = '''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="border-color: rgba(75,98,212,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Firma de la casa" data-en="House signature">Firma de la casa</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Extensión de Pestañas" data-en="Lash Extensions">Extensión de Pestañas</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Set completo de pestañas aplicado pelo a pelo, clásico o de volumen según lo que busques. Desde $115, 1h 45min dedicadas." data-en="A full lash set applied lash by lash, classic or volume depending on what you want. From $115, a dedicated 1h 45min.">Set completo de pestañas aplicado pelo a pelo, clásico o de volumen según lo que busques. Desde $115, 1h 45min dedicadas.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$115</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 45min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Uñas" data-en="Nails">Uñas</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Manicura Gel" data-en="Gel Manicure">Manicura Gel</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Manicura en gel con acabado brillante y duradero, en el color que elijas, cuidando la uña natural." data-en="Gel manicure with a glossy, long-lasting finish, in the color you choose, caring for the natural nail.">Manicura en gel con acabado brillante y duradero, en el color que elijas, cuidando la uña natural.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies" data-en="Feet">Pies</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pedicure completo con exfoliación, hidratación y esmaltado, una hora dedicada al cuidado de tus pies." data-en="A full pedicure with exfoliation, hydration and polish, a full hour dedicated to your feet.">Pedicure completo con exfoliación, hidratación y esmaltado, una hora dedicada al cuidado de tus pies.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$50</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Uñas" data-en="Nails">Uñas</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Acrylic Nails</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Extensión en acrílico en la forma y largo que prefieras, base resistente y lista para diseño." data-en="Acrylic extensions in the shape and length you prefer, a durable base ready for nail art.">Extensión en acrílico en la forma y largo que prefieras, base resistente y lista para diseño.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p></div>
            <a href="''' + BOOKSY + '''" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>

      <!-- Menu completo por categoria -->
      <div class="grid lg:grid-cols-3 gap-5 mt-10">
        <div class="glass rounded-3xl p-7 reveal">
          <h3 class="font-display text-xl mb-5" data-es="Pestañas &amp; Cejas" data-en="Lashes &amp; Brows">Pestañas &amp; Cejas</h3>
          <div class="divide-y divide-[color:var(--accent-ghost)] text-sm">
            <div class="flex items-center justify-between py-3"><span data-es="Extensión de pestañas" data-en="Lash extensions">Extensión de pestañas</span><span class="font-display text-lg">$115</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Retoque de pestañas 3 semanas" data-en="Lash fill, 3 weeks">Retoque de pestañas 3 semanas</span><span class="font-display text-lg">$80</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Retoque de pestañas 2 semanas" data-en="Lash fill, 2 weeks">Retoque de pestañas 2 semanas</span><span class="font-display text-lg">$65</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Diseño, depilación y tinte de cejas" data-en="Brow shaping, wax &amp; tint">Diseño, depilación y tinte de cejas</span><span class="font-display text-lg">$45</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Depilación de cejas" data-en="Eyebrow wax">Depilación de cejas</span><span class="font-display text-lg">$15</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:90ms">
          <h3 class="font-display text-xl mb-5" data-es="Uñas" data-en="Nails">Uñas</h3>
          <div class="divide-y divide-[color:var(--accent-ghost)] text-sm">
            <div class="flex items-center justify-between py-3"><span data-es="Manicura gel" data-en="Gel manicure">Manicura gel</span><span class="font-display text-lg">$30</span></div>
            <div class="flex items-center justify-between py-3"><span>Acrylic nails</span><span class="font-display text-lg">$65</span></div>
            <div class="flex items-center justify-between py-3"><span>Polygel</span><span class="font-display text-lg">$65</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Rubber gel" data-en="Rubber gel">Rubber gel</span><span class="font-display text-lg">$65</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Builder gel" data-en="Builder gel">Builder gel</span><span class="font-display text-lg">$65</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Cambio de color" data-en="Color change">Cambio de color</span><span class="font-display text-lg">$25</span></div>
            <div class="flex items-center justify-between py-3"><span>Pedicure</span><span class="font-display text-lg">$50</span></div>
          </div>
        </div>
        <div class="glass rounded-3xl p-7 reveal" style="transition-delay:180ms">
          <h3 class="font-display text-xl mb-5" data-es="Cabello" data-en="Hair">Cabello</h3>
          <div class="divide-y divide-[color:var(--accent-ghost)] text-sm">
            <div class="flex items-center justify-between py-3"><span data-es="Corte y secado" data-en="Cut &amp; blowout">Corte y secado</span><span class="font-display text-lg">$55</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Secado" data-en="Blowout">Secado</span><span class="font-display text-lg">$40</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Retoque de raíz y secado" data-en="Root touch-up &amp; blowout">Retoque de raíz y secado</span><span class="font-display text-lg">$85</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Alisado" data-en="Blowout smoothing">Alisado</span><span class="font-display text-lg">$200</span></div>
            <div class="flex items-center justify-between py-3"><span data-es="Hidratación" data-en="Deep conditioning">Hidratación</span><span class="font-display text-lg">$150</span></div>
            <div class="flex items-center justify-between py-3"><span>Highlights</span><span class="font-display text-lg">$250</span></div>
            <div class="flex items-center justify-between py-3"><span>Balayage</span><span class="font-display text-lg">$300</span></div>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_highlights + h[m.end():]

# ================= SERVICIOS: nota final =================
nota_pattern = re.compile(r'<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">.*?</p>', flags=re.S)
m2 = nota_pattern.search(h)
assert m2, 'nota de servicios no encontrada'
new_nota = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Todos los precios y duraciones son los publicados por DessiSosa Studio en Booksy." data-en="All prices and durations are as published by DessiSosa Studio on Booksy.">Todos los precios y duraciones son los publicados por DessiSosa Studio en Booksy.</span></p>'
h = h[:m2.start()] + new_nota + h[m2.end():]

open('output/dessisosastudio/index.html', 'w').write(h)
print('servicios OK')
