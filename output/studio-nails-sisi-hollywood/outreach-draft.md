# Outreach draft: Studio Nails By Sisi (Pembroke Pines, FL)

Estado: borrador, pendiente de aprobacion humana. No enviado. Sin canal de email publico verificado (ver nota abajo), asi que el envio real por ahora seria por WhatsApp/DM usando el `dm_message`.

## dm_message (WhatsApp / IG DM, ~450 caracteres max)

```
Hola! Soy Michael de Merktop. Vi Studio Nails By Sisi en Booksy (5.0 con 37 reseñas) y les construi un sitio web de muestra, gratis: https://siteforge-demos.odd-forest-9504.workers.dev/studio-nails-sisi-hollywood/ No toca su sistema de reservas de Booksy. Si les gusta se los dejamos en su propio dominio, si no lo retiramos, sin compromiso.
```

(341 caracteres, 0 em-dash)

## Cold email (borrador completo, en espanol)

Nota: no se encontro un email publico del negocio (ver "Investigacion de contacto" mas abajo), por lo que este correo queda listo para el dia que aparezca un email verificado, o para enviarlo por WhatsApp/DM adaptado. Sender real seria `Michael Vargas <michael@go.merktop.com>`, reply-to `jose@merktop.com`.

**Para:** (pendiente, sin email publico verificado)
**De:** Michael Vargas <michael@go.merktop.com>
**Asunto:** Un sitio de muestra para Studio Nails By Sisi

Hola Sisi,

Soy Michael, trabajo con Merktop. Encontre Studio Nails By Sisi buscando salones de unas en Pembroke Pines y me quede viendo su perfil de Booksy: 5.0 de calificacion con 37 reseñas es un numero que casi nadie tiene, y las fotos de sus sets (Russian manicure, polygel, la coleccion Signature Press On) se ven espectaculares.

Vi que hoy no tienen un sitio web propio, solo Booksy e Instagram, asi que les arme uno de muestra con sus datos reales: servicios, precios, reseñas y fotos tal como estan publicados. Pueden verlo aqui:

https://siteforge-demos.odd-forest-9504.workers.dev/studio-nails-sisi-hollywood/

Es solo una vitrina: no toca ni reemplaza su sistema de reservas de Booksy, el boton de reservar sigue llevando directo ahi. Si les gusta, se los podemos dejar corriendo en su propio dominio (StudioNailsBySisi.com o el que prefieran). Si no les interesa, lo retiramos sin ningun problema ni costo.

Cualquier pregunta, con gusto respondo.

Saludos,
Michael Vargas
Merktop
https://merktop.com

---

## Investigacion de contacto (para que quede registrado por que email = null)

- Booksy (JSON-LD del listing y HTML crudo del perfil): sin email de negocio, solo `help.us@booksy.com` (soporte de Booksy, no de la marca).
- Instagram `@studionailsbysisi`: `web_profile_info` devolvio 401 "Please wait a few minutes" (rate limited); WebFetch directo al perfil devolvio 429. No se pudo leer la bio ni el `external_url` en esta sesion.
- Facebook (`facebook.com/share/15tyCdGmPo`): WebFetch trajo el contenido truncado, solo se alcanzo a confirmar el nombre de la propietaria (Sileidy Leon), sin seccion About visible con email.
- Directorio nailmastersusa.com (listado de terceros): trae telefono (786) 739-0598 y direccion, pero ningun email ni link a dominio propio real (el link "Website" del listado apunta al propio nailmastersusa.com, no a un sitio del negocio).
- Yelp (`yelp.com/biz/studio-nails-by-sisi-hollywood`): bloqueado con 403 en WebFetch y en curl.
- Lemon8 (post promocional de la cuenta): confirma metodo de contacto = WhatsApp/Instagram, sin telefono ni email publicados ahi.
- Conclusion: `email: null`. El canal de contacto real y verificado es telefono/WhatsApp (786) 739-0598 e Instagram DM.

## Verificacion has_own_site

- `studionailsbysisi.com` y `studionailsbysisi.net`: no resuelven (curl exit 56 / sin DNS).
- `website_candidates` del dossier de Booksy: vacio.
- El unico "Website" que aparece en directorios de terceros (nailmastersusa.com) es un link a su propia pagina de listado, no un dominio propio del negocio.
- Conclusion: `has_own_site: false`, confirmado.
