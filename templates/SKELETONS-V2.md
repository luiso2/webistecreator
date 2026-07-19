# Esqueletos v2: derivacion por transformacion anclada (el metodo probado)

> Este es el metodo con el que se construyeron los batches manuales 1-3 (masielsugey, lashbloom,
> wandafulnails, pureartistry, paintboxnails, adryansbarber, laperlabarber, taywayhair, yulinails).
> Un site NUEVO nunca se escribe desde cero: se DERIVA de un esqueleto congelado con un script Python.

## Esqueletos congelados
- `templates/light-v2/index.html`: light, EN default (copia exacta de lashbloom: lash studio, plum-pink `#a04a72`/`#c47a9c`, Booksy 519855, "Lash Bloom", "Yesi", West Palm Beach). 830 lineas.
- `templates/dark-v2/index.html`: dark, EN default (copia exacta de pureartistry: hair studio, gold `#d4a84b`/`#b8934a`, Booksy 121705, "Pure Artistry", Orlando). 830 lineas.

Ambos traen completo el motion v2+v3 (preloader, scroll-progress, parallax, reveals, contadores,
marquee x2, split-word, sec-num, tile-cap, cursor-ring, foot-mark, heroInner, tilt, magnetic,
cursor-glow, back-top), bilingue data-es/data-en, JSON-LD, merktop-badge y book-float.

## Receta de derivacion (script Python, un solo archivo, correr con heredoc)

```python
import re, os, json
h = open('output/<slug>/index.html').read()   # copia previa del esqueleto
def rep(a, b, n=1):
    global h
    assert a in h, 'NO: ' + a[:80]   # el assert detecta anclas rotas ANTES de escribir
    h = h.replace(a, b, n)
```

Orden de operaciones (respetarlo evita el 90% de los errores):
1. **Proteger el badge Merktop** (solo si vas a cambiar paleta dorada o rgba(212,168,75)):
   `m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)` ->
   sustituir por token `@@BADGE@@`, hacer la paleta, restaurar. El badge SIEMPRE queda dorado.
2. **Paleta**: lista de pares `(hex_viejo, hex_nuevo)` con `h.replace(a, b)` global. Cubrir TODOS
   los tonos del esqueleto (accent deep/mid, bg, bg-2, ink, rgbas de accent e ink, shimmer x3,
   orbs x3, btn-3d x4 + sombras, dark-band x8, scroll-progress, tile-cap, book-float, CTA/footer bgs).
   Paletas ya usadas (no repetir en la misma ciudad+nicho): coral fairy `#c04e62`, caramelo `#a86a2e`,
   esmeralda `#2f7d5a`, teal acero `#4fb8b8`, violeta dark `#b18ae8`, rosa dark, gold dark (original).
3. **Globales**: URL de Booksy (replace all), URL de IG, @handle, imagen de logo/avatar.
4. **Head**: title, meta description, og:title/description/image, JSON-LD completo (regex sobre
   `<script type="application/ld\+json">.*?</script>` con DOTALL, tipo schema correcto:
   Barbershop/NailSalon/HairSalon/BeautySalon, telephone si existe).
5. **Idioma**: si el negocio es ES: `<html lang="es"` y
   `applyLang(lang === 'es' ? 'es' : 'en')` -> `applyLang(lang === 'en' ? 'en' : 'es')`.
   El texto visible de los elementos NUEVOS se escribe igual al data del idioma principal.
6. **Secciones con anclas literales** (preloader, nav, hero, strip, marquee, experiencia, metodo,
   opiniones, ubicacion, CTA, footer): rep() con el string EXACTO del esqueleto (el texto visible
   de los esqueletos = valor data-en). Los 4 marquee-word de cada palabra se cambian con
   `assert h.count(old) == 4` + replace global.
7. **Secciones que se reemplazan enteras por regex** (no intentar reps parciales):
   - Grid de servicios: `r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)'`
   - Nota de servicios: `r'(<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">).*?(</p>)'`
   - Grid de galeria: `r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>'`
   Las 4 cards: card 2 es la destacada (border-color accent 0.4 + btn-3d; las otras btn-ghost).
   La galeria: 1 tile ancho 16/9 + 5 tiles 3/4 con tile-cap bilingue y alt reales.
8. **Imagenes**: cambiar los <img> por su TAG COMPLETO (src + alt) para no romper el alt. Orden:
   primero experiencia, luego hero, al final el replace global del logo (evita colisiones cuando
   el logo nuevo reutiliza un numero bk-N que el esqueleto usaba en otra seccion).
9. Escribir el archivo y correr `python3 scripts/gate.py <slug> --lang <es|en> --forbid "<leftovers>"`.
   En --forbid poner SIEMPRE: nombre del negocio del esqueleto, artista, ciudad, calle, id de Booksy
   viejo y 2-3 palabras del nicho anterior (p.ej. "Lash Bloom,Yesi,West Palm,Cresthaven,519855,lash").

## Gotchas que ya costaron iteraciones (no repetir)
- Script que falla en un assert aborta ANTES de escribir: se corrige el ancla y se rele el script COMPLETO.
- Heredoc `<<'PYEOF'`: para texto con apostrofes usar strings Python con comillas dobles.
- Un rep() con n=2 temprano hace fallar un rep() posterior del mismo string.
- Las clases del div de botones del hero son iguales a otros divs: NUNCA anclar regex en clases
  genericas; usar literales unicos con assert.
- Cambiar contadores data-count en STRIP y en EXPERIENCIA (hay dos juegos; el de experiencia
  quedo una vez en 4.8 heredado: bug real).
- Booksy renombra negocios: la URL vieja redirige al listado y el fetch trae OTROS negocios.
  Verificar que el nombre extraido coincida antes de usar datos.
