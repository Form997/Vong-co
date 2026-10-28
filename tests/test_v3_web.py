"""Static integrity checks for the V3 Vietnamese web viewer."""

import html.parser
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HTML = ROOT / "web" / "v3" / "index.html"


class ScriptCollector(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.inside = not any(k == "src" for k, _ in attrs)
            if self.inside:
                self.scripts.append("")

    def handle_data(self, data):
        if self.inside and self.scripts:
            self.scripts[-1] += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.inside = False


class V3WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML.read_text(encoding="utf-8")
        parser = ScriptCollector()
        parser.feed(cls.html)
        cls.scripts = parser.scripts

    def test_vi_mobile_layout(self):
        self.assertIn('<html lang="vi">', self.html)
        self.assertIn('name="viewport"', self.html)
        self.assertIn("@media(max-width:560px)", self.html)

    def test_catalog_is_fetched_from_versioned_json(self):
        self.assertIn('const DATA_URL = "../../data/v3/catalog.json";', self.html)
        self.assertTrue((ROOT / "data/v3/catalog.json").is_file())

    def test_four_group_filters(self):
        for label in ("sau-bac", "bay-le", "ba-nam", "bon-oan"):
            with self.subTest(label=label):
                self.assertIn(f'data-group="{label}"', self.html)

    def test_user_text_uses_text_content_not_inner_html(self):
        self.assertIn("e.textContent = String(text)", self.html)
        self.assertNotIn("innerHTML", self.html)

    def test_status_disclaimer_present(self):
        self.assertIn("0/20", self.html)
        self.assertIn("20/20", self.html)
        self.assertIn("chưa", self.html.lower())

    def test_editorial_design_uses_one_cohesive_accessible_palette(self):
        self.assertIn("--paper:#f6f4ee", self.html)
        self.assertIn("--forest:#10382f", self.html)
        self.assertIn('class="hero-art" aria-hidden="true"', self.html)
        self.assertIn('class="hero-copy"', self.html)
        self.assertIn("prefers-reduced-motion:reduce", self.html)
        self.assertIn(":focus-visible", self.html)
        self.assertIn('id="tra-cuu"', self.html)

    def test_ui_is_independent_of_external_fonts_or_decorative_assets(self):
        self.assertNotIn("@import", self.html)
        self.assertNotIn("fonts.googleapis.com", self.html)
        self.assertNotIn("unsplash", self.html.lower())
        self.assertNotIn("<iframe", self.html.lower())

    def test_inline_script_present(self):
        self.assertEqual(len(self.scripts), 1)
        self.assertIn("function updateDetail()", self.scripts[0])


if __name__ == "__main__":
    unittest.main()
