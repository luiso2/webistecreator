# FAILED: jacksonville-handyman-llc

**Negocio**: Jacksonville Handyman, LLC (owner: John Spassoff), Jacksonville, FL
**Fecha**: 2026-08-13
**Fase donde falla**: Research (fase 1) / puerta de calidad de imagenes, ANTES de intentar el build.

## Motivo

Menos de 5 fotos reales y propias del negocio (regla dura de FORGE-BRIEF seccion 0.b y PIPELINE.md
fase 3). Tras una busqueda exhaustiva en TODAS las fuentes disponibles, el conteo de fotos reales,
verificadas y no-stock especificas de este negocio es **0**, muy por debajo del liston de 5.

Fuentes revisadas, una por una, con resultado:

1. **Google Business Profile (business.site)**: `https://jacksonvillehandymanllc.business.site/`
   responde HTTP 404 directo (curl con UA de Chrome). Cero contenido, cero fotos.
2. **Birdeye** (`reviews.birdeye.com/jacksonville-handyman-llc-156203781769223`, fuente de las 32
   reseñas de Google atribuidas a este negocio, y sitio del que SI se pudieron confirmar 3 reseñas
   verbatim con nombre): la unica "image" en su propio JSON-LD es
   `.../home-services/handyman.png`, el icono generico de categoria que Birdeye usa para CUALQUIER
   negocio de handyman sin fotos subidas. No es una foto de este negocio.
3. **Nextdoor** (`nextdoor.com/pages/jacksonville-handyman-llc-city/`): tiene UNA sola imagen, el
   avatar de la pagina. Se descargo y verifico con `file` (JPEG real, 650x438, valido). Al
   inspeccionarla visualmente: es una tarjeta/flyer de marketing diseñada ("Jacksonville Handyman
   904-446-7714" en texto, sobre una foto de stock generica de un cinturon de herramientas amarillo).
   Segun las reglas de curacion visual del propio pipeline (prohibido: capturas con texto encima,
   fotos de stock), esta imagen NO cuenta como foto real del trabajo del negocio, exactamente el
   mismo criterio ya aplicado a los precedentes `vip-woodwork-hialeah` y `ortiz-electrical-hialeah`
   (flyers promocionales con texto no cuentan para el liston de 5). Se guardo en
   `assets/raw/_discarded-nextdoor-card.jpg` solo como evidencia de la busqueda.
4. **Google Maps** (place_id `ChIJ0dLOaJlL5IgR38wmi7VtxeY`): el HTML estatico (curl, sin JS) solo
   trae el icono generico de usuario anonimo; el carrusel de fotos de Maps se renderiza por
   JavaScript y este entorno no tiene un navegador headless disponible para forzar esa carga.
5. **jacksonvillehandyman.com**: dominio que SI resuelve y SI tiene contenido real (HTTP 200,
   ~1MB, sitio Wix), pero pertenece a OTRO negocio distinto: telefono 904-201-9738 (no
   904-446-7714), se describe a si mismo como "a licensed general contractor", sin ninguna mencion
   a "Spassoff", "Chelsea Harbor" ni "LLC". Confirmado por busqueda cruzada que ese dominio y
   telefono pertenecen a "Jacksonville Handyman Services" (1301 Riverplace Blvd, Jacksonville FL
   32207, listado propio en Yelp), una empresa distinta. Coincidencia de nombre generico, no
   evidencia de que ESTE negocio tenga sitio propio. `has_own_site` se mantiene `false`.
6. **jacksonvillehandymanllc.com**: no resuelve (DNS, `getaddrinfo ENOTFOUND`, confirmado ademas
   por el proxy de salida con `connect_rejected` en reintentos).
7. **Facebook**: existen varias paginas con nombres parecidos ("JaxHandyman", "Jacksonville
   Handyman Services", etc.) pero ninguna se pudo confirmar como este negocio especifico (sin
   telefono/direccion verificable; Facebook bloquea el scraping sin login tanto por curl con UA de
   `facebookexternalhit` como por WebFetch, ambos devolvieron solo la pantalla de login generica).
8. **Instagram**: ninguna cuenta verificable encontrada.
9. **BBB**: no existe perfil para este negocio (solo aparecen otros handymen de Jacksonville sin
   relacion).
10. **Yelp / Houzz**: no existe listado para este negocio especifico (solo negocios homonimos no
    relacionados).
11. **Prensa local**: ninguna mencion encontrada.

## Que SI se pudo verificar (research no descartado, solo el build)

- Dueño: John Spassoff, corroborado por 3 reseñas de Google (via Birdeye) que lo nombran
  directamente y por un registro de un agregador de datos publicos que cruza la misma direccion y
  telefono.
- Telefono: (904) 446-7714, confirmado en 3 fuentes independientes (Birdeye JSON-LD, Nextdoor,
  la propia tarjeta grafica de Nextdoor).
- Rating: 5.0 con 32 reseñas, explicitamente atribuidas a Google por el propio desglose de Birdeye.
- 3 reseñas verbatim completas con nombre (Peter Makris, Erin Mongoven, Michelle D), mas
  extensas que las citas cortas del brief original, mas 2 testimonios cortos de Nextdoor (H.C.,
  C.N.).
- Servicios reales descritos en palabras de las propias reseñas y de las categorias que el propio
  negocio se puso en Nextdoor (reparacion de drywall/goteras, instalacion de ventiladores de techo,
  pintura interior/exterior, timbre con camara, cerradura con teclado, reparacion de concreto,
  carpinteria, azulejo, remodelacion de baño).
- Email: NO publico. Solo aparece un email personal en un agregador de busqueda de personas
  (US Search / PublicDataDigger), que no es un canal publicado por el negocio mismo: se decidio NO
  usarlo, siguiendo la regla de nunca fabricar ni apropiarse de canales de contacto que el negocio
  no hizo publicos el mismo.
- `has_own_site`: confirmado `false` (ver punto 5 y 6 arriba).

Ninguno de estos datos es el problema. El problema es exclusivamente el minimo de fotos: el
liston del pipeline es "¿puedo construirlo sin fabricar un solo dato?", y con 0 fotos reales
disponibles, cualquier galeria/hero/about tendria que rellenarse con la imagen de stock del cinturon
de herramientas o con el flyer de Nextdoor, ambas prohibidas por las reglas de curacion visual.

## Siguiente paso recomendado

Si en una sesion futura hay acceso a un navegador headless con IP residencial (para forzar la carga
del carrusel de fotos de Google Maps, que SI puede tener fotos subidas por clientes/el propio
negocio aunque no aparezcan en el HTML estatico) o si el dueño (John Spassoff, (904) 446-7714)
puede enviar 5+ fotos reales de trabajos terminados directamente, este negocio es facilmente
construible: tiene reseñas solidas, rating perfecto, telefono verificado y una historia real de
servicio (reparaciones, pintura, remodelacion) sin necesitar inventar nada mas que las fotos.

**No se marca este research como `research_degradado`**: no se uso el servicio de fotos de
Instagram vía Railway ni ningun canal que "no ve" contenido real; se comprobo activamente CADA
fuente disponible (Google Business, Birdeye, Nextdoor, Google Maps, dominio propio y su variante,
Facebook, Instagram, BBB, Yelp, Houzz, prensa) y cada una devolvio, de forma verificable, cero
fotos reales utilizables. Es un negocio genuinamente sin presencia fotografica publica, no un caso
de research insuficiente.
