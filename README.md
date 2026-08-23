# Siteforge (Merktop)

Generador automatico de websites demo premium para cold outreach: encuentra negocios locales, construye un site personalizado con sus datos e imagenes reales (plantilla probada), lo deploya a Cloudflare Workers y envia el email de outreach.

## Como funciona
- **`PIPELINE.md`**: la especificacion completa del pipeline (research -> build -> verify -> deploy -> outreach -> registro). Es la fuente de verdad.
- **`DESIGN.md`**: design system compartido de los sites (estructura fija, paleta por marca).
- **`templates/dark/index.html`**: ejemplar de base oscura (Mizū Head Spa).
- **`templates/light/index.html`**: ejemplar de base clara (Amani HeadSpa).
- **`templates/assets/tailwind.js`**: Tailwind 3.4.16 local (el CDN no soporta SRI).
- **`config.json`**: nicho, ciudad, volumen diario, flags de outreach y deploy.
- **`data/processed.json`**: registro de negocios ya procesados (idempotencia, nunca reprocesar ni re-contactar).
- **`output/<slug>/`**: sites generados (index.html + assets + data.json del research).

## Control Plane del GPT (single-owner)

El GPT existente conserva sus Actions v1 para descubrimiento y builds. Las operaciones sobre
websites viven en `/api/agent/v2`: `GET /tools`, `POST /execute`, `GET /audit` y
`GET /sites/<slug>/spec`. El GPT puede localizar un sitio por nombre, ciudad o slug, cambiar
contenido/branding/SEO mediante un SiteSpec versionado y pedir una publicación confirmada.
La forja aplica el patch JSON al `content.json` existente, ejecuta `derive.py` + `gate.py` y
publica con el mismo Worker compartido. Esta instalación todavía es de un solo propietario:
no hay `tenant_id` ni aislamiento multi-tenant.

## Uso local (on-demand)
En Claude Code: `/siteforge <instagram handle | nombre del negocio | "buscar">`.
- Con handle/nombre: procesa ese negocio.
- Con "buscar": modo descubrimiento segun `config.json`.
Requisitos locales: wrangler OAuth logueado (cuenta Vargas MMI) y `RESEND_API_KEY` en `~/.zshrc`.

## Rutina cloud diaria
La rutina `siteforge-daily` (claude.ai/code/routines) corre este pipeline cada dia usando este repo como fuente:
- Descubre negocios nuevos, hace research, construye los sites y (si hay credenciales) los deploya.
- **NO envia outreach a los negocios**: redacta los borradores y los manda en el reporte diario a jose@merktop.com para aprobacion. El envio real se hace en sesion con `/siteforge` (aprobacion por lote) o manualmente.
- Reporte diario: conector MCP de Resend (adjunto a la rutina), solo a jose@merktop.com.
- Deploy: requiere el secret `CLOUDFLARE_API_TOKEN` en el entorno cloud "Merktop" (permiso Workers Scripts:Edit). Sin el, deja los sites en `output/` como `pending_deploy` y lo avisa en el reporte.
- Registro: la rutina commitea `data/processed.json` y `output/` de vuelta al repo.

## Reglas duras (no negociables)
1. Solo datos reales verificados. Nada inventado.
2. Verificar SIEMPRE si el negocio ya tiene website propio antes de escribirle (leccion MaRe: cambia el angulo del mensaje).
3. Cold email SOLO desde `go.merktop.com`. Maximo `daily_count` negocios/dia. Nunca 2 emails al mismo negocio.
4. Todo envio de outreach requiere aprobacion humana del lote (en sesion o respondiendo al reporte diario). Nada de envio desatendido.
5. Sin em-dash en ningun output.
6. Footer "Powered by Merktop" en todo site.
