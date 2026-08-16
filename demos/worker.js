import { SHARED_STYLE_REV } from './shared-style.js';

// Worker de demos: sirve los sitios de output/ como assets estaticos.
// - En workers.dev (path-based): siteforge-demos.../<slug>/ -> se sirve tal cual.
// - En un dominio propio comprado desde el panel: se mapea el hostname -> slug via KV
//   (llave "domain:<hostname>" escrita por el panel al comprar) y se reescribe la ruta a
//   /<slug>/... para servir ese sitio en la raiz del dominio. SSL lo pone Cloudflare solo.
// Colores: el panel guarda en KV "color:<slug>" los 4 tokens de acento del sitio, y aqui se
// inyectan como un <style> al final del <head>. Asi cambiar el color de un sitio es instantaneo
// y NO exige reconstruirlo ni volver a deployar los 500+ sitios.
// Solo se aceptan valores de color con forma conocida: estos valores acaban dentro de un
// <style>, y sin validarlos una escritura en KV podria cerrar la etiqueta e inyectar markup.
const COLOR_OK = /^(#[0-9a-f]{3,8}|rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*(?:,\s*(?:0|1|0?\.\d+)\s*)?\))$/i;
const TOKENS = ['deep', 'mid', 'soft', 'ghost'];

// Los esqueletos NO usan var(--accent-*) en todas partes: el gradiente de .text-shine, el
// relieve de .btn-3d, .step-num, .stars, .book-float y la barra de progreso llevan el dorado
// escrito a mano. Cambiar solo las variables dejaba el titular y los botones dorados sobre un
// sitio ya recoloreado. Por eso se derivan los tonos y se reescriben tambien esas reglas.
const hexRGB = h => {
  const s = h.replace('#', '');
  const n = s.length === 3 ? s.split('').map(c => c + c).join('') : s.slice(0, 6);
  const v = [0, 2, 4].map(i => parseInt(n.slice(i, i + 2), 16));
  return v.some(Number.isNaN) ? null : v;
};
const aHex = v => '#' + v.map(x => Math.max(0, Math.min(255, Math.round(x))).toString(16).padStart(2, '0')).join('');
const claro = (rgb, t) => aHex(rgb.map(v => v + (255 - v) * t));   // mezcla con blanco
const oscuro = (rgb, f) => aHex(rgb.map(v => v * f));              // multiplica

function reglasExtra(deep) {
  const rgb = hexRGB(deep);
  if (!rgb) return '';
  const c = rgb.join(',');
  const luz = claro(rgb, 0.55);     // brillo del gradiente (era #f0dc9e)
  const medio = claro(rgb, 0.28);   // (era #e5c374)
  const hondo = oscuro(rgb, 0.72);  // (era #9a7431)
  const sombra = oscuro(rgb, 0.5);  // relieve del boton (era #6b5222)
  const tinta = oscuro(rgb, 0.13);  // texto sobre el boton (era #1c1408)
  return [
    `.text-shine{background:linear-gradient(110deg,${deep} 0%,${luz} 30%,${hondo} 52%,${deep} 75%,${medio} 100%);background-size:200% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}`,
    `.step-num{background:linear-gradient(180deg,${medio},${hondo});-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}`,
    `.stars{color:${deep};text-shadow:0 0 14px rgba(${c},0.45)}`,
    `.btn-3d{background:linear-gradient(180deg,${luz} 0%,${medio} 48%,${hondo} 100%);color:${tinta};box-shadow:inset 0 1px 0 rgba(255,255,255,0.3),inset 0 -2px 5px rgba(0,0,0,0.25),0 5px 0 ${sombra},0 12px 24px rgba(0,0,0,0.5)}`,
    `.btn-3d:hover{box-shadow:inset 0 1px 0 rgba(255,255,255,0.35),inset 0 -2px 5px rgba(0,0,0,0.25),0 7px 0 ${sombra},0 18px 34px rgba(0,0,0,0.55),0 0 40px rgba(${c},0.25)}`,
    `.btn-3d:active{box-shadow:inset 0 1px 0 rgba(255,255,255,0.25),inset 0 -1px 3px rgba(0,0,0,0.3),0 1px 0 ${sombra},0 4px 10px rgba(0,0,0,0.45)}`,
    `.dark-band .btn-3d{background:linear-gradient(180deg,${claro(rgb, 0.8)} 0%,${luz} 48%,${medio} 100%);color:${tinta};box-shadow:inset 0 1px 0 rgba(255,255,255,0.55),inset 0 -2px 5px rgba(0,0,0,0.2),0 5px 0 ${oscuro(rgb, 0.65)},0 12px 24px rgba(0,0,0,0.45)}`,
    `.book-float{background:linear-gradient(180deg,${luz} 0%,${medio} 48%,${hondo} 100%);box-shadow:0 6px 0 ${sombra},0 14px 30px rgba(0,0,0,0.5)}`,
    `.book-float:hover{box-shadow:0 8px 0 ${sombra},0 20px 40px rgba(0,0,0,0.55),0 0 34px rgba(${c},0.35)}`,
    `.book-float svg{stroke:${tinta}}`,
    `#scroll-progress{background:linear-gradient(90deg,${hondo} 0%,${deep} 45%,${luz} 100%)}`,
    `.merktop-dot{background:${deep}}`,
  ].join('');
}

async function estiloDe(env, slug) {
  if (!slug || !/^[a-z0-9-]{1,40}$/.test(slug)) return null;
  let p;
  try {
    p = await env.DOMAIN_MAP.get('color:' + slug, 'json');
  } catch (_) { return null; }
  if (!p || typeof p !== 'object') return null;
  const reglas = TOKENS
    .filter(t => typeof p[t] === 'string' && COLOR_OK.test(p[t].trim()))
    .map(t => `--accent-${t}:${p[t].trim()}`);
  if (!reglas.length) return null;
  const deep = typeof p.deep === 'string' && /^#[0-9a-f]{3,8}$/i.test(p.deep.trim()) ? p.deep.trim() : null;
  // Un solo bloque al final del head gana por orden de cascada sin tocar el resto del CSS.
  return `<style id="sf-color">:root{${reglas.join(';')}}${deep ? reglasExtra(deep) : ''}</style>`;
}

class InyectarColor {
  constructor(css) { this.css = css; }
  element(el) { el.append(this.css, { html: true }); }
}

// og:image ABSOLUTA: WhatsApp, iMessage y SMS solo muestran la tarjeta con foto del link si
// og:image es una URL absoluta, y los sites la llevan relativa ("assets/raw/bk-8.jpg"), asi
// que el preview salia sin imagen en TODOS. Se corrige al servir, sin reconstruir ninguno.
class OgAbsoluta {
  constructor(base) { this.base = base; }
  element(el) {
    const prop = el.getAttribute('property');
    if (prop === 'og:image') {
      const v = el.getAttribute('content') || '';
      if (v && !/^https?:\/\//i.test(v)) el.setAttribute('content', this.base + v.replace(/^\.?\//, ''));
    } else if (prop === 'og:url') {
      el.setAttribute('content', this.base);
    }
  }
}

// Cada demo historico trae una copia del compilador de Tailwind (451 KB) en
// <slug>/assets/tailwind.js. Antes el navegador descargaba y EJECUTABA ese
// compilador en cada demo: una tarea costosa que bloqueaba el render. Ahora se
// reemplaza por un CSS ya compilado, compartido y versionado por contenido.
class EstilosCompartidos {
  element(el) {
    el.replace(
      `<link rel="stylesheet" href="/_shared/tailwind.css?v=${SHARED_STYLE_REV}">`,
      { html: true },
    );
  }
}

async function servirEstiloCompartido(env, req) {
  const res = await env.ASSETS.fetch(req);
  const headers = new Headers(res.headers);
  // La URL lleva la huella del contenido, asi que puede vivir en la cache del
  // navegador sin revalidacion. Si el CSS cambia, cambia tambien la URL.
  headers.set('cache-control', 'public, max-age=31536000, immutable');
  return new Response(res.body, {
    status: res.status,
    statusText: res.statusText,
    headers,
  });
}

// La mayoría de las galerías históricas no declaraban loading="lazy". Eso
// iniciaba descargas de todas sus fotos (y de varios vídeos) aunque estuvieran
// muchos scrolls por debajo del primer pantallazo. Los dos primeros <img> se
// conservan prioritarios para logo/hero; el resto se difiere de forma nativa.
class MediosDiferidos {
  constructor() {
    this.imagenes = 0;
    this.tieneAutoplay = false;
  }

  imagen(el) {
    this.imagenes += 1;
    if (!el.hasAttribute('decoding')) el.setAttribute('decoding', 'async');
    if (!el.hasAttribute('loading')) {
      if (this.imagenes <= 2) {
        if (this.imagenes === 2) el.setAttribute('fetchpriority', 'high');
      } else {
        el.setAttribute('loading', 'lazy');
        el.setAttribute('fetchpriority', 'low');
      }
    }
  }

  video(el) {
    if (!el.hasAttribute('autoplay')) return;
    this.tieneAutoplay = true;
    el.removeAttribute('autoplay');
    el.setAttribute('preload', 'none');
    el.setAttribute('data-sf-autoplay', '');
  }

  end(end) {
    if (!this.tieneAutoplay) return;
    end.append(
      `<script>(function(){var q='video[data-sf-autoplay]';if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting){v.play().catch(function(){});}else{v.pause();}});},{rootMargin:'300px 0px'});document.querySelectorAll(q).forEach(function(v){io.observe(v);});})();</script>`,
      { html: true },
    );
  }
}

function reescritorDeDemo(css, origen) {
  const medios = new MediosDiferidos();
  let rw = new HTMLRewriter()
    .on('img', { element: el => medios.imagen(el) })
    .on('video', { element: el => medios.video(el) })
    .onDocument({ end: end => medios.end(end) })
    .on('script[src="assets/tailwind.js"]', new EstilosCompartidos());
  if (css) rw = rw.on('head', new InyectarColor(css));
  if (origen) rw = rw.on('meta[property^="og:"]', new OgAbsoluta(origen));
  return rw;
}

// Huella corta y estable del CSS inyectado, para meterla en el ETag.
function huella(s) {
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h * 33) ^ s.charCodeAt(i)) >>> 0;
  return h.toString(36);
}

async function servir(env, req, slug) {
  const css = await estiloDe(env, slug);
  const origen = slug ? `https://siteforge-demos.odd-forest-9504.workers.dev/${slug}/` : null;
  // Sin color, el HTML igual pasa por el rewriter para absolutizar og:image (el preview de
  // WhatsApp/iMessage no funciona con rutas relativas); lo no-HTML no se toca.
  if (!css) {
    const res0 = await env.ASSETS.fetch(req);
    const tipo0 = res0.headers.get('content-type') || '';
    if (!tipo0.includes('text/html') || !origen) return res0;
    return reescritorDeDemo(null, origen).transform(res0);
  }

  // EL BUG QUE ESTO ARREGLA (2026-08-12): el HTMLRewriter cambia el BODY pero conservaba los
  // headers del asset, incluido su ETag. Al recargar, el navegador mandaba If-None-Match con
  // el ETag del HTML SIN color, el asset no habia cambiado y Cloudflare respondia 304: el
  // navegador se quedaba con su copia vieja. El color solo se veia en la primera visita, y
  // al volver a abrir el sitio parecia que el cambio no habia hecho nada.
  // Solucion: pedir el asset sin cabeceras condicionales (para tener siempre body que
  // transformar) y devolverlo con un ETag propio que incluye la huella del color, de modo que
  // el navegador siga cacheando pero revalide en cuanto el color cambie.
  const h = new Headers(req.headers);
  h.delete('if-none-match');
  h.delete('if-modified-since');
  const res = await env.ASSETS.fetch(new Request(req.url, { method: req.method, headers: h }));
  const tipo = res.headers.get('content-type') || '';
  if (!tipo.includes('text/html')) return res;

  const salida = new Headers(res.headers);
  const base = (salida.get('etag') || 'sf').replace(/[^A-Za-z0-9._-]/g, '');
  salida.set('etag', `"${base}-c${huella(css)}"`);
  const rw = reescritorDeDemo(css, origen);
  return rw.transform(
    new Response(res.body, { status: res.status, statusText: res.statusText, headers: salida }));
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const host = url.hostname;

    // Esta ruta comun no pertenece a un slug. Debe resolverse antes del
    // enrutado workers.dev; de otro modo caerá en servir(..., null) y se
    // perderá la politica de cache inmutable.
    if (url.pathname === '/_shared/tailwind.css') return servirEstiloCompartido(env, req);
    // Fallback para HTML que algun navegador pudo haber dejado en cache antes
    // del cambio a CSS precompilado.
    if (url.pathname === '/_shared/tailwind.js') return env.ASSETS.fetch(req);

    // workers.dev = comportamiento por path original (sin lookup de dominio)
    if (host.endsWith('.workers.dev')) {
      const m = url.pathname.match(/^\/([a-z0-9-]{1,40})(?:\/|$)/);
      return servir(env, req, m ? m[1] : null);
    }

    // Dominio propio: buscar el slug mapeado
    let slug = null;
    try {
      slug = await env.DOMAIN_MAP.get('domain:' + host);
    } catch (_) { /* KV no disponible: cae a servir tal cual */ }

    if (slug && /^[a-z0-9-]{1,40}$/.test(slug)) {
      let p = url.pathname;
      if (p === '/' || p === '') {
        p = '/' + slug + '/';
      } else if (!p.startsWith('/' + slug + '/')) {
        p = '/' + slug + p;
      }
      const rewritten = new URL(req.url);
      rewritten.pathname = p;
      return servir(env, new Request(rewritten.toString(), req), slug);
    }

    // Dominio no mapeado: servir assets normales (404 si no existe)
    return env.ASSETS.fetch(req);
  },
};
