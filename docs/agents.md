# GPT y agentes

El GPT existente se conserva. Su Action debe importar o añadir estas operaciones:

- `GET /api/agent/v2/tools`
- `POST /api/agent/v2/execute`
- `GET /api/agent/v2/audit`
- `GET /api/agent/v2/sites/{slug}/spec`

El GPT puede buscar por nombre, ciudad, teléfono o slug. Si la búsqueda devuelve varios resultados, el backend no elige silenciosamente: devuelve candidatos y solicita más precisión.

Ejemplo de plan:

```json
{
  "request_id": "change-phone-2026-08-23-001",
  "plan": {
    "goal": "Cambiar el teléfono del sitio",
    "steps": [
      { "tool": "website.search", "args": { "query": "Miami Handyman" } },
      { "tool": "website.content.update", "args": {
        "site": { "slug": "miami-handyman" },
        "patch": { "hero": { "tarjeta": { "destacado": "305-555-1234" } } }
      } },
      { "tool": "website.publish", "args": { "site": { "slug": "miami-handyman" }, "reason": "phone update" } }
    ],
    "confirmed": true
  }
}
```

`request_id` es obligatorio. Repetirlo devuelve el mismo resultado y no crea una segunda publicación.
