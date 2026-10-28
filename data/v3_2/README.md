# DỮ LIỆU V3.2 — CHỈ MỤC TỪNG CÂU CÓ NGUỒN, KHÔNG PHẢI TỔNG PHỔ

**Bắt đầu:** 28/10/2026 · **Định dạng:** JSON UTF‑8 · **Phạm vi đã kiểm:** hai hệ bản riêng biệt, **72 nhãn câu** trên văn bản V2, **0 nhãn được nghiệm thu diễn xướng**.

- [`phrase_index.json`](phrase_index.json): nguồn xác định của hệ, phạm vi lớp, vị trí nhãn câu nhạc/lời, trang in nếu đã kiểm, ghi chú ở sổ V2, chỉ mục cặp chỉ dùng cho rà soát.
- [`schema.json`](schema.json): cấu trúc JSON Schema draft 2020-12, cấm các trường không khai báo, giữ `rights_status=unverified`, `performance_status=pending`.
- [`scripts/v3_2_validate.py`](../../scripts/v3_2_validate.py): trình kiểm định **có đối chiếu trực tiếp lại cả 72 hàng trong sổ V2** và so đúng `variant_id`, `phrase_count`, `beats_per_phrase` với [catalog V3](../v3/catalog.json). Không có sự phụ thuộc package Python ngoài chuẩn.

## Hai hệ có thể tra theo câu

| Bài | Hệ nguồn | Sổ kiểm V2 | Phạm vi chỉ mục | Lớp |
|---|---|---|---|---|
| [01 – Lưu Thủy Trường](../../ban-to/01-luu-thuy-truong/README.md) | `LT-32-4`: **32 câu nhịp tư** từ trang Văn Dần | [Sổ 32 câu](../../ban-to/01-luu-thuy-truong/v2-ra-soat-32-cau.md) | **32 nhãn nhạc + 32 nhãn lời tương ứng theo số**, chữ kết ngắn theo nguồn; **không có số trang in** | I 1–8; II 9–16; III 17–24; IV 25–32 |
| [20 – Phụng Cầu Hoàng Duyên](../../ban-to/20-phung-cau/README.md) | `PC-40-8`: **40 câu nhịp tám** từ bản Nhị Tấn tập IV | [Sổ 40 câu](../../ban-to/20-phung-cau/v2-ra-soat-40-cau.md) | **40 nhãn nhạc/lời và trang in chính xác**: nhạc 332/334/336/338/340, lời 333/335/337/339/341; cặp 1–20 chỉ là phép nhóm | I 1–18; II 19–26; III 27–40 |

### Chỉ dẫn đọc số liệu

- **72** là số **vị trí câu trong hai hệ bản**, không phải 72 giai điệu được ghi âm, ký âm lại hoặc xác nhận chuyên môn.
- Cách viết `HO` ở câu đầu Lưu Thủy Trường được **giữ nguyên**, không tự thay thành `HÒ`; chữ kết không cho biết cao độ tuyệt đối hoặc mọi nét luyến láy.
- Lưu Thủy Trường còn các hệ `LT-16-8` và `LT-32-8` **khác nguồn**. Hai hệ này hiện **không được lập sổ V3.2**, không đổi nhịp tư sang nhịp tám bằng phép tính.
- Tại Phụng Cầu, trang PDF **38–47** tương ứng các trang in **332–341** trong tài liệu đã kiểm ở V2; bộ chỉ mục không sao chép ảnh PDF, bản ký âm hay lời. Nhãn cặp 1–20 **không phải 20 điểm chầu/mô đã xác minh**.
- **18/20 bài còn lại:** V3.2 chưa có sổ nhãn từng câu được chọn và đối chiếu đúng hệ. Giao diện thông báo trạng thái chưa sẵn sàng, không tạo đủ 20 “bài học” giả.

## Cơ chế kiểm nguồn tránh dữ liệu AI bịa

Từ thư mục gốc repository:

```bash
python scripts/v3_validate.py --json
python scripts/v3_2_validate.py --json
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/v3_build_site.py --out _site
```

Trình kiểm sẽ **từ chối**: thiếu hàng 1–32 hoặc 1–40, số trùng, sai lớp, trang nhạc/lời không đúng sổ V2, sai chữ kết nguồn, sai chỉ mục cặp, đổi hệ 32/4 ↔ 16/8, URL nguồn khác catalog, hoặc ai đó gắn thêm `audio_url`, `melody`, `lesson_certified` chưa có quy chế quyền/thẩm định.

**Hiệu lực nguồn:** mô tả trang/hệ dựa trên **sổ V2 đã ghi**, không đồng nghĩa trợ lý kiểm lại từng ảnh PDF hoặc bản thu trong lần nâng V3.2. Khi biên bản V2 thay đổi, phải kiểm lại dữ liệu và nhận giải trình trước khi cập nhật.

## Công bố, giấy phép và trách nhiệm

Tất cả vật liệu là **metadata nghiên cứu** có liên kết nguồn. `rights_status=unverified` không chứng minh dữ liệu nào được phép dùng thương mại, huấn luyện AI hoặc tái bản ký âm/ca từ/bản thu. Không nhúng player, sample, MIDI hoặc chép toàn bộ lời ca vào website khi chưa có giấy phép thích hợp.

**Tiếp tục:** [Phương pháp nghiệm thu nguồn – âm nhạc](../../docs/v3.2-quy-trinh-tham-dinh.md) · [Mẫu phiếu tự học/đối chiếu](../../docs/v3.2-phieu-thuc-hanh.md) · [Nhật ký V3.2](../../docs/v3.2-khoi-dong.md).
