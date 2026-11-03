#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAI ĐẤT V3.2 — fail-closed static legal/security publication gate.

Mechanical consistency checks only: this does NOT establish legal compliance,
rightsholder consent, privacy adequacy, vulnerability-free code, or a legal opinion.
"""
from __future__ import annotations

from datetime import date
from html.parser import HTMLParser
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from v3_validate import ROOT
from v3_2_six_country_validate import validate_all as validate_six_countries

INDEX = ROOT / "data" / "v3_2" / "legal_sources.json"
POLICIES = {
    "PRIVACY.md",
    "SECURITY.md",
    "RIGHTS_AND_LICENSING.md",
    "docs/phap-ly-an-ninh-mang-v3.2.md",
    "docs/quy-trinh-thuong-mai-hoa.md",
    "docs/quy-trinh-ung-pho-su-co.md",
}
FRONTEND = ROOT / "web" / "v3" / "index.html"
LEGAL_PAGE = ROOT / "web" / "v3" / "legal.html"

REQUIRED_IDS = {
    "VN-CYBER-2025": "2026-07-01",
    "VN-PERSONAL-2025": "2026-01-01",
    "VN-PERSONAL-DECREE": "2026-01-01",
    "VN-IP-2025": "2026-04-01",
    "VN-DATA-2024": "2025-07-01",
    "VN-INTERNET-2024": "2024-12-25",
    "VN-ECOM-2025": "2026-07-01",
    "VN-ECOM-DECREE-2026": "2026-07-01",
    "VN-HERITAGE-2024": "2025-07-01",
    "EU-GDPR": "2018-05-25",
    "EU-DSA": "2024-02-17",
    "EU-AI-ACT": None,
    "EU-AI-OMNIBUS-2026": None,
    "UK-DATA": "2018-05-25",
    "US-COPPA": "2025-06-23",
    "US-DMCA-512": "1998-10-28",
    "WIPO-BERNE": None,
    "NIST-CSF": None,
    "CC-LICENSES": None,
    "GITHUB-PAGES-LIMITS": None,
    "GITHUB-PAGES-PRIVACY": None,
}
ALLOWED_DOMAINS = {
    "vanban.chinhphu.vn", "chinhphu.vn", "vbpl.moj.gov.vn",
    "bocongan.gov.vn", "eur-lex.europa.eu", "www.gov.uk",
    "www.ftc.gov", "www.copyright.gov", "www.wipo.int",
    "www.nist.gov", "creativecommons.org", "docs.github.com",
}
SOURCE_FIELDS = {
    "id", "jurisdiction", "title", "effective_on", "legal_weight",
    "applicability", "official_url",
}


class ResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.external_scripts: list[str] = []
        self.external_frames: list[str] = []
        self.forms = 0
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = dict(attrs)
        if tag == "script" and d.get("src"):
            self.external_scripts.append(d["src"])
        if tag in {"iframe", "object", "embed"}:
            self.external_frames.append(str(d.get("src") or d.get("data") or tag))
        if tag == "form":
            self.forms += 1
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])


def validate_source_registry(data: object, current_date: date | None = None) -> list[str]:
    """Check source metadata, date strings, authority domains, and explicit scopes."""
    today = current_date or date(2026, 10, 29)
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Legal sources registry must be a JSON object."]
    if data.get("revision") != "V3.2 legal-security.1":
        errors.append("Revision must match documented legal gate.")
    if data.get("verified_on") != "2026-10-29":
        errors.append("Legal registry verified_on must be 2026-10-29.")
    sources = data.get("sources")
    if not isinstance(sources, list):
        return errors + ["Legal registry missing sources array."]
    if len(sources) != len(REQUIRED_IDS):
        errors.append(f"Expected {len(REQUIRED_IDS)} source entries, got {len(sources)}.")
    seen: set[str] = set()
    for n, item in enumerate(sources, start=1):
        if not isinstance(item, dict) or set(item) != SOURCE_FIELDS:
            errors.append(f"Entry {n}: unexpected or missing fields.")
            continue
        sid = item["id"]
        if not isinstance(sid, str):
            errors.append(f"Entry {n}: ID must be a string.")
            continue
        if sid in seen:
            errors.append(f"Duplicate source ID: {sid}.")
        seen.add(sid)
        if sid not in REQUIRED_IDS:
            errors.append(f"Unreviewed source ID: {sid}.")
        for label in ("title", "jurisdiction", "applicability"):
            v = item[label]
            if not isinstance(v, str) or len(v.strip()) < 4:
                errors.append(f"Source {sid}: missing {label}.")
        kind = item["legal_weight"]
        if kind not in {"binding", "treaty", "voluntary", "platform-terms", "guidance"}:
            errors.append(f"Source {sid}: unrecognized weight.")
        url = item["official_url"]
        if not isinstance(url, str):
            errors.append(f"Source {sid}: URL is missing.")
        else:
            p = urlsplit(url)
            if p.scheme != "https" or p.hostname not in ALLOWED_DOMAINS or p.username or p.password:
                errors.append(f"Source {sid}: not an allowlisted HTTPS authority.")
        effective = item["effective_on"]
        if effective is not None:
            if not isinstance(effective, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", effective):
                errors.append(f"Source {sid}: malformed effective_on.")
            else:
                try:
                    when = date.fromisoformat(effective)
                    if when > today:
                        errors.append(f"Source {sid}: future law misreported as currently effective.")
                except ValueError:
                    errors.append(f"Source {sid}: invalid effective_on calendar date.")
        if sid in REQUIRED_IDS and effective != REQUIRED_IDS[sid]:
            errors.append(f"Source {sid}: effective date differs from manually reviewed record.")
    missing = set(REQUIRED_IDS) - seen
    if missing:
        errors.append(f"Missing reviewed source IDs: {sorted(missing)}.")
    # EU AI Act was amended in July 2026; never silently revert to a 2024-only source.
    if "EU-AI-ACT" not in seen or "EU-AI-OMNIBUS-2026" not in seen:
        errors.append("EU AI Act amendment 2026 must be explicitly documented.")
    return errors


def validate_policy_files(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in POLICIES:
        file = root / relative
        if not file.is_file():
            errors.append(f"Missing policy file: {relative}.")
            continue
        text = file.read_text(encoding="utf-8")
        if len(text) < 1200:
            errors.append(f"Policy document too short: {relative}.")
        if "https://" not in text:
            errors.append(f"Policy has no primary source links: {relative}.")
        if re.search(r"docid=215855\b", text):
            errors.append(f"Stale personal-data law citation: {relative}.")
    if any(not (root / name).is_file() for name in POLICIES):
        return errors  # Missing-policy test must fail closed, not crash on FileNotFoundError.
    rights = (root / "RIGHTS_AND_LICENSING.md").read_text(encoding="utf-8")
    if "không" not in rights.lower() or "bên thứ ba" not in rights.lower():
        errors.append("Rights policy must distinguish third-party materials.")
    security = (root / "SECURITY.md").read_text(encoding="utf-8")
    if "private vulnerability reporting" not in security.lower():
        errors.append("Security policy must document private vulnerability reporting limitations.")
    privacy = (root / "PRIVACY.md").read_text(encoding="utf-8")
    if "GitHub Pages" not in privacy or "IP" not in privacy:
        errors.append("Privacy policy must disclose GitHub Pages IP logging.")
    commerce = (root / "docs/quy-trinh-thuong-mai-hoa.md").read_text(encoding="utf-8")
    if not all(f"G{i:02d}" in commerce for i in range(1, 13)) or "NO-GO" not in commerce:
        errors.append("Commercial release must retain 12 no-go evidence gates.")
    return errors


def validate_website_legal(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in ("web/v3/index.html", "web/v3/legal.html"):
        file = root / relative
        if not file.is_file():
            errors.append(f"Missing public HTML: {relative}.")
            continue
        html = file.read_text(encoding="utf-8")
        parser = ResourceParser()
        parser.feed(html)
        if parser.external_scripts or parser.external_frames or parser.forms:
            errors.append(f"{relative}: external JS/embed or data-collection form requires new review.")
        for marker in ("pixel", "google-analytics", "googletagmanager", "facebook.net/tr"):
            if marker in html.lower():
                errors.append(f"{relative}: unreviewed analytics or tracking marker: {marker}.")
        if "web/v3/index.html" in relative:
            if "legal.html" not in parser.links:
                errors.append("Public catalog footer must link the legal notice.")
        else:
            if "PRIVACY.md" not in html or "SECURITY.md" not in html or "RIGHTS_AND_LICENSING.md" not in html:
                errors.append("Public legal page must link three core policies.")
            if "29/10/2026" not in html:
                errors.append("Public legal page must display review date.")
            if not any("eur-lex.europa.eu/eli/reg/2026/1744" in link for link in parser.links):
                errors.append("Public legal page must cite the amended 2026 EU AI Act.")
    return errors


def validate_all(root: Path = ROOT) -> list[str]:
    try:
        data = json.loads((root / "data/v3_2/legal_sources.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Legal sources unavailable or invalid: {exc}"]
    return (validate_source_registry(data) + validate_policy_files(root) +
            validate_website_legal(root) + validate_six_countries(root))


def main() -> int:
    parser = argparse.ArgumentParser(description="Kiểm thử nhất quán pháp lý và an ninh xuất bản V3.2")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = validate_all()
    result = {
        "status": "pass" if not errors else "fail",
        "sources": len(REQUIRED_IDS),
        "policy_files": len(POLICIES),
        "foreign_country_sources": 28,
        "foreign_country_count": 6,
        "commercial_enabled": False,
        "privacy_impact_assessment_completed": False,
        "legal_compliance_certified": False,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS: 21 nguồn và chính sách có cấu trúc, chưa chứng nhận tuân thủ." if not errors else "\n".join(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
