"""V3.3: 150 machine-readable source-label locators, NOT 150 approved music phrases."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from v3_validate import CATALOG, strict_load
from v3_2_validate import INDEX as V32_INDEX, validate_phrase_index
from v3_3_validate import INDEX, SCHEMA, validate_v33, candidate_phrase, parse_rows, validate_schema
from v3_build_site import build, page_for_piece

class V33SourceIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v33=strict_load(INDEX)
        cls.prev=strict_load(V32_INDEX)
        cls.cat=strict_load(CATALOG)
        cls.pieces={x["piece_id"]:x for x in cls.v33["items"]}

    def rejected(self, data, why):
        self.assertTrue(validate_v33(data,self.cat),f"Unsafe data accepted: {why}")

    def test_150_labels_4_systems_and_zero_performance_approvals(self):
        self.assertEqual(validate_v33(self.v33,self.cat),[])
        self.assertEqual([x["piece_id"] for x in self.v33["items"]],[1,2,3,20])
        self.assertEqual([len(x["phrases"]) for x in self.v33["items"]],[32,34,44,40])
        self.assertEqual(sum(len(x["phrases"]) for x in self.v33["items"]),150)
        self.assertEqual(self.v33["performance_status"],"pending")
        self.assertEqual(self.v33["rights_status"],"unverified")

    def test_old_72_source_labels_unchanged_and_v32_still_valid(self):
        self.assertEqual(validate_phrase_index(self.prev,self.cat),[])
        self.assertEqual(self.pieces[1],self.prev["items"][0])
        self.assertEqual(self.pieces[20],self.prev["items"][1])

    def test_phu_luc_34_music_but_only_32_printed_lyric_labels(self):
        plc=self.pieces[2]
        self.assertEqual(len(plc["phrases"]),34)
        self.assertEqual([x["number"] for x in plc["phrases"] if x["printed_lyric_page"] is None],[33,34])
        self.assertTrue(all("Văn Dần" in x["source_lyric_locator"] for x in plc["phrases"][32:]))
        self.assertEqual([x["number"] for x in plc["phrases"] if "DỊ BẢN" in (x["source_note"] or "")],[8,34])
        self.assertEqual(plc["phrases"][33]["printed_music_page"],130)
        self.assertEqual(plc["phrases"][33]["ending_token"],"(nghỉ)")

    def test_binh_ban_has_44_printed_source_labels_in_four_layers(self):
        b=self.pieces[3]
        self.assertEqual(len(b["phrases"]),44)
        self.assertEqual([(x["label"],x["start"],x["end"]) for x in b["sections"]],
                         [("I",1,10),("II",11,22),("III",23,32),("IV",33,44)])
        self.assertEqual((b["phrases"][0]["printed_music_page"],b["phrases"][0]["printed_lyric_page"]),(130,131))
        self.assertEqual((b["phrases"][-1]["printed_music_page"],b["phrases"][-1]["printed_lyric_page"]),(134,135))

    def test_reject_fabricated_lyric_page_34(self):
        d=copy.deepcopy(self.v33)
        d["items"][1]["phrases"][33]["printed_lyric_page"]=131
        self.rejected(d,"missing lyric 34 fabricated")

    def test_reject_wrong_variant_endings_08_and_34(self):
        for n in [8,34]:
            d=copy.deepcopy(self.v33)
            d["items"][1]["phrases"][n-1]["source_note"]="Chưa rà"
            self.rejected(d,f"source conflict {n} silently removed")

    def test_reject_wrong_edition_or_undocumented_page_number(self):
        d=copy.deepcopy(self.v33)
        d["items"][1]["source_url"]="https://www.namkyluctinh.org/other.pdf"
        self.rejected(d,"switching Nhi Tan edition")
        d=copy.deepcopy(self.v33)
        d["items"][2]["phrases"][-1]["printed_music_page"]=137
        self.rejected(d,"fabricated printed page")

    def test_reject_swapped_bbc_and_plc_or_mixed_beat_systems(self):
        d=copy.deepcopy(self.v33)
        d["items"][2]["beats_per_phrase"]=8
        self.rejected(d,"BBC 44/4 falsely assigned 22/8")
        d=copy.deepcopy(self.v33)
        d["items"][1]["sections"]=self.v33["items"][2]["sections"]
        self.rejected(d,"PLC V2 layer boundaries overwritten")

    def test_reject_altered_v32_baseline(self):
        d=copy.deepcopy(self.v33)
        d["items"][0]["phrases"][2]["ending_token"]="HO"  # preserve HÒ vs HO
        self.rejected(d,"V3.2 historic source altered")
        d=copy.deepcopy(self.v33)
        d["items"][3]["phrases"][-1]["printed_music_page"]=342
        self.rejected(d,"Phung Cau source overwritten")

    def test_reject_false_commercial_rights_or_expert_certification(self):
        for key,value in [("rights_status","verified"),("performance_status","approved"),("research_scope","full_score")]:
            d=copy.deepcopy(self.v33)
            d[key]=value
            self.rejected(d,key)

    def test_reject_fifth_unreviewed_piece_and_missing_piece(self):
        d=copy.deepcopy(self.v33)
        d["items"].append(copy.deepcopy(d["items"][0]))
        self.rejected(d,"fifth duplicate/non-reviewed piece")
        d=copy.deepcopy(self.v33)
        d["items"].pop(1)
        self.rejected(d,"missing PLC")

    def test_schema_explicitly_disallows_unknowns(self):
        schema=strict_load(SCHEMA)
        self.assertEqual(validate_schema(schema),[])
        schema["properties"]["rights_status"]["const"]="approved"
        self.assertTrue(validate_schema(schema))
        schema=strict_load(SCHEMA)
        schema["$defs"]["phrase"]["additionalProperties"]=True
        self.assertTrue(validate_schema(schema))

    def test_renderer_does_not_fake_pdf_page_offset_for_volume_ii(self):
        catalog={x["id"]:x for x in self.cat["items"]}
        html=page_for_piece(catalog[2],catalog[1],catalog[3],self.pieces[2])
        self.assertEqual(html.count('class="phrase-row"'),34)
        self.assertIn("KHÔNG CÓ trong trang lời",html)
        self.assertIn("DỊ BẢN",html)
        self.assertIn("Xáng Tồn",html)
        self.assertNotIn("#page=-",html)
        self.assertNotIn("#page=0",html)
        self.assertNotIn("#page=40",html) # volume-II mapping MUST NOT assume volume-IV offset
        self.assertNotIn("<audio",html)
        self.assertIn("0/20",html)

    def test_renderer_escapes_untrusted_note(self):
        data=copy.deepcopy(self.pieces[3])
        data["phrases"][0]["source_note"]='<img src=x onerror=alert(1)>'
        cat={x["id"]:x for x in self.cat["items"]}
        html=page_for_piece(cat[3],cat[2],cat[4],data)
        self.assertNotIn('<img src=x onerror=',html)
        self.assertIn("&lt;img",html)

    def test_site_build_preserves_v33_and_includes_v34(self):
        with tempfile.TemporaryDirectory() as temp:
            dst=Path(temp)/"site"
            result=build(dst)
            self.assertEqual(result["status"],"pass")
            self.assertEqual(result["file_count"], 48)
            self.assertEqual(result["indexed_lesson_pieces"],6)
            self.assertEqual(result["indexed_lesson_phrases"],300)
            self.assertFalse(result["includes_rights_restricted_media"])
            published=set(result["published_files"])
            self.assertIn("data/v3_4/phrase_index.json",published)
            self.assertIn("data/v3_3/phrase_index.json",published)
            self.assertIn("data/v3_2/phrase_index.json",published)  # historical previous version
            for n,count in [(1,32),(2,34),(3,44),(20,40)]:
                cat=self.cat["items"][n-1]
                html=(dst/"bai"/cat["slug"]/"index.html").read_text(encoding="utf-8")
                self.assertEqual(html.count('class="phrase-row"'),count)
                self.assertIn("V3.6",html)
            html=(dst/"bai"/self.cat["items"][17]["slug"]/"index.html").read_text(encoding="utf-8")
            self.assertNotIn('class="phrase-row"',html)
            self.assertIn("chưa chuẩn hóa",html)
            self.assertFalse(any(x.endswith((".mp3",".wav",".mid",".pdf",".docx",".env")) for x in published))

if __name__=="__main__":
    unittest.main()
