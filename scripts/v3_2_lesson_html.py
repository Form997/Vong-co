# -*- coding: utf-8 -*-
"""Render accessible V3.2 source-locator lessons; no score/audio is copied."""
from __future__ import annotations

from html import escape
from urllib.parse import quote, urlsplit

BLOB = "https://github.com/Form997/Vong-co/blob/v3-development/"
LESSON_CSS = """

/* HAI ĐẤT V3.2 • Source-first lesson cards, integrated heritage design */
.lesson-intro{padding:18px 21px;border-radius:13px;background:#fbf1dd;border:1px solid #e3d1a8;margin:19px 0;color:#685238;font-size:13px;line-height:1.8}
.lesson-intro strong{color:#644422}
.lesson-links{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:21px 0 28px}
.lesson-links a{display:inline-flex;align-items:center;min-height:36px;padding:8px 13px;background:#eff3ed;border:1px solid #d5e1d5;border-radius:100px;color:#285b49;text-decoration:none;font-weight:750;font-size:11px;line-height:1.4}
.lesson-links a:hover{background:#e1ece2;border-color:#b7cdbc}
.lesson-group{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px;margin:36px 0 25px;align-items:start}
.lesson-group h3{grid-column:1/-1;font:500 27px/1.25 Georgia,"Times New Roman",serif;color:#173a30;border-bottom:1px solid #d6e0d7;padding:0 0 14px;margin:0 0 5px;letter-spacing:-.02em}
.phrase-row{background:#f8f9f4;border:1px solid #dde6dc;border-radius:13px;overflow:hidden;margin:0;min-width:0;transition:border-color .18s,box-shadow .18s}
.phrase-row:hover{border-color:#afc8b5}
.phrase-row[open]{background:#fffefb;border-color:#8fb0a2;box-shadow:0 10px 26px rgba(27,62,48,.06)}
.phrase-row summary{position:relative;list-style:none;cursor:pointer;display:flex;align-items:center;padding:14px 42px 14px 16px;min-height:61px;font-weight:750;font-size:12px;color:#244d3d;line-height:1.5}
.phrase-row summary::-webkit-details-marker{display:none}
.phrase-row summary:after{content:"+";position:absolute;right:15px;top:50%;transform:translateY(-50%);font-size:23px;font-weight:300;color:#4f7965}
.phrase-row[open] summary:after{content:"−"}
.phrase-row:focus-within{outline:2px solid #bd985c;outline-offset:1px}
.phrase-row .body{padding:0 16px 17px;border-top:1px solid #e3eae0;font-size:12px;line-height:1.72;color:#586b60;overflow-wrap:anywhere}
.phrase-row .body p{margin:10px 0;color:#586b60}
.phrase-row .body strong{color:#234638}
.phrase-row .body a{font-weight:750;display:inline-block;margin-top:4px}
.phrase-row .body code{background:#eaf0e8;color:#204b3d;border-radius:5px;padding:3px 7px;font:700 12px ui-monospace,SFMono-Regular,monospace}
.lesson-practice{background:#edf3ea;border-radius:14px;border:1px solid #cbded0;padding:22px 25px;margin:17px 0;color:#29493b;font-size:13px}
.lesson-practice strong{font-weight:800;color:#1e4735}
.lesson-practice ol{padding-left:20px;margin:12px 0 0}
.lesson-practice li{margin:7px 0}
.lesson-empty{padding:19px 21px;border-radius:12px;background:#f9f1e4;border:1px dashed #dac6a6;color:#665844;font-size:13px;line-height:1.8}
@media(max-width:760px){.lesson-group{grid-template-columns:1fr}.lesson-group h3{font-size:24px}.phrase-row summary{font-size:13px}}
@media(max-width:560px){.lesson-intro{padding:16px}.lesson-practice{padding:17px}.lesson-links{gap:7px}.lesson-links a{font-size:11px}.lesson-group{margin-top:28px}}
@media print{.top,.button{display:none}.section,.phrase-row{break-inside:avoid}body{background:white;color:black}.muted{color:#555}.phrase-row[open]{box-shadow:none}}

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
                'nhưng V3.3 chưa chuẩn hóa và kiểm lại từng hàng để đưa thành bài học. '
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
                # Mapping print-page -> PDF-page was checked ONLY for Nhị Tấn IV, piece #20.
                # Do not apply this offset to volume II or turn absent lyric pages into numbers.
                if lesson["piece_id"] == 20:
                    if lyric is None:
                        raise ValueError("Phụng Cầu page pair unexpectedly incomplete.")
                    mp, lp = music - 294, lyric - 294
                    fields.append(
                        f'<p><strong>Trang bản in:</strong> nhạc {music}; lời {lyric}. '
                        f'<a href="{source}#page={mp}" target="_blank" rel="noopener noreferrer">'
                        f'Xem PDF trang nhạc {mp} ↗</a> · '
                        f'<a href="{source}#page={lp}" target="_blank" rel="noopener noreferrer">'
                        f'Xem PDF trang lời {lp} ↗</a></p>'
                    )
                else:
                    lyric_text = str(lyric) if lyric is not None else "KHÔNG CÓ trong trang lời của nguồn Nhị Tấn II"
                    fields.append(
                        f'<p><strong>Trang bản in (tập II):</strong> nhạc {music}; lời {html_text(lyric_text)}. '
                        f'<a href="{source}" target="_blank" rel="noopener noreferrer">'
                        'Đối chiếu trực tiếp PDF theo số trang IN; chưa xác minh trang PDF 1-based ↗</a></p>'
                    )
            if phrase["ending_token"] is not None:
                ending_label = ("Ký hiệu cuối dòng chữ nhạc in tại nguồn V2" if
                                lesson["piece_id"] in (2, 3) else "Chữ kết ghi trong sổ V2")
                fields.append(
                    f'<p><strong>{ending_label}:</strong> '
                    f'<code>{html_text(phrase["ending_token"])}</code>. '
                    'Giữ nguyên mặt chữ nguồn; không suy ra cao độ, trường độ, điểm song lang hay MIDI.</p>'
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
<span class="eyebrow">V3.3 · Bài học từ sổ nguồn</span>
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
