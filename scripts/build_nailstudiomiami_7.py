import re

h = open('output/nailstudiomiami/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# Corregir alt texts de experiencia (contenido real verificado en el sheet: bk-4 = negro marmoleado
# sobre el volante, bk-7 = negro con acento naranja, NO "nude"/"marmol blanco y negro" como se puso antes)
rep('<img src="assets/raw/bk-4.jpg" alt="Nude gel manicure resting on a car steering wheel" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-4.jpg" alt="Black marbled gel manicure resting on a car steering wheel" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-7.jpg" alt="Black and white marble nail art at The Nail Studio Miami" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-7.jpg" alt="Black gel manicure with a bold orange accent nail at The Nail Studio Miami" class="blur-up w-full h-full object-cover" loading="lazy" />')

# Reconstruir la galeria: los 4 tiles bk-16/bk-9/bk-14/bk-10 son thumbnails de 100x100px
# (thumbnails de Booksy, no fotos de portafolio) -> se descartan por calidad. Solo quedan
# bk-6 (wide, ya correcto), bk-5 y bk-8 como fotos reales de alta resolucion sin usar aun.
gallery_re = re.compile(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>', re.S)
mg = gallery_re.search(h)
assert mg, 'grid galeria no encontrado'
new_gallery = '''<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div class="frame zoomable col-span-2 aspect-[16/9] img-reveal"><span class="tile-cap" data-es="Set nuevo, clienta feliz" data-en="Fresh set, happy client">Fresh set, happy client</span><img src="assets/raw/bk-6.jpg" alt="Pink ombre gel manicure with a gold ring at The Nail Studio Miami" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:90ms"><span class="tile-cap" data-es="Sobre ruedas" data-en="On the go">On the go</span><img src="assets/raw/bk-5.jpg" alt="Blue gel manicure resting on a car dashboard" class="blur-up w-full h-full object-cover" /></div>
        <div class="frame zoomable aspect-[3/4] img-reveal" style="transition-delay:150ms"><span class="tile-cap" data-es="Uñas con carácter" data-en="Statement nails">Statement nails</span><img src="assets/raw/bk-8.jpg" alt="Black gel manicure with a yellow to orange gradient accent nail" class="blur-up w-full h-full object-cover" loading="lazy" /></div>
      </div>
    </div>
  </section>'''
h = h[:mg.start()] + new_gallery + h[mg.end():]

open('output/nailstudiomiami/index.html', 'w').write(h)
print('galeria corregida (solo fotos de alta resolucion), alts de experiencia corregidos')
