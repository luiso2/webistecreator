import sys
import types
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

try:
    import playwright.sync_api  # noqa: F401
except ModuleNotFoundError:
    playwright = types.ModuleType("playwright")
    sync_api = types.ModuleType("playwright.sync_api")
    sync_api.TimeoutError = TimeoutError
    sync_api.sync_playwright = lambda: None
    playwright.sync_api = sync_api
    sys.modules["playwright"] = playwright
    sys.modules["playwright.sync_api"] = sync_api

from maps_discover import _parse_rating_reviews  # noqa: E402


class MapsRatingParserTests(unittest.TestCase):
    def test_combined_english_maps_label(self):
        self.assertEqual(
            _parse_rating_reviews(["4.8 stars 127 reviews"]),
            (4.8, 127),
        )

    def test_separate_labels_and_abbreviated_reviews(self):
        self.assertEqual(
            _parse_rating_reviews(["4.9 stars", "1.2K Google reviews"]),
            (4.9, 1200),
        )

    def test_spanish_maps_label_is_safe_fallback(self):
        self.assertEqual(
            _parse_rating_reviews(["4,7 estrellas 89 reseñas"]),
            (4.7, 89),
        )


if __name__ == "__main__":
    unittest.main()
