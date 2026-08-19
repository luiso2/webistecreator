# forja-railway

Worker que construye los sites automaticamente desde Railway, consumiendo la cola del panel.
Sondea cada 25s: un item encolado a mano se toma en segundos, no en slots de ~7 min.

## Como funciona
cola del panel -> research_ig (Playwright del container) -> curacion+contenido con LLM
(DeepSeek primero; si falla o no tiene saldo, cae a Anthropic) -> guard anti-invencion
deterministico -> derive + gate -> sube al repo (API GitHub) -> Workers Builds deploya ->
verifica 200 -> registra en el panel -> done.

Division de trabajo: esta forja procesa items con @handle de IG. Los items por NOMBRE
(necesitan busqueda web) se los deja a la rutina cloud sin reclamarlos.

## Deploy / redeploy
El paquete es autocontenido (scripts y template copiados aqui). Desde esta carpeta:

    bash preparar.sh          # refresca scripts/ y templates/ desde el repo
    railway up --service forja --detach

## Variables del servicio (Railway -> forja -> Variables)
- DEEPSEEK_API_KEY   proveedor primario (OJO: necesita saldo; sin saldo cae a Anthropic)
- ANTHROPIC_API_KEY  fallback con vision
- GITHUB_TOKEN       para subir los sites al repo
- GH_REPO            luiso2/webistecreator
