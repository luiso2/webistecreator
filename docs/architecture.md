# Siteforge Control Plane

Esta fase mantiene una instalación de propietario único. No existe todavía una dimensión `tenant_id`.

```mermaid
flowchart TD
  U[Usuario / GPT actual] --> A[Action API v2]
  A --> R[Plan validator + Intent tools]
  R --> P[Permission engine]
  P --> E[Execution engine]
  E --> S[SiteSpec v1 en KV]
  E --> Q[QueueClaims + cola de forja]
  Q --> F[Railway deterministic forge]
  F --> G[derive.py + gate.py]
  G --> C[GitHub atomic commit]
  C --> W[Cloudflare shared demo Worker]
  E --> L[Audit log]
```

El GPT no escribe HTML ni ejecuta Cloudflare directamente. Para modificar un sitio localiza el registro, cambia el `SiteSpec`, prueba la revisión y solicita publicación. La forja aplica el `contentPatch` al `content.json` existente y reutiliza el pipeline probado.

## Latencia de ejecución

`POST /api/agent/v2/execute` ejecuta y valida el plan antes de responder, pero persiste la
auditoría en segundo plano con `waitUntil`. Así la respuesta del GPT no queda bloqueada por
el segundo viaje al Durable Object que conserva el historial; los eventos siguen siendo
durables y `GET /api/agent/v2/audit` los expone cuando el usuario los necesita.

## Compatibilidad

Los endpoints `/api/agent/build`, `/api/agent/jobs/*` y `/api/agent/sites` se mantienen. El nuevo contrato vive en `/api/agent/v2/*`, por lo que el GPT actual puede seguir funcionando mientras se actualiza su Action.

## Persistencia actual

- `site-spec:<slug>:current`: revisión activa.
- `site-spec:<slug>:v:<revision>`: historial inmutable de revisiones.
- `control:audit:<id>` y `control:audit:index`: eventos de herramientas.
- `control:idempotency:<request_id>`: resultado durante 24 horas para evitar dobles operaciones.

KV es suficiente para esta fase de propietario único. La migración futura a D1/R2/Queues puede conservar estas mismas interfaces.
