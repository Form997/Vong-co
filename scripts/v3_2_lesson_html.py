# -*- coding: utf-8 -*-
"""Render accessible V3.2 source-locator lessons; no score/audio is copied."""
from __future__ import annotations

from html import escape
from urllib.parse import quote, urlsplit

BLOB = "https://github.com/Form997/Vong-co/blob/v3-development/"
LESSON_CSS = """
.lesson-intro{padding:15px 18px;background:#263245;border:1px solid #86724c;border-radius:12px;margin:15px 0;color:#f8e7c2}
.lesson-links{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}
.lesson-links a{padding:7px 11px;border:1px solid #627c87;border-radius:8px;font-weight:600;font-size:13px}
.lesson-group{margin:20px 0;padding-top:8px;border-top:1px solid var(--line)}
.lesson-group h3{color:var(--gold);font-size:20px}
.phrase-row{margin:9px 0;background:#0c2130;border:1px solid #3c556a;border-radius:12px;overflow:hidden}
.phrase-row:focus-within{border-color:var(--gold)}
.phrase-row summary{padding:12px 14px;cursor:pointer;font-size:14px;font-weight:700}
.phrase-row summary:hover{background:#1d384b}
.phrase-row .body{padding:3px 15px 16px;font-size:13px}
.phrase-row .body p{margin:7px 0;color:var(--dim)}
.phrase-row .body strong{color:var(--ink)}
.lesson-practice{border:1px solid #4b716e;padding:14px 17px;background:#0f2b31;border-radius:12px}
.lesson-empty{padding:17px 19px;border:1px dashed var(--line);border-radius:10px;color:var(--dim)}
@media print{.top,.button{display:none}.section,.phrase-row{break-inside:avoid}body{background:white;color:black}.muted{color:#444}}
@media(max-width:560px){.phrase-row summary{font-size:13px}}
"""


def html_text(value: object) -> str:
    return escape(str(value), quote=True)


def safe_url(value: str) -> str:
    u = urlsplit(value)
    if u.scheme != "https" or not u.hostname or u.username or u.password:
        raise ValueError("Nguồn học câu phải là URL HTTPS hợp lệ.")
    return html_text(value)


def render_lesson(piece: dict, lesson: dict | None) -> str:
    """Return static, keyboard-accessible HTML. Never embeds media or lyrics."""
    if lesson is None:
        return ('<section class="section" id="hoc-tung-cau" aria-labelledby="learn-title">'
                '<h2 id="learn-title">Học theo từng câu — đang chờ sổ nguồn</h2>'
                '<p class="lesson-empty">Bài này có bảng hoặc sổ câu V2 ở mức độ khác nhau, '
                'nhưng V3.2 chưa chuẩn hóa và kiểm lại từng hàng để đưa thành bài học. '
                'Không tự tạo nốt đờn, lời ca, ngón bấm, điểm song lang hoặc số trang.</p>'
                '<p>Đọc hồ sơ và biên bản nguồn V2 ở phần bên dưới để biết điều đã kiểm.</p>'
                '</section>')
    variant_id = html_text(lesson["variant_id"])
    source = safe_url(lesson["source_url"])
    register = safe_url(BLOB + quote(lesson["source_register"], safe="/-"))
    jump, sections = [], []
    for layer in lesson["sections"]:
        label = html_text(layer["label"])
        anchor = "lop-" + label.lower()
        jump.append(f'<a href="#{anchor}">Lớp {label}: {layer["start"]}–{layer["end"]}</a>')
        rows = []
        for phrase in lesson["phrases"]:
            n = phrase["number"]
            if not layer["start"] <= n <= layer["end"]:
                continue
            fields = [
                f'<p><strong>Nhạc:</strong> {html_text(phrase["source_music_locator"])}</p>',
                f'<p><strong>Lời:</strong> {html_text(phrase["source_lyric_locator"])}</p>',
            ]
            music, lyric = phrase["printed_music_page"], phrase["printed_lyric_page"]
            if music is not None:
                # V2 source records: printed p.332 = PDF page 38 (1-based).
                # Applies solely to the indexed digitized Nhị Tấn volume IV.
                mp, lp = music - 294, lyric - 294
                fields.append(
                    f'<p><strong>Trang bản in:</strong> nhạc {music}; lời {lyric}. '
                    f'<a href="{source}#page={mp}" target="_blank" rel="noopener noreferrer">'
                    f'Xem PDF trang nhạc {mp} ↗</a> · '
                    f'<a href="{source}#page={lp}" target="_blank" rel="noopener noreferrer">'
                    f'Xem PDF trang lời {lp} ↗</a></p>'
                )
            if phrase["ending_token"] is not None:
                fields.append(
                    f'<p><strong>Chữ kết ghi trong sổ V2:</strong> '
                    f'<code>{html_text(phrase["ending_token"])}</code>. '
                    'Giữ nguyên mặt chữ nguồn; không suy ra cao độ, trường độ hoặc MIDI.</p>'
                )
            if phrase["pair_index"] is not None:
                fields.append(
                    f'<p><strong>Nhóm kiểm đếm lẻ/chẵn:</strong> cặp {phrase["pair_index"]}. '
                    'Chưa có đối chứng cho vị trí chầu/mô hoặc dứt ngoại trong bản thu.</p>'
                )
            if phrase["source_note"] is not None:
                fields.append(
                    f'<p><strong>Ghi chú nguồn:</strong> {html_text(phrase["source_note"])}</p>'
                )
            fields.append(
                '<p><strong>Chưa kiểm:</strong> nhịp thực tấu, song lang, ngón đờn, '
                'đặt lời theo phách và đối chiếu bản ghi. Chưa được phép sao chép nhạc/lời.</p>'
            )
            rows.append(
                f'<details class="phrase-row" id="cau-{n:02d}">'
                f'<summary>Câu {n:02d} · Lớp {label} · xem nguồn & điểm cần kiểm</summary>'
                f'<div class="body">{"".join(fields)}</div></details>'
            )
        sections.append(
            f'<section class="lesson-group" id="{anchor}" aria-label="Lớp {label}">'
            f'<h3>Lớp {label} · Câu {layer["start"]:02d}–{layer["end"]:02d}</h3>'
            f'{"".join(rows)}</section>'
        )
    count = lesson["phrase_count"]
    return f"""<section class="section" id="hoc-tung-cau" aria-labelledby="learn-title">
<span class="eyebrow">V3.2 · Bài học từ sổ nguồn</span>
<h2 id="learn-title">Học từng câu theo đúng hệ {variant_id}</h2>
<p>Có <strong>{count}/{count} nhãn câu được rà ở V2</strong>; không phải
 {count} câu đã thẩm âm. Tên hệ nhịp và cách phân câu chỉ áp dụng cho
 <strong>phiên bản {variant_id}</strong>.</p>
<p class="muted">{html_text(lesson["source_description"])}</p>
<div class="lesson-intro"><strong>Không thay chứng cứ bằng phỏng đoán:</strong>
chưa có ký âm/toàn bộ lời/âm thanh được phép tái bản để phát lại.
Không tự đổi nhịp tư thành nhịp tám, không áp quy luật song lang chung.
Toàn bộ dự án hiện có 0/20 bài nghiệm thu diễn xướng.</div>
<nav class="lesson-links" aria-label="Nguồn và lớp">
<a href="{source}" target="_blank" rel="noopener noreferrer">Nguồn bài gốc ↗</a>
<a href="{register}" target="_blank" rel="noopener noreferrer">Sổ V2 từng câu ↗</a>
<a href="{safe_url(BLOB + 'docs/v3.2-quy-trinh-tham-dinh.md')}" target="_blank" rel="noopener noreferrer">Quy trình thẩm định ↗</a>
<a href="{safe_url(BLOB + 'docs/v3.2-phieu-thuc-hanh.md')}" target="_blank" rel="noopener noreferrer">Phiếu thực hành ↗</a>
{' '.join(jump)}
</nav>
<div class="lesson-practice" role="note">
<strong>Trình tự tự học gợi ý (chưa được nghệ nhân nghiệm thu):</strong>
<ol>
<li>Mở <em>đúng nguồn và đúng hệ {variant_id}</em>; tìm nhãn câu tại bản gốc.</li>
<li>Đối chiếu nhãn nhạc và nhãn lời theo lớp, ghi lại chỗ chưa rõ.</li>
<li>Chỉ tập theo nhịp/song lang và đặt lời khi có bản thu cùng hệ
hoặc người hướng dẫn chuyên môn kiểm phách.</li>
<li>Ghi nguồn, vị trí, ngày đối chiếu và người kiểm; không tự cấp chứng nhận.</li>
</ol></div>
{''.join(sections)}
<p class="muted">Dữ liệu từng câu được kiểm tự động với sổ V2 gốc.
Có thể gửi vấn đề qua GitHub Issues kèm số câu, trang và hệ bản.</p>
</section>"""
