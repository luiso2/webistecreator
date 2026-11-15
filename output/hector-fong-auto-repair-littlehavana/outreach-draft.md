# Outreach draft: Hector Fong Auto Repair (hector-fong-auto-repair-littlehavana)

NO enviado. Requiere aprobacion humana antes de contactar al negocio por cualquier canal.

## Datos de contacto verificados
- Nombre: Hector Fong Auto Repair
- Direccion: 999 W Flagler St, Miami, FL 33130 (Little Havana)
- Telefono (Google Business): +1 305-902-0920
- Telefono secundario visible en banners del local: 786-230-7072
- Email publico: NO encontrado (busqueda web + directorios no arrojo ningun email; el negocio no tiene
  website, Instagram ni Facebook localizables). Canal disponible: solo telefono / visita en persona.
- Instagram / redes: ninguna encontrada.
- Rating verificado: 4.8 estrellas, 44 reseñas en Google.
- has_own_site: false.

## Canal de outreach
Sin email ni redes sociales publicas, el unico canal real es telefonico o visita presencial al
taller. outreach = `pending_manual`. Se deja el guion de llamada/WhatsApp listo para que el
usuario decida como y cuando contactar.

## Guion de llamada / mensaje de texto (si el numero tiene WhatsApp, no confirmado)
Angulo: "les construi un website de muestra" (has_own_site: false).

Español:
> Hola, buenas, hablo con el taller de Hector Fong? Mi nombre es Michael, trabajo con Merktop.
> Los encontre en Google, vi que tienen 4.8 estrellas con 44 reseñas y no tienen pagina web, asi
> que les arme una de muestra sin costo para que la vean: va a ir por WhatsApp/mensaje de texto.
> No toca para nada como manejan el taller ni las citas. Si les gusta, se la dejamos en su propio
> dominio; si no, no hay ningun compromiso. Le parece si le mando el link?

English (si prefieren o si contesta alguien que no habla español):
> Hi, is this Hector Fong Auto Repair? My name is Michael, I work with Merktop. I found you on
> Google, saw you have a 4.8 rating with 44 reviews and no website, so I put together a free
> sample site for you to see, I will text you the link. It does not change anything about how
> you run the shop. If you like it we can put it on your own domain, if not, no strings attached.
> Mind if I send the link over?

## dm_message (version corta para WhatsApp/SMS, max 450 caracteres, idioma: es)
Caracteres: 417

```
Hola, soy Michael de Merktop. Vi que Hector Fong Auto Repair tiene 4.8 estrellas con 44 reseñas en Google y no tienen website, así que les construí uno de muestra gratis: https://siteforge-demos.odd-forest-9504.workers.dev/hector-fong-auto-repair-littlehavana/. No toca para nada su operación del taller. Si les gusta se lo dejamos en su propio dominio, y si no, lo retiramos sin compromiso. Me avisan que les parece.
```

## Firma
Michael Vargas / Merktop (reply-to jose@merktop.com cuando exista canal de email; aqui no aplica
por falta de email publico).

## Nota importante para quien apruebe el envio
Ya existe en el repo (sin registrar en `data/processed.json`, sin publicar/deploy) un build previo
y abandonado del MISMO negocio en `output/hector-fong-auto-repair/` (mismo Google Place ID, mismo
telefono y direccion, commit `388236be`). Ese build usa un esqueleto antiguo que ya no pasa el gate
actual (localStorage de idioma no aislado por sitio) y nunca fue publicado ni registrado. Antes de
desplegar `hector-fong-auto-repair-littlehavana`, conviene borrar o archivar ese directorio viejo
para no terminar con dos demos del mismo negocio en el repo.
