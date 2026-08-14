# FAILED: cages-maintenance-capecoral

**Motivo:** menos de 5 fotos reales utilizables (minimo del pipeline). Solo se encontro 1 foto real apta para galeria; el resto de fuentes verificadas no aportan fotos utilizables o no tienen presencia publica.

## Negocio verificado (real, sin datos inventados)
- Nombre: Cage's Maintenance & More (LLC)
- Ciudad: Cape Coral, FL
- Direccion: 913 SW 16th Terrace, Cape Coral, FL 33991
- Telefono: +1 239-222-9477
- Email: Maintenanceexperts@yahoo.com (visto en foto de tarjeta de presentacion real, ver abajo)
- Owner: Anthony Cage (con Sarah E. Cage como co-manager/registered agent, segun Sunbiz)
- Categoria Google: Handyman/Handywoman/Handyperson
- Rating Google: 5.0 (10 resenas) - verificado 2 veces via `gmaps_detail.js` (rating) y confirmado el conteo de resenas (10) via `gmaps_discover.js` sobre "handyman in Cape Coral, FL" (mismo Place ID: 0x88db47a64211cd95:0xb2b920774e76f021, misma direccion/telefono).
- Website propio: NINGUNO. `gmaps_detail.js` -> `website: null`. `gmaps_discover.js` -> `hasWebsiteButton: false`. Busque dominios candidatos (cagesmaintenance.com, cagesmaintenanceandmore.com, cagemaintenance.com, yourmaintenanceexpert.com, cagesmaintenancemore.com): ninguno resuelve (502/NXDOMAIN via el proxy). Sunbiz (registro estatal LLC, doc L22000469614) no lista website. BBB: sin ficha (busqueda site:bbb.org sin resultados, y una busqueda BBB previa en el scratchpad de esta sesion tampoco encontro coincidencias). **PASO 1 (filtro duro) PASA: no tiene website propio.**
- Facebook: pagina existe ("Cage's Maintenance & More | Cape Coral FL", handle `yourmaintenanceexpert`, https://www.facebook.com/yourmaintenanceexpert/) pero Facebook bloquea todo scraping/WebFetch sin login (pagina siempre redirige a login, confirmado con curl, WebFetch y Playwright con Chrome real). No se pudo extraer ninguna foto ni texto de "About".
- Instagram: no se encontro cuenta propia (busquedas web no arrojan ningun perfil de Instagram del negocio; los resultados de "Cage's Maintenance Instagram" son de negocios de screen/pool cage NO relacionados).
- Yelp: sin ficha encontrada (bloqueado por captcha ademas).
- Angi/HomeAdvisor/Thumbtack: sin ficha encontrada para este negocio especifico.
- Nextdoor: pagina de negocio existe (https://nextdoor.com/pages/anthony-cage-cape-coral-fl/) con descripcion real: "We are a local family owned business based out of Cape Coral. We offer many different services ranging from small home maintenance, pressure washing, video surveillance and all your screening needs. We strive to leave all of our customers happy with a job well done." y 2 recomendaciones verbatim reales:
  - "He did the rebuild as well after Hurricane Ian. Front and back. ❤️"
  - "Anthony and Seth's company has been maintaining our lanai since we bought our home. He did the rebuild as well after Hurricane Ian. Front and back. ❤️"
- Servicios reales confirmados (Nextdoor + tarjeta de presentacion real vista en foto): pool cage cleaning & repairs, entryway repair & rebuild, security cameras, pressure cleaning, small home repairs, hurricane restoration/rebuild, screen installation & maintenance, TV mounting, shelf/closet rack installation, light electrical.
- Idioma: ingles (sin evidencia de negocio/resenas en espanol).

## Fotos: research exhaustivo, resultado insuficiente
Descargadas a `assets/raw/` (verificadas con `file`, las 3 son JPEG reales, no rotas):
1. `gmaps-1.jpg` (1600x1200, unica foto en la ficha de Google Maps, confirmada real y sin duplicados tras 3 corridas de `gmaps_detail.js` con distinto Place URL): foto atmosferica de un pool cage/lanai screened enclosure, aparentemente trabajo del negocio. **APTA para galeria/hero.**
2. `nextdoor-cover.jpg`: foto de la tarjeta de presentacion del negocio (texto: nombre, Anthony Cage owner, email, telefono, "Service's we offer") sobre una encimera. **NO apta**: texto/caption superpuesto, prohibido en galeria por el design system.
3. `nextdoor-logo.jpg`: otra foto de tarjeta de presentacion pegada sobre una malla de mosquitero/screen. **NO apta**: mismo motivo (texto superpuesto), y el unico contenido "de trabajo" visible es una malla generica sin valor visual.

Fuentes agotadas sin exito (Google es la fuente principal por PIPELINE.md, seguido de directorios y redes sociales):
- Google Maps: solo 1 foto en la ficha (confirmado como señal real, no fallo de script, segun la nota de limitaciones conocidas de `gmaps_verify.js`).
- Facebook: pagina real pero completamente bloqueada por login-wall (curl, WebFetch, y Playwright con Chrome headless real probados, los 3 metodos redirigen a pantalla de login).
- Instagram: sin cuenta propia localizable.
- BBB: sin ficha.
- Yelp: sin ficha (y bloqueado por captcha ademas).
- Angi/HomeAdvisor/Thumbtack/Manta/YellowPages/Chamber of Commerce: sin ficha con fotos.
- Directorios que si tienen ficha (bizprofile.net, leadsmartinc.com, fortmyersdirections.com): sin fotos propias del negocio (solo iconos genericos de plantilla).
- Bing image search por el nombre del negocio: sin resultados relevantes.

**Resultado: 1 sola foto real utilizable en galeria (gmaps-1.jpg). El minimo del pipeline es 5. No se puede construir el demo sin rellenar con fotos borrosas/con texto/genericas, lo cual esta prohibido y degradaria la calidad premium exigida.**

## Decision
FAIL segun regla de PIPELINE.md fase 3.5 ("failed se reserva para cuando faltan los MINIMOS: menos de 5 fotos reales propias...") y las instrucciones de esta corrida ("<5 utilizables = FAIL con FAILED.md"). No se prosigue a build. No se contacto al negocio por ningun canal.
