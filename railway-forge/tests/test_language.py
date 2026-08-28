import sys
import unittest
from pathlib import Path


FORGE = Path(__file__).resolve().parents[1]
REPO = FORGE.parent
sys.path.insert(0, str(FORGE))

import contenido_script as content  # noqa: E402


class LanguageDecisionTests(unittest.TestCase):
    def test_explicit_language_wins(self):
        decision = content.decidir_idioma({
            'requested_language': 'en-US',
            'name': 'El Rincón Venezolano',
            'address': 'San Juan, Puerto Rico',
        })
        self.assertEqual(decision['language'], 'en')
        self.assertEqual(decision['source'], 'explicit:requested_language')

    def test_hispanic_country_is_spanish(self):
        decision = content.decidir_idioma({
            'name': 'Miramar Food Truck Park',
            'address': 'San Juan, Puerto Rico',
        })
        self.assertEqual(decision['language'], 'es')
        self.assertEqual(decision['source'], 'country')

    def test_strong_business_language_beats_generic_maps_category(self):
        for name in ('DE LO MIO STREET FOOD', 'El Lider Miami', 'Paparrilla Food Truck',
                     'CDMX Taquería', 'Dayi Masajes Linfáticos Spa'):
            with self.subTest(name=name):
                self.assertEqual(content.detectar_idioma({
                    'name': name, 'nicho': 'food truck spa',
                }), 'es')

    def test_english_and_ambiguous_names_do_not_become_spanish(self):
        for name in ('CoolMint Mobile Car Detailing', 'Dapper Dogs Grooming Salon',
                     'Bella Nails', 'Taco Bell', 'Miami Scuba Diving',
                     'Panama City Beach Cleaning'):
            with self.subTest(name=name):
                self.assertEqual(content.detectar_idioma({'name': name}, fallback='en'), 'en')

    def test_country_signal_is_structured_and_reviews_cannot_fake_it(self):
        self.assertEqual(content.detectar_idioma({
            'name': 'Beach Cleaning', 'address': 'Panama City Beach, FL',
            'reviewSamples': ['We visited Mexico last month and love this company'],
        }, fallback='en'), 'en')
        self.assertEqual(content.detectar_idioma({
            'name': 'Beach Cleaning', 'address': 'Panama City, Panama',
        }, fallback='en'), 'es')
        self.assertEqual(content.detectar_idioma({
            'name': 'Servicio Demo', 'country': 'MX',
        }, fallback='en'), 'es')

    def test_strong_business_signal_beats_unrelated_english_reviews(self):
        decision = content.decidir_idioma({
            'name': 'Paparrilla Food Truck',
            'nicho': 'food truck',
            'review_samples': [
                'Amazing food and friendly service',
                'The portions were great and we will be back',
                'One of the best food trucks in Miami',
            ],
        })
        self.assertEqual(decision['language'], 'es')
        self.assertEqual(decision['source'], 'business_text')

    def test_dm_matches_primary_site_language(self):
        common = {'nombre': 'Negocio Demo', 'ciudad': 'Miami, FL', 'nicho': 'cleaning'}
        url = 'https://siteforge-demos.odd-forest-9504.workers.dev/negocio-demo/'
        message_es = content.generar_dm({**common, 'primary_language': 'es'}, url)
        message_en = content.generar_dm({**common, 'primary_language': 'en'}, url)
        self.assertTrue(message_es.startswith('Hola Negocio Demo'))
        self.assertTrue(message_en.startswith('Hi Negocio Demo'))
        self.assertIn(url, message_es)
        self.assertIn(url, message_en)

    def test_site_spec_and_dm_share_one_language(self):
        photos = {
            'hero': 'hero.jpg', 'nosotros': ['one.jpg', 'two.jpg'],
            'galeria': ['one.jpg', 'two.jpg'], 'contacto': 'one.jpg', 'logo': 'logo.jpg',
        }
        site, message, _ = content.construir({
            'slug': 'el-rincon-demo', 'nombre': 'El Rincón Demo', 'ciudad': 'Miami, FL',
            'nicho': 'food truck', 'primary_language': 'es',
        }, photos)
        self.assertEqual(site['lang'], 'es')
        self.assertTrue(message.startswith('Hola El Rincón Demo'))

    def test_english_site_has_english_scalar_metadata_and_marquee(self):
        photos = {
            'hero': 'hero.jpg', 'nosotros': ['one.jpg', 'two.jpg'],
            'galeria': ['one.jpg', 'two.jpg'], 'contacto': 'one.jpg', 'logo': 'logo.jpg',
        }
        site, message, _ = content.construir({
            'slug': 'coolmint-demo', 'nombre': 'CoolMint Mobile Car Detailing',
            'ciudad': 'Miami, FL', 'nicho': 'detailing', 'primary_language': 'en',
        }, photos)
        self.assertEqual(site['head']['title'], 'CoolMint Mobile Car Detailing · Services in Miami, FL')
        self.assertEqual(site['jsonld']['description'], 'Services in Miami, FL.')
        self.assertIn('Local service', site['marquee'])
        self.assertNotIn('Servicio local', site['marquee'])
        self.assertEqual(site['strip'][0]['valor'], 'Services')
        self.assertTrue(message.startswith('Hi CoolMint Mobile Car Detailing'))

    def test_unknown_website_status_uses_neutral_outreach_copy(self):
        url = 'https://siteforge-demos.odd-forest-9504.workers.dev/demo/'
        message_es = content.generar_dm({
            'nombre': 'Demo', 'ciudad': 'Miami', 'primary_language': 'es',
        }, url)
        message_en = content.generar_dm({
            'nombre': 'Demo', 'ciudad': 'Miami', 'primary_language': 'en',
        }, url)
        self.assertNotIn('No vi un website propio', message_es)
        self.assertNotIn('could not find a dedicated website', message_en)


class LanguagePipelineSourceTests(unittest.TestCase):
    def test_pipeline_does_not_force_maps_or_instagram_language(self):
        main = (FORGE / 'main.py').read_text(encoding='utf-8')
        builder = (FORGE / 'scripts' / 'build_maps_site.py').read_text(encoding='utf-8')
        self.assertNotIn("hechos['idioma_principal'] = 'en'", main)
        self.assertNotIn("hechos['idioma_principal'] = 'es'", main)
        self.assertNotIn('content["lang"] = "en"', builder)
        self.assertIn('cs.decidir_idioma', main)
        self.assertIn('language_decision = decidir_idioma', builder)

    def test_templates_scope_preference_per_site_and_use_primary_language(self):
        for template in (
            REPO / 'templates' / 'dark-v2' / 'index.html',
            REPO / 'templates' / 'light-v2' / 'index.html',
            FORGE / 'templates' / 'dark-v2' / 'index.html',
        ):
            with self.subTest(template=template):
                html = template.read_text(encoding='utf-8')
                self.assertIn('siteforge:lang:', html)
                self.assertIn('document.documentElement.lang', html)
                self.assertNotIn("localStorage.getItem('lang')", html)
                self.assertNotIn('navigator.language', html)

    def test_registry_update_preserves_unknown_website_flag_and_accepts_v3(self):
        worker = (REPO / 'ui' / 'worker.js').read_text(encoding='utf-8')
        self.assertIn("typeof body.has_own_site === 'boolean'", worker)
        self.assertIn('[2, 3].includes(Number(body.message_version))', worker)
        self.assertIn("language must be es or en", worker)

    def test_explicit_language_reaches_direct_and_discovery_builds(self):
        worker = (REPO / 'ui' / 'worker.js').read_text(encoding='utf-8')
        main = (FORGE / 'main.py').read_text(encoding='utf-8')
        self.assertIn("request?.language || 'auto'", worker)
        self.assertIn("...(buildLanguage ? { language: buildLanguage } : {})", worker)
        claim_block = worker[worker.index('async claim('):worker.index('async progress(')]
        self.assertIn("...(['es', 'en'].includes(q.language) ? { language: q.language } : {})", claim_block)
        self.assertIn("item.get('language')", main)
        self.assertIn("{'language': request.get('language')}", main)

    def test_partial_registry_upsert_does_not_reset_operational_fields(self):
        worker = (REPO / 'ui' / 'worker.js').read_text(encoding='utf-8')
        endpoint = worker[worker.index("if (url.pathname === '/api/public/registry-upsert'"):
                          worker.index("if (url.pathname.startsWith('/api/'))")]
        self.assertNotIn("status: 'staging'", endpoint)
        self.assertNotIn("outreach: 'pending_manual'", endpoint)
        self.assertIn("name: S(body.name, 120)", endpoint)
        self.assertNotIn("name: S(body.name, 120) || slug", endpoint)
        self.assertIn("language: ['es', 'en', 'fr'].includes(body.language) ? body.language : undefined", endpoint)

    def test_site_update_resynchronizes_generated_message(self):
        main = (FORGE / 'main.py').read_text(encoding='utf-8')
        update_block = main[main.index('def procesar_actualizacion'):main.index('def procesar_nombre')]
        self.assertIn("panel('/api/public/registry-upsert'", update_block)
        self.assertIn("'primary_language': lang", update_block)
        self.assertIn("'message_version': 3", update_block)


if __name__ == '__main__':
    unittest.main()
