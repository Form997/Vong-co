"""Tests for V3 Pages public artifact: strict allowlist and correct HTTP routing."""
import functools
import http.server
import json
import pathlib
import sys
import tempfile
import threading
import unittest
from urllib.request import urlopen

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from v3_build_site import build


class V3PagesBuildTests(unittest.TestCase):
    def test_build_copies_only_safe_public_files(self):
        with tempfile.TemporaryDirectory() as temp:
            target = pathlib.Path(temp) / "site"
            result = build(target)
            self.assertEqual(result["status"], "pass")
            self.assertEqual(result["pieces"], 20)
            self.assertEqual(result["variants"], 30)
            self.assertEqual(result["file_count"], 7)
            self.assertNotIn("ban-to/", "|".join(result["published_files"]))
            self.assertNotIn("docs/", "|".join(result["published_files"]))
            self.assertNotIn(".github/", "|".join(result["published_files"]))
            self.assertIn(".nojekyll", result["published_files"])
            self.assertIn("web/v3/index.html", result["published_files"])

    def test_nonempty_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = pathlib.Path(temp) / "site"
            target.mkdir()
            (target / "old.html").write_text("old", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "rỗng"):
                build(target)

    def test_site_is_served_at_project_root_with_json(self):
        with tempfile.TemporaryDirectory() as temp:
            target = pathlib.Path(temp) / "site"
            build(target)
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(target))
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
            server.daemon_threads = True
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                root = f"http://127.0.0.1:{server.server_address[1]}"
                for path in ("/", "/web/v3/", "/data/v3/catalog.json", "/data/v3/schema.json"):
                    with self.subTest(path=path):
                        with urlopen(root + path, timeout=5) as response:
                            self.assertEqual(response.status, 200)
                with urlopen(root + "/data/v3/catalog.json", timeout=5) as response:
                    self.assertEqual(len(json.load(response)["items"]), 20)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
