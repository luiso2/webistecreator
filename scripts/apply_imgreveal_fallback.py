#!/usr/bin/env python3
"""Inyecta el fallback de reveal en los ESQUELETOS (y en los sites que se le pasen).

Uso: python3 scripts/apply_imgreveal_fallback.py <ruta.html> [<ruta.html> ...]
     python3 scripts/apply_imgreveal_fallback.py --templates      (los 4 esqueletos)

EL BUG (medido 2026-07-29 en Chromium headless, site prestigeautocargo):
`.img-reveal` arranca con `clip-path: inset(0 0 100% 0)`, o sea con la caja pintada a
altura cero. El motor calcula intersectionRatio 0 para ese estado, asi que el
IntersectionObserver que debia ponerle la clase `in` NO dispara nunca: para revelarse
tendria que estar ya revelado. Resultado: hero, experiencia y galeria en blanco.
Evidencia del site sin parchear: `.reveal` (sin clip-path) 49/50 con clase `in`,
`.img-reveal` 0/10.

`scripts/fix_imgreveal_bug.py` ya arreglaba esto site por site, pero el parche nunca se
llevo a los esqueletos: por eso cada site nuevo nacia con el bug otra vez. Este script
lo aplica en la RAIZ. Es idempotente: si el fallback ya esta, no toca el archivo.
"""
import sys

TEMPLATES = ['templates/dark-v2/index.html', 'templates/light-v2/index.html',
             'templates/dark/index.html', 'templates/light/index.html']

VIEJO = """    document.querySelectorAll('.reveal, .img-reveal').forEach(el => io.observe(el));"""

NUEVO = """    const revealEls = document.querySelectorAll('.reveal, .img-reveal');
    revealEls.forEach(el => io.observe(el));
    // Fallback obligatorio: un elemento con clip-path que lo recorta al 100% tiene caja
    // pintada de altura 0, y varios motores le calculan intersectionRatio 0. El observer
    // de arriba entonces NUNCA lo revela (medido: .reveal 49/50 in, .img-reveal 0/10) y
    // el hero y la galeria se quedan en blanco. getBoundingClientRect mide la caja de
    // layout, que si existe, asi que rompe el circulo.
    const checkVisibleFallback = () => {
      revealEls.forEach(el => {
        if (el.classList.contains('in')) return;
        const r = el.getBoundingClientRect();
        if (r.top < window.innerHeight * 0.94 && r.bottom > 0) { el.classList.add('in'); io.unobserve(el); }
      });
    };
    window.addEventListener('scroll', checkVisibleFallback, { passive: true });
    window.addEventListener('resize', checkVisibleFallback, { passive: true });
    window.addEventListener('load', checkVisibleFallback);
    checkVisibleFallback();
    setTimeout(checkVisibleFallback, 400);"""


def parchear(ruta):
    h = open(ruta, encoding='utf-8').read()
    if 'checkVisibleFallback' in h:
        print(f'  ya parcheado: {ruta}')
        return False
    if VIEJO not in h:
        print(f'  ANCLA NO ENCONTRADA (revisar a mano): {ruta}')
        return False
    open(ruta, 'w', encoding='utf-8').write(h.replace(VIEJO, NUEVO, 1))
    print(f'  parcheado: {ruta}')
    return True


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    rutas = TEMPLATES if args[0] == '--templates' else args
    n = sum(parchear(r) for r in rutas)
    print(f'{n} archivo(s) modificado(s) de {len(rutas)}')


if __name__ == '__main__':
    main()
