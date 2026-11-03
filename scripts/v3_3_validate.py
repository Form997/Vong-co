#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V3.3: independent, fail-closed V2-ledger -> 150 source-label contract.

Indexes are metadata, NOT transcribed scores, verified meter, timing or licensed audio.
Keep V3.2's 72 positions byte-equivalent at item level. Never conflate Vắn/Trường.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from v3_validate import ROOT, CATALOG, strict_load, validate_catalog
from v3_2_validate import INDEX as V32_INDEX, validate_phrase_index

INDEX = ROOT / "data/v3_3/phrase_index.json"
SCHEMA = ROOT / "data/v3_3/schema.json"
NT_II = "https://www.namkyluctinh.org/eBooks/AmNhac/Nhac%20Tai%20Tu%20Nam%20Bo%202%20-%20Nhi%20Tan.pdf"
SETTINGS = {
    1: ("LT-32-4", 32, 4, "ban-to/01-luu-thuy-truong/v2-ra-soat-32-cau.md"),
    2: ("PLC-34-4", 34, 4, "ban-to/02-phu-luc-chan/v2-ra-soat-34-cau.md"),
    3: ("BBC-44-4", 44, 4, "ban-to/03-binh-ban-chan/v2-ra-soat-44-cau.md"),
    20: ("PC-40-8", 40, 8, "ban-to/20-phung-cau/v2-ra-soat-40-cau.md")
}
LAYERS = {
    2: (("I",1,8),("II",9,16),("III",17,24),("IV",25,34)),
    3: (("I",1,10),("II",11,22),("III",23,32),("IV",33,44))
}
ROOT_FIELDS = {"schema_version","started_on","research_scope","performance_status","rights_status","reader_notice","items"}
ITEM_FIELDS = {"piece_id","slug","title","variant_id","phrase_count","beats_per_phrase","source_register","source_url","source_description","sections","phrases"}
PHRASE_FIELDS = {"number","section","source_music_locator","source_lyric_locator","printed_music_page","printed_lyric_page","ending_token","pair_index","source_note"}
SECTION_FIELDS = {"label","start","end"}


def parse_rows(path: Path, count: int, columns: int) -> list[list[str]]:
    """Parse ONLY numbered rows; never infer music or missing values."""
    rows=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\|\s*\d{1,2}\s*\|",line):
            cells=[c.strip() for c in line.split("|")[1:-1]]
            rows.append(cells)
    if len(rows)!=count:
        raise ValueError(f"{path.name}: {len(rows)} rows, expected {count}.")
    for idx,c in enumerate(rows,1):
        if len(c)!=columns or not c[0].isdigit() or int(c[0])!=idx:
            raise ValueError(f"{path.name} line {idx}: bad row/order/columns.")
    return rows


def candidate_phrase(piece: int, n: int, c: list[str]) -> dict:
    """Build a deterministic comparison value, not a musical transcription."""
    if piece==2:
        _,layer,music_text,ending,lyric_text,label,note=c
        music=int(music_text)
        lyric=None if lyric_text=="—" else int(lyric_text)
        if layer not in ("I","II","III","IV") or music not in (126,128,130):
            raise ValueError(f"PLC {n}: unexpected music page/layer.")
        if lyric is not None and lyric not in (127,129):
            raise ValueError(f"PLC {n}: unexpected lyric page.")
        if (n<=32) != (lyric is not None):
            raise ValueError(f"PLC {n}: 34 music/32 printed lyrics discrepancy hidden.")
        if n in (8,34) and "DỊ BẢN" not in note:
            raise ValueError(f"PLC {n}: variant conflict marker removed.")
        if label not in ("Có nhãn câu trong Nhị Tấn và Văn Dần",
                         "Chỉ thấy ở Văn Dần; chưa thấy ở lời Nhị Tấn tập II"):
            raise ValueError(f"PLC {n}: unfamiliar lyric evidence marker.")
        if n>32 and label.startswith("Có nhãn"):
            raise ValueError(f"PLC {n}: misrepresented printed lyric presence.")
        notes=[
            note if note!="Chưa rà phách/song lang" else None,
            "Văn Dần có nhãn lời, sách Nhị Tấn tập II không in câu lời này." if n>32 else None,
            "Ký hiệu gạch ở cuối dòng bản in; KHÔNG kết luận khoảng nghỉ thực tấu." if ending=="(nghỉ)" else None
        ]
        return {
            "number":n,"section":layer,
            "source_music_locator":f"Nhị Tấn tập II, chữ nhạc tr. {music}, câu {n:02d}",
            "source_lyric_locator":(f"Nhị Tấn tập II, lời tr. {lyric}, câu {n:02d}" if lyric else
               f"Chỉ có nhãn lời ở Văn Dần cho câu {n:02d}; Nhị Tấn II không có tr. lời"),
            "printed_music_page":music,"printed_lyric_page":lyric,
            "ending_token":ending,"pair_index":None,
            "source_note":" | ".join(x for x in notes if x) or None
        }
    if piece==3:
        _,layer,pages,ending,tech=c
        bits=pages.split("/")
        if len(bits)!=2 or not all(x.isdigit() for x in bits) or layer not in ("I","II","III","IV") or tech!="Chờ nghe kiểm":
            raise ValueError(f"BBC {n}: invalid pages/layer/review marker.")
        music,lyric=map(int,bits)
        if (music,lyric) not in ((130,131),(132,133),(134,135)):
            raise ValueError(f"BBC {n}: invalid printed pages.")
        return {
            "number":n,"section":layer,
            "source_music_locator":f"Nhị Tấn tập II, chữ nhạc tr. {music}, câu {n:02d}",
            "source_lyric_locator":f"Nhị Tấn tập II, lời tr. {lyric}, câu {n:02d}",
            "printed_music_page":music,"printed_lyric_page":lyric,
            "ending_token":ending,"pair_index":None,
            "source_note":("Ký hiệu gạch cuối hàng chữ nhạc; chưa xác minh âm thanh, trường độ hoặc phách." if ending=="—" else None)
        }
    raise ValueError("Only V3.3 additions 02/03 supported.")


def validate_schema(schema: object) -> list[str]:
    if not isinstance(schema,dict):
        return ["V3.3 schema is not a JSON object."]
    issues=[]
    if schema.get("properties",{}).get("schema_version",{}).get("const")!="3.3.0-alpha.1":
        issues.append("V3.3 schema version mismatch.")
    for label,obj,req in [
        ("root",schema,ROOT_FIELDS),
        ("item",schema.get("$defs",{}).get("item",{}),ITEM_FIELDS),
        ("section",schema.get("$defs",{}).get("section",{}),SECTION_FIELDS),
        ("phrase",schema.get("$defs",{}).get("phrase",{}),PHRASE_FIELDS)
    ]:
        if not isinstance(obj,dict) or set(obj.get("required",[]))!=req or obj.get("additionalProperties") is not False:
            issues.append(f"V3.3 schema {label} missing fields/strictness.")
    if schema.get("properties",{}).get("rights_status",{}).get("const")!="unverified" or schema.get("properties",{}).get("performance_status",{}).get("const")!="pending":
        issues.append("Schema falsely approves rights/performance.")
    items=schema.get("properties",{}).get("items",{})
    if items.get("minItems")!=4 or items.get("maxItems")!=4:
        issues.append("Schema must keep exactly 4 source systems.")
    if schema.get("$defs",{}).get("phrase",{}).get("properties",{}).get("number",{}).get("maximum")!=44:
        issues.append("Schema must permit 44 as upper bound.")
    if schema.get("$defs",{}).get("item",{}).get("properties",{}).get("piece_id",{}).get("enum")!=[1,2,3,20]:
        issues.append("Schema must list only four explicitly reviewed sources.")
    return issues


def validate_v33(data: object, catalog: dict, root: Path=ROOT) -> list[str]:
    errors=[]
    try:
        previous=strict_load(root / "data/v3_2/phrase_index.json")
        errors+=validate_phrase_index(previous,catalog,root)
    except (OSError,ValueError,TypeError,KeyError) as exc:
        errors.append(f"V3.2 locked baseline unavailable: {exc}")
        return errors
    try:
        errors+=validate_schema(strict_load(root/"data/v3_3/schema.json"))
    except (OSError,ValueError,TypeError) as exc:
        errors.append(f"V3.3 schema unavailable: {exc}")
    if not isinstance(data,dict) or set(data)!=ROOT_FIELDS:
        return errors+["V3.3 root fields invalid."]
    if (data["schema_version"],data["started_on"],data["research_scope"])!=("3.3.0-alpha.1","2026-10-29","source_label_index_only"):
        errors.append("V3.3 version, date or purpose mismatch.")
    if data["performance_status"]!="pending" or data["rights_status"]!="unverified" or "0/20" not in data["reader_notice"]:
        errors.append("False rights/performance approval or missing warning.")
    if not isinstance(data["items"],list) or len(data["items"])!=4:
        return errors+["V3.3 requires 4 selected source variants, no automatic 20/20 graduation."]
    if [p.get("piece_id") for p in data["items"] if isinstance(p,dict)]!=[1,2,3,20]:
        return errors+["V3.3 variants must be exactly #01/#02/#03/#20."]
    cat={p["id"]:p for p in catalog["items"]}
    for item in data["items"]:
        if not isinstance(item,dict) or set(item)!=ITEM_FIELDS:
            errors.append("Unexpected or missing V3.3 item fields.")
            continue
        piece=item["piece_id"]
        vid,count,beats,register=SETTINGS[piece]
        if (item["slug"],item["title"],item["variant_id"],item["phrase_count"],item["beats_per_phrase"],item["source_register"])!=(
            cat[piece]["slug"],cat[piece]["title"],vid,count,beats,register
        ):
            errors.append(f"{piece}: source variant ID, slug, beats or count mismatch.")
        if not any(v["variant_id"]==vid and v["phrase_count"]==count and v["beats_per_phrase"]==beats for v in cat[piece]["variants"]):
            errors.append(f"{piece}: variant absent from 20-piece catalog.")
        url=urlsplit(item["source_url"])
        if url.scheme!="https" or not url.hostname or url.username or url.password:
            errors.append(f"{piece}: source HTTPS URL invalid.")
        if not isinstance(item["source_description"],str) or len(item["source_description"])<70:
            errors.append(f"{piece}: missing source/limitations description.")
        if not isinstance(item["phrases"],list) or len(item["phrases"])!=count:
            errors.append(f"{piece}: incorrect number of phrase rows.")
            continue
        if piece in (1,20):
            old=next(x for x in previous["items"] if x["piece_id"]==piece)
            if item!=old:
                errors.append(f"{piece}: V3.2 72 phrase baseline was altered.")
            continue
        if item["source_url"]!=NT_II:
            errors.append(f"{piece}: unexpected source edition; cannot silently mix books.")
        sections=LAYERS[piece]
        if item["sections"]!=[{"label":label,"start":lo,"end":hi} for label,lo,hi in sections]:
            errors.append(f"{piece}: V2 layer boundaries changed.")
        try:
            rows=parse_rows(root/register,count,7 if piece==2 else 5)
        except (OSError,ValueError) as exc:
            errors.append(f"{piece}: V2 ledger error: {exc}")
            continue
        for n,(phrase,row) in enumerate(zip(item["phrases"],rows),1):
            if not isinstance(phrase,dict) or set(phrase)!=PHRASE_FIELDS:
                errors.append(f"{piece} #{n}: fields missing/extra.")
                continue
            try:
                expected=candidate_phrase(piece,n,row)
            except (ValueError,TypeError) as exc:
                errors.append(f"{piece} #{n}: V2 row unacceptable: {exc}")
                continue
            if phrase!=expected:
                errors.append(f"{piece} #{n}: source row, printed page, ending or issue mismatch.")
        if piece==2:
            # Separate source declarations: 34 music / 32 printed lyrics. No fabricated lyrics.
            missing=[x["number"] for x in item["phrases"] if x["printed_lyric_page"] is None]
            if missing!=[33,34] or not all("DỊ BẢN" in item["phrases"][n-1]["source_note"] for n in (8,34)):
                errors.append("PLC must retain missing lyric pages 33/34 and conflicting endings 08/34.")
            if any(x["source_note"] and ("đã nghiệm thu" in x["source_note"].lower()) for x in item["phrases"]):
                errors.append("PLC wrongly claims a phrase has been approved.")
    if sum(len(x["phrases"]) for x in data["items"] if isinstance(x,dict) and isinstance(x.get("phrases"),list))!=150:
        errors.append("V3.3 published count must be exactly 32+34+44+40 = 150.")
    return errors


def main() -> int:
    parser=argparse.ArgumentParser(description="Validate 150 source-indexed labels from V2 without pretending they are music.")
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args()
    try:
        catalog=strict_load(CATALOG)
        data=strict_load(INDEX)
        errors=validate_catalog(catalog)+validate_v33(data,catalog)
    except (ValueError,OSError,TypeError) as exc:
        errors=[str(exc)]
    info={"status":"pass" if not errors else "fail","source_label_systems":4,"indexed_labels":150,"performances_approved":0,"commercial_enabled":False,"rights_to_audio_verified":False,"errors":errors}
    if args.json:
        print(json.dumps(info,ensure_ascii=False,indent=2))
    else:
        print("PASS: V3.3 150 labels in 4 source systems. No performance approval." if not errors else "\n".join(errors))
    return 0 if not errors else 1


if __name__=="__main__":
    raise SystemExit(main())
