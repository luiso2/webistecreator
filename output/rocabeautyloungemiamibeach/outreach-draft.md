# Outreach draft: Roca Beauty Lounge (rocabeautyloungemiamibeach)

- **Estado**: pending_manual (sin email publico; NO enviar nada sin OK explicito del usuario)
- **Para**: sin email publico confirmado. Contacto disponible por Instagram DM (@rocabeautylounge, bio dice "DM TO BOOK AN APPOINTMENT!") o telefono (305) 409-5772
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-rocabeautyloungemiamibeach-2026-08-02
- **Angulo**: sin website propio (has_own_site=false). Presencia solo en Booksy, Instagram y Google Maps.
- **Idioma**: espanol (bio de Instagram es bilingue con "CALL | LLAME", negocio dominicano Miami Beach)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/rocabeautyloungemiamibeach/

## Busqueda de email (fase 1, punto 7 del pipeline)
- IG `web_profile_info` de @rocabeautylounge: `business_email` vacio (`business_contact_method: CALL`), sin campo de email publico.
- Bio de Instagram: unico link externo es un acortador de Google Maps (`g.co/kgs/DwDVCZD`), sin linktree ni poplme que abrir.
- Pagina de Booksy del negocio (dossier completo, 40 servicios extraidos): el unico email presente en el HTML es `help.us@booksy.com` (soporte de la plataforma, no del negocio); sin mailto propio.
- Facebook (facebook.com/p/Roca-Beauty-Lounge-100063635407522/): redirige a muro de login (HTTP 302), seccion About no accesible sin autenticacion.
- Dominio propio: `rocabeautylounge.com` no resuelve (DNS/gateway rechaza la conexion); `rocabeauty.com` SI resuelve pero es una pagina de parking generica sin relacion con el negocio (redirect a "defaultsite", plantilla de hosting por defecto, sin contenido).
- Conclusion: no hay email publico verificable tras busqueda exhaustiva en las 4 fuentes obligatorias. Contacto recomendado: DM de Instagram o llamada al (305) 409-5772.

## Asunto (si en algun momento se consigue email)
Un website de muestra para Roca Beauty Lounge (ya esta listo)

## Cuerpo

Hola,

Soy Michael, de Merktop, aqui en Miami. Encontre Roca Beauty Lounge por su calificacion de 4.8 estrellas y 71 reseñas en Google, y por el trabajo de color y keratina que comparten en @rocabeautylounge, y me parecio que el salon se merecia un website a la altura.

Hoy las clientas los encuentran solo por Instagram, Booksy y Google Maps, sin un sitio propio. Por eso arme uno de muestra con sus fotos reales, su menu completo (balayage, keratina, manicure, faciales y mas) y sus precios publicados en Booksy:

https://siteforge-demos.odd-forest-9504.workers.dev/rocabeautyloungemiamibeach/

Dos cosas importantes:
- No toca su operacion: las reservas siguen llegando a su Booksy de siempre.
- Esta en espanol e ingles, listo para todas sus clientas.

Si les gusta, lo dejamos en su propio dominio y lo ajustamos juntos. Y si no, lo retiro sin ningun compromiso.

Un saludo,
Michael Vargas
Merktop · merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hola! Soy Michael, de Merktop (Miami). Encontre Roca Beauty Lounge por sus 4.8 estrellas y 71 reseñas en Google, y su trabajo de color en @rocabeautylounge. Como no tienen website propio, les arme uno de muestra con fotos reales, su menu y precios de Booksy: https://siteforge-demos.odd-forest-9504.workers.dev/rocabeautyloungemiamibeach/ No toca sus reservas de Booksy. Si les gusta lo dejamos en su dominio, si no lo retiro sin problema.
