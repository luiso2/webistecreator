# Outreach draft: Juanca's Bakery (juancas-bakery-cape-coral)

- **Estado**: `pending_manual` (no se encontro email publico tras busqueda exhaustiva: sin website
  propio, IG bloqueado en los 2 intentos permitidos, TikTok sin email visible sin login)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-juancas-bakery-cape-coral-2026-11-04
- **Angulo**: sin website propio (`has_own_site: false`) -> "les construi un sitio de muestra"
- **Idioma**: espanol (panaderia cubana, letrero/menu en espanol, ficha de Google marcada "Identifies
  as Latino-owned"; los quotes de resenas usadas en el site estan en ingles, su idioma original, sin
  traducir, tal como pide DESIGN.md)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/juancas-bakery-cape-coral/
- **Telefono verificado**: (239) 257-1403 (ficha de Google Maps)
- **Direccion**: 1524 Hancock Bridge Pkwy, Cape Coral, FL 33990

## Verificacion de rating y resenas
Google Maps en vivo (via Playwright): 5.0 de calificacion, 161 resenas, scrapeado 2026-11-04. 4
resenas verbatim guardadas con nombre real (Natan Saidon, Kathleen Hawkins, Royalty Padding, Nina
R), una de ellas menciona explicitamente un video viral de TikTok de su torta de guayaba.

## Chequeo de website propio
- El campo "website" de la ficha de Google Maps apunta a `https://www.tiktok.com/@juanca.bakery`.
  TikTok es una red social, no un dominio propio, asi que NO cuenta como website propio.
- No se encontro ningun dominio propio adicional.
- Conclusion: `has_own_site: false`.

## Busqueda de email
- Sin dominio propio del cual sacar email.
- Intentos de lookup de Instagram (`juancasbakery`, `juanca.bakery`) devolvieron respuesta vacia /
  bloqueada en los 2 intentos permitidos por el pipeline; no se insistio mas.
- Conclusion: `outreach: pending_manual`. Contactar por telefono al (239) 257-1403.

## Subject (referencia)
Un sitio de muestra gratis para Juanca's Bakery

## Cuerpo (referencia)

```
Hola,

Encontre Juanca's Bakery buscando panaderias cubanas en Cape Coral. Una calificacion de 5.0 con
161 resenas, y clientes que mencionan hasta un video viral en TikTok de su torta de guayaba, es
una carta de presentacion seria.

Note que Juanca's Bakery no tiene un sitio web propio (lo unico que aparece en su ficha de Google
es un link a TikTok), asi que les construi uno de muestra, sin costo y sin compromiso:

https://siteforge-demos.odd-forest-9504.workers.dev/juancas-bakery-cape-coral/

Usa sus fotos reales, su direccion, su telefono y resenas reales de sus clientes. No toca para
nada su operacion actual: no es su pagina oficial, no reemplaza nada, y el boton principal solo
llama a su telefono.

Si les gusta la direccion, puedo transferirles los archivos o ayudarles a apuntar su propio
dominio. Si no es para ustedes, lo entiendo, lo bajo sin ningun problema.

Cualquier ajuste (colores, fotos, texto) lo hago con gusto antes de que decidan.

Saludos,
Michael Vargas
Merktop
```

---

## Version corta para DM / WhatsApp (dm_message)

```
Hola! Soy Michael, de Merktop. Vi Juanca's Bakery en Cape Coral, 5.0 en resenas con 161 opiniones,
gente que menciona hasta un video viral de su torta de guayaba en TikTok. Les hice un sitio de
muestra gratis con sus fotos reales: https://siteforge-demos.odd-forest-9504.workers.dev/juancas-bakery-cape-coral/
No toca su operacion actual. Si les gusta, se los transfiero sin costo. Si no, lo bajo sin
problema. Michael Vargas, Merktop.
```

(435 caracteres, en espanol por ser el idioma principal del negocio, sin em-dash.)
