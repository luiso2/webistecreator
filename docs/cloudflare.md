# Cloudflare y publicación

La infraestructura actual se conserva: un Worker compartido sirve `output/<slug>/`, mientras que `DOMAIN_MAP` resuelve dominios personalizados y `SITEFORGE_KV` mantiene configuración rápida.

## Publicación independiente de demos

Los demos nuevos ya no dependen de que Workers Builds vuelva a subir todo `output/`.
Railway publica cada sitio como un bundle inmutable en R2:

1. sube archivos a `sites/<slug>/versions/<sha256>/...`;
2. envía un manifest con tamaño y SHA-256 por archivo;
3. el Worker verifica todos los objetos con `head()`;
4. escribe el manifest inmutable;
5. activa la versión con una única escritura de `sites/<slug>/current.json`.

La ruta estable `/<slug>/` resuelve el puntero actual. Al entregar HTML, el Worker cambia
las referencias relativas de imágenes y scripts por URLs inmutables bajo
`/_siteforge/assets/<slug>/<version>/...`. `Static Assets` permanece como fallback para
los sitios históricos y permite una migración gradual sin romper URLs existentes.

El endpoint de publicación requiere el secret `SITEFORGE_PUBLISH_KEY`. Nunca se activa una
versión si falta `index.html`, un checksum no coincide o algún objeto no está presente.

Las operaciones de publicación pasan por QueueClaims y Railway. Railway reutiliza `derive.py`, `gate.py`, el commit atómico de GitHub y la comprobación del HTML publicado. Esto evita desplegar un Worker separado por website y permite rollback lógico mediante SiteSpec.
