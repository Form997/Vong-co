#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal offline HTML renderer for six evidence-scoped national law summaries."""
from __future__ import annotations
from html import escape
from urllib.parse import quote

COUNTRIES = {
    "US": ("Mỹ", "Hoa Kỳ", "my"),
    "RU": ("Nga", "Liên bang Nga", "nga"),
    "CN": ("Trung Quốc", "Trung Quốc", "trung-quoc"),
    "AU": ("Úc", "Úc", "uc"),
    "JP": ("Nhật Bản", "Nhật Bản", "nhat-ban"),
    "KR": ("Hàn Quốc", "Hàn Quốc", "han-quoc"),
}
STATUS = {
    "in_force": "Có hiệu lực theo mốc đã ghi",
    "phased": "Hiệu lực từng phần — cần kiểm mốc",
    "promulgated-pending": "Đã công bố — chưa được coi là có hiệu lực đầy đủ",
    "official-guidance": "Hướng dẫn cơ quan — không phải luật",
}
CATEGORY = {
    "privacy": "Quyền riêng tư", "privacy-state": "Dữ liệu theo bang",
    "privacy-children": "Dữ liệu trẻ em", "privacy-amendment": "Sửa đổi riêng tư",
    "cybersecurity": "An ninh mạng", "cyber-information": "Thông tin và bảo vệ hệ thống",
    "cybercrime": "Xâm nhập hệ thống", "data-security": "An toàn dữ liệu",
    "crossborder-data": "Chuyển dữ liệu xuyên biên giới", "critical-infrastructure": "Hạ tầng trọng yếu",
    "data-breach": "Thông báo vi phạm dữ liệu",
    "copyright": "Bản quyền và quyền liên quan", "copyright-amendment": "Sửa đổi bản quyền",
    "ecommerce": "Thương mại điện tử", "consumer-commerce": "Người tiêu dùng",
    "ai-system": "Sản phẩm trí tuệ nhân tạo",
}

CSS = """
:root{color-scheme:light;--paper:#f6f4ee;--forest:#143c31;--gold:#d0ac72;--jade:#246651;--ink:#16342b;--muted:#5b7165;--line:#dbe5d8}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.75 system-ui,-apple-system,"Segoe UI",sans-serif}a{color:var(--jade);overflow-wrap:anywhere;text-underline-offset:4px}a:focus-visible{outline:3px solid #b99059;outline-offset:3px}.wrap{max-width:1080px;margin:auto;padding:0 25px}
header{background:#fffdf9;border-bottom:1px solid var(--line);padding:15px 0}header .wrap{display:flex;flex-wrap:wrap;gap:15px;justify-content:space-between;align-items:center}header a{font-size:13px;font-weight:750;text-decoration:none}header .brand{font-size:18px;letter-spacing:2px;color:var(--forest)}
.hero{background:linear-gradient(115deg,#103b30,#214d3c);color:#fff;border-radius:19px;padding:45px clamp(22px,5vw,55px);margin:32px 0 23px}.eyebrow{font-weight:750;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#ead1a6}h1,h2{font-family:Georgia,"Times New Roman",serif;font-weight:500;line-height:1.24;letter-spacing:-.03em}h1{font-size:clamp(35px,5vw,54px);margin:13px 0}h2{font-size:28px;margin:14px 0}.hero p{color:#e0ede5;max-width:790px}.notice{border:1px solid #e4d1a8;background:#fff2d8;color:#59462a;border-radius:12px;padding:15px 19px;margin:20px 0}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-bottom:20px}.card{background:#fffefa;border:1px solid var(--line);border-radius:14px;padding:23px;min-width:0}.card h2{margin:7px 0 15px;font-size:24px}.card p,.card li{font-size:13px;color:var(--muted)}.card li{margin:9px 0}.full{grid-column:1/-1}.sources{display:grid;gap:14px}.source{border:1px solid var(--line);border-radius:12px;background:#f9faf5;padding:18px}.source .tag{font-size:10px;font-weight:800;color:#2b6752;letter-spacing:1px;text-transform:uppercase}.source h3{font-size:16px;line-height:1.55;margin:8px 0}.source p{margin:6px 0;font-size:12px;color:#52675b}.source a{font-size:12px;font-weight:750}.source .status{display:inline-block;border-radius:50px;background:#e9f0e8;color:#315f4f;padding:3px 10px;font-size:11px;font-weight:750}.source .status.pending{background:#fff0d8;color:#795c31}.resource{margin-top:23px;font-size:13px;color:var(--muted)}.resource a{font-weight:700}
footer{background:#11392f;color:#e1eade;padding:29px 0;font-size:12px}footer a{color:#e9ce9c}
@media(max-width:700px){.wrap{padding:0 16px}.grid{grid-template-columns:1fr}.full{grid-column:1}.hero{padding:31px 22px;margin:16px 0}h1{font-size:36px}.card{padding:19px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""


def render_country_page(code: str, catalog: dict) -> str:
    if code not in COUNTRIES:
        raise ValueError("Country not in reviewed legal set.")
    short, full, slug = COUNTRIES[code]
    entries = [x for x in catalog["sources"] if x["jurisdiction"] == code]
    if not entries:
        raise ValueError(f"No legal evidence for {code}.")
    cards = []
    for x in entries:
        pending = x["status"] != "in_force"
        when = x["effective_on"] or "Kiểm mốc riêng / hướng dẫn"
        cards.append(f"""
        <article class="source" id="{escape(x['id'],quote=True)}">
          <span class="tag">{escape(CATEGORY.get(x['theme'],x['theme']))} · {escape(x['id'])}</span>
          <h3>{escape(x['title'])}</h3>
          <span class="status{' pending' if pending else ''}">{escape(STATUS[x['status']])}</span>
          <p><strong>Mốc hiệu lực:</strong> {escape(when)}</p>
          <p><strong>Điều kiện áp dụng:</strong> {escape(x['scope_note'])}</p>
          <p><strong>Phiên bản/giới hạn:</strong> {escape(x['version_note'])}</p>
          <a href="{escape(x['official_url'],quote=True)}" target="_blank" rel="noopener noreferrer">Đọc văn bản gốc tại cơ quan nhà nước ↗</a>
        </article>""")
    md_link = f"https://github.com/Form997/Vong-co/blob/v3-development/docs/phap-ly-quoc-te/{quote(slug)}.md"
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f6f4ee">
<meta name="description" content="Hồ sơ pháp luật {escape(full,quote=True)} áp dụng có điều kiện cho HAI ĐẤT, kiểm đến 29/10/2026.">
<link rel="canonical" href="https://form997.github.io/Vong-co/web/v3/quoc-gia/{slug}.html">
<title>Pháp luật {escape(short)} · HAI ĐẤT V3.2</title>
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap"><a class="brand" href="../">HAI ĐẤT</a><nav aria-label="Điều hướng"><a href="../legal.html">Pháp lý 6 quốc gia</a> · <a href="../">Thư viện bản Tổ</a></nav></div></header>
<main class="wrap">
<section class="hero" aria-labelledby="title">
<div class="eyebrow">Hồ sơ pháp lý quốc tế · {code} · Cập nhật 29/10/2026</div>
<h1 id="title">{escape(full)} — nguồn luật chính thức</h1>
<p>{len(entries)} văn bản hoặc hướng dẫn cơ quan đã được phân loại theo trạng thái và điều kiện áp dụng. Đây là tài liệu kiểm nguồn phục vụ dự án nghiên cứu HAI ĐẤT; không phải tư vấn luật cá nhân hoặc chứng nhận tuân thủ tại {escape(full)}.</p>
</section>
<div class="notice" role="note"><strong>Chú ý:</strong> HAI ĐẤT hiện là website tra cứu phi thương mại, không đăng nhập hoặc thu tiền. Việc truy cập được website từ {escape(full)} không đủ để kết luận tất cả luật địa phương cùng áp dụng. Không sao chép ký âm, ca từ hay bản ghi chưa được cấp phép. <strong>Thương mại = NO-GO</strong> cho tới khi đánh giá riêng.</div>
<div class="grid">
<section class="card"><h2>Đang sử dụng</h2><p>Thư viện nghiên cứu 20 bản Tổ; 72 nhãn câu thuộc hai hệ có đối chứng với sổ V2. Không có trình phát nhạc, thanh toán, dữ liệu người học hoặc voice clone. Hoạt động phi thương mại không tự cho quyền sử dụng tác phẩm của chủ sở hữu khác.</p></section>
<section class="card"><h2>Nếu mở thương mại</h2><p>Phải kiểm luật của quốc gia này theo loại dịch vụ, tài khoản, dữ liệu cá nhân, trẻ em, quyền bản ghi/người biểu diễn, hoạt động AI, bảo vệ người tiêu dùng và nơi lưu dữ liệu. Không coi bản dịch hay tài liệu nghiên cứu là giấy phép kinh doanh.</p></section>
<section class="card full" aria-labelledby="sources"><h2 id="sources">Nguồn luật và giải thích phạm vi</h2><div class="sources">{''.join(cards)}</div>
<p class="resource"><strong>Tài liệu chuyên sâu:</strong> <a href="{escape(md_link,quote=True)}" target="_blank" rel="noopener noreferrer">Mở hồ sơ tiếng Việt đầy đủ tại GitHub ↗</a>. Các mốc chưa xác minh chính xác được để trống, nguồn hướng dẫn không coi là đạo luật, các bản sửa có hiệu lực tương lai không tính là đang áp dụng.</p></section>
</div></main>
<footer><div class="wrap">HAI ĐẤT · Bảo tồn và nghiên cứu có nguồn · <a href="../legal.html">Pháp lý &amp; quyền riêng tư</a> · Không có chứng nhận pháp lý hay nghiệm thu biểu diễn (0/20).</div></footer>
</body></html>"""
