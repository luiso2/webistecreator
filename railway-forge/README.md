# forja-railway

Worker que construye los sites automáticamente desde Railway, consumiendo la cola del panel.
Sondea cada 10s: un item encolado a mano se toma en segundos, no en slots de ~7 min.

También incluye `cron.py`, un job corto para Railway que descubre negocios en Google
Maps, descarta fichas con website propio, evita duplicados y encola candidatos con
rating/reseñas/contacto suficientes. El job rota nichos y ciudades según `config.json`.

## Como funciona
cola del panel -> research (Instagram o Google Maps con Playwright del container) ->
curacion + contenido por reglas y plantillas por nicho (sin llamada a un modelo) ->
guard anti-invencion deterministico -> derive + gate -> sube al repo (API GitHub) ->
Workers Builds deploya -> verifica 200 -> registra en el panel -> done.

El worker procesa tanto items con `@handle` como items `nombre (ciudad)`. Las búsquedas
manuales de nicho + ciudad (`request.type=discovery`) tienen prioridad sobre los candidatos
del Cron: una sola reclamación descubre y construye hasta tres negocios sin website propio,
sin quedarse esperando a que el Cron vuelva a ejecutarse. El Cron sigue descubriendo en
segundo plano y el claim atómico decide qué instancia construye cada item.

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
esta misma carpeta, con Start Command `python3 cron.py`, y configura en Settings →
Cron Schedule `*/15 * * * *` (UTC). Ese servicio debe terminar al acabar; no uses
`main.py` como Cron porque `main.py` es el worker permanente.

El Cron llena hasta 12 huecos por ejecución (sin superar los 20 pendientes del panel),
rota nicho/ciudad cada 15 minutos y deja que las réplicas permanentes construyan en
paralelo. `railway.json` está preparado con 4 réplicas del worker; si el plan de Railway
permite más recursos, subir ese número acelera linealmente el camino hacia 10.000 demos.

Variables adicionales del servicio Cron:

- `SITEFORGE_UI_KEY`: el mismo access key que usa el panel (`.env` local), para
  poder crear items en `/api/queue` sin exponerlo en el código.
- `DISCOVERY_TARGET`: candidatos nuevos por ejecución (por defecto `12`, máximo `20`).
- `DISCOVERY_ROTATION_MINUTES`: intervalo de rotación de nicho/ciudad (por defecto `15`).
- `CRON_MAX_BUILDS`: cuántos construye el Cron directamente si el worker
  permanente no los reclama (por defecto `1`).
- `DISCOVERY_NICHES` y `DISCOVERY_LOCATIONS`: listas separadas por comas para
  limitar o personalizar la rotación. Si se omiten, usa `config.json`.

## Variables del servicio (Railway -> forja -> Variables)
- GITHUB_TOKEN       para subir los sites al repo
- GH_REPO            luiso2/webistecreator
- PANEL_URL          opcional; por defecto usa el panel Siteforge
- SITEFORGE_UI_KEY   access key del panel, solo necesario para el servicio Cron
