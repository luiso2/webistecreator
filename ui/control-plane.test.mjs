import test from 'node:test';
import assert from 'node:assert/strict';
import {
  businessIdentityKeys,
  businessesShareIdentity,
  deepMerge,
  googleMapsIdentity,
  normalizeRef,
  permissionForPlan,
  sanitizePatch,
  siteSpecFromRegistry,
  validatePlan,
  validateSiteSpec,
} from './control-plane.mjs';

test('crea identidad estable con Maps, teléfono y nombre normalizado', () => {
  const business = {
    name: 'Café Río & Spa',
    city: 'Miami, Florida',
    phone: '+1 (305) 555-0100',
    maps_url: 'https://www.google.com/maps/place/Cafe+Rio/data=!4m2!3m1!1s0xabc:0xdef',
  };
  const keys = businessIdentityKeys(business);
  assert.ok(keys.includes('maps:place:0xabc:0xdef'));
  assert.ok(keys.includes('phone:13055550100'));
  assert.ok(keys.includes('name-city:cafe rio spa|miami florida'));
  assert.equal(googleMapsIdentity('https://evil.example/maps/place/Cafe'), null);
});

test('detecta un negocio existente aunque cambie el slug', () => {
  assert.equal(businessesShareIdentity(
    { name: 'Monique Austin Studio', city: 'Miami', phone: '305-555-0199' },
    { slug: 'monique-austin', name: 'Monique A. Studio', city: 'Hialeah', phone: '+1 305 555 0199' },
  ), true);
});

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
