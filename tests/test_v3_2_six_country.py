"""Country-law research metadata and public HTML: adversarial checks, not legal certification."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from v3_2_six_country_validate import COUNTRIES, REGISTRY, validate_country_registry, validate_country_docs, validate_country_public_hub, validate_all
from v3_2_country_html import render_country_page
from v3_build_site import build


class SixJurisdictionLawTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def invalid(self, mutated, reason):
        self.assertTrue(validate_country_registry(mutated), f"Incorrectly accepted {reason}")

    def test_28_official_or_agency_records_cover_six_countries(self):
        self.assertEqual(validate_country_registry(self.data), [])
        self.assertEqual(set(COUNTRIES), set(self.data["jurisdictions"]))
        self.assertEqual(len(self.data["sources"]), 28)
        self.assertFalse(self.data["commercial_enabled"])

    def test_all_country_docs_link_every_source(self):
        self.assertEqual(validate_country_docs(self.data), [])
        self.assertEqual(validate_country_public_hub(), [])
        self.assertEqual(validate_all(), [])

    def test_korean_2026_copyright_exact_29_october(self):
        s = {x["id"]:x for x in self.data["sources"]}
        self.assertEqual(s["KR-COPYRIGHT-2026"]["effective_on"], "2026-10-29")
        self.assertEqual(s["KR-NETWORK-2026"]["effective_on"], "2026-10-02")
        self.assertEqual(s["KR-PIPA-2026"]["effective_on"], "2026-09-11")
        self.assertEqual(s["CN-CSL-2026"]["effective_on"], "2026-01-01")

    def test_japan_pending_2026_amendment_not_labeled_in_force(self):
        x = {q["id"]:q for q in self.data["sources"]}
        self.assertEqual(x["JP-COPYRIGHT-AMEND-2026"]["status"], "promulgated-pending")
        self.assertIsNone(x["JP-COPYRIGHT-AMEND-2026"]["effective_on"])
        s = copy.deepcopy(self.data)
        next(q for q in s["sources"] if q["id"]=="JP-COPYRIGHT-AMEND-2026")["status"] = "in_force"
        self.invalid(s, "promulgated-but-not-commenced Japanese reform")

    def test_reject_unknown_official_domain_http_and_lookalike(self):
        for url in ["http://www.law.go.kr/", "https://law.go.kr.evil.example/a",
                    "https://notlaw.example.com", "https://github.com/Form997/Vong-co"]:
            with self.subTest(url=url):
                d=copy.deepcopy(self.data)
                d["sources"][0]["official_url"]=url
                self.invalid(d, "untrusted source URL")

    def test_reject_future_or_fake_effective_date(self):
        for when in ["2027-01-01", "2026-02-30", "2026-11-01", "2026-09-31"]:
            with self.subTest(effective=when):
                d=copy.deepcopy(self.data)
                d["sources"][0]["effective_on"]=when
                self.invalid(d, "future/non-calendar date")

    def test_reject_duplicated_or_deleted_country(self):
        d=copy.deepcopy(self.data)
        d["sources"].extend([copy.deepcopy(d["sources"][0])])
        self.invalid(d, "duplicate law")
        d=copy.deepcopy(self.data)
        d["jurisdictions"].remove("RU")
        self.invalid(d, "missing Russian jurisdiction")

    def test_reject_falsely_enabled_commerce(self):
        d=copy.deepcopy(self.data)
        d["commercial_enabled"]=True
        self.invalid(d, "commercial mode without approval")

    def test_reject_mutated_mandatory_fresh_law_date(self):
        d=copy.deepcopy(self.data)
        next(x for x in d["sources"] if x["id"]=="KR-COPYRIGHT-2026")["effective_on"]="2026-08-11"
        self.invalid(d, "obsolete Korean copyright edition")

    def test_rendered_pages_escape_html_in_source_note(self):
        d=copy.deepcopy(self.data)
        x=next(x for x in d["sources"] if x["jurisdiction"]=="US")
        x["scope_note"]='foo<img src=x onerror=alert(1)>bar'
        page=render_country_page("US",d)
        self.assertNotIn("<img",page)
        self.assertIn("&lt;img",page)
        self.assertNotIn("<script",page)

    def test_renderer_rejects_nonapproved_country(self):
        with self.assertRaises(ValueError):
            render_country_page("FAKE",self.data)

    def test_all_6_public_html_pages_and_20_songs_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            site=Path(tmp)/"www"
            result=build(site)
            self.assertEqual(result["file_count"],42)
            self.assertEqual(result["country_law_pages"],6)
            self.assertEqual(result["country_law_source_records"],28)
            for code, obj in COUNTRIES.items():
                f=site/"web"/"v3"/"quoc-gia"/obj["file"].replace(".md",".html")
                self.assertTrue(f.exists(),code)
                text=f.read_text(encoding="utf-8")
                self.assertIn("NO-GO",text)
                self.assertIn("29/10/2026",text)
                self.assertNotIn("<iframe",text)
            self.assertFalse(any(x.endswith((".pdf",".mp3",".wav",".mid",".env")) for x in result["published_files"]))
            self.assertEqual(result["indexed_lesson_phrases"],300)

if __name__=="__main__":
    unittest.main()
