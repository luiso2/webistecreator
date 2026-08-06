# Outreach draft: Doc Grace Aesthetics (doc-grace-aesthetics)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico encontrado (ver seccion abajo) -> `outreach: pending_manual`
- **Canal recomendado**: DM de Instagram (@doc.graceaesthetics) o llamada/WhatsApp al (305) 978-9545
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-doc-grace-aesthetics-2026-08-06
- **Angulo**: sin website propio (`has_own_site: false`, ver seccion abajo)
- **Idioma**: español (idioma principal del negocio: captions de IG, reseñas bilingues con mayoria en español, nombre de la dueña "Dra. Grace" / "Grechy")
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/doc-grace-aesthetics/
- **Telefono verificado**: (305) 978-9545

## Verificacion de rating (Google, via Birdeye que lo agrega)
- Birdeye (reviews.birdeye.com/doc-grace-aesthetics-169816754023755) muestra JSON-LD con
  `aggregateRating: { ratingValue: 5, reviewCount: 91 }`, telephone "(305) 978-9545" (coincide con
  el numero conocido) y horario 9:00-18:00 los 7 dias, coherente con el mismo dato en Fresha.
- Se confirmaron por separado los nombres y textos parciales de las reseñas ya conocidas (Nina
  Vidal, M A, German Ospina, M R, Jessica Acosta) en la misma pagina.
- Conclusion: 5.0 con 91 reseñas verificado de forma independiente (>= umbral). Coincide con el
  dato entregado.

## Direccion y datos del negocio
- Fresha (fresha.com/lvp/doc-grace-aesthetics-southwest-137th-avenue-miami-BKnr3K, `__NEXT_DATA__`)
  confirma: nombre "Doc Grace Aesthetics", direccion "11285 SW 211 St #305, Miami, FL 33189",
  telefono "(305) 978-9545", horario 9:00 AM - 6:00 PM los 7 dias, `websiteUrl: ""` (vacio, sin
  sitio propio registrado).
- Una foto promocional real del feed de Instagram (flyer de "Vida HealthCare", el consultorio
  donde Grace atiende) confirma la misma direccion impresa: "11285 SW 211 St Cutler Bay, FL 33189
  Suite 305".
- El listado de Fresha es un perfil "lite" (no tiene menu de servicios con precios ni booking
  online real, solo "Call to book"): por eso el sitio usa el telefono como canal de reserva
  principal, no un link de checkout.

## Chequeo de website propio
- Fresha: `websiteUrl` vacio.
- Directorios (medspaflorida.com, atly.com) no listan sitio propio, solo el perfil del directorio.
- Dominios obvios probados (docgraceaesthetics.com, docgraceaesthetics.net, docgrace.com): no
  resuelven.
- Conclusion: `has_own_site: false`.

## Verificacion de email
- Se revisaron: endpoint web_profile_info de IG (no disponible, IG devolvio error de esquema
  obsoleto en el intento directo), pagina de Instagram directa (bloqueada con muro de login),
  payload de Fresha (sin campo email en este perfil lite), seccion About de Facebook (bloqueada sin
  sesion), directorio medspaflorida.com (sin datos de contacto reales, solo texto placeholder).
- No se encontro ningun email publico tras la busqueda profunda. Se marca `outreach: pending_manual`
  con telefono e Instagram como canales de contacto.

## Fotos: origen y curaduria
- 12 fotos publicas reales descargadas del feed de Instagram (@doc.graceaesthetics, via el
  servicio de fotos IG). Se revisaron una por una: se descartaron capturas con texto/caption
  encima (flyers promocionales, antes/despues con rotulos "Before/After"), selfies personales sin
  relacion con el consultorio (viaje, gimnasio) y una captura de un noticiero.
- De las fotos aprovechables se recortaron las bandas de texto/flyer para dejar solo la fotografia
  real (procedimiento de bótox, foto con clienta, ambiente del consultorio), sin agregar ni
  inventar contenido. 6 fotos reales quedaron en el site final: hero, 2 en la seccion "Nosotros",
  avatar de la Dra. Grace, y 2 en la galeria.

## Subject
Un sitio de muestra para Doc Grace Aesthetics (ya esta listo)

## Cuerpo (referencia, para DM o si se consigue email despues)

Hola Dra. Grace,

Soy Michael, de Merktop. Encontre Doc Grace Aesthetics buscando consultorios de estetica en
Cutler Bay, y su calificacion de 5.0 con 91 reseñas en Google me llamo la atencion.

Vi que no tienen un sitio web propio, asi que les arme uno de muestra con sus datos reales, fotos
del consultorio y las reseñas de sus clientas:

https://siteforge-demos.odd-forest-9504.workers.dev/doc-grace-aesthetics/

Dos cosas que vale la pena saber:
- No toca su operacion para nada. Las citas se siguen agendando igual, por telefono, como hasta
  ahora.
- Es bilingue (español e ingles), para que lo puedan compartir con toda su clientela.

Si les gusta, lo puedo dejar en su propio dominio y lo ajustamos juntos. Si no es para ustedes, lo
retiro sin problema, sin compromiso de ningun lado.

Saludos,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hola! Soy Michael de Merktop. Vi que Doc Grace Aesthetics tiene 5.0 en Google con 91 reseñas y no
tienen sitio web propio, asi que les arme uno de muestra con sus datos y fotos reales:
https://siteforge-demos.odd-forest-9504.workers.dev/doc-grace-aesthetics/ No toca su forma de
agendar citas. Si les gusta lo dejamos en su dominio, si no lo retiro sin compromiso.
