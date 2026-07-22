import re

h = open('output/iloveawaxingmiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/1037088_i-love-waxing-miami_hair-removal_15889_miami'

# ---------- SERVICIOS: 4 cards destacadas ----------
services_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', re.S)
m = services_re.search(h)
assert m, 'grid servicios no encontrado'
new_services = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cejas y rostro" data-en="Brows &amp; face">Brows &amp; face</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Eyebrow Waxing &amp; Tinting</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cejas definidas con cera y tinte en la misma cita. Rostro completo desde $40, o cejas solas por $20." data-en="Defined brows with wax and tint in the same visit. Full face from $40, or eyebrows alone for $20.">Defined brows with wax and tint in the same visit. Full face from $40, or eyebrows alone for $20.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$40</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30 min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(160,74,92,0.4); box-shadow: 0 18px 50px rgba(51,34,40,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Diva Bikini</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El bikini brasileño de la casa, con la técnica de más de una década de Gisele. La opción esencial I Love Waxing Bikini está desde $45." data-en="The house Brazilian-style bikini, with over a decade of Gisele\'s technique behind it. The essential I Love Waxing Bikini starts at $45.">The house Brazilian-style bikini, with over a decade of Gisele\'s technique behind it. The essential I Love Waxing Bikini starts at $45.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$65</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Cera corporal" data-en="Body waxing">Body waxing</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Full Back</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cera de cuerpo completo, de espalda a piernas: full legs $45, full arms $30, underarms $15." data-en="Full body waxing, from back to legs: full legs $45, full arms $30, underarms $15.">Full body waxing, from back to legs: full legs $45, full arms $30, underarms $15.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$30</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">30 min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="El paquete completo" data-en="The full package">The full package</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Lovely Spa Day</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El paquete más completo del estudio: cera y cuidado de piel de principio a fin en una sola cita." data-en="The studio\'s most complete package: waxing and skin care from start to finish in a single visit.">The studio\'s most complete package: waxing and skin care from start to finish in a single visit.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$140</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h 30min</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_services + h[m.end():]

rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios y duraciones publicados por I Love Waxing Miami en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by I Love Waxing Miami on Booksy. Booking confirms instantly.">Prices and durations as published by I Love Waxing Miami on Booksy. Booking confirms instantly.</p>')

# ---------- SERVICIOS: menu completo agrupado por categoria (31 servicios, >20: no colapsable) ----------
def cat_block(title_en, title_es, rows):
    rows_html = ''
    for name, price, dur in rows:
        dur_html = f'<p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-0.5">{dur}</p>' if dur else ''
        rows_html += f'''<div class="flex items-center justify-between gap-4 border-b border-[color:var(--accent-ghost)] pb-3 last:border-b-0 last:pb-0">
              <div><p class="text-sm font-medium leading-snug">{name}</p>{dur_html}</div>
              <p class="font-display text-lg text-shine shrink-0">${price}</p>
            </div>'''
    return f'''<div class="glass rounded-3xl p-7 sm:p-8 reveal">
          <h3 class="font-display text-xl mb-5 text-[color:var(--accent-deep)]"><span data-es="{title_es}" data-en="{title_en}">{title_en}</span></h3>
          <div class="space-y-3">
            {rows_html}
          </div>
        </div>'''

brows_face = [
    ('Eyebrows', 20, None),
    ('Eyebrow Waxing &amp; Tinting', 40, '30 min'),
    ('Full Face', 40, '30 min'),
    ('Full Face And Eyebrow', 55, None),
    ('Brow Lamination', 90, '1h'),
    ('Lash Lift &amp; Tint', 55, None),
    ('Nose Wax', 4, '5 min'),
    ('Cheeks', 10, '10 min'),
    ('Upper Lip', 7, None),
    ('Side Burns', 7, None),
    ('Chin', 5, '10 min'),
]
body = [
    ('Full Arms', 30, '30 min'),
    ('Half Arms', 20, None),
    ('Full Legs', 45, None),
    ('Upper Legs', 30, '30 min'),
    ('Lower Legs', 25, '30 min'),
    ('Underarms', 15, None),
    ('Stomach', 25, '30 min'),
    ('Stomach Strip', 7, None),
    ('Bust', 15, None),
    ('Neck', 10, '10 min'),
    ('Lower Back', 15, None),
    ('Full Back', 30, '30 min'),
]
bikini = [
    ('I Love Waxing Bikini', 45, None),
    ('Diva Bikini', 65, '1h'),
    ('Lovely Smooth Vajacial', 85, '1h'),
]
packages = [
    ('Texas Girl', 55, None),
    ('California Girl', 80, '1h'),
    ('New York Girl', 60, '1h'),
    ('Miami Girl', 100, '1h'),
    ('Lovely Spa Day', 140, '1h 30min'),
    ('I&#129505; My Sking Facial', 90, '1h'),
]

full_menu = '<div class="grid md:grid-cols-2 gap-6">\n        '
full_menu += cat_block('Brows &amp; Face', 'Cejas y Rostro', brows_face) + '\n        '
full_menu += cat_block('Body Waxing', 'Cera Corporal', body) + '\n        '
full_menu += cat_block('Bikini &amp; Brazilian', 'Bikini y Brasileña', bikini) + '\n        '
full_menu += cat_block('Signature Packages &amp; Spa', 'Paquetes y Spa', packages) + '\n      </div>'

label_block = '''<div class="reveal mb-10 mt-14 text-center" style="transition-delay:60ms">
        <p class="text-xs tracking-[0.3em] uppercase text-[color:var(--ink-40)]" data-es="Menú completo, agrupado por categoría" data-en="Full menu, grouped by category">Full menu, grouped by category</p>
      </div>
      '''

old_note = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>'
new_note = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-10"><span data-es="111 reseñas de 5 estrellas en Booksy. Disponibilidad y extras al reservar." data-en="111 five-star reviews on Booksy. Availability and add-ons shown at booking.">111 five-star reviews on Booksy. Availability and add-ons shown at booking.</span></p>'
assert old_note in h, 'nota de cierre no encontrada'
h = h.replace(old_note, label_block + full_menu + '\n      ' + new_note, 1)

open('output/iloveawaxingmiami/index.html', 'w').write(h)
print('servicios (destacados + menu completo) OK')
