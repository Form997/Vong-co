#!/usr/bin/env python3
"""V3.4: validate source-label locators against the two distinct V2 ledgers.

The comparison proves agreement with V2 records, not independent PDF, audio,
rights or performance verification. Never derive one Cổ Bản system from another.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v3_validate import ROOT, CATALOG, strict_load, validate_catalog
from v3_3_validate import (INDEX as V33_INDEX, NT_II, ROOT_FIELDS, ITEM_FIELDS,
                            PHRASE_FIELDS, parse_rows, validate_v33)

INDEX = ROOT / "data/v3_4/phrase_index.json"
SCHEMA = ROOT / "data/v3_4/schema.json"
SETTINGS = {
    "CBV-34-4": {
        "count": 34, "register": "ban-to/04-co-ban-van/v2-kiem-34-cau-co-ban-van.md",
        "layers": [("I",1,6),("II",7,12),("III",13,19),("IV",20,26),("V",27,34)],
        "description": "Cổ Bản Vắn, Nhị Tấn tập II: sổ V2 ghi 34 nhãn, 5 lớp; trang lời 117 được đối chiếu qua văn bản PDF. Không nhập mục Thủ tập I hay trộn với bản Trường.",
    },
    "CBT-68-4": {
        "count": 68, "register": "ban-to/04-co-ban-van/v2-kiem-68-cau-co-ban-truong.md",
        "layers": [("I",1,6),("II",7,12),("III",13,24),("IV",25,30),("V",31,36),("VI",37,42),("VII",43,52),("VIII",53,68)],
        "description": "Cổ Bản Trường, Nhị Tấn tập II: sổ V2 ghi 68 nhãn, 8 lớp; trang 136–137 được đối chiếu qua văn bản PDF. Không nhập mục Thủ tập I hay trộn với bản Vắn.",
    },
}


def candidate_phrase(variant: str, n: int, row: list[str]) -> dict:
    """Build locators exclusively from the corresponding numbered V2 row."""
    cfg = SETTINGS[variant]
    _, layer, music_text, lyric_text, evidence, note, status = row
    expected_layer = next(label for label, first, last in cfg["layers"] if first <= n <= last)
    if variant == "CBV-34-4":
        expected_pages = (114,115) if n <= 16 else (116,117)
        expected_evidence = "Có ở hai nguồn"
    else:
        expected_pages = ((134,135) if n <= 10 else (136,137) if n <= 30
                          else (138,139) if n <= 50 else (140,141))
        expected_evidence = "Có nhãn tại Nhị Tấn II và Văn Dần"
    if not music_text.isdigit() or not lyric_text.isdigit():
        raise ValueError(f"{variant} #{n}: trang phải là số trang in được ghi trong sổ.")
    music, lyric = int(music_text), int(lyric_text)
    if (layer != expected_layer or (music,lyric) != expected_pages or
            evidence != expected_evidence or status != "CHỜ" or not note):
        raise ValueError(f"{variant} #{n}: lớp, trang, chứng cứ hoặc trạng thái không khớp sổ V2.")
    # Keep the V2 row's issue as a locator note, not a lyric or musical reading.
    # Exclude short lyric fragments in the ledger: the ledger remains linked.
    if variant == "CBV-34-4" and n in (3,4):
        note = "Sổ V2 ghi khác biệt chữ lời giữa hai nguồn; cần đối chiếu."
    elif variant == "CBT-68-4" and n in (2,3,5):
        note = "Sổ V2 ghi khác biệt chữ lời giữa hai nguồn; cần đối chiếu."
    if variant == "CBV-34-4" and lyric == 117:
        note += " Theo sổ V2, trang lời 117 đối chiếu qua văn bản trích PDF."
    if variant == "CBT-68-4" and music == 136:
        note += " Theo sổ V2, trang 136–137 đối chiếu qua văn bản trích PDF."
    return {
        "number": n, "section": layer,
        "source_music_locator": f"Theo sổ V2: Nhị Tấn tập II, chữ nhạc tr. {music}, câu {n:02d}",
        "source_lyric_locator": f"Theo sổ V2: Nhị Tấn tập II, lời tr. {lyric}, câu {n:02d}",
        "printed_music_page": music, "printed_lyric_page": lyric,
        "ending_token": None, "pair_index": None, "source_note": note,
    }


def expected_item(variant: str, catalog: dict, root: Path = ROOT) -> dict:
    cfg = SETTINGS[variant]
    piece = next(p for p in catalog["items"] if p["id"] == 4)
    rows = parse_rows(root / cfg["register"], cfg["count"], 7)
    return {
        "piece_id": 4, "slug": piece["slug"], "title": piece["title"],
        "variant_id": variant, "phrase_count": cfg["count"], "beats_per_phrase": 4,
        "source_register": cfg["register"], "source_url": NT_II,
        "source_description": cfg["description"],
        "sections": [{"label": label, "start": first, "end": last}
                     for label, first, last in cfg["layers"]],
        "phrases": [candidate_phrase(variant, n, row) for n, row in enumerate(rows,1)],
    }


def validate_schema(schema: object) -> list[str]:
    if not isinstance(schema, dict):
        return ["V3.4 schema phải là đối tượng JSON."]
    errors = []
    props, defs = schema.get("properties", {}), schema.get("$defs", {})
    for name, obj, fields in (("root", schema, ROOT_FIELDS), ("item", defs.get("item", {}), ITEM_FIELDS),
                              ("phrase", defs.get("phrase", {}), PHRASE_FIELDS),
                              ("section", defs.get("section", {}), {"label", "start", "end"})):
        if not isinstance(obj,dict) or set(obj.get("required", [])) != fields or obj.get("additionalProperties") is not False:
            errors.append(f"Schema V3.4: trường hoặc tính chặt chẽ {name} không đúng.")
    if (props.get("schema_version", {}).get("const") != "3.4.0-alpha.1" or
            props.get("performance_status", {}).get("const") != "pending" or
            props.get("rights_status", {}).get("const") != "unverified" or
            props.get("items", {}).get("minItems") != 6 or props.get("items", {}).get("maxItems") != 6):
        errors.append("Schema V3.4 sai phiên bản, số hệ hoặc trạng thái quyền/nghiệm thu.")
    return errors


def validate_v34(data: object, catalog: dict, root: Path = ROOT) -> list[str]:
    errors = []
    try:
        previous = strict_load(root / "data/v3_3/phrase_index.json")
        errors += validate_v33(previous, catalog, root)
        errors += validate_schema(strict_load(root / "data/v3_4/schema.json"))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return [f"Không kiểm được cơ sở lịch sử hoặc schema V3.4: {exc}"]
    if not isinstance(data, dict) or set(data) != ROOT_FIELDS:
        return errors + ["Trường gốc V3.4 không hợp lệ."]
    if (data["schema_version"], data["started_on"], data["research_scope"], data["performance_status"], data["rights_status"]) != (
            "3.4.0-alpha.1", "2026-10-29", "source_label_index_only", "pending", "unverified"):
        errors.append("Sai phiên bản, mục đích hoặc trạng thái quyền/nghiệm thu.")
    if not isinstance(data["reader_notice"], str) or "0/20" not in data["reader_notice"]:
        errors.append("Thiếu cảnh báo 0/20 bài nghiệm thu.")
    items = data["items"]
    if not isinstance(items, list) or len(items) != 6 or any(not isinstance(i,dict) for i in items):
        return errors + ["V3.4 phải có đúng sáu hệ."]
    if [x.get("variant_id") for x in items] != ["LT-32-4", "PLC-34-4", "BBC-44-4", "CBV-34-4", "CBT-68-4", "PC-40-8"]:
        return errors + ["Sai thứ tự hoặc thiếu hệ Vắn/Trường riêng biệt."]
    if [items[i] for i in (0,1,2,5)] != previous["items"]:
        errors.append("Dữ liệu bốn hệ lịch sử V3.3 bị thay đổi.")
    for i, variant in ((3,"CBV-34-4"), (4,"CBT-68-4")):
        try:
            expected = expected_item(variant, catalog, root)
            if items[i] != expected:
                errors.append(f"{variant}: dữ liệu, nguồn, trang hoặc ghi chú không khớp từng hàng sổ V2.")
            piece = next(p for p in catalog["items"] if p["id"] == 4)
            catalog_variant = next((v for v in piece["variants"] if v["variant_id"] == variant), None)
            if not catalog_variant or (catalog_variant["phrase_count"], catalog_variant["beats_per_phrase"]) != (SETTINGS[variant]["count"], 4):
                errors.append(f"{variant}: khác danh mục.")
        except (OSError, ValueError, TypeError, KeyError, StopIteration) as exc:
            errors.append(f"{variant}: không kiểm được sổ V2: {exc}")
    if len({x.get("piece_id") for x in items}) != 5:
        errors.append("Sáu hệ phải thuộc năm bài riêng biệt.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Kiểm V3.4 với hai sổ Cổ Bản V2, không nghiệm thu diễn xướng.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        catalog, data = strict_load(CATALOG), strict_load(INDEX)
        errors = validate_catalog(catalog) + validate_v34(data, catalog)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors = [str(exc)]
    result = {"status": "fail" if errors else "pass", "indexed_pieces": 5, "source_label_systems": 6,
              "indexed_labels": 252, "performances_approved": 0, "rights_status": "unverified", "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else
          "\n".join(errors) if errors else "PASS: 252 nhãn thuộc 6 hệ / 5 bài; 0/20 nghiệm thu.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
