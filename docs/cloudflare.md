# Cloudflare y publicación

La infraestructura actual se conserva: un Worker compartido sirve `output/<slug>/`, mientras que `DOMAIN_MAP` resuelve dominios personalizados y `SITEFORGE_KV` mantiene configuración rápida.

Las operaciones de publicación pasan por QueueClaims y Railway. Railway reutiliza `derive.py`, `gate.py`, el commit atómico de GitHub y la comprobación del HTML publicado. Esto evita desplegar un Worker separado por website y permite rollback lógico mediante SiteSpec.
