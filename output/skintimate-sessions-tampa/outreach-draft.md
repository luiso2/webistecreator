# Outreach draft: Skintimate Sessions (Tampa, FL)

## Estado
- Email publico: **NO encontrado.** Se busco en (1) data.json (`phone`: null, `instagram`: skintimatesessions, `same_as`: solo IG), (2) pagina de Facebook publica (solo muro de login, sin About visible sin sesion), (3) WebSearch "Skintimate Sessions email/contact", (4) WebSearch por "Naromi" + negocio, (5) WebSearch de posible Linktree. Yelp y Groupon devolvieron 403 al fetch (no se pudo revisar su contenido). Ningun email publico salio indexado.
- Telefono: no publicado en Booksy (`phone: null` en data.json).
- Canal de contacto verificado: **Instagram** (@skintimatesessions) y Booksy (reservas).
- Outreach: `pending_manual` via Instagram DM (no hay email ni telefono publico para email frio ni WhatsApp).
- Nota de direccion: Yelp lista "6708 E Fowler Ave" y otras fuentes dicen "Temple Terrace" vs "Tampa"; el site y este borrador usan EXCLUSIVAMENTE la direccion que trae `data.json` de Booksy: 6406 E Fowler Ave, Suite E, Temple Terrace, FL 33617 (Booksy la etiqueta como area "Tampa").

## Borrador de DM (Instagram, no se envia sin aprobacion)

Hi Naromi! I came across Skintimate Sessions on Booksy (5.0 with 129 reviews, seriously impressive) and I put together a free sample website for the studio, just to show what it could look like:

https://siteforge-demos.odd-forest-9504.workers.dev/skintimate-sessions-tampa/

It doesn't touch your Booksy bookings at all, it's just a landing page with your real photos, services and reviews. Happy to hand it over for your own domain, tweak it, or you can ignore it completely, no pressure either way. Let me know if you'd like it!

Best,
Michael Vargas
Merktop

## dm_message (version corta, campo del registro, < 450 caracteres)

"Hi Naromi! Saw Skintimate Sessions on Booksy (5.0, 129 reviews) and built a free sample website for the studio: https://siteforge-demos.odd-forest-9504.workers.dev/skintimate-sessions-tampa/ Doesn't touch your Booksy bookings, just a preview. Happy to hand it over or you can ignore it, no pressure. Michael Vargas, Merktop."

(Longitud: ~285 caracteres, dentro del limite.)

## Notas
- Angulo: "les construimos un sitio de muestra" (has_own_site: false, no se encontraron `website_candidates` en el dossier).
- Idioma principal del negocio: ingles (confirmado por `language: "en"` en data.json y por el idioma de las reseñas/menu). El DM va en ingles.
- Firmado Michael Vargas / Merktop, sin em-dash.
- NUNCA se envia nada desde este borrador: requiere aprobacion humana explicita por lote (PIPELINE Fase 5). No se contacto al negocio por ningun canal durante esta corrida.
- Reseña de "Zayna" en Booksy tenia el autor guardado literalmente como un email personal (`Zaynapowell34@gmail.com`) en vez de un nombre anonimizado como las otras dos reseñas (`Ashlee W…`, `Karyna P…`). Se redacto a "Zayna P." en el site y en este borrador para no publicar el email personal de una clienta (dato de un tercero, no del negocio); el texto de la reseña se mantuvo verbatim.
