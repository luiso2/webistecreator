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
from maps_research import parse_rating_reviews  # noqa: E402


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

    def test_business_summary_is_not_overwritten_by_review_rows(self):
        labels = ["4.9 stars", "82 reviews", "5 stars, 79 reviews", "1 star, 1 review"]
        self.assertEqual(_parse_rating_reviews(labels), (4.9, 82))
        self.assertEqual(parse_rating_reviews(labels), ("4.9", "82"))


if __name__ == "__main__":
    unittest.main()
