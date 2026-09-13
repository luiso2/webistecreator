import { DurableObject } from 'cloudflare:workers';
import {
  TOOL_DEFINITIONS,
  assertSiteSpec,
  businessIdentityKeys,
  businessesShareIdentity,
  deepMerge,
  googleMapsIdentity,
  normalizeRef,
  normalizeSlug,
  permissionForPlan,
  sanitizePatch,
  siteSpecFromRegistry,
  toolDefinition,
  validatePlan,
} from './control-plane.mjs';
import { inferLeadSource, normalizeInstagramHandle } from './public/social-channels.mjs';
import { cleanMessage, repairDemoSeparator } from './public/outreach-message.mjs';
import { boundedBody, verifyTelnyxWebhook } from './telnyx.mjs';
export { OutreachCampaign } from './outreach.js';

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8' },
  });

// Solo se aceptan URLs de demo dentro de la cuenta Cloudflare del usuario.
const DEMO_URL_RE = /^https:\/\/[a-z0-9-]+\.odd-forest-9504\.workers\.dev(\/[a-z0-9-]*\/?)?$/;

// Quita angle brackets y caracteres de control de texto que entra por endpoints publicos,
// como defensa en profundidad contra inyeccion (el front igual escapa todo al renderizar).
const stripUnsafe = s => String(s).replace(/[<>\x00-\x1F\x7F]/g, "");

// Texto que viene del panel y acaba guardado en KV. Ademas de evitar markup, se colapsan
// espacios para que dos filtros iguales no creen trabajos duplicados por un espacio extra.
const queueText = (value, max) => stripUnsafe(value ?? '').trim().replace(/\s+/g, ' ').slice(0, max);
const discoveryKey = request => [request?.niche, request?.location, request?.language || 'auto']
  .map(v => String(v || '').toLocaleLowerCase()).join('|');
const directBuildKey = input => `direct:${String(input || '').normalize('NFKD')
  .replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()}`;
const publicBusinessSite = site => ({
  slug: site?.slug || null,
  name: site?.name || null,
  city: site?.city || null,
  phone: site?.phone || null,
  url_demo: typeof site?.url_demo === 'string' && DEMO_URL_RE.test(site.url_demo) ? site.url_demo : null,
  maps_url: site?.maps_url || null,
  business_key: site?.business_key || null,
});
const cleanBusinessCandidate = (raw, fallbackIndex = 0) => {
  raw = raw && typeof raw === 'object' && !Array.isArray(raw) ? raw : {};
  const name = queueText(raw.name, 120);
  const location = queueText(raw.location || raw.city, 100);
  const proposedSlug = queueText(raw.slug, 64).toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40);
  const derivedSlug = name.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '')
    .replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40);
  const mapsUrl = typeof raw.maps_url === 'string' && googleMapsIdentity(raw.maps_url)
    ? raw.maps_url.slice(0, 600) : undefined;
  const businessKey = typeof raw.business_key === 'string'
    ? raw.business_key.toLowerCase().replace(/[^a-z0-9:|._-]/g, '').slice(0, 220) : undefined;
  return {
    index: Number.isInteger(raw.index) && raw.index >= 0 && raw.index < 100 ? raw.index : fallbackIndex,
    name,
    slug: proposedSlug || derivedSlug || undefined,
    location,
    city: location,
    niche: queueText(raw.niche, 100) || undefined,
    phone: queueText(raw.phone, 30) || undefined,
    maps_url: mapsUrl,
    business_key: businessKey || undefined,
    language: ['es', 'en'].includes(String(raw.language || '').toLowerCase())
      ? String(raw.language).toLowerCase() : undefined,
  };
};
// Railway corta cada forja a los 510 s. A los nueve minutos desde started_at la
// ejecución ya rebasó ese presupuesto y se puede rescatar aunque su último heartbeat
// haya ocurrido cerca del final.
const STALE_FORGE_MS = 9 * 60 * 1000;
const BUSINESS_PUBLISHED_EXPIRES_AT = 4_102_444_800_000; // 2100-01-01
const isStaleForge = (item, now) => item?.status === 'processing'
  && now - Date.parse(item.started_at || item.created) >= STALE_FORGE_MS;

// KV sirve para el estado y el historial, pero no ofrece un compare-and-set para
// cuatro réplicas de Railway. Este objeto único serializa reclamos Y mutaciones de
// cola/registro, evitando tanto dobles builds como actualizaciones que se pisan.
export class QueueClaims extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    ctx.blockConcurrencyWhile(async () => {
      ctx.storage.sql.exec('CREATE TABLE IF NOT EXISTS claims (id TEXT PRIMARY KEY, expires_at INTEGER NOT NULL)');
      ctx.storage.sql.exec(`CREATE TABLE IF NOT EXISTS active_jobs (
        id TEXT PRIMARY KEY,
        token TEXT NOT NULL,
        expires_at INTEGER NOT NULL
      )`);
      ctx.storage.sql.exec(`CREATE TABLE IF NOT EXISTS business_reservations (
        identity_key TEXT PRIMARY KEY,
        job_id TEXT NOT NULL,
        claim_token TEXT NOT NULL,
        slug TEXT,
        status TEXT NOT NULL,
        expires_at INTEGER NOT NULL,
        site_json TEXT,
        updated_at INTEGER NOT NULL
      )`);
      ctx.storage.sql.exec('CREATE INDEX IF NOT EXISTS idx_business_reservations_job ON business_reservations(job_id, status)');
    });
  }

  async claim(id, now, ttl) {
    return this.ctx.blockConcurrencyWhile(async () => {
      const row = this.ctx.storage.sql.exec('SELECT expires_at FROM claims WHERE id = ?', id).toArray()[0];
      if (row && Number(row.expires_at) > now) return { ok: false, error: 'item ya reclamado' };
      const queue = (await this.env.SITEFORGE_KV.get('queue', 'json')) || [];
      let item;
      const updated = queue.map(q => {
        if (q.id !== id || (q.status !== 'pending' && !isStaleForge(q, now))) return q;
        const claimToken = crypto.randomUUID();
        item = {
          id: q.id, input: q.input, request: q.request, created: q.created, claim_token: claimToken,
          ...(q.candidate ? { candidate: q.candidate } : {}),
          ...(['es', 'en'].includes(q.language) ? { language: q.language } : {}),
        };
        return {
          ...q, status: 'processing', stage: 'research', stage_at: new Date(now).toISOString(),
          started_at: new Date(now).toISOString(), note: 'Forja iniciada', claim_token: claimToken,
        };
      });
      if (!item) return { ok: false, error: 'item ya reclamado' };
      await this.env.SITEFORGE_KV.put('queue', JSON.stringify(updated));
      this.ctx.storage.sql.exec(
        'INSERT INTO claims (id, expires_at) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET expires_at = excluded.expires_at',
        id, now + ttl,
      );
      this.ctx.storage.sql.exec(
        'INSERT INTO active_jobs (id, token, expires_at) VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET token = excluded.token, expires_at = excluded.expires_at',
        id, item.claim_token, now + ttl,
      );
      return { ok: true, item };
    });
  }

  async progress(id, token, stage, note, now) {
    return this.ctx.blockConcurrencyWhile(async () => {
      const queue = (await this.env.SITEFORGE_KV.get('queue', 'json')) || [];
      const item = queue.find(q => q.id === id && q.status === 'processing' && q.claim_token === token);
      if (!item) return { ok: false, error: 'item no activo' };
      const updated = queue.map(q => q.id === id ? {
        ...q, status: 'processing', stage, stage_at: new Date(now).toISOString(),
        started_at: q.started_at || new Date(now).toISOString(),
        note: typeof note === 'string' ? note.slice(0, 140) : q.note,
      } : q);
      await this.env.SITEFORGE_KV.put('queue', JSON.stringify(updated));
      return { ok: true };
    });
  }

  async done(id, token, result, now) {
    return this.ctx.blockConcurrencyWhile(async () => {
      const queue = (await this.env.SITEFORGE_KV.get('queue', 'json')) || [];
      if (!queue.some(q => q.id === id && q.status === 'processing' && q.claim_token === token)) {
        return { ok: false, error: 'item no pendiente' };
      }
      const updated = queue.map(q => q.id === id ? {
        ...q, status: result.failed === true ? 'failed' : 'done',
        done_at: new Date(now).toISOString(), result,
      } : q);
      await this.env.SITEFORGE_KV.put('queue', JSON.stringify(updated));
      this.ctx.storage.sql.exec('DELETE FROM claims WHERE id = ?', id);
      this.ctx.storage.sql.exec('DELETE FROM active_jobs WHERE id = ?', id);
      this.ctx.storage.sql.exec("DELETE FROM business_reservations WHERE job_id = ? AND status = 'building'", id);
      return { ok: true };
    });
  }

  async enqueue(item, discoveryKeyValue = null, operationKeyValue = null) {
    return this.ctx.blockConcurrencyWhile(async () => {
      const queue = (await this.env.SITEFORGE_KV.get('queue', 'json')) || [];
      if (queue.filter(q => q.status === 'pending').length >= QUEUE_PENDING_LIMIT) {
        return { ok: false, error: `cola llena (${QUEUE_PENDING_LIMIT} pendientes max)`, status: 429 };
      }
      if (discoveryKeyValue && queue.some(q => (q.status === 'pending' || q.status === 'processing')
        && q.request?.type === 'discovery' && discoveryKey(q.request) === discoveryKeyValue)) {
        return { ok: false, error: 'esa busqueda ya esta activa en la cola', status: 409 };
      }
      if (operationKeyValue && queue.some(q => (q.status === 'pending' || q.status === 'processing')
        && (q.request?.operation_key || (!q.request ? directBuildKey(q.input) : null)) === operationKeyValue)) {
        return { ok: false, error: 'esa operación ya está activa en la cola', status: 409 };
      }
      queue.push(item);
      await this.env.SITEFORGE_KV.put('queue', JSON.stringify(queue));
      return { ok: true, item };
    });
  }

  async retry(id, now) {
    return this.ctx.blockConcurrencyWhile(async () => {
      const queue = (await this.env.SITEFORGE_KV.get('queue', 'json')) || [];
      const item = queue.find(q => q.id === id);
      if (!item) return { ok: false, error: 'item no encontrado', status: 404 };
      const wasFailed = item.status === 'failed' || (item.status === 'done' && item.result?.failed === true);
      if (!wasFailed) return { ok: false, error: 'solo se pueden reintentar fallos', status: 409 };
      const retries = Number(item.retry_count || 0);
      // Publicacion/Builds son fallos transitorios; los filtros de Maps conservan
      // el limite corto para no repetir negocios que no cumplen los minimos.
      const transient = /demo no respondio|Subida a GitHub|Research Instagram/i.test(item.result?.motivo || '');
      const maxRetries = transient ? 5 : 3;
      if (retries >= maxRetries) return { ok: false, error: `este item ya tiene ${maxRetries} reintentos`, status: 409 };
      const stamp = new Date(now).toISOString();
      const updated = queue.map(q => q.id === id ? {
        ...q, status: 'pending', stage: null, stage_at: null, started_at: null, done_at: null,
        result: null, claim_token: null, note: 'Reintento solicitado desde el panel', retry_count: retries + 1, retry_at: stamp,
      } : q);
      await this.env.SITEFORGE_KV.put('queue', JSON.stringify(updated));
      this.ctx.storage.sql.exec('DELETE FROM claims WHERE id = ?', id);
      this.ctx.storage.sql.exec('DELETE FROM active_jobs WHERE id = ?', id);
      this.ctx.storage.sql.exec("DELETE FROM business_reservations WHERE job_id = ? AND status = 'building'", id);
      return { ok: true, retry_count: retries + 1 };
    });
  }

  async recover(id, now, minAge) {
    return this.ctx.blockConcurrencyWhile(async () => {
      const queue = (await this.env.SITEFORGE_KV.get('queue', 'json')) || [];
      const item = queue.find(q => q.id === id);
      if (!item) return { ok: false, error: 'item no encontrado', status: 404 };
      if (item.status !== 'processing') return { ok: false, error: 'el item no esta processing', status: 409 };
      const age = now - Date.parse(item.started_at || item.created);
      if (!Number.isFinite(age) || age < minAge) {
        return { ok: false, error: 'la ejecución aún está dentro de su presupuesto', status: 409 };
      }
      const stamp = new Date(now).toISOString();
      const updated = queue.map(q => q.id === id ? {
        ...q, status: 'pending', stage: null, stage_at: null, started_at: null, done_at: null,
        claim_token: null, note: 'Recuperado tras reinicio de la forja', recovered_at: stamp,
      } : q);
      await this.env.SITEFORGE_KV.put('queue', JSON.stringify(updated));
      this.ctx.storage.sql.exec('DELETE FROM claims WHERE id = ?', id);
      this.ctx.storage.sql.exec('DELETE FROM active_jobs WHERE id = ?', id);
      this.ctx.storage.sql.exec("DELETE FROM business_reservations WHERE job_id = ? AND status = 'building'", id);
      return { ok: true, recovered: true };
    });
  }

  activeJob(id, token, now, requireFresh = true) {
    const row = this.ctx.storage.sql.exec(
      'SELECT token, expires_at FROM active_jobs WHERE id = ?', id,
    ).toArray()[0];
    return Boolean(row && row.token === token && (!requireFresh || Number(row.expires_at) > now));
  }

  async reserveBusinesses(id, token, candidates, now, ttl) {
    let registry;
    if (!this.activeJob(id, token, now)) {
      // Compatibilidad durante el rollout: una fila reclamada por la versión anterior
      // aún no tiene active_jobs. Su token en KV permite incorporarla una sola vez.
      const [currentRegistry, queue] = await Promise.all([
        this.env.SITEFORGE_KV.get('registry', 'json'),
        this.env.SITEFORGE_KV.get('queue', 'json'),
      ]);
      const active = (queue || []).find(item => item.id === id
        && item.status === 'processing' && item.claim_token === token);
      if (!active) return { ok: false, error: 'item no activo', status: 409 };
      registry = currentRegistry || [];
      this.ctx.storage.sql.exec(
        'INSERT INTO active_jobs (id, token, expires_at) VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET token = excluded.token, expires_at = excluded.expires_at',
        id, token, now + ttl,
      );
    }
    // KV se lee antes de tocar las reservas. Tras este await se vuelve a validar el
    // claim; todas las comprobaciones/escrituras SQL posteriores quedan en el mismo
    // segmento síncrono y se confirman atómicamente por el output gate del DO.
    registry = registry || (await this.env.SITEFORGE_KV.get('registry', 'json')) || [];
    if (!this.activeJob(id, token, now)) return { ok: false, error: 'item no activo', status: 409 };
    this.ctx.storage.sql.exec(
      "DELETE FROM business_reservations WHERE status = 'building' AND expires_at <= ?", now,
    );
    const reserved = [];
    const skipped = [];

    for (const original of candidates.slice(0, 20)) {
      const candidate = { ...original };
      const requestedKey = candidate.business_key;
      const keys = businessIdentityKeys({ ...candidate, business_key: undefined });
      if (!keys.length) {
        skipped.push({ candidate, reason: 'identidad insuficiente' });
        continue;
      }
      candidate.business_key = keys.includes(requestedKey) ? requestedKey : keys[0];
      const existing = registry.find(site => businessesShareIdentity(candidate, site));
      if (existing) {
        const site = publicBusinessSite(existing);
        const siteJson = JSON.stringify(site);
        for (const key of new Set([...keys, ...businessIdentityKeys(existing)])) {
          this.ctx.storage.sql.exec(
            `INSERT INTO business_reservations
              (identity_key, job_id, claim_token, slug, status, expires_at, site_json, updated_at)
             VALUES (?, ?, ?, ?, 'published', ?, ?, ?)
             ON CONFLICT(identity_key) DO UPDATE SET
               slug = excluded.slug, status = 'published', expires_at = excluded.expires_at,
               site_json = excluded.site_json, updated_at = excluded.updated_at`,
            key, id, token, site.slug, BUSINESS_PUBLISHED_EXPIRES_AT, siteJson, now,
          );
        }
        skipped.push({ candidate, reason: 'ya existe en el registro', existing: site });
        continue;
      }

      const placeholders = keys.map(() => '?').join(',');
      const conflicts = this.ctx.storage.sql.exec(
        `SELECT job_id, claim_token, status, expires_at, site_json
         FROM business_reservations WHERE identity_key IN (${placeholders})`,
        ...keys,
      ).toArray().filter(row => row.status === 'published'
        || (Number(row.expires_at) > now && (row.job_id !== id || row.claim_token !== token)));
      if (conflicts.length) {
        const published = conflicts.find(row => row.status === 'published' && row.site_json);
        let existingSite = null;
        try { existingSite = published ? JSON.parse(published.site_json) : null; } catch { existingSite = null; }
        skipped.push({
          candidate,
          reason: published ? 'ya fue publicado' : 'otra forja ya lo está construyendo',
          ...(existingSite ? { existing: existingSite } : {}),
        });
        continue;
      }

      for (const key of keys) {
        this.ctx.storage.sql.exec(
          `INSERT INTO business_reservations
            (identity_key, job_id, claim_token, slug, status, expires_at, site_json, updated_at)
           VALUES (?, ?, ?, ?, 'building', ?, NULL, ?)
           ON CONFLICT(identity_key) DO UPDATE SET
             job_id = excluded.job_id, claim_token = excluded.claim_token, slug = excluded.slug,
             status = 'building', expires_at = excluded.expires_at, site_json = NULL,
             updated_at = excluded.updated_at`,
          key, id, token, candidate.slug || null, now + ttl, now,
        );
      }
      reserved.push(candidate);
    }
    return { ok: true, reserved, skipped };
  }

  completeBusiness(id, token, candidate, site, now) {
    if (!this.activeJob(id, token, now)) return { ok: false, error: 'item no activo', status: 409 };
    const keys = [...new Set([
      ...businessIdentityKeys({ ...candidate, business_key: undefined }),
      ...businessIdentityKeys({ ...site, business_key: undefined }),
    ])];
    if (!keys.length) return { ok: false, error: 'identidad insuficiente', status: 400 };
    const siteJson = JSON.stringify(publicBusinessSite(site));
    for (const key of keys) {
      const current = this.ctx.storage.sql.exec(
        'SELECT job_id, claim_token, status, site_json FROM business_reservations WHERE identity_key = ?', key,
      ).toArray()[0];
      if (current?.status === 'published' && (current.job_id !== id || current.claim_token !== token)) {
        let existing = null;
        try { existing = current.site_json ? JSON.parse(current.site_json) : null; } catch { existing = null; }
        return { ok: false, error: 'identidad ya publicada', status: 409, ...(existing ? { existing } : {}) };
      }
    }
    for (const key of keys) {
      this.ctx.storage.sql.exec(
        `INSERT INTO business_reservations
          (identity_key, job_id, claim_token, slug, status, expires_at, site_json, updated_at)
         VALUES (?, ?, ?, ?, 'published', ?, ?, ?)
         ON CONFLICT(identity_key) DO UPDATE SET
           job_id = excluded.job_id, claim_token = excluded.claim_token, slug = excluded.slug,
           status = 'published', expires_at = excluded.expires_at,
           site_json = excluded.site_json, updated_at = excluded.updated_at`,
        key, id, token, site.slug || candidate.slug || null,
        BUSINESS_PUBLISHED_EXPIRES_AT, siteJson, now,
      );
    }
    return { ok: true, business_key: candidate.business_key || keys[0] };
  }

  releaseBusiness(id, token, candidate, now) {
    if (!this.activeJob(id, token, now, false)) return { ok: false, error: 'item no activo', status: 409 };
    const keys = businessIdentityKeys(candidate);
    for (const key of keys) {
      this.ctx.storage.sql.exec(
        "DELETE FROM business_reservations WHERE identity_key = ? AND job_id = ? AND claim_token = ? AND status = 'building'",
        key, id, token,
      );
    }
    return { ok: true, released: keys.length };
  }

  async registryUpsert(limpio) {
    return this.ctx.blockConcurrencyWhile(async () => {
      const registry = (await this.env.SITEFORGE_KV.get('registry', 'json')) || [];
      const exactSlug = registry.findIndex(b => b.slug === limpio.slug);
      const identityMatch = exactSlug >= 0 ? exactSlug : registry.findIndex(b => businessesShareIdentity(limpio, b));
      if (identityMatch >= 0 && registry[identityMatch].slug !== limpio.slug) {
        return {
          ok: true,
          duplicate: true,
          skipped: 'la identidad ya existe con otro slug',
          existing: publicBusinessSite(registry[identityMatch]),
        };
      }
      const idx = identityMatch;
      if (idx >= 0) {
        const actual = registry[idx];
        if (actual.outreach === 'sent') return { ok: true, skipped: 'ya contactado' };
        if (actual.outreach === 'skip_duplicate') return { ok: true, skipped: 'marcado como duplicado' };
        const nuevo = Object.fromEntries(Object.entries(limpio).filter(([, v]) => v !== undefined));
        delete nuevo.outreach;
        registry[idx] = { ...actual, ...nuevo };
      } else {
        if (registry.length >= REGISTRY_LIMIT) return { ok: false, error: 'registro lleno', status: 429 };
        const nuevo = Object.fromEntries(Object.entries(limpio).filter(([, v]) => v !== undefined));
        if (!nuevo.business_key) {
          nuevo.business_key = businessIdentityKeys({ ...nuevo, business_key: undefined })[0];
        }
        registry.push({
          name: limpio.slug, outreach: 'pending_manual', status: 'staging', language: 'es',
          fecha: new Date().toISOString().slice(0, 10), ...nuevo,
        });
      }
      await this.env.SITEFORGE_KV.put('registry', JSON.stringify(registry));
      return { ok: true, count: registry.length };
    });
  }

  async markOutreachSent(slug, providerId, at, channel = 'email') {
    return this.ctx.blockConcurrencyWhile(async () => {
      const registry = (await this.env.SITEFORGE_KV.get('registry', 'json')) || [];
      const sentLog = (await this.env.SITEFORGE_KV.get('sent_log', 'json')) || {};
      sentLog[slug] = at;
      await this.env.SITEFORGE_KV.put('sent_log', JSON.stringify(sentLog));
      await this.env.SITEFORGE_KV.put('registry', JSON.stringify(registry.map(b => b.slug === slug
        ? { ...b, outreach: 'sent', ...(channel === 'sms' ? { telnyx_id: providerId } : { resend_id: providerId }) } : b)));
      return { ok: true };
    });
  }

  async audit(event) {
    return this.ctx.blockConcurrencyWhile(async () => {
      const index = (await this.env.SITEFORGE_KV.get('control:audit:index', 'json')) || [];
      const ids = [event.id, ...index.filter(id => id !== event.id)].slice(0, 500);
      await this.env.SITEFORGE_KV.put(`control:audit:${event.id}`, JSON.stringify(event));
      await this.env.SITEFORGE_KV.put('control:audit:index', JSON.stringify(ids));
      return { ok: true, id: event.id };
    });
  }

  release(id) {
    this.ctx.storage.sql.exec('DELETE FROM claims WHERE id = ?', id);
    this.ctx.storage.sql.exec('DELETE FROM active_jobs WHERE id = ?', id);
    this.ctx.storage.sql.exec("DELETE FROM business_reservations WHERE job_id = ? AND status = 'building'", id);
    return true;
  }
}
// La meta operativa es 10.000 demos. KV admite un registro bastante mayor que
// el límite histórico de 800; dejamos margen para no bloquear la forja al llegar
// a la meta y para conservar los datos CRM en la misma lista.
const REGISTRY_LIMIT = 12000;
const QUEUE_PENDING_LIMIT = 20;

// SHA-256 del access key (el key real vive solo en el .env local del usuario)
const KEY_HASH = 'b1e35fb9b55f29a4272b16173553f5f92b19b0b824ddb3d9789f28332bd4bf06';
// Clave independiente para el GPT de Siteforge. Nunca reutilizar x-sf-key en un GPT:
// el secreto del Action podria acabar dando acceso a todo el panel administrativo.
const AGENT_KEY_HASH = 'fcee22ff252c2cb328ec9a43f0abf249af79ec671db61fb3c8bd86fb889c51d2';

async function isAuthorized(req) {
  const key = req.headers.get('x-sf-key') || '';
  if (!key) return false;
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(key));
  const hex = [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
  return safeEqualHex(hex, KEY_HASH);
}

async function isAgentAuthorized(req) {
  const key = req.headers.get('x-siteforge-agent-key') || '';
  if (!key) return false;
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(key));
  const hex = [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
  return safeEqualHex(hex, AGENT_KEY_HASH);
}

// Comparación constante para hashes de credenciales. Evita terminar en una
// comparación de strings que revele el prefijo correcto por timing.
function safeEqualHex(actual, expected) {
  if (typeof actual !== 'string' || typeof expected !== 'string' || actual.length !== expected.length) return false;
  let diff = 0;
  for (let i = 0; i < actual.length; i += 1) diff |= actual.charCodeAt(i) ^ expected.charCodeAt(i);
  return diff === 0;
}

const agentItem = item => ({
  id: item.id,
  input: item.input,
  request: item.request,
  status: item.status,
  stage: item.stage,
  stage_at: item.stage_at,
  created: item.created,
  started_at: item.started_at,
  done_at: item.done_at,
  retry_count: Number(item.retry_count || 0),
  result: item.result || null,
  note: item.note || null,
});

const canonicalInstagram = value => {
  const handle = normalizeInstagramHandle(value);
  return handle ? `@${handle}` : null;
};

const agentSite = site => ({
  slug: site.slug,
  name: site.name,
  city: site.city || null,
  url_demo: site.url_demo || null,
  has_own_site: site.has_own_site === true,
  email: site.email || null,
  phone: site.phone || null,
  ig: canonicalInstagram(site.ig),
  maps_url: site.maps_url || null,
  source: inferLeadSource(site),
  business_key: site.business_key || null,
  language: site.language || 'es',
  outreach: site.outreach || 'pending_manual',
  dm_message: repairDemoSeparator(site.dm_message, site.url_demo) || null,
  fecha: site.fecha || null,
});

const CONTROL_SPEC_PREFIX = 'site-spec:';
const CONTROL_AUDIT_INDEX = 'control:audit:index';
const CONTROL_IDEMPOTENCY_PREFIX = 'control:idempotency:';
const CONTROL_TEXT = value => queueText(value, 240);
const controlSpecKey = slug => `${CONTROL_SPEC_PREFIX}${slug}:current`;
const controlSpecVersionKey = (slug, revision) => `${CONTROL_SPEC_PREFIX}${slug}:v:${revision}`;

async function controlRegistry(env) {
  return (await env.SITEFORGE_KV.get('registry', 'json')) || [];
}

function siteSearchHaystack(site) {
  return [site.name, site.slug, site.email, site.ig, site.phone, site.city, site.custom_domain]
    .filter(Boolean).join(' ').toLocaleLowerCase();
}

async function resolveControlSite(env, ref) {
  const normalized = normalizeRef(ref);
  if (!normalized) throw new Error('indica site.slug o site.query para localizar el website');
  const registry = await controlRegistry(env);
  if (normalized.slug) {
    const exact = registry.find(site => site.slug === normalized.slug);
    if (!exact) throw new Error(`website no encontrado: ${normalized.slug}`);
    return exact;
  }
  const query = String(normalized.query || '').toLocaleLowerCase();
  const city = String(normalized.city || '').toLocaleLowerCase();
  const matches = registry.filter(site => siteSearchHaystack(site).includes(query)
    && (!city || String(site.city || '').toLocaleLowerCase().includes(city)));
  if (!matches.length) throw new Error(`no se encontró un website para "${normalized.query}"`);
  if (matches.length > 1) {
    const options = matches.slice(0, 5).map(site => ({ slug: site.slug, name: site.name, city: site.city || null }));
    const error = new Error('la búsqueda devuelve más de un website; especifica el slug o la ciudad');
    error.code = 'AMBIGUOUS_SITE';
    error.options = options;
    throw error;
  }
  return matches[0];
}

async function loadControlSpec(env, site) {
  const stored = await env.SITEFORGE_KV.get(controlSpecKey(site.slug), 'json');
  if (stored) {
    assertSiteSpec(stored);
    return stored;
  }
  const initial = siteSpecFromRegistry(site);
  assertSiteSpec(initial);
  await Promise.all([
    env.SITEFORGE_KV.put(controlSpecKey(site.slug), JSON.stringify(initial)),
    env.SITEFORGE_KV.put(controlSpecVersionKey(site.slug, initial.revision), JSON.stringify(initial)),
  ]);
  return initial;
}

async function saveControlSpec(env, previous, next, reason) {
  const candidate = {
    ...next,
    version: 1,
    siteId: previous.slug,
    slug: previous.slug,
    revision: Number(previous.revision || 0) + 1,
    metadata: {
      ...(next.metadata || {}),
      updatedAt: new Date().toISOString(),
      changeReason: CONTROL_TEXT(reason || 'agent update'),
    },
  };
  assertSiteSpec(candidate);
  await Promise.all([
    env.SITEFORGE_KV.put(controlSpecKey(previous.slug), JSON.stringify(candidate)),
    env.SITEFORGE_KV.put(controlSpecVersionKey(previous.slug, candidate.revision), JSON.stringify(candidate)),
  ]);
  return candidate;
}

function redactControlAudit(value, depth = 0) {
  if (depth > 5) return '[depth-limited]';
  if (typeof value === 'string') return value.slice(0, 500);
  if (value === null || typeof value === 'number' || typeof value === 'boolean') return value;
  if (Array.isArray(value)) return value.slice(0, 30).map(item => redactControlAudit(item, depth + 1));
  if (!value || typeof value !== 'object') return null;
  const output = {};
  for (const [key, item] of Object.entries(value).slice(0, 80)) {
    output[key] = /secret|token|password|authorization|api[-_]?key/i.test(key)
      ? '[redacted]' : redactControlAudit(item, depth + 1);
  }
  return output;
}

function createControlAudit(event) {
  return {
    id: crypto.randomUUID(),
    agentId: 'siteforge-gpt',
    action: event.action,
    tool: event.tool,
    input: redactControlAudit(event.input || {}),
    result: redactControlAudit(event.result || null),
    status: event.status || 'ok',
    timestamp: new Date().toISOString(),
    duration: Number(event.duration || 0),
  };
}

async function persistControlAudit(env, audit) {
  // La cola DO ya serializa mutaciones de esta instalación de propietario único;
  // el registro de auditoría se escribe allí para no perder eventos concurrentes.
  await env.QUEUE_CLAIMS.getByName('siteforge-queue').audit(audit);
  return audit;
}

async function controlAudit(env, event) {
  return persistControlAudit(env, createControlAudit(event));
}

async function enqueueSiteUpdate(env, site, spec, reason = 'agent publish') {
  const item = {
    id: crypto.randomUUID(),
    input: `Actualizar website ${site.name || site.slug}`,
    status: 'pending',
    created: new Date().toISOString(),
    request: {
      type: 'site_update',
      operation_key: `site-update:${site.slug}`,
      slug: site.slug,
      ...(typeof site.has_own_site === 'boolean' ? { has_own_site: site.has_own_site } : {}),
      spec_revision: spec.revision,
      content_patch: spec.contentPatch || {},
      reason: CONTROL_TEXT(reason),
    },
  };
  const queued = await env.QUEUE_CLAIMS.getByName('siteforge-queue').enqueue(
    item, null, item.request.operation_key,
  );
  if (!queued.ok) throw new Error(queued.error || 'no se pudo encolar la publicación');
  return queued.item;
}

function pageById(spec, pageId) {
  const id = CONTROL_TEXT(pageId).toLowerCase();
  const page = spec.pages.find(item => item.id === id);
  if (!page) throw new Error(`página no encontrada: ${id}`);
  return page;
}

function normalizePage(page) {
  if (!page || typeof page !== 'object' || Array.isArray(page)) throw new Error('page debe ser un objeto');
  const id = CONTROL_TEXT(page.id).toLowerCase().replace(/[^a-z0-9-]/g, '-').replace(/^-+|-+$/g, '').slice(0, 50);
  if (!id) throw new Error('page.id requerido');
  const path = CONTROL_TEXT(page.path || `/${id}`).replace(/\s/g, '-').slice(0, 100);
  return {
    id,
    path: path.startsWith('/') ? path : `/${path}`,
    title: CONTROL_TEXT(page.title || id).slice(0, 120),
    sections: Array.isArray(page.sections) ? page.sections.slice(0, 80) : [],
  };
}

function applyPageTool(spec, tool, args) {
  const pages = Array.isArray(spec.pages) ? spec.pages.map(page => ({ ...page, sections: [...(page.sections || [])] })) : [];
  if (tool === 'website.page.list') return { pages };
  if (tool === 'website.page.create') {
    const page = normalizePage(args.page);
    if (pages.some(item => item.id === page.id || item.path === page.path)) throw new Error('ya existe una página con ese id o path');
    pages.push(page);
  } else if (tool === 'website.page.update') {
    const id = CONTROL_TEXT(args.pageId).toLowerCase();
    const index = pages.findIndex(page => page.id === id);
    if (index < 0) throw new Error(`página no encontrada: ${id}`);
    pages[index] = normalizePage({ ...pages[index], ...(args.patch || {}), id });
  } else if (tool === 'website.page.delete') {
    const id = CONTROL_TEXT(args.pageId).toLowerCase();
    if (id === 'home') throw new Error('la página home no se puede eliminar');
    const next = pages.filter(page => page.id !== id);
    if (next.length === pages.length) throw new Error(`página no encontrada: ${id}`);
    return { ...spec, pages: next };
  } else {
    const page = pageById({ ...spec, pages }, args.pageId);
    const sections = page.sections || [];
    if (tool === 'website.section.add') {
      const section = sanitizePatch(args.section || {});
      section.id = CONTROL_TEXT(section.id || `${section.type || 'section'}-${Date.now()}`).toLowerCase().replace(/[^a-z0-9-]/g, '-').slice(0, 60);
      if (!section.type) throw new Error('section.type requerido');
      if (sections.some(item => item.id === section.id)) throw new Error('section.id ya existe');
      const index = Number.isInteger(args.index) ? Math.max(0, Math.min(args.index, sections.length)) : sections.length;
      sections.splice(index, 0, section);
    } else if (tool === 'website.section.update') {
      const sectionId = CONTROL_TEXT(args.sectionId);
      const index = sections.findIndex(section => section.id === sectionId);
      if (index < 0) throw new Error(`sección no encontrada: ${sectionId}`);
      sections[index] = deepMerge(sections[index], sanitizePatch(args.patch || {}));
    } else if (tool === 'website.section.remove') {
      const sectionId = CONTROL_TEXT(args.sectionId);
      const next = sections.filter(section => section.id !== sectionId);
      if (next.length === sections.length) throw new Error(`sección no encontrada: ${sectionId}`);
      page.sections = next;
    } else if (tool === 'website.section.reorder') {
      const sectionId = CONTROL_TEXT(args.sectionId);
      const index = sections.findIndex(section => section.id === sectionId);
      if (index < 0) throw new Error(`sección no encontrada: ${sectionId}`);
      const [section] = sections.splice(index, 1);
      const target = Number.isInteger(args.index) ? Math.max(0, Math.min(args.index, sections.length)) : sections.length;
      sections.splice(target, 0, section);
    }
    page.sections = sections;
  }
  return { ...spec, pages };
}

async function executeControlTool(env, plan, tool, args) {
  permissionForPlan(plan, tool);
  if (tool === 'website.search') {
    const registry = await controlRegistry(env);
    const query = CONTROL_TEXT(args.query || '').toLocaleLowerCase();
    const city = CONTROL_TEXT(args.city || '').toLocaleLowerCase();
    const limit = Math.max(1, Math.min(Number(args.limit || 20), 100));
    const sites = registry.filter(site => (!query || siteSearchHaystack(site).includes(query))
      && (!city || String(site.city || '').toLocaleLowerCase().includes(city)))
      .slice(0, limit).map(agentSite);
    return { ok: true, total: sites.length, sites };
  }

  const site = await resolveControlSite(env, args.site || args.slug || args.query);
  let spec = await loadControlSpec(env, site);
  if (tool === 'website.get') return { ok: true, site: agentSite(site), spec };
  if (tool === 'website.preview') {
    assertSiteSpec(spec);
    return { ok: true, site: agentSite(site), revision: spec.revision, spec, preview_url: site.url_demo || null };
  }
  if (tool === 'website.test') {
    const errors = [];
    try { assertSiteSpec(spec); } catch (error) { errors.push(error.message); }
    if (!site.url_demo) errors.push('el website todavía no tiene url_demo publicada');
    return { ok: errors.length === 0, site: agentSite(site), revision: spec.revision, errors };
  }
  if (tool === 'website.page.list') return { ok: true, site: agentSite(site), ...applyPageTool(spec, tool, args) };
  if (tool.startsWith('website.page.') || tool.startsWith('website.section.')) {
    spec = applyPageTool(spec, tool, args);
    const saved = await saveControlSpec(env, spec, spec, tool);
    return { ok: true, site: agentSite(site), spec: saved, requires_publish: true, renderer: 'spec-only for pages/sections' };
  }
  if (tool === 'website.rollback') {
    const revision = Number(args.revision);
    if (!Number.isInteger(revision) || revision < 1) throw new Error('revision requerida');
    const prior = await env.SITEFORGE_KV.get(controlSpecVersionKey(site.slug, revision), 'json');
    if (!prior) throw new Error(`revisión no encontrada: ${revision}`);
    const saved = await saveControlSpec(env, spec, { ...prior, metadata: { ...(prior.metadata || {}), rollbackFrom: revision } }, `rollback to ${revision}`);
    return { ok: true, site: agentSite(site), spec: saved, requires_publish: true, rollback_from: revision };
  }
  if (tool === 'website.content.update') {
    const patch = sanitizePatch(args.patch || {});
    const saved = await saveControlSpec(env, spec, { ...spec, contentPatch: deepMerge(spec.contentPatch || {}, patch) }, 'content update');
    return { ok: true, site: agentSite(site), spec: saved, requires_publish: true };
  }
  if (tool === 'website.branding.update') {
    const branding = sanitizePatch(args.branding || {});
    const saved = await saveControlSpec(env, spec, { ...spec, branding: deepMerge(spec.branding || {}, branding) }, 'branding update');
    const palette = saved.branding?.palette;
    if (palette && ['deep', 'mid', 'soft', 'ghost'].every(key => typeof palette[key] === 'string')) {
      const colorOk = /^(#[0-9a-f]{3,8}|rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*(?:,\s*(?:0|1|0?\.\d+)\s*)?\))$/i;
      if (['deep', 'mid', 'soft', 'ghost'].some(key => !colorOk.test(palette[key]))) throw new Error('palette contiene un color inválido');
      await env.SITEFORGE_KV.put(`color:${site.slug}`, JSON.stringify(palette));
    }
    return { ok: true, site: agentSite(site), spec: saved, requires_publish: false };
  }
  if (tool === 'website.seo.configure') {
    const seo = sanitizePatch(args.seo || {});
    const saved = await saveControlSpec(env, spec, { ...spec, seo: deepMerge(spec.seo || {}, seo) }, 'seo configure');
    return { ok: true, site: agentSite(site), spec: saved, requires_publish: true };
  }
  if (tool === 'website.seo.analyze') {
    const seo = spec.seo || {};
    const title = typeof seo.title === 'string' ? seo.title.trim() : '';
    const description = typeof seo.description === 'string' ? seo.description.trim() : '';
    const findings = [];
    if (!title) findings.push({ level: 'warning', code: 'missing_title', message: 'Falta un título SEO.' });
    else if (title.length > 60) findings.push({ level: 'warning', code: 'title_long', message: 'El título SEO supera 60 caracteres.' });
    if (!description) findings.push({ level: 'warning', code: 'missing_description', message: 'Falta una meta description.' });
    else if (description.length > 160) findings.push({ level: 'warning', code: 'description_long', message: 'La meta description supera 160 caracteres.' });
    return { ok: true, site: agentSite(site), revision: spec.revision, score: Math.max(0, 100 - findings.length * 25), findings };
  }
  if (tool === 'website.image.update') {
    const patch = sanitizePatch(args.patch || {});
    const saved = await saveControlSpec(env, spec, { ...spec, contentPatch: deepMerge(spec.contentPatch || {}, patch) }, 'image update');
    return { ok: true, site: agentSite(site), spec: saved, requires_publish: true };
  }
  if (['website.form.create', 'website.form.update', 'website.booking.install', 'website.booking.configure',
    'website.whatsapp.install', 'website.whatsapp.configure', 'website.payment.install'].includes(tool)) {
    const config = sanitizePatch(args.config || {});
    const type = tool.split('.').slice(1).join('_');
    const integrations = Array.isArray(spec.integrations) ? [...spec.integrations] : [];
    const index = integrations.findIndex(item => item.type === type);
    const entry = { type, config, updatedAt: new Date().toISOString() };
    if (index >= 0) integrations[index] = { ...integrations[index], ...entry };
    else integrations.push(entry);
    const saved = await saveControlSpec(env, spec, { ...spec, integrations }, `${type} configure`);
    return { ok: true, site: agentSite(site), spec: saved, requires_publish: true };
  }
  if (tool === 'website.analytics.get') {
    return { ok: true, site: agentSite(site), metrics: [], note: 'Analytics aún no está conectado a una fuente de eventos.' };
  }
  if (tool === 'website.update') {
    const patch = sanitizePatch(args.patch || {});
    const next = deepMerge(spec, patch);
    const saved = await saveControlSpec(env, spec, next, 'website update');
    return { ok: true, site: agentSite(site), spec: saved, requires_publish: true };
  }
  if (tool === 'website.publish') {
    const job = await enqueueSiteUpdate(env, site, spec, args.reason || plan.goal);
    return { ok: true, site: agentSite(site), revision: spec.revision, job: agentItem(job), queued: true };
  }
  throw new Error(`tool registrada pero sin adapter: ${tool}`);
}

async function executeControlPlan(env, plan, actor = 'siteforge-gpt', options = {}) {
  const normalized = validatePlan(plan);
  const results = [];
  const recordAudit = async event => {
    const audit = createControlAudit(event);
    const pending = persistControlAudit(env, audit);
    // Audit is durable work, but it should not hold the user-facing GPT response
    // behind a second Durable Object round trip. Cloudflare's waitUntil keeps the
    // write alive after the response; local/unit callers still await it normally.
    if (options.deferAudit && typeof options.scheduleAudit === 'function') options.scheduleAudit(pending);
    else await pending;
    return audit;
  };
  for (const step of normalized.steps) {
    const started = Date.now();
    try {
      const result = await executeControlTool(env, normalized, step.tool, step.args);
      const stepOk = result?.ok !== false;
      const audit = await recordAudit({
        action: normalized.goal, tool: step.tool, input: step.args, result,
        status: stepOk ? 'ok' : 'failed', duration: Date.now() - started,
      });
      results.push({ tool: step.tool, ok: stepOk, result, audit_id: audit.id });
      // Adapters such as website.test can report a deterministic validation
      // failure without throwing. Stop dependent steps and surface that state
      // to the GPT instead of returning a misleading plan-level ok:true.
      if (!stepOk) return { ok: false, actor, plan: normalized, results, failed_step: step.tool };
    } catch (error) {
      const detail = { error: String(error.message || error), ...(error.code ? { code: error.code } : {}), ...(error.options ? { options: error.options } : {}) };
      const audit = await recordAudit({
        action: normalized.goal, tool: step.tool, input: step.args, result: detail,
        status: 'failed', duration: Date.now() - started,
      });
      results.push({ tool: step.tool, ok: false, error: detail, audit_id: audit.id });
      return { ok: false, actor, plan: normalized, results, failed_step: step.tool };
    }
  }
  return { ok: true, actor, plan: normalized, results };
}

// Resuelve el token de Registrar aunque el nombre de la variable venga con espacios o una
// coma al final (typo comun al pegar el nombre en el dashboard de Cloudflare).
function cfRegistrarToken(env) {
  if (env.CF_REGISTRAR_TOKEN) return env.CF_REGISTRAR_TOKEN;
  for (const [k, v] of Object.entries(env)) {
    if (typeof v === 'string' && k.replace(/[\s,]+$/g, '') === 'CF_REGISTRAR_TOKEN') return v;
  }
  return null;
}

const CF_API = 'https://api.cloudflare.com/client/v4';
const DOMAIN_PENDING_PREFIX = 'domain-pending:';
const DOMAIN_WAITING_STATES = new Set(['pending', 'in_progress', 'action_required', 'blocked']);

function cfRequest(token, path, options = {}) {
  const target = path.startsWith('http') ? path : `${CF_API}${path}`;
  return fetch(target, {
    ...options,
    headers: {
      authorization: `Bearer ${token}`,
      'content-type': 'application/json',
      ...(options.headers || {}),
    },
  });
}

async function responseData(response) {
  return response.json().catch(() => ({}));
}

async function zoneIdFor(token, domain) {
  const response = await cfRequest(token, `/zones?name=${encodeURIComponent(domain)}`);
  const data = await responseData(response);
  return (response.ok && data.result && data.result[0] && data.result[0].id) || null;
}

// Termina el trabajo que empieza al pulsar "Comprar y lanzar". Registrar puede
// responder 202 mientras el registro sigue en curso; esta función es idempotente
// y la ejecutan tanto la respuesta inicial como el Cron del Worker.
async function finalizePendingDomain(env, pending) {
  const token = cfRegistrarToken(env);
  if (!token || !env.CF_ACCOUNT_ID) return { pending: true, error: 'falta configuración de Registrar' };
  const domain = pending.domain;
  const slug = pending.slug;
  let state = pending.registration_state || null;
  let complete = pending.registration_complete === true;

  if (!complete) {
    const statusPath = pending.status_url || `/accounts/${env.CF_ACCOUNT_ID}/registrar/registrations/${encodeURIComponent(domain)}/registration-status`;
    const statusResponse = await cfRequest(token, statusPath);
    const statusData = await responseData(statusResponse);
    const workflow = statusData.result || {};
    state = workflow.state || state;
    complete = workflow.completed === true || state === 'succeeded';
    if (!statusResponse.ok) return { pending: true, state, error: 'Cloudflare aún no expone el estado del registro' };
    if (state === 'failed') return { failed: true, error: workflow.error?.message || 'Cloudflare rechazó el registro del dominio' };
    if (!complete || DOMAIN_WAITING_STATES.has(state)) return { pending: true, state: state || 'in_progress' };
  }

  const zoneId = await zoneIdFor(token, domain);
  if (!zoneId) return { pending: true, state: 'zone_pending' };

  const attachResponse = await cfRequest(token, `/accounts/${env.CF_ACCOUNT_ID}/workers/domains`, {
    method: 'PUT',
    body: JSON.stringify({ hostname: domain, service: 'siteforge-demos', zone_id: zoneId }),
  });
  const attachData = await responseData(attachResponse);
  if (!attachResponse.ok || attachData.success === false) {
    return { pending: true, state: 'worker_attach_pending', error: 'El dominio existe, pero Cloudflare aún no lo pudo enlazar al Worker' };
  }

  await env.SITEFORGE_KV.put('domain:' + domain, slug);
  const buys = (await env.SITEFORGE_KV.get('domain_buys', 'json')) || [];
  if (!buys.some(b => b.domain === domain)) {
    buys.push({ domain, slug, at: pending.created_at || new Date().toISOString() });
    await env.SITEFORGE_KV.put('domain_buys', JSON.stringify(buys));
  }
  const registry = (await env.SITEFORGE_KV.get('registry', 'json')) || [];
  const updated = registry.map(b => (b.slug === slug
    ? { ...b, custom_domain: domain, live_url: `https://${domain}/`, domain_status: 'live' }
    : b));
  await env.SITEFORGE_KV.put('registry', JSON.stringify(updated));
  await env.SITEFORGE_KV.delete(DOMAIN_PENDING_PREFIX + domain);
  return { done: true, domain, slug, live_url: `https://${domain}/`, worker_attached: true };
}

async function reconcilePendingDomains(env) {
  const listed = await env.SITEFORGE_KV.list({ prefix: DOMAIN_PENDING_PREFIX });
  for (const key of listed.keys.slice(0, 50)) {
    const pending = await env.SITEFORGE_KV.get(key.name, 'json');
    if (!pending || !pending.domain || !pending.slug) continue;
    try {
      const result = await finalizePendingDomain(env, pending);
      if (result.failed) {
        await env.SITEFORGE_KV.put('domain-failed:' + pending.domain, JSON.stringify({ ...pending, ...result, checked_at: new Date().toISOString() }));
        await env.SITEFORGE_KV.delete(key.name);
      } else if (!result.done) {
        await env.SITEFORGE_KV.put(key.name, JSON.stringify({ ...pending, ...result, checked_at: new Date().toISOString() }));
      }
    } catch (error) {
      await env.SITEFORGE_KV.put(key.name, JSON.stringify({ ...pending, error: String(error).slice(0, 220), checked_at: new Date().toISOString() }));
    }
  }
}

async function reconcileStaleQueue(env) {
  const queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
  const now = Date.now();
  const guard = env.QUEUE_CLAIMS.getByName('siteforge-queue');
  for (const item of queue.filter(q => q.status === 'processing')) {
    const startedAt = Date.parse(item.started_at || item.created);
    if (!Number.isFinite(startedAt) || now - startedAt < STALE_FORGE_MS) continue;
    // El propio DO vuelve a comprobar la edad bajo exclusión mutua, evitando
    // rescatar un trabajo que acaba de enviar heartbeat mientras se leyó KV.
    await guard.recover(item.id, now, STALE_FORGE_MS);
  }
}

export default {
  async scheduled(_controller, env) {
    await Promise.all([reconcilePendingDomains(env), reconcileStaleQueue(env),
      env.OUTREACH_CAMPAIGN.getByName('permission-pilot-v1').run()]);
  },

  async fetch(req, env, ctx) {
    const url = new URL(req.url);

    if (url.pathname === '/webhooks/telnyx' && req.method === 'POST') {
      let raw;
      try { raw = await boundedBody(req); } catch { return json({ error: 'too large' }, 413); }
      if (!(await verifyTelnyxWebhook(raw, req.headers, env.TELNYX_PUBLIC_KEY))) return json({ error: 'invalid signature' }, 401);
      try {
        return json(await env.OUTREACH_CAMPAIGN.getByName('permission-pilot-v1').telnyxEvent(JSON.parse(raw).data));
      } catch { return json({ error: 'event could not be recorded' }, 503); }
    }

    // Unsubscribe is a secret capability link: GET only displays, POST applies.
    if (url.pathname.startsWith('/unsubscribe/')) {
      if (!['GET', 'POST'].includes(req.method)) return new Response('Method not allowed', { status: 405 });
      const token = url.pathname.slice('/unsubscribe/'.length);
      const valid = await env.OUTREACH_CAMPAIGN.getByName('permission-pilot-v1').unsubscribe(token, req.method === 'POST');
      if (!valid) return new Response('Invalid link', { status: 404 });
      const body = req.method === 'POST' ? '<h1>Unsubscribed / Baja confirmada</h1><p>No more outreach emails will be sent to this address.</p>'
        : '<h1>Merktop · Email preferences</h1><form method="post"><button type="submit">Unsubscribe / No recibir más correos</button></form>';
      return new Response(`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Merktop · Email preferences</title><body>${body}</body></html>`, {
        headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'referrer-policy': 'no-referrer', 'content-security-policy': "default-src 'none'; form-action 'self'; frame-ancestors 'none'" },
      });
    }

    // API minima para el GPT Agent de Siteforge. Tiene una clave propia y solo expone
    // cola, estados, registro y reintentos. Outreach y compra de dominios siguen fuera
    // de este contrato hasta añadir una confirmacion explicita de usuario.
    if (url.pathname.startsWith('/api/agent/')) {
      if (!(await isAgentAuthorized(req))) return json({ error: 'unauthorized' }, 401);

      // Control Plane v2: el mismo GPT puede descubrir un website, modificar su
      // SiteSpec, probarlo, publicar una revisión y consultar la auditoría. No hay
      // tenant_id en esta fase: la instalación sigue siendo de un solo propietario.
      if (url.pathname === '/api/agent/v2/tools' && req.method === 'GET') {
        return json({ ok: true, version: 1, tools: TOOL_DEFINITIONS });
      }

      if (url.pathname === '/api/agent/v2/execute' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        const requestId = typeof body?.request_id === 'string'
          ? body.request_id.replace(/[^A-Za-z0-9._:-]/g, '').slice(0, 100) : '';
        if (!requestId) return json({ error: 'request_id requerido para idempotencia' }, 400);
        const cacheKey = CONTROL_IDEMPOTENCY_PREFIX + requestId;
        const previous = await env.SITEFORGE_KV.get(cacheKey, 'json');
        if (previous) return json({ ...previous, idempotent_replay: true });
        const plan = body.plan || body;
        let result;
        try {
          result = await executeControlPlan(env, plan, 'siteforge-gpt', {
            deferAudit: Boolean(ctx?.waitUntil),
            scheduleAudit: pending => ctx?.waitUntil(pending.catch(() => {})),
          });
        } catch (error) {
          return json({ ok: false, error: String(error.message || error) }, 400);
        }
        await env.SITEFORGE_KV.put(cacheKey, JSON.stringify(result), { expirationTtl: 24 * 60 * 60 });
        return json(result, result.ok ? 200 : 422);
      }

      if (url.pathname === '/api/agent/v2/audit' && req.method === 'GET') {
        const limit = Math.max(1, Math.min(Number(url.searchParams.get('limit') || 30), 100));
        const ids = (await env.SITEFORGE_KV.get(CONTROL_AUDIT_INDEX, 'json')) || [];
        const events = [];
        for (const id of ids.slice(0, limit)) {
          const event = await env.SITEFORGE_KV.get(`control:audit:${id}`, 'json');
          if (event) events.push(event);
        }
        return json({ ok: true, total: events.length, events });
      }

      const specMatch = url.pathname.match(/^\/api\/agent\/v2\/sites\/([a-z0-9-]{1,40})\/spec$/);
      if (specMatch && req.method === 'GET') {
        try {
          const site = await resolveControlSite(env, { slug: specMatch[1] });
          const spec = await loadControlSpec(env, site);
          return json({ ok: true, site: agentSite(site), spec });
        } catch (error) {
          return json({ ok: false, error: String(error.message || error) }, error.code === 'AMBIGUOUS_SITE' ? 409 : 404);
        }
      }

      if (url.pathname === '/api/agent/health' && req.method === 'GET') {
        return json({ ok: true, service: 'siteforge-agent', queue_url: `${url.origin}/api/agent/queue` });
      }

      if (url.pathname === '/api/agent/queue' && req.method === 'GET') {
        const queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
        const counts = queue.reduce((out, item) => {
          out[item.status] = (out[item.status] || 0) + 1;
          return out;
        }, {});
        const items = queue
          .filter(item => item.status !== 'done')
          .sort((a, b) => Date.parse(b.created) - Date.parse(a.created))
          .slice(0, 100)
          .map(agentItem);
        return json({ ok: true, counts, items });
      }

      if (url.pathname === '/api/agent/build' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        let input;
        let request;
        let buildLanguage;
        if (body && (body.niche !== undefined || body.location !== undefined)) {
          const niche = queueText(body.niche, 70);
          const location = queueText(body.location, 80);
          const count = Number(body.count || 1);
          const language = String(body.language || '').toLowerCase();
          if (!niche || !location) return json({ error: 'niche and location are required' }, 400);
          if (!Number.isInteger(count) || count < 1 || count > 5) {
            return json({ error: 'count must be an integer between 1 and 5' }, 400);
          }
          if (body.language !== undefined && !['es', 'en'].includes(language)) {
            return json({ error: 'language must be es or en' }, 400);
          }
          request = { type: 'discovery', niche, location, count, require_no_website: true,
            ...(['es', 'en'].includes(language) ? { language } : {}) };
          input = `Buscar ${count} ${niche} en ${location} sin website propio`;
        } else {
          input = queueText(body?.input, 200);
          if (!input) return json({ error: 'input is required (max 200 chars)' }, 400);
          const language = String(body?.language || '').toLowerCase();
          if (body?.language !== undefined && !['es', 'en'].includes(language)) {
            return json({ error: 'language must be es or en' }, 400);
          }
          if (['es', 'en'].includes(language)) buildLanguage = language;
        }
        const item = {
          id: crypto.randomUUID(), input, status: 'pending', created: new Date().toISOString(),
          ...(request ? { request } : {}),
          ...(buildLanguage ? { language: buildLanguage } : {}),
        };
        const queued = await env.QUEUE_CLAIMS.getByName('siteforge-queue').enqueue(
          item, request ? discoveryKey(request) : null, request ? null : directBuildKey(input),
        );
        if (!queued.ok) return json(queued, queued.status || 500);
        return json({ ok: true, job: agentItem(queued.item) });
      }

      const jobMatch = url.pathname.match(/^\/api\/agent\/jobs\/([^/]+)$/);
      if (jobMatch && req.method === 'GET') {
        const id = decodeURIComponent(jobMatch[1]);
        const queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
        const item = queue.find(q => q.id === id);
        if (!item) return json({ error: 'job not found' }, 404);
        return json({ ok: true, job: agentItem(item) });
      }

      const retryMatch = url.pathname.match(/^\/api\/agent\/jobs\/([^/]+)\/retry$/);
      if (retryMatch && req.method === 'POST') {
        const id = decodeURIComponent(retryMatch[1]);
        const retried = await env.QUEUE_CLAIMS.getByName('siteforge-queue').retry(id, Date.now());
        return json(retried, retried.ok ? 200 : (retried.status || 500));
      }

      if (url.pathname === '/api/agent/sites' && req.method === 'GET') {
        const registry = (await env.SITEFORGE_KV.get('registry', 'json')) || [];
        const query = queueText(url.searchParams.get('q'), 120).toLocaleLowerCase();
        const city = queueText(url.searchParams.get('city'), 80).toLocaleLowerCase();
        const limit = Math.max(1, Math.min(Number(url.searchParams.get('limit') || 50), 100));
        const sites = registry.filter(site => {
          const haystack = [site.name, site.slug, site.email, site.ig, site.phone].join(' ').toLocaleLowerCase();
          return (!query || haystack.includes(query)) && (!city || String(site.city || '').toLocaleLowerCase().includes(city));
        }).slice(0, limit).map(agentSite);
        return json({ ok: true, total: sites.length, sites });
      }

      const siteMatch = url.pathname.match(/^\/api\/agent\/sites\/([a-z0-9-]{1,40})$/);
      if (siteMatch && req.method === 'GET') {
        const registry = (await env.SITEFORGE_KV.get('registry', 'json')) || [];
        const site = registry.find(item => item.slug === siteMatch[1]);
        if (!site) return json({ error: 'site not found' }, 404);
        return json({ ok: true, site: agentSite(site) });
      }

      return json({ error: 'agent route not found' }, 404);
    }

    // Endpoints publicos autorizados por el usuario (2026-07-16): permiten que la
    // rutina cloud procese la cola sin guardar credenciales. Solo exponen metadata
    // de la cola; agregar items y escribir el registro siguen requiriendo la key.
    if (url.pathname === '/api/public/queue' && req.method === 'GET') {
      const queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
      const now = Date.now();
      const pending = queue
        .filter(q => q.status === 'pending' || isStaleForge(q, now))
        .sort((a, b) => Date.parse(a.created) - Date.parse(b.created))
        .map(({ id, input, request, created }) => ({ id, input, request, created }));
      return json({ pending });
    }

    // Reclamo atomico: una sola forja puede tomar el item. Evita que dos slots hagan
    // el mismo website cuando leen la cola simultaneamente.
    if (url.pathname === '/api/public/queue/claim' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      if (typeof body.id !== 'string' || !body.id) return json({ error: 'id requerido' }, 400);
      const claimGuard = env.QUEUE_CLAIMS.getByName('siteforge-queue');
      const claimed = await claimGuard.claim(body.id, Date.now(), STALE_FORGE_MS);
      if (!claimed.ok) return json({ error: claimed.error || 'item ya reclamado' }, 409);
      return json({ ok: true, item: claimed.item });
    }

    if (url.pathname === '/api/public/queue/progress' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      const STAGES = ['research', 'build', 'verify', 'commit'];
      if (!body.id || typeof body.token !== 'string' || !STAGES.includes(body.stage)) return json({ error: 'id, token y stage validos requeridos' }, 400);
      const result = await env.QUEUE_CLAIMS.getByName('siteforge-queue').progress(
        body.id, body.token, body.stage, body.note, Date.now(),
      );
      return json(result, result.ok ? 200 : 404);
    }

    // Reserva permanente/atómica por identidad antes de investigar o construir.
    // El claim token actúa como capability de corta duración: ningún caller puede
    // reservar negocios para un item que no haya reclamado primero.
    if (url.pathname === '/api/public/queue/candidates/reserve' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      if (typeof body.id !== 'string' || typeof body.token !== 'string'
        || !Array.isArray(body.candidates) || body.candidates.length < 1 || body.candidates.length > 20) {
        return json({ error: 'id, token y entre 1 y 20 candidates requeridos' }, 400);
      }
      const candidates = body.candidates.map(cleanBusinessCandidate)
        .filter(candidate => candidate.name || candidate.slug);
      if (!candidates.length) return json({ error: 'candidates sin identidad válida' }, 400);
      const result = await env.QUEUE_CLAIMS.getByName('siteforge-queue').reserveBusinesses(
        body.id, body.token, candidates, Date.now(), STALE_FORGE_MS,
      );
      return json(result, result.ok ? 200 : (result.status || 500));
    }

    if (url.pathname === '/api/public/queue/candidates/complete' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      if (typeof body.id !== 'string' || typeof body.token !== 'string') {
        return json({ error: 'id y token requeridos' }, 400);
      }
      const candidate = cleanBusinessCandidate(body.candidate);
      const site = cleanBusinessCandidate(body.site);
      site.url_demo = typeof body.site?.url_demo === 'string' && DEMO_URL_RE.test(body.site.url_demo)
        ? body.site.url_demo : undefined;
      if (!site.slug || !site.url_demo) return json({ error: 'site requiere slug y url_demo válidos' }, 400);
      const result = await env.QUEUE_CLAIMS.getByName('siteforge-queue').completeBusiness(
        body.id, body.token, candidate, site, Date.now(),
      );
      return json(result, result.ok ? 200 : (result.status || 500));
    }

    if (url.pathname === '/api/public/queue/candidates/release' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      if (typeof body.id !== 'string' || typeof body.token !== 'string') {
        return json({ error: 'id y token requeridos' }, 400);
      }
      const candidate = cleanBusinessCandidate(body.candidate);
      const result = await env.QUEUE_CLAIMS.getByName('siteforge-queue').releaseBusiness(
        body.id, body.token, candidate, Date.now(),
      );
      return json(result, result.ok ? 200 : (result.status || 500));
    }

    if (url.pathname === '/api/public/queue/done' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      if (!body.id || typeof body.token !== 'string') return json({ error: 'id y token requeridos' }, 400);
      const siteResult = raw => {
        raw = raw && typeof raw === 'object' ? raw : {};
        const site = {};
        if (typeof raw.slug === 'string' && /^[a-z0-9-]{1,40}$/.test(raw.slug)) site.slug = raw.slug;
        if (typeof raw.name === 'string' && raw.name.length <= 120) site.name = stripUnsafe(raw.name);
        if (typeof raw.url_demo === 'string' && DEMO_URL_RE.test(raw.url_demo)) site.url_demo = raw.url_demo;
        if (typeof raw.dm === 'string' && raw.dm.length <= 900) site.dm = cleanMessage(raw.dm, 900);
        return site;
      };
      const result = siteResult(body);
      // Una busqueda filtrada puede producir hasta cinco negocios. El contrato anterior
      // (slug/name/url_demo en la raiz) sigue funcionando para pedidos directos.
      if (body.sites !== undefined) {
        if (!Array.isArray(body.sites) || body.sites.length < 1 || body.sites.length > 5) {
          return json({ error: 'sites debe contener entre 1 y 5 resultados' }, 400);
        }
        const sites = body.sites.map(siteResult);
        if (sites.some(site => !site.slug || !site.url_demo)) {
          return json({ error: 'cada site requiere slug y url_demo validos' }, 400);
        }
        result.sites = sites;
      }
      if (body.failed === true) {
        result.failed = true;
        if (typeof body.motivo === 'string') result.motivo = stripUnsafe(body.motivo.slice(0, 240));
      }
      const finished = await env.QUEUE_CLAIMS.getByName('siteforge-queue').done(body.id, body.token, result, Date.now());
      return json(finished, finished.ok ? 200 : 404);
    }

    // Upsert publico de UN negocio al registro del panel (autorizado por el usuario 2026-07-19).
    // Permite que las corridas cloud reflejen sus demos sin credenciales. Defensas:
    // solo url_demo del dominio de demos, campos con tope, NUNCA pisa outreach 'sent',
    // y nunca borra: solo agrega o actualiza el slug que registra.
    if (url.pathname === '/api/public/registry-upsert' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      const slug = (body.slug || '').toString();
      if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
      if (typeof body.url_demo !== 'string' || !DEMO_URL_RE.test(body.url_demo)) return json({ error: 'url_demo invalida' }, 400);
      if (body.language !== undefined && !['es', 'en', 'fr'].includes(body.language)) {
        return json({ error: 'language invalido' }, 400);
      }
      // Nota: no se verifica el demo con fetch aqui. Un Worker no puede hacer fetch fiable a
      // otro Worker de la MISMA cuenta workers.dev (da 404 aunque el demo este live), y el repo
      // es privado (raw github 404 sin token). La prevencion de tarjetas fantasma vive en la
      // forja (verifica 200 antes de upsert, ver FORGE-BRIEF) y en el chequeo client-side del panel.
      const S = (v, max) => (typeof v === 'string' ? stripUnsafe(v.slice(0, max)) : undefined);
      const instagramHandle = normalizeInstagramHandle(body.ig);
      const limpio = {
        slug,
        name: S(body.name, 120),
        city: S(body.city, 80),
        ig: instagramHandle ? `@${instagramHandle}` : undefined,
        url_demo: body.url_demo,
        has_own_site: typeof body.has_own_site === 'boolean' ? body.has_own_site : undefined,
        // undefined (no null): un upsert que viene sin email NO debe borrar el email que ya
        // se habia encontrado para ese negocio (el filtro de abajo descarta solo undefined).
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.email || '') ? S(body.email, 120) : undefined,
        phone: S(body.phone, 30),
        maps_url: typeof body.maps_url === 'string' && googleMapsIdentity(body.maps_url)
          ? S(body.maps_url, 600) : undefined,
        source: ['google_maps', 'instagram', 'manual'].includes(body.source) ? body.source : undefined,
        business_key: typeof body.business_key === 'string'
          ? body.business_key.toLowerCase().replace(/[^a-z0-9:|._-]/g, '').slice(0, 220) || undefined
          : undefined,
        language: ['es', 'en', 'fr'].includes(body.language) ? body.language : undefined,
        dm_message: typeof body.dm_message === 'string' ? cleanMessage(body.dm_message, 900) : undefined,
        message_version: [2, 3].includes(Number(body.message_version)) ? Number(body.message_version) : undefined,
        thumb: typeof body.thumb === 'string' && body.thumb.startsWith('https://') && body.thumb.includes('.odd-forest-9504.workers.dev') ? S(body.thumb, 300) : undefined,
        fecha: /^\d{4}-\d{2}-\d{2}$/.test(body.fecha || '') ? body.fecha : undefined,
      };
      const registryResult = await env.QUEUE_CLAIMS.getByName('siteforge-queue').registryUpsert(limpio);
      return json(registryResult, registryResult.ok ? 200 : (registryResult.status || 500));
    }

    if (url.pathname.startsWith('/api/')) {
      if (!(await isAuthorized(req))) return json({ error: 'unauthorized' }, 401);

      if (url.pathname.startsWith('/api/outreach/')) {
        const campaign = env.OUTREACH_CAMPAIGN.getByName('permission-pilot-v1');
        if (url.pathname === '/api/outreach/status' && req.method === 'GET') return json(await campaign.status());
        if (url.pathname === '/api/outreach/inbox' && req.method === 'GET') {
          const thread = url.searchParams.get('thread');
          if (thread !== null && !/^[a-f0-9]{64}$/.test(thread)) return json({ error: 'invalid thread' }, 400);
          return json(await campaign.inbox(thread ?? undefined));
        }
        if (req.method !== 'POST') return json({ error: 'method not allowed' }, 405);
        let input;
        try { input = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        if (!input || typeof input !== 'object' || Array.isArray(input)) return json({ error: 'invalid input' }, 400);
        try {
          if (url.pathname === '/api/outreach/config') return json(await campaign.configure(input));
          if (url.pathname === '/api/outreach/consent') return json(await campaign.consent(input));
          if (url.pathname === '/api/outreach/event') return json(await campaign.event(input));
          if (url.pathname === '/api/outreach/read') return json(await campaign.readReply(input));
          if (url.pathname === '/api/outreach/run') {
            if (input.slug !== undefined && !/^[a-z0-9-]{1,40}$/.test(input.slug)) return json({ error: 'invalid slug' }, 400);
            return json(await campaign.run(input.slug));
          }
        } catch { return json({ error: 'La operación requiere datos válidos y evidencia verificable; revise consentimiento o supresión.' }, 400); }
        return json({ error: 'not found' }, 404);
      }

      if (url.pathname === '/api/state' && req.method === 'GET') {
        const [registry, queue, crm, colores, mensajes] = await Promise.all([
          env.SITEFORGE_KV.get('registry', 'json'),
          env.SITEFORGE_KV.get('queue', 'json'),
          env.SITEFORGE_KV.get('crm', 'json'),
          // Colores personalizados: se listan las llaves y se leen solo las que existen, para
          // que el panel marque el color activo de cada sitio sin una lectura por negocio.
          env.SITEFORGE_KV.list({ prefix: 'color:' })
            .then(l => Promise.all(l.keys.map(k =>
              env.SITEFORGE_KV.get(k.name, 'json').then(v => [k.name.slice(6), v]))))
            .then(pares => Object.fromEntries(pares.filter(([, v]) => v)))
            .catch(() => ({})),
          // Mensajes editados a mano, igual que los colores: una lista y luego solo los que hay.
          env.SITEFORGE_KV.list({ prefix: 'msg:' })
            .then(l => Promise.all(l.keys.map(k =>
              env.SITEFORGE_KV.get(k.name).then(v => [k.name.slice(4), v]))))
            .then(pares => Object.fromEntries(pares.filter(([, v]) => v)))
            .catch(() => ({})),
        ]);
        // El CRM (cliente cerrado / descartado) vive en su propia llave: ninguna
        // sincronizacion del registro desde el repo o la forja lo puede pisar.
        const map = crm || {};
        const reg = (registry || [])
          // Compatibilidad inmediata con el registro histórico: URLs de perfil se
          // canonizan y sentinels como "Google Maps" dejan de salir como Instagram.
          .map(b => ({
            ...b,
            dm_message: repairDemoSeparator(b.dm_message, b.url_demo),
            ig: canonicalInstagram(b.ig),
            source: inferLeadSource(b) || undefined,
          }))
          .map(b => (map[b.slug]
          ? {
              ...b,
              crm_status: map[b.slug].status,
              crm_at: map[b.slug].at,
              contacted_at: map[b.slug].contacted_at || null,
              contacted_via: map[b.slug].via || null,
            }
          : b))
          .map(b => (colores[b.slug] ? { ...b, color: colores[b.slug] } : b))
          .map(b => (mensajes[b.slug] ? { ...b, msg_editado: repairDemoSeparator(mensajes[b.slug], b.url_demo) } : b));
        return json({ registry: reg, queue: queue || [] });
      }

      // CRM: marcar un negocio como cliente cerrado / descartado / reabrir.
      // Accion directa del usuario autenticado; reversible; sin efectos externos.
      if (url.pathname === '/api/mark' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        const slug = (body.slug || '').toString();
        if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
        const status = body.status;
        // 'contacted' = ya le escribi o lo llame, para no repetir el contacto. Es distinto de
        // 'client' (cerro) y de 'declined' (dijo que no): es el paso intermedio que faltaba.
        if (!['client', 'declined', 'contacted', 'pending'].includes(status)) return json({ error: 'status invalido' }, 400);
        const crm = (await env.SITEFORGE_KV.get('crm', 'json')) || {};
        if (status === 'pending') {
          delete crm[slug];
        } else {
          const via = ['llamada', 'whatsapp', 'dm', 'email', 'visita'].includes(body.via) ? body.via : null;
          crm[slug] = {
            status,
            at: new Date().toISOString(),
            ...(via ? { via } : {}),
            // conservar cuando se contacto por primera vez aunque luego cierre o descarte
            ...(crm[slug] && crm[slug].contacted_at ? { contacted_at: crm[slug].contacted_at }
                : (status === 'contacted' ? { contacted_at: new Date().toISOString() } : {})),
          };
        }
        await env.SITEFORGE_KV.put('crm', JSON.stringify(crm));
        const vals = Object.values(crm);
        return json({
          ok: true, slug, status,
          clientes: vals.filter(c => c.status === 'client').length,
          contactados: vals.filter(c => c.status === 'contacted').length,
        });
      }

      // Color del sitio: se guarda en el MISMO KV que lee el worker de demos, que lo inyecta
      // como <style> al servir. Por eso el cambio se ve al instante y no hace falta
      // reconstruir el sitio ni redeployar. Enviar sin `palette` lo devuelve a su color original.
      if (url.pathname === '/api/color' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        const slug = (body.slug || '').toString();
        if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
        if (!body.palette) {
          await env.SITEFORGE_KV.delete('color:' + slug);
          return json({ ok: true, slug, palette: null });
        }
        // Mismo filtro que aplica el worker de demos: estos valores acaban dentro de un
        // <style>, asi que solo pasan formas de color conocidas.
        const OK = /^(#[0-9a-f]{3,8}|rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*(?:,\s*(?:0|1|0?\.\d+)\s*)?\))$/i;
        const limpia = {};
        for (const t of ['deep', 'mid', 'soft', 'ghost']) {
          const v = (body.palette[t] || '').toString().trim();
          if (!OK.test(v)) return json({ error: `color invalido en "${t}"`, valor: v.slice(0, 40) }, 400);
          limpia[t] = v;
        }
        if (typeof body.nombre === 'string') limpia.nombre = stripUnsafe(body.nombre.slice(0, 40));
        await env.SITEFORGE_KV.put('color:' + slug, JSON.stringify(limpia));
        return json({ ok: true, slug, palette: limpia });
      }

      // Mensaje de outreach editado a mano para un negocio. Se guarda para que el texto que
      // se ajusto no se pierda al recargar el panel ni al cambiar de dispositivo: el DM de
      // Instagram hay que pegarlo a mano, asi que conviene tenerlo tal cual se dejo.
      if (url.pathname === '/api/mensaje' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        const slug = (body.slug || '').toString();
        if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
        if (typeof body.texto !== 'string' || !body.texto.trim()) {
          await env.SITEFORGE_KV.delete('msg:' + slug);
          return json({ ok: true, slug, texto: null });
        }
        // Tope generoso: un DM largo cabe de sobra y evita que una escritura rara llene el KV.
        const texto = body.texto.slice(0, 1200);
        await env.SITEFORGE_KV.put('msg:' + slug, texto);
        return json({ ok: true, slug, largo: texto.length });
      }

      if (url.pathname === '/api/queue' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        let input;
        let request;
        let candidate;
        let buildLanguage;
        if (body.request !== undefined) {
          const raw = body.request;
          if (!raw || typeof raw !== 'object' || raw.type !== 'discovery') {
            return json({ error: 'request de descubrimiento invalido' }, 400);
          }
          const niche = queueText(raw.niche, 70);
          const location = queueText(raw.location, 80);
          const count = Number(raw.count);
          const language = String(raw.language || '').toLowerCase();
          if (!niche || !location) return json({ error: 'nicho y pais o zona son requeridos' }, 400);
          if (!Number.isInteger(count) || count < 1 || count > 5) {
            return json({ error: 'cantidad debe ser un entero entre 1 y 5' }, 400);
          }
          if (raw.language !== undefined && !['es', 'en'].includes(language)) {
            return json({ error: 'idioma debe ser es o en' }, 400);
          }
          // Los descubrimientos creados en el panel SIEMPRE excluyen negocios con web propia.
          // No se acepta un flag del cliente para que nadie pueda invertir esta regla por error.
          request = { type: 'discovery', niche, location, count, require_no_website: true,
            ...(['es', 'en'].includes(language) ? { language } : {}) };
          input = `Buscar ${count} ${niche} en ${location} sin website propio`;
        } else {
          input = queueText(body.input, 200);
          if (!input) return json({ error: 'input requerido (max 200 chars)' }, 400);
          const language = String(body.language || '').toLowerCase();
          if (body.language !== undefined && !['es', 'en'].includes(language)) {
            return json({ error: 'idioma debe ser es o en' }, 400);
          }
          if (['es', 'en'].includes(language)) buildLanguage = language;
          if (body.candidate !== undefined) {
            candidate = cleanBusinessCandidate(body.candidate);
            if (!candidate.name || !candidate.slug) return json({ error: 'candidate directo inválido' }, 400);
          }
        }
        const item = {
          id: crypto.randomUUID(), input, status: 'pending', created: new Date().toISOString(),
          ...(request ? { request } : {}),
          ...(candidate ? { candidate } : {}),
          ...(buildLanguage ? { language: buildLanguage } : {}),
        };
        const queued = await env.QUEUE_CLAIMS.getByName('siteforge-queue').enqueue(
          item, request ? discoveryKey(request) : null, request ? null : directBuildKey(input),
        );
        return json(queued, queued.ok ? 200 : (queued.status || 500));
      }

      // Reintento manual de un fallo visible en el historial. Los fallos no se
      // reencolan solos porque algunos son definitivos (por ejemplo, una ficha sin
      // cinco fotos propias); el usuario decide cuándo vale la pena volver a probar.
      if (url.pathname === '/api/queue/retry' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        if (!body.id) return json({ error: 'id requerido' }, 400);
        const retried = await env.QUEUE_CLAIMS.getByName('siteforge-queue').retry(body.id, Date.now());
        return json(retried, retried.ok ? 200 : (retried.status || 500));
      }

      // Recupera un item que quedó processing por un reinicio de Railway. Se
      // permite a los nueve minutos desde started_at, igual que el reconciliador.
      if (url.pathname === '/api/queue/recover' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        if (!body.id) return json({ error: 'id requerido' }, 400);
        const recovered = await env.QUEUE_CLAIMS.getByName('siteforge-queue').recover(
          body.id, Date.now(), STALE_FORGE_MS,
        );
        return json(recovered, recovered.ok ? 200 : (recovered.status || 500));
      }

      if (url.pathname === '/api/queue/done' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        // Sin este guard, un body sin id recorre la cola comparando contra undefined y responde
        // ok:true sin haber cerrado nada (falso positivo para el que llama).
        if (!body.id || typeof body.token !== 'string') return json({ error: 'id y token requeridos' }, 400);
        const result = body.failed === true
          ? { failed: true, motivo: typeof body.motivo === 'string' ? stripUnsafe(body.motivo.slice(0, 240)) : undefined }
          : {};
        const finished = await env.QUEUE_CLAIMS.getByName('siteforge-queue').done(body.id, body.token, result, Date.now());
        return json(finished, finished.ok ? 200 : 404);
      }

      // Manual and scheduled sends use the SAME permission, QA and durable dedup gate.
      if (url.pathname === '/api/send' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        if (!/^[a-z0-9-]{1,40}$/.test(body?.slug || '')) return json({ error: 'slug invalido' }, 400);
        const result = await env.OUTREACH_CAMPAIGN.getByName('permission-pilot-v1').run(body.slug);
        return json(result.ok ? result : { ...result, error: 'Envío bloqueado: ' + result.reason }, result.ok ? 200 : 409);
      }

      // ---- DOMINIOS (Cloudflare Registrar) ----
      // Checar disponibilidad + precio de un nombre en varios TLDs. Gratis, sin riesgo.
      if (url.pathname === '/api/domain/check' && req.method === 'POST') {
        const cfTok = cfRegistrarToken(env);
        if (!cfTok || !env.CF_ACCOUNT_ID) {
          return json({
            error: 'Falta CF_REGISTRAR_TOKEN en el worker',
            como_arreglarlo: 'npx wrangler secret put CF_REGISTRAR_TOKEN -c ui/wrangler.jsonc',
            nota: 'Ponerlo como SECRET, no como variable del dashboard: un deploy reemplaza las vars y la borra.',
          }, 500);
        }
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        // El punto que separa nombre y TLD es DATO, no suciedad: sanear a lo bruto con
        // replace(/[^a-z0-9-]/g,'') convertia "mibarberia.com" en "mibarberiacom" y buscaba
        // "mibarberiacom.com". Hay que parsear primero y limpiar despues.
        const crudo = (body.name || '').toString().toLowerCase().trim()
          .replace(/^https?:\/\//, '')   // pegar la URL entera tambien vale
          .replace(/^www\./, '')
          .replace(/[/?#].*$/, '')       // quitar path/query
          .replace(/\s+/g, '');          // "mi barberia" -> "mibarberia"
        const conTld = crudo.match(/^([a-z0-9][a-z0-9-]*)\.([a-z]{2,24}(?:\.[a-z]{2,24})?)$/);
        const base = (conTld ? conTld[1] : crudo).replace(/[^a-z0-9-]/g, '').replace(/^-+|-+$/g, '').slice(0, 50);
        if (!base) return json({ error: 'nombre invalido' }, 400);
        const pedido = conTld ? conTld[2] : null;
        // Si el usuario escribio un TLD concreto, ese va PRIMERO y siempre se consulta.
        const porDefecto = ['com', 'net', 'co', 'studio'];
        const listaTlds = Array.isArray(body.tlds) && body.tlds.length ? body.tlds : porDefecto;
        const tlds = [...new Set([...(pedido ? [pedido] : []), ...listaTlds])]
          .map(t => String(t).toLowerCase().replace(/[^a-z.]/g, '')).filter(Boolean).slice(0, 6);
        const domains = tlds.map(t => `${base}.${t}`);
        const r = await fetch(`https://api.cloudflare.com/client/v4/accounts/${env.CF_ACCOUNT_ID}/registrar/domain-check`, {
          method: 'POST',
          headers: { authorization: `Bearer ${cfTok}`, 'content-type': 'application/json' },
          body: JSON.stringify({ domains }),
        });
        const data = await r.json().catch(() => ({}));
        if (!r.ok) return json({ error: 'CF domain-check fallo', detail: data }, 502);
        const list = (data.result && data.result.domains) || data.result || [];
        // `base` y `buscados` vuelven al panel para que se vea QUE se busco de verdad:
        // si el texto se normaliza, el usuario tiene que poder notarlo.
        return json({ ok: true, base, buscados: domains, results: Array.isArray(list) ? list : [] });
      }

      // Comprar un dominio y montar el sitio en el. ACCION DE DINERO: requiere key + confirm:true,
      // tope diario y anti-duplicado. Nunca compra sin confirmacion explicita del precio.
      if (url.pathname === '/api/domain/buy' && req.method === 'POST') {
        const cfTok = cfRegistrarToken(env);
        if (!cfTok || !env.CF_ACCOUNT_ID) {
          return json({
            error: 'Falta CF_REGISTRAR_TOKEN en el worker',
            como_arreglarlo: 'npx wrangler secret put CF_REGISTRAR_TOKEN -c ui/wrangler.jsonc',
            nota: 'Ponerlo como SECRET, no como variable del dashboard: un deploy reemplaza las vars y la borra.',
          }, 500);
        }
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        if (body.confirm !== true) return json({ error: 'la compra requiere confirm:true' }, 400);
        const slug = (body.slug || '').toString();
        if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
        const domain = (body.domain || '').toString().toLowerCase().trim();
        if (!/^[a-z0-9-]{1,63}\.[a-z]{2,20}$/.test(domain)) return json({ error: 'dominio invalido' }, 400);
        const registry = (await env.SITEFORGE_KV.get('registry', 'json')) || [];
        const biz = registry.find(b => b.slug === slug);
        if (!biz) return json({ error: 'negocio no encontrado en el registro' }, 404);
        const mappedSlug = await env.SITEFORGE_KV.get('domain:' + domain);
        if (mappedSlug === slug) {
          return json({ ok: true, domain, slug, live_url: `https://${domain}/`, worker_attached: true, already: true });
        }
        const pendingKey = DOMAIN_PENDING_PREFIX + domain;
        const existingPending = await env.SITEFORGE_KV.get(pendingKey, 'json');
        if (existingPending && existingPending.slug !== slug) {
          return json({ error: 'ese dominio ya está reservado para otro negocio' }, 409);
        }
        if (existingPending) {
          return json({ ok: true, pending: true, domain, slug, live_url: `https://${domain}/`, note: 'El registro sigue en curso; el Worker lo enlazará automáticamente.' }, 202);
        }
        // Guardas de dinero: tope diario + anti-duplicado
        const buys = (await env.SITEFORGE_KV.get('domain_buys', 'json')) || [];
        const today = new Date().toISOString().slice(0, 10);
        if (buys.filter(b => (b.at || '').slice(0, 10) === today).length >= 10) {
          return json({ error: 'tope diario de compras alcanzado (10). Reintenta manana.' }, 429);
        }
        if (buys.some(b => b.domain === domain)) return json({ error: 'ese dominio ya fue comprado' }, 409);
        // 1) re-check justo antes de registrar (recomendado por CF)
        const chk = await cfRequest(cfTok, `/accounts/${env.CF_ACCOUNT_ID}/registrar/domain-check`, { method: 'POST', body: JSON.stringify({ domains: [domain] }) }).then(responseData).catch(() => ({}));
        const availList = (chk.result && chk.result.domains) || chk.result || [];
        const avail = (Array.isArray(availList) ? availList : []).find(d => (d.domain || d.name) === domain);
        if (avail && avail.registrable === false) return json({ error: 'el dominio ya no esta disponible', detail: avail }, 409);
        // 2) registrar el dominio (cobra al billing profile de la cuenta CF)
        const reg = await cfRequest(cfTok, `/accounts/${env.CF_ACCOUNT_ID}/registrar/registrations`, {
          method: 'POST',
          body: JSON.stringify({ domain_name: domain }),
        });
        const regData = await responseData(reg);
        if (!reg.ok) return json({ error: 'registro fallo (revisa: registrant contact configurado, metodo de pago valido, acceso a la beta de Registrar API)', detail: regData }, 502);
        // Registrar puede completar en 201 o devolver 202 con un workflow. En
        // ambos casos guardamos el estado para que el Cron de este Worker lo
        // reintente hasta que la zona y el custom domain estén listos.
        const workflow = regData.result || {};
        const state = workflow.state || (reg.status === 201 ? 'succeeded' : 'in_progress');
        const pending = {
          domain,
          slug,
          created_at: new Date().toISOString(),
          status_url: workflow.links?.self || `/accounts/${env.CF_ACCOUNT_ID}/registrar/registrations/${encodeURIComponent(domain)}/registration-status`,
          registration_state: state,
          registration_complete: workflow.completed === true || state === 'succeeded',
        };
        const result = await finalizePendingDomain(env, pending);
        if (result.done) {
          return json({ ok: true, ...result, note: 'Sitio montado. SSL puede tardar unos minutos.' });
        }
        if (result.failed) return json({ error: result.error || 'registro de dominio fallido' }, 502);
        await env.SITEFORGE_KV.put(pendingKey, JSON.stringify({ ...pending, ...result, checked_at: new Date().toISOString() }));
        return json({
          ok: true,
          pending: true,
          domain,
          slug,
          live_url: `https://${domain}/`,
          note: 'Registro iniciado. El Worker lo enlazará y publicará automáticamente cuando Cloudflare termine.',
        }, 202);
      }

      if (url.pathname === '/api/domain/status' && req.method === 'GET') {
        const slug = (url.searchParams.get('slug') || '').toString();
        const domain = (url.searchParams.get('domain') || '').toString().toLowerCase().trim();
        if (!/^[a-z0-9-]{1,40}$/.test(slug) || !/^[a-z0-9-]{1,63}\.[a-z]{2,20}$/.test(domain)) {
          return json({ error: 'slug o dominio invalido' }, 400);
        }
        const mappedSlug = await env.SITEFORGE_KV.get('domain:' + domain);
        if (mappedSlug === slug) return json({ ok: true, domain, slug, live_url: `https://${domain}/`, ready: true });
        const pending = await env.SITEFORGE_KV.get(DOMAIN_PENDING_PREFIX + domain, 'json');
        if (pending && pending.slug === slug) {
          const lastCheck = Date.parse(pending.checked_at || '');
          // El panel puede consultar cada pocos segundos. Se intenta finalizar en la
          // propia petición, con un throttle corto para no martillar Registrar.
          if (Number.isFinite(lastCheck) && Date.now() - lastCheck < 5_000) {
            return json({
              ok: true, pending: true, domain, slug, ready: false,
              state: pending.state || pending.registration_state || 'in_progress',
            }, 202);
          }
          try {
            const result = await finalizePendingDomain(env, pending);
            if (result.done) return json({ ok: true, ...result, ready: true });
            const checkedAt = new Date().toISOString();
            if (result.failed) {
              await Promise.all([
                env.SITEFORGE_KV.put('domain-failed:' + domain, JSON.stringify({ ...pending, ...result, checked_at: checkedAt })),
                env.SITEFORGE_KV.delete(DOMAIN_PENDING_PREFIX + domain),
              ]);
              return json({ error: result.error || 'Cloudflare rechazó el dominio', domain, slug }, 502);
            }
            await env.SITEFORGE_KV.put(
              DOMAIN_PENDING_PREFIX + domain,
              JSON.stringify({ ...pending, ...result, checked_at: checkedAt }),
            );
            return json({
              ok: true, pending: true, domain, slug, ready: false,
              state: result.state || pending.registration_state || 'in_progress',
            }, 202);
          } catch (error) {
            await env.SITEFORGE_KV.put(DOMAIN_PENDING_PREFIX + domain, JSON.stringify({
              ...pending, error: String(error).slice(0, 220), checked_at: new Date().toISOString(),
            }));
            return json({ ok: true, pending: true, domain, slug, ready: false, state: 'retrying' }, 202);
          }
        }
        const failed = await env.SITEFORGE_KV.get('domain-failed:' + domain, 'json');
        if (failed && failed.slug === slug) return json({ error: failed.error || 'registro de dominio fallido', domain, slug }, 502);
        return json({ error: 'dominio no encontrado para este negocio' }, 404);
      }

      if (url.pathname === '/api/registry' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        if (!Array.isArray(body)) return json({ error: 'se espera un array' }, 400);
        await env.SITEFORGE_KV.put('registry', JSON.stringify(body));
        return json({ ok: true, count: body.length });
      }

      return json({ error: 'not found' }, 404);
    }

    return env.ASSETS.fetch(req);
  },
};
