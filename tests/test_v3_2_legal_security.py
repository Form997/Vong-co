"""V3.2 legal/security checks prove consistency, not regulatory certification."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from v3_2_legal_validate import (
    REQUIRED_IDS, validate_all, validate_policy_files,
    validate_source_registry, validate_website_legal
)
from v3_build_site import build

class LegalSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads(
            (ROOT / "data/v3_2/legal_sources.json").read_text(encoding="utf-8")
        )

    def test_registry_contains_reputable_21_references(self):
        self.assertEqual(validate_source_registry(self.sources), [])
        self.assertEqual(len(self.sources["sources"]), 21)
        self.assertEqual(len({x["id"] for x in self.sources["sources"]}), 21)

    def test_specific_vietnam_laws_have_correct_effective_date(self):
        known = {s["id"]:s for s in self.sources["sources"]}
        for sid, date in REQUIRED_IDS.items():
            with self.subTest(source=sid):
                self.assertEqual(known[sid]["effective_on"], date)

    def test_ai_act_2026_amendment_cannot_be_omitted(self):
        source = copy.deepcopy(self.sources)
        source["sources"] = [x for x in source["sources"] if x["id"] != "EU-AI-OMNIBUS-2026"]
        self.assertTrue(validate_source_registry(source))

    def test_reject_fake_official_domains(self):
        for url in ["http://vanban.chinhphu.vn/doc", "https://law-official.example/bill",
                    "https://github.com/Form997/Vong-co", "https://vanban.chinhphu.vn.evil.tld/"]:
            with self.subTest(url=url):
                source=copy.deepcopy(self.sources)
                source["sources"][0]["official_url"]=url
                self.assertTrue(validate_source_registry(source))

    def test_reject_wrong_effective_date_or_nonexistent_date(self):
        for date in ["2030-01-01", "2026-02-30", "2025-07-01", "tomorrow"]:
            with self.subTest(date=date):
                source=copy.deepcopy(self.sources)
                source["sources"][0]["effective_on"]=date
                self.assertTrue(validate_source_registry(source))

    def test_reject_new_source_without_legal_review(self):
        source=copy.deepcopy(self.sources)
        rogue=copy.deepcopy(source["sources"][0])
        rogue["id"]="UNREVIEWED-NEWS"
        source["sources"].append(rogue)
        self.assertTrue(validate_source_registry(source))

    def test_reject_duplicate_source_identifier(self):
        source=copy.deepcopy(self.sources)
        source["sources"][-1]["id"]=source["sources"][0]["id"]
        self.assertTrue(validate_source_registry(source))

    def test_policy_files_exist_and_have_audit_disclaimers(self):
        self.assertEqual(validate_policy_files(), [])
        self.assertEqual(validate_website_legal(), [])
        self.assertEqual(validate_all(), [])

    def test_reject_missing_privacy_notice(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            # Copy all except privacy to prove validator fails closed.
            import shutil
            for name in ("SECURITY.md", "RIGHTS_AND_LICENSING.md"):
                shutil.copy2(ROOT/name,root/name)
            (root/"docs").mkdir()
            for name in ("phap-ly-an-ninh-mang-v3.2.md", "quy-trinh-thuong-mai-hoa.md", "quy-trinh-ung-pho-su-co.md"):
                shutil.copy2(ROOT/"docs"/name,root/"docs"/name)
            self.assertTrue(validate_policy_files(root))

    def test_reject_policy_change_that_hides_host_ip_logging(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            import shutil
            for relative in ("PRIVACY.md", "SECURITY.md", "RIGHTS_AND_LICENSING.md"):
                shutil.copy2(ROOT/relative,root/relative)
            (root/"docs").mkdir()
            for name in ("phap-ly-an-ninh-mang-v3.2.md", "quy-trinh-thuong-mai-hoa.md", "quy-trinh-ung-pho-su-co.md"):
                shutil.copy2(ROOT/"docs"/name,root/"docs"/name)
            privacy=root/"PRIVACY.md"
            privacy.write_text(privacy.read_text(encoding="utf-8").replace("GitHub Pages","HOST").replace("IP","network-identifier"),encoding="utf-8")
            self.assertTrue(validate_policy_files(root))

    def test_reject_commercial_gate_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            import shutil
            for relative in ("PRIVACY.md", "SECURITY.md", "RIGHTS_AND_LICENSING.md"):
                shutil.copy2(ROOT/relative,root/relative)
            (root/"docs").mkdir()
            for name in ("phap-ly-an-ninh-mang-v3.2.md", "quy-trinh-thuong-mai-hoa.md", "quy-trinh-ung-pho-su-co.md"):
                shutil.copy2(ROOT/"docs"/name,root/"docs"/name)
            c=root/"docs"/"quy-trinh-thuong-mai-hoa.md"
            c.write_text(c.read_text(encoding="utf-8").replace("G12","REMOVED"),encoding="utf-8")
            self.assertTrue(validate_policy_files(root))

    def test_reject_unaudited_external_scripts_or_forms(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            folder=root/"web"/"v3"
            folder.mkdir(parents=True)
            import shutil
            shutil.copy2(ROOT/"web/v3/index.html",folder/"index.html")
            shutil.copy2(ROOT/"web/v3/legal.html",folder/"legal.html")
            p=folder/"legal.html"
            p.write_text(p.read_text(encoding="utf-8").replace(
                "</body>", '<script src="https://track.example/track.js"></script></body>'
            ),encoding="utf-8")
            self.assertTrue(validate_website_legal(root))

    def test_legal_page_is_in_fixed_website_allowlist(self):
        from v3_build_site import ALLOWLIST
        self.assertIn(("web/v3/legal.html","web/v3/legal.html"), ALLOWLIST)
        with tempfile.TemporaryDirectory() as tmp:
            result=build(Path(tmp)/"site")
            self.assertEqual(result["status"], "pass")
            self.assertEqual(result["file_count"],36)
            self.assertIn("web/v3/legal.html",result["published_files"])
            self.assertFalse(result["includes_rights_restricted_media"])

if __name__ == "__main__":
    unittest.main()
