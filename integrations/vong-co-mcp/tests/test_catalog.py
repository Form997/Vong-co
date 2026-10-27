"""Offline tests: no GitHub access, no MCP server dependency."""
import unittest

from catalog import (
    BRANCHES,
    Catalog,
    SourceNotFound,
    WORKS,
    _fold,
    _valid_path,
)


def fake_fetch(branch, path):
    if (branch, path) == (
        "v1-frozen", "ban-to/01-luu-thuy-truong/README.md"
    ):
        return (
            "# Lưu Thủy Trường\n"
            "Bản Vắn và bản Trường là dị bản khác nhau.\n"
            "[Viện Âm nhạc](https://vienamnhac.vn/nguon.pdf)\n"
        )
    if (branch, path) == (
        "v2-development",
        "ban-to/01-luu-thuy-truong/v2-bien-ban-nghiem-thu.md",
    ):
        return "# Biên bản V2\n**PHÁN QUYẾT: CHỜ NGHIỆM THU**\n"
    if (branch, path) == ("v2-development", "docs/ke-hoach-v2.md"):
        return "# Quy chế V2: kiểm chứng từng câu"
    raise SourceNotFound(path)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.store = Catalog(fetch_text=fake_fetch)

    def test_twenty_groups_and_unique_folders(self):
        self.assertEqual(len(WORKS), 20)
        self.assertEqual(len({w.folder for w in WORKS}), 20)
        groups = [w.group for w in WORKS]
        self.assertEqual(groups.count("Sáu Bắc"), 6)
        self.assertEqual(groups.count("Bảy Lễ"), 7)
        self.assertEqual(groups.count("Ba Nam"), 3)
        self.assertEqual(groups.count("Bốn Oán"), 4)

    def test_accent_insensitive_search(self):
        found = self.store.search_ban_to("luu thuy")
        self.assertEqual(found["match_count"], 1)
        self.assertEqual(found["works"][0]["number"], 1)
        self.assertEqual(_fold("ĐỜN"), "don")

    def test_read_v1_and_citation(self):
        result = self.store.get_ban_to(1)
        self.assertIn("Vắn", result["content"])
        self.assertIn("v1-frozen", result["source_url"])
        self.assertEqual(result["source_branch"], BRANCHES["v1"])

    def test_missing_v2_report_is_not_a_pass(self):
        missing = self.store.get_nghiem_thu(2)
        self.assertFalse(missing["accepted"])
        self.assertEqual(missing["status"], "CHUA_CO_BIEN_BAN_V2")

    def test_pending_v2_report_is_not_a_pass(self):
        result = self.store.get_nghiem_thu(1)
        self.assertEqual(result["status"], "CHO_NGHIEM_THU")
        self.assertFalse(result["accepted"])

    def test_sources_and_variants(self):
        links = self.store.get_nguon(1)["links"]
        self.assertEqual(links[0]["url"], "https://vienamnhac.vn/nguon.pdf")
        snippets = self.store.get_di_ban(1)["excerpts"]
        self.assertTrue(any("dị bản" in x for x in snippets))

    def test_only_allowlisted_paths(self):
        self.assertTrue(_valid_path("ban-to/01-luu-thuy-truong/README.md"))
        self.assertFalse(_valid_path("../README.md"))
        self.assertFalse(_valid_path("https://example.com/file.md"))
        self.assertFalse(_valid_path("docs/../../secrets.md"))

    def test_reject_bad_inputs(self):
        with self.assertRaises(ValueError):
            self.store.get_ban_to(21)
        with self.assertRaises(ValueError):
            self.store.get_ban_to(1, version="master")
        with self.assertRaises(ValueError):
            self.store.search_ban_to("  ")

    def test_v2_rules_read(self):
        self.assertIn("kiểm chứng từng câu", self.store.get_quy_che_v2()["content"])


if __name__ == "__main__":
    unittest.main()
