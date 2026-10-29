#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAI ĐẤT V3.2: generate the strictly allowlisted GitHub Pages website.

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
from v3_2_validate import INDEX as LESSON_INDEX, validate_phrase_index
from v3_2_lesson_html import render_lesson, LESSON_CSS
from v3_2_legal_validate import validate_all as validate_legal_publication

BASE_URL = "https://form997.github.io/Vong-co/"
REPO_BLOB = "https://github.com/Form997/Vong-co/blob/v3-development/"
ALLOWLIST = (
    ("web/v3/index.html", "web/v3/index.html"),
    ("web/v3/legal.html", "web/v3/legal.html"),
    ("data/v3/catalog.json", "data/v3/catalog.json"),
    ("data/v3/schema.json", "data/v3/schema.json"),
    ("data/v3_2/phrase_index.json", "data/v3_2/phrase_index.json"),
    ("data/v3_2/schema.json", "data/v3_2/schema.json"),
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
  <title>HAI ĐẤT V3.2 · Thư viện 20 bản Tổ</title>
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

:root{color-scheme:light;--paper:#f6f4ee;--surface:#fffefb;--card:#fffefb;--line:#d9e0d8;--ink:#18312a;--dim:#5e7065;--jade:#286954;--gold:#b28a54;--mint:#245c4d;--forest:#123b30;--soft:#f0f2ea;--shadow:0 17px 44px rgba(15,48,33,.055)}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:96px}
body{margin:0;min-width:280px;background:var(--paper);color:var(--ink);font:16px/1.75 system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--jade);text-underline-offset:4px;overflow-wrap:anywhere}
a:hover{color:#163d32}
:focus-visible{outline:3px solid #c59854;outline-offset:3px}
::selection{background:#296655;color:white}
.container{max-width:1100px;padding:0 29px;margin:auto}
.top{background:rgba(255,254,251,.97);border-bottom:1px solid var(--line);padding:19px 0;position:sticky;top:0;z-index:20;backdrop-filter:blur(13px)}
.top .container{display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.brand{font-weight:800;letter-spacing:3px;text-decoration:none;color:var(--forest);font-size:17px;line-height:1.4}
.brand:before{content:"Đ";display:inline-grid;place-items:center;width:32px;height:32px;border:1px solid #9fac9e;border-radius:50%;margin-right:12px;font:500 22px Georgia,serif;color:var(--forest)}
.top nav{display:flex;gap:15px;flex-wrap:wrap;align-items:center}
.top nav a{font-size:12px;text-decoration:none;color:var(--jade);font-weight:750}
.top nav a:hover{text-decoration:underline}
main{padding-top:29px;padding-bottom:85px}
.detail-hero{position:relative;overflow:hidden;border-radius:23px;color:#f8faf3;background:linear-gradient(110deg,#113e34,#0d302a);padding:57px 6% 54px;margin-bottom:27px;isolation:isolate}
.detail-hero:before{content:"";position:absolute;right:-90px;top:-130px;width:460px;height:460px;border:1px solid rgba(240,211,167,.32);border-radius:50%;box-shadow:0 0 0 45px rgba(232,205,159,.045),0 0 0 100px rgba(232,205,159,.05);z-index:-1}
.detail-hero:after{content:"";position:absolute;right:94px;top:55px;width:195px;height:195px;border:1px solid rgba(235,205,159,.18);border-radius:50%;z-index:-1}
.eyebrow{font-size:11px;letter-spacing:2.3px;text-transform:uppercase;color:var(--gold);font-weight:800}
.detail-hero .eyebrow{color:#e6c690}
h1,h2{font-family:Georgia,"Times New Roman",serif;font-weight:500;letter-spacing:-.03em;line-height:1.2}
h1{font-size:clamp(40px,5.7vw,67px);margin:15px 0 17px;max-width:780px}
h2{font-size:clamp(27px,3vw,35px);margin:8px 0 18px}
.lead{max-width:720px;color:#d4e4d9;font-size:15px;line-height:1.85}
.quick-links{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}
.quick-links a{display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid rgba(232,244,233,.4);border-radius:100px;color:#f4f8f3;text-decoration:none;padding:9px 16px;font-size:12px;font-weight:750}
.quick-links a:first-child{color:#1a3e31;background:#ebd2a1;border-color:#ebd2a1}
.quick-links a:hover{border-color:#e9d0a0}
.notice{display:flex;gap:8px;align-items:start;border:1px solid #e5d6b6;border-radius:13px;background:#faf0df;padding:17px 21px;margin:24px 0;color:#695940;font-size:13px}
.notice strong{color:#614323;white-space:nowrap}
.section{margin:24px 0;padding:30px 32px;background:var(--surface);border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow)}
.section>h2:before{content:"";display:block;width:38px;height:3px;border-radius:3px;background:#b89b73;margin-bottom:19px}
.section>p{line-height:1.8}
.muted{color:var(--dim)}
.tag{display:inline-flex;border-radius:100px;background:#eaf2e9;color:#2c5b46;border:1px solid #cfdfcf;padding:6px 12px;font-size:12px;font-weight:700;margin:4px 6px 4px 0}
.variants{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,310px),1fr));gap:13px}
.variant{border-radius:14px;background:#f6f8f2;border:1px solid #e0e7dd;padding:21px;overflow-wrap:anywhere}
.variant h3{font:750 17px/1.45 system-ui,sans-serif;margin:0 0 12px}
.variant p{margin:10px 0;color:var(--dim);font-size:13px}
.variant a{font-size:13px;font-weight:750}
.metrics{font-size:13px;color:var(--jade);font-weight:800}
.actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:21px 0 0}
.button{display:inline-flex;padding:11px 16px;font-size:12px;font-weight:800;border:1px solid #afc0b6;border-radius:100px;text-decoration:none;color:var(--forest)}
.button.main{background:var(--forest);color:#fff;border-color:var(--forest)}
.button:hover{background:#eef3ed;color:var(--forest)}
.button.main:hover{background:#29594b;color:#fff}
footer{background:#12352c;color:#c8dacf;padding:32px 0;font-size:12px}
footer .container{max-width:1100px}
@media(max-width:700px){
 .container{padding:0 16px}.top{padding:14px 0}.top .container{gap:8px}.top nav{gap:9px}
 .top nav a{font-size:11px}.brand{font-size:14px;letter-spacing:2px}.brand:before{width:27px;height:27px;font-size:18px;margin-right:8px}
 main{padding-top:16px}.detail-hero{border-radius:15px;padding:38px 24px}
 .detail-hero:before{width:260px;height:260px;right:-155px}
 h1{font-size:clamp(35px,9vw,47px)}.lead{font-size:14px}
 .notice{display:block;padding:14px 16px;font-size:12px}.notice strong{display:block}
 .section{padding:23px 20px;border-radius:15px}
 .variants{grid-template-columns:1fr}.variant{padding:18px}
}
@media(max-width:560px){.container{padding:0 15px}.section{padding:22px 18px}h2{font-size:27px}.detail-hero{padding:33px 19px}.top nav a:nth-child(3){display:none}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation:none!important;transition:none!important}}

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


def page_for_piece(piece: dict, previous_piece: dict | None, next_piece: dict | None,
                   lesson: dict | None = None) -> str:
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
  <meta name="theme-color" content="#f6f4ee">
  <link rel="canonical" href="{url}">
  <title>{title} · Bản Tổ số {piece['id']:02d} | HAI ĐẤT V3.2</title>
  <style>{CSS}{LESSON_CSS}</style>
</head><body>
<header class="top"><div class="container">
 <a class="brand" href="../../web/v3/" aria-label="HAI ĐẤT — trở về danh mục">HAI ĐẤT</a>
 <nav aria-label="Điều hướng">{' '.join(nav_links)}</nav>
</div></header>
<main class="container">
 <section class="detail-hero" aria-label="Giới thiệu tác phẩm">
 <span class="eyebrow">{family} · Bản Tổ số {piece['id']:02d} · V3.2</span>
 <h1>{title}</h1>
 <p class="lead">Một bản Tổ có thể có nhiều hệ câu, lớp và dị bản. Trang này giúp lần theo
 nguồn và ghi rõ điều chưa được người thực hành thẩm định.</p>
 <div class="quick-links"><a href="#hoc-tung-cau">Học từng câu theo nguồn ↗</a><a href="#variants">Đọc các hệ bản</a><a href="#records">Hồ sơ chứng cứ</a></div>
 </section>
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
 {render_lesson(piece, lesson)}
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
 · V3.2 · Thư viện di sản âm nhạc · Không thay thế chứng nhận chuyên môn
 · <a href="../../web/v3/legal.html">Pháp lý, quyền riêng tư và an ninh mạng</a></div></footer>
</body></html>
"""


def generate_sitemap(pieces: list[dict]) -> str:
    urls = [BASE_URL, BASE_URL + "web/v3/", BASE_URL + "web/v3/legal.html"] + [piece_url(p) for p in pieces]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += '  <url><loc>' + xml_escape(url) + '</loc></url>\n'
    return xml + '</urlset>\n'


def build(output: Path) -> dict[str, object]:
    data = strict_load(CATALOG)
    lesson_data = strict_load(LESSON_INDEX)
    errors = validate_catalog(data) + validate_phrase_index(lesson_data, data) + validate_legal_publication()
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
    lesson_by_piece = {item["piece_id"]: item for item in lesson_data["items"]}
    for i, p in enumerate(pieces):
        page = target / "bai" / p["slug"] / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(page_for_piece(p, pieces[i-1] if i else None,
                                  pieces[i+1] if i+1 < len(pieces) else None,
                                  lesson_by_piece.get(p["id"])),
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
        "indexed_lesson_pieces": len(lesson_by_piece),
        "indexed_lesson_phrases": sum(len(i["phrases"]) for i in lesson_data["items"]),
        "includes_rights_restricted_media": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Đóng gói an toàn trang tra cứu V3.2")
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
