#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAI ĐẤT V3.1: generate the strictly allowlisted GitHub Pages website.

The 20 standalone research pages are generated from V3 catalog metadata only.
No copyrighted score, lyric, audio, PDF, archive, or private GitHub file is
included. Run from anywhere: python scripts/v3_build_site.py --out _site
"""
from __future__ import annotations

import argparse
from html import escape
import json
import shutil
from pathlib import Path
from urllib.parse import quote, urlsplit
from xml.sax.saxutils import escape as xml_escape

from v3_validate import ROOT, CATALOG, validate_catalog, strict_load

BASE_URL = "https://form997.github.io/Vong-co/"
REPO_BLOB = "https://github.com/Form997/Vong-co/blob/v3-development/"
ALLOWLIST = (
    ("web/v3/index.html", "web/v3/index.html"),
    ("data/v3/catalog.json", "data/v3/catalog.json"),
    ("data/v3/schema.json", "data/v3/schema.json"),
)
BASE_FILES = ("index.html", ".nojekyll", "robots.txt", "sitemap.xml")

LANDING = """<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="index,follow">
  <meta name="description" content="HAI ĐẤT — Tra cứu 20 bản Tổ Đờn ca tài tử Nam Bộ, bảo tồn nguồn gốc và dị bản.">
  <meta http-equiv="refresh" content="0;url=web/v3/">
  <title>HAI ĐẤT V3.1 · Thư viện 20 bản Tổ</title>
  <link rel="canonical" href="https://form997.github.io/Vong-co/web/v3/">
</head>
<body><main>
  <h1>HAI ĐẤT · Thư viện 20 bản Tổ</h1>
  <p>Đang mở trang tra cứu. <a href="web/v3/">Bấm vào đây nếu trình duyệt không tự chuyển trang.</a></p>
</main></body></html>
"""
ROBOTS = "User-agent: *\nAllow: /\nSitemap: " + BASE_URL + "sitemap.xml\n"
EVIDENCE_LABELS = {
    "source_indexed": "Đã định vị ở hồ sơ V2 — chưa nghiệm thu biểu diễn",
    "source_reported": "Nguồn thuật lại — cần đối chiếu trực tiếp",
    "derived_unverified": "Ánh xạ đề xuất — chưa kiểm chứng độc lập",
}
CSS = """
:root{color-scheme:dark;--bg:#0b1826;--card:#162c40;--line:#385166;--ink:#f8f3e9;--dim:#b7c8d1;--gold:#ebc687;--mint:#92dbd1}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:radial-gradient(ellipse at 80% 0%,#254257 0,transparent 50%),var(--bg);color:var(--ink);font:16px/1.68 system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--mint);text-underline-offset:3px;overflow-wrap:anywhere}
a:focus-visible{outline:3px solid var(--gold);outline-offset:4px}
.container{max-width:940px;padding:0 22px;margin:0 auto}
.top{background:#0e2031;border-bottom:1px solid var(--line);padding:17px 0}
.top .container{display:flex;gap:14px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.brand{font-size:18px;letter-spacing:2px;font-weight:800;text-decoration:none;color:var(--gold)}
.top nav{display:flex;gap:16px;flex-wrap:wrap}
.top nav a{font-size:13px;color:var(--dim)}
main{padding-top:45px;padding-bottom:65px}
.eyebrow{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);font-weight:700}
h1,h2{font-family:Georgia,"Times New Roman",serif;font-weight:500;line-height:1.25}
h1{font-size:clamp(35px,6vw,56px);margin:12px 0}
h2{font-size:28px;margin:15px 0 14px}
.lead{max-width:780px;color:var(--dim);font-size:16px}
.notice{border:1px solid #8f774c;border-radius:13px;background:#2b2c34;padding:16px 19px;margin:22px 0;color:#fff0cb}
.section{margin:22px 0;padding:22px;background:var(--card);border:1px solid var(--line);border-radius:17px}
.muted{color:var(--dim)}
.tag{display:inline-flex;padding:5px 11px;border-radius:25px;border:1px solid #6b7e83;font-size:12px;color:#d0f2ec;margin:4px 5px 4px 0}
.variants{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:14px}
.variant{background:#0f2234;border:1px solid var(--line);border-radius:12px;padding:18px}
.variant h3{font-size:17px;margin:0 0 8px}
.variant p{font-size:13px;color:var(--dim);margin:8px 0}
.metrics{font-size:13px;color:var(--gold);font-weight:650}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin:19px 0}
.button{display:inline-block;border:1px solid #60758a;padding:10px 15px;border-radius:10px;font-weight:650;text-decoration:none;color:var(--ink)}
.button.main{color:#172331;background:var(--gold);border-color:var(--gold)}
footer{border-top:1px solid var(--line);padding:26px 0;color:var(--dim);font-size:13px}
@media(max-width:560px){.container{padding:0 15px}main{padding-top:28px}.section{padding:16px}h2{font-size:25px}}
"""


def html_text(value: object) -> str:
    return escape(str(value), quote=True)


def safe_https(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("URL tham khảo không phải HTTPS hợp lệ.")
    return html_text(url)


def piece_url(piece: dict) -> str:
    return BASE_URL + "bai/" + quote(piece["slug"], safe="-") + "/"


def page_for_piece(piece: dict, previous_piece: dict | None, next_piece: dict | None) -> str:
    title = html_text(piece["title"])
    family = html_text(piece["family_label"])
    aliases = ", ".join(html_text(x) for x in piece["aliases"]) or "Không ghi nhận trong danh mục V3"
    prefix = "../../"  # from /Vong-co/bai/<slug>/ back to /Vong-co/
    slug = quote(piece["slug"], safe="-")
    url = safe_https(piece_url(piece))
    review = safe_https(REPO_BLOB + quote(piece["review_document"],safe="/-"))
    readme = safe_https(REPO_BLOB + quote(piece["readme_document"],safe="/-"))
    disclaimer = (
        "Hồ sơ chỉ dùng metadata V2 có dẫn nguồn. 20/20 hồ sơ được mở; "
        "0/20 bài nghiệm thu diễn xướng. Nhịp/số câu thuộc từng hệ nguồn, "
        "không phải tổng phổ được chứng nhận. Không mặc định có quyền tái bản nhạc và lời."
    )
    variant_cards = []
    for v in piece["variants"]:
        count = int(v["phrase_count"])
        beat = "Chưa rõ hệ nhịp" if v["beats_per_phrase"] is None else "Nhịp " + str(v["beats_per_phrase"])
        name = html_text(v["label"])
        status = html_text(EVIDENCE_LABELS[v["evidence_status"]])
        note = html_text(v["qualification"])
        source = safe_https(v["reference_url"])
        variant_cards.append(
            f'<article class="variant"><h3>{name}</h3>'
            f'<div class="metrics">{count} câu · {html_text(beat)}</div>'
            f'<p><strong>Mức chứng cứ:</strong> {status}</p>'
            f'<p>{note}</p>'
            f'<a href="{source}" target="_blank" rel="noopener noreferrer">Đọc nguồn được dẫn ↗</a></article>'
        )
    nav_links = ['<a href="../../web/v3/">← Tất cả 20 bài</a>']
    if previous_piece:
        nav_links.append('<a rel="prev" href="../' + quote(previous_piece["slug"],safe="-") + '/">← Bài '
                         + str(previous_piece["id"]).zfill(2) + '</a>')
    if next_piece:
        nav_links.append('<a rel="next" href="../' + quote(next_piece["slug"],safe="-") + '/">Bài '
                         + str(next_piece["id"]).zfill(2) + ' →</a>')
    # All external/metadata values are escaped, not interpreted as HTML.
    description = html_text(
        f"{piece['title']} — {piece['family_label']} · {len(piece['variants'])} hệ tham chiếu. "
        "Tra cứu nguồn và sai biệt; chưa nghiệm thu diễn xướng."
    )
    return f"""<!doctype html>
<html lang="vi"><head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{description}">
  <meta name="robots" content="index,follow">
  <meta name="theme-color" content="#0b1826">
  <link rel="canonical" href="{url}">
  <title>{title} · Bản Tổ số {piece['id']:02d} | HAI ĐẤT V3.1</title>
  <style>{CSS}</style>
</head><body>
<header class="top"><div class="container">
 <a class="brand" href="../../web/v3/" aria-label="HAI ĐẤT — trở về danh mục">HAI ĐẤT</a>
 <nav aria-label="Điều hướng">{' '.join(nav_links)}</nav>
</div></header>
<main class="container">
 <span class="eyebrow">{family} · Bản Tổ số {piece['id']:02d} · V3.1</span>
 <h1>{title}</h1>
 <p class="lead">Một bản Tổ có thể có nhiều hệ câu, lớp và dị bản. Trang này giúp lần theo
 nguồn và ghi rõ điều chưa được người thực hành thẩm định.</p>
 <div class="notice" role="note"><strong>Chưa nghiệm thu diễn xướng.</strong> {html_text(disclaimer)}</div>
 <section class="section" aria-labelledby="overview">
   <h2 id="overview">Thông tin bản Tổ</h2>
   <span class="tag">{family}</span>
   <span class="tag">{len(piece['variants'])} hệ tham chiếu</span>
   <span class="tag">Nguồn: hồ sơ V2 đã mở</span>
   <p><strong>Tên khác:</strong> {aliases}</p>
   <p class="muted">{html_text(piece['research_note'])}</p>
 </section>
 <section class="section" aria-labelledby="variants">
   <h2 id="variants">Các hệ câu / dị bản theo nguồn</h2>
   <p class="muted">Số câu, nhịp và nhận xét chỉ có ý nghĩa trong hệ tài liệu được dẫn.
   Một số nguồn được thuật lại hoặc đề xuất ánh xạ, chưa có đối chứng trực tiếp.</p>
   <div class="variants">{''.join(variant_cards)}</div>
 </section>
 <section class="section" aria-labelledby="records">
   <h2 id="records">Đọc hồ sơ và đối chiếu chứng cứ</h2>
   <div class="actions">
    <a class="button main" href="{review}" target="_blank" rel="noopener noreferrer">Biên bản rà nguồn V2 ↗</a>
    <a class="button" href="{readme}" target="_blank" rel="noopener noreferrer">Hồ sơ bài đầy đủ ↗</a>
    <a class="button" href="{prefix}web/v3/#bai-{piece['id']:02d}">Xem trong danh mục ↗</a>
   </div>
   <p class="muted">Nguồn được trích dẫn không tự cấp quyền sao chép, trình diễn, phân phối
   audio hay dùng nguyên văn cho AI. Không khẳng định tài liệu này được UNESCO, nghệ nhân hoặc
   Viện Âm nhạc chứng nhận.</p>
 </section>
 <nav class="actions" aria-label="Chuyển bài">{' '.join(nav_links)}</nav>
</main>
<footer><div class="container">HAI ĐẤT · Gìn giữ tiếng đờn, không đánh mất xuất xứ.
 · Phiên bản V3.1 (bản xem trước nghiên cứu) · Ngày bắt đầu 28/10/2026</div></footer>
</body></html>
"""


def generate_sitemap(pieces: list[dict]) -> str:
    urls = [BASE_URL, BASE_URL + "web/v3/"] + [piece_url(p) for p in pieces]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += '  <url><loc>' + xml_escape(url) + '</loc></url>\n'
    return xml + '</urlset>\n'


def build(output: Path) -> dict[str, object]:
    data = strict_load(CATALOG)
    errors = validate_catalog(data)
    if errors:
        raise ValueError("Không xuất bản metadata không hợp lệ: " + "; ".join(errors[:5]))
    target, source = output.resolve(), ROOT.resolve()
    if target == source or source.is_relative_to(target):
        raise ValueError("Thư mục đích trùng/chứa cả repository: không an toàn.")
    target.mkdir(parents=True, exist_ok=True)
    if any(target.iterdir()):
        raise ValueError("Thư mục đích phải rỗng để tránh lộ dữ liệu cũ.")

    for origin, destination in ALLOWLIST:
        src, dest = ROOT / origin, target / destination
        if not src.is_file():
            raise FileNotFoundError(f"Không có file cần xuất bản: {origin}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    (target / "index.html").write_text(LANDING, encoding="utf-8")
    (target / ".nojekyll").write_text("", encoding="utf-8")
    (target / "robots.txt").write_text(ROBOTS, encoding="utf-8")

    pieces = data["items"]
    for i, p in enumerate(pieces):
        page = target / "bai" / p["slug"] / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(page_for_piece(p, pieces[i-1] if i else None,
                                  pieces[i+1] if i+1 < len(pieces) else None),
                        encoding="utf-8")
    (target / "sitemap.xml").write_text(generate_sitemap(pieces), encoding="utf-8")

    files = sorted(p.relative_to(target).as_posix()
                   for p in target.rglob("*") if p.is_file())
    expected = sorted([destination for _, destination in ALLOWLIST]
                      + list(BASE_FILES)
                      + [f"bai/{p['slug']}/index.html" for p in pieces])
    if files != expected:
        raise RuntimeError("Tệp xuất bản khác allowlist; từ chối: " + repr(files))
    return {
        "status": "pass",
        "published_files": files,
        "file_count": len(files),
        "total_bytes": sum(p.stat().st_size for p in target.rglob("*") if p.is_file()),
        "pieces": len(pieces),
        "variants": sum(len(x["variants"]) for x in pieces),
        "detail_pages": len(pieces),
        "includes_rights_restricted_media": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Đóng gói an toàn trang tra cứu V3.1")
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
