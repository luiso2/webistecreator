# FAILED: wildman-family-lawn-ocala

**Business**: Wildman Family Lawn Service LLC (owner Paul R. Wildman per BBB; field crew led by Caleb
Wildman and Luke per Google reviews)
**Niche**: landscaping / lawn care (also pressure washing per Nextdoor flyer and reviews)
**City**: Ocala, FL (4715 SE 31st St, Ocala, FL 34480)
**Fecha**: 2026-08-14
**Status**: failed

## Motivo

**Menos de 5 fotos reales verificables** tras busqueda exhaustiva en todos los canales
indicados y varios adicionales. Solo se recuperaron **4** fotos reales y propias del negocio,
cada una verificada con `file` (decodifican, >0 bytes) y MIRADA antes de contarla:

1. `gmaps_1.jpg`: foto real subida a la ficha de Google Maps del negocio (verificada en vivo con
   `scripts/gmaps_verify.js`, TLS fix): patio trasero con piscina, cesped recien cortado con
   lineas de corte nitidas, cortacesped y trabajador visibles al fondo. Calidad hero.
2. `crop_before_v3.jpg`: recorte real (SIN texto, SIN fondo del flyer) de la mitad "Before" de
   un flyer de servicio de pressure washing publicado por el negocio en su pagina de Nextdoor
   (aria-label del post confirma "Avatar for Wildman family lawn service"): cerca sucia/con
   moho antes del lavado a presion.
3. `crop_after_v4.jpg`: recorte real (mismo flyer, mitad "After"): fachada y cerca limpias tras
   el lavado a presion, con un trabajador visible a distancia realizando el trabajo.
4. `nd2_logo.jpg`: foto real (no vectorial) de un letrero fisico de yarda "Wildman Lawn Care,
   Mowing - Pressure Washing - Trimming, 352-209-2457" (mismo telefono confirmado), usada como
   imagen de perfil en una ficha duplicada de Nextdoor del mismo negocio.

El logo vectorial del negocio (mismo asset en Facebook y en el directorio de Nextdoor,
"WILDMAN FAMILY LAWN SERVICE" con icono de cortacesped) SI se recupero limpio y verificado, pero
por precedente de la forja (ver output/serrano-handyman-kissimmee/data.json > photos.used) un
logo es un activo de marca, no cuenta para el minimo duro de fotos de trabajo.

### Canales agotados (busqueda exhaustiva, con metodo y resultado)
- **Google Maps EN VIVO** (`scripts/gmaps_verify.js` y variantes propias con el mismo fix TLS):
  confirma 5.0 / 20 reseñas, "Add website" (sin website), telefono y direccion exactos. La ficha
  declara "22 Photos" pero el panel de Maps sin sesion iniciada solo expone la foto principal
  (limitacion documentada del propio script); se probo clic en el boton hero, clic en el enlace
  "22 Photos", clic en pestaña "All", scroll con `mouse.wheel` y scroll inyectado directamente en
  el contenedor del panel (`div[role="main"]`), y la pestaña de Reviews (que si devolvio 9 reseñas
  verbatim completas con nombre, pero ninguna foto de reseña en tamaño util, solo un avatar de
  32x32). Resultado: 1 sola foto accesible, la ya usada.
- **Facebook** (perfil confirmado, `facebook.com/people/Wildman-Family-Lawn-Service-LLC/61573596368443/`):
  fetch directo con UA `facebookexternalhit/1.1` a la raiz (200, solo el logo como og:image) y a
  `/about`, `/photos`, `/videos`, `/reviews` (los 4 devuelven 404). Tambien se probo
  `mbasic.facebook.com` (400) y Chrome completo real vs `/photos` (login-wall, pagina vacia) y
  contra `/61573596368443/photos` directo (error de certificado del proxy en la primera pasada,
  reintentado con `ignoreHTTPSErrors` y `--ignore-certificate-errors`: redirige a un muro de
  login vacio, 9 caracteres de body). La pagina en si es muy nueva y delgada (3 likes, "1
  talking about this").
- **Instagram**: sin cuenta propia localizable. Busqueda web ("Wildman Family Lawn Service Ocala
  instagram") solo encontro cuentas homonimas NO relacionadas (Wildman Landscaping en Huffman TX;
  Luke Wildman Dobbs; lukewildmann, 0 seguidores). Se probaron 6 handles candidatos directos
  (`wildmanfamilylawnservice`, `wildmanfamilylawn`, `wildman_family_lawn`, `wildmanlawnservicellc`,
  `wildman.family.lawn`, `wildmanlawncareocala`) con `scripts/ig_scrape_fixed.js`: ninguno resolvio
  a un perfil valido.
- **Yelp** (la ficha declara explicitamente "10 Photos" en el titulo indexado por Google): BLOQUEADO
  de forma consistente en las 4 vias intentadas: `curl` UA de escritorio (403), `curl` UA movil vía
  `m.yelp.com` (403), `WebFetch` (403), Playwright con el mismo fix TLS/proxy usado con exito en
  Google Maps y Nextdoor (`scripts/yelp_scrape_fixed.js`, 2 corridas, bodyText vacio, status HTTP
  403 confirmado con listener de respuesta), y el lector proxy `r.jina.ai` (devuelve advertencia de
  CAPTCHA de Yelp). Es un bloqueo de Cloudflare a nivel de IP del entorno (mismo patron que el
  bloqueo de IG por IP de datacenter documentado en FORGE-BRIEF), no un fallo de metodo: las 10
  fotos existen pero no son alcanzables con las herramientas disponibles en esta sesion.
- **BBB** (`bbb.org/us/fl/ocala/profile/landscape-contractors/wildman-family-lawn-service-llc-0733-235978250`):
  `curl` bloqueado (403); `WebFetch` si funciono (200, vía su propio fetcher) pero, preguntado
  explicitamente dos veces por imagenes/galeria, confirma que la pagina NO tiene seccion de fotos
  (solo el logo de BBB y un grafico decorativo). Tambien confirma A- rating, "NOT BBB Accredited",
  fundador Paul R. Wildman, inicio 3/1/2025, expediente abierto 21/1/2026. El metodo de pago
  (tarjeta/Venmo/PayPal) mencionado en el brief de la tarea NO se pudo re-confirmar de forma
  independiente en el texto de la pagina via WebFetch (puede estar en una pestaña que requiere JS
  que el fetcher no ejecuto); se deja sin usar por no poder verificarlo de primera mano.
- **Nextdoor**: dos fichas del mismo negocio bajo nombres ligeramente distintos,
  `nextdoor.com/pages/wildman-family-lawn-service-ocala-fl/` (1 post real, el flyer de pressure
  washing, unico slide del carrusel) y `nextdoor.com/pages/wildman-lawn-care-ocala-fl/` (sin
  posts propios, solo el feed generico de "Conversaciones en Ocala"; se verifico que las
  imagenes adicionales que aparecian al hacer scroll en esa pagina pertenecen a publicaciones
  de OTROS vecinos del feed general, no del negocio, y se descartaron explicitamente para no
  contaminar el research).
- **LinkedIn**: solo el perfil personal de Caleb Wildman (`linkedin.com/in/caleb-wildman-37ab06388`),
  bloqueado (HTTP 999 "Unknown Status", tipico de LinkedIn anti-scraping). No existe pagina de
  empresa (`linkedin.com/company/...`) para este negocio (el unico resultado "Wildman" en LinkedIn
  companies es una empresa homonima no relacionada en Indiana, "Wildman Business Group").
  No fue posible confirmar ninguna foto adicional por esta via.
- **Directorios generales**: Angi, Thumbtack y HomeAdvisor buscados especificamente por "Wildman"
  en Ocala: sin coincidencia (el negocio no tiene perfil en ninguno de los tres).

## Reseñas verbatim SI verificadas (para si se reintenta este negocio mas adelante)
Confirmadas en vivo via el panel de Reviews de Google Maps (no usadas, el build no se completo):
- Sara Comiskey: "Caleb and his team are very professional, responsive and kind!! They have
  given us a ton of hours back with our family by us out sourcing our lawn to them, we are so
  very thankful! They are hard workers and always do what they say they will!"
- Kay Bishop: "Wildman's Family Lawn Service did power washing of sidewalks, driveway, and
  entryway as well as gutter cleaning. This is a Christian based company with high standards of
  performance. I highly recommend their services."
- Eric Miller: "Yard looks great! These 2 young men are great at what they do. Give them a call!"
- Kyle: "They came in when my old lawn people were falling behind and got my entire place back
  in shape. Also love that it's a family business."
- C Fuster: "Luke and his team did a great job maintaining our property. Very professional,
  reliable, and easy to communicate with. The lawn looks clean and well maintained every visit.
  I also appreciate the attention to detail around the edges and landscaping areas. Highly
  recommend Wildman Family Lawn Service."
- james c: "Caleb does a good job with communicating, followed my specific requests avoiding any
  above ground sprinklers and cleaned up well when done. I use him everytime I need work done
  and life has me tied up."

## Datos verificados (para referencia si se reintenta)
- Telefono: +1 352-209-2457 (confirmado identico en Google Maps EN VIVO, BBB y el letrero fisico
  fotografiado en Nextdoor)
- Direccion: 4715 SE 31st St, Ocala, FL 34480 (confirmada en Google Maps EN VIVO)
- Rating/reseñas: 5.0 / 20 en Google, confirmado EN VIVO (no solo de un espejo de terceros)
- has_own_site: false. `wildmanfamilylawn.com`, `wildmanlawnservice.com`,
  `wildmanfamilylawnservice.com`, `wildmanlawncareocala.com`: los 4 devuelven `curl -> 000`
  (no resuelven DNS / no conectan), re-confirmado en esta sesion. Google Maps EN VIVO muestra
  "Add website" (sin sitio declarado).
- Facebook: `facebook.com/people/Wildman-Family-Lawn-Service-LLC/61573596368443/` (confirmado
  autentico via og:title/og:description: "Wildman Family Lawn Service is a family-owned lawn
  care service in Ocala, FL, specializing in mowing, leaf blowing, hedge trimming,...")
- Instagram: no localizado (ver arriba)
- Email publico: no encontrado en ningun canal revisado (Facebook, Nextdoor, BBB, Google Maps)
- Fundado: 1 marzo 2025 (BBB), negocio familiar muy joven

No se fabrico ningun dato ni foto. Se recomienda reintentar este negocio en una sesion con
acceso a Yelp (las 10 fotos declaradas ahi probablemente resuelven el minimo de 5 por si solas)
o si el negocio sube mas fotos a su ficha de Google Maps o abre una cuenta de Instagram.
