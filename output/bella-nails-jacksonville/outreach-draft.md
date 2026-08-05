# Outreach draft: Bella Nails (bella-nails-jacksonville)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email" abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-bella-nails-jacksonville-2026-08-05
- **Angulo**: sin website propio (dominios candidatos probados, ver seccion "Chequeo de website propio")
- **Idioma**: español (idioma principal del negocio, reseñas mayormente en español)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/bella-nails-jacksonville/
- **Canal disponible**: sin email ni telefono publico confirmados para ESTE negocio. Registrado como `outreach: pending_manual` con su Instagram @bella_nailsjax para DM manual.

## Chequeo de website propio
- `website_candidates` en data.json (extraido del dossier de Booksy): vacio.
- Probados via curl/DNS: `bellanailsjax.com`, `bellanailsjacksonville.com`, `bella-nailsjax.com`, `bellanailsbeach.com`: ninguno resuelve (sin DNS).
- Busquedas web de "Bella Nails" + Jacksonville devuelven MULTIPLES negocios con nombre similar pero en OTRAS direcciones, todos descartados por no coincidir con 8595 Beach Blvd Building 320 Suite 117, 32216:
  - Bella Nail Salon, 13475 Atlantic Blvd (telefono (904) 647-6550, email Bellanailsalon@ymail.com, IG @bellanailsalon_): negocio distinto.
  - Bella & Me Nails, 8206 Philips Hwy / bellaandmenailsjacksonville.com: negocio distinto (tiene website propio, pero no es este negocio).
  - Bella Diva Hair Nails and Spa, 7643 Gate Pkwy: negocio distinto.
- Conclusion: `has_own_site: false`.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- data.json (dossier de Booksy): sin campo de email, `phone: null`.
- Pagina de Booksy (HTML crudo, curl, JSON-LD embebido): confirma direccion "8595 Beach Blvd, Building 320 Suite 117, Jacksonville, 32216" pero sin campo `telephone` ni email en el payload.
- Instagram (@bella_nailsjax): `web_profile_info` y WebFetch directo devolvieron HTTP 429 (rate limit) en los intentos realizados; no se pudo leer bio/external_url/business_email.
- Facebook (`same_as` en data.json, link de share `facebook.com/share/1AmuKxmTN6`): el link de share redirige a la pantalla de login de Facebook sin sesion iniciada, no expone About/telefono/email publicamente sin autenticacion.
- Hallazgo relevante (descartado): busquedas por el nombre de la tecnica "Rocio Ocana" (mencionada en las reseñas y en `staff` de data.json) devuelven referencias a un listado antiguo del mismo Booksy ID dentro de "Fatima Beauty Center Salon", 3505 Southside Blvd Unit 10, Jacksonville 32216, con telefono (904) 641-0093. Ese numero pertenece al salon anfitrion ("Fatima Beauty Center Salon", nombre de negocio distinto) en una direccion vieja que YA NO aparece en el listado actual de Booksy (que muestra 8595 Beach Blvd, Building 320 Suite 117). Al no coincidir ni con el nombre "Bella Nails" ni con la direccion actual, ese telefono NO se usa aqui: no cumple el criterio de coincidencia exacta pedido.
- Conclusion: sin telefono ni email publico verificable que coincida con la direccion actual o el handle @bella_nailsjax. `phone: null`, `email: null`.

## Subject (para cuando haya un canal de email)
Un sitio de muestra para Bella Nails (ya esta listo)

## Cuerpo (referencia, para email o como base del DM largo)

Hola,

Soy Michael, de Merktop. Encontre Bella Nails en Booksy y me llamo la atencion su calificacion de 5.0 con 72 reseñas, asi que revise su menu y su trabajo con mas detalle.

Vi que no tienen un sitio web propio, solo Booksy e Instagram, asi que les arme uno de muestra con su menu real, precios reales y reseñas reales:

https://siteforge-demos.odd-forest-9504.workers.dev/bella-nails-jacksonville/

Dos cosas que vale la pena saber:
- No toca su sistema de reservas para nada. Cada cita sigue yendo directo a su Booksy, exactamente como hoy.
- Es bilingue (español e ingles), listo para toda su clientela en Jacksonville.

Si les gusta, lo puedo poner en su propio dominio y lo ajustamos juntos. Si no es para ustedes, lo bajo sin problema, sin compromiso de ningun lado.

Saludos,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hola! Soy Michael, de Merktop. Vi que Bella Nails tiene 5.0 con 72 reseñas en Booksy, así que les armé un sitio de muestra con su menú, precios y reseñas reales: https://siteforge-demos.odd-forest-9504.workers.dev/bella-nails-jacksonville/ No toca su sistema de reservas de Booksy, sigue funcionando igual. Si les gusta, lo dejo en su propio dominio; si no, lo bajo sin problema.
