"""Publication revision is deterministic and covers every built page."""
from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from v3_build_site import build, stamp_site_revision


class UpdateTags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.revisions = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name") == "hai-dat-revision":
            self.revisions.append(attrs.get("content"))
        if tag == "script" and attrs.get("src", "").endswith("auto-update.js"):
            self.scripts.append(attrs["src"])


class AutomaticUpdateBuildTests(unittest.TestCase):
    def test_deterministic_revision_and_update_script_for_all_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            a, b = Path(temp) / "a", Path(temp) / "b"
            first, second = build(a), build(b)
            revision = first["site_revision"]
            self.assertRegex(revision, r"^[0-9a-f]{64}$")
            self.assertEqual(revision, second["site_revision"])
            self.assertEqual(json.loads((a / "site-version.json").read_text()), {"version": revision})
            self.assertEqual((a / "site-version.json").read_bytes(), (b / "site-version.json").read_bytes())
            for page in a.rglob("*.html"):
                relative = page.relative_to(a).as_posix()
                with self.subTest(page=relative):
                    tags = UpdateTags()
                    tags.feed(page.read_text(encoding="utf-8"))
                    self.assertEqual(tags.revisions, [revision])
                    self.assertEqual(len(tags.scripts), 1)
                    script_url = urljoin("https://example.test/Vong-co/" + relative, tags.scripts[0])
                    self.assertEqual(script_url, "https://example.test/Vong-co/web/v3/auto-update.js")

    def test_revision_changes_with_published_content(self):
        with tempfile.TemporaryDirectory() as temp:
            versions = []
            for index, content in enumerate(("first", "second")):
                target = Path(temp) / str(index)
                target.mkdir()
                (target / "index.html").write_text("<html><head></head><body>" + content + "</body></html>")
                versions.append(stamp_site_revision(target))
            self.assertNotEqual(*versions)


if __name__ == "__main__":
    unittest.main()
