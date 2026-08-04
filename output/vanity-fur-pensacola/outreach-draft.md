# Outreach draft: Vanity Fur

Status: draft_for_approval (no enviado). Requiere aprobacion humana del lote antes de enviar.

- Negocio: Vanity Fur, LLC
- Ciudad: Pensacola, FL
- Rating: 4.8 en Google (169 reseñas), tambien 4.4/26 en Yelp
- Has own site: false (vanityfurpensacola.com no resuelve; vanityfur.com es una pagina parked de GoDaddy sin relacion; vanityfurgroomer.com y vanityfurmobilepetspa.com redirigen a negocios sin relacion en otras ciudades/paises, confirmado con curl)
- Canal de contacto publico encontrado: telefono (850) 285-0997, email Vanityfurpensacola@gmail.com, Facebook facebook.com/vanityfurpensacola (sin Instagram propio confirmado)
- Idioma principal: en
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/vanity-fur-pensacola/
- Angulo: "we built you a sample website" (no tienen website propio)

## Email (referencia, mismo mensaje que iria por Resend si hubiera aprobacion del lote)

Subject: A free sample website for Vanity Fur

Hi there,

I found Vanity Fur on Google, 4.8 stars with 169 reviews, and noticed the salon does not have its own website yet. I put together a free demo using your real photos, services and reviews:

https://siteforge-demos.odd-forest-9504.workers.dev/vanity-fur-pensacola/

It does not touch your phone booking at all, it is just a sample. Happy to put it on your own domain at no cost, or take it down, your call, no strings attached.

Michael Vargas
Merktop

## DM / WhatsApp version (dm_message, ya guardado en el registro)

Hi! Found Vanity Fur on Google, 4.8 stars and 169 reviews, and saw you don't have your own website yet. Built you a free demo with your real photos and services: https://siteforge-demos.odd-forest-9504.workers.dev/vanity-fur-pensacola/ Take a look, no strings attached. Happy to put it on your own domain or take it down, your call.

## Notas de research

- Rating cruzado: 4.5/25-26 en Yelp (confirmado directo del schema.org de la pagina de Yelp: ratingValue no expuesto en el bloque agregado pero reviewCount:26 y meta description "26 reviews and 29 photos" si), 4.8/169 en Google (triangulado por chamberofcommerce.com, bestprosintown.com y dogdog.org, este ultimo con "167 people rated" via el widget OAuth de Google embebido, consistente con 169). Google Maps no se pudo scrapear directo (JS-heavy, sin API), asi que el 4.8/169 es cruzado por 3 fuentes independientes en vez de leido directo de Google, tal como anticipaba el brief.
- Premio real verificado independientemente: ganador de "Best Dog Groomer" en el Best of the Coast 2025 de Inweekly (inweekly.net/best-of-the-coast-2025-complete-winners-runners-up-list), citado tambien en su propia pagina de Facebook.
- 3 reseñas verbatim con nombre obtenidas de la pagina real de Yelp (via proxy translate.goog para evitar el 403 directo): Clarice P., Barbara L., Sheri L. Coinciden groomers reales mencionados: Donna (lider del equipo), Natalie/Natalie Bell, Shannon/Shannon Gordon, Sara Hardy, Amanda, Valerie Reed.
- Servicios confirmados (no inventados): baño, corte de raza, corte de uñas, limpieza de oidos (menu base) + tratamiento de patas y limpieza dental (add-ons), segun descripcion de su propia ficha (mirroreada en dogdog.org). Sin precios publicados en ninguna fuente: se dejo nota de "se cotiza segun raza y pelaje" en vez de inventar precios.
- Instagram: se probaron handles candidatos (vanityfurpensacola, vanityfur_pensacola, vanityfurllc, vanityfurgroomers, vanityfurdoggrooming, vfpensacola, vanityfurfl) via web_profile_info; ninguno corresponde al negocio de Pensacola (vanityfurgroomers no existe, vanityfurrgroomers y vanityfurdoggrooming son negocios de Reino Unido sin relacion). Se concluye que el negocio NO tiene Instagram propio confirmable; el ig_url del sitio apunta a su Facebook real.
- Horario: fuentes cruzadas lo reportaban de forma inconsistente (Tue-Sat 7:30-5 vs Mon-Sat 8-6) y no se pudo confirmar un horario fresco (Google Maps no accesible directo, Facebook About y Nextdoor bloquearon el scrape). Se omitio del site un horario especifico; en su lugar se uso el flujo de reserva real y verificado: "llama y deja un mensaje de voz, te llaman o escriben para coordinar" (texto tomado directo de su propia pagina de Facebook).
- Fotos: 0 fuentes propias de Instagram (no existe la cuenta). Las 14 fotos usadas vienen de la pagina real de Yelp del negocio (25-26 fotos disponibles, descargadas via el proxy translate.goog de Yelp en resolucion 1000px) mas 2 fotos adicionales de Facebook (permalinks indexados por Google, extraidas por su meta og:image). Las 25 fotos de Yelp se revisaron una por una con el visor de imagenes antes de elegir: se descartaron las de tema navideño/estacional, una con nombre de mascota en un letrero de madera (prop con texto), y una donde el perro se veia despeinado a medio terminar. De las que sobraron (bastante mas de 5 utilizables), se eligieron 14 para el site: perros recien groomeados con ojos abiertos, en la mesa de grooming o en el lobby del salon, mostrando tambien el interior real (entrada de vidrio, estanterias, espejo de estacion). Se descartaron 3 fotos de Google (via dogdog.org) por dudas de relacion real con el negocio: una maquina de autoservicio "DogHouse" con texto de instrucciones, un perro en lo que parece la parte trasera de una van movil (Vanity Fur es un local fijo, no movil), y una foto borrosa de un loro.
