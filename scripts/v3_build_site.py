#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a minimal, public-safe HAI ĐẤT V3 static Pages site.

Only approved public metadata and the web viewer are published.
The source Markdown/audio/scores, repository internals and test files are
never copied to the deployment directory.

Examples:
    python scripts/v3_build_site.py --out _site
    python -m http.server 8000 --directory _site
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from v3_validate import ROOT, CATALOG, validate_catalog, strict_load

ALLOWLIST = (
    ("web/v3/index.html", "web/v3/index.html"),
    ("data/v3/catalog.json", "data/v3/catalog.json"),
    ("data/v3/schema.json", "data/v3/schema.json"),
)
LANDING = """<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="index,follow">
  <meta name="description" content="HAI ĐẤT — Tra cứu 20 bản Tổ Đờn ca tài tử Nam Bộ, bảo tồn nguồn gốc và dị bản.">
  <meta http-equiv="refresh" content="0;url=web/v3/">
  <title>HAI ĐẤT V3 · Thư viện 20 bản Tổ</title>
  <link rel="canonical" href="https://form997.github.io/Vong-co/web/v3/">
</head>
<body>
  <main>
    <h1>HAI ĐẤT · Thư viện 20 bản Tổ</h1>
    <p>Đang mở trang tra cứu. <a href="web/v3/">Nhấn vào đây nếu trình duyệt không tự chuyển trang.</a></p>
  </main>
</body>
</html>
"""
ROBOTS = """User-agent: *
Allow: /
Sitemap: https://form997.github.io/Vong-co/sitemap.xml
"""
SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://form997.github.io/Vong-co/</loc></url>
  <url><loc>https://form997.github.io/Vong-co/web/v3/</loc></url>
</urlset>
"""


def build(output: Path) -> dict[str, object]:
    data = strict_load(CATALOG)
    errs = validate_catalog(data)
    if errs:
        raise ValueError("Không xuất bản metadata không hợp lệ: " + "; ".join(errs[:5]))
    target = output.resolve()
    source = ROOT.resolve()
    if target == source or source.is_relative_to(target):
        raise ValueError("Thư mục đích trùng/chứa cả repository: không an toàn.")
    target.mkdir(parents=True, exist_ok=True)
    if any(target.iterdir()):
        # Fail rather than accidentally publishing stale files.
        raise ValueError("Thư mục đích phải rỗng để tránh lộ dữ liệu cũ.")
    for origin, destination in ALLOWLIST:
        src = ROOT / origin
        dest = target / destination
        if not src.is_file():
            raise FileNotFoundError(f"Không có file cần xuất bản: {origin}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    (target / "index.html").write_text(LANDING, encoding="utf-8")
    (target / ".nojekyll").write_text("", encoding="utf-8")
    (target / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (target / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
    # Verify no unexpected files exist in the deployment artifact.
    relative_files = sorted(p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file())
    expected = sorted([d for _, d in ALLOWLIST] + ["index.html", ".nojekyll", "robots.txt", "sitemap.xml"])
    if relative_files != expected:
        raise RuntimeError("Tập tin xuất bản khác allowlist: " + repr(relative_files))
    return {
        "status": "pass",
        "published_files": relative_files,
        "file_count": len(relative_files),
        "total_bytes": sum(p.stat().st_size for p in target.rglob("*") if p.is_file()),
        "pieces": len(data["items"]),
        "variants": sum(len(x["variants"]) for x in data["items"]),
        "includes_rights_restricted_media": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Tạo gói xuất bản web V3 có kiểm dữ liệu")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = build(args.out)
    except (ValueError, RuntimeError, OSError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
