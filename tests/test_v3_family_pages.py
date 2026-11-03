"""Four standalone family pages: 6/7/3/4, source fidelity and escaping."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from v3_build_site import BASE_URL, CSS, REPO_BLOB, build
from v3_family_pages import FAMILIES, page_for_family
from v3_validate import CATALOG, strict_load


class FamilyPagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = strict_load(CATALOG)["items"]

    def test_all_groups_have_expected_members_and_links(self):
        self.assertEqual([x[2] for x in FAMILIES], [6, 7, 3, 4])
        for slug, label, count, ids, _ in FAMILIES:
            with self.subTest(slug=slug):
                html = page_for_family(slug, self.items, BASE_URL, REPO_BLOB, CSS)
                self.assertIn(f"<h1 id=\"group-title\">{label}</h1>", html)
                self.assertIn("0/20", html)
                self.assertIn(f"/Vong-co/nhom/{slug}/", html)
                self.assertEqual(html.count('class="family-piece"'), count)
                members = [item for item in self.items if item["family_label"] == label]
                self.assertEqual(tuple(p["id"] for p in members), ids)
                for item in members:
                    self.assertIn("../../bai/" + item["slug"] + "/", html)
                    self.assertIn(item["title"], html)
                for item in self.items:
                    if item not in members:
                        self.assertNotIn(f'Mở hồ sơ bài {item["id"]:02d}', html)
                for another, *_ in FAMILIES:
                    self.assertIn(f'href="../{another}/"', html)

    def test_wrong_family_count_rejected(self):
        catalog = copy.deepcopy(self.items)
        catalog[0]["family_label"] = "Bốn Oán"
        with self.assertRaisesRegex(ValueError, "không khớp"):
            page_for_family("sau-bac", catalog, BASE_URL, REPO_BLOB, CSS)

    def test_untrusted_catalog_data_escaped(self):
        catalog = copy.deepcopy(self.items)
        catalog[0]["title"] = '<img src=x onerror=alert("x")>'
        catalog[0]["research_note"] = '<script>alert(1)</script>'
        html = page_for_family("sau-bac", catalog, BASE_URL, REPO_BLOB, CSS)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn('<img src=x', html)
        self.assertNotIn('<script>alert(1)</script>', html)


if __name__ == "__main__":
    unittest.main()
