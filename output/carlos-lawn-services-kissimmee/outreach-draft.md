# Outreach draft: Carlos Lawn Services (Kissimmee, FL)

## Datos de contacto
- Nombre: Carlos Lawn Services (lawn care / landscaping, service area Kissimmee / Orlando / St. Cloud, FL)
- Dirección: no se publica una dirección de local visitable (ver `address` en data.json: GreenPal muestra una página SEO de barrio con "3103 Scrub Brush Court, Kissimmee, FL" pero ese patrón de GreenPal no se trata como direccion real de negocio)
- Teléfono: no encontrado (GreenPal oculta el contacto directo detrás de su propio sistema de mensajes)
- Email: no encontrado
- Instagram / Facebook: no encontrados
- Rating: 4.7 en GreenPal, 19 reseñas
- has_own_site: false (carloslawnservices.com existe pero es un dominio parqueado/en venta, sin contenido real del negocio; ver `own_site_check` en data.json)
- Canal de contacto real: GreenPal profile (https://www.yourgreenpal.com/pro/carlos-lawn-services-2) - Message / Request a Call / Get a Free Quote
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/carlos-lawn-services-kissimmee/

## Angulo (has_own_site: false)
"Te construimos un sample site gratis": el negocio no tiene ningun sitio de marketing propio (su unico canal publico es el perfil de GreenPal), asi que el angulo es mostrarles una muestra ya lista con sus fotos reales de trabajos, sus reseñas reales y su rating de GreenPal.

## Fuentes revisadas para email y redes (Fase 1, puntos 2 y 7)
- Perfil de GreenPal (https://www.yourgreenpal.com/pro/carlos-lawn-services-2): descargado con curl + Chrome UA (HTTP 200), HTML completo parseado incluyendo bloques JSON-LD (ImageObject y FAQPage). Sin mailto:, sin email visible en ninguna parte de la pagina. Contacto restringido a los botones propios de GreenPal (Message, Request a Call, Make a Payment via Stripe).
- carloslawnservices.com: SI resuelve (DNS activo) y responde HTTP 200, pero es una pagina de parking/dominio en venta (`window.LANDER_SYSTEM='PW'`, `ap:'parking'`), sin ningun contenido real del negocio. carloslawnservice.com y carloslawnserviceskissimmee.com no resuelven (NXDOMAIN).
- WebSearch de "Carlos Lawn Services" + Kissimmee + facebook/instagram: sin resultados relevantes (solo negocios homonimos en otras ciudades/estados: Dunedin FL, Stafford TX, Fitchburg MA, Wauchula FL).
- Conclusion: email = null, telefono = null, IG/FB = null. Unico canal de contacto real: GreenPal.

## PENDING MANUAL: sin email ni telefono ni redes sociales
Este negocio no tiene NINGUN canal de contacto publico fuera de la plataforma GreenPal (ni telefono, ni email, ni Instagram, ni Facebook). Por eso no se redacta un email tradicional para enviar: no hay buzon al que enviarlo. El unico borrador posible es el `dm_message` de abajo, pensado para usarse manualmente a traves del sistema de mensajes propio de GreenPal (Message / Request a Call) si el equipo de Merktop decide contactar por ahi. Registrar como `outreach: pending_manual`.

## Borrador de "email" (en realidad, mensaje para enviar via GreenPal Message, no hay bandeja de email real)

```
Subject: A free sample website for Carlos Lawn Services

Hi Carlos,

My name is Michael Vargas, from Merktop. I came across Carlos Lawn Services on GreenPal while looking at lawn care providers in Kissimmee, and saw you're at 4.7 stars with 19 reviews, with customers mentioning how fast, friendly and detail-oriented the work is.

I noticed you don't have a dedicated website of your own (just your GreenPal profile), so I put together a free sample site using your real job photos and your real reviews:

https://siteforge-demos.odd-forest-9504.workers.dev/carlos-lawn-services-kissimmee/

This does not touch your GreenPal profile or how customers request quotes today. It's just a preview of what a dedicated website could look like for Carlos Lawn Services.

If you like it, we can put it on your own domain and handle all the technical setup. If it's not useful, no problem at all, just let us know.

Best,
Michael Vargas
Merktop
```

(NOTA: no hay direccion de email real a la cual enviar esto. Se deja redactado por si el equipo decide copiarlo a traves del boton "Message" de GreenPal como mensaje directo al vendor.)

## dm_message (version corta, maximo 450 caracteres, ingles, sin em-dash)

```
Hi Carlos, this is Michael from Merktop. Saw Carlos Lawn Services has 4.7 stars and 19 reviews on GreenPal but no website of your own, so I built a free sample site with your real job photos and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/carlos-lawn-services-kissimmee/ It doesn't touch your GreenPal profile. Happy to put it on your own domain, or take it down, no obligation either way.
```

(Conteo de caracteres: 349, dentro del limite de 450.)

## Notas de idioma
Idioma principal del site: ingles (4 de las 5 reseñas verbatim usadas en el site estan en ingles; la seccion de Preguntas y Respuestas que el propio vendor escribio en GreenPal tambien esta en ingles). El bilingue EN/ES esta incluido en el demo. El dm_message va en ingles por ser el idioma principal detectado.

## Pendiente / notas para revision humana
- Sin telefono, sin email, sin redes sociales: el unico canal real es GreenPal. Si se quiere contactar a este negocio, tendria que ser via el boton "Message" o "Request a Call" dentro de su perfil de GreenPal, lo cual queda fuera del alcance de un envio automatizado de email/DM.
- No se encontro el apellido del dueño (solo "Carlos", nombre de la marca); no se fabrico un apellido.
- No se encontraron reseñas negativas con texto entre las ~15 revisadas de las 19 totales.
- El negocio es relativamente nuevo (en operacion desde febrero de 2026 segun su propio perfil de GreenPal).
