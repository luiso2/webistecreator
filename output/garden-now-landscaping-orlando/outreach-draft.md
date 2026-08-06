# Outreach Draft: Garden Now Landscaping Orlando (garden-now-landscaping-orlando)

Status: DRAFT ONLY. Not sent. Requires explicit user approval before send, per PIPELINE.md Fase 5.

- Sender: Michael Vargas <michael@go.merktop.com> (never merktop.com directly)
- Reply-to: jose@merktop.com
- Tag: campaign=siteforge
- To: no public email found (see data below, email_note). Contact via phone (407) 914-1712 (call/text) or Instagram DM to @gardennow_.
- Idempotency-Key: siteforge-garden-now-landscaping-orlando-2026-08-06
- Angle: has_own_site = false -> "les construí un website de muestra"
- Language: Spanish (site/registry language = es; business's IG captions and ad copy are predominantly Portuguese, and the pipeline only supports es/en, so Spanish was chosen as the closer language and used consistently for outreach and dm_message)

---

**Subject:** Un sitio de muestra para Garden Now Landscaping

Hola equipo de Garden Now,

Los encontré revisando paisajismo en Dr. Phillips: 5.0 estrellas en Google es una marca real, y como no vi un website propio, les construí uno de muestra con sus fotos y servicios reales:

https://siteforge-demos.odd-forest-9504.workers.dev/garden-now-landscaping-orlando/

No toca nada de cómo trabajan hoy: el botón de contacto va directo a su teléfono, (407) 914-1712, y todo el contenido sale de su propio Instagram (@gardennow_). Los precios no están publicados porque ustedes tampoco los publican, cada proyecto sigue cotizándose como siempre.

Si les gusta, los ayudo a ponerlo en su propio dominio. Si no, lo retiro sin compromiso, solo avísenme.

Saludos,
Michael Vargas
Merktop
https://merktop.com

---

## dm_message (para el botón DM/WhatsApp del panel, máx 450 caracteres)

Hola! Soy Michael, de Merktop. Vi que Garden Now Landscaping tiene 5.0 estrellas en Google pero sin website propio, así que les construí uno de muestra con sus fotos y servicios reales: https://siteforge-demos.odd-forest-9504.workers.dev/garden-now-landscaping-orlando/ No cambia nada de cómo trabajan hoy. Si les gusta, se lo dejamos en su propio dominio; si no, lo retiro sin problema.

(cuenta de caracteres: 387, dentro del límite de 450)

## Nota de entrega

No se encontró email público tras búsqueda exhaustiva: intento directo del endpoint `web_profile_info` de Instagram (bloqueado por rate limit HTTP 400/401/429 en varios reintentos), bio de Instagram (no accesible por el mismo rate limit; sin linktree/beacons.ai asociados, ambos devuelven 404/403), directorios (BrightPath Contractors, SimplyLawn, ServiceAgent.ai, Yelp) sin mailto expuesto, y sin página de Facebook propia localizable con sección About legible. El único canal de contacto público verificado es el teléfono (407) 914-1712 y el Instagram @gardennow_ (DM). Registrado como `outreach: pending_manual`.

Nota adicional: se probó `gardennow.com` (candidato generado automáticamente a partir del nombre del negocio, no visto en ninguna bio ni listado). Responde HTTP 403 detrás de un reto de Cloudflare y redirige a `telepathy.com`, un dominio sin relación aparente con paisajismo. Se interpreta como una coincidencia de nombre / dominio no relacionado, no como el sitio propio del negocio; `has_own_site` se mantiene en `false`, consistente con el research previo (gardennowlandscaping.com y variantes no existen; agregadores muestran "Website: Not provided").
