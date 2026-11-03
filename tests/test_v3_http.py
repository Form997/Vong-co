"""Actual HTTP smoke test for V3 static web files — no external network."""

from __future__ import annotations

import functools
import http.server
import json
import pathlib
import threading
import unittest
from urllib.request import urlopen

ROOT = pathlib.Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, _format, *_args):
        pass


class V3HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(QuietHandler, directory=str(ROOT))
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.server.daemon_threads = True
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def test_v3_html_is_served_over_http(self):
        with urlopen(self.base_url + "/web/v3/", timeout=5) as response:
            html = response.read().decode("utf-8")
            self.assertEqual(response.status, 200)
            self.assertIn("text/html", response.headers.get("Content-Type", ""))
            self.assertIn("HAI ĐẤT V3", html)

    def test_json_path_from_html_resolves(self):
        # Relative "../../data/v3/catalog.json" from /web/v3/index.html.
        with urlopen(self.base_url + "/data/v3/catalog.json", timeout=5) as response:
            data = json.load(response)
            self.assertEqual(response.status, 200)
            self.assertIn("application/json", response.headers.get("Content-Type", ""))
        self.assertEqual(len(data["items"]), 20)
        self.assertEqual(sum(len(x["variants"]) for x in data["items"]), 30)

    def test_schema_is_served_as_valid_json(self):
        with urlopen(self.base_url + "/data/v3/schema.json", timeout=5) as response:
            schema = json.load(response)
        self.assertEqual(schema["properties"]["schema_version"]["const"], "3.0.0-alpha.1")


if __name__ == "__main__":
    unittest.main()
