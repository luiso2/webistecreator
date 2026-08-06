# Outreach draft: Pelusa's Pet Grooming (pelusas-pet-grooming-gainesville)

- **Estado**: pending_manual (NO enviar email, no se encontro email publico)
- **Para**: sin email publico verificado (ver seccion abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-pelusas-pet-grooming-gainesville-2026-08-06
- **Angulo**: sin website propio (`has_own_site: false`)
- **Idioma**: ingles (todas las reseñas encontradas, en Yelp y Nextdoor, estan en ingles; sin evidencia de contenido en español en ninguna fuente)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/pelusas-pet-grooming-gainesville/
- **Telefono verificado**: (754) 366-3687 (confirmado identico en Yelp, Nextdoor, thegoodypet.com, dogdog.org, wheree.com, carefurpets.net, whodoyou.com)
- **Facebook**: https://www.facebook.com/profile.php?id=362328610511805 ("Pelusa's Pet Grooming | Facebook", pagina de reseñas titulada "Pelusa's Pet Grooming - Gainesville, FL - Pet Groomer"); contenido no se pudo renderizar en esta sesion (bloqueo de JS/login wall), el link se incluye en el site pero no se citan cifras de esa pagina que no se pudieron verificar de primera mano (ej. conteo de seguidores).
- **Instagram**: NO confirmado (ver seccion abajo). No se uso en el site ni en el registro.
- **Canal disponible para outreach**: llamada o SMS al (754) 366-3687. Sin email, este borrador queda como referencia para el envio manual, no se manda.

## Verificacion de rating
- **Fuente principal: Yelp.** Titulo de pagina obtenido por busqueda (texto real del `<title>`, no resumen de IA): "PELUSA'S PET GROOMING - Updated June 2026 - 15 Reviews - 3737 W University, Gainesville, Florida - Pet Groomers - Phone Number - Yelp". Un fetch directo de `thegoodypet.com` (agregador que cita su fuente explicitamente) confirma: "5.0 stars on Yelp (15 reviews)". Otro resultado de busqueda independiente confirmo "4 photos and 15 reviews on their Yelp page, listing currently marked as unclaimed".
- **Yelp.com directo bloqueado**: `www.yelp.com/biz/pelusas-pet-grooming-gainesville` devolvio HTTP 403 en todos los intentos (fetch y curl), tanto en esta sesion como es tipico para Yelp sin API key. Por eso el rating se cita como **"5.0 · 15 reviews on Yelp"**, explicitamente atribuido a Yelp, en vez de presentarlo como verificado en vivo.
- **Google Maps: NO se pudo verificar directamente.** `google.com/maps?cid=10758724800295544355` y la busqueda de Google devuelven solo el shell de JavaScript sin datos server-side renderizados (WebFetch no ejecuta JS). Un agregador (`dogdog.org`) mostraba "146 people rated this" sin atribucion visible a ninguna plataforma (ni "Google" ni "Yelp" aparecen cerca de esa cifra): se descarto por no poder confirmarse la fuente, no se uso en el site ni en el registro.
- **Discrepancia menor**: un resumen de busqueda temprano (no el titulo crudo de la pagina) menciono "13 reviews" en vez de 15; el titulo de pagina mas reciente y repetido en multiples busquedas dice "Updated June 2026 - 15 Reviews", que es el numero usado (mas reciente y consistente en 3+ resultados independientes).
- **Reseñas verbatim reales** (8 en total, con nombre/iniciales, fecha aproximada donde disponible, y plataforma):
  - Jerry F. (Yelp via Yahoo Local): "Always do a great job on our two spaniels. We wouldn't go anywhere else."
  - Lupe M. (Yelp via Yahoo Local): "Very friendly staff, reasonable prices and my dogs look great"
  - Tess H. (Yelp via Yahoo Local): "Best groomer in town! I always trust my Charlie with them."
  - Jimena D. (Yelp via Yahoo Local): "they work with what you need and prefer...my puppy is in great hands"
  - S.J. (Nextdoor, 13 mayo): "I just wish they would be open more days than what they are now. But, they are incredible."
  - Y.B. (Nextdoor, 16 abril): "Pelusa pet Grooming! (754) 366-3687 Inexpensive and family run!!"
  - K.W. (Nextdoor, 29 oct): "Pelusa does a great job at the best price I have found in town."
  - Usadas en el site (3, grid principal): Jerry F., Tess H. y K.W.

## Chequeo de website propio
- Un agregador (`thegoodypet.com`) lista "Website: http://pelusapet.webs.com/". Se probo directamente: `curl` y `WebFetch` devuelven **fallo de resolucion DNS** (`ENOTFOUND pelusapet.webs.com` / `Could not resolve host`), confirmado dos veces por metodos distintos. Es un dominio de Webs.com (plataforma gratuita de paginas web, en gran parte descontinuada) que ya no resuelve: no es un sitio propio activo, y aunque lo fuera, un subdominio de plataforma tipo `*.webs.com` tampoco cuenta como "website propio" segun el criterio del pipeline (equivalente a square.site o glossgenius.com).
- **IMPORTANTE, disambiguacion ya prevista en el brief**: el dominio `pelusapetgrooming.com` (sin apostrofe/plural distinto) pertenece a un negocio DIFERENTE y no relacionado: un servicio de grooming movil en el sur de Charlotte, NC ("Pelusa Pet Grooming | We bring the grooming salon to you!"). Aparece repetidamente en los resultados de busqueda por similitud de nombre. Se verifico que NO es el mismo negocio (ciudad distinta, modelo de negocio distinto: movil vs. local fisico) y no se uso ningun dato de ese dominio.
- No se encontro ningun otro dominio propio activo, ni pagina de Facebook con dominio propio en el link de "Website".
- Conclusion: `has_own_site: false`.

## Verificacion de Instagram (busqueda exhaustiva, sin resultado confirmado)
- Busqueda directa encontro dos candidatos: `@pelusa.petgrooming` y `@pelusas_pet`.
- `@pelusa.petgrooming`: su bio dice **"We come to your home, so you don't have to!"** y describe un servicio de grooming a domicilio ("in-home pet grooming"). Esto es inconsistente con Pelusa's Pet Grooming Gainesville, que es un local fisico fijo en 3737 W University Ave (confirmado por fotos de Google Maps, Nextdoor y multiples agregadores). Alto riesgo de ser un negocio distinto (posiblemente relacionado al mismo patron de nombre que causa la confusion con `pelusapetgrooming.com` de NC). **Se descarto, no se uso.**
- `@pelusas_pet`: no se pudo verificar su bio. Intentos con WebFetch devolvieron HTTP 429 (rate limit) en 2+ ocasiones; un intento adicional con Playwright local (`scripts/ig_contact.py`) fallo por `ERR_CONNECTION_RESET` (sin salida de red disponible en este entorno para Instagram). Sin biografia verificada, no se puede confirmar que corresponda a este negocio especifico.
- Conclusion: `ig: null`. No se afirma ningun handle de Instagram en el site, en el registro ni en el `dm_message`.

## Verificacion de email (busqueda profunda, sin resultado)
- Ningun agregador (Yelp indirecto via Yahoo Local, Nextdoor, dogdog.org, thegoodypet.com, wheree.com, carefurpets.net, whodoyou.com, bringfido.com) publica un email de contacto.
- Facebook: la pagina no se pudo renderizar (login wall / requiere JS), asi que no se pudo revisar su seccion "About" en busca de email.
- El dominio `pelusapet.webs.com` (ver arriba) no resuelve, asi que tampoco se pudo revisar un posible email `@webs.com` o custom en esa pagina muerta.
- Instagram: sin bio verificada (ver arriba), no se pudo revisar `business_email` ni link externo.
- Sunbiz (registro de "Pelusa's Pet Grooming, Inc.", activo desde 2009): solo expone agente registrado y direccion legal, no email de contacto al publico.
- Conclusion: sin email publico encontrado. `outreach: pending_manual`, contactar por llamada o SMS al (754) 366-3687.

## Fotos: origen y verificacion
6 fotos reales verificadas (minimo del pipeline: 5), todas confirmadas con `file` como JPEG validas >15KB antes de redimensionar, y revisadas visualmente una por una:
- `pg-goldendoodle.jpg`: foto de Google Maps (`lh5.googleusercontent.com`, listado real de la ficha del negocio via `place_id:ChIJEwpSOlCj6IgRIybNJTSrTpU`) — goldendoodle recien peinado con panuelo de trebol, en la mesa de trabajo del salon.
- `pg-table.jpg`: foto de Google Maps — perro pequeño recien peinado en la mesa de trabajo, interior del salon visible.
- `pg-storefront.jpg`: foto de galeria de negocio de Nextdoor (`us1-photo.nextdoor.com`) — fachada real del local con el letrero "PELUSA'S / PET GROOMING" visible.
- `pg-freshcut.jpg`, `pg-towel.jpg`, `pg-pickup.jpg`: fotos de reseñas de Yelp (via el CDN de Yahoo Local, `s.yimg.com`) adjuntas a reseñas verificadas del negocio — mascotas recien peinadas o bañadas.
- **Descartadas**: una foto de reseña de Yelp que era una selfie de una clienta (regla dura: nunca selfies/retratos en la galeria). Cinco fotos adicionales de Google Maps (`lh5.googleusercontent.com`) que mostraban mascotas en entornos claramente NO relacionados con el local (sendero de montana, patio trasero, piso de una casa, una jaula de un color de pared inconsistente con el salon real): se descartaron por no poder confirmarse que fueran tomadas en o para este negocio especifico, evitando el riesgo de usar fotos de otro negocio o de otra ubicacion.
- Ningun Instagram verificado (ver arriba), asi que no hubo fuente de IG para fotos.

## Servicios y precios
- Ningun agregador publica una lista de precios exacta para este negocio (ni Yelp, ni Nextdoor, ni ningun directorio). El texto descriptivo de servicios (baño, corte, uñas, oidos, de-shedding) aparece de forma casi identica en varios directorios (dogdog.org, wheree.com, care.com), lo cual sugiere boilerplate generico de directorio mas que copy propio del negocio, pero son categorias de servicio estandar y verosimiles para cualquier peluqueria canina, no precios ni especialidades inventadas.
- Siguiendo la variante adaptada (PIPELINE fase 3.5 / FORGE-BRIEF 0.b): las 4 tarjetas de servicio en el site NO llevan precio, llevan la nota "Se cotiza por telefono" / "Quoted by phone" y CTA directo a `tel:+17543663687`.

## Subject (referencia, para cuando se use email si aparece)
A sample website for Pelusa's Pet Grooming (it's ready)

## Cuerpo (referencia)

Hi Martha and Enrique,

I'm Michael, from Merktop. I found Pelusa's Pet Grooming while looking at pet groomers in
Gainesville, your 5.0 rating on Yelp caught my eye, and I took a closer look at your work.

I noticed you don't have your own website, just your phone number and word of mouth, so I went
ahead and built you a sample one with your real reviews and photos:

https://siteforge-demos.odd-forest-9504.workers.dev/pelusas-pet-grooming-gainesville/

Two things worth knowing:
- It doesn't touch how you run things at all. Every appointment still starts with a phone call to
  (754) 366-3687, exactly like today.
- It's bilingual (English and Spanish), so more of Gainesville can read it.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you,
I'll take it down, no hard feelings either way. Feel free to call or text me back at this same
number if that's easier.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi! I'm Michael from Merktop. I found Pelusa's Pet Grooming, saw your 5.0 rating on Yelp, and
built you a sample website with your real reviews and photos:
https://siteforge-demos.odd-forest-9504.workers.dev/pelusas-pet-grooming-gainesville/ It doesn't
touch how you run things, every visit still starts with a call. Like it, keep it on your domain.
If not, I'll take it down, no pressure.
