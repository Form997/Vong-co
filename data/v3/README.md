# HAI ĐẤT V3 — Danh mục dữ liệu có cấu trúc

**Tình trạng:** `3.0.0-alpha.1` · **Bắt đầu 28/10/2026** · **20/20** hồ sơ V2 được liên kết · **0/20** bản được nghiệm thu diễn xướng.

## Mở dữ liệu

- [`catalog.json`](catalog.json) — danh mục máy đọc (UTF-8, JSON), gồm **20 bản Tổ, 30 hệ bản/dị bản được quản lý**.
- [`schema.json`](schema.json) — bản thiết kế JSON Schema Draft 2020-12.
- [`scripts/v3_validate.py`](../../scripts/v3_validate.py) — chương trình kiểm định bằng Python 3.11, chỉ dùng thư viện chuẩn.
- [Giao diện tra cứu tiếng Việt](../../web/v3/README.md).

## Cấu trúc từng bản Tổ

| Trường | Ý nghĩa |
|---|---|
| `id`, `slug`, `title`, `family` | Chỉ mục bài 01–20 trong hệ dự án, nhóm Bắc/Lễ/Nam/Oán |
| `aliases` | Tên gọi khác; không tự suy các tên là cùng tác phẩm nếu chưa có bằng chứng |
| `review_document`, `readme_document` | Đường dẫn nội bộ sang biên bản/hồ sơ gốc V2 |
| `review_status` | `source_review_open`: **đã mở hồ sơ kiểm nguồn**, không phải đã duyệt biểu diễn |
| `performance_status` | `pending`: chưa nghiệm thu diễn xướng (toàn bộ V3 alpha) |
| `rights_status` | `unverified`: chưa có quyền mặc định sao chép nhạc, ca từ hoặc âm thanh |
| `variants[].phrase_count` | Số câu **của hệ bản tương ứng**, không phải số câu “chuẩn” áp dụng cho mọi nguồn |
| `variants[].beats_per_phrase` | Nhịp tư (`4`) / nhịp tám (`8`) / chưa rõ (`null`), **theo hệ tham chiếu** |
| `variants[].evidence_status` | `source_indexed`, `source_reported` hoặc `derived_unverified` |
| `variants[].reference_url` | URL tư liệu được biên bản V2 sử dụng, **không** hàm ý đã đọc bản thu hoặc cấp phép |
| `variants[].qualification`, `research_note` | Những điểm cần cảnh báo, sai biệt hoặc chưa đủ chứng cứ |

### Ba mức chứng cứ không được nhập nhằng

- **`source_indexed`**: tài liệu/số câu được định vị hoặc đối chiếu ở hồ sơ V2; *không phải* nghiệm thu ký âm–phách–ngón hay diễn xướng.
- **`source_reported`**: thông tin một nguồn được hồ sơ V2 thuật lại; cần kiểm chứng sâu hơn bằng bản gốc/bản thu.
- **`derived_unverified`**: cách ánh xạ hoặc hệ suy luận hiện chưa được xác nhận độc lập.

Ví dụ: **Nam Ai** có hệ 84 vị trí (4 chuyển + 80 lòng đánh số lại) khác cách mô tả 68 câu. **Đảo Ngũ Cung** có 67 vị trí Nhị Tấn (4+48+15), trong khi nguồn khác mô tả 68 (4+48+16). **Phụng Hoàng** số 18 chưa có 48 nhãn ký âm được rà trực tiếp; **không được gắn chứng nhận** chỉ vì danh mục ghi 48.

## Thử kiểm tra (không cần cài thư viện bên ngoài)

```bash
python scripts/v3_validate.py
python scripts/v3_validate.py --json
python -m unittest discover -s tests -p "test_*.py" -v
```

Chạy tại thư mục gốc của repository. Lệnh đầu chỉ xác thực **cấu trúc, trạng thái kiểm định và liên kết hồ sơ gốc**, không kiểm được đúng giai điệu cổ nhạc, quyền tác giả hoặc nghe bản thu.

## Quy tắc đóng góp dữ liệu

1. Trước khi thêm hệ bản, đọc đúng [biên bản V2](../../docs/ke-hoach-v2.md) và đưa URL tư liệu cụ thể.
2. Nếu chưa rõ số câu/nhịp, không bịa: tách hệ tham chiếu hoặc dùng `null` (nhịp), ghi `qualification`.
3. Không đặt `performance_status="approved"` hoặc `rights_status="cleared"` theo suy đoán.
4. Không đưa ký âm, nguyên lời ca, bản ghi MP3 hoặc PDF bên thứ ba vào JSON khi chưa có quyền.
5. Khi dữ liệu thay đổi, chạy **kiểm thử** và cập nhật **Nhật ký thế hệ V** bằng số đo Git SHA mới.

**Đây là bản dữ liệu nghiên cứu thử nghiệm, chưa công bố như một chuẩn học thuật chính thức.**
