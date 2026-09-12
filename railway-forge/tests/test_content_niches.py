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

        site, message, detected = contenido_script.construir({
            "slug": "la-coolmena-llc",
            "nombre": "La Coolmena LLC",
            "ciudad": "Kissimmee, FL",
            "nicho": "food truck",
            "primary_language": "en",
            "phone": "(321) 447-0380",
        }, {
            "hero": "gmaps-1.jpg",
            "nosotros": ["gmaps-2.jpg", "gmaps-3.jpg"],
            "galeria": [f"gmaps-{index}.jpg" for index in range(2, 8)],
            "contacto": "gmaps-2.jpg",
            "logo": "gmaps-1.jpg",
        })
        serialized = str(site).lower()
        self.assertEqual(detected, "food_truck")
        self.assertNotIn("your project", serialized)
        self.assertNotIn("clear quote", serialized)
        self.assertNotIn("handover", serialized)
        self.assertEqual(site["jsonld"]["@type"], "FoodEstablishment")
        self.assertEqual(site["paleta"]["hue"], 28)
        self.assertIn("looking for local food", message)
        self.assertIn("nothing has been published under your domain", message)


if __name__ == "__main__":
    unittest.main()
