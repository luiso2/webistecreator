# SiteSpec v1

El esquema canónico está en [`schemas/site-spec.v1.json`](../schemas/site-spec.v1.json). El Worker valida el mismo contrato en `ui/control-plane.mjs`.

Un SiteSpec contiene:

- identidad y negocio;
- branding;
- páginas y secciones reutilizables;
- features e integraciones;
- SEO;
- estado de deployment;
- `contentPatch`, que es la única entrada que la forja puede aplicar al `content.json` existente.

Las revisiones se numeran de forma creciente. Rollback no borra historial: crea una nueva revisión basada en una revisión anterior.
