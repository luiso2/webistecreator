import sys

slug = sys.argv[1]
path = f'output/{slug}/index.html'
# encoding explicito: en la forja cloud el locale puede no ser UTF-8 y los acentos/enes
# del site se corromperian al reescribir el archivo.
h = open(path, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:160]
    h = h.replace(a, b, n)

OLD = """    // Reveals
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal, .img-reveal').forEach(el => io.observe(el));"""

NEW = """    // Reveals
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    const revealEls = document.querySelectorAll('.reveal, .img-reveal');
    revealEls.forEach(el => io.observe(el));
    // Fallback: algunos navegadores calculan intersectionRatio 0 para elementos con clip-path
    // en su estado inicial (bug real de IntersectionObserver + clip-path en Chromium), dejando
    // hero/galeria con clip-path al 100% para siempre. Revision manual por getBoundingClientRect.
    const checkVisibleFallback = () => {
      revealEls.forEach(el => {
        if (el.classList.contains('in')) return;
        const r = el.getBoundingClientRect();
        if (r.top < window.innerHeight * 0.94 && r.bottom > 0) { el.classList.add('in'); io.unobserve(el); }
      });
    };
    window.addEventListener('scroll', checkVisibleFallback, { passive: true });
    window.addEventListener('load', checkVisibleFallback);
    checkVisibleFallback();
    setTimeout(checkVisibleFallback, 400);"""

rep(OLD, NEW)
open(path, 'w', encoding='utf-8').write(h)
print(f'{slug}: fallback de reveal aplicado')
