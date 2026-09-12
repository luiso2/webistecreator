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
const SLUG_OK = /^[a-z0-9-]{1,40}$/;
const VERSION_OK = /^[a-f0-9]{64}$/;
const MAX_FILE_BYTES = 15 * 1024 * 1024;
const MAX_BUNDLE_FILES = 160;

function rutaValida(path) {
  return typeof path === 'string' && path.length > 0 && path.length <= 240
    && !path.startsWith('/') && !path.includes('..')
    && /^[A-Za-z0-9._/-]+$/.test(path);
}

async function sha256Hex(value) {
  const digest = await crypto.subtle.digest('SHA-256', value);
  return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
}

async function secretoValido(provided, expected) {
  if (!provided || !expected) return false;
  const encoder = new TextEncoder();
  const [a, b] = await Promise.all([
    crypto.subtle.digest('SHA-256', encoder.encode(provided)),
    crypto.subtle.digest('SHA-256', encoder.encode(expected)),
  ]);
  const left = new Uint8Array(a);
  const right = new Uint8Array(b);
  let difference = 0;
  for (let index = 0; index < left.length; index += 1) difference |= left[index] ^ right[index];
  return difference === 0;
}

function json(data, status = 200) {
  return Response.json(data, {
    status,
    headers: { 'cache-control': 'no-store' },
  });
}

function versionPrefix(slug, version) {
  return `sites/${slug}/versions/${version}/`;
}

async function publicarArchivo(req, env, url) {
  const slug = url.searchParams.get('slug') || '';
  const version = url.searchParams.get('version') || '';
  const path = url.searchParams.get('path') || '';
  if (!SLUG_OK.test(slug) || !VERSION_OK.test(version) || !rutaValida(path)) {
    return json({ ok: false, error: 'Ruta de bundle invalida.' }, 400);
  }
  const length = Number(req.headers.get('content-length') || 0);
  if (length > MAX_FILE_BYTES) return json({ ok: false, error: 'Archivo demasiado grande.' }, 413);
  const body = await req.arrayBuffer();
  if (body.byteLength > MAX_FILE_BYTES) return json({ ok: false, error: 'Archivo demasiado grande.' }, 413);
  const actualSha = await sha256Hex(body);
  const expectedSha = (req.headers.get('x-siteforge-sha256') || '').toLowerCase();
  if (!VERSION_OK.test(expectedSha) || actualSha !== expectedSha) {
    return json({ ok: false, error: 'Checksum del archivo no coincide.' }, 400);
  }
  const key = versionPrefix(slug, version) + path;
  const object = await env.DEMO_BUNDLES.put(key, body, {
    httpMetadata: {
      contentType: req.headers.get('content-type') || 'application/octet-stream',
      cacheControl: 'public, max-age=31536000, immutable',
    },
    customMetadata: { sha256: actualSha },
    sha256: actualSha,
  });
  if (!object) return json({ ok: false, error: 'R2 no confirmo la escritura.' }, 502);
  return json({ ok: true, path, size: body.byteLength, sha256: actualSha });
}

async function finalizarPublicacion(req, env, origin) {
  let payload;
  try {
    payload = await req.json();
  } catch (_) {
    return json({ ok: false, error: 'Manifest JSON invalido.' }, 400);
  }
  const slug = String(payload?.slug || '');
  const version = String(payload?.version || '');
  const files = Array.isArray(payload?.files) ? payload.files : [];
  if (!SLUG_OK.test(slug) || !VERSION_OK.test(version) || files.length < 1 || files.length > MAX_BUNDLE_FILES) {
    return json({ ok: false, error: 'Manifest invalido.' }, 400);
  }
  const normalized = [];
  const seen = new Set();
  for (const entry of files) {
    const path = String(entry?.path || '');
    const size = Number(entry?.size);
    const sha256 = String(entry?.sha256 || '').toLowerCase();
    if (!rutaValida(path) || seen.has(path) || !Number.isSafeInteger(size) || size < 0
        || size > MAX_FILE_BYTES || !VERSION_OK.test(sha256)) {
      return json({ ok: false, error: `Entrada de manifest invalida: ${path.slice(0, 80)}` }, 400);
    }
    seen.add(path);
    normalized.push({ path, size, sha256, contentType: String(entry?.contentType || 'application/octet-stream') });
  }
  if (!seen.has('index.html')) return json({ ok: false, error: 'El bundle no contiene index.html.' }, 400);

  const prefix = versionPrefix(slug, version);
  for (let offset = 0; offset < normalized.length; offset += 12) {
    const batch = normalized.slice(offset, offset + 12);
    const heads = await Promise.all(batch.map(entry => env.DEMO_BUNDLES.head(prefix + entry.path)));
    for (let index = 0; index < batch.length; index += 1) {
      const entry = batch[index];
      const object = heads[index];
      if (!object || object.size !== entry.size || object.customMetadata?.sha256 !== entry.sha256) {
        return json({ ok: false, error: `Archivo ausente o corrupto: ${entry.path}` }, 409);
      }
    }
  }

  const publishedAt = new Date().toISOString();
  const manifest = {
    schemaVersion: 1,
    slug,
    version,
    publishedAt,
    files: normalized.map(entry => ({
      ...entry,
      url: `${origin}/_siteforge/assets/${slug}/${version}/${entry.path}`,
    })),
  };
  const manifestKey = prefix + 'manifest.json';
  await env.DEMO_BUNDLES.put(manifestKey, JSON.stringify(manifest), {
    httpMetadata: { contentType: 'application/json; charset=UTF-8', cacheControl: 'public, max-age=31536000, immutable' },
  });
  // R2 is strongly consistent. This final write is the atomic cutover: readers
  // never see the new version until every object above has been verified.
  await env.DEMO_BUNDLES.put(`sites/${slug}/current.json`, JSON.stringify({ ...manifest, manifestKey }), {
    httpMetadata: { contentType: 'application/json; charset=UTF-8', cacheControl: 'no-store' },
  });
  return json({
    ok: true,
    url: `${origin}/${slug}/`,
    manifestUrl: `${origin}/_siteforge/manifests/${slug}/${version}.json`,
    version,
    files: normalized.length,
  });
}

async function manejarPublicacion(req, env, url) {
  const valid = await secretoValido(req.headers.get('x-siteforge-publish-key') || '', env.SITEFORGE_PUBLISH_KEY || '');
  if (!valid) return json({ ok: false, error: 'No autorizado.' }, 401);
  if (req.method === 'PUT' && url.pathname === '/__siteforge/publish/file') {
    return publicarArchivo(req, env, url);
  }
  if (req.method === 'POST' && url.pathname === '/__siteforge/publish/finalize') {
    return finalizarPublicacion(req, env, url.origin);
  }
  return json({ ok: false, error: 'Ruta de publicacion no encontrada.' }, 404);
}

async function objetoR2Response(req, object, immutable) {
  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set('etag', object.httpEtag);
  headers.set('cache-control', immutable ? 'public, max-age=31536000, immutable' : 'public, max-age=30, must-revalidate');
  if (req.headers.get('if-none-match') === object.httpEtag) return new Response(null, { status: 304, headers });
  return new Response(req.method === 'HEAD' ? null : object.body, { headers });
}

async function manifestActual(env, slug) {
  if (!SLUG_OK.test(slug)) return null;
  const object = await env.DEMO_BUNDLES.get(`sites/${slug}/current.json`);
  if (!object) return null;
  try {
    const manifest = await object.json();
    return VERSION_OK.test(manifest?.version || '') ? manifest : null;
  } catch (_) {
    return null;
  }
}

async function servirR2Inmutable(req, env, url) {
  const match = url.pathname.match(/^\/_siteforge\/assets\/([a-z0-9-]{1,40})\/([a-f0-9]{64})\/(.+)$/);
  if (!match || !rutaValida(match[3])) return null;
  const object = await env.DEMO_BUNDLES.get(versionPrefix(match[1], match[2]) + match[3]);
  return object ? objetoR2Response(req, object, true) : new Response('Not found', { status: 404 });
}

async function servirManifestR2(req, env, url) {
  const match = url.pathname.match(/^\/_siteforge\/manifests\/([a-z0-9-]{1,40})\/([a-f0-9]{64})\.json$/);
  if (!match) return null;
  const object = await env.DEMO_BUNDLES.get(versionPrefix(match[1], match[2]) + 'manifest.json');
  return object ? objetoR2Response(req, object, true) : new Response('Not found', { status: 404 });
}

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

class AssetInmutable {
  constructor(attribute, base) {
    this.attribute = attribute;
    this.base = base;
  }
  element(el) {
    const value = el.getAttribute(this.attribute) || '';
    if (!value || value === 'assets/tailwind.js' || value === './assets/tailwind.js') return;
    const clean = value.replace(/^\.\//, '');
    if (clean.startsWith('assets/')) el.setAttribute(this.attribute, this.base + clean);
  }
}

async function servirEstiloCompartido(env, req) {
  const shared = await env.DEMO_BUNDLES.get('shared/tailwind.css');
  if (shared) return objetoR2Response(req, shared, true);
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

function reescritorDeDemo(css, origen, assetBase = null) {
  const medios = new MediosDiferidos();
  let rw = new HTMLRewriter()
    .on('img', { element: el => medios.imagen(el) })
    .on('video', { element: el => medios.video(el) })
    .onDocument({ end: end => medios.end(end) })
    .on('script[src="assets/tailwind.js"]', new EstilosCompartidos());
  if (assetBase) {
    rw = rw
      .on('img[src]', new AssetInmutable('src', assetBase))
      .on('source[src]', new AssetInmutable('src', assetBase))
      .on('video[src]', new AssetInmutable('src', assetBase))
      .on('video[poster]', new AssetInmutable('poster', assetBase))
      .on('script[src]', new AssetInmutable('src', assetBase))
      .on('link[href]', new AssetInmutable('href', assetBase));
  }
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
  let r2 = null;
  let current = null;
  if (slug && SLUG_OK.test(slug)) {
    current = await manifestActual(env, slug);
    if (current) {
      const url = new URL(req.url);
      let relative = url.pathname.replace(new RegExp(`^/${slug}/?`), '');
      if (!relative) relative = 'index.html';
      if (rutaValida(relative)) {
        const object = await env.DEMO_BUNDLES.get(versionPrefix(slug, current.version) + relative);
        if (object) r2 = await objetoR2Response(req, object, false);
      }
    }
  }
  if (r2) {
    const tipo = r2.headers.get('content-type') || '';
    if (!tipo.includes('text/html') || !origen || req.method === 'HEAD') return r2;
    const headers = new Headers(r2.headers);
    const base = (headers.get('etag') || 'sf').replace(/[^A-Za-z0-9._-]/g, '');
    headers.set('etag', `"${base}${css ? `-c${huella(css)}` : ''}"`);
    headers.set('cache-control', 'no-cache');
    const assetBase = `/_siteforge/assets/${slug}/${current.version}/`;
    return reescritorDeDemo(css, origen, assetBase).transform(
      new Response(r2.body, { status: r2.status, statusText: r2.statusText, headers }),
    );
  }
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

// A new site is committed to GitHub before Workers Builds finishes uploading the
// asset bundle. During that short window the slug is valid but ASSETS returns 404,
// which made the panel look broken and encouraged users to retry the same build.
// Keep real missing files as 404s, but give the canonical site root a small,
// uncached readiness page while the next asset deployment is propagating.
function demoEnConstruccion(slug) {
  const safeSlug = String(slug).replace(/[^a-z0-9-]/g, '');
  return new Response(`<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="15"><title>Preparando tu demo</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#111;color:#f5f1e8;font:16px system-ui,sans-serif;text-align:center}main{max-width:34rem;padding:2rem}h1{font-size:clamp(1.8rem,5vw,3rem);margin:0 0 1rem}p{line-height:1.6;color:#c9c3b8}.dot{display:inline-block;width:.65rem;height:.65rem;border-radius:50%;background:#d7b56d;box-shadow:0 0 18px #d7b56d;margin:.2rem}</style></head><body><main><div aria-hidden="true"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div><h1>Tu demo se está preparando</h1><p>La página de <strong>${safeSlug}</strong> ya fue publicada y estará disponible en unos segundos. Esta pantalla se actualizará automáticamente.</p></main></body></html>`, {
    status: 200,
    headers: { 'content-type': 'text/html; charset=UTF-8', 'cache-control': 'no-store', 'x-siteforge-demo-status': 'building' },
  });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const host = url.hostname;

    if (url.pathname.startsWith('/__siteforge/publish/')) return manejarPublicacion(req, env, url);
    const immutable = await servirR2Inmutable(req, env, url);
    if (immutable) return immutable;
    const manifest = await servirManifestR2(req, env, url);
    if (manifest) return manifest;

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
      const slug = m ? m[1] : null;
      const response = await servir(env, req, slug);
      if (slug && req.method === 'GET' && (url.pathname === `/${slug}` || url.pathname === `/${slug}/`) && response.status === 404) {
        return demoEnConstruccion(slug);
      }
      return response;
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
