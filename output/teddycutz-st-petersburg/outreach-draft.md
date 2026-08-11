dm_message: "Hi! I'm Michael, from Merktop. I saw Teddycutz has a 5.0 rating across 213 reviews on Booksy, so I built you a sample website with your real cuts, prices and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/teddycutz-st-petersburg/ It doesn't touch your Booksy booking at all. If you like it, I can put it on your own domain, if not I'll take it down, no pressure either way."

Subject: A sample website for Teddycutz (it's ready)

Hi there,

I'm Michael, from Merktop. I found Teddycutz on Booksy and a perfect 5.0 rating across 213 reviews caught my eye, so I took a closer look at James's fades, beard work and the custom hair designs.

I noticed you don't have your own website, just your Booksy booking page, so I went ahead and built you a sample one with your real menu, real prices and real reviews:

https://siteforge-demos.odd-forest-9504.workers.dev/teddycutz-st-petersburg/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Booksy, exactly like today.
- It's bilingual (English and Spanish), ready for both sides of your St. Petersburg client base.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you, I'll take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

---

# Research notes (not part of the email)

## Estado
- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email")
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-teddycutz-st-petersburg-2026-08-11
- **Angulo**: sin website propio (ver "Chequeo de website propio")
- **Idioma**: ingles (reseñas de Booksy 100% en ingles, negocio en Florida)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/teddycutz-st-petersburg/
- **Telefono verificado**: ninguno publico encontrado (Booksy no lo expone; sin listing con telefono confirmado)
- **Canal disponible**: sin email ni telefono ni Instagram verificados. Registrado como `outreach: pending_manual`. El unico canal de contacto confirmado y activo es Booksy (mensajeria interna de la plataforma).

## Chequeo de website propio (CRITICO)
- Se probaron `teddycutzbarber.com`, `teddycutzstpete.com`, `teddycutzstpetersburg.com`, `teddycutzbarbershop.com`: los cuatro fallan resolucion DNS (curl exit 56 / sin respuesta).
- **Se encontro `teddycutz.com` (dominio real y activo)**, pero verificado a fondo (WebFetch + curl del HTML) resulto ser OTRO negocio: una barberia "Celebrity Cuts / Teddy Cutz" en **Rochester, NY**, propiedad de un barbero distinto que dice haberse certificado como Master Barber en 1997 y abrio su primer local en Portland Avenue en 1999. Sin ninguna mencion a St. Petersburg, Florida ni a James Johnson. Coincidencia de nombre de marca, negocio distinto.
- Conclusion: `has_own_site: false` para Teddycutz (St. Petersburg, FL, Booksy id 192874). No se construyo nada para el Teddycutz de Rochester, NY (fuera de alcance, negocio distinto).

## Chequeo de Instagram (hallazgo importante)
- Booksy lista `https://www.instagram.com/beardabarber/` como el Instagram oficial del negocio (`data-test="social-instagram"` y `sameAs` de su JSON-LD).
- Verificado directamente contra el endpoint publico de Instagram (`web_profile_info`): la cuenta **@beardabarber** pertenece a un barbero distinto, dueño de "Broadway Barbers" en **1316 South Broadway Suite B**, con telefono de area code 805 (California), sin ninguna relacion con St. Petersburg, FL ni con Teddycutz.
- Conclusion: el link de Instagram que trae Booksy para este negocio esta desactualizado o es incorrecto (probable caso de handle reciclado/reclamado por otro barbero). **No se uso ese Instagram como fuente de fotos ni como canal de contacto**, y el site construido NO enlaza a esa cuenta en ningun boton (se reemplazaron los CTAs de "Instagram" del esqueleto por CTAs a Booksy y a la direccion real en Google Maps). `ig: null` (no verificado) en el registro.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- Payload/HTML de Booksy: sin campo de email visible.
- No hay Instagram propio verificado del negocio (ver arriba), por lo que no se pudo revisar bio/external_url/linktree de una cuenta real.
- No se encontro pagina de Facebook propia del negocio en los resultados de busqueda (solo aparecen otras barberias de la zona con nombres similares: Ted's Barber Shop, Against The Grain, Creative Kutz).
- Yahoo Local lista "Teddy Cutz Barber Salon LLC" en una direccion distinta (3153 Central Ave #D, St Petersburg) sin telefono ni email ni website.
- No se encontro ficha de Yelp para este negocio especifico.
- Conclusion: sin email publico verificable tras busqueda exhaustiva. `email: null`.

## Fotos (research fase 1, punto 2)
- El dossier de Booksy inicial trajo 16 "fotos" pero 13 de ellas eran miniaturas de reseñas de 100x100px (inservibles). Se recuperaron las versiones a resolucion completa quitando el parametro `?size=` de las URLs de cloudfront (los review_photos de Booksy se sirven completos si se pide la URL sin ese query param).
- De las ~15 fotos recuperadas a resolucion completa, la mayoria eran selfies de clientes, fotos con overlays de texto/emoji (Snapchat/IG stories) o fotos sin relacion clara con un corte terminado: se descartaron por curaduria visual.
- Se intento complementar con Instagram (@beardabarber vía ig_photos.py con servicio Playwright/Railway, y fallback Playwright local): 0 fotos encontradas por el servicio. Dado que ademas se confirmo que esa cuenta NO es del negocio (ver arriba), no se habria podido usar de todas formas.
- Quedaron 5 fotos reales, verificadas visualmente una por una, sin overlays de texto, sin selfies puras: un barbero cortando un diseño personalizado ("ZACH") tallado en el cabello de un cliente, un fade limpio visto desde arriba, un cliente con dreadlocks teñidos frente a un local en la calle, un niño con corte limpio (buzz cut), y las herramientas (maquinas, navajas) sobre la estacion de trabajo. Cumple el minimo de 5 fotos buenas requerido para continuar a build.

## Servicios y precios (Booksy, dossier verificado)
Men cut and design $75/45min, Haircut and Beard $40/45min, Just haircut no beard $30, Women cuts and design $65/45min, Women's Haircut $25/45min, Teen Haircut $20/30min, Kids Haircut $20/30min, Kids cuts and design $30, Razor shave $30, Beard trim $15/20min, Line Up $15/20min, Edge razor $15/20min, Designs $30. (13 servicios totales; 4 destacados como cards, el resto resumido en la nota de precios).
