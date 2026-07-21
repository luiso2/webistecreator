// Worker de demos: sirve los sitios de output/ como assets estaticos.
// - En workers.dev (path-based): siteforge-demos.../<slug>/ -> se sirve tal cual.
// - En un dominio propio comprado desde el panel: se mapea el hostname -> slug via KV
//   (llave "domain:<hostname>" escrita por el panel al comprar) y se reescribe la ruta a
//   /<slug>/... para servir ese sitio en la raiz del dominio. SSL lo pone Cloudflare solo.
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const host = url.hostname;

    // workers.dev = comportamiento por path original (sin lookup, rapido)
    if (host.endsWith('.workers.dev')) return env.ASSETS.fetch(req);

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
      return env.ASSETS.fetch(new Request(rewritten.toString(), req));
    }

    // Dominio no mapeado: servir assets normales (404 si no existe)
    return env.ASSETS.fetch(req);
  },
};
