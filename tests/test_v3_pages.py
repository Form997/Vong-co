"""GitHub Pages V3.1: strict artifact allowlist, 20 dedicated pages and HTTP."""

from __future__ import annotations

import functools
from html import escape
import http.server
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from v3_build_site import build, generate_sitemap, page_for_piece
from v3_validate import strict_load, CATALOG


class V31PagesBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = strict_load(CATALOG)["items"]

    def test_build_copies_only_public_metadata_and_20_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            result = build(site)
            self.assertEqual(result["status"], "pass")
            self.assertEqual(result["pieces"], 20)
            self.assertEqual(result["variants"], 30)
            self.assertEqual(result["detail_pages"], 20)
            self.assertEqual(result["file_count"], 40)  # 14 base + 20 pieces + 6 country pages
            names = set(result["published_files"])
            self.assertEqual(len(names), 40)
            self.assertIn(".nojekyll", names)
            self.assertIn("web/v3/index.html", names)
            self.assertIn("web/v3/legal.html", names)
            for slug in ("my", "nga", "trung-quoc", "uc", "nhat-ban", "han-quoc"):
                self.assertIn(f"web/v3/quoc-gia/{slug}.html", names)
            self.assertIn("data/v3_2/phrase_index.json", names)
            self.assertIn("data/v3_2/schema.json", names)
            self.assertIn("data/v3_3/phrase_index.json", names)
            self.assertIn("data/v3_3/schema.json", names)
            self.assertIn("data/v3_4/phrase_index.json", names)
            self.assertIn("data/v3_4/schema.json", names)
            for item in self.catalog:
                self.assertIn(f'bai/{item["slug"]}/index.html', names)
            self.assertFalse(any(p.startswith(("ban-to/", "docs/", ".github/", "tests/", "scripts/")) for p in names))
            self.assertFalse(any(p.endswith((".mp3", ".pdf", ".zip", ".wav", ".py", ".md")) for p in names))
            self.assertFalse(result["includes_rights_restricted_media"])
            self.assertEqual(result["indexed_lesson_pieces"], 5)
            self.assertEqual(result["indexed_lesson_phrases"], 252)

    def test_sitemap_contains_all_20_canonical_pages(self):
        sitemap = generate_sitemap(self.catalog)
        self.assertEqual(sitemap.count("<url>"), 29)  # root, browser, legal page, 6 countries, 20 pieces
        self.assertIn("/Vong-co/web/v3/legal.html", sitemap)
        for slug in ("my", "nga", "trung-quoc", "uc", "nhat-ban", "han-quoc"):
            self.assertIn(f"/Vong-co/web/v3/quoc-gia/{slug}.html", sitemap)
        for item in self.catalog:
            self.assertIn(f'/Vong-co/bai/{item["slug"]}/', sitemap)

    def test_page_has_sources_and_explicit_not_approved(self):
        for item in self.catalog:
            with self.subTest(piece=item["id"]):
                i = item["id"] - 1
                html = page_for_piece(item, self.catalog[i-1] if i else None,
                                      self.catalog[i+1] if i < 19 else None)
                self.assertIn(item["title"], html)
                self.assertIn(item["family_label"], html)
                self.assertIn("0/20", html)
                self.assertIn('rel="canonical"', html)
                self.assertIn("Biên bản rà nguồn V2", html)
                self.assertIn("Hồ sơ bài đầy đủ", html)
                self.assertIn("../../web/v3/", html)
                for v in item["variants"]:
                    self.assertIn(v["reference_url"], html)
                    self.assertIn(escape(v["qualification"], quote=True), html)

    def test_external_values_are_html_escaped(self):
        data = json.loads(json.dumps(self.catalog[0]))
        data["title"] = '<img src=x onerror=alert("bad")>'
        data["research_note"] = 'X & Y <script>alert(1)</script>'
        data["variants"][0]["qualification"] = '<script>alert("x")</script>'
        html = page_for_piece(data, None, None)
        self.assertNotIn('<img src=x', html)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;img", html)
        self.assertIn("&lt;script&gt;", html)

    def test_nonempty_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            site.mkdir()
            (site / "old.html").write_text("stale", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "rỗng"):
                build(site)

    def test_site_is_served_at_all_20_distinct_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            build(site)
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
            server.daemon_threads = True
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            root_url = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                for path in ("/", "/web/v3/", "/data/v3/catalog.json", "/data/v3/schema.json", "/web/v3/legal.html",
                             "/web/v3/quoc-gia/my.html", "/web/v3/quoc-gia/nga.html",
                             "/web/v3/quoc-gia/trung-quoc.html", "/web/v3/quoc-gia/uc.html",
                             "/web/v3/quoc-gia/nhat-ban.html", "/web/v3/quoc-gia/han-quoc.html",
                             "/sitemap.xml"):
                    with self.subTest(path=path):
                        with urlopen(root_url + path, timeout=5) as response:
                            self.assertEqual(response.status, 200)
                for item in self.catalog:
                    with self.subTest(piece=item["id"]):
                        with urlopen(root_url + "/bai/" + item["slug"] + "/", timeout=5) as response:
                            html = response.read().decode("utf-8")
                            self.assertEqual(response.status, 200)
                            self.assertIn(item["title"], html)
                with urlopen(root_url + "/data/v3/catalog.json", timeout=5) as response:
                    self.assertEqual(len(json.load(response)["items"]), 20)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
