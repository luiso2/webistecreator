# Outreach draft: Real Moving And Storage (real-moving-and-storage)

- **Estado**: `pending_manual` (no se encontro email publico tras busqueda exhaustiva: sin website
  propio, sin Facebook/Instagram localizable, dominio realmovingandstorage.com es un parking de Sedo
  no relacionado)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-real-moving-and-storage-2026-11-04
- **Angulo**: sin website propio (`has_own_site: false`) -> "les construi un sitio de muestra"
- **Idioma**: ingles (reseñas de Google en ingles, rotulacion del remolque en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/real-moving-and-storage/
- **Telefono verificado**: (239) 309-9125 (ficha de Google Maps y visible en la rotulacion del
  remolque en varias fotos propias del negocio)
- **Direccion**: 3507 Lee Blvd, Lehigh Acres, FL 33971 (empresa de mudanzas, atiende a domicilio en
  Fort Myers, Cape Coral y el suroeste de Florida; no es un local de visita)

## Verificacion de rating y resenas
Google Maps en vivo (via Playwright): 4.8 de calificacion, 265 resenas, scrapeado 2026-11-04.
4 resenas verbatim guardadas con nombre real (Julia Mullins Birt, Mary Majka, AJ Gomez, marcelo
palacios), todas mencionan al dueno, Octavio Real, por nombre.

## Chequeo de website propio
- La ficha de Google Maps no trae boton de website ("Add website").
- Se probo `realmovingandstorage.com`: resuelve con HTTP 200, pero el contenido es una pagina de
  parking de Sedo ("This website is for sale!"), sin relacion con el negocio real. Se probaron
  variantes `realmovingstorage.com` (redirect generico) y `realmovingfl.com` (dominio inexistente).
- Conclusion: `has_own_site: false`.

## Busqueda de email
- Sin Facebook ni Instagram localizables para el negocio o para Octavio Real tras busqueda directa.
- Sin email en la ficha de Google Maps ni en el dominio parqueado.
- Conclusion: `outreach: pending_manual`. Contactar por telefono/WhatsApp al (239) 309-9125.

## Subject (referencia)
A free sample website for Real Moving And Storage

## Cuerpo (referencia)

```
Hi,

I came across Real Moving And Storage while looking at movers in the Fort Myers / Lehigh Acres
area. A 4.8 rating with 265 reviews, with customers naming Octavio by name and saying he showed up
himself and took extra care of their furniture, says a lot.

I noticed the business does not have its own website (the only thing online is the Google Maps
listing), so I put together a free sample site, no cost and no obligation:

https://siteforge-demos.odd-forest-9504.workers.dev/real-moving-and-storage/

It uses your real photos, your real rating and real reviews from your customers. It does not touch
your current operation at all, the main button just calls your phone.

If you like the direction, I can hand over the files or help you point your own domain to it. If
it is not for you, no problem, I will take it down.

Happy to adjust colors, photos or text before you decide.

Best,
Michael Vargas
Merktop
```

---

## Version corta para DM / WhatsApp (dm_message)

```
Hi! This is Michael with Merktop. Found Real Moving And Storage, 4.8 rating, 265 Google reviews,
customers naming Octavio for how careful he is with furniture. Built a free sample site with your
real photos and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/real-moving-and-storage/
Does not touch how you take calls today. Like it? I put it on your own domain, no cost. If not, I
take it down, no problem. Michael Vargas, Merktop.
```

(445 caracteres, en ingles por ser el idioma principal del negocio, sin em-dash.)
