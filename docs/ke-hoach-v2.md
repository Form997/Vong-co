# KẾ HOẠCH V2 — TỪ HỒ SƠ NGUỒN ĐẾN GIÁO TRÌNH ĐỜN CA KIỂM ĐỊNH

**Khởi động:** 27/10/2026 · **Phạm vi:** 20 bản Tổ, 6 Bắc – 7 Lễ – 3 Nam – 4 Oán.

## Chốt V1 đúng nghĩa
- **ĐẠT V1 về phạm vi:** 20/20 thư mục, phân nhóm, hồ sơ nguồn sơ bộ, ghi tình trạng dị bản.
- **CHƯA ĐẠT về biểu diễn:** chưa xác minh 20/20 tổng phổ, toàn văn lời, nhịp/song lang/ngón và bản thu có phép. Các sổ kiểm hiện là checklist, không phải chứng nhận.
- Baseline: xem [kiểm toán V1](kiem-toan-v1-20-ban.md) và [danh mục 20 bản](20-ban-to.md). Không viết lại kết quả V1; sửa sai bằng errata có nguồn.

## Mục tiêu V2
Mỗi bài có **một phiên bản ký âm và một phiên bản lời nhất quán** với bản thu tham chiếu, có thư mục nguồn có provenance và phiếu kiểm định câu; nếu không có quyền sao chép thì chỉ đặt liên kết và chỉ mục, không tự đẩy PDF/MP3/ca từ lên kho.

### Hợp đồng dữ liệu cho mỗi câu
`work_id, variant_id, section_id, phrase_index, beat_unit, source_id, source_page, note_symbols, lyric_source_id, lyric_alignment_status, song_lang_status, ornament_status, audio_source_id, timecode_start, timecode_end, verifier, verification_date, rights_status, decision, review_note`.

Giá trị `decision`: `unverified` / `source_verified` / `music_checked` / `performance_verified`; **không mặc định đạt do tồn tại ô**. Nếu chưa có phép, `note_symbols` và `lyrics` chỉ là tham chiếu có quyền, không sao chép tác phẩm.

## Lộ trình làm theo cổng nghiệm thu
| Giai đoạn | Nội dung | Tiêu chí kết thúc |
|---|---|---|
| V2.0 – khóa hệ bản | 20 mã bài, tên và dị danh, nguồn bản chép, bản thu; gắn ID riêng cho Vắn/Trường, 60/61, 68/84, 67/68 | Không có bản trích bị coi là toàn bài; mọi biến thể có mã |
| V2.1 – ký âm | Chọn một bản chép được kiểm nguồn mỗi bài; giải mã chữ nhạc, trường độ, lớp/câu và đoạn chuyển | Từng câu có trang nguồn hoặc đánh dấu chưa có |
| V2.2 – lời ca | Chọn bản lời có tên tác giả, phân biệt xưa/mới, ghép âm tiết với câu/phách, chỗ lấy hơi | Có bằng chứng khớp hoặc để trạng thái chưa duyệt |
| V2.3 – biểu diễn | Gắn audio nghệ nhân với mốc thời gian câu, kiểm chữ kết, nhấn/rung, song lang, mô/chầu | Người kiểm có chuyên môn ký xác nhận, ghi lỗi khác biệt |
| V2.4 – xuất bản | 20 hồ sơ có chỉ mục tìm kiếm, bảng sai khác, bài tập, giấy phép, bản phát hành | Kiểm link, lỗi số câu/nhịp, quyền tác giả, không có placeholder giả đạt |

## Ưu tiên theo rủi ro, không theo thứ tự bài
1. **Bài 10 Long Đăng — điểm nghẽn đang mở:** truy tận trang ký âm 40 câu (*Nhị Tấn* tập V), đối chiếu bài lời *Bàng Quyên xuống núi* (Thái Thụy Phong) với chữ đờn, xác minh bản đờn Ba Tu; không nhầm Long Đăng Nhã nhạc Huế. [Nguồn và tồn đọng](../ban-to/10-long-dang/nguon-loi-ky-am-can-kiem.md).
2. **Bài 04 & 06 — chuẩn hóa hệ chính:** xác định Cổ Bản Trường/Vắn, Tây Thi Trường/Vắn đúng với hệ được cơ quan chuyên ngành liệt kê; lập ledger riêng, không đổi slug khi thiếu chuyển hướng.
3. **Bài 15 & 16 — sai khác lớn:** Nam Ai 68/84; Nam Đảo 67/68 và 52+15, đối chiếu bằng ký âm, không tự gộp.
4. **Bài 01 & 08 — phân nhịp/câu:** Lưu Thủy Trường 32/16; Ngũ Đối Thượng 61/60.
5. **Các bài còn lại:** đối chiếu lần lượt phần chưa kiểm, ưu tiên bài đã có bản chép cùng lời có tác giả; chưa tìm thì ghi thiếu.

## Điều kiện công nhận một bài đạt V2
- [ ] Có tên, phân loại và định danh **phiên bản**, không chỉ số thứ tự bài.
- [ ] Có tài liệu đầu nguồn (người chép/in, năm, trang, giấy phép hoặc giới hạn sử dụng).
- [ ] Đã so đủ **số câu** với bản chép và audio **cùng hệ**; không dùng nguồn bản trích 12/16/20 câu thay bản đầy đủ.
- [ ] Có lời ca **đúng phiên bản**, tác giả/năm nếu được chứng minh; chưa xác định ghi 'chưa rõ'.
- [ ] Đã kiểm điểm nhịp, song lang, chuyển lớp và kỹ thuật rao/ngón bằng chứng cứ, không gán giả.
- [ ] Có lịch sử hiệu đính, người duyệt, thời điểm kiểm và trạng thái quyền phát hành.
- [ ] Bài chưa đủ tiêu chí phải để **V2-DRAFT**. Chỉ đạt **V2-VERIFIED** khi tất cả tiêu chí được thỏa.

**Nguyên tắc quan trọng:** V2 là **nâng chuẩn bằng bằng chứng**, không phải tăng số trang hay gắn nhãn "hoàn chỉnh" cho tài liệu chưa đối chiếu.
