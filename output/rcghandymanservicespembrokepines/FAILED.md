# FAILED: RCG Handyman Services (Pembroke Pines, FL)

**Slug**: rcghandymanservicespembrokepines
**Fecha**: 2026-08-14
**Motivo**: menos de 5 fotos reales propias disponibles (minimo del pipeline, Fase 3.5 / PIPELINE.md).

## Que se intento (research exhaustivo)

### Fotos
1. **Google Maps** (unica fuente confirmada por el research previo): se descargo la unica foto
   real provista (`assets/raw/gmaps-1.jpg`, verificada con `file` como JPEG real 1300x667). Al
   curarla visualmente (Read) resulto ser un **flyer promocional con texto superpuesto** (logo RCG
   Handyman, lista de servicios en texto, dos telefonos, url `www.rcghandymanservices.com`, fondo
   de tablero de madera con herramientas) y NO una foto real de trabajo/jobsite. Segun
   PIPELINE.md Fase 3 punto 2 ("PROHIBIDO en galeria: ... capturas con texto/caption encima"),
   esta imagen queda descartada de la galeria. Resultado neto: **0 fotos reales utilizables** de
   esta fuente.
2. **Google Maps place page** (fetch directo de la URL de la ficha): la pagina no renderiza
   server-side el carrusel de fotos (se carga por JS/XHR tras el load), asi que no fue posible
   extraer mas URLs `lh3/lh4/lh5/lh6.ggpht.com` reales desde el HTML estatico.
3. **Yelp** (`yelp.com/biz/rcg-handyman-services-hialeah-2`, listado con 124 fotos segun snippet
   de busqueda, mismo telefono 954-446-3771 que confirma que es el mismo negocio bajo direccion
   Hialeah): bloqueado por proteccion Datadome/captcha en todos los intentos (curl directo con
   varios User-Agents, headers de navegador con Referer de Google, WebFetch, proxy lector r.jina.ai).
   HTTP 403 consistente en las 4 rutas probadas. No fue posible extraer ninguna foto.
4. **Facebook** (`facebook.com/p/RCG-Contractor-Handyman-100063625508325/`, posible match sin
   confirmar segun la nota del research): tanto la version de escritorio como `mbasic.facebook.com`
   devuelven muro de login sin datos de negocio verificables (no se pudo confirmar telefono/ciudad
   coincidentes), y no se pudo extraer ninguna foto.
5. **Instagram**: el unico handle encontrado por busqueda, `@rcghandymanservices`, es explicitamente
   un negocio DISTINTO en California segun la nota de research; se descarto sin usarlo (regla dura:
   solo aceptar match solido nombre+ciudad+telefono).
6. **Thumbtack**: busqueda especifica "RCG Handyman Services Pembroke Pines thumbtack" no arrojo
   perfil del negocio.
7. **YellowPages** (`yellowpages.com/hialeah-fl/mip/rcg-handyman-services-561483730`): confirmado
   via WebFetch que el listado muestra "Be the first to add a photo" (sin fotos).
8. **Manta.com**, **Tupalo.co**: ambos bloqueados (403 / reto anti-bot Anubis) sin acceso a contenido.
9. **Sitio propio historico**: el flyer de Google Maps menciona `www.rcghandymanservices.com`. Se
   verifico que el dominio **no resuelve actualmente** (`Could not resolve host`, confirmado con
   `curl` y `socket.gethostbyname` en dos intentos), es decir, no es un sitio propio activo hoy
   (consistente con la verificacion en vivo de la ficha de Google sin boton de website). Wayback
   Machine tiene un snapshot de 2022 pero `web.archive.org` esta bloqueado para fetch en este
   entorno (herramienta WebFetch y curl directo fallan), asi que no se pudo recuperar contenido
   ni fotos historicas de ese snapshot tampoco.

### Email
Busqueda exhaustiva sin resultado: Google, Yelp (bloqueado), YellowPages (sin email), Manta
(bloqueado), sunbiz.org (bloqueado por reto Cloudflare), BBB (el unico resultado de "RCG
Contractor & Handyman LLC" en BBB es un negocio distinto en Vancouver, WA, no este). `email: null`.

## Conclusion
Con 0 fotos reales curables (el unico asset descargado es un flyer promocional con texto, no una
foto de trabajo) el negocio no alcanza el minimo de 5 fotos reales que exige el pipeline
(PIPELINE.md Fase 3.5: "`failed` se reserva para cuando faltan los MINIMOS: menos de 5 fotos
reales propias..."). No se construyo `content.json` ni `index.html`. No se toco
`data/processed.json`. No se contacto al negocio.
