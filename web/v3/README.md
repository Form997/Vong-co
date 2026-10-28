# HAI ĐẤT V3.2 — Thư viện tra cứu và HỌC THEO NHÃN CÂU CÓ NGUỒN

**Ngày bắt đầu V3.2:** 28/10/2026.  
**Nhánh làm việc:** [`v3.2-development`](https://github.com/Form997/Vong-co/tree/v3.2-development).  
**Website công khai hiện tại:** [HAI ĐẤT V3.1](https://form997.github.io/Vong-co/), đã được [GitHub Pages xác nhận triển khai](https://github.com/Form997/Vong-co/actions/runs/40689588576). **V3.2 chưa thay thế website đó cho tới khi Pull Request được kiểm và merge.**

## Điều mới trong V3.2

Website vẫn có **20 trang riêng / 30 hệ bản thuộc danh mục V3**, đồng thời bổ sung:

- **72 vị trí câu có nguồn:** 32 vị trí của **Lưu Thủy Trường – LT-32-4** và 40 vị trí của **Phụng Cầu Hoàng Duyên – PC-40-8**. Đây là **nhãn câu V2**, không phải 72 câu đờn đã được kiểm nghe.
- Khối **“Học từng câu”** ngay ở trang bài: nút mở từng số câu có lớp, nguồn nhạc/lời, chữ kết ngắn nếu có, trang PDF nếu đã đối chứng, những chỗ cần người học hỏi nghệ nhân.
- Lọc bài theo trạng thái **đã chuyển thành chỉ mục học V3.2 (2)** hoặc **chưa chuyển (18)**. **18 bản đều có sổ hoặc bảng V2 ở nhiều mức**, không có nghĩa “mất nguồn”: [Kiểm toán từng bài](../../docs/v3.2-kiem-toan-20-ban.md).
- [JSON 72 câu](../../data/v3_2/phrase_index.json), [JSON Schema](../../data/v3_2/schema.json) và [trình kiểm dữ liệu theo sổ V2](../../scripts/v3_2_validate.py), không cần API bên ngoài.
- Link đến [quy chế thẩm định](../../docs/v3.2-quy-trinh-tham-dinh.md) và [phiếu thực hành](../../docs/v3.2-phieu-thuc-hanh.md). Mọi trang ghi **0/20 nghiệm thu diễn xướng**, chưa có bản ghi có quyền tái phát.

## Xem thử V3.2 từ GitHub (chưa cần cập nhật website)

Trên máy có Python 3.11+, mở nhánh `v3.2-development`. Chạy **tại thư mục gốc repository**:

```bash
python scripts/v3_validate.py --json
python scripts/v3_2_validate.py --json
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/v3_build_site.py --out _site
python -m http.server 8000 --directory _site
```

Mở:

```text
http://localhost:8000/web/v3/
http://localhost:8000/bai/01-luu-thuy-truong/#hoc-tung-cau
http://localhost:8000/bai/20-phung-cau/#hoc-tung-cau
http://localhost:8000/bai/18-phung-hoang/#hoc-tung-cau
```

Dùng **GitHub Codespaces** cũng được: mở port 8000 ở tab **Ports**. Trang bài #18 cố ý **không hiển thị 48 câu giả** khi sổ V2 còn ghi “Chưa xác minh”. Với lần build sau, thư mục `_site` cần rỗng; công cụ sẽ từ chối đè lên output cũ để tránh đăng nhầm tệp.

**Không mở riêng file HTML qua `file://`**: JavaScript tải JSON bằng HTTP, và trình duyệt có thể chặn đường dẫn file cục bộ.

## Dữ liệu kiểm nguồn được trình bày thế nào?

**Câu Lưu Thủy Trường:** hệ `LT-32-4` có 4 lớp × 8 câu. Website giữ mặt chữ ngắn `HO` và `HÒ` khác nhau theo sổ V2. Không lấy chữ kết để suy ra nốt Tây phương, độ dài hoặc cách đánh ngón. Không trộn 16 câu nhịp tám từ nguồn Nguyễn Vĩnh Bảo.

**Câu Phụng Cầu:** hệ `PC-40-8` có lớp I **18 câu**, II **8 câu**, III **14 câu**. Nhạc tr.**332–340**, lời tr.**333–341** ở tập IV Nhị Tấn, đoạn cuối câu 40 tiếp ngay sang bài khác. Các link mở PDF đúng trang nếu trình duyệt hỗ trợ. Cặp 1–20 chỉ là **nhãn để rà**, không chứng nhận chầu/mô hay nhịp 7/8.

**18 bài chưa vào module V3.2:** [tổng hợp 20 sổ V2](../../docs/v3.2-kiem-toan-20-ban.md). Nhiều bảng có số câu và nguồn nhưng cần parser riêng từng cấu trúc (ví dụ 61/60, 84/80, 67/68). Không tạo số trang hoặc nốt nhạc không có bằng chứng.

## Kiểm thử, phát hành và quyền

- Bộ Python phải kiểm đúng toàn bộ 72 hàng V2 và chặn tự gắn `audio_url`, nốt, `lesson_certified`, đổi quyền hoặc đổi hệ nhịp.
- Chromium thực tế kiểm: 20 bản/30 hệ, tìm không dấu, lọc 2/18, 32+40 nhãn câu, trang PDF, khả năng xem điện thoại 390 px và không có lỗi JavaScript.
- Gói GitHub Pages chỉ được phép chứa **HTML tra cứu, JSON/schema và robots/sitemap**, không chép nguồn PDF/MP3/ký âm hoặc thư mục V2 lên web. 20 trang bài vẫn giữ nguyên địa chỉ từ V3.1.
- **Chỉ merge vào `v3-development` sau khi CI đạt và được rà soát**. Website công khai chỉ cập nhật khi [workflow Pages](../../.github/workflows/pages-v3.yml) có **Deploy Success**.

**Đã mở hồ sơ nguồn 20/20, nhưng nghiệm thu biểu diễn vẫn 0/20.** Địa chỉ web, README hoặc điểm kiểm thử phần mềm không phải chứng nhận của cơ quan chuyên môn.

[Nhật ký V3.2](../../docs/v3.2-khoi-dong.md) · [Chính sách source-first](../../docs/v3.2-quy-trinh-tham-dinh.md) · [Danh mục nguồn V2](../../docs/nguon-tham-khao.md).
