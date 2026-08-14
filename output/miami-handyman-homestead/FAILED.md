# FAILED: miami-handyman-homestead

**Motivo**: tiene website propio: https://www.miami-handyman.net

## Evidencia

- Ficha de Google Maps (fuente): "Miami-Handyman", rating 4.7, 27 reseñas, categoria
  "Handyman/Handywoman/Handyperson", direccion "437 SW 7th St Apt 209, Miami, FL 33130,
  United States", telefono "+1 786-636-5512". El campo `website` de `gmaps_detail.js` dio
  `null` (Google no tiene el link registrado en la ficha), pero eso NO significa que el
  negocio no tenga dominio propio: el filtro duro exige probar dominios candidatos y buscar
  por telefono exacto, no solo confiar en el campo de la ficha.
- Nota sobre la ciudad: la direccion real de la ficha de Google es Miami, FL 33130 (Brickell/
  downtown), NO Homestead, FL. El input de la tarea traia "Homestead, FL" pero el negocio
  encontrado (mismo nombre exacto "Miami-Handyman", mismo rating 4.7, mismo telefono, misma
  ficha) esta en Miami. `gmaps_discover.js` con la query "Miami-Handyman Homestead FL" devolvio
  esta misma ficha (unica con ese nombre exacto) entre 34 resultados, confirmando que es el
  mismo negocio y que no existe una version homonima en Homestead.
- WebSearch por el telefono exacto "786-636-5512" encontro: "Miami-Handyman's website is
  www.miami-handyman.net with the phone number 786-636-5512."
- Se descargo y verifico `https://www.miami-handyman.net` con curl (User-Agent Chrome):
  responde 200, es un sitio completo y funcional (no un placeholder ni un parked domain):
  - Titulo: "Handyman Miami & Brickell · Open 24/7 · Drywall · Plumbing · Electrical ·
    (786) 636-5512"
  - JSON-LD `HomeAndConstructionBusiness` con:
    - `telephone`: "+1-786-636-5512" (EXACTO match con la ficha de Google)
    - `address.streetAddress`: "437 SW 7th St APT 209" (EXACTO match con la ficha de Google)
    - `geo`: latitude 25.7674122, longitude -80.2016357 (EXACTO match con las coordenadas de
      la ficha de Google Maps de este negocio)
    - `aggregateRating`: ratingValue 4.7, reviewCount 25 (consistente con el 4.7/27 real)
    - Catalogo real de servicios: Furniture Assembly, Drywall Patching, Electrical Repair,
      Plumbing Repair, Doors/Cabinets & Flooring Install, Painting
  - Contenido completo: nav, hero, franjas de badges, secciones de servicios con textos
    propios, todo con diseño propio (no una landing generica sin datos).

## Conclusion

El negocio SI tiene un website propio funcional (`miami-handyman.net`), con los mismos datos
de contacto y geolocalizacion exactos que su ficha de Google Maps. Segun PIPELINE.md Paso 1,
esto es motivo de FAIL inmediato: no se construyo el demo.

No se contacto al negocio por ningun canal. No se hizo build, gate, ni deploy.
