# Design System Compartido: Siteforge (plantilla universal premium)

## Nivel $100k: sistema de motion obligatorio (v2, 2026-07-16)
Todo site debe sentirse como un website de seis cifras. Los ejemplares (`templates/dark`, `templates/light`) ya integran este paquete de motion; los builds lo HEREDAN al copiar el ejemplar. Todo en CSS + JS vanilla self-contained (sin librerias externas), con IntersectionObserver + requestAnimationFrame, y TODO desactivado bajo `prefers-reduced-motion` y en dispositivos touch donde aplique:
1. **Preloader de marca** (max 1.2s): monograma/wordmark con reveal, fade-out al cargar.
2. **Barra de progreso de scroll** (2px, gradiente del accent, top fijo).
3. **Parallax en capas del hero**: orbs e imagen a velocidades distintas (factores 0.06-0.2, rAF).
4. **Reveals editoriales**: texto con fadeInUp escalonado; imagenes con clip-path reveal (inset) + escala 1.06 a 1.
5. **Contadores animados** en el strip de confianza (rating, reseñas, duracion) al entrar en viewport.
6. **Marquee infinito** entre secciones: palabras clave del negocio en Playfair italic separadas por ✦, lento, pausa on hover.
7. **Testimonios en carrusel** con drag/swipe, autoplay suave y dots (no grid estatico).
8. **Botones magneticos**: el CTA principal sigue el cursor (max 6px, spring back). Solo desktop.
9. **Tilt 3D sutil en cards** de servicio (rotateX/Y max 3deg + glare). Solo desktop.
10. **Cursor glow** en secciones de banda oscura (radial que sigue el mouse). Solo desktop.
11. **Back-to-top** discreto tras 2 viewports de scroll.
Performance: nada de listeners de scroll sin rAF; will-change solo donde anima; imagenes lazy salvo hero. La pagina debe seguir fluida en movil.


## Nivel $100k+: motion v3 (2026-07-19, en ambos ejemplares)
Los builds lo HEREDAN al copiar el template. Marcadores: `split-word`, `sec-num`, `tile-cap`, `cursor-ring`, `foot-mark`, `heroInner`.
1. **Split-text del hero**: el JS envuelve cada palabra del `h1.split` y suben en cascada (90ms de stagger). El h1 usa clase `split` (NO `reveal`).
2. **Numerales editoriales**: `<span class="sec-num">01</span>` como primer hijo de cada seccion principal (outline gigante, arriba-derecha).
3. **Galeria cinematografica**: el primer tile va `col-span-2 aspect-[16/9]`; TODOS los tiles llevan `<span class="tile-cap">Nombre del servicio</span>` (caption serif italic que sube al hover; visible fijo en touch).
4. **Cursor ring**: anillo que sigue el puntero con lerp (solo desktop), crece sobre links/botones. `<div id="cursorRing" class="cursor-ring">`.
5. **Watermark del footer**: `<span class="foot-mark">NombreMarca</span>` (outline gigante tras el footer; footer necesita `overflow-hidden`).
6. **Fade del hero al scroll**: `#heroInner` pierde opacidad y baja 46px durante el primer viewport (dentro del rAF de scroll existente).
Reglas: el bloque JS v3 vive a NIVEL RAIZ del script (nunca dentro de `if (finePointer)`, o el split muere en mobile); todo respeta prefers-reduced-motion; cero animaciones infinitas nuevas sobre imagenes.

## Historia: origen (Head Spa Demos Miami)

> Derivado del sistema visual de Ava Luxury Head Spa (`~/Desktop/ava-head-spa/index.html`), estilo aprobado en proyectos previos.
> Regla: MISMO estilo premium en los 5 sites; cambia SOLO la paleta de acento, las fotos reales, el menu de servicios, los reviews y los datos de contacto.

## Stack por site
- Un solo archivo `index.html` por negocio (self-contained salvo fuentes Google Fonts, Tailwind CDN y mapa embed).
- Tailwind CDN (`https://cdn.tailwindcss.com`) + bloque `<style>` propio con el sistema de abajo.
- Fuentes: `Playfair Display` (display/serif, titulares) + `Poppins` (cuerpo). Google Fonts.
- Iconos: SVG inline (estilo Lucide, stroke 1.5-2, sin dependencia externa).
- Idioma: espanol (mercado Hialeah/Flagami/Gables/North Miami). Nombres de servicios EXACTOS como los publica el negocio (aunque esten en ingles).
- Mobile-first. Breakpoints Tailwind estandar.

## Tokens (variables CSS, mismos NOMBRES en los 5; los VALORES siguen la marca real)
La base puede ser clara u oscura segun la marca del negocio (research `brand_vibe` manda). Estructura, componentes, motion y tipografia NO cambian.
```css
--bg: ...;            /* base de pagina (crema o charcoal segun marca) */
--surface: ...;       /* cards glass */
--ink: ...;           /* texto principal */
--accent-deep: ...;   /* botones 3D, titulares enfasis */
--accent-mid: ...;    /* hovers, subrayados, iconos */
--accent-soft: ...;   /* fondos alternos, orbs */
--accent-ghost: ...;  /* bordes glass 8-16% alpha */
```
Paletas POR NEGOCIO (derivadas del brand real encontrado en research, campo `brand_vibe` de cada data.json):
- **mizu** (BASE OSCURA): bg warm black #14110e, ink cream #f4ead8, deep champagne #eacda4, mid bronze #c2ab90, taupe #b2a293. Zen japones dark + gold.
- **amani** (base clara): bg cream #f5f0e8, ink espresso #32281f, deep mocha/gold-olive #8a6f4d, mid taupe #a8907a, soft #ece3d4. Quiet luxury calido.
- **mare** (base clara): bg sand/cream #f7f3ec, ink chocolate #33261d, deep teal #296167 (color oficial de su Mangomint), mid #4a8288, soft #dce9e8. Spa-lab europeo.
- **alea** (base clara): bg white/blush #faf4ef, ink #33261f, deep gold #c9a45c, mid #b28d55, acento noche azul-violeta #2b2f4a para secciones oscuras. Gold-on-white con halo.
- **pausa** (base clara): bg warm white #f8f6f1, ink #2e3228, deep sage #6f7f63, mid sage claro #a8b79b, soft #e9ede2, toque dorado suave. Botanico sereno.

## Componentes obligatorios (copiar el patron Ava, re-tintado con las variables)
1. `.glass-cream`: rgba(250,247,241,0.7) + blur(16px) saturate(150%) + borde accent-ghost.
2. `.text-shine`: gradiente animado shimmer 12s sobre titular clave (tonos del accent).
3. `.orb`: 2-3 orbs radiales blur(110px) animacion breathe 16s en hero y CTA final.
4. `.grain-paper::after`: SVG feTurbulence opacity 0.05 en secciones editoriales.
5. `.reveal` / `.reveal.in`: translateY(42px) + opacity, cubic-bezier(0.22,1,0.36,1) 1s, IntersectionObserver con stagger (delay por indice).
6. `img.blur-up`: blur(18px)->0 al load.
7. `.btn-3d` (CTA principal): gradiente vertical del accent-deep, box-shadow con "suela" (0 5px 0 tono mas oscuro), hover -2px, active +4px press.
8. `.merktop-badge`: pill oscura, dot dorado #D4A84B pulsante, texto "Powered by Merktop" -> https://merktop.com (obligatorio en footer).

## Estructura de secciones (identica en los 5)
1. **Nav** fija glass: monograma/nombre, links ancla (Experiencia, Servicios, Galeria, Opiniones, Ubicacion), CTA "Reservar" (btn-3d) -> canal real de reserva (GlossGenius/Square/Mangomint/tel/WhatsApp).
2. **Hero**: eyebrow (barrio + "Head Spa"), H1 Playfair con palabra en .text-shine, subtitulo emocional, badge rating real (estrellas + "5.0 · 102 resenas en Google"), doble CTA (Reservar + Llamar/WhatsApp), foto hero real con marco editorial + orbs detras.
3. **Strip de confianza**: 3-4 items (rating, "Se habla espanol" si aplica, barrio, servicio insignia con precio real).
4. **Experiencia/About**: que es el ritual head spa + que hace especial a ESTE negocio (usar research, no inventar), 1-2 fotos.
5. **El Ritual paso a paso**: 4 pasos genericos de head spa (diagnostico, limpieza profunda/vapor, masaje craneal, nutricion) en cards glass numeradas.
6. **Servicios**: menu REAL con precios/duraciones exactos del booking. Cards glass con hover lift + gradient border. Si hay categorias (head spa / facial / body / laser), tabs o grupos. Cada card con boton "Reservar" al canal real.
7. **Galeria**: grid masonry-ish de fotos reales (assets/ relativos), blur-up + hover zoom suave.
8. **Testimonios**: 3-4 quotes reales de Google/Yelp, con nombre y estrellas. Carrusel suave o grid.
9. **Ubicacion**: direccion real, horarios si se encontraron, telefono click-to-call, iframe Google Maps `https://www.google.com/maps?q=<direccion urlencoded>&output=embed`, boton "Como llegar".
10. **CTA final**: fondo accent-deep (seccion oscura), orbs, titular emocional, boton claro.
11. **Footer**: contacto, IG real, nota "Sitio de demostracion creado para <negocio>" NO (omitir: es demo de venta, se ve como site real), copyright con nombre del negocio, `.merktop-badge`.

## SEO/head minimo por site
- `<title>` = "<Negocio> · Head Spa en <Ciudad> | <tagline corto>"
- meta description con servicios y barrio, og:title/description/image (imagen local), theme-color = accent-soft.
- JSON-LD `HealthAndBeautyBusiness` con nombre, direccion, telefono, rating real (aggregateRating con reviewCount real), horarios si existen, sameAs (Instagram real, booking real).

## Imagenes
- Usar SOLO las descargadas en `<slug>/assets/raw/` que verificaron como validas. Elegir: 1 hero (la mas atmosferica), 2 para about, 6-8 galeria.
- Rutas relativas: `assets/raw/<archivo>`.
- `loading="lazy"` en todo excepto hero. `alt` descriptivo en espanol.

## Datos: verdad estricta
- Precios, nombres de servicios, rating, numero de resenas, direccion, telefono: EXACTOS del research. Nada inventado.
- Si un dato no se encontro (ej. horarios), omitir la fila, no rellenar.
- Reviews: solo quotes reales encontradas; si hay menos de 3, mostrar las que haya.

## Multilenguaje (OBLIGATORIO en todo demo)
Cada site se construye BILINGUE (espanol + ingles) en el mismo archivo:
1. **Idioma principal**: el del negocio (detectado en research: captions de IG, reseñas, menu). Es el idioma por defecto de la pagina y del `lang` del `<html>`.
2. **Mecanismo**: atributos `data-es` / `data-en` en cada nodo de texto traducible (o un dict JS `I18N = { es: {...}, en: {...} }` con claves por seccion). Toggle "ES | EN" en el nav (pill pequeño junto al CTA). Al cambiar: swap de textos, `document.documentElement.lang`, y persistir en `localStorage('lang')`. Al cargar: usar localStorage, si no `navigator.language`.
3. **Que NO se traduce**: nombres de servicios EXACTOS como los publica el negocio, precios, nombre del negocio, quotes de reseñas (van en su idioma original siempre).
4. Meta description y title en el idioma principal.
Snippet de referencia:
```html
<button id="langToggle" class="btn-ghost rounded-full px-3 py-1.5 text-xs">EN</button>
<script>
const applyLang = l => { document.querySelectorAll('[data-es]').forEach(el => el.textContent = el.dataset[l] || el.dataset.es); document.documentElement.lang = l; localStorage.setItem('lang', l); document.getElementById('langToggle').textContent = l === 'es' ? 'EN' : 'ES'; };
let lang = localStorage.getItem('lang') || (navigator.language || 'es').slice(0,2);
applyLang(lang === 'en' ? 'en' : 'es');
document.getElementById('langToggle').onclick = () => applyLang(document.documentElement.lang === 'es' ? 'en' : 'es');
</script>
```

## Accesibilidad y detalles
- Contraste AA sobre crema. `prefers-reduced-motion`: desactivar shimmer/orbs/reveal.
- `scroll-smooth`, anclas con `scroll-margin-top`.
- Sin em-dash en ningun copy. Copy en espanol neutro, calido, sin relleno.
