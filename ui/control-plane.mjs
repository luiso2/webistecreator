/*
 * Siteforge Control Plane primitives.
 *
 * This module deliberately has no Cloudflare-specific imports.  Keeping the
 * schema, planner validation and tool metadata portable lets the Worker and
 * the test suite exercise the same rules.  The current product is a single
 * owner installation: there is no tenant dimension yet.
 */

export const SITE_SPEC_VERSION = 1;
export const PLAN_VERSION = 1;
export const MAX_PLAN_STEPS = 8;
export const MAX_PATCH_DEPTH = 6;
export const MAX_PATCH_KEYS = 120;
export const MAX_PATCH_BYTES = 16_000;

const SAFE_SLUG = /^[a-z0-9-]{1,40}$/;
const SAFE_TEXT = value => String(value ?? '')
  .replace(/[<>\x00-\x1F\x7F]/g, '')
  .replace(/\s+/g, ' ')
  .trim();

export const normalizeSlug = value => {
  const slug = SAFE_TEXT(value).toLowerCase();
  return SAFE_SLUG.test(slug) ? slug : null;
};

export const normalizeRef = value => {
  if (typeof value === 'string') {
    const text = SAFE_TEXT(value).slice(0, 120);
    return text ? { query: text } : null;
  }
  if (!value || typeof value !== 'object' || Array.isArray(value)) return null;
  const slug = value.slug === undefined ? null : normalizeSlug(value.slug);
  const query = value.query === undefined ? null : SAFE_TEXT(value.query).slice(0, 120);
  const city = value.city === undefined ? null : SAFE_TEXT(value.city).slice(0, 80);
  if (value.slug !== undefined && !slug) return null;
  if (!slug && !query) return null;
  return { ...(slug ? { slug } : {}), ...(query ? { query } : {}), ...(city ? { city } : {}) };
};

const clone = value => JSON.parse(JSON.stringify(value));

const sanitizeValue = (value, depth = 0, state = { keys: 0 }) => {
  if (depth > MAX_PATCH_DEPTH) throw new Error(`patch demasiado profundo (máximo ${MAX_PATCH_DEPTH})`);
  if (value === null || typeof value === 'number' || typeof value === 'boolean') return value;
  if (typeof value === 'string') return SAFE_TEXT(value).slice(0, 2_000);
  if (Array.isArray(value)) {
    if (value.length > 40) throw new Error('las listas de un patch no pueden superar 40 elementos');
    return value.map(item => sanitizeValue(item, depth + 1, state));
  }
  if (!value || typeof value !== 'object') throw new Error('valor de patch inválido');
  const output = {};
  for (const [key, item] of Object.entries(value)) {
    state.keys += 1;
    if (state.keys > MAX_PATCH_KEYS) throw new Error('patch demasiado grande');
    const cleanKey = SAFE_TEXT(key).slice(0, 80);
    if (!cleanKey || cleanKey.includes('__') || cleanKey === 'constructor' || cleanKey === 'prototype') {
      throw new Error(`clave de patch no permitida: ${key}`);
    }
    output[cleanKey] = sanitizeValue(item, depth + 1, state);
  }
  return output;
};

export const sanitizePatch = patch => {
  if (!patch || typeof patch !== 'object' || Array.isArray(patch)) {
    throw new Error('patch debe ser un objeto');
  }
  const clean = sanitizeValue(patch);
  if (JSON.stringify(clean).length > MAX_PATCH_BYTES) throw new Error('patch supera el límite de 16 KB');
  return clean;
};

export const deepMerge = (base, patch) => {
  const result = base && typeof base === 'object' && !Array.isArray(base) ? clone(base) : {};
  for (const [key, value] of Object.entries(patch || {})) {
    if (value && typeof value === 'object' && !Array.isArray(value)
      && result[key] && typeof result[key] === 'object' && !Array.isArray(result[key])) {
      result[key] = deepMerge(result[key], value);
    } else {
      result[key] = clone(value);
    }
  }
  return result;
};

export const siteSpecFromRegistry = site => {
  const slug = normalizeSlug(site?.slug);
  if (!slug) throw new Error('registro sin slug válido');
  const name = SAFE_TEXT(site.name || slug).slice(0, 120);
  return {
    version: SITE_SPEC_VERSION,
    revision: 1,
    siteId: slug,
    slug,
    business: {
      name,
      industry: SAFE_TEXT(site.industry || '').slice(0, 100) || null,
      location: SAFE_TEXT(site.city || '').slice(0, 100) || null,
      audience: null,
      primaryGoal: 'lead_generation',
    },
    branding: {
      palette: site.color || null,
      logo: null,
      voice: null,
    },
    pages: [{ id: 'home', path: '/', title: name, sections: [] }],
    features: [],
    integrations: [],
    seo: {
      title: null,
      description: null,
      keywords: [],
    },
    deployment: {
      status: site.url_demo ? 'published' : 'draft',
      url: site.url_demo || null,
      currentRevision: 1,
    },
    contentPatch: {},
    metadata: {
      source: 'registry-adapter',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
  };
};

export const validateSiteSpec = spec => {
  const errors = [];
  if (!spec || typeof spec !== 'object' || Array.isArray(spec)) return ['spec debe ser un objeto'];
  if (spec.version !== SITE_SPEC_VERSION) errors.push(`version debe ser ${SITE_SPEC_VERSION}`);
  if (!normalizeSlug(spec.slug)) errors.push('slug inválido');
  if (spec.siteId !== spec.slug) errors.push('siteId debe coincidir con slug');
  if (!Number.isInteger(spec.revision) || spec.revision < 1) errors.push('revision inválida');
  if (!spec.business || typeof spec.business !== 'object') errors.push('business requerido');
  if (!Array.isArray(spec.pages)) errors.push('pages debe ser una lista');
  if (!Array.isArray(spec.features)) errors.push('features debe ser una lista');
  if (!Array.isArray(spec.integrations)) errors.push('integrations debe ser una lista');
  if (!spec.deployment || typeof spec.deployment !== 'object') errors.push('deployment requerido');
  try { sanitizePatch(spec.contentPatch || {}); } catch (error) { errors.push(error.message); }
  return errors;
};

export const assertSiteSpec = spec => {
  const errors = validateSiteSpec(spec);
  if (errors.length) throw new Error(`SiteSpec inválido: ${errors.join('; ')}`);
  return spec;
};

export const TOOL_DEFINITIONS = Object.freeze([
  { name: 'website.search', description: 'Busca websites del registro por nombre, ciudad, teléfono, email o slug.', permission: 'READ', riskLevel: 'LOW' },
  { name: 'website.get', description: 'Obtiene el registro y el SiteSpec versionado de un website.', permission: 'READ', riskLevel: 'LOW' },
  { name: 'website.update', description: 'Actualiza el SiteSpec de forma determinista sin publicar.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW' },
  { name: 'website.content.update', description: 'Aplica un patch de contenido respaldado por el SiteSpec.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW' },
  { name: 'website.branding.update', description: 'Actualiza branding y paleta permitida del website.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW' },
  { name: 'website.preview', description: 'Valida y devuelve la versión de preview del SiteSpec.', permission: 'READ', riskLevel: 'LOW' },
  { name: 'website.test', description: 'Ejecuta validaciones deterministas del SiteSpec y del registro.', permission: 'READ', riskLevel: 'LOW' },
  { name: 'website.publish', description: 'Publica una revisión mediante la forja Railway y el Worker compartido.', permission: 'MEDIUM_RISK_WRITE', riskLevel: 'MEDIUM' },
  { name: 'website.rollback', description: 'Restaura una revisión anterior y la deja lista para publicar.', permission: 'HIGH_RISK_WRITE', riskLevel: 'HIGH' },
  { name: 'website.page.create', description: 'Crea una página en el SiteSpec.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'scaffolded' },
  { name: 'website.page.update', description: 'Actualiza una página del SiteSpec.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'scaffolded' },
  { name: 'website.page.delete', description: 'Elimina una página del SiteSpec.', permission: 'DESTRUCTIVE', riskLevel: 'HIGH', status: 'scaffolded' },
  { name: 'website.page.list', description: 'Lista las páginas del SiteSpec.', permission: 'READ', riskLevel: 'LOW', status: 'scaffolded' },
  { name: 'website.section.add', description: 'Añade una sección reutilizable a una página.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'scaffolded' },
  { name: 'website.section.update', description: 'Actualiza una sección reutilizable.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'scaffolded' },
  { name: 'website.section.remove', description: 'Elimina una sección.', permission: 'DESTRUCTIVE', riskLevel: 'HIGH', status: 'scaffolded' },
  { name: 'website.section.reorder', description: 'Reordena secciones de una página.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'scaffolded' },
  { name: 'website.image.update', description: 'Actualiza la referencia de una imagen en el contenido.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'adapter' },
  { name: 'website.seo.configure', description: 'Configura SEO versionado del website.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'adapter' },
  { name: 'website.seo.analyze', description: 'Analiza el SEO determinista del SiteSpec.', permission: 'READ', riskLevel: 'LOW', status: 'adapter' },
  { name: 'website.analytics.get', description: 'Consulta métricas disponibles del website.', permission: 'READ', riskLevel: 'LOW', status: 'adapter_pending' },
  { name: 'website.form.create', description: 'Registra una configuración de formulario.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'adapter' },
  { name: 'website.form.update', description: 'Actualiza una configuración de formulario.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'adapter' },
  { name: 'website.booking.install', description: 'Registra una integración de reservas.', permission: 'MEDIUM_RISK_WRITE', riskLevel: 'MEDIUM', status: 'adapter' },
  { name: 'website.booking.configure', description: 'Configura la integración de reservas.', permission: 'MEDIUM_RISK_WRITE', riskLevel: 'MEDIUM', status: 'adapter' },
  { name: 'website.whatsapp.install', description: 'Registra la integración de WhatsApp.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'adapter' },
  { name: 'website.whatsapp.configure', description: 'Configura WhatsApp del website.', permission: 'LOW_RISK_WRITE', riskLevel: 'LOW', status: 'adapter' },
  { name: 'website.payment.install', description: 'Registra una integración de pagos.', permission: 'HIGH_RISK_WRITE', riskLevel: 'HIGH', status: 'adapter_pending' },
].map(tool => ({
  ...tool,
  handler: `control.${tool.name}`,
  inputSchema: { type: 'object', additionalProperties: true },
  outputSchema: { type: 'object', additionalProperties: true },
})));

export const toolDefinition = name => TOOL_DEFINITIONS.find(tool => tool.name === name) || null;

export const validatePlan = plan => {
  if (!plan || typeof plan !== 'object' || Array.isArray(plan)) throw new Error('plan debe ser un objeto');
  const steps = Array.isArray(plan.steps) ? plan.steps : [{ tool: plan.tool, args: plan.args || {} }];
  if (!steps.length || steps.length > MAX_PLAN_STEPS) throw new Error(`el plan debe tener entre 1 y ${MAX_PLAN_STEPS} pasos`);
  return {
    version: Number(plan.version || PLAN_VERSION),
    goal: SAFE_TEXT(plan.goal || 'Siteforge operation').slice(0, 200),
    confirmed: plan.confirmed === true,
    steps: steps.map((step, index) => {
      const name = SAFE_TEXT(step?.tool || '');
      if (!toolDefinition(name)) throw new Error(`tool no registrada en el paso ${index + 1}: ${name}`);
      if (!step.args || typeof step.args !== 'object' || Array.isArray(step.args)) throw new Error(`args inválidos en el paso ${index + 1}`);
      return { tool: name, args: sanitizeValue(step.args) };
    }),
  };
};

export const permissionForPlan = (plan, tool) => {
  const definition = toolDefinition(tool);
  if (!definition) throw new Error(`tool no registrada: ${tool}`);
  if (definition.permission === 'HIGH_RISK_WRITE' || definition.permission === 'DESTRUCTIVE') {
    if (!plan.confirmed) throw new Error(`${tool} requiere confirmed:true`);
  }
  if (definition.name === 'website.publish' && !plan.confirmed) {
    throw new Error('website.publish requiere confirmed:true');
  }
  return definition.permission;
};
