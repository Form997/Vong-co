#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAI ĐẤT V3.2 — validate phrase-label locators against source V2 ledgers.

Only 2 specific systems are indexed in this release:
  LT-32-4 from Văn Dần via the 32-row V2 review
  PC-40-8 from Nhị Tấn IV via the 40-row V2 review

This does not verify musical notes, meter in performance, song lang, lyric
alignment by beat, transcriptions, audio rights or artistic correctness.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from v3_validate import ROOT, CATALOG, strict_load, validate_catalog

INDEX = ROOT / "data" / "v3_2" / "phrase_index.json"
ROOT_KEYS = {"schema_version", "started_on", "research_scope",
             "performance_status", "rights_status", "reader_notice", "items"}
ITEM_KEYS = {"piece_id", "slug", "title", "variant_id", "phrase_count",
             "beats_per_phrase", "source_register", "source_url",
             "source_description", "sections", "phrases"}
SECTION_KEYS = {"label", "start", "end"}
PHRASE_KEYS = {"number", "section", "source_music_locator", "source_lyric_locator",
               "printed_music_page", "printed_lyric_page", "ending_token",
               "pair_index", "source_note"}
CONFIGS = {
    1: ("LT-32-4", 32, 4, "ban-to/01-luu-thuy-truong/v2-ra-soat-32-cau.md",
        (("I", 1, 8), ("II", 9, 16), ("III", 17, 24), ("IV", 25, 32))),
    20: ("PC-40-8", 40, 8, "ban-to/20-phung-cau/v2-ra-soat-40-cau.md",
         (("I", 1, 18), ("II", 19, 26), ("III", 27, 40))),
}


def exact_fields(entry: object, keys: set[str], label: str, errors: list[str]) -> bool:
    if not isinstance(entry, dict):
        errors.append(f"{label} không phải object.")
        return False
    missing = keys - set(entry)
    extra = set(entry) - keys
    if missing or extra:
        errors.append(f"{label}: thiếu {sorted(missing)}, trường lạ {sorted(extra)}.")
        return False
    return True


def source_rows(path: Path, expected_count: int) -> list[list[str]]:
    """Read only the numbered table rows from the user's existing V2 ledger."""
    rows: list[list[str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\|\s*\d{2}\s*\|", line):
            cells = [x.strip() for x in line.strip().split("|")[1:-1]]
            if len(cells) != 6:
                raise ValueError(f"{path}: bảng V2 bị đổi số cột ({len(cells)}).")
            rows.append(cells)
    if len(rows) != expected_count:
        raise ValueError(f"{path}: có {len(rows)} dòng nhãn, chờ {expected_count}.")
    for n, cells in enumerate(rows, start=1):
        if cells[0] != f"{n:02d}":
            raise ValueError(f"{path}: dòng số {n} không còn liên tục.")
    return rows


def expectation(piece_id: int, cells: list[str], number: int) -> dict:
    if piece_id == 1:
        layer = int(cells[1])
        if not 1 <= layer <= 4 or cells[3] != "Có số câu tương ứng" or not cells[5].startswith("CHỜ"):
            raise ValueError(f"Lưu Thủy Trường câu {number}: bảng chưa được đối chiếu.")
        section = ("I", "II", "III", "IV")[layer - 1]
        return {
            "number": number,
            "section": section,
            "source_music_locator": f"Bảng V2: nhãn nhạc câu {number:02d}",
            "source_lyric_locator": f"Bảng V2: nhãn lời câu {number:02d}",
            "printed_music_page": None,
            "printed_lyric_page": None,
            "ending_token": cells[2],  # preserve source glyph HO != HÒ
            "pair_index": None,
            "source_note": None if cells[4] == "—" else cells[4],
        }
    if cells[1] not in ("I", "II", "III") or not cells[5].startswith("CHỜ"):
        raise ValueError(f"Phụng Cầu câu {number}: lớp/trạng thái không hợp lệ.")
    pages = [x.strip() for x in cells[3].split("/")]
    if len(pages) != 2 or not all(x.isdigit() for x in pages):
        raise ValueError(f"Phụng Cầu câu {number}: thiếu trang in nhạc/lời.")
    music, lyric = map(int, pages)
    if music not in (332, 334, 336, 338, 340) or lyric != music + 1:
        raise ValueError(f"Phụng Cầu câu {number}: trang nằm ngoài dải 332–341.")
    pair = int(cells[2])
    if pair != (number + 1) // 2:
        raise ValueError(f"Phụng Cầu câu {number}: sai chỉ mục cặp lẻ/chẵn.")
    return {
        "number": number,
        "section": cells[1],
        "source_music_locator": f"Bản Nhị Tấn IV, nhạc tr. {music}, câu {number:02d}",
        "source_lyric_locator": f"Bản Nhị Tấn IV, lời tr. {lyric}, câu {number:02d}",
        "printed_music_page": music,
        "printed_lyric_page": lyric,
        "ending_token": None,
        "pair_index": pair,
        "source_note": None if cells[4] == "—" else cells[4],
    }


def validate_phrase_index(data: object, catalog: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if not exact_fields(data, ROOT_KEYS, "Gốc V3.2", errors):
        return errors
    if data["schema_version"] != "3.2.0-alpha.1" or data["started_on"] != "2026-10-28":
        errors.append("Sai mã/niên đại phiên bản V3.2.")
    if data["research_scope"] != "source_label_index_only":
        errors.append("Không được tự nâng cấp chỉ mục câu thành tổng phổ.")
    if data["performance_status"] != "pending" or data["rights_status"] != "unverified":
        errors.append("Không được khai báo đã nghiệm thu/cấp quyền khi chưa có chứng cứ.")
    if not isinstance(data["reader_notice"], str) or "0/20" not in data["reader_notice"]:
        errors.append("Thiếu cảnh báo 0/20 nghiệm thu.")
    if not isinstance(data["items"], list) or len(data["items"]) != 2:
        return errors + ["V3.2 đợt này chỉ có 2 hệ đã kiểm sổ câu; không tự sinh đủ 20."]
    catalog_by_id = {p["id"]: p for p in catalog["items"]}
    seen = set()
    for item in data["items"]:
        if not exact_fields(item, ITEM_KEYS, "Hệ bài", errors):
            continue
        piece_id = item["piece_id"]
        if type(piece_id) is not int or piece_id not in CONFIGS or piece_id in seen:
            errors.append("Mã bài trùng hoặc ngoài 01/20.")
            continue
        seen.add(piece_id)
        variant_id, count, beats, register, sections = CONFIGS[piece_id]
        original = catalog_by_id[piece_id]
        if (item["slug"], item["title"], item["variant_id"],
            item["phrase_count"], item["beats_per_phrase"], item["source_register"]) != (
                original["slug"], original["title"], variant_id, count, beats, register):
            errors.append(f"Bài {piece_id}: tên/hệ/nhịp/nguồn khác catalog và V2.")
        variant = next((v for v in original["variants"] if v["variant_id"] == variant_id), None)
        if variant is None or item["source_url"] != variant["reference_url"]:
            errors.append(f"Bài {piece_id}: URL không đúng hệ nguồn V3.")
        url = urlsplit(str(item["source_url"]))
        if url.scheme != "https" or not url.hostname:
            errors.append(f"Bài {piece_id}: URL phải HTTPS.")
        if not isinstance(item["source_description"], str) or len(item["source_description"]) < 40:
            errors.append(f"Bài {piece_id}: thiếu mô tả giới hạn nguồn.")
        sections_data = item["sections"]
        expected_sections = [{"label": l, "start": a, "end": b} for l, a, b in sections]
        if sections_data != expected_sections:
            errors.append(f"Bài {piece_id}: lớp không đúng phạm vi V2 (không được quy đổi hệ).")
        expected_register = root / register
        try:
            rows = source_rows(expected_register, count)
        except (OSError, ValueError) as e:
            errors.append(str(e))
            continue
        phrases = item["phrases"]
        if not isinstance(phrases, list) or len(phrases) != count:
            errors.append(f"Bài {piece_id}: phải đủ {count} câu theo một hệ.")
            continue
        for n, phrase in enumerate(phrases, start=1):
            if not exact_fields(phrase, PHRASE_KEYS, f"Bài {piece_id} câu {n}", errors):
                continue
            try:
                expected = expectation(piece_id, rows[n-1], n)
            except (ValueError, TypeError) as e:
                errors.append(str(e))
                continue
            if phrase != expected:
                different = [k for k in PHRASE_KEYS if phrase.get(k) != expected[k]]
                errors.append(f"Bài {piece_id} câu {n}: không trùng bảng nguồn V2 ở {different}.")
    if seen != set(CONFIGS):
        errors.append("Chưa đủ 2 hệ chỉ mục đã chọn.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Kiểm định dữ liệu 72 vị trí câu học V3.2")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        catalog = strict_load(CATALOG)
        errors = validate_catalog(catalog) + validate_phrase_index(strict_load(INDEX), catalog)
    except (OSError, ValueError, TypeError) as exc:
        errors = [str(exc)]
    results = {
        "status": "pass" if not errors else "fail",
        "catalog_pieces": 20,
        "indexed_pieces": 2,
        "indexed_variants": 2,
        "indexed_phrases": 72,
        "performance_approved": 0,
        "rights_verified": False,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("PASS: 72 nhãn câu đối chiếu nguyên vị trí V2." if not errors else "\n".join(errors))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
