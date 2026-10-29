#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAI DAT V3.2: mechanical evidence gate for six foreign jurisdictions.

Only validates provenance, edition labels, country coverage and stated limits.
It does NOT certify legal compliance or verify laws live on the internet.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
from urllib.parse import urlsplit

from v3_validate import ROOT

REGISTRY = ROOT / "data/v3_2/six_country_sources.json"
COUNTRIES = {
    "US": {"file": "my.md", "ids": {"US-COPPA", "US-CCPA-2026", "US-DMCA-512", "US-CFAA-1030"}},
    "RU": {"file": "nga.md", "ids": {"RU-PD-152", "RU-INFO-149", "RU-KII-187", "RU-IP-IV"}},
    "CN": {"file": "trung-quoc.md", "ids": {"CN-CSL-2026", "CN-PIPL", "CN-DSL", "CN-CROSSBORDER-2024", "CN-COPYRIGHT-2021", "CN-ECOM-2019"}},
    "AU": {"file": "uc.md", "ids": {"AU-PRIVACY-2026", "AU-NDB", "AU-CYBER-2024", "AU-COPYRIGHT-2026", "AU-ACL"}},
    "JP": {"file": "nhat-ban.md", "ids": {"JP-APPI-2026", "JP-APPI-2026-AMEND", "JP-COPYRIGHT", "JP-COPYRIGHT-AMEND-2026"}},
    "KR": {"file": "han-quoc.md", "ids": {"KR-PIPA-2026", "KR-NETWORK-2026", "KR-COPYRIGHT-2026", "KR-AI-2026", "KR-ECOM-2026"}},
}
LEGAL_DOMAINS = {
    "www.ftc.gov", "cppa.ca.gov", "uscode.house.gov",
    "mintrud.gov.ru", "rosstat.gov.ru", "www.cert.gov.ru", "rospatent.gov.ru",
    "www.cac.gov.cn", "flk.npc.gov.cn", "www.ncac.gov.cn", "www.beijing.gov.cn",
    "www.legislation.gov.au", "www.oaic.gov.au", "www.accc.gov.au",
    "www.ppc.go.jp", "www.bunka.go.jp", "www.law.go.kr", "law.go.kr",
}
FIELDS = {"id", "jurisdiction", "theme", "title", "status", "effective_on", "official_url", "scope_note", "version_note"}
STATUSES = {"in_force", "phased", "promulgated-pending", "official-guidance"}
STATEMENT_DATE = date(2026, 10, 29)


def validate_country_registry(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Six-country registry must be a JSON object."]
    if data.get("revision") != "V3.2 six-jurisdictions.1" or data.get("verified_on") != "2026-10-29":
        errors.append("Revision and as-of date do not match the reviewed six-country snapshot.")
    if data.get("commercial_enabled") is not False:
        errors.append("International policy cannot claim commercial use enabled.")
    if data.get("jurisdictions") != list(COUNTRIES):
        errors.append("Six countries must be present exactly once in their reviewed order.")
    sources = data.get("sources")
    if not isinstance(sources, list):
        return errors + ["Sources must be a list."]
    required_ids = {i for country in COUNTRIES.values() for i in country["ids"]}
    if len(sources) != len(required_ids):
        errors.append(f"Expected {len(required_ids)} source entries, got {len(sources)}.")
    seen: set[str] = set()
    counted = {country: 0 for country in COUNTRIES}
    for index, entry in enumerate(sources, 1):
        if not isinstance(entry, dict) or set(entry) != FIELDS:
            errors.append(f"Source {index}: missing or extra attributes.")
            continue
        sid = entry["id"]
        country = entry["jurisdiction"]
        if not isinstance(sid, str):
            errors.append(f"Source {index}: id must be text.")
            continue
        if sid in seen:
            errors.append(f"Duplicate source ID: {sid}.")
        seen.add(sid)
        if country not in COUNTRIES or sid not in COUNTRIES[country]["ids"]:
            errors.append(f"Wrong country or unreviewed source: {sid}/{country}.")
        else:
            counted[country] += 1
        if entry["status"] not in STATUSES:
            errors.append(f"{sid}: invalid status.")
        url = entry["official_url"]
        if not isinstance(url, str):
            errors.append(f"{sid}: missing official URL.")
        else:
            parsed = urlsplit(url)
            if parsed.scheme != "https" or parsed.hostname not in LEGAL_DOMAINS or parsed.username or parsed.password:
                errors.append(f"{sid}: URL must be exact allowlisted official https host.")
        for key in ("theme", "title", "scope_note", "version_note"):
            if not isinstance(entry[key], str) or len(entry[key].strip()) < (35 if key.endswith("note") else 4):
                errors.append(f"{sid}: missing meaningful {key}.")
        effective = entry["effective_on"]
        if effective is not None:
            try:
                if not isinstance(effective, str) or effective != date.fromisoformat(effective).isoformat():
                    raise ValueError
                if date.fromisoformat(effective) > STATEMENT_DATE:
                    errors.append(f"{sid}: future effective date reported as current.")
            except (ValueError, TypeError):
                errors.append(f"{sid}: malformed effective date.")
        if entry["status"] in {"official-guidance", "promulgated-pending"} and effective is not None:
            errors.append(f"{sid}: official guidance or future-effective law must not claim a single effective date here.")
    if seen != required_ids:
        errors.append(f"Missing/extra source IDs: {sorted(seen.symmetric_difference(required_ids))}.")
    for country, expected in COUNTRIES.items():
        if counted[country] != len(expected["ids"]):
            errors.append(f"{country}: incomplete source coverage.")
    expected_fixed_dates = {
        "US-CCPA-2026": "2026-01-01",
        "CN-CSL-2026": "2026-01-01",
        "CN-PIPL": "2021-11-01",
        "CN-DSL": "2021-09-01",
        "CN-CROSSBORDER-2024": "2024-03-22",
        "CN-COPYRIGHT-2021": "2021-06-01",
        "CN-ECOM-2019": "2019-01-01",
        "RU-IP-IV": "2008-01-01",
        "KR-PIPA-2026": "2026-09-11",
        "KR-NETWORK-2026": "2026-10-02",
        "KR-COPYRIGHT-2026": "2026-10-29",
        "KR-AI-2026": "2026-07-21",
        "KR-ECOM-2026": "2026-07-21",
    }
    for entry in sources:
        if not isinstance(entry, dict):
            continue
        expected = expected_fixed_dates.get(entry.get("id"))
        if expected and entry.get("effective_on") != expected:
            errors.append(f"{entry.get('id')}: incorrectly changed manually verified effective date.")
    if not any(s.get("id") == "JP-COPYRIGHT-AMEND-2026" and s.get("status") == "promulgated-pending" for s in sources if isinstance(s, dict)):
        errors.append("Japan's 2026 copyright amendment must not be mislabeled already effective.")
    return errors


def validate_country_docs(data: object, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or not isinstance(data.get("sources"), list):
        return ["Cannot validate country documents without a source registry."]
    base = root / "docs/phap-ly-quoc-te"
    index = base / "README.md"
    if not index.is_file():
        return ["Missing six-country index README."]
    index_text = index.read_text(encoding="utf-8")
    for country, info in COUNTRIES.items():
        file = base / info["file"]
        if info["file"] not in index_text:
            errors.append(f"Index missing {country} country's document link.")
        if not file.is_file():
            errors.append(f"Missing document for {country}.")
            continue
        body = file.read_text(encoding="utf-8")
        if len(body) < 2500:
            errors.append(f"{country}: document is not sufficiently substantive.")
        for s in data["sources"]:
            if not isinstance(s, dict) or s.get("jurisdiction") != country:
                continue
            if s.get("id") not in body or s.get("official_url") not in body:
                errors.append(f"{country}: source {s.get('id')} not traceable in its document.")
        if "NO-GO" not in body or "phi thương mại" not in body:
            errors.append(f"{country}: must distinguish non-commercial and unreleased commerce.")
    if "KHÔNG" not in index_text and "không" not in index_text:
        errors.append("Index lacks limitations and scope disclaimers.")
    return errors


def validate_country_public_hub(root: Path = ROOT) -> list[str]:
    file = root / "web/v3/legal.html"
    if not file.is_file():
        return ["Public legal hub missing."]
    html = file.read_text(encoding="utf-8")
    errors: list[str] = []
    for country, info in COUNTRIES.items():
        route = f"quoc-gia/{info['file'].replace('.md','.html')}"
        if f'href="{route}"' not in html:
            errors.append(f"Public hub missing {country} law page link.")
    if "commercial" not in html.lower() and "thương mại" not in html.lower():
        errors.append("Public hub must retain commercial-use limitation.")
    return errors


def validate_all(root: Path = ROOT) -> list[str]:
    try:
        data = json.loads((root / "data/v3_2/six_country_sources.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Six-country law sources missing or malformed: {exc}"]
    return validate_country_registry(data) + validate_country_docs(data, root) + validate_country_public_hub(root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = validate_all()
    result = {
        "status": "pass" if not errors else "fail",
        "countries": list(COUNTRIES),
        "official_or_agency_sources": 28,
        "commercial_enabled": False,
        "certified_compliant": False,
        "errors": errors
    }
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else
          ("PASS: Six-country source consistency gate (not a legal certification)." if not errors else "\n".join(errors)))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
