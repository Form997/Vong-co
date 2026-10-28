#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thống kê dung lượng phiên bản từ GitHub, KHÔNG tính ZIP, .git hay lịch sử.

Ví dụ:
    python scripts/thong-ke-dung-luong.py --refs v1-frozen v2-development
    python scripts/thong-ke-dung-luong.py --refs v3-development --json

Dùng API /git/trees/<ref>?recursive=1. Đơn vị KiB=1.024 byte, MiB=1.048.576 byte.
Kết quả chỉ là snapshot của nhánh/commit tại thời điểm gọi.
"""
import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


def human_size(size: int) -> str:
    if size < 1024:
        return f"{size} byte ({size * 8} bit)"
    units = ("KiB", "MiB", "GiB", "TiB")
    amount = float(size)
    for unit in units:
        amount /= 1024.0
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.2f} {unit}"
    raise AssertionError("Unreachable")


def get_snapshot(repository: str, ref: str) -> dict:
    owner, name = repository.split("/", 1)
    endpoint = (
        "https://api.github.com/repos/"
        f"{quote(owner, safe='')}/{quote(name, safe='')}/git/trees/"
        f"{quote(ref, safe='')}?recursive=1"
    )
    req = Request(endpoint, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "Hai-Dat-Version-Size-Reporter/1.0",
    })
    with urlopen(req, timeout=25) as response:
        result = json.load(response)
    if result.get("truncated"):
        raise RuntimeError(
            f"GitHub cắt ngắn cây {ref}; KHÔNG được báo dung lượng thiếu."
        )
    blobs = [node for node in result["tree"] if node.get("type") == "blob"]
    if any(not isinstance(node.get("size"), int) for node in blobs):
        raise RuntimeError("Thiếu kích thước tệp; không thể tính chính xác.")
    total = sum(node["size"] for node in blobs)
    return {
        "repository": repository,
        "ref": ref,
        "tree_sha": result["sha"],
        "files": len(blobs),
        "bytes": total,
        "human": human_size(total),
        "kB_decimal": round(total / 1000, 2),
        "KiB_binary": round(total / 1024, 2),
        "measurement": "Tong kich thuoc blob trong Git tree, KHONG phai ZIP",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Thống kê dung lượng các thế hệ HAI ĐẤT")
    parser.add_argument("--repo", default="Form997/Vong-co")
    parser.add_argument("--refs", nargs="+", default=["v1-frozen", "v2-development"])
    parser.add_argument("--json", action="store_true", help="In JSON thay bảng Markdown")
    args = parser.parse_args()

    if args.repo.count("/") != 1 or not all(args.repo.split("/")):
        parser.error("--repo cần dạng owner/repository")
    try:
        snapshots = [get_snapshot(args.repo, ref) for ref in args.refs]
    except (HTTPError, URLError, ValueError, RuntimeError, KeyError) as exc:
        print(f"Lỗi lấy dữ liệu GitHub: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(snapshots, ensure_ascii=False, indent=2))
    else:
        print("| Phiên bản/ref | Số tệp | Dung lượng | Byte (chính xác) | Tree SHA |")
        print("|---|---:|---:|---:|---|")
        for x in snapshots:
            print(f"| `{x['ref']}` | {x['files']} | "
                  f"{x['human']} | {x['bytes']:,} | `{x['tree_sha'][:12]}` |")
        print("\n**Lưu ý:** Đo blob Git chưa nén, không phải dung lượng ZIP/.git.")
        print("Ngày bắt đầu một phiên bản cần ghi bằng chứng commit riêng,")
        print("không tự suy diễn ngày bắt đầu công việc ngoài GitHub.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
