# Outreach draft: DIVAH Beauty (divahbeauty)

- **Estado**: DRAFT ONLY, pending_manual (sin email publico; NO enviar nada sin OK explicito del usuario; PROHIBIDO contactar al negocio desde esta sesion)
- **Para**: sin email publico confirmado. Contacto disponible por Instagram DM (@divahbeauty_)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-divahbeauty-2026-07-23
- **Angulo**: sin website propio (has_own_site=false). divahbeauty.com existe pero es un dominio parqueado/lander sin contenido real (el script en la pagina solo redirige a `/lander`, sin marca ni informacion del negocio); Booksy tampoco lista un website.
- **Idioma**: espanol (la mayoria de las reseñas de Booksy estan en espanol, incluyendo las 3 reseñas con nombre)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/divahbeauty/

## Busqueda de email y telefono (fase 1, punto 7 del pipeline)

- Booksy (dossier `booksy_dossier.py`): `phone: null`, sin mailto visible en la pagina.
- Instagram `@divahbeauty_`: `ig_contact.py` con Playwright (2 intentos, limite del pipeline) fallo ambas veces por error de red (`ERR_CONNECTION_RESET`) al cargar instagram.com; no se pudo leer la bio.
- Busqueda web dirigida ("DIVAH Beauty" Miami lashes brows contact) solo devolvio resultados de un negocio distinto y no relacionado ("Diva Beauty SPA Lashes & Brows", North Miami Beach, telefono (786) 246-4376): se descarto explicitamente para NO contaminar el registro con datos de otro negocio.
- Segunda busqueda ("divahbeauty_" instagram Sweetwater / 33174) tampoco encontro el perfil ni datos de contacto adicionales.
- Conclusion: no hay email ni telefono publico verificable para DIVAH Beauty. Contacto recomendado: DM de Instagram.

## Asunto (si en algun momento se consigue email)
Un website de muestra para DIVAH Beauty (ya esta listo)

## Cuerpo

Hola,

Soy Michael, de Merktop, aqui en Miami. Vi el perfil de DIVAH Beauty en Booksy, con 5.0 de calificacion perfecta en 20 reseñas, y el trabajo de Diana en pestañas y cejas en @divahbeauty_, y me parecio que el estudio se merecia un website a la altura.

Hoy las clientas encuentran DIVAH Beauty solo por Instagram y Booksy, sin un sitio propio (el dominio divahbeauty.com esta parqueado, sin contenido real). Por eso arme uno de muestra, con las fotos reales del estudio, el menu completo (extensiones clasicas, hibridas, volumen 5D, laminado de cejas) y los precios reales:

https://siteforge-demos.odd-forest-9504.workers.dev/divahbeauty/

Dos cosas importantes:
- No toca la operacion: las reservas siguen llegando al Booksy de siempre.
- Esta en español e ingles, listo para las clientas de Sweetwater y Miami.

Si les gusta, lo dejamos en su propio dominio y lo ajustamos juntos. Y si no, lo retiro sin ningun compromiso.

Un saludo,
Michael Vargas
Merktop · merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hola! Soy Michael, de Merktop (Miami). Vi DIVAH Beauty en Booksy, 5.0 perfecto con 20 reseñas, y el trabajo de Diana en @divahbeauty_. Como no tienen website propio, les arme uno de muestra con fotos reales, el menu completo y los precios reales: https://siteforge-demos.odd-forest-9504.workers.dev/divahbeauty/ No toca las reservas de Booksy. Si les gusta lo dejamos en su propio dominio, si no lo retiro sin problema.
