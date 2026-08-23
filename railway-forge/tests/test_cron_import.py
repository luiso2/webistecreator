import os
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CronImportTests(unittest.TestCase):
    def test_cron_imports_discovery_from_service_root(self):
        code = textwrap.dedent(
            """
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
            assert callable(cron.main)
            """
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
