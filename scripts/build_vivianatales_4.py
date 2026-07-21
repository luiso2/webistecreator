import re

h = open('output/vivianatales/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/941017_viviana-tales-lash-studio_brows-lashes_15889_miami'

rep('data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Servicios" data-en="Services">Servicios</p>\n        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span></h2>\n        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Precios y duraciones publicados por Viviana Tales Lash Studio en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Viviana Tales Lash Studio on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Viviana Tales Lash Studio en Booksy. Reserva con confirmación inmediata.</p>')

# ---------- SERVICIOS: grid completo reemplazado ----------
services_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', re.S)
m = services_re.search(h)
assert m, 'grid servicios no encontrado'
new_services = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Efecto natural" data-en="Natural effect">Efecto natural</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Classic Full Set</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Una extensión por pestaña natural para un efecto limpio de siempre. Refill clásico desde $80 (1h 30min)." data-en="One extension per natural lash for a clean, everyday effect. Classic refill from $80 (1h 30min).">Una extensión por pestaña natural para un efecto limpio de siempre. Refill clásico desde $80 (1h 30min).</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="Full set" data-en="Full set">Full set</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(140,63,82,0.4); box-shadow: 0 18px 50px rgba(46,25,20,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Favorito del estudio</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Soft Volume Lashes</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Abanicos suaves de volumen para densidad natural con más cuerpo. Refill de volumen suave desde $90." data-en="Soft volume fans for natural density with more body. Soft volume refill from $90.">Abanicos suaves de volumen para densidad natural con más cuerpo. Refill de volumen suave desde $90.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$130</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Máximo impacto" data-en="Maximum impact">Máximo impacto</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Wispy &amp; Mega Volume</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Textura wispy con puntas definidas por $140 (1h 35min), o mega volumen para densidad total por $150 (1h 40min). Refill de mega volumen desde $100." data-en="Wispy texture with defined tips at $140 (1h 35min), or mega volume for full density at $150 (1h 40min). Mega volume refill from $100.">Textura wispy con puntas definidas por $140 (1h 35min), o mega volumen para densidad total por $150 (1h 40min). Refill de mega volumen desde $100.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$140+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 35min+</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas y piel" data-en="Brows &amp; skin">Cejas y piel</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cejas &amp; Faciales" data-en="Brows &amp; Facials">Cejas &amp; Faciales</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Laminado de cejas $90, henna $40, cera de cejas $25, limpieza facial $120 (1h 30min) y depilación facial $50." data-en="Brow lamination $90, henna $40, brow wax $25, facial cleansing $120 (1h 30min) and facial waxing $50.">Laminado de cejas $90, henna $40, cera de cejas $25, limpieza facial $120 (1h 30min) y depilación facial $50.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$25+</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">25min+</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Reservar</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_services + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="18 servicios en el menú, más entrenamiento profesional. Lista completa y disponibilidad en Booksy." data-en="18 services on the menu, plus professional training. Full list and availability on Booksy.">18 servicios en el menú, más entrenamiento profesional. Lista completa y disponibilidad en Booksy.</span></p>')

# ---------- GALERIA: grid completo reemplazado (solo 3 fotos reales de alta resolucion sin repetir) ----------
gallery_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', re.S)
mg = gallery_re.search(h)
assert mg, 'grid galeria no encontrado'
new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Después de la cita" data-en="After the appointment">Después de la cita</span><img src="assets/raw/bk-9.jpg" alt="Retrato de clienta tras su cita de pestañas en Viviana Tales Lash Studio" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Cejas y pestañas" data-en="Brows &amp; lashes">Cejas y pestañas</span><img src="assets/raw/bk-5.jpg" alt="Closeup de cejas y pestañas, clienta mirando hacia arriba" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Momento spa" data-en="Spa moment">Momento spa</span><img src="assets/raw/bk-3.jpg" alt="Momento spa relajante en Viviana Tales Lash Studio" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:mg.start()] + new_gallery + h[mg.end():]

rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Miradas</span> <span class="text-shine" data-es="reales" data-en="lashes">reales</span></h2>')

open('output/vivianatales/index.html', 'w').write(h)
print('servicios + galeria OK')
