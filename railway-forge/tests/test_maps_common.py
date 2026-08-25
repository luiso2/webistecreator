import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from maps_common import instagram_handle, is_own_website, safe_google_maps_url  # noqa: E402


class MapsWebsiteFilterTests(unittest.TestCase):
    def test_profiles_and_booking_pages_are_not_owned_websites(self):
        for url in (
            "https://instagram.com/example",
            "https://example.booksy.com/",
            "https://my-business.square.site/",
            "https://linktr.ee/example",
        ):
            with self.subTest(url=url):
                self.assertFalse(is_own_website(url))

    def test_hosted_builders_count_as_real_websites(self):
        for url in (
            "https://example.wixsite.com/home",
            "https://example.squarespace.com/",
            "https://example.webflow.io/",
            "https://example.wordpress.com/",
            "https://example.my.canva.site/",
            "https://business.example.com/",
        ):
            with self.subTest(url=url):
                self.assertTrue(is_own_website(url))

    def test_exact_maps_url_is_strictly_validated(self):
        valid = "https://www.google.com/maps/place/Demo/data=!4m2!3m1!1s0xabc:0xdef"
        self.assertEqual(safe_google_maps_url(valid), valid)
        self.assertIsNone(safe_google_maps_url("http://www.google.com/maps/place/Demo"))
        self.assertIsNone(safe_google_maps_url("https://example.com/maps/place/Demo"))

    def test_instagram_handles_and_profile_urls_are_canonicalized(self):
        self.assertEqual(instagram_handle("@pure.artistrysk"), "pure.artistrysk")
        self.assertEqual(
            instagram_handle("https://www.instagram.com/bareface.estheticsfl/?igsh=profilecard"),
            "bareface.estheticsfl",
        )
        self.assertEqual(instagram_handle("instagram.com/_u/demo_studio/"), "demo_studio")

    def test_non_profile_channels_never_become_instagram_handles(self):
        for value in (
            "Google Maps",
            "https://www.google.com/maps/place/Demo",
            "https://facebook.com/demo",
            "https://instagram.com/p/ABC123/",
            "https://instagram.com/reel/ABC123/",
            "https://instagram.com/stories/demo/123/",
            "@nails-by_meliza",
            "@demo (no confirmado)",
        ):
            with self.subTest(value=value):
                self.assertIsNone(instagram_handle(value))


if __name__ == "__main__":
    unittest.main()
