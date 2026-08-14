# FAILED: handyman-multiservice-capecoral

**Motivo**: fotos insuficientes (menos de 5 fotos reales utilizables tras agotar las fuentes disponibles).

## Resumen de research (verificado, sin inventar nada)

- **Nombre**: Handyman Multiservice (aparece tambien como "Handy Man Multiservice" en BBB, y "HANDYMAN MULTISERVICE" en Yelp). Entidad legal: Handyman Multiservice LLC (Sunbiz FL, doc# L17000074625).
- **Ciudad**: Cape Coral, FL 33909. Direccion probable: 2620 NE 21st Ave, Cape Coral, FL 33909 (fuente: snippet de busqueda web, no verificada directamente en Sunbiz por bloqueo Cloudflare).
- **Telefono**: +1 239-677-0724 (confirmado en vivo por Google Maps).
- **Rating/reviews**: 4.9 / 69 en Google Maps, verificado EN VIVO dos veces (`gmaps_detail.js` x3 y `gmaps_verify.js` con query "Handyman Multiservice Cape Coral FL 33909" devolviendo `"ratingLive": "4.9", "reviewCountLive": "69"`). Coincide con el dato de discovery.
- **Categoria Google**: Handyman/Handywoman/Handyperson.
- **Website propio**: NINGUNO. Confirmado: `gmaps_detail.js` devuelve `website: null` en 3 corridas; WebSearch no encontro dominio propio; probados `handymanmultiservice.com`, `handymanmultiservicecapecoral.com`, `handymanmultiservicecc.com` (los 3 no resuelven, código 000/sin DNS).
- **Servicios** (de Yelp, via snippet de busqueda, consistente en 2 queries distintas): kitchen remodel, floor repair, mailbox installation, carpenter handyman work, sink repair, window repair. Categoria general: "high quality residential and commercial services", establecido en 2013.
- **Presencia online**: Yelp (18 fotos declaradas en el titulo de la pagina, pero la pagina esta bloqueada por DataDome CAPTCHA, no se pudo acceder ni con curl ni con Playwright headless), HomeAdvisor (bloqueado por Cloudflare challenge), BBB (accesible pero sin fotos ni resenas ni email publicados, no acreditados, expediente abierto 6/4/2024), Sunbiz (bloqueado por Cloudflare challenge).
- **Facebook / Instagram**: no se encontro ninguna pagina de Facebook ni perfil de Instagram propios tras varias búsquedas (incluida búsqueda por el numero de telefono).
- **Email publico**: no encontrado en ninguna fuente accesible.

## Por que fallo (fotos)

Fuentes agotadas segun el protocolo:
1. **Google Maps** (`gmaps_detail.js`, 3 corridas + `gmaps_verify.js`): solo **1 foto real** disponible (`lh3.googleusercontent.com/gps-cs-s/AHRPTWmsold9...`), sin galeria adicional, sin resenas verbatim renderizadas, sin service mentions.
2. **Facebook**: sin pagina propia encontrada.
3. **Instagram**: sin perfil propio encontrado.
4. **BBB / Angi**: BBB accesible pero sin fotos ni menu de servicios; no hay perfil dedicado en Angi para este negocio especifico (solo listados genericos de "mejores handymen en Cape Coral" que no lo mencionan).
5. **Yelp** (18 fotos en el titulo de la pagina, la mejor fuente potencial): bloqueado por proteccion anti-bot DataDome en todos los intentos (curl directo, curl vía proxy de lectura, Playwright headless con fix de TLS x2). No se pudo extraer ninguna foto.
6. **HomeAdvisor y Sunbiz**: bloqueados por el challenge gestionado de Cloudflare en todos los intentos.

Resultado: **1 foto real verificada**, muy por debajo del minimo de 5 fotos reales utilizables que exige el pipeline. No se completo el build para evitar un demo degradado (imagenes stock o repetidas queman el lead).

## Recomendacion

Reintentar mas adelante si Yelp/HomeAdvisor dejan de bloquear el scraping, o si el negocio abre una pagina de Facebook/Instagram con fotos propias. No reprocesar el slug hasta entonces.
