# Tool Registry

Cada tool declara `name`, `description`, `permission` y `riskLevel`. El backend valida el plan antes de ejecutar cada paso y escribe un evento de auditoría.

## Activas

- `website.search`
- `website.get`
- `website.update`
- `website.content.update`
- `website.branding.update`
- `website.preview`
- `website.test`
- `website.publish`
- `website.rollback`
- `website.seo.configure`
- `website.seo.analyze`
- page/section operations sobre el SiteSpec
- configuraciones de forms, booking y WhatsApp como datos versionados

## Adaptadores pendientes

`website.analytics.get` devuelve explícitamente que todavía no hay una fuente de eventos conectada. Payments y otras integraciones externas están registradas, pero no ejecutan efectos externos hasta que exista un adapter y una política de aprobación específica.
