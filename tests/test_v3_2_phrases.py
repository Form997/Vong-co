"""V3.2: provenance safety, 72 indexed phrase locators, and honest lesson pages."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from v3_validate import CATALOG, strict_load
from v3_2_validate import INDEX, CONFIGS, validate_phrase_index, expectation, source_rows
from v3_2_lesson_html import render_lesson
from v3_build_site import build

class PhraseLessonsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = strict_load(CATALOG)
        cls.data = strict_load(INDEX)
        cls.items = {x["piece_id"]: x for x in cls.data["items"]}
        cls.pieces = {x["id"]: x for x in cls.catalog["items"]}

    def reject(self, data, label):
        errors = validate_phrase_index(data, self.catalog)
        self.assertTrue(errors, f"Changed {label} wrongly passed validation")

    def test_v3_2_index_has_72_source_specific_rows(self):
        self.assertEqual(validate_phrase_index(self.data, self.catalog), [])
        self.assertEqual([x["piece_id"] for x in self.data["items"]], [1, 20])
        self.assertEqual([len(x["phrases"]) for x in self.data["items"]], [32, 40])
        self.assertEqual(self.data["performance_status"], "pending")
        self.assertEqual(self.data["rights_status"], "unverified")
        self.assertEqual(self.data["research_scope"], "source_label_index_only")

    def test_01_preserves_original_glyph_and_classes(self):
        lt = self.items[1]
        self.assertEqual(lt["variant_id"], "LT-32-4")
        self.assertEqual(lt["phrases"][0]["ending_token"], "HO")
        self.assertEqual(lt["phrases"][2]["ending_token"], "HÒ")
        self.assertEqual(lt["phrases"][31]["ending_token"], "LIU")
        self.assertEqual([p["section"] for p in lt["phrases"]],
                         ["I"]*8+["II"]*8+["III"]*8+["IV"]*8)
        self.assertIsNone(lt["phrases"][0]["printed_music_page"])

    def test_20_exact_page_and_layer_boundaries(self):
        pc = self.items[20]
        self.assertEqual(pc["variant_id"], "PC-40-8")
        self.assertEqual([p["section"] for p in pc["phrases"]],
                         ["I"]*18+["II"]*8+["III"]*14)
        for i, pages in [(1, (332,333)), (9, (332,333)), (10,(334,335)),
                         (19,(334,335)), (20,(336,337)), (27,(336,337)),
                         (30,(338,339)), (39,(338,339)), (40,(340,341))]:
            p = pc["phrases"][i-1]
            self.assertEqual((p["printed_music_page"],p["printed_lyric_page"]), pages)
        self.assertEqual(pc["phrases"][39]["pair_index"], 20)
        self.assertIsNone(pc["phrases"][39]["ending_token"])

    def test_all_source_ledger_rows_revalidated_without_inference(self):
        for piece_id, item in self.items.items():
            expected_count = CONFIGS[piece_id][1]
            rows = source_rows(ROOT / item["source_register"], expected_count)
            for n, row in enumerate(rows, 1):
                with self.subTest(piece=piece_id, phrase=n):
                    self.assertEqual(item["phrases"][n-1], expectation(piece_id,row,n))

    def test_reject_fabricated_melody_or_audio_link(self):
        data = copy.deepcopy(self.data)
        data["items"][0]["phrases"][0]["audio_url"] = "https://example.org/fake.mp3"
        self.reject(data, "invented audio")
        del data["items"][0]["phrases"][0]["audio_url"]
        data["items"][0]["phrases"][0]["melody"] = ["C", "D", "E"]
        self.reject(data, "invented notes")

    def test_reject_unverified_permission_promotion(self):
        data = copy.deepcopy(self.data)
        data["rights_status"] = "licensed"
        self.reject(data, "unverified rights")
        data = copy.deepcopy(self.data)
        data["performance_status"] = "approved"
        self.reject(data, "unverified performance")

    def test_reject_wrong_system_32_4_as_16_8(self):
        data = copy.deepcopy(self.data)
        data["items"][0]["variant_id"] = "LT-16-8"
        data["items"][0]["beats_per_phrase"] = 8
        self.reject(data, "merged incompatible systems")

    def test_reject_wrong_source_locator_and_note(self):
        data = copy.deepcopy(self.data)
        data["items"][0]["phrases"][0]["source_music_locator"] = "Tự tưởng tượng câu 01"
        self.reject(data, "new locator")
        data = copy.deepcopy(self.data)
        data["items"][1]["phrases"][39]["source_note"] = "Mọi câu chẵn đều kết phách 7"
        self.reject(data, "unverified song lang")

    def test_reject_wrong_printed_page_and_pair(self):
        data = copy.deepcopy(self.data)
        data["items"][1]["phrases"][39]["printed_music_page"] = 342
        self.reject(data, "wrong original page")
        data = copy.deepcopy(self.data)
        data["items"][1]["phrases"][20]["pair_index"] = 15
        self.reject(data, "wrong pair")

    def test_reject_missing_or_duplicate_rows(self):
        data = copy.deepcopy(self.data)
        del data["items"][0]["phrases"][4]
        self.reject(data, "missing row")
        data = copy.deepcopy(self.data)
        data["items"][0]["phrases"][7]["number"] = 1
        self.reject(data, "duplicate label")

    def test_reject_extra_piece_or_unknown_field(self):
        data = copy.deepcopy(self.data)
        data["items"].append(copy.deepcopy(data["items"][0]))
        self.reject(data, "fake third indexed piece")
        data = copy.deepcopy(self.data)
        data["items"][0]["lesson_certified"] = True
        self.reject(data, "unverified certification")

    def test_renderer_does_not_fabricate_18_missing_courses(self):
        for item in self.catalog["items"]:
            if item["id"] in (1,20):
                continue
            html = render_lesson(item, None)
            self.assertIn("chưa có bảng chỉ mục", html)
            self.assertNotIn("class=\"phrase-row\"", html)

    def test_lesson_01_and_20_include_only_their_indexed_rows(self):
        a = render_lesson(self.pieces[1], self.items[1])
        b = render_lesson(self.pieces[20], self.items[20])
        self.assertEqual(a.count('class="phrase-row"'), 32)
        self.assertEqual(b.count('class="phrase-row"'), 40)
        self.assertIn("nhịp tư", a.lower())
        self.assertIn("PDF trang nhạc 38", b)
        self.assertIn("PDF trang lời 47", b)
        self.assertIn("0/20", a)
        self.assertIn("0/20", b)
        self.assertNotIn("<audio", a+b)
        self.assertNotIn("<iframe", a+b)

    def test_renderer_escapes_untrusted_source_notes(self):
        tampered = copy.deepcopy(self.items[1])
        tampered["phrases"][0]["source_note"] = '<script>alert("bad")</script>'
        html = render_lesson(self.pieces[20], tampered)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_generated_site_has_72_rows_and_no_fake_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/"site"
            result = build(target)
            self.assertEqual(result["file_count"], 29)
            self.assertEqual(result["indexed_lesson_pieces"], 2)
            self.assertEqual(result["indexed_lesson_phrases"], 72)
            a = (target/"bai/01-luu-thuy-truong/index.html").read_text(encoding="utf-8")
            b = (target/"bai/20-phung-cau/index.html").read_text(encoding="utf-8")
            missing = (target/"bai/18-phung-hoang/index.html").read_text(encoding="utf-8")
            self.assertEqual(a.count('class="phrase-row"'), 32)
            self.assertEqual(b.count('class="phrase-row"'), 40)
            self.assertEqual(missing.count('class="phrase-row"'), 0)
            self.assertIn("đang chờ sổ nguồn", missing)

if __name__ == "__main__":
    unittest.main()
