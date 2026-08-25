import test from 'node:test';
import assert from 'node:assert/strict';
import {
  inferLeadSource,
  instagramDmUrl,
  normalizeGoogleMapsUrl,
  normalizeInstagramHandle,
} from './public/social-channels.mjs';

test('canonicaliza handles y URLs directas de Instagram', () => {
  assert.equal(normalizeInstagramHandle('@pure.artistrysk'), 'pure.artistrysk');
  assert.equal(
    normalizeInstagramHandle('https://www.instagram.com/bareface.estheticsfl/?igsh=profilecard'),
    'bareface.estheticsfl',
  );
  assert.equal(normalizeInstagramHandle('instagram.com/_u/Demo_Studio/'), 'Demo_Studio');
  assert.equal(instagramDmUrl('@demo.studio'), 'https://ig.me/m/demo.studio');
});

test('rechaza fuentes, redes distintas y rutas que no son perfiles', () => {
  for (const value of [
    'Google Maps',
    'https://www.google.com/maps/place/Demo',
    'https://facebook.com/demo',
    'https://instagram.com/p/ABC123/',
    'https://instagram.com/reel/ABC123/',
    'https://instagram.com/stories/demo/123/',
    'https://instagram.com/%E0%A4%A/',
    '@nails-by_meliza',
    '@demo (no confirmado)',
  ]) assert.equal(normalizeInstagramHandle(value), null, value);
  assert.equal(instagramDmUrl('Google Maps'), null);
});

test('solo permite enlaces seguros de Google Maps', () => {
  const maps = 'https://www.google.com/maps/place/Demo/data=!4m2!3m1!1s0xabc:0xdef';
  assert.equal(normalizeGoogleMapsUrl(maps), maps);
  assert.equal(normalizeGoogleMapsUrl('https://maps.app.goo.gl/abc123'), 'https://maps.app.goo.gl/abc123');
  assert.equal(normalizeGoogleMapsUrl('http://www.google.com/maps/place/Demo'), null);
  assert.equal(normalizeGoogleMapsUrl('https://evil.example/maps/place/Demo'), null);
});

test('conserva Google Maps como fuente, nunca como Instagram', () => {
  assert.equal(inferLeadSource({ ig: 'Google   Maps' }), 'google_maps');
  assert.equal(inferLeadSource({ maps_url: 'https://www.google.com/maps/place/Demo' }), 'google_maps');
  assert.equal(inferLeadSource({ source: 'instagram', ig: '@demo' }), 'instagram');
  assert.equal(inferLeadSource({ ig: '@demo' }), null);
});
