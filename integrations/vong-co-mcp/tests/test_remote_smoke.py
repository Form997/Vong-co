"""Opt-in live GitHub read smoke tests.

Run with RUN_REMOTE_SMOKE=1; normal offline unit tests never need network.
"""
import os
import unittest

from catalog import Catalog

ENABLED = os.environ.get("RUN_REMOTE_SMOKE") == "1"


@unittest.skipUnless(ENABLED, "Set RUN_REMOTE_SMOKE=1 to exercise public GitHub data")
class RemoteSmokeTests(unittest.TestCase):
    def test_v1_frozen_readme_is_public(self):
        result = Catalog().get_ban_to(1, "v1")
        self.assertIn("LƯU THỦY TRƯỜNG", result["content"].upper())
        self.assertIn("v1-frozen", result["source_url"])

    def test_v2_review_is_pending_not_passed(self):
        result = Catalog().get_nghiem_thu(1)
        self.assertEqual(result["status"], "CHO_NGHIEM_THU")
        self.assertFalse(result["accepted"])
        self.assertIn("CHỜ NGHIỆM THU", result["report"])
