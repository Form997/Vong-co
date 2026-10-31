#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Four standalone, source-linked family index pages for the 20 Ban To.

This uses ONLY catalog metadata. No score, lyric, recording or PDF is copied.
"""
from __future__ import annotations

from html import escape
from string import Template
from urllib.parse import quote

FAMILIES = (
    ("sau-bac", "Sáu Bắc", 6, (1, 2, 3, 4, 5, 6), "Sáu bài thuộc nhóm Bắc trong danh mục nghiên cứu."),
    ("bay-le", "Bảy Lễ", 7, (7, 8, 9, 10, 11, 12, 13), "Bảy bài thuộc nhóm Lễ trong danh mục nghiên cứu."),
    ("ba-nam", "Ba Nam", 3, (14, 15, 16), "Ba bài thuộc nhóm Nam trong danh mục nghiên cứu."),
    ("bon-oan", "Bốn Oán", 4, (17, 18, 19, 20), "Bốn bài thuộc nhóm Oán trong danh mục nghiên cứu."),
)

FAMILY_STYLES = """
.family-intro{margin:19px 0 28px;font-size:15px;color:var(--dim)}
.family-menu{display:flex;flex-wrap:wrap;gap:9px;margin:16px 0 27px}
.family-menu a{padding:10px 17px;border:1px solid #aec6b5;border-radius:999px;background:#fffefb;text-decoration:none;font-size:13px;font-weight:750}
.family-menu a[aria-current="page"]{background:#123b30;color:#fff;border-color:#123b30}
.family-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.family-piece{border:1px solid var(--line);border-radius:16px;background:var(--surface);padding:24px;overflow-wrap:anywhere}
.family-piece .family-number{color:#856336;font:italic 27px Georgia,serif}
.family-piece h2{font-size:25px;margin:8px 0 14px}
.family-piece p{color:var(--dim);font-size:13px;line-height:1.8}
.family-piece a{font-size:13px;font-weight:750;margin-right:16px}
.family-piece .family-variants{font-size:12px;background:#edf2eb;padding:10px 12px;border-radius:9px}
.family-foot{margin-top:35px;font-size:13px}
@media(max-width:680px){.family-grid{grid-template-columns:1fr}.family-piece{padding:20px}.family-piece h2{font-size:23px}}
"""

PAGE = Template("""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="$DESCRIPTION">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#f6f4ee">
<link rel="canonical" href="$CANONICAL">
<title>$LABEL · $COUNT bản Tổ | HAI ĐẤT V3.5</title>
<style>$CSS</style>
</head>
<body>
<header class="top"><div class="container">
<a class="brand" href="../../web/v3/">HAI ĐẤT</a>
<nav aria-label="Điều hướng"><a href="../../web/v3/">← Danh mục đủ 20 bài</a></nav>
</div></header>
<main class="container">
<section class="detail-hero" aria-labelledby="group-title">
<span class="eyebrow">Đờn ca tài tử Nam Bộ · Nhóm $LABEL</span>
<h1 id="group-title">$LABEL</h1>
<p class="lead">$INTRO</p>
<div class="quick-links"><a href="#danh-muc-nhom">Xem $COUNT bản Tổ</a><a href="../../web/v3/">Về thư viện chính</a></div>
</section>
<div class="notice" role="note"><strong>Đang nghiên cứu.</strong> 20/20 hồ sơ kiểm nguồn đã mở, nhưng 0/20 bài được nghiệm thu diễn xướng. Không coi chỉ mục câu, nhịp hay dẫn nguồn là bản ghi âm hoặc ký âm đã được chứng nhận. Cần xác minh quyền sử dụng trước khi tái phát tư liệu.</div>
<nav class="family-menu" aria-label="Chuyển giữa bốn nhóm">$MENU</nav>
<section id="danh-muc-nhom" aria-labelledby="group-list-title">
<h2 id="group-list-title">Danh mục $COUNT bài nhóm $LABEL</h2>
<p class="family-intro">Tên bài và hệ bản được lấy trực tiếp từ danh mục dữ liệu V3.5; nhấn vào từng bài để đọc hệ nguồn và biên bản đối chiếu V2.</p>
<div class="family-grid">$CARDS</div>
</section>
<p class="family-foot">Thư viện cung cấp đường dẫn nghiên cứu, không phát âm thanh, không sao chép lời ca hoặc tổng phổ của bên thứ ba. <a href="../../web/v3/legal.html">Pháp lý và quyền sử dụng</a>.</p>
</main>
<footer><div class="container">HAI ĐẤT · 20 bản Tổ Nam Bộ · $LABEL · V3.5 · 0/20 nghiệm thu diễn xướng</div></footer>
</body></html>
""")


def page_for_family(slug: str, items: list[dict], base_url: str, repo_blob: str, css: str) -> str:
    record = next((f for f in FAMILIES if f[0] == slug), None)
    if record is None:
        raise ValueError("Nhóm không có trong danh mục.")
    _, label, count, ids, intro = record
    members = [item for item in items if item["family_label"] == label]
    if len(members) != count or tuple(i["id"] for i in members) != ids:
        raise ValueError("Danh mục nhóm không khớp 6/7/3/4 và số thứ tự bài.")
    menu = []
    for other_slug, other_label, *_ in FAMILIES:
        current = ' aria-current="page"' if other_slug == slug else ""
        menu.append(f'<a href="../{other_slug}/"{current}>{escape(other_label)}</a>')
    cards = []
    for item in members:
        title = escape(item["title"], quote=True)
        number = int(item["id"])
        piece_slug = quote(item["slug"], safe="-")
        review = repo_blob + quote(item["review_document"], safe="/-")
        variants = ", ".join(escape(v["label"], quote=True) for v in item["variants"])
        note = escape(item["research_note"], quote=True)
        cards.append(
            '<article class="family-piece">'
            f'<div class="family-number">{number:02d}</div>'
            f'<h2>{title}</h2>'
            f'<p class="family-variants"><strong>Hệ bản được ghi:</strong> {variants}</p>'
            f'<p>{note}</p>'
            f'<a href="../../bai/{piece_slug}/">Mở hồ sơ bài {number:02d} ↗</a>'
            f'<a href="{escape(review, quote=True)}" target="_blank" rel="noopener noreferrer">Biên bản nguồn V2 ↗</a>'
            '</article>'
        )
    return PAGE.substitute(
        DESCRIPTION=escape(f"{label}: {count} bản Tổ trong kho HAI ĐẤT V3.5, có dẫn nguồn và cảnh báo chưa nghiệm thu.", quote=True),
        CANONICAL=escape(base_url + "nhom/" + slug + "/", quote=True),
        LABEL=escape(label), COUNT=count, INTRO=escape(intro),
        CSS=css + FAMILY_STYLES, MENU="".join(menu), CARDS="".join(cards),
    )
