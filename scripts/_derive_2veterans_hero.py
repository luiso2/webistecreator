import re
SLUG = 'output/2-veterans-handyman-service/index.html'
h = open(SLUG, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    cnt = h.count(a)
    assert cnt == n, f'NO (found {cnt}, need {n}): {a[:140]!r}'
    h = h.replace(a, b, n)

PHONE_TEL = '+17542667735'
PHONE_DISPLAY = '(754) 266-7735'
GREV_URL = 'https://www.google.com/search?q=2+Veterans+Handyman+Service+Cape+Coral+FL+reviews'

old_hero = '''      <div class="lg:col-span-7">
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="https://www.instagram.com/pure.artistrysk/" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            @pure.artistrysk
          </a>
        </div>
        <div class="reveal hero-proof mt-5" style="transition-delay:420ms" aria-label="Lo que encontrará el cliente">
          <span data-es="Fotos reales" data-en="Real work">Fotos reales</span>
          <span data-es="Servicios claros" data-en="Clear services">Servicios claros</span>
          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>
          </div>
        </div>
      </div>'''

new_hero = f'''      <div class="lg:col-span-7">
        <p class="reveal text-xs sm:text-sm tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-6" data-es="Cape Coral, FL · Handyman" data-en="Cape Coral, FL · Handyman">Cape Coral, FL · Handyman</p>
        <p class="reveal font-script text-xl sm:text-2xl text-[color:var(--ink-60)] mb-4" style="transition-delay:80ms" data-es="Veteranos cuidando tu casa." data-en="Veterans looking after your home.">Veterans looking after your home.</p>
        <h1 class="split font-display text-5xl sm:text-6xl lg:text-7xl leading-[1.05] mb-7">
          <span data-es="Drywall, remodelacion" data-en="Drywall, remodeling">Drywall, remodeling</span><br /><span data-es="y reparaciones del hogar, " data-en="and home repairs, ">and home repairs, </span><span class="text-shine" data-es="hecho bien" data-en="done right">done right</span>
        </h1>
        <p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es="Reparacion e instalacion de drywall, remodelacion de cocinas y banos, montaje de TV, ventiladores, luces y reparaciones generales en Cape Coral. Negocio veterano, licenciado y asegurado, con 4.7 estrellas en 55 resenas de Google." data-en="Drywall repair and installation, kitchen and bathroom remodeling, TV mounts, ceiling fans, light fixtures and general repairs across Cape Coral. Veteran-owned, licensed and insured, with a 4.7 rating across 55 Google reviews.">Drywall repair and installation, kitchen and bathroom remodeling, TV mounts, ceiling fans, light fixtures and general repairs across Cape Coral. Veteran-owned, licensed and insured, with a 4.7 rating across 55 Google reviews.</p>
        <div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="4.7 · 55 resenas en Google" data-en="4.7 · 55 reviews on Google">4.7 · 55 reviews on Google</span>
        </div>
        <div class="reveal flex flex-wrap gap-4" style="transition-delay:360ms">
          <a href="tel:{PHONE_TEL}" class="btn-3d rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <span data-es="Llama al (754) 266-7735" data-en="Call (754) 266-7735">Call (754) 266-7735</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
          <a href="{GREV_URL}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-8 py-4 text-sm inline-flex items-center gap-2">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            Google Reviews
          </a>
        </div>
        <div class="reveal hero-proof mt-5" style="transition-delay:420ms" aria-label="Lo que encontrará el cliente">
          <span data-es="Veterano, licenciado" data-en="Veteran-owned, licensed">Veteran-owned, licensed</span>
          <span data-es="Cotizaciones gratis" data-en="Free estimates">Free estimates</span>
          <span data-es="Contacto directo" data-en="Direct contact">Contacto directo</span>
        </div>
      </div>
      <div class="lg:col-span-5 reveal" style="transition-delay:280ms">
        <div class="relative max-w-sm lg:max-w-md mx-auto lg:ml-auto" data-parallax="0.06">
          <div class="frame zoomable img-reveal aspect-[3/4]" style="transition-delay:240ms">
            <img src="assets/hero-chandelier-install.jpg" alt="Finished light fixture installation by 2 Veterans Handyman Service in a Cape Coral home" class="blur-up w-full h-full object-cover" />
          </div>
          <div class="glass rounded-2xl px-5 py-4 absolute -bottom-6 -left-4 sm:-left-10">
            <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Disponible" data-en="Available">Available</p>
            <p class="font-display text-lg">24/7</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Llamadas de emergencia" data-en="Emergency calls">Emergency calls</p>
          </div>
        </div>
      </div>'''
rep(old_hero, new_hero)

open(SLUG, 'w', encoding='utf-8').write(h)
print('HERO OK, length', len(h))
