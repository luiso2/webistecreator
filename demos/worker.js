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
  // Un solo :root al final del head gana por orden de cascada sin tocar el resto del CSS.
  return `<style id="sf-color">:root{${reglas.join(';')}}</style>`;
}

class InyectarColor {
  constructor(css) { this.css = css; }
  element(el) { el.append(this.css, { html: true }); }
}

async function servir(env, req, slug) {
  const res = await env.ASSETS.fetch(req);
  const tipo = res.headers.get('content-type') || '';
  if (!tipo.includes('text/html')) return res;
  const css = await estiloDe(env, slug);
  if (!css) return res;
  return new HTMLRewriter().on('head', new InyectarColor(css)).transform(res);
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const host = url.hostname;

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
