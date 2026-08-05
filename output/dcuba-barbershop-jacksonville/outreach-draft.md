# Outreach draft: D'Cuba Barbershop (dcuba-barbershop-jacksonville)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email" abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-dcuba-barbershop-jacksonville-2026-08-05
- **Angulo**: sin website propio (ver seccion "Chequeo de website propio")
- **Idioma**: ingles (idioma principal del negocio, data.json language: "en")
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/dcuba-barbershop-jacksonville/
- **Telefono verificado**: (904) 910-7618
- **Canal disponible**: sin email publico confirmado. Registrado como `outreach: pending_manual` con telefono (904) 910-7618 y su Instagram @dcuba_barbershop para DM/WhatsApp/llamada manual.

## Chequeo de telefono (data.json lo traia null)
- `data.json` (extraido de Booksy) traia `"phone": null`.
- Busqueda "D'Cuba Barbershop" Jacksonville FL phone: TikTok oficial (@dcuba.barbershop) publica en su propio video "D'Cuba Barbershop 📲 9049107618 📍11757 Beach Blvd", mismo numero y misma direccion que `data.json`.
- Confirmado independientemente en un post propio de su pagina de Facebook (facebook.com/d.cuba.barber): "D'Cuba Barbershop 📲 (904) 910-7618 DCubabarber.booksy.com".
- Yahoo Local y el directorio Atly listan el mismo numero para la misma direccion (11757-10 Beach Blvd, Jacksonville, FL 32246).
- Conclusion: telefono **(904) 910-7618** verificado para ESTE negocio (11757 Beach Blvd #10), via 3 fuentes independientes que coinciden en numero y direccion.
- Nota aparte: existe un mirror de Fresha ("D'Cubabarber / Damian Barber") para una ubicacion DISTINTA (7001-29 Merrill Rd, Jacksonville, 32277), con el mismo numero de telefono. Parece ser una segunda locacion del mismo dueno/marca, pero el negocio que se construyo aqui es el de Beach Blvd (coincide con `data.json`, Booksy id 706709). No se mezclaron datos de ambas ubicaciones.

## Chequeo de website propio
- `website_candidates` en data.json: vacio.
- `same_as` en data.json: solo Facebook (link de share) e Instagram.
- Busqueda "D'Cuba Barbershop" Jacksonville: unicos resultados son Booksy (booking oficial), el mirror de Fresha de la otra locacion, Facebook (facebook.com/d.cuba.barber), Instagram (@dcuba_barbershop), Yelp (dos fichas, una por locacion), Nextdoor, TikTok y el directorio Atly. Ningun dominio propio.
- Conclusion: `has_own_site: false`.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- `data.json`: sin campo de email.
- Bio de Instagram (@dcuba_barbershop, 475 seguidores, 220 posts, via resultados de busqueda): sin linktree ni `external_url` visible que apunte a un email; bio solo menciona horario, DM y el link de Booksy.
- Pagina de Facebook (facebook.com/d.cuba.barber): sus posts publicos muestran telefono y el link de Booksy, sin direccion de correo.
- Fresha (listado de la otra locacion, no oficial de este local): no se encontro campo de email en los resultados de busqueda.
- Yelp (dos fichas): no expone email en los resultados de busqueda.
- Conclusion: sin email publico verificable tras busqueda exhaustiva. `email: null`.

## Subject (para cuando haya un canal de email)
A sample website for D'Cuba Barbershop (it's ready)

## Cuerpo (referencia, para email o como base del DM largo)

Hi there,

I'm Michael, from Merktop. I found D'Cuba Barbershop on Booksy and a 4.9 rating across 108 reviews caught my eye, so I took a closer look at Damian's fades and beard work.

I noticed you don't have your own website, just Booksy, Instagram and Facebook, so I went ahead and built you a sample one with your real menu, real reviews and real photos of your work:

https://siteforge-demos.odd-forest-9504.workers.dev/dcuba-barbershop-jacksonville/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Booksy, exactly like today.
- It's bilingual (English and Spanish), ready for both sides of your Jacksonville client base.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you, I'll take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi! I'm Michael, from Merktop. I saw D'Cuba Barbershop has a 4.9 rating across 108 reviews on Booksy, so I built you a sample website with your real cuts, prices and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/dcuba-barbershop-jacksonville/ It doesn't touch your Booksy booking at all. If you like it, I can put it on your own domain, if not I will take it down, no pressure either way.
