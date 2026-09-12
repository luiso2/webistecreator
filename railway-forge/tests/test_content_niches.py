import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import contenido_script


class ContentNicheTests(unittest.TestCase):
    def test_food_truck_uses_food_copy_instead_of_contractor_copy(self):
        niche_id, niche = contenido_script.detectar_nicho({
            "nombre": "La Coolmena LLC",
            "nicho": "food truck",
        })

        self.assertEqual(niche_id, "food_truck")
        self.assertEqual(niche["h1"][0]["en"], "Made-to-order flavor,")
        self.assertNotIn("project", niche["h1"][0]["en"].lower())


if __name__ == "__main__":
    unittest.main()
