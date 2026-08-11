# Outreach draft: Alex @GalleryBarberStudio (Tampa, FL)

## Estado
- Email publico: NO encontrado. Research realizado: `data.json` (phone/instagram/same_as), busqueda web de "Gallery Barber Studio Tampa email/contact", Facebook de `alexblends__` y de la pagina del estudio "Fly Gallery Barber Studio" (ambas bloqueadas por login al hacer WebFetch, sin datos de contacto visibles publicamente), Instagram de `@alexblends__` (WebFetch devolvio 429, no se pudo leer la bio; no se intento con Playwright por restriccion del entorno).
- Telefono: NO encontrado (`data.json.phone = null`, tampoco aparece en busquedas web).
- Canal de contacto verificado: **Instagram DM** (`@alexblends__`) o mensaje en su pagina de Booksy.
- `has_own_site`: false. Nota: existe el dominio `gallerybarberstudio.com`, pero pertenece a un negocio DISTINTO en Sacramento, CA (@gallerybarbers916). Verificado como falso positivo, descartado, NO es el mismo negocio de Tampa.
- Idioma principal del negocio: ingles (`language: "en"` en data.json, resenas en ingles).
- Outreach: `pending_manual` (sin email, va por Instagram).

## Borrador de DM (Instagram, ingles, angulo "site de muestra")

Hey Alex! I came across your Gallery Barber Studio page in Tampa, 5.0 rating with 486 reviews on Booksy is no joke. I put together a free sample website for you, no strings attached: https://siteforge-demos.odd-forest-9504.workers.dev/alex-atgallerybarberstudio-tampa/

It's built entirely from your real photos and Booksy info, doesn't touch your booking flow at all. If you like it I can help you get it live on your own domain, if not, no worries, I'll just take it down.

Let me know what you think.

Michael Vargas
Merktop

## dm_message (version corta, para el registro, menos de 450 caracteres)

Hey Alex! Found your Gallery Barber Studio page, 5.0 with 486 reviews on Booksy. Built you a free sample site with your real photos, no strings attached: https://siteforge-demos.odd-forest-9504.workers.dev/alex-atgallerybarberstudio-tampa/ Doesn't touch your booking. Like it? I can help put it on your own domain. If not, I'll take it down, no worries. Michael Vargas, Merktop.

(caracteres: ~347)

## Notas
- NUNCA se envia nada: este es solo un borrador para aprobacion humana por lote (PIPELINE fase 5).
- No se contacto al negocio por ningun canal durante esta corrida.
- Sin em-dash en el mensaje.
- Si en una siguiente pasada se localiza un email publico real (p.ej. si el negocio lo agrega a Booksy o a su Instagram), reemplazar este canal por email siguiendo el mismo angulo.
