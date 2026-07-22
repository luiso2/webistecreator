import re

h = open('output/trulyblessedspa/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- GALERIA: grid completo reemplazado ----------
gallery_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', re.S)
mg = gallery_re.search(h)
assert mg, 'grid galeria no encontrado'
new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Cavitación &amp; Masaje Linfático" data-en="Cavitation &amp; Lymphatic Massage">Cavitation &amp; Lymphatic Massage</span><img src="assets/raw/bk-16.jpg" alt="Cavitation with RF and lymphatic massage treatment at Truly Blessed Spa &amp; Boutique" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Ombré con acentos dorados" data-en="Ombré with gold accents">Ombré with gold accents</span><img src="assets/raw/bk-14.jpg" alt="Ombre nail set with gold foil accents at Truly Blessed Spa &amp; Boutique" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Diseño de estrellas a mano" data-en="Hand-painted star art">Hand-painted star art</span><img src="assets/raw/bk-13.jpg" alt="Red, white and blue hand-painted star nail art" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:120ms"><span class="tile-cap" data-es="Trenzas de caja" data-en="Box braids">Box braids</span><img src="assets/raw/bk-7.jpg" alt="Finished box braids at Truly Blessed Spa &amp; Boutique" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:210ms"><span class="tile-cap" data-es="Ombré blanco clásico" data-en="Classic white ombré">Classic white ombré</span><img src="assets/raw/bk-6.jpg" alt="White ombre stiletto nail set" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
        <div class="frame zoomable aspect-[3/4] lg:mt-10 img-reveal" style="transition-delay:300ms"><span class="tile-cap" data-es="Contorno corporal" data-en="Body contouring">Body contouring</span><img src="assets/raw/bk-3.jpg" alt="Radiofrequency cavitation body contouring session at Truly Blessed Spa &amp; Boutique" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:mg.start()] + new_gallery + h[mg.end():]

rep('<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span></h2>',
    '<p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Galería" data-en="Gallery">Galería</p>\n          <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Resultados" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="results">results</span></h2>')

open('output/trulyblessedspa/index.html', 'w').write(h)
print('galeria OK')
