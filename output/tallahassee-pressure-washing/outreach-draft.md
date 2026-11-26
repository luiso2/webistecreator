# Outreach draft: Tallahassee Pressure Washing (Tallahassee, FL)

## Datos de contacto
- Nombre: Tallahassee Pressure Washing (lavado a presion y soft wash, residencial y comercial)
- Ciudad / area de servicio: Tallahassee, FL y Leon County (negocio movil, sin direccion de local publica)
- Telefono: (850) 694-2790 / +18506942790
- Facebook: https://www.facebook.com/TallahasseePressureWashing (confirmado real via WebFetch, titulo de pagina "Tallahassee Pressure Washing | Tallahassee FL")
- Instagram: no encontrado
- Email: no encontrado (ver data.json, `email_notes`)
- Rating: 5.0 en Google, 90 resenas
- has_own_site: false. IMPORTANTE: el camion de la empresa anuncia el dominio "TallahasseePressureWashing.net", pero se verifico con consultas DNS-over-HTTPS directas (Google y Cloudflare) que ese dominio devuelve NXDOMAIN (no existe/no resuelve). No es un website propio real, solo un rotulo con un dominio expirado o nunca activado.
- Canal de contacto real: telefono directo. Facebook como canal secundario.
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/tallahassee-pressure-washing/

## Angulo (has_own_site: false)
"Te construimos un sample site gratis": el negocio no tiene un website propio real que funcione (el dominio impreso en su camion ni siquiera resuelve en DNS), solo su ficha de Google y una pagina de Facebook. El angulo es mostrarles una muestra ya lista con sus fotos reales, su rating real (5.0, 90 resenas) y su telefono, lista para usar en el dominio que ya tienen impreso en su flota si quieren activarlo, o en uno nuevo.

## Fuentes revisadas para email y redes (Fase 1, puntos 2 y 7)
- Ficha de Google Maps (gmaps_detail.js + gmaps_reviews.js + gmaps_photocycle.js via Playwright): rating 5.0/90, telefono +1 850-694-2790, categoria "Pressure washing service", boton "Add website" (no "Website"), sin email publico, horario "Open 24 hours" los 7 dias.
- Dominio impreso en el camion, TallahasseePressureWashing.net: probado con curl (502 del proxy), WebFetch (fallo de resolucion DNS) y consultas directas a los resolvers publicos dns.google y cloudflare-dns.com (DNS-over-HTTPS) para registro tipo A: Status 3 = NXDOMAIN en ambos. El dominio NO existe/no resuelve. No se uso como email ni como website propio.
- Facebook: facebook.com/TallahasseePressureWashing confirmado real (WebFetch devolvio el titulo de la pagina). Se intento ademas /about para buscar email o sitio adicional: bloqueado por el muro de login de Facebook (2 intentos, limite del pipeline alcanzado).
- WebSearch dirigido: "Tallahassee Pressure Washing" + email, + telefono 850-694-2790, + BBB Tallahassee pressure washing, + Garrett/Matt (tecnicos mencionados en las resenas), + Instagram: ningun resultado con un email o perfil de Instagram propio del negocio.

Conclusion: email = null, canal de contacto = llamada/mensaje de texto al telefono, o mensaje por Facebook. Registrar como `pending_manual`.

## Borrador de email (ingles, idioma principal del negocio)

Nota: no hay email publico verificado para este negocio (ver arriba), asi que este borrador queda preparado para el dia que se consiga un email (ej. si el negocio responde por telefono/Facebook y lo comparte), pero el canal de envio real recomendado hoy es telefono o Facebook, no email.

```
Subject: A sample website for Tallahassee Pressure Washing

Hi Tallahassee Pressure Washing team,

My name is Michael Vargas, from Merktop. I came across Tallahassee Pressure Washing while looking at pressure washing companies around Tallahassee, and saw you're at 5.0 stars with 90 reviews on Google, with people specifically calling out Garrett and Matt for being honest, punctual and doing great work on driveways, roofs and home exteriors.

I noticed Google doesn't have a website linked to your listing, so I put together a free sample site using your real photos, your reviews and your phone number:

https://siteforge-demos.odd-forest-9504.workers.dev/tallahassee-pressure-washing/

This does not touch your Google listing, your Facebook page, or anything you already have running. It's just a preview of what a dedicated website could look like for Tallahassee Pressure Washing.

If you like it, we can put it on your own domain and handle the setup. If it's not useful, just reply "no" and we won't follow up.

Best,
Michael Vargas
Merktop
```

## dm_message (version corta, maximo 450 caracteres, ingles, sin em-dash)

```
Hi, I'm Michael from Merktop. Found Tallahassee Pressure Washing on Google, 5.0 stars and 90 reviews, people rave about Garrett and Matt. I built a free sample website with your real photos and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/tallahassee-pressure-washing/ Does not touch your Google listing or Facebook. Happy to put it on your own domain, or remove it, no obligation either way.
```

(Conteo de caracteres: 395, dentro del limite de 450.)

## Notas de idioma
Idioma principal del site: ingles (todas las resenas con texto disponible y el rotulado del camion estan en ingles; Tallahassee es mercado mayoritariamente angloparlante para este nicho). El bilingue EN/ES esta incluido en el demo. El email y el dm_message van en ingles por ser el idioma principal detectado.

## Pendiente / notas para revision humana
- Sin email publico verificado: el canal de contacto recomendado es llamada o mensaje de texto al (850) 694-2790, o mensaje directo por la pagina de Facebook confirmada (facebook.com/TallahasseePressureWashing).
- No se encontraron resenas negativas graves en la muestra de 5 resenas extraidas (todas 5 estrellas); no hay alertas adicionales mas alla de la verificacion estandar antes de contactar.
- Dato curioso para el pitch humano: el dominio que ya tienen impreso en su flota de camiones (TallahasseePressureWashing.net) no existe/no resuelve, lo cual es un buen gancho de conversacion ("ya tienen el nombre pensado y hasta impreso en el camion, solo falta que el sitio exista de verdad").
