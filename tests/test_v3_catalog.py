"""Safety and regression tests for V3 metadata, all offline."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("v3_validate", ROOT / "scripts" / "v3_validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class V3CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = validator.strict_load(validator.CATALOG)

    def check_invalid(self, changed: dict, expected_substring: str):
        errors = validator.validate_catalog(changed)
        self.assertTrue(
            any(expected_substring in e for e in errors),
            f"Expected {expected_substring!r} in {errors}",
        )

    def test_20_pieces_and_30_variants(self):
        self.assertEqual(validator.validate_catalog(self.catalog), [])
        result = validator.summary(self.catalog)
        self.assertEqual(result["pieces"], 20)
        self.assertEqual(result["variants"], 30)
        self.assertEqual(result["families"], {
            "Sáu Bắc": 6, "Bảy Lễ": 7, "Ba Nam": 3, "Bốn Oán": 4,
        })

    def test_every_review_file_exists(self):
        for item in self.catalog["items"]:
            with self.subTest(piece=item["id"]):
                self.assertTrue((ROOT / item["review_document"]).is_file())
                self.assertTrue((ROOT / item["readme_document"]).is_file())

    def test_all_performance_status_pending(self):
        self.assertTrue(all(x["performance_status"] == "pending" for x in self.catalog["items"]))
        self.assertEqual(validator.summary(self.catalog)["performance_approved"], 0)

    def test_catalog_rejects_approved_without_review(self):
        data = copy.deepcopy(self.catalog)
        data["items"][0]["performance_status"] = "approved"
        self.check_invalid(data, "nghiệm thu biểu diễn")

    def test_catalog_rejects_unverified_rights_promotion(self):
        data = copy.deepcopy(self.catalog)
        data["items"][1]["rights_status"] = "commercial"
        self.check_invalid(data, "quyền tài liệu")

    def test_wrong_number_rejected(self):
        data = copy.deepcopy(self.catalog)
        data["items"][1]["id"] = 1
        self.check_invalid(data, "số 2")

    def test_wrong_family_rejected(self):
        data = copy.deepcopy(self.catalog)
        data["items"][6]["family"] = "sau-bac"
        self.check_invalid(data, "nhóm sai")

    def test_missing_local_review_rejected(self):
        data = copy.deepcopy(self.catalog)
        data["items"][0]["review_document"] = "../outside.md"
        self.check_invalid(data, "không trỏ đúng")

    def test_variant_number_cannot_be_fake(self):
        data = copy.deepcopy(self.catalog)
        data["items"][0]["variants"][0]["phrase_count"] = 0
        self.check_invalid(data, "1–500")

    def test_duplicate_variant_id_rejected(self):
        data = copy.deepcopy(self.catalog)
        data["items"][1]["variants"][0]["variant_id"] = data["items"][0]["variants"][0]["variant_id"]
        self.check_invalid(data, "trùng")

    def test_variant_cannot_be_marked_verified_performance(self):
        data = copy.deepcopy(self.catalog)
        data["items"][0]["variants"][0]["evidence_status"] = "approved"
        self.check_invalid(data, "mức chứng cứ")

    def test_http_unsecured_reference_rejected(self):
        data = copy.deepcopy(self.catalog)
        data["items"][0]["variants"][0]["reference_url"] = "http://example.test/score"
        self.check_invalid(data, "HTTPS")

    def test_phung_hoang_and_phung_cau_distinct(self):
        self.assertNotEqual(self.catalog["items"][17]["title"], self.catalog["items"][19]["title"])
        data = copy.deepcopy(self.catalog)
        data["items"][17]["title"] = data["items"][19]["title"]
        self.check_invalid(data, "hai bài khác nhau")

    def test_duplicate_json_object_keys_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            filename = Path(tmp) / "duplicate.json"
            filename.write_text('{"id": 1, "id": 2}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "lặp khóa"):
                validator.strict_load(filename)

    def test_invalid_date_rejected(self):
        data = copy.deepcopy(self.catalog)
        data["started_on"] = "2027-01-01"
        self.check_invalid(data, "Ngày khởi động V3")

    def test_null_beats_can_be_used_for_unknown(self):
        data = copy.deepcopy(self.catalog)
        data["items"][0]["variants"][0]["beats_per_phrase"] = None
        self.assertEqual(validator.validate_catalog(data), [])

    def test_empty_variant_list_rejected(self):
        data = copy.deepcopy(self.catalog)
        data["items"][0]["variants"] = []
        self.check_invalid(data, "ít nhất một hệ bản")


if __name__ == "__main__":
    unittest.main()
