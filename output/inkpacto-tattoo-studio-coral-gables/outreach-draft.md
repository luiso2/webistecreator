# Outreach Draft: InkPacto Tattoo Studio (inkpacto-tattoo-studio-coral-gables)

Status: DRAFT ONLY. Not sent. Requires explicit user approval before send, per PIPELINE.md Fase 5.

- Sender: Michael Vargas <michael@go.merktop.com> (never merktop.com directly)
- Reply-to: jose@merktop.com
- Tag: campaign=siteforge
- To: no public email found (see data below, email_note). Contact via phone (786) 223-9238 (call/text) or Instagram DM to @mansotattoo.
- Idempotency-Key: siteforge-inkpacto-tattoo-studio-coral-gables-2026-08-06
- Angle: has_own_site = false -> "les construí un website de muestra"
- Language: Spanish (site/registry language = es; Fresha rating summary language and IG bio skew Spanish, matches the pipeline's es/en detection)

---

**Subject:** Un sitio de muestra para InkPacto Tattoo Studio

Hola equipo de InkPacto,

Los encontré revisando estudios de tatuajes en Coral Gables: 5.0 estrellas con 44 reseñas en Fresha es una marca real, y como no vi un website propio, les construí uno de muestra con sus tatuajes reales:

https://siteforge-demos.odd-forest-9504.workers.dev/inkpacto-tattoo-studio-coral-gables/

No toca nada de cómo trabajan hoy: el botón de reserva va directo a su Fresha, y las fotos y precios que ven ahí son los mismos que ya tienen publicados ahí (sesiones full color y black & gray, $50 en adelante).

Si les gusta, los ayudo a ponerlo en su propio dominio. Si no, lo retiro sin compromiso, solo avísenme.

Saludos,
Michael Vargas
Merktop
https://merktop.com

---

## dm_message (para el botón DM/WhatsApp del panel, máx 450 caracteres)

Hola! Soy Michael, de Merktop. Vi que InkPacto Tattoo Studio tiene 5.0 estrellas con 44 reseñas en Fresha pero sin website propio, así que les construí uno de muestra con sus tatuajes reales: https://siteforge-demos.odd-forest-9504.workers.dev/inkpacto-tattoo-studio-coral-gables/ No cambia nada de cómo trabajan hoy. Si les gusta, se lo dejamos en su propio dominio; si no, lo retiro sin problema.

(cuenta de caracteres: 398, dentro del límite de 450)

## Nota de entrega

No se encontró email público tras búsqueda exhaustiva: el campo `email` del payload de Fresha (`__NEXT_DATA__`, la fuente más fiable para este negocio) viene vacío, no hay linktree/beacons.ai asociado a la bio de Instagram, la página de Facebook (facebook.com/mansotatto) muestra un muro de login que bloquea el About, Yelp devuelve 403, un agregador de terceros (wheree.com) devuelve 403, y dos intentos de leer la bio de Instagram directamente (WebFetch: HTTP 429; Playwright local vía `ig_contact.py`: `ERR_CONNECTION_RESET`; `ig_scrape_fixed.js` con el fix de Chrome completo documentado en FORGE-BRIEF: `ERR_HTTP_RESPONSE_CODE_FAILURE`) no lograron cargar el perfil. El único canal de contacto público verificado es el teléfono (786) 223-9238, el Instagram @mansotattoo (DM) y la reserva directa en Fresha. Registrado como `outreach: pending_manual`.

Nota adicional (verificación de website propio): se probaron cinco dominios candidatos por curl (`inkpactotattoo.com`, `mansotattoo.com`, `inkpacto.com`, `inkpactotattoostudio.com`, `inkpactotattoo.net`); ninguno resolvió (sin DNS o TLS, no registrados o inalcanzables). Un sexto candidato, `inkpactostudio.com`, sí responde HTTP 200, pero es una página de parking de Sedo ("inkpactostudio.com is your first and best source for information about inkpactostudio"), no un sitio real del negocio. Los únicos canales propios confirmados son Fresha (perfil y booking, fuente de rating/reseñas/menú), Facebook, Instagram y un subdominio de Square (`inkpacto-tatto-studio.square.site`, plataforma de terceros, no dominio propio). `has_own_site` se mantiene en `false`.
