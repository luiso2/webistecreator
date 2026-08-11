# Outreach draft: Yanila & Jany Nails (yanilaandjanynails-miami)

## Estado
- Email publico: **NO encontrado**. Busqueda realizada en: `data.json` (phone=null, same_as solo trae Instagram), ficha de Chamber of Commerce (`chamberofcommerce.com/.../yanila-jany-nails`, sin email visible), bio de Instagram `@yanilayvl` (2 intentos: endpoint `web_profile_info` devolvio 404/bloqueado, fetch directo de `instagram.com/yanilayvl/` devolvio respuesta vacia, consistente con el bloqueo conocido del entorno), y busquedas web `"Yanila" "Jany" nails Miami email contact` / `"yanilayvl" instagram nails contact`. Ningun resultado expuso un correo.
- Telefono: **no publicado** (`data.json.phone = null`).
- Canal de contacto verificado: **Instagram** `@yanilayvl` (https://www.instagram.com/yanilayvl/) y el propio Booksy (booking).
- `outreach`: `pending_manual` (DM de Instagram, requiere aprobacion humana antes de enviarse).
- Nota: existe otra ficha duplicada de Booksy del mismo negocio (id 861607, "Yanila & Jany Nails"), ya descartada en discovery; no aplica a este outreach.

## Borrador de DM (Instagram, español)

Hola! Soy Michael de Merktop. Vi su perfil de Yanila & Jany Nails (5.0 con 306 reseñas en Booksy, impresionante) y les arme una pagina de muestra para que vean como se veria un sitio propio, sin tocar para nada su sistema de reservas en Booksy:

https://siteforge-demos.odd-forest-9504.workers.dev/yanilaandjanynails-miami/

Es solo una muestra, sin compromiso: si les gusta lo dejamos listo en su propio dominio, y si no, no pasa nada y lo retiramos. Cualquier duda con gusto la resolvemos por aqui.

Michael Vargas / Merktop

## dm_message (version corta, campo del registro)
```
Hola! Soy Michael de Merktop. Vi Yanila & Jany Nails (5.0 con 306 reseñas en Booksy) y les arme una pagina de muestra, sin tocar su booking de Booksy: https://siteforge-demos.odd-forest-9504.workers.dev/yanilaandjanynails-miami/ Sin compromiso: si les gusta la dejamos en su dominio, si no la retiramos. Michael / Merktop
```
(Longitud: 321 caracteres, dentro del limite de 450.)

## Notas
- Angulo: `has_own_site: false` -> "les construimos un sitio de muestra" (no tienen website propio, `website_candidates` vino vacio en el dossier).
- Idioma principal del negocio: español (confirmado por `data.json.language = "es"` y las reseñas en español).
- Firmado Michael Vargas / Merktop, sin em-dash, sin datos inventados.
- Este borrador NO se envia: queda pendiente de aprobacion humana por lote, segun PIPELINE.md Fase 5. No se contacto al negocio por ningun canal.
