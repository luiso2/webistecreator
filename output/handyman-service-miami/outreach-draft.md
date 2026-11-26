# Outreach draft: Handyman Service (Miami, FL)

## Datos de contacto
- Nombre: Handyman Service (handyman/remodelacion; las resenas de Google se refieren al dueno/operador como "Julian")
- Direccion: no publica direccion exacta en su ficha de Google (negocio movil/de area de servicio). Un agregador independiente (Birdeye) que replica las mismas resenas de Google muestra 722 SW 65th Ave, Miami, FL 33144, pero esa direccion NO se publico en el site por no ser publica en la ficha de Google en vivo. Ver `data.json` -> `address_note`.
- Telefono: (305) 484-4393 / +13054844393
- Instagram/Facebook: no encontrado (ver `data.json` -> `ig_source`)
- Email: no encontrado (ver `data.json` -> `email_notes`)
- Rating: 4.6 en Google, 18 resenas
- has_own_site: false (handymanservicemiami.com es un dominio aparcado en venta via GoDaddy, no un sitio real; ver `own_site_check` en data.json)
- Canal de contacto real: llamada telefonica al (305) 484-4393
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/handyman-service-miami/

## NOTA PARA REVISION HUMANA ANTES DE ENVIAR
El negocio aparecio originalmente en una busqueda de Google Maps acotada a "Miami Beach, FL" (tarea original), pero investigacion cruzada con un agregador independiente (Birdeye, que replica verbatim la misma resena de Kassandra Torrens sobre el "Thin Blue Line challenge coin holder", confirmando que es el mismo negocio/Place ID) indica que su direccion real esta en Miami (zip 33144, area de Westchester/Fontainebleau), no en la isla de Miami Beach. Se amplio el area de busqueda de "Miami Beach" a "Miami" (ambas areas estan en `config.json` -> `extra_areas`) tras una busqueda exhaustiva en Miami Beach que no arrojo ningun candidato limpio del nicho handyman/remodelacion (ver seccion de candidatos descartados en el reporte final del agente). El site y el outreach usan honestamente "Miami, FL (incluye Miami Beach)" como area de servicio, sin afirmar una direccion especifica en Miami Beach.

## Angulo (has_own_site: false)
"Te construimos un sample site gratis": el negocio no tiene un sitio de marketing propio (su unico dominio de nombre similar, handymanservicemiami.com, esta aparcado en venta sin contenido real), asi que el angulo es mostrarles una muestra ya lista con sus fotos reales de trabajos, su rating de Google y sus resenas reales.

## Fuentes revisadas para email y redes (Fase 1, puntos 2 y 7)
- Ficha de Google Maps en vivo (scripts/gmaps_discover.js + gmaps_detail.js): website=null, boton "Add website", sin email publico.
- Dominios probados: handymanservicemiami.com (200, pero redirige a forsale.godaddy.com: dominio aparcado en venta), handyman-service-miami.com y handymanservicefl.com (no resuelven).
- WebSearch del telefono (305) 484-4393 en multiples variantes de formato: sin resultados de un sitio propio, IG o FB.
- WebSearch de "Julian" (nombre mencionado en las resenas) + handyman + Miami: no arrojo ningun perfil de Instagram o Facebook propio verificable.
- Un agregador independiente (Birdeye, reviews.birdeye.com/handyman-julian-167602812383697) replica las mismas resenas de Google pero tampoco expone un sitio propio, solo el enlace a Google Maps.

Conclusion: email = null, redes = null. Registrar como `pending_manual` con telefono como unico canal.

## Borrador de email (ingles, idioma principal del negocio)

```
Subject: A free sample website for Handyman Service (Miami, FL)

Hi there,

My name is Michael Vargas, from Merktop. I came across Handyman Service while looking at handyman and remodeling crews in the Miami area, and saw you're at 4.6 stars with 18 reviews on Google, with reviewers praising the custom carpentry work, the flooring and painting jobs, and how reliable and professional the crew is.

I noticed Google doesn't have a dedicated website linked to your listing, so I put together a free sample site using your real photos (kitchen and bathroom remodels, custom woodwork, door installs) and your real reviews:

https://siteforge-demos.odd-forest-9504.workers.dev/handyman-service-miami/

This does not touch your current phone line, your Google listing, or anything you already have running. It's just a preview of what a dedicated website could look like for your business.

If you like it, we can put it on your own domain and handle all the technical setup. If it's not useful, just reply "no" and we won't follow up.

Best,
Michael Vargas
Merktop
```

## dm_message (version corta, maximo 450 caracteres, ingles, sin em-dash)

```
Hi! I'm Michael from Merktop. Found your handyman/remodeling business on Google, 4.6 stars with 18 reviews, people love the carpentry and remodeling work. I noticed you don't have a website, so I built a free sample one with your real photos and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/handyman-service-miami/ Doesn't change anything you're doing. Happy to put it on your own domain, or take it down, no obligation either way.
```

(Conteo de caracteres: 427, dentro del limite de 450.)

## Notas de idioma
Idioma principal del site: ingles (las 5 resenas verbatim recolectadas estan en ingles). El bilingue EN/ES esta incluido en el demo (toggle ES/EN en el nav). El email y el dm_message van en ingles por ser el idioma principal detectado.

## Pendiente
- Sin email publico verificado y sin Instagram/Facebook propio confirmado: el canal de contacto recomendado es llamada directa al (305) 484-4393.
- Revisar la nota de ubicacion arriba (area ampliada de Miami Beach a Miami) antes de aprobar el envio del lote.
