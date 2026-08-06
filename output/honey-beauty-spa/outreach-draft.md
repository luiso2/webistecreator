# Outreach draft: Honey Beauty Spa (honey-beauty-spa)

- **Estado**: `pending_manual` (sin email publico verificado de forma independiente esta sesion, ver abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-honey-beauty-spa-2026-08-06
- **Angulo**: sin website propio (`has_own_site: false`, ver seccion abajo)
- **Idioma**: espanol (idioma principal del negocio: bio de Instagram, descripcion en Fresha y mayoria de reseñas en espanol)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/honey-beauty-spa/
- **Telefono verificado**: (305) 456-3183
- **WhatsApp verificado**: https://wa.link/eucnn0 (resuelve a +1 786-669-4541)
- **Canal disponible**: sin email publico confirmado de forma independiente -> WhatsApp o DM de Instagram (@honey.beautyspa)

## Verificacion de datos (research fase 1)

- **Fuente principal**: pagina propia de reservas en Fresha (`fresha.com/a/honey-beauty-spa-miami-ee-uu-8150-southwest-8th-street-hgan6m6r`),
  leida directo desde su JSON-LD y el payload `__NEXT_DATA__` de la pagina (dato de primera mano, no un
  agregador de terceros).
- **Nombre**: "Honey Beauty Spa" (coincide en Fresha, Instagram `full_name`, y registro de
  Sunbiz.org: HONEY BEAUTY SPA, LLC, documento L21000472881, activa, direccion principal
  8150 SW 8 ST STE 216 MIAMI, FL 33144).
- **Direccion**: 8150 SW 8th St, Suite 216, Miami, FL 33144 (coincide en Fresha, Sunbiz y la bio de
  Instagram). Zona de servicio "Westchester" segun el propio campo `servicingAreas` de Fresha.
- **Telefono**: +1 305-456-3183, confirmado en el JSON-LD de Fresha (`telephone`) y coincide con el
  numero pedido en el research previo.
- **Rating y reseñas**: **5.0 con 245 reseñas**, verificado directo en el `AggregateRating` del
  JSON-LD de Fresha y en el payload `reviewsTotal`/`rating5Total` (244 de 5 estrellas, 1 de 4 estrellas
  = 245 total). Fuente de primera mano, no estimada.
  - **Limitacion honesta**: no se pudo verificar de forma independiente un numero de reseñas
    especifico de Google esta sesion (Yelp, Facebook y Google Maps bloquearon el acceso directo por
    muro de login/anti-bot con las herramientas disponibles). El sitio y este registro citan
    unicamente el numero de Fresha, con su fuente declarada, en vez de mezclarlo con una cifra de
    Google no verificada.
- **Horario**: confirmado en el `workingTime` de Fresha: Lunes a Viernes 8:30am a 6:30pm, Sabado
  8:30am a 5:30pm, Domingo cerrado. Coincide exactamente con el horario dado.
- **Servicios**: menu completo (38 tratamientos en 8 categorias: Pestañas, Cejas, Rostro, Laser, Cera,
  Labios, Mesoterapia, Manicura) extraido directo del campo `services` del mismo payload de Fresha,
  con nombres, precios y duraciones exactos tal como los publica el negocio.
- **Instagram**: @honey.beautyspa, 2,193 seguidores, bio "Belleza, bienestar y confianza en un solo
  lugar", con los links de bio (`external_url`/`bio_links`) apuntando exactamente a la pagina de
  reservas de Fresha y a `wa.link/eucnn0`, tal como se indico en el research previo.
- **Reseñas verbatim**: las 5 reseñas del research previo (Lieta M, Ana D, Miriam L, Mirta G, Sofia M)
  se confirmaron palabra por palabra en el payload de reseñas de Fresha, mas una sexta de Lieta M
  ("El mejor spa"). Se usaron 3 en el sitio (Ana D, Miriam L, Mirta G) para variedad de idioma.

## Chequeo de website propio (leccion MaRe, obligatorio)

- El campo `external_url` de Instagram apunta unicamente a la pagina de reservas de Fresha, sin
  dominio propio ni linktree.
- Se probo directo el dominio `honeybeautyspa.com`: responde pero **redirige a
  `atom.com/name/HoneyBeautySpa`**, un marketplace de nombres de dominio en venta, no un sitio del
  negocio. Confirma que el dominio no esta en uso por el negocio.
- Facebook (bloqueado por muro de login) e Instagram no muestran ningun otro dominio.
- Conclusion: **`has_own_site: false`**.

## Verificacion de email (fase 1, punto 7 del pipeline)

- El research previo indicaba `spahoneybeauty@gmail.com` como email ya encontrado. Esta sesion se
  intento reconfirmar de forma independiente en TODAS las fuentes indicadas por el pipeline:
  - `business_email` del endpoint `web_profile_info` de Instagram: **null** (no publicado).
  - Pagina de Fresha (HTML completo y `__NEXT_DATA__`): sin ningun `mailto:` ni campo de email.
  - Bio de Instagram / linktree: no hay linktree, solo los dos links ya conocidos (Fresha y WhatsApp).
  - Facebook "About": bloqueado por muro de login con las herramientas disponibles esta sesion.
  - Sunbiz.org (registro de la LLC): no publica email de contacto.
  - Busqueda directa del string exacto `"spahoneybeauty@gmail.com"`: sin resultados que lo confirmen
    en una pagina real.
- **No se pudo confirmar de forma independiente que ese email sea genuinamente publico** con las
  herramientas disponibles esta sesion. Siguiendo la regla de no inventar ni asumir datos no
  verificados, el sitio NO incluye ningun email de contacto y el registro se marca `pending_manual`
  con telefono, WhatsApp e Instagram como canales verificados para el envio manual.

## Version corta para DM / WhatsApp (dm_message)

Hola! Soy Michael, de Merktop. Vi que Honey Beauty Spa tiene 5.0 en Fresha con 245 reseñas, asi que
les arme un sitio de muestra con sus tratamientos, precios y fotos reales:
https://siteforge-demos.odd-forest-9504.workers.dev/honey-beauty-spa/ No toca su agenda de Fresha
para nada. Si les gusta, lo dejamos en su propio dominio. Si no, lo bajamos, sin compromiso.

(365 caracteres, dentro del limite de 450)

## Cuerpo de referencia (para cuando se confirme un email publico)

Hola,

Soy Michael, de Merktop. Encontre Honey Beauty Spa en Fresha, su calificacion de 5.0 con 245
reseñas me llamo la atencion, y revise su trabajo en pestañas, cejas y facial.

Vi que no tienen un sitio web propio, solo su pagina de reservas en Fresha e Instagram, asi que les
arme uno de muestra con sus tratamientos, precios y fotos reales:

https://siteforge-demos.odd-forest-9504.workers.dev/honey-beauty-spa/

Dos cosas que vale la pena saber:
- No toca su operacion de reservas para nada. Cada cita sigue llegando directo a su agenda de
  Fresha, igual que hoy.
- Es bilingue (espanol e ingles), para que tanto sus clientas de Westchester como cualquier otra
  puedan leerlo.

Si les gusta, lo puedo dejar en su propio dominio y lo ajustamos juntos. Si no es para ustedes, lo
bajo, sin ningun problema.

Saludos,
Michael Vargas
Merktop . merktop.com
