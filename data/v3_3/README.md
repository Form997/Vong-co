# DỮ LIỆU V3.3 — CHỈ MỤC 150 NHÃN CÂU THEO BỐN NGUỒN V2

**Ngày khởi tạo:** 29/10/2026. **Phạm vi:** metadata về vị trí nhãn câu, trang in, lớp và ký hiệu cuối dòng **được sổ V2 ghi nhận**; chưa được xác nhận bằng thực tấu. **Không có tổng phổ, nhạc số MIDI, lời ca nguyên văn hoặc tệp audio**.

## Thành phần

- [`phrase_index.json`](phrase_index.json): **bốn hệ bài độc lập**, `LT-32-4` (32), `PLC-34-4` (34), `BBC-44-4` (44), `PC-40-8` (40), tổng **150 nhãn**.
- [`schema.json`](schema.json): cấu trúc dữ liệu và ràng buộc `pending`, `unverified`. Phải đọc đồng thời với trình kiểm Python; schema không tự chứng minh nội dung nguồn.
- [`scripts/v3_3_validate.py`](../../scripts/v3_3_validate.py): tạo lại giá trị dự kiến từ **từng hàng** trong sổ kiểm V2 và so sánh JSON V3.3 (không lấy JSON tự đối chiếu với chính nó); kiểm **72 vị trí lịch sử V3.2 không thay đổi**.
- [`tests/test_v3_3_phrases.py`](../../tests/test_v3_3_phrases.py): kiểm thử đối chứng các trường hợp sai mốc trang in, thiếu lời, sai biến thể, sai hệ, tự nghiệm thu và giả mạo quyền.

## Vị trí nguồn

| Mã | Nguồn kiểm thứ cấp trong kho | Vấn đề cần giữ |
|---|---|---|
| `LT-32-4` | [V2 #01](../../ban-to/01-luu-thuy-truong/v2-ra-soat-32-cau.md) | Chữ nguồn HO khác HÒ; không lấy 16/8 hoặc 32/8 để thay 32/4 |
| `PLC-34-4` | [V2 #02](../../ban-to/02-phu-luc-chan/v2-ra-soat-34-cau.md) | Nhạc 34, **lời Nhị Tấn chỉ 32**, câu 08/34 dị bản Văn Dần, tập II khác “Thủ” tập I |
| `BBC-44-4` | [V2 #03](../../ban-to/03-binh-ban-chan/v2-ra-soat-44-cau.md) | 44/4 khác hệ 22/8, ký hiệu cuối hàng không phải âm nhạc đã thẩm |
| `PC-40-8` | [V2 #20](../../ban-to/20-phung-cau/v2-ra-soat-40-cau.md) | Trang in 332–341 tập IV, chưa có chầu/mô, dứt ngoại và thực tấu kiểm đủ |

## Chính sách cập nhật

1. **Không sửa dữ liệu V3.2** để đưa bài mới. Mọi số câu trang nhạc phải truy được về một hàng V2 và một nguồn đã nêu.
2. `printed_lyric_page: null` nghĩa **không có căn cứ về trang lời trong bản đang kiểm**, không được thay bằng phỏng đoán.
3. Ký hiệu `(nghỉ)`, `—`, `HO`, `HÒ` giữ nguyên mặt chữ, **không chuyển trực tiếp thành nốt, trường độ, ký âm, song lang**.
4. Không chuyển trạng thái `pending`/ `unverified` sang đã chứng nhận hoặc tái bản khi chưa có giấy phép/biên bản.
5. CI xanh chỉ kiểm **tính nhất quán metadata với các sổ V2 đang lưu**, không thay kiểm PDF gốc, bản ghi có bản quyền hoặc nghệ nhân.

[Đọc kế hoạch V3.3](../../docs/v3.3-khoi-dong.md) · [Kiểm nguồn 20 bản Tổ](../../docs/v3.2-kiem-toan-20-ban.md).
