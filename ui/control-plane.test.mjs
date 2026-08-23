import test from 'node:test';
import assert from 'node:assert/strict';
import {
  deepMerge,
  normalizeRef,
  permissionForPlan,
  sanitizePatch,
  siteSpecFromRegistry,
  validatePlan,
  validateSiteSpec,
} from './control-plane.mjs';

test('normaliza referencias por slug y búsqueda', () => {
  assert.deepEqual(normalizeRef({ slug: 'miami-handyman', city: 'Miami' }), {
    slug: 'miami-handyman', city: 'Miami',
  });
  assert.deepEqual(normalizeRef('  Miami Handyman  '), { query: 'Miami Handyman' });
  assert.equal(normalizeRef({ slug: 'Bad Slug!' }), null);
});

test('crea y valida un SiteSpec desde el registro existente', () => {
  const spec = siteSpecFromRegistry({ slug: 'demo-site', name: 'Demo Site', city: 'Miami', url_demo: 'https://demo.example' });
  assert.equal(spec.version, 1);
  assert.equal(spec.siteId, 'demo-site');
  assert.deepEqual(validateSiteSpec(spec), []);
});

test('deepMerge preserva campos y reemplaza listas de forma determinista', () => {
  const merged = deepMerge({ hero: { title: 'old', tags: ['a'] }, keep: true }, { hero: { title: 'new', tags: ['b'] } });
  assert.deepEqual(merged, { hero: { title: 'new', tags: ['b'] }, keep: true });
});

test('rechaza claves peligrosas y patches demasiado grandes', () => {
  assert.throws(() => sanitizePatch(JSON.parse('{"__proto__":{"polluted":true}}')), /clave.*permitida/i);
  assert.equal(sanitizePatch({ hero: { copy: '<script>alert(1)</script>' } }).hero.copy, 'scriptalert(1)/script');
});

test('valida planes y exige confirmación para publicar', () => {
  const plan = validatePlan({ goal: 'Publicar', steps: [{ tool: 'website.publish', args: { site: { slug: 'demo-site' } } }] });
  assert.throws(() => permissionForPlan(plan, 'website.publish'), /confirmed/);
  const confirmed = validatePlan({ confirmed: true, steps: [{ tool: 'website.publish', args: { site: { slug: 'demo-site' } } }] });
  assert.equal(permissionForPlan(confirmed, 'website.publish'), 'MEDIUM_RISK_WRITE');
});
