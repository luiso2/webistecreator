# FAILED: K&F Handyman Services (Homestead, FL)

**Slug**: kf-handyman-services-homestead
**Fecha**: 2026-11-09
**Motivo**: menos de 5 fotos reales utilizables (minimo del pipeline, PIPELINE.md Fase 3 / FORGE-BRIEF.md 0.b).

## Paso 1: verificacion de website propio (OK, no descarta)

- `detail.website` del research packet es `null` (sin boton de website en la ficha de Google Maps).
- Se probaron dominios candidatos por curl: `kandf-handyman-services.com` (sin resolver),
  `kfhandymanservices.com` / `.net` (sin resolver), `kfhandymanserviceshomestead.com` (sin
  resolver), `kandfhandyman.com` (sin resolver), `khandfservices.com` (sin resolver).
  `khandyman.com` responde 403 mediante un reto de Cloudflare generico (dominio parkeado/no
  relacionado, sin contenido verificable). `kfhandyman.com` responde 200 pero es un negocio
  DISTINTO ("KF Handyman", Los Angeles CA, generado con Hostinger AI Builder) sin relacion con
  este negocio de Homestead, FL: coincidencia de nombre, no el mismo negocio.
- WebSearch por `"K&F Handyman Services" Homestead FL` y por el nombre del posible dueno
  (`Fizal Mohamed`, mencionado en una resena de Google) no encontro website propio, pagina de
  Facebook ni perfil de Instagram para este negocio especifico.
- Conclusion paso 1: NO tiene website propio. `has_own_site: false`. Esto no descarta el
  negocio (no es el motivo del fail), pero no hay ningun canal de contacto adicional (ni email,
  ni redes) mas alla del telefono.

## Paso 2: curaduria visual de fotos (motivo real del fail)

El research packet (Maps) trae solo 4 URLs de fotos (`detail.photos`), ya avisado de antemano
como un caso limite. Se descargaron las 4 con `scripts/_gmaps_photos.py` (las 4 son JPEG
validos, verificados con PIL) y se genero `output/kf-handyman-services-homestead/_sheet.jpg`
para curaduria visual (Read del sheet + de cada foto individual):

- `gmaps-1.jpg` y `gmaps-2.jpg`: la MISMA tarjeta grafica (logo "K&F" + "K&F Handyman Services
  LLC" + "Contact us: 786-416-1103") sobre fondo azul oscuro. Es un grafico de marca con texto
  superpuesto, no una foto de un trabajo real. PROHIBIDO en galeria por regla dura de curaduria
  visual (PIPELINE.md Fase 3 punto 2: "capturas con texto/caption encima"). Descartadas.
- `gmaps-3.jpg`: foto real y de buena calidad de una entrada vehicular de concreto estampado
  (stamped concrete driveway) terminada, con la fachada de una casa. Trabajo real, visible,
  bien iluminado. VALIDA.
- `gmaps-4.jpg`: interior de una oficina/local comercial a medio proceso de pintura/preparacion
  (piso cubierto con papel y cinta de pintor, latas de pintura, una sierra ingletadora, paredes
  sin terminar). Muestra contexto de trabajo real (no selfie, no blur, sin texto superpuesto),
  pero es una habitacion vacia en preparacion, no un resultado terminado. Se cuenta como
  utilizable en el limite (foto de "proceso"), pero es la unica candidata ademas de gmaps-3.

**Resultado: 2 fotos reales utilizables de 4** (`gmaps-3.jpg`, `gmaps-4.jpg`), muy por debajo
del minimo de 5 que exige el pipeline. No hay otra fuente de fotos disponible: el negocio no
tiene website propio, Instagram ni Facebook localizables (ver paso 1), asi que no hay galeria
de respaldo de donde rescatar mas imagenes reales.

## Conclusion

Con solo 2 fotos reales curables (muy por debajo del minimo de 5), el negocio no alcanza el
minimo que exige el pipeline (PIPELINE.md Fase 3 / FORGE-BRIEF.md 0.b: "`failed` se reserva
para cuando faltan los MINIMOS: menos de 5 fotos reales y propias del negocio"). No se
construyo `content.json` ni `index.html`. No se toco `data/processed.json`. No se contacto al
negocio por ningun canal.
