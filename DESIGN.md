# Design System Compartido: Head Spa Demos Miami (5 sites)

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
- `<title>` = "<Negocio> — Head Spa · <Ciudad> | <tagline corto>"
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

## Accesibilidad y detalles
- Contraste AA sobre crema. `prefers-reduced-motion`: desactivar shimmer/orbs/reveal.
- `scroll-smooth`, anclas con `scroll-margin-top`.
- Sin em-dash en ningun copy. Copy en espanol neutro, calido, sin relleno.
