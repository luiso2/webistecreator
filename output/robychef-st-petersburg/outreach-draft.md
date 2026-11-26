# Outreach draft: RobyChef - Personal Chef & Catering (St. Petersburg, FL)

## Resumen
- Negocio: RobyChef - Personal Chef & Catering (Chef Roberta Massetti)
- Nicho: catering / personal chef (cocina italiana a domicilio)
- Ciudad: St. Petersburg, FL (sirve Tampa Bay)
- Google: 5.0 rating, 13 reseñas, boton "Add website" (sin website propio)
- Telefono: +1 727-310-4312
- Instagram: @robychef_tampa (https://www.instagram.com/robychef_tampa/)
- Facebook: https://www.facebook.com/robycheftampa
- Email publico: NO encontrado (ver "Fuentes revisadas" abajo)
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/robychef-st-petersburg/

## Angulo (has_own_site: false)
"Te construimos un sample site gratis": el negocio no tiene website propio (confirmado en Google
Maps y por el dominio robychef.com, que aparece mencionado en perfiles de terceros pero HOY NO
RESUELVE / esta caido). Angulo = mostrarle una demo real, gratis, sin compromiso, construida con
sus propias fotos y reseñas de Google.

## Fuentes revisadas para contacto (busqueda profunda, Fase 1 punto 7)
1. Ficha de Google Maps (gmaps_detail.js en vivo): sin email, solo telefono. Boton "Add website"
   visible, confirma que Google no tiene website registrado para esta ficha.
2. Perfil TakeAChef (chef Roberta Massetti, y variante duplicada "Roby Fanelli"): sin email
   personal, solo formulario de booking de la plataforma y linea de soporte de TakeAChef.
3. Articulo GoSolo / collabs.io (entrevista a Roberta Massetti): menciona "Website:
   https://www.robychef.com/" pero el dominio NO RESUELVE hoy (verificado con curl y WebFetch:
   ENOTFOUND tanto en robychef.com como www.robychef.com). Tratado como dominio caido/expirado,
   no como website propio activo.
4. Facebook (facebook.com/robycheftampa): bloqueado tras muro de login, no se pudo leer la
   seccion About ni un email de contacto.
5. LinkedIn (roberta-massetti-chef): bloqueado por proteccion anti-bot (HTTP 999).
6. Instagram (@robychef_tampa): bloqueado (API privada denegada por el sandbox + WebFetch
   devolvio 429 Too Many Requests). Politica del pipeline: maximo 2 intentos, luego pasar a otras
   fuentes, cosa que se hizo.

Conclusion: no hay email publico verificable hoy. Canal de contacto recomendado: telefono/WhatsApp
+1 727-310-4312 e Instagram @robychef_tampa (DM). outreach: pending_manual.

## dm_message (version corta, EN, maximo 450 caracteres, sin em-dash)

```
Hi Chef Roberta! I found RobyChef on Google (5.0 stars, 13 reviews) and noticed you don't have your own website yet, so I built you a free sample site using your real photos and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/robychef-st-petersburg/
No strings attached, it doesn't touch your bookings. Happy to hand it over on your own domain, or just take it down if it's not useful.
Michael Vargas, Merktop
```

(Conteo de caracteres del mensaje: 365, dentro del limite de 450)

## Borrador completo (email / mensaje largo)

Asunto sugerido: A free sample website for RobyChef

```
Hi Chef Roberta,

My name is Michael Vargas, I work with Merktop, a small studio that builds demo websites for
local businesses in Florida.

I came across RobyChef on Google while looking at highly-rated catering and personal chef
businesses around St. Petersburg and Tampa Bay. You're sitting at a 5.0 rating across 13 reviews,
which is a great sign, and I noticed your Google listing doesn't have a website attached (and the
robychef.com domain that shows up in a couple of older interviews doesn't seem to be live
anymore).

So I went ahead and built you a free sample site using your real photos from Google, your actual
reviews (Patte, Jessica, Tracy, Joshua, Carmen, all five stars), and your bio as the Italian-trained
chef behind RobyChef. You can see it here:

https://siteforge-demos.odd-forest-9504.workers.dev/robychef-st-petersburg/

This doesn't touch how you currently take bookings or run your business at all, it's just a
finished example of what a site for RobyChef could look like. If you like it, I'm happy to help
you put it on your own domain (robychef.com or a new one). If it's not useful to you, just let me
know and I'll take it down, no hard feelings either way.

You can reach me by replying here, or by text/WhatsApp/Instagram DM at the numbers below if that's
easier.

Best,
Michael Vargas
Merktop
Phone/WhatsApp: see below
```

## Canal de envio
Sin email publico verificado: el envio real (si se aprueba) sera por WhatsApp/llamada al
+1 727-310-4312 o por DM a Instagram @robychef_tampa, nunca email automatizado a una direccion no
confirmada. outreach_mode = draft_for_approval (sin aprobacion humana no se envia nada).
