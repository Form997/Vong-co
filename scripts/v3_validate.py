#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAI ĐẤT V3.0 — validate metadata without third-party dependencies or network.

Run from anywhere:
    python scripts/v3_validate.py
    python scripts/v3_validate.py --json
    python -m unittest discover -s tests -p "test_*.py" -v

This checks provenance links to local V2 reviews and prevents accidental promotion
of unverified V2 material into approved performance or rights-cleared data.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "v3" / "catalog.json"
SCHEMA = ROOT / "data" / "v3" / "schema.json"
FAMILIES = (
    ("sau-bac", "Sáu Bắc", 1, 6),
    ("bay-le", "Bảy Lễ", 7, 13),
    ("ba-nam", "Ba Nam", 14, 16),
    ("bon-oan", "Bốn Oán", 17, 20),
)
ALLOWED_EVIDENCE = frozenset(("source_indexed", "source_reported", "derived_unverified"))
ROOT_FIELDS = frozenset((
    "schema_version", "project", "started_on", "origin_branch", "catalog_status",
    "rights_notice", "verification_notice", "variant_status_definitions", "items",
))
PIECE_FIELDS = frozenset((
    "id", "slug", "title", "family", "family_label", "aliases", "review_status",
    "performance_status", "rights_status", "readme_document", "review_document",
    "variants", "research_note",
))
VARIANT_FIELDS = frozenset((
    "variant_id", "label", "phrase_count", "beats_per_phrase",
    "evidence_status", "reference_url", "qualification",
))


def require_exact_fields(errors: list[str], entry: dict, fields: frozenset[str], context: str):
    missing = fields - set(entry)
    extra = set(entry) - fields
    if missing:
        errors.append(f"{context}: thiếu trường {sorted(missing)}.")
    if extra:
        errors.append(f"{context}: có trường lạ {sorted(extra)}.")



def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"JSON lặp khóa: {key!r}")
        result[key] = value
    return result


def strict_load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        obj = json.load(f, object_pairs_hook=reject_duplicate_keys)
    if not isinstance(obj, dict):
        raise ValueError("JSON phải là object ở cấp gốc")
    return obj


def validate_catalog(data: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Gốc JSON không phải object."]
    require_exact_fields(errors, data, ROOT_FIELDS, "Dữ liệu gốc")
    if data.get("schema_version") != "3.0.0-alpha.1":
        errors.append("Sai schema_version V3.0-alpha.1.")
    if data.get("catalog_status") != "research_preview":
        errors.append("V3 mới chỉ được đánh dấu research_preview.")
    if data.get("origin_branch") != "v2-development":
        errors.append("Thiếu provenance gốc V2.")
    if data.get("started_on") != "2026-10-28":
        errors.append("Ngày khởi động V3 phải khớp biên bản 28/10/2026.")
    for key in ("project", "verification_notice", "rights_notice"):
        if not isinstance(data.get(key), str) or len(data[key].strip()) < 20:
            errors.append(f"Thiếu giải thích cấp toàn bộ dữ liệu: {key}.")
    definitions = data.get("variant_status_definitions")
    if not isinstance(definitions, dict) or set(definitions) != ALLOWED_EVIDENCE:
        errors.append("Thiếu từ điển ba mức chứng cứ của dị bản.")

    items = data.get("items")
    if not isinstance(items, list):
        return errors + ["'items' phải là mảng."]
    if len(items) != 20:
        errors.append(f"Cần đúng 20 bản Tổ, hiện có {len(items)}.")
    seen_slugs: set[str] = set()
    seen_variants: set[str] = set()
    expected_by_number = {
        i: (group, label)
        for group, label, first, last in FAMILIES
        for i in range(first, last + 1)
    }
    for idx, item in enumerate(items, start=1):
        prefix = f"items[{idx - 1}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} phải là object.")
            continue
        require_exact_fields(errors, item, PIECE_FIELDS, prefix)
        piece_id = item.get("id")
        if type(piece_id) is not int or piece_id != idx:
            errors.append(f"{prefix}.id phải là số {idx}, không được đảo/trùng.")
        slug = item.get("slug")
        if not isinstance(slug, str) or not re.fullmatch(rf"{idx:02d}-[a-z0-9-]+", slug):
            errors.append(f"{prefix}.slug không khớp số bài: {slug!r}.")
            slug = ""
        if slug in seen_slugs:
            errors.append(f"{prefix}.slug lặp: {slug}.")
        seen_slugs.add(slug)
        if not isinstance(item.get("title"), str) or not item["title"].strip():
            errors.append(f"{prefix}.title trống.")
        family = expected_by_number.get(idx)
        if family and (item.get("family"), item.get("family_label")) != family:
            errors.append(f"{prefix} nhóm sai cho bài {idx}.")
        if not isinstance(item.get("aliases"), list) or any(not isinstance(x, str) for x in item["aliases"]):
            errors.append(f"{prefix}.aliases phải là mảng chuỗi.")
        elif len(set(norm.casefold() for norm in item["aliases"])) != len(item["aliases"]):
            errors.append(f"{prefix}.aliases có tên trùng.")
        if item.get("review_status") != "source_review_open":
            errors.append(f"{prefix}: hồ sơ V2 chỉ mới được mở, chưa thể nâng cấp mức kiểm nguồn.")
        if item.get("performance_status") != "pending":
            errors.append(f"{prefix}: nghiêm cấm đánh dấu đã nghiệm thu biểu diễn không có chứng cứ.")
        if item.get("rights_status") != "unverified":
            errors.append(f"{prefix}: quyền tài liệu chưa được làm rõ.")
        if not isinstance(item.get("research_note"), str) or len(item["research_note"].strip()) < 12:
            errors.append(f"{prefix}: cần ghi rõ cảnh báo nghiên cứu.")
        for field, suffix in (
            ("readme_document", "README.md"),
            ("review_document", "v2-bien-ban-nghiem-thu.md"),
        ):
            rel = item.get(field)
            required = f"ban-to/{slug}/{suffix}"
            if rel != required:
                errors.append(f"{prefix}.{field} không trỏ đúng hồ sơ bài {idx}: {rel!r}.")
                continue
            file_path = (root / rel).resolve()
            if not file_path.is_relative_to(root.resolve()) or not file_path.is_file():
                errors.append(f"{prefix}.{field}: không tồn tại tệp {rel}.")
        variants = item.get("variants")
        if not isinstance(variants, list) or not variants:
            errors.append(f"{prefix}: cần ít nhất một hệ bản có nguồn.")
            continue
        for j, variant in enumerate(variants):
            name = f"{prefix}.variants[{j}]"
            if not isinstance(variant, dict):
                errors.append(f"{name} không phải object.")
                continue
            require_exact_fields(errors, variant, VARIANT_FIELDS, name)
            vid = variant.get("variant_id")
            if not isinstance(vid, str) or not re.fullmatch(r"[A-Z0-9-]+", vid):
                errors.append(f"{name}.variant_id không hợp lệ.")
            if vid in seen_variants:
                errors.append(f"{name}.variant_id trùng: {vid}.")
            seen_variants.add(vid)
            count = variant.get("phrase_count")
            if type(count) is not int or not 1 <= count <= 500:
                errors.append(f"{name}.phrase_count phải là số nguyên 1–500.")
            beats = variant.get("beats_per_phrase")
            if beats not in (4, 8, None) or isinstance(beats, bool):
                errors.append(f"{name}.beats_per_phrase chỉ là 4, 8 hoặc null.")
            if variant.get("evidence_status") not in ALLOWED_EVIDENCE:
                errors.append(f"{name}: mức chứng cứ không hợp lệ.")
            url = variant.get("reference_url")
            if not isinstance(url, str):
                errors.append(f"{name}: thiếu URL nguồn.")
            else:
                u = urlsplit(url)
                if u.scheme != "https" or not u.netloc or u.username or u.password:
                    errors.append(f"{name}: URL nguồn phải là HTTPS hợp lệ.")
            for key in ("qualification", "label"):
                if not isinstance(variant.get(key), str) or len(variant[key].strip()) < 5:
                    errors.append(f"{name}: thiếu {key}.")
    # The 18/20 pair is a known frequent confounder, make accidental merge fail.
    if len(items) >= 20 and all(isinstance(x, dict) for x in items):
        if items[17].get("title") == items[19].get("title"):
            errors.append("Phụng Hoàng (#18) và Phụng Cầu (#20) là hai bài khác nhau.")
    return errors


def summary(data: dict) -> dict:
    items = data.get("items", [])
    return {
        "schema_version": data["schema_version"],
        "pieces": len(items),
        "variants": sum(len(x["variants"]) for x in items),
        "families": {label: sum(x["family"] == group for x in items) for group, label, _, _ in FAMILIES},
        "performance_approved": sum(x["performance_status"] != "pending" for x in items),
        "status": data["catalog_status"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Kiểm định danh mục V3 — chỉ dùng thư viện chuẩn")
    parser.add_argument("--json", action="store_true", help="In kết quả máy đọc JSON")
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    args = parser.parse_args()
    try:
        data = strict_load(args.catalog)
        schema = strict_load(SCHEMA)
        if schema.get("properties", {}).get("schema_version", {}).get("const") != "3.0.0-alpha.1":
            raise ValueError("JSON Schema không cùng thế hệ.")
        if set(schema.get("required", ())) != ROOT_FIELDS:
            raise ValueError("JSON Schema thiếu/thừa trường gốc so với validator.")
        if set(schema.get("$defs", {}).get("piece", {}).get("required", ())) != PIECE_FIELDS:
            raise ValueError("JSON Schema thiếu/thừa trường bài bản so với validator.")
        if set(schema.get("$defs", {}).get("variant", {}).get("required", ())) != VARIANT_FIELDS:
            raise ValueError("JSON Schema thiếu/thừa trường dị bản so với validator.")
        errors = validate_catalog(data)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if errors:
        for problem in errors:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    result = summary(data)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"PASS: {result['pieces']}/20 bản Tổ, {result['variants']} hệ bản/dị bản.")
        print("PASS: tất cả biên bản V2 tồn tại, 0/20 nghiệm thu diễn xướng.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
