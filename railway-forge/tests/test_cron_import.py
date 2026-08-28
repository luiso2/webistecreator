import os
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CronImportTests(unittest.TestCase):
    def _run(self, body: str):
        code = textwrap.dedent(
            f"""
            import os
            import sys
            import types

            os.environ.setdefault("GITHUB_TOKEN", "test-token")
            playwright = types.ModuleType("playwright")
            sync_api = types.ModuleType("playwright.sync_api")
            sync_api.TimeoutError = TimeoutError
            sync_api.sync_playwright = lambda: None
            playwright.sync_api = sync_api
            sys.modules["playwright"] = playwright
            sys.modules["playwright.sync_api"] = sync_api

            import cron
            {body}
            """
        )
        return subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            timeout=15,
        )

    def test_cron_imports_discovery_from_service_root(self):
        result = self._run("assert callable(cron.main)")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_bilingual_config_labels_become_maps_categories(self):
        result = self._run(
            "assert cron._search_niche('handyman / remodelacion') == 'handyman'; "
            "assert cron._search_niche('plomeria / plumbing') == 'plumber'; "
            "assert cron._search_niche('custom / locksmith') == 'locksmith'"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_florida_rotation_locations_are_unambiguous(self):
        result = self._run(
            "cfg = {'city': 'Florida (statewide)'}; "
            "assert cron._search_location('St. Petersburg', cfg) == 'St. Petersburg, FL'; "
            "assert cron._search_location('Miami, FL', cfg) == 'Miami, FL'; "
            "assert cron._search_location('Florida (statewide)', cfg) == 'Florida'"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rotation_batches_do_not_repeat_adjacent_queries(self):
        result = self._run(
            "niches = ['a', 'b', 'c']; locations = ['one', 'two']; "
            "assert cron._rotation_pairs(niches, locations, 2, slot=0) == "
            "[('a', 'one'), ('b', 'one')]; "
            "assert cron._rotation_pairs(niches, locations, 2, slot=1) == "
            "[('c', 'one'), ('a', 'two')]"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_transient_maps_outage_does_not_fail_scheduled_service(self):
        result = self._run(
            "cron._known = lambda: set(); "
            "cron.forge.panel = lambda *args, **kwargs: {'pending': []}; "
            "cron.discover = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError('maps unavailable')); "
            "cron.DISCOVERY_QUERIES = 1; "
            "assert cron.main() == 0"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('se reintentará en el próximo cron', result.stdout)


if __name__ == "__main__":
    unittest.main()
