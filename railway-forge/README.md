# forja-railway

Worker que construye los sites automáticamente desde Railway, consumiendo la cola del panel.
Sondea cada 10s: un item encolado a mano se toma en segundos, no en slots de ~7 min. Cada forja tiene un límite duro de 510s (8.5 min) para cerrarse antes del SLA de diez minutos.

También incluye `cron.py`, un job corto para Railway que descubre negocios en Google
Maps, descarta fichas con website propio, evita duplicados y encola candidatos con
rating/reseñas/contacto suficientes. El job rota nichos y ciudades según `config.json`.

## Como funciona
cola del panel -> research (Instagram o Google Maps con Playwright del container) ->
curacion + contenido por reglas y plantillas por nicho (sin llamada a un modelo) ->
guard anti-invencion deterministico -> derive + gate -> publica un bundle versionado en
R2 -> verifica 200 -> registra en el panel -> done. El commit de GitHub se conserva como
archivo y fallback, pero ya no bloquea la disponibilidad del demo.

El worker procesa tanto items con `@handle` como items `nombre (ciudad)`. Las búsquedas
manuales de nicho + ciudad (`request.type=discovery`) tienen prioridad sobre los candidatos
del Cron: una sola reclamación descubre y construye hasta cinco negocios sin website propio,
sin quedarse esperando a que el Cron vuelva a ejecutarse. El Cron sigue descubriendo en
segundo plano y el claim atómico decide qué instancia construye cada item. Después del
descubrimiento, el Durable Object reserva cada negocio por place id de Maps, teléfono,
nombre+ciudad y slug. Una segunda réplica lo omite mientras está en construcción y un
negocio ya publicado devuelve su demo existente sin volver a investigarlo.

Los candidatos de una misma búsqueda manual se construyen en paralelo (por defecto, tres
workers por item), así que una solicitud de varios demos no queda bloqueada por una cadena
serial de investigaciones y despliegues. Se puede ajustar con `DISCOVERY_BUILD_WORKERS`
(1–3) si Railway dispone de más o menos CPU.

Si la solicitud llega sin un nicho útil (por ejemplo, "negocio local"), la forja prueba
categorías concretas como handyman, plumber, electrician y auto repair en la ciudad pedida.
Consulta dos categorías a la vez y como máximo cuatro, de modo que discovery no consume
todo el presupuesto. El filtro de website propio, rating, reseñas y fotos se mantiene en
cada consulta. Booksy, Facebook o Square siguen siendo perfiles; Wix, Squarespace,
WordPress, Webflow, GoDaddy Sites y Canva sí cuentan como websites existentes.

El segundo research abre directamente la URL exacta de Maps encontrada en discovery, sin
repetir una búsqueda ambigua por nombre. Al publicar, los archivos se suben en paralelo a
un prefijo inmutable de R2. El Worker comprueba tamaño y SHA-256 de cada objeto antes de
cambiar el puntero `current.json`; por eso nunca expone un bundle parcial. Después conserva
el árbol y commit atómicos de GitHub como respaldo.

El primer mensaje se genera con datos verificables (zona, fotos públicas, servicios y enlace
del demo), explica el beneficio para el cliente y termina en una pregunta de bajo compromiso.
Nunca se envía automáticamente: el panel exige la acción directa del usuario. El mensaje de
seguimiento comunica la oferta de $600 total, con dominio y mantenimiento incluidos durante
el primer año.

## Deploy / redeploy
El paquete es autocontenido (scripts y template copiados aqui). Desde esta carpeta:

    bash preparar.sh          # refresca scripts/ y templates/ desde el repo
    railway up --service forja --detach

Para activar el descubrimiento automático crea un segundo servicio Railway desde
esta misma carpeta y selecciona `railway-cron.json` como Railway Config File. Ese
archivo fija el Dockerfile, Start Command `python3 cron.py` y Cron Schedule
`*/5 * * * *` (UTC). El servicio debe terminar al acabar; no uses `main.py` como
Cron porque `main.py` es el worker permanente.

El Cron consulta dos combinaciones de nicho/ciudad, llena hasta 12 huecos por ejecución
(sin superar los 20 pendientes del panel), rota cada 5 minutos y deja que las réplicas permanentes construyan en
paralelo. `railway.json` está preparado con 4 réplicas del worker; si el plan de Railway
permite más recursos, subir ese número acelera linealmente el camino hacia 10.000 demos.

Ambos servicios limitan los autodeploys a `/railway-forge/**`. Los commits que publican
un demo bajo `output/` siguen activando Cloudflare, pero no reinician los workers de
Railway ni interrumpen el cierre del item que acaba de publicarlo.

Variables adicionales del servicio Cron:

- `SITEFORGE_UI_KEY`: el mismo access key que usa el panel (`.env` local), para
  poder crear items en `/api/queue` sin exponerlo en el código.
- `DISCOVERY_TARGET`: candidatos nuevos por ejecución (por defecto `12`, máximo `20`).
- `DISCOVERY_ROTATION_MINUTES`: intervalo de rotación de nicho/ciudad (por defecto `5`).
- `DISCOVERY_QUERIES`: combinaciones distintas por ejecución (por defecto `2`, máximo `3`).
- `CRON_MAX_BUILDS`: cuántos construye el Cron directamente si el worker
  permanente no los reclama (por defecto `1`).
- `DISCOVERY_NICHES` y `DISCOVERY_LOCATIONS`: listas separadas por comas para
  limitar o personalizar la rotación. Si se omiten, usa `config.json`.

## Variables del servicio (Railway -> forja -> Variables)
- GITHUB_TOKEN       para subir los sites al repo
- GH_REPO            luiso2/webistecreator
- PANEL_URL          opcional; por defecto usa el panel Siteforge
- SITEFORGE_PUBLISH_KEY clave privada para publicar bundles en R2; debe coincidir con el
  secret del Worker. Por compatibilidad también acepta `SITEFORGE_AGENT_KEY` o
  `SITEFORGE_UI_KEY`.
- SITEFORGE_UI_KEY   access key del panel y fallback de publicación; necesario en Cron
