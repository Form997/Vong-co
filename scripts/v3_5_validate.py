#!/usr/bin/env python3
"""Validate V3.5 locators against V2; no claim of performance verification."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from v3_validate import ROOT, CATALOG, strict_load, validate_catalog
from v3_3_validate import ROOT_FIELDS, parse_rows, NT_II
from v3_4_validate import validate_v34

INDEX = ROOT / "data/v3_5/phrase_index.json"
REGISTER = "ban-to/05-xuan-tinh-chan/v2-ra-soat-48-cau.md"
LAYERS = [("I", 1, 14), ("II", 15, 30), ("III", 31, 40), ("IV", 41, 48)]
DESCRIPTION = "Xuân Tình Chấn, Nhị Tấn tập II: sổ V2 ghi 48 nhãn, 4 lớp; trang 146–147 chia sẻ với đầu bài Tây Thi. Không trộn bản Thủ tập I."

def expected_item(catalog: dict, root: Path = ROOT) -> dict:
    piece = next(p for p in catalog["items"] if p["id"] == 5)
    rows = parse_rows(root / REGISTER, 48, 6)
    phrases = []
    for n, row in enumerate(rows, 1):
        _, section, pages, evidence, note, status = row
        layer = next(label for label, start, end in LAYERS if start <= n <= end)
        expected = (142,143) if n <= 20 else (144,145) if n <= 40 else (146,147)
        parts = pages.split("/")
        if len(parts) != 2 or any(not p.strip().isdigit() for p in parts):
            raise ValueError(f"XTC {n}: sai trang trong sổ.")
        music, lyric = (int(p.strip()) for p in parts)
        if (section != layer or (music,lyric) != expected or
            evidence != "Có số câu ở Nhị Tấn II và Văn Dần" or status != "CHỜ" or not note):
            raise ValueError(f"XTC {n}: lớp, trang, chứng cứ hoặc trạng thái không khớp.")
        if n == 37 and "NHẠC" not in note:
            raise ValueError("XTC 37: thiếu cảnh báo khác biệt.")
        if n in (5,11,12,23,26,30,41):
            note = "Sổ V2 ghi khác biệt hoặc điểm cần kiểm về chữ lời; cần đối chiếu."
        elif n == 37:
            note = "Sổ V2 ghi khác biệt ký hiệu nhạc; chờ thẩm âm."
        phrases.append({
            "number": n, "section": section,
            "source_music_locator": f"Theo sổ V2: Nhị Tấn tập II, chữ nhạc tr. {music}, câu {n:02d}",
            "source_lyric_locator": f"Theo sổ V2: Nhị Tấn tập II, lời tr. {lyric}, câu {n:02d}",
            "printed_music_page": music, "printed_lyric_page": lyric,
            "ending_token": None, "pair_index": None, "source_note": note,
        })
    return {
        "piece_id":5, "slug":piece["slug"], "title":piece["title"],
        "variant_id":"XTC-48-4", "phrase_count":48, "beats_per_phrase":4,
        "source_register":REGISTER, "source_url":NT_II, "source_description":DESCRIPTION,
        "sections":[{"label":label,"start":start,"end":end} for label,start,end in LAYERS],
        "phrases":phrases,
    }

def validate_v35(data: object, catalog: dict, root: Path = ROOT) -> list[str]:
    errors = []
    try:
        previous = strict_load(root / "data/v3_4/phrase_index.json")
        errors += validate_v34(previous, catalog, root)
        schema = strict_load(root / "data/v3_5/schema.json")
        expected_schema = copy.deepcopy(strict_load(root / "data/v3_4/schema.json"))
        expected_schema["properties"]["schema_version"]["const"] = "3.5.0-alpha.1"
        expected_schema["properties"]["items"]["minItems"] = 7
        expected_schema["properties"]["items"]["maxItems"] = 7
        if schema != expected_schema:
            errors.append("Schema V3.5 không khớp quy tắc V3.4 và số hệ.")
        if not isinstance(data,dict) or set(data) != ROOT_FIELDS:
            return errors + ["Trường gốc V3.5 không hợp lệ."]
        if (data["schema_version"], data["started_on"], data["research_scope"],
            data["performance_status"], data["rights_status"]) != (
            "3.5.0-alpha.1", "2026-10-29", "source_label_index_only", "pending", "unverified"):
            errors.append("Sai phiên bản, mục đích hoặc trạng thái quyền/nghiệm thu.")
        if not isinstance(data["reader_notice"],str) or "0/20" not in data["reader_notice"]:
            errors.append("Thiếu cảnh báo 0/20.")
        items = data["items"]
        if not isinstance(items,list) or len(items) != 7 or any(not isinstance(i,dict) for i in items):
            return errors + ["V3.5 phải có bảy hệ."]
        if [items[i] for i in (0,1,2,3,4,6)] != previous["items"]:
            errors.append("Dữ liệu lịch sử V3.4 bị thay đổi.")
        if items[5] != expected_item(catalog, root):
            errors.append("XTC: dữ liệu không khớp từng hàng sổ V2.")
        v = next(v for v in next(p for p in catalog["items"] if p["id"]==5)["variants"] if v["variant_id"]=="XTC-48-4")
        if (v["phrase_count"],v["beats_per_phrase"]) != (48,4):
            errors.append("XTC khác danh mục.")
        if len({i.get("piece_id") for i in items}) != 6:
            errors.append("Bảy hệ phải thuộc sáu bài.")
    except (OSError, ValueError, TypeError, KeyError, StopIteration, IndexError) as exc:
        errors.append(f"Không kiểm được V3.5: {exc}")
    return errors

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    try:
        catalog, data = strict_load(CATALOG), strict_load(INDEX)
        errors = validate_catalog(catalog) + validate_v35(data,catalog)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors = [str(exc)]
    result = {"status":"fail" if errors else "pass", "indexed_pieces":6,
              "source_label_systems":7,"indexed_labels":300,
              "performances_approved":0,"rights_status":"unverified","errors":errors}
    print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else
          "\n".join(errors) if errors else "PASS: 300 nhãn, 7 hệ, 6 bài; 0/20 nghiệm thu.")
    return int(bool(errors))

if __name__ == "__main__":
    raise SystemExit(main())
