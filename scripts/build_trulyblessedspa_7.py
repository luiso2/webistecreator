import re

h = open('output/trulyblessedspa/index.html').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

# ---------- FIX: .img-reveal a veces nunca recibe .in ----------
# El propio elemento .img-reveal tiene clip-path inset(0 0 100% 0) (altura visible 0),
# y en algunos motores el IntersectionObserver calcula la interseccion sobre el rect YA
# recortado por el clip-path del propio target, asi que nunca cruza el threshold y la
# imagen queda oculta para siempre. Fallback robusto por geometria (idempotente con la IO
# existente, no la reemplaza) solo para .img-reveal.
anchor = "document.querySelectorAll('.reveal, .img-reveal').forEach(el => io.observe(el));"
assert anchor in h
fallback = anchor + """

    // Fallback geometrico para .img-reveal (ver nota arriba): asegura que las imagenes
    // con clip-path propio se revelen aunque el IntersectionObserver no dispare sobre ellas.
    if (!reducedMotion) {
      const imgRevealEls = Array.from(document.querySelectorAll('.img-reveal'));
      const checkImgReveal = () => {
        const vh = window.innerHeight;
        for (let i = imgRevealEls.length - 1; i >= 0; i--) {
          const el = imgRevealEls[i];
          const r = el.getBoundingClientRect();
          if (r.top < vh * 0.94 && r.bottom > 0) {
            el.classList.add('in');
            imgRevealEls.splice(i, 1);
          }
        }
        if (!imgRevealEls.length) window.removeEventListener('scroll', onImgRevealScroll);
      };
      let imgTicking = false;
      const onImgRevealScroll = () => {
        if (!imgTicking) { imgTicking = true; requestAnimationFrame(() => { imgTicking = false; checkImgReveal(); }); }
      };
      window.addEventListener('scroll', onImgRevealScroll, { passive: true });
      window.addEventListener('resize', onImgRevealScroll, { passive: true });
      checkImgReveal();
    } else {
      document.querySelectorAll('.img-reveal').forEach(el => el.classList.add('in'));
    }"""
h = h.replace(anchor, fallback, 1)

open('output/trulyblessedspa/index.html', 'w').write(h)
print('img-reveal fallback OK')
