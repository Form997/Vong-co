"""Regression checks for the source index, not performance certification."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from v3_validate import CATALOG, strict_load
from v3_4_validate import INDEX as OLD_INDEX
from v3_5_validate import INDEX, validate_v35
from v3_build_site import build

class V35Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = strict_load(INDEX)
        cls.old = strict_load(OLD_INDEX)
        cls.catalog = strict_load(CATALOG)

    def test_source_rows_and_history(self):
        self.assertEqual(validate_v35(self.data,self.catalog), [])
        self.assertEqual([self.data["items"][i] for i in (0,1,2,3,4,6)], self.old["items"])
        item = self.data["items"][5]
        self.assertEqual((item["piece_id"],item["variant_id"],len(item["phrases"])), (5,"XTC-48-4",48))
        self.assertIn("khác biệt",item["phrases"][36]["source_note"])
        self.assertEqual((item["phrases"][40]["printed_music_page"],item["phrases"][40]["printed_lyric_page"]), (146,147))

    def test_reject_false_page_variant_rights_and_history(self):
        for mutate in (
            lambda d: d["items"][5]["phrases"][40].__setitem__("printed_music_page",999),
            lambda d: d["items"][5].__setitem__("variant_id","THU-48"),
            lambda d: d.__setitem__("rights_status","verified"),
            lambda d: d.__setitem__("performance_status","approved"),
            lambda d: d["items"][0]["phrases"][0].__setitem__("number",999),
        ):
            data=copy.deepcopy(self.data)
            mutate(data)
            self.assertTrue(validate_v35(data,self.catalog))

    def test_build_has_48_labels_without_media(self):
        with tempfile.TemporaryDirectory() as temp:
            dst=Path(temp)/"site"
            result=build(dst)
            self.assertEqual((result["indexed_lesson_pieces"],result["indexed_lesson_systems"],result["indexed_lesson_phrases"]),(6,7,300))
            html=(dst/"bai/05-xuan-tinh-chan/index.html").read_text(encoding="utf-8")
            self.assertEqual(html.count('class="phrase-row"'),48)
            self.assertIn("khác biệt",html)
            self.assertNotIn("<audio",html)
            self.assertNotIn("#page=",html)

if __name__ == "__main__":
    unittest.main()
