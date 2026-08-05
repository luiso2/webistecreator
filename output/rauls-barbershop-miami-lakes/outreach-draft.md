# Outreach draft: Raul's Barbershop (rauls-barbershop-miami-lakes)

- **Estado**: pending_approval (NO enviar sin OK explícito del usuario)
- **Para**: sin email público confirmado (ver sección "Búsqueda de email" abajo para el detalle completo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-rauls-barbershop-miami-lakes-2026-08-05
- **Ángulo**: sin website propio (raulsbarbershop.com existe pero pertenece a un negocio homónimo y no relacionado en Agoura Hills, CA; ver detalle abajo)
- **Idioma**: español (idioma principal observado: mayoría de reseñas verbatim de Google en español, más el área de Miami Lakes/Hialeah)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/rauls-barbershop-miami-lakes/
- **Canal disponible**: sin email público confirmado. Registrado como `outreach: pending_manual` con teléfono (786) 401-6505 y su Instagram @raulsbarbershop_ para DM/WhatsApp manual.

## Check de website propio (lección MaRe, obligatorio)
`raulsbarbershop.com` resuelve con 200 y certificado SSL válido, pero corresponde a un negocio
homónimo y no relacionado: "Raul's Barbershop" en 5679 Kanan Rd, Agoura Hills, CA 91301, teléfono
(747) 222-7318 (confirmado vía búsqueda web: Yelp, Fresha, Chamber of Commerce listan esa dirección
y teléfono, ambos en California). El negocio de este build es "Raul's Barbershop" en 18518 NW 67th
Ave, Miami Lakes, FL 33015, teléfono (786) 401-6505: dirección, estado y teléfono distintos, sin
relación entre ambos. Confirmado: `has_own_site: false` para el negocio de Miami Lakes.

## Búsqueda de email (profundizada, PIPELINE fase 1 punto 7)
- Booksy (`booksy_dossier.py` sobre su perfil real): campo de email/teléfono no publicado en el
  payload del venue; solo se extrajeron nombre, dirección y geo.
- Bio de Instagram (@raulsbarbershop_): "Miami Lakes FL, BarberShop In SFL, Specializing In Regular
  Cuts, Fades, Designs, DM To Book Your Appointment". Sin email ni link externo, solo indica DM.
- Facebook (página "Rauls BarberShop | Miami Lakes FL", facebook.com/100063620460251): About no
  accesible sin login (bloqueo estándar de Facebook a scraping no autenticado); búsqueda no
  encontró email publicado en snippets indexados.
- Directorio de plaza (countryclubplazafl.com/rauls-barber-shop): lista teléfono, sin email ni
  website.
- Búsqueda web general "Raul's Barbershop Miami Lakes email": sin resultado adicional verificable.
- Conclusión: sin email público verificable tras búsqueda exhaustiva. `email: null`.

## Verificación de rating
Google Maps: 5.0 estrellas, 254 reseñas (dato de partida). Corroborado de forma independiente vía
Birdeye (agregador de reseñas de Google/Facebook para este negocio, reviews.birdeye.com/rauls-barbershop-170252508264646):
5.0 estrellas, 260 reseñas al momento de la verificación (crecimiento natural sobre las 254
reportadas), con reseñas verbatim reales visibles (Matty Chavez, Henry, Felipe Padron, todas
citadas en el site). Booksy muestra 4.8 sobre 17 reseñas, una fuente secundaria de menor volumen:
el site usa Google (5.0 / 254) como el dato principal, tal como indica el research.

## Fotos
7 fotos reales curadas del feed público de Instagram (@raulsbarbershop_, vía ig_photos.py) y del
listado de Booksy (fachada real de la tienda): fades y cortes terminados con buena luz, interior de
la barbería con su letrero iluminado, un barbero atendiendo a un cliente, y un corte de niño.
Descartadas: 2 gráficos de flyer/aniversario con texto superpuesto, 1 foto de evento nocturno sin
relación con el trabajo de barbería, 1 primer plano a medio proceso, y 1 foto con caption superpuesto
("mid fade francés") que viola la regla de curación visual.

## Subject (para cuando haya un canal de email)
Un sitio de muestra para Raul's Barbershop (ya está listo)

## Cuerpo (referencia, para email o como base del DM largo)

Hola,

Soy Michael, de Merktop. Encontré Raul's Barbershop por su calificación de 5.0 en Google con 254
reseñas, y me pasé por su Instagram (@raulsbarbershop_) para ver los fades y diseños que publican.

Vi que no tienen un sitio propio, solo Instagram y Booksy, así que les armé un sitio de muestra con
sus fotos reales, sus reseñas reales y su ubicación en Miami Lakes:

https://siteforge-demos.odd-forest-9504.workers.dev/rauls-barbershop-miami-lakes/

Dos cosas que vale la pena saber:
- No toca su reserva en Booksy para nada. Cada cita sigue llegando exactamente igual que hoy.
- Es bilingüe (español e inglés), listo para toda su clientela de Miami Lakes.

Si les gusta, se los dejo en su propio dominio y lo ajustamos juntos. Si no es para ustedes, lo bajo,
sin problema.

Saludos,
Michael Vargas
Merktop · merktop.com

## Versión corta para DM / WhatsApp (dm_message, 356 caracteres)

¡Hola! Soy Michael, de Merktop. Vi que Raul's Barbershop tiene 5.0 en Google con 254 reseñas, así
que les armé un sitio de muestra con sus fotos y reseñas reales: https://siteforge-demos.odd-forest-9504.workers.dev/rauls-barbershop-miami-lakes/
No toca su reserva en Booksy para nada. Si les gusta, se los dejo en su dominio, si no lo bajo, sin
compromiso.
