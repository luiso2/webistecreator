# FAILED: renovationrestorationhandymanorlando

**Negocio**: RENOVATION & RESTORATION HANDYMAN SERVICES L.L.C. (Orlando, FL)
**Motivo**: menos de 5 fotos reales y propias del negocio disponibles tras research exhaustivo (minimo del pipeline). Research NO degradado: se hizo con Playwright con acceso completo a Google Maps, BBB, Nextdoor, bizprofile/Sunbiz y busqueda web; no es un caso de "research_degradado" (seccion 0.b de FORGE-BRIEF).

## Research completado (para que no se repita)

### Identidad y website propio: CONFIRMADO sin dominio propio
- `rr-handyman-services-llc.business.site` (el "website" que muestra su propia ficha de BBB): HTTP 404, inactivo.
- `rrhandymanservices.com`: dominio parqueado en HugeDomains (a la venta), no es un site del negocio.
- `rrhandymanandrenovations.com` / `rrhandymanservicesorlando.com`: son de **otro negocio distinto** llamado "RR Handyman & Renovation Services" (telefono (305) 609-6847, contacto Christian / rrhandyman.renovationservices@gmail.com), confirmado por busqueda de resenas de Facebook. NO es el mismo negocio (nombre parecido, coincidencia comun en el nicho handyman de Orlando: existen al menos 3 negocios "R&R"/"RR Handyman" distintos en la zona).
- Conclusion: `has_own_site: false`, confirmado con evidencia solida (BBB, dominio parqueado, 404).

### Contacto
- **Telefono**: +1 407-401-0184 (verificado en Google Maps, BBB, Nextdoor, coincide en todas las fuentes).
- **Email encontrado**: `Rick192005@aol.com`, publicado en la ficha de negocio de Nextdoor (`https://nextdoor.com/pages/r-r-services-llc-orlando-fl/`), junto con el mismo telefono y el mismo (dead) business.site. Fuente publica, sin login.
- **Registered agent / dueno**: Rickey L. Heath, Jr. (Sunbiz doc L20000123235, EIN 85-1364469, LLC activa desde 5/6/2020), via bizprofile.net.
- Nextdoor confirma ademas: "Neighborhood Favorite in 2023", y multiples recomendaciones verbatim de vecinos citando el mismo telefono ("You can call R&R Services 407-401-0184. They are reasonable & do great work." — H.H., Orlando).

### Redes sociales
- Sin Instagram propio verificable (varios handles candidatos probados via endpoint publico, rate-limited/sin match confirmado).
- Facebook: existen paginas candidatas (`facebook.com/Rickey591/`, `facebook.com/HandymanRR/`) pero ambas quedan detras del muro de login de Facebook sin forma de confirmar nombre+ciudad+telefono: NO se aceptan sin ese match solido (regla del pipeline).

### Fotos: el bloqueador
- **Google Maps (fuente principal)**: la ficha tiene exactamente **1 foto real** subida (confirmado con Playwright abriendo la ficha completa, sin sesion iniciada = "vista limitada" de Google, sin boton de resenas visible tampoco). Se descargo: `assets/raw/gmaps-1.jpg` (vista aerea de techo/canaleta de una casa, foto de trabajo real).
- **Nextdoor**: la pagina de negocio trae una seccion "Photo gallery +1" con una foto adicional de una reparacion de tuberia de riego (`assets/raw/nd-irrigation-nextdoor.jpg`), consistente con el tema de resenas "irrigation system repair & maintenance". Se descargo pero con confianza MEDIA en su atribucion (no se pudo confirmar 100% que sea foto subida por el propio negocio y no por un vecino en un hilo de recomendacion).
- El resto de imagenes encontradas en Nextdoor son: (a) un flyer/grafico con texto superpuesto (promocional, descartado por regla de curaduria: "prohibido capturas con texto/caption encima"), y (b) dos fotos de un callejon/patio que por la estructura de la pagina parecen pertenecer al hilo de un vecino pidiendo sugerencias de instalacion de cerca (no al trabajo del negocio): se descartaron por riesgo de mala atribucion.
- **BBB**: sin fotos (perfil no acreditado, solo datos de registro).
- **LocallyFind**: bloqueado por error de handshake TLS/SSL en todos los intentos (curl y Playwright).
- **Yelp**: existe un listado "R&R Services" en Maitland Blvd, Orlando con 24 fotos, pero es una **direccion distinta** (Maitland Blvd vs 6402 Beggs Rd) y Yelp bloqueo el acceso (403 / "You have been blocked") antes de poder confirmar telefono: no se pudo verificar que sea el mismo negocio, así que NO se uso.
- **Thumbtack, Houzz, Angi, HomeAdvisor**: sin perfil propio identificable para este negocio especifico (busquedas devuelven negocios homonimos/competidores distintos).
- **Instagram**: sin perfil confirmado (ver arriba).
- **Facebook**: paginas candidatas bloqueadas por login, imposible extraer fotos.

**Resultado**: 1 foto de alta confianza (Google Maps) + 1 foto de confianza media (Nextdoor, riego) = maximo 2 fotos reales utilizables, por debajo del minimo de 5 que exige el pipeline. No se fabrico ni se relleno con material de otros negocios ni stock.

## Assets conservados
- `assets/raw/gmaps-1.jpg`: foto real de Google Maps (techo/canaleta), unica foto de la ficha de Google del negocio.
- `assets/raw/nd-irrigation-nextdoor.jpg`: foto real de Nextdoor (reparacion de tuberia de riego), atribucion de confianza media.

No se construyo `content.json` ni `index.html`: el pipeline prohibe avanzar a build con menos de 5 fotos reales verificadas.
