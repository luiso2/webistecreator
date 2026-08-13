# FAILED: mcconnells-express-jacksonville

**Business**: McConnell's Express Services, LLC (owner: Jason McConnell)
**Niche**: handyman / exterior painting / drywall / pressure washing / general home repair
**City**: Jacksonville, FL (450 State Road 13N, Suite #106/#123, Jacksonville, FL 32259; a suite/mailbox address, not a public storefront)
**Fecha**: 2026-08-13
**Status**: failed

## Motivo

Menos de 5 fotos reales y propias del negocio tras una busqueda exhaustiva. Se encontraron
y verificaron solo **2** fotos utilizables (ver detalle abajo), muy por debajo del minimo
duro de 5 que exige el quality gate (DESIGN.md / FORGE-BRIEF seccion 3.2 y 0.b). Contacto SI
existe (telefono verificado en 4+ fuentes independientes), asi que el fallo es puramente por
volumen y calidad de imagen, no por falta de canal de contacto ni por no poder describir el
negocio.

## Que se intento (research exhaustivo, por fuente)

1. **Birdeye** (`https://reviews.birdeye.com/mcconnell-s-express-services-llc-170083743666407`):
   fetch directo con curl + Chrome UA, HTTP 200, HTML completo guardado y parseado. Confirma
   rating 4.8/20 reviews (17 Google + 3 Birdeye), las 3 reviews verbatim ya conocidas (Susan A.,
   The D., Nora Moks M.), horario L-V 9am-6pm. **No trae fotos reales**: la unica imagen
   referenciada en el HTML es un cover generico de stock (`.../cover-image/home-services/handyman.png`)
   y un placeholder `default-business-250x250.png`, cero fotos subidas por clientes o por el
   negocio pese a que el brief sugeria que Birdeye suele embeber fotos de reseñas (no es el caso
   aqui, verificado con grep sobre el HTML crudo).
2. **Yelp** (`mcconnell-s-express-service-s-jacksonville-2`, listado con **92 fotos** segun el
   propio titulo indexado por el buscador): bloqueado en TODOS los intentos.
   - WebFetch directo: HTTP 403.
   - curl + Chrome UA completo (headers Accept/Accept-Language): HTTP 403, header
     `server: DataDome` / `x-datadome: protected` (bot-protection activo, no es un fallo
     transitorio).
   - `m.yelp.com` (version movil): HTTP 403 igual.
   - Proxy de renderizado `r.jina.ai`: tambien 403 (Cloudflare challenge en el proxy mismo).
   Las 92 fotos de Yelp (la fuente mas prometedora, con reviews que mencionan pintura exterior,
   drywall y trabajo del carport) quedaron inaccesibles con las herramientas disponibles en este
   entorno (sin navegador headless con IP residencial disponible aqui).
3. **Facebook** (`facebook.com/p/McConnells-Express-Services-LLc-100083404335887/`):
   WebFetch devuelve solo la pantalla de login ("Log in or sign up to view"). `mbasic.facebook.com`
   devuelve un error generico. Se probo el endpoint publico
   `graph.facebook.com/100083404335887/picture?type=large` (funciona sin token para fotos de
   perfil publicas): devolvio un **silueta placeholder generica** (200x200 y 1290x1290), es decir
   ese ID no tiene foto de perfil real accesible por esa via, o el ID no corresponde exactamente
   a la pagina. Sin acceso al feed/album de fotos de la pagina.
4. **Nextdoor** (2 paginas de negocio distintas, ambas indexadas para este mismo negocio):
   `nextdoor.com/pages/mcconnells-express-services-llc-jacksonville-fl/` y la variante `-1/`.
   Ambas cargaron con HTTP 200 (HTML completo, sin bloqueo). Se extrajeron y descargaron con
   curl + Chrome UA **las 7 imagenes reales** referenciadas en ambas paginas
   (`us1-photo.nextdoor.com/...`), verificadas con `file` (todas JPEG validos, ninguna de 0
   bytes) y **inspeccionadas visualmente una por una** (herramienta Read):
   - `nd-cover-1.jpeg` / `nd-cover-2.jpeg`: la MISMA foto (dos recortes/resoluciones distintas
     del mismo cover de negocio) de su trailer/remolque negro con el rotulo pintado del negocio,
     telefono (904)625-5771 y lista de servicios. Es una foto real del vehiculo de la empresa,
     pero cuenta como 1 sola imagen (duplicado) y lleva mucho texto pintado encima (rotulacion
     del vehiculo, no apto para tile de galeria "resultado terminado" segun la regla de curacion
     de FORGE-BRIEF punto 3.2, aunque si confirma independientemente el telefono).
   - `nd-logo-1.jpeg`: logo vectorial/clip-art del negocio (no es una fotografia; incluso tiene
     un error tipografico "McConell's" en el arte). No sirve como foto de galeria ni de hero.
   - `nd-logo-2.jpeg`: foto real del remolque/tanque de hidrolavado (pressure washing) rotulado
     con el logo del negocio. **Foto real y utilizable** (equipo de trabajo, buena luz, sin
     texto invasivo mas alla del logo pequeño en el tanque).
   - `nd-post-1.jpg`: foto de un jardin/casa con un arbusto podado, pero lleva el watermark de
     **TikTok de otra persona** ("@jayflay1981") superpuesto y bordes negros de video: no es
     contenido propio verificable del negocio, se descarta por posible mala atribucion.
   - `nd-post-2.jpeg` / `nd-post-3.jpeg`: fotos de una tarjeta de presentacion fisica
     (papel fotografiado). Confirman el nombre del dueno ("Jason McConnell"), el telefono y la
     lista de servicios (Lawn Care, Pressure Washing, Drywall, Small Electrical, Small Plumbing,
     Turn Key, Ceiling Fans, Screen Repair, Sprinkler Repair, Clean Outs), pero son fotos de
     texto/tarjeta, no de trabajo real, y estan prohibidas como tile de galeria (captura con
     texto encima).
   **Resultado neto de Nextdoor: 2 fotos reales utilizables** (el remolque rotulado y el tanque
   de hidrolavado), ninguna muestra pintura exterior, drywall o el trabajo en el carport que
   mencionan las reviews.
5. **HomeAdvisor** (`homeadvisor.com/rated.mcconnellsexpress.116937883.html`) y **Angi**
   (`angi.com/companylist/us/fl/st-johns/mcconnells-express-services-llc-reviews-1.htm`):
   ambos bloquean con HTTP 403 tanto a WebFetch como a curl con Chrome UA. Solo se pudo obtener
   contenido via resumen indexado del buscador (confirma rating 5.0, telefono, direccion,
   reviews de texto), sin acceso a fotos.
6. **LinkedIn** (`linkedin.com/in/jason-mcconnell-b54502327/`, perfil del dueño): WebFetch
   devuelve error HTTP 999 (bloqueo estandar de LinkedIn a fetchers automatizados). Sin acceso.
7. **Google Maps / Google Business Profile**: no se pudo acceder (la pagina de Maps es
   enteramente JS, WebFetch no ejecuta JS y no devuelve contenido util). Busquedas de imagen en
   Bing no devolvieron fotos hospedadas en dominios relevantes (yelp.com, facebook scontent,
   lh3.googleusercontent.com); los resultados de imagen fueron ruido no relacionado.
8. **Instagram**: no se encontro ningun handle verificable para este negocio (se descarto
   `mcconnelltransport` de una busqueda por no ser el mismo negocio: es una empresa de
   transporte distinta).
9. **Dominio propio**: se probaron `mcconnellsexpressservices.com`, `mcconnellsexpress.com`,
   `mcconnellexpressservices.com`, `mcconnellsexpressservicesllc.com` y `mcconnellsexpressjax.com`
   con curl; los 5 fallan en resolucion DNS (no existen). Confirma `has_own_site: false`, sin
   necesidad de detener el build por ese motivo (el bloqueo es solo por fotos).

## Contacto (para referencia, no bloquea el build por si solo)

- **Telefono**: `(904) 625-5771`, verificado de forma independiente en al menos 4 fuentes:
  (a) rotulado directamente en el propio remolque de la empresa (foto real, Nextdoor), (b) foto
  de la tarjeta de presentacion fisica (Nextdoor), (c) resumen indexado del listado en
  lawncarejacksonvillefl.com, (d) resumen indexado de Nextdoor/Angi/HomeAdvisor via busqueda web.
  Alta confianza.
- **Email**: NO encontrado en ninguna fuente (Birdeye, Nextdoor x2, Facebook, busqueda web
  general de variantes `mcconnellsexpress@`/`mcconnellexpressservices@`). Se registra como
  `null`.
- **Owner**: Jason McConnell (confirmado en tarjeta de presentacion fotografiada y en resumen de
  lawncarejacksonvillefl.com: "Owner/CEO", negocio fundado en 2013 segun ese listado y "EST 2012"
  segun el propio logo del negocio; discrepancia menor de un año entre dos fuentes secundarias,
  no crítica).

## Por que no se degrada el gate

Ninguna de las fuentes bloqueadas (Yelp/DataDome, Facebook/login, HomeAdvisor, Angi, LinkedIn)
es un "canal que solo devuelve URLs" en el sentido de la excepcion de `research_degradado` de
FORGE-BRIEF 0.b (esa excepcion aplica a un servicio de fotos de IG que no ve la bio real). Aqui
se obtuvo HTML completo y real de Birdeye y de ambas paginas de Nextdoor (HTTP 200, contenido
verificado), y las fuentes que fallaron lo hicieron con bloqueos duros de bot-protection
(DataDome, muros de login, 403 consistentes) that no tienen una via de rescate disponible con
las herramientas de este entorno (sin navegador headless con IP residencial). El resultado de
2 fotos reales utilizables es, por tanto, el resultado genuino del research, no un falso
negativo por canal degradado.

## Que se descarto y por que

Se descartaron explicitamente como NO utilizables para galeria/hero/about (aun siendo
descargas reales, no stock): la foto duplicada del remolque (texto pintado invasivo, cuenta
como 1 sola imagen ademas), el logo vectorial (no es fotografia), las 2 fotos de la tarjeta de
presentacion (capturas de texto), y la foto de jardin con watermark ajeno de TikTok (posible
mala atribucion a otra persona). Ninguna foto de pintura exterior, reparacion de drywall,
reemplazo de madera podrida o instalacion de vigas de soporte del carport (los trabajos que
describen las reviews reales) pudo ser localizada ni verificada.

## Archivos generados en esta corrida

- `output/mcconnells-express-jacksonville/assets/raw/*`: las 7 imagenes reales descargadas y
  verificadas de Nextdoor + Facebook graph picture (incluida la placeholder, dejada para
  evidencia), conservadas como evidencia del research pero NO usadas para construir ningun site.
- Este archivo (`FAILED.md`).

No se genero `data.json`, `content.json`, `index.html`, `registry_entry.json` ni
`outreach-draft.md`: por instruccion explicita, ante un fallo del HARD RULE de fotos el
proceso se detiene aqui sin construir un site degradado.
