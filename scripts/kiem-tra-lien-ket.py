#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm tra liên kết nội bộ trong README/tài liệu; không truy cập web.

Examples:
  python scripts/kiem-tra-lien-ket.py
  python scripts/kiem-tra-lien-ket.py README.md docs/tong-hop-phat-hien-v2.md
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILES = (
    "README.md",
    "README.en.md",
    "CONTRIBUTING.md",
    "docs/tong-hop-phat-hien-v2.md",
)

# Only check local Markdown links (not images), and HTML anchors.
MD_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+[^)]+)?\)")
HTML_LINK = re.compile(r"<a\b[^>]*\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)


def broken_links(file_path: Path) -> tuple[int, list[str]]:
    body = file_path.read_text(encoding="utf-8")
    hrefs = MD_LINK.findall(body) + HTML_LINK.findall(body)
    bad: list[str] = []
    checked = 0

    for href in hrefs:
        if href.startswith("#"):
            continue
        u = urlsplit(href)
        if u.scheme or u.netloc or href.startswith("//"):
            continue
        raw = unquote(u.path).strip()
        if not raw:
            continue
        checked += 1
        dest = (file_path.parent / raw).resolve()
        if not dest.is_relative_to(ROOT) or not dest.exists():
            bad.append(f"{file_path.relative_to(ROOT)}: {href}")
    return checked, bad


def main(paths: tuple[str, ...] | list[str] | None = None) -> int:
    selected = paths if paths is not None else sys.argv[1:] or DEFAULT_FILES
    total = 0
    errors: list[str] = []

    for relative in selected:
        source = (ROOT / relative).resolve()
        if not source.is_relative_to(ROOT) or not source.is_file():
            errors.append(f"Không tìm thấy tài liệu: {relative}")
            continue
        count, bad = broken_links(source)
        total += count
        errors.extend(bad)

    if errors:
        for problem in errors:
            print("LỖI LIÊN KẾT: " + problem, file=sys.stderr)
        print(f"FAIL: {len(errors)} lỗi; {total} link nội bộ đã kiểm.", file=sys.stderr)
        return 1
    print(f"PASS: {total} liên kết nội bộ hợp lệ trong {len(selected)} tài liệu.")
    print("Lưu ý: Chưa kiểm link ngoài Internet và anchor nội dung.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
