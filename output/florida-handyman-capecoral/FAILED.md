# FAILED: florida-handyman-capecoral

**Motivo:** tiene website propio: https://northfortmyershandyman.com/

## Detalle de verificacion (PASO 1)

- `gmaps_detail.js` sobre la ficha de Google Maps de "FLORIDA HANDYMAN" (corrido 3 veces, con
  la URL dada y con la URL reencontrada via `gmaps_discover.js`) devolvio consistentemente
  `website: null` y solo 1 foto (`photos: [1]`), sin `reviewSamples` y sin `address` (ficha
  limitada / sin address publica, listado como negocio de area de servicio).
- `gmaps_discover.js "FLORIDA HANDYMAN Cape Coral FL"` confirma la misma ficha
  (`hasWebsiteButton: false`, telefono `+1 239-745-5585`, rating 5.0), sin boton de website en
  el listado del mapa.
- WebSearch por el telefono exacto `239-745-5585` / `(239) 745-5585` identifico el negocio real:
  **Florida Handyman General Repair Services LLC**, dueno **Jesus Jamaica**, con perfil BBB
  (`bbb.org/us/fl/north-fort-myers/profile/handyman/florida-handyman-0653-90420782`, A+, no
  acreditado, activo desde 1/24/2022) que lista domicilio en **North Fort Myers, FL 33917**
  (no Cape Coral: el negocio aparece en la busqueda de Cape Coral porque su ficha de Google es
  de area de servicio y cubre esa zona, pero su base real es North Fort Myers).
- Ese mismo research encontro el email `JesusJamaica@northfortmyershandyman.com`, cuyo dominio
  (`northfortmyershandyman.com`) se probo directamente por curl:
  - `curl -sS -L -A "<Chrome UA>" https://northfortmyershandyman.com/` -> **HTTP 200**, 171 KB
    de HTML.
  - `<title>Florida Handyman - Your Trusted Handyman Near Me</title>`, meta description real
    ("Florida Handyman offers reliable and professional handyman services near you...").
  - El telefono en la pagina (`tel:+1239-745-5585`, `tel:2397455585`) y el email
    (`mailto:JesusJamaica@northfortmyershandyman.com`) coinciden EXACTOS con los del negocio de
    la ficha de Google Maps: es el mismo negocio, sin ambiguedad de nombre generico.
  - Contenido real de la pagina (no landing vacia ni "coming soon"): hero "Fix it with Florida
    Handyman", seccion "About Florida Handyman Services" (Professional Handyman Services, 24/7
    Emergency Services, Transparent Pricing), "Our Latest Projects Gallery" (galeria de 6 fotos),
    "Customer Testimonials", "Contact Us", sistema de citas online ("Schedule Now" / "Bookings"
    / login de cuenta), y link a su pagina de Facebook
    (`https://www.facebook.com/196394756887853`).
  - Construida sobre GoDaddy Website Builder (`img1.wsimg.com`), pero en **dominio propio**
    `northfortmyershandyman.com` (no un subdominio de plataforma de booking tipo square.site o
    glossgenius.com: esos NO cuentan como website propio, este SI porque es dominio propio con
    contenido de marca completo).

## Conclusion

El negocio SI tiene un website propio funcional con contenido real (no un stub ni un
subdominio de booking). Segun el filtro duro de esta corrida, esto es un FAIL: no se
construyo el demo. No se realizo ningun build, no se descargaron fotos adicionales, no se
contacto al negocio por ningun canal, y no se hizo commit/push/deploy.

Si en una corrida futura se decide procesar este negocio bajo el modo "handle/nombre directo"
(que SI acepta negocios con website propio, PIPELINE.md linea 8), el angulo de outreach
correcto seria "propuesta de rediseno", nunca "les construimos un sitio de muestra" ni
afirmar "no tienen website".
