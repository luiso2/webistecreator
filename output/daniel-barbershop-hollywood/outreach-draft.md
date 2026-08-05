# Outreach draft: Daniel Barbershop (daniel-barbershop-hollywood)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email" abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-daniel-barbershop-hollywood-2026-08-05
- **Angulo**: sin website propio (ver seccion "Chequeo de website propio")
- **Idioma**: ingles (idioma principal del negocio, reseñas en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/daniel-barbershop-hollywood/
- **Canal disponible**: sin email publico confirmado y sin telefono confirmado. Registrado como `outreach: pending_manual` con su Instagram @dani_barber_cuba para DM manual.

## Chequeo de website propio
- `website_candidates` en data.json (extraido de Booksy): vacio.
- `same_as` en data.json incluye `https://barbershopcuba2022.booksy.com`, que es un subdominio de la plataforma Booksy, no un dominio propio (no cuenta segun la regla dura).
- Busqueda "Daniel Barbershop" Hollywood FL Facebook / website: sin resultados que apunten a un dominio propio para esta direccion exacta (1625 N Hiatus Rd) o este handle de IG. Resultados encontrados como "danithebarber.com" y un funnel de gohighlevel para una barberia de Orlando/Kissimmee son negocios DISTINTOS sin relacion.
- Conclusion: `has_own_site: false`.

## Busqueda de telefono (profundizada, misma direccion bajo varios nombres)
- data.json (extraido del payload de Booksy): `phone: null`.
- El mismo local en 1625 N Hiatus Rd, Hollywood FL 33026 aparece en Booksy y en directorios bajo varios nombres relacionados: "Daniel Barbershop" (booksy id 871216), "A Barber Legend" / "A Barber's Legend" (booksy id 1488201), y en Yelp como "Barber Legend". Se reviso cada listado.
- Yelp (`yelp.com/biz/barber-legend-hollywood`, fetch directo): confirma la direccion "1625 N Hiatus Rd, Hollywood, FL 33026" y a Daniel como dueño/barbero, pero NO publica un numero de telefono en la pagina.
- Yahoo Local (`local.yahoo.com/info-239858837-barber-legend-hollywood`): confirma la misma direccion, sin telefono publicado.
- Booksy (paginas 871216 y 1488201, ambas para el mismo local): sin telefono visible en el HTML publico.
- Se descarto explicitamente el telefono (754) 225-3318 encontrado para "Great Clips" en la misma direccion de plaza comercial: es un negocio distinto (ya cerrado) en otra unidad del mismo strip mall, no pertenece a Daniel Barbershop.
- Conclusion: sin telefono publico verificable tras busqueda exhaustiva. `phone: null`.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- data.json (extraido del payload de Booksy): sin campo de email.
- Bio de Instagram (@dani_barber_cuba): WebFetch devolvio 429 (rate limit) al intentar acceder directamente al perfil.
- Booksy (ambas paginas del mismo local, 871216 y 1488201): sin `mailto:` en el HTML.
- Redireccion del link de `same_as` (`barbershopcuba2022.booksy.com` -> deep link de la app de Booksy): no expone email de contacto, solo abre la app/pagina de reserva.
- Busqueda de "Daniel Barbershop" / "dani_barber_cuba" + Hollywood + email/gmail: no aparecio ninguna direccion de correo publica que corresponda a este negocio.
- Conclusion: sin email publico verificable tras busqueda exhaustiva. `email: null`.

## Subject (para cuando haya un canal de email)
A sample website for Daniel Barbershop (it's ready)

## Cuerpo (referencia, para email o como base del DM largo)

Hi there,

I'm Michael, from Merktop. I found Daniel Barbershop on Booksy and a 5.0 rating across 198 reviews caught my eye, so I took a closer look at your fades, beard work and kids cuts.

I noticed you don't have your own website, just Booksy and Instagram, so I went ahead and built you a sample one with your real menu, real reviews and real photos of your work:

https://siteforge-demos.odd-forest-9504.workers.dev/daniel-barbershop-hollywood/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Booksy, exactly like today.
- It's bilingual (English and Spanish), ready for both sides of your Hollywood client base.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you, I'll take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi! I'm Michael, from Merktop. I found Daniel Barbershop on Booksy, 5.0 rating across 198 reviews, so I built you a free sample website with your real menu, prices and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/daniel-barbershop-hollywood/ It doesn't touch your Booksy booking at all. If you like it, I can put it on your own domain, if not I'll take it down, no pressure either way.
