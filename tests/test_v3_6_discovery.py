"""Offline security tests for the V3.6 source-candidate scanner."""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from v3_6_discover import read_config, normalize, doi_clean, load_api, scan, render_issue


class ScannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config()

    def test_config_denies_automatic_publication(self):
        self.assertFalse(self.config["auto_publish"])
        c = copy.deepcopy(self.config)
        c["auto_publish"] = True
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "config.json"
            p.write_text(json.dumps(c), encoding="utf-8")
            with self.assertRaises(ValueError):
                read_config(p)

    def test_duplicate_config_key_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "config.json"
            p.write_text('{"a":1,"a":2}', encoding="utf-8")
            with self.assertRaises(ValueError):
                read_config(p)

    def test_safe_source_links_and_pending_status(self):
        self.assertEqual(doi_clean("https://doi.org/10.1234/ABC"), "10.1234/abc")
        self.assertIsNone(doi_clean("https://malicious.example/10.1234/test"))
        item = normalize({"title":["Đờn ca tài tử Nam Bộ"], "DOI":"10.1234/TEST",
                          "published":{"date-parts":[[2021]]}},
                         "crossref",self.config["title_match_phrases"])
        self.assertEqual(item["url"],"https://doi.org/10.1234/test")
        self.assertFalse(item["approved_for_publication"])
        self.assertEqual(item["review_status"], "pending_review")

    def test_unrelated_and_html_are_not_promoted(self):
        self.assertIsNone(normalize({"title":["Rice crop growth"],"DOI":"10.1234/g"},
                                    "crossref",self.config["title_match_phrases"]))
        item = normalize({"title":["Vọng cổ <script>alert(1)</script>"],
                          "DOI":"10.1234/h"}, "crossref",self.config["title_match_phrases"])
        self.assertIsNotNone(item)
        self.assertNotIn("<script>",item["title"])

    def test_offline_discovery_deduplicates_and_skips_openalex_without_key(self):
        def fake(url,auth=None):
            self.assertIn("api.crossref.org",url)
            self.assertIsNone(auth)
            return {"message":{"items":[
                {"DOI":"10.1234/D","title":["Đờn ca tài tử Việt Nam"]},
                {"DOI":"10.1234/d","title":["Đờn ca tài tử Việt Nam"]},
                {"DOI":"10.1234/r","title":["Soybean yields"]},
            ]}}
        result = scan(self.config,requester=fake,at=datetime(2026,10,31,tzinfo=timezone.utc))
        self.assertEqual(result["status"],"complete")
        self.assertEqual(result["candidate_count"],1)
        self.assertEqual(result["requests_ok"]["openalex"],0)
        self.assertTrue(result["requests_ok"]["openalex_skipped"])
        self.assertFalse(result["auto_publish"])
        self.assertIn("0/20", render_issue(result))

    def test_optional_openalex_key_not_exposed_and_doi_deduplicated(self):
        calls = []
        def fake(url,auth=None):
            calls.append((url,auth))
            if "crossref" in url:
                return {"message":{"items":[{"title":["Vọng cổ Nam Bộ"],"DOI":"10.1234/dup"}]}}
            return {"results":[
                {"display_name":"Vọng cổ Nam Bộ","doi":"https://doi.org/10.1234/DUP"},
                {"display_name":"Vietnamese chamber music","id":"https://openalex.org/W12345"},
            ]}
        result=scan(self.config,requester=fake,openalex_key="SAMPLE_SECRET")
        self.assertEqual(result["candidate_count"],2)
        self.assertTrue(any(auth=="SAMPLE_SECRET" for _,auth in calls))
        self.assertNotIn("SAMPLE_SECRET",json.dumps(result))

    def test_network_failure_is_never_success(self):
        def broken(url,auth=None):
            raise RuntimeError("fail")
        result=scan(self.config,requester=broken)
        self.assertEqual(result["status"],"failed")
        self.assertFalse(result["auto_publish"])

    def test_no_ssrf_or_plaintext_http(self):
        for bad in ("http://api.crossref.org/works", "https://127.0.0.1/works",
                    "https://evil.example/works"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                load_api(bad)


if __name__ == "__main__":
    unittest.main()
