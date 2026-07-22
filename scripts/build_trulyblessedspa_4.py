import re

h = open('output/trulyblessedspa/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

BOOKSY = 'https://booksy.com/en-us/1780520_truly-blessed-spa-boutique-llc_wellness-day-spa_15746_brandon'

# ---------- SERVICIOS: destacados (4 cards) ----------
services_re = re.compile(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)', re.S)
m = services_re.search(h)
assert m, 'grid servicios no encontrado'
new_highlights = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Uñas" data-en="Nails">Nails</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Ombré</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Degradado de color hecho a mano, del favorito del estudio. Full set regular también disponible por $57." data-en="Hand-blended color fade, the studio favorite. A regular full set is also available for $57.">Hand-blended color fade, the studio favorite. A regular full set is also available for $57.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$71</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="precio" data-en="price">price</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(139,74,160,0.4); box-shadow: 0 18px 50px rgba(45,34,51,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Insignia del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Cavitación &amp; Masaje" data-en="Cavitation &amp; Massage">Cavitation &amp; Massage</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Cavitación con radiofrecuencia y masaje linfático, el servicio del que más hablan las reseñas de Janaira." data-en="Cavitation with RF and lymphatic massage, the service Janaira's reviews mention the most.">Cavitation with RF and lymphatic massage, the service Janaira's reviews mention the most.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$19</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="precio" data-en="price">price</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pies" data-en="Feet">Feet</p>
          <h3 class="font-display text-2xl leading-snug mb-3">Ultimate Pedicure</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="El nivel más completo de pedicura. También disponible Basic $34 y Deluxe $43." data-en="The most complete pedicure tier. Basic $34 and Deluxe $43 are also available.">The most complete pedicure tier. Basic $34 and Deluxe $43 are also available.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$51</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide" data-es="precio" data-en="price">price</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Piel" data-en="Skin">Skin</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Skin Treatment Facial" data-en="Skin Treatment Facial">Skin Treatment Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Facial dirigido a piel con necesidades específicas, de 1 hora. Express Facial también disponible por $51." data-en="A one-hour facial targeted at specific skin needs. An Express Facial is also available for $51.">A one-hour facial targeted at specific skin needs. An Express Facial is also available for $51.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$100</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOKSY}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:m.start()] + new_highlights + h[m.end():]

rep('<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>',
    '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="39+ servicios en el menú. Precios y disponibilidad en Booksy." data-en="39+ services on the menu. Prices and availability on Booksy.">39+ services on the menu. Prices and availability on Booksy.</span></p>')

rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios publicados por Truly Blessed Spa &amp; Boutique en Booksy. Reserva con confirmación inmediata." data-en="Prices as published by Truly Blessed Spa &amp; Boutique on Booksy. Booking confirms instantly.">Prices as published by Truly Blessed Spa &amp; Boutique on Booksy. Booking confirms instantly.</p>')

rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="ritual" data-en="ritual">ritual</span>')

# ---------- SERVICIOS: menu completo agrupado por categoria (insertado tras los destacados) ----------
def row(name, price, dur=None):
    d = f' <span class="text-[10px] text-[color:var(--ink-40)]">· {dur}</span>' if dur else ''
    return f'<div class="flex items-baseline justify-between gap-4 border-b border-[color:var(--accent-ghost)] pb-3"><span class="text-[color:var(--ink-60)] font-light">{name}</span><span class="font-display whitespace-nowrap">${price}{d}</span></div>'

def last_row(name, price, dur=None):
    d = f' <span class="text-[10px] text-[color:var(--ink-40)]">· {dur}</span>' if dur else ''
    return f'<div class="flex items-baseline justify-between gap-4"><span class="text-[color:var(--ink-60)] font-light">{name}</span><span class="font-display whitespace-nowrap">${price}{d}</span></div>'

gel_builder = [
    ('Gel X Fill In', 38, None), ('Gel X Fullset Short', 47, '2h 10min'), ('Gel X Fullset Medium', 55, None),
    ('Gel X Fullset Long', 64, '2h 15min'), ('Poly Gel Fill In', 45, '2h'), ('PolyGel Full Set', 65, '2h'),
    ('Builder Fill In', 38, None), ('Builder Gel Fullset Short', 51, None), ('Builder Gel Fullset Medium', 60, '2h 10min'),
    ('Builder Gel Fullset Long', 68, '2h 20min'), ('Acrylic Fill In', 45, '2h'),
]
mani_extras = [
    ('Ombré', 71, None), ('Full set', 57, None), ('Reg Manicure', 26, '35min'), ('Gel Manicure', 38, None),
    ('Polish change (Gel)', 30, None), ('Polish change (Regular)', 20, '45min'), ('Soak Off', 25, '40min'),
    ('Kids Gel Manicure', 19, None), ('Kids Regular Manicure', 14, '30min'),
]
pedicures = [
    ('Basic Pedicure', 34, None), ('Deluxe Pedicure', 43, None), ('Ultimate Pedicure', 51, None), ('Kids Pedicure', 24, '40min'),
]
waxing = [
    ('Eyebrow Wax', 13, '30min'), ('Lip Wax', 6, '10min'), ('Chin Wax', 6, '10min'), ('Under Arm Wax', 17, '30min'),
    ('Arm Wax', 26, '35min'), ('Leg Wax', 34, None), ('Brazilian Wax', 55, None), ('Full Body Wax', 115, '1h 35min'),
]
facials_body = [
    ('Hydrating Facial', 72, '1h'), ('Express Facial', 51, None), ('Skin Treatment Facial', 100, '1h'),
    ('Extractions', 21, '30min'), ('Cavitation W/ RF &amp; Lymphatic Massage', 19, None),
]
braids = [
    ('Perimeter Redo (LG Braids)', 75, None), ('Micro Braids', 250, '10h'),
]

def category_card(title_es, title_en, items, delay=None):
    rows = ''.join(row(n, p, d) for n, p, d in items[:-1]) + last_row(*items[-1])
    style = f' style="transition-delay:{delay}ms"' if delay else ''
    count_es = f'{len(items)} servicios'
    count_en = f'{len(items)} services'
    return f'''<div class="glass rounded-3xl p-7 reveal"{style}>
          <h4 class="font-display text-xl mb-1" data-es="{title_es}" data-en="{title_en}">{title_en}</h4>
          <p class="text-[11px] uppercase tracking-wide text-[color:var(--ink-40)] mb-5" data-es="{count_es}" data-en="{count_en}">{count_en}</p>
          <div class="space-y-3 text-sm">
            {rows}
          </div>
        </div>'''

full_menu = f'''
      <div class="mb-10">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-2" data-es="Menú completo" data-en="Full menu">Full menu</p>
        <h3 class="reveal font-display text-2xl sm:text-3xl" data-es="El menú completo, precios claros" data-en="The full menu, transparent prices">The full menu, transparent prices</h3>
      </div>
      <div class="grid sm:grid-cols-2 gap-5">
        {category_card('Gel-X &amp; Builder Gel', 'Gel-X &amp; Builder Gel', gel_builder)}
        {category_card('Manicura, Ombré &amp; Esmaltado', 'Manicure, Ombré &amp; Polish', mani_extras, 80)}
        {category_card('Pedicura', 'Pedicure', pedicures, 120)}
        {category_card('Depilación con cera', 'Waxing', waxing, 160)}
        {category_card('Faciales &amp; Contorno Corporal', 'Facials &amp; Body Contouring', facials_body, 200)}
        {category_card('Trenzas', 'Braids', braids, 240)}
      </div>
      <p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-10" data-es="Precios publicados por Truly Blessed Spa &amp; Boutique en Booksy al momento de la consulta. Reserva online con confirmación inmediata." data-en="Prices as published by Truly Blessed Spa &amp; Boutique on Booksy at time of writing. Book online with instant confirmation.">Prices as published by Truly Blessed Spa &amp; Boutique on Booksy at time of writing. Book online with instant confirmation.</p>
    </div>
  </section>'''

anchor = '</div>\n  </section>\n\n  <!-- GALERIA -->'
assert anchor in h, 'anchor cierre servicios no encontrado'
h = h.replace(anchor, full_menu + '\n\n  <!-- GALERIA -->', 1)

open('output/trulyblessedspa/index.html', 'w').write(h)
print('servicios (destacados + menu completo) OK')
