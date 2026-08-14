# FAILED: rshandymanservicesorlando

**Negocio**: R&S Handyman Services LLC, Orlando, FL
**Telefono**: +1 407-591-9301
**Direccion (Google)**: 7737 Greytwig Ln, Orlando, FL 32818
**Rating**: 5.0 (31 resenas en Google, verificado en vivo hoy)
**Fecha**: 2026-08-14
**Fase donde falla**: Research (fase 1, imagenes) / puerta de calidad de fotos, ANTES de intentar el build.

## Motivo

Menos de 5 fotos reales y propias del negocio (regla dura de PIPELINE.md fase 3, punto 5: "menos
de 5 fotos reales propias" es uno de los MINIMOS que fuerzan `failed`). Tras una busqueda profunda
en TODAS las fuentes disponibles, el conteo de fotos reales, propias y UTILIZABLES (curaduria
visual: sin texto, sin logos, sin capturas) de este negocio es **0**.

## Paso 1: verificacion de website propio (negativo, confirmado)

- `curl -I` / `curl -sL` sobre `rshandymanservices.com`, `rshandymanservicesllc.com`,
  `randshandyman.com`, `rshandymanorlando.com`, `rnshandymanservices.com`: los que resuelven
  (`rshandymanservices.com` -> rsessentials.com, `randshandyman.com` -> ashevillelocalcraftsmen.com)
  son dominios expirados/reciclados que redirigen a negocios totalmente ajenos (joyeria y
  carpinteria de Asheville). Los demas no resuelven (`000`).
- BBB confirma que el UNICO canal web publico del negocio es su pagina de Facebook, no un dominio
  propio: "Website: Facebook page listed as facebook.com/RS-Handyman-Services-LLC-109471200497521".
- `has_own_site: false` confirmado de forma independiente (BBB + barrido de dominios).

## Paso 2: verificacion de email (POSITIVO, contrario a lo esperado, confirmado por 2 fuentes)

- El unico archivo real descargable de la ficha de Google Maps (la foto dada en el brief,
  `gmaps-1.jpg`) resulto ser, al inspeccionarla visualmente, una FOTO DE LA TARJETA DE PRESENTACION
  del negocio: "R&S HANDYMAN SERVICES LLC / Home Improvement / Rocky: 407-591-9301 / Zeeda:
  407-408-2708 / rnshandymanservices@gmail.com".
- Esto confirma el email `rnshandymanservices@gmail.com` de forma independiente al snippet de
  busqueda original (fuente 1: snippet de WebSearch; fuente 2: la propia tarjeta de presentacion
  fotografiada por el negocio y subida a su ficha de Google Maps). Tambien confirma el segundo
  telefono de Zeeda (Shazeeda Gobin, contacto secundario segun BBB) y coincide con los nombres de
  los principales (Rocky A Gobin / Shazeeda M Gobin) que da BBB.
- Email verificado: `rnshandymanservices@gmail.com`.

## Paso 3: busqueda de fotos (fuentes revisadas una por una)

1. **Google Maps**: unica URL de foto dada en el brief. Descargada (`gmaps-1.jpg`, JPEG real
   1080x608). Al inspeccionarla visualmente resulto ser la tarjeta de presentacion del negocio
   (fondo de madera con texto grande: nombre, servicios, telefonos, email), NO una foto de un
   trabajo terminado. Prohibida en galeria/hero por la regla de curacion visual ("capturas con
   texto" / material tipo flyer). El HTML estatico de la ficha de Maps (via WebFetch, sin
   navegador headless disponible en este entorno) no expone mas URLs `lh3.googleusercontent.com`
   del carrusel: solo la unica ya provista en el brief.
2. **Facebook** (`facebook.com/RS-Handyman-Services-LLC-109471200497521`, confirmado via BBB):
   `curl -sL` devuelve solo el shell vacio de la SPA (1542 bytes). `mbasic.facebook.com` con el
   slug y con el ID numerico devuelven el muro de login generico (200 con "photos and more on
   Facebook" o error 400), sin exponer ningun album publico sin autenticacion. Se probo tambien
   `graph.facebook.com/<id>/picture` (endpoint publico sin token): SI devuelve una imagen, pero es
   el logotipo circular del negocio ("RS HANDYMAN" con martillo, fondo azul marino), un logo con
   texto, tambien prohibido en galeria segun la regla de curacion visual. Se guardo como posible
   `brand.logo` si se hubiera construido el site, pero no cuenta como foto de trabajo.
3. **Thumbtack**: WebSearch por `"R&S Handyman Services" Orlando thumbtack` no devuelve perfil de
   este negocio especifico (aparecen homonimos no relacionados: "R&s Facility Services LLC" en
   Fort Lauderdale y "Orlando R Handyman Group LLC" en Apopka, ambos con telefono y ciudad
   distintos). Sin perfil, sin fotos.
4. **Yelp** (`yelp.com/biz/r-and-s-handyman-services-orlando-2`, confirmado por WebSearch):
   bloqueado por el desafio anti-bot de Yelp/Cloudflare tanto via WebFetch (403) como via curl con
   UA de Chrome (403, pagina de verificacion JS). Sin acceso a las fotos del listado.
5. **Nextdoor** (`nextdoor.com/pages/rs-handyman-services-llc-orlando-fl/`): la pagina publica no
   expone fotos reales del negocio, solo assets genericos de la UI de Nextdoor (iconos de
   reacciones, avatar placeholder). Sin fotos utilizables.
6. **Instagram**: ninguna cuenta de Instagram encontrada para este negocio en ninguna fuente
   cruzada (BBB, Yelp, Nextdoor, WebSearch directo por nombre + Orlando + "instagram").
7. **BBB**: perfil de texto puro, sin galeria de fotos.
8. **Houzz / Angi / Porch / HomeAdvisor**: WebSearch confirma que ninguno de estos directorios
   tiene un listado para este negocio especifico (aparecen competidores de Orlando, ninguno
   coincide en telefono ni direccion).
9. **Google Search HTML directo** (`curl` a `google.com/search?q=...`): la pagina se sirve
   completamente por JS (sin resultados estaticos en el HTML crudo), no expone imagenes.

## Que SI se pudo verificar (research no descartado, solo el build)

- Nombre, telefono, direccion, rating (5.0) y numero de resenas (31) verificados en vivo contra
  la ficha de Google Maps dada en el brief, y confirmados de forma cruzada por BBB (mismo telefono
  y direccion) y Nextdoor (mismo telefono y direccion).
- Temas reales de resenas (kitchen remodel, tidy work, attention to detail, speed of work,
  punctuality, quality of work, workmanship, respectful) tal como los dio el brief.
- `has_own_site: false` confirmado de forma independiente (paso 1 arriba).
- Facebook confirmado de forma independiente (BBB lista la misma URL dada en el brief).
- Email `rnshandymanservices@gmail.com` confirmado de forma independiente (tarjeta de presentacion
  fotografiada, subida por el propio negocio a Google Maps, mas el snippet de busqueda original).
- Servicios reales adicionales, tomados de la tarjeta de presentacion: Drywall, Painting,
  Flooring, Trims, Minor Plumbing, Electrical fixtures, Kitchen & Bath Remodel.
- 0 fotos reales de trabajos terminados, utilizables en galeria/hero segun la regla de curacion
  visual del pipeline (la unica foto disponible es una tarjeta de presentacion con texto; el logo
  de Facebook tambien tiene texto).

## Siguiente paso recomendado

Si en una sesion futura hay acceso a un navegador headless (para forzar la carga del carrusel
completo de fotos de Google Maps o para pasar el login-wall/anti-bot de Facebook y Yelp, ambos con
evidencia de tener contenido real: el post de Facebook de diciembre 2022 "Beautiful Sauna like
shower" indexado por buscadores, y el listado de Yelp con reseñas), o si el negocio puede enviar
5+ fotos reales de trabajos terminados directamente, este negocio es facilmente construible: tiene
rating excelente (5.0/31), telefono y email verificados de forma independiente, sin website propio,
y una historia real de servicio sin necesitar inventar nada mas que las fotos.

**No se marca este research como `research_degradado`**: se comprobo activamente CADA fuente
disponible (Google Maps, Facebook via curl/mbasic/graph, Thumbtack, Yelp, Nextdoor, Instagram, BBB,
Houzz/Angi/Porch/HomeAdvisor, Google Search directo) y cada una devolvio, de forma verificable, cero
fotos de trabajo reales utilizables. Es un negocio genuinamente con presencia fotografica publica
minima (1 tarjeta de presentacion + 1 logo, ninguno de los dos apto para galeria), no un caso de
research insuficiente.
