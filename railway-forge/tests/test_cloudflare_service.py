import importlib
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class CloudflareServiceTests(unittest.TestCase):
    def test_health_snapshot_does_not_expose_secrets(self):
        os.environ["FORGE_ROLE"] = "cron"
        module = importlib.import_module("cloudflare_service")
        snapshot = module.health_snapshot()
        self.assertTrue(snapshot["ok"])
        self.assertEqual(snapshot["runtime"], "cloudflare-container")
        self.assertEqual(snapshot["role"], "cron")
        serialized = str(snapshot).lower()
        self.assertNotIn("github_token", serialized)
        self.assertNotIn("publish_key", serialized)

    def test_cron_role_does_not_start_forge_worker(self):
        os.environ["FORGE_ROLE"] = "cron"
        module = importlib.import_module("cloudflare_service")
        module._start_worker()
        self.assertFalse(module.health_snapshot()["worker_alive"])


if __name__ == "__main__":
    unittest.main()
