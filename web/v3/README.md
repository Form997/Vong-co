# HAI ĐẤT V3.2 — Thư viện tra cứu và HỌC THEO NHÃN CÂU CÓ NGUỒN

**Ngày bắt đầu V3.2:** 28/10/2026.  
**Nhánh làm việc:** [`v3.2-development`](https://github.com/Form997/Vong-co/tree/v3.2-development).  
**Website công khai hiện tại:** [HAI ĐẤT V3.2](https://form997.github.io/Vong-co/); [PR #8 đã merge](https://github.com/Form997/Vong-co/pull/8) và [GitHub Pages Deploy thành công](https://github.com/Form997/Vong-co/actions/runs/40694415309) ngày 28/10/2026.

## Điều mới trong V3.2

Website vẫn có **20 trang riêng / 30 hệ bản thuộc danh mục V3**, đồng thời bổ sung:

- **72 vị trí câu có nguồn:** 32 vị trí của **Lưu Thủy Trường – LT-32-4** và 40 vị trí của **Phụng Cầu Hoàng Duyên – PC-40-8**. Đây là **nhãn câu V2**, không phải 72 câu đờn đã được kiểm nghe.
- Khối **“Học từng câu”** ngay ở trang bài: nút mở từng số câu có lớp, nguồn nhạc/lời, chữ kết ngắn nếu có, trang PDF nếu đã đối chứng, những chỗ cần người học hỏi nghệ nhân.
- Lọc bài theo trạng thái **đã chuyển thành chỉ mục học V3.2 (2)** hoặc **chưa chuyển (18)**. **18 bản đều có sổ hoặc bảng V2 ở nhiều mức**, không có nghĩa “mất nguồn”: [Kiểm toán từng bài](../../docs/v3.2-kiem-toan-20-ban.md).
- [JSON 72 câu](../../data/v3_2/phrase_index.json), [JSON Schema](../../data/v3_2/schema.json) và [trình kiểm dữ liệu theo sổ V2](../../scripts/v3_2_validate.py), không cần API bên ngoài.
- Link đến [quy chế thẩm định](../../docs/v3.2-quy-trinh-tham-dinh.md) và [phiếu thực hành](../../docs/v3.2-phieu-thuc-hanh.md). Mọi trang ghi **0/20 nghiệm thu diễn xướng**, chưa có bản ghi có quyền tái phát.

## Thiết kế UI mới — Heritage Editorial (28/10/2026)

**Đã phát hành sau [PR #9](https://github.com/Form997/Vong-co/pull/9).** Không còn toàn bộ trang xanh đen với các hộp dày đặc: nay dùng **nền ngà `#f6f4ee`**, **xanh rừng `#10382f`**, **vàng đồng `#c79c5d`**; font hệ thống kết hợp Georgia cho tiêu đề. Trang đầu có hình tròn đồng tâm vẽ bằng CSS **không phải ảnh đàn/ảnh nghệ nhân**. Dễ đọc trên màn hình nhỏ và không cần CDN.

Trang chính có khối giới thiệu rõ nét, thanh tìm kiếm lớn, tab lọc nhóm, bộ lọc chứng cứ, thẻ bài và thông tin nguồn song song; trang từng bài có hero nhận diện, nút chuyển đến nguồn/bài học, accordion từng câu dễ bấm. Có `focus-visible`, `prefers-reduced-motion`, phông chữ fallback và nhãn biểu mẫu. Không sử dụng ảnh/font ngoài hay trình phát âm thanh chưa có quyền.

**Đối chứng kỹ thuật:** [62 Python tests đạt](https://github.com/Form997/Vong-co/actions/runs/40697296133); [Chromium 5 kích thước màn hình đạt và có ảnh](https://github.com/Form997/Vong-co/actions/runs/40697296268); [Pages đã triển khai](https://github.com/Form997/Vong-co/actions/runs/40697296276). Gói HTML/JSON xuất bản: **29 tệp, 462.065 byte** tại lần build này.

## Chính sách sử dụng và an ninh mạng (29/10/2026)

Dự án giữ **miễn phí/phi thương mại** ở V3.2. Trang [pháp lý dành cho người đọc](legal.html) đã được [GitHub Pages triển khai thành công](https://github.com/Form997/Vong-co/actions/runs/40791942791) qua [PR #10](https://github.com/Form997/Vong-co/pull/10), cùng gói **30 tệp / 473.683 byte**. Nội dung có đường dẫn đến [quy định pháp lý](../../docs/phap-ly-an-ninh-mang-v3.2.md), [quyền riêng tư](../../PRIVACY.md), [an ninh](../../SECURITY.md), [quyền và giấy phép](../../RIGHTS_AND_LICENSING.md), [cổng thương mại](../../docs/quy-trinh-thuong-mai-hoa.md) và [ứng phó sự cố](../../docs/quy-trinh-ung-pho-su-co.md).

**Mục đích là minh bạch, không tự cấp chứng nhận.** GitHub Pages có thể ghi địa chỉ IP phục vụ an ninh; mã trang không triển khai tracker, đăng ký hay thanh toán. Trước khi đưa website sang thu phí/API thương mại, đánh giá pháp luật và chuyển hạ tầng phù hợp: [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

### Sáu trang pháp luật quốc tế mới (29/10/2026)

Trang [pháp lý V3.2](legal.html) có thêm **6 thẻ quốc gia** dẫn đến các trang tĩnh sinh từ 28 nguồn nhà nước ở [sổ luật](../../data/v3_2/six_country_sources.json). Mỗi trang có tên luật gốc và điều kiện phạm vi sử dụng, không có JavaScript bên thứ ba hay tracker:

- `web/v3/quoc-gia/my.html` — Hoa Kỳ
- `web/v3/quoc-gia/nga.html` — Nga
- `web/v3/quoc-gia/trung-quoc.html` — Trung Quốc
- `web/v3/quoc-gia/uc.html` — Úc
- `web/v3/quoc-gia/nhat-ban.html` — Nhật Bản
- `web/v3/quoc-gia/han-quoc.html` — Hàn Quốc

**Đã triển khai trên website:** [GitHub Pages Build + Deploy thành công](https://github.com/Form997/Vong-co/actions/runs/40794249686) sau khi [PR #11](https://github.com/Form997/Vong-co/pull/11) hợp nhất. Gói web có **36 tệp / 540.826 byte** tại bản phát hành 29/10/2026; sáu trang luật được trình duyệt kiểm tra. Đây là nghiên cứu pháp lý có nguồn, không thay kiểm toán/tư vấn pháp lý và không mở khóa `commercial_enabled=false`.

## Mở bản công khai hoặc chạy thử V3.2 tại máy

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
- **Đã hợp nhất PR #8 vào `v3-development` và xác nhận [workflow Pages Deploy Success](https://github.com/Form997/Vong-co/actions/runs/40694415309).** [Python 60/60](https://github.com/Form997/Vong-co/actions/runs/40694415249) và [Chromium](https://github.com/Form997/Vong-co/actions/runs/40694415286) đều đạt trên commit merge. Bạn có thể [mở bài 01](https://form997.github.io/Vong-co/bai/01-luu-thuy-truong/#hoc-tung-cau) hoặc [bài 20](https://form997.github.io/Vong-co/bai/20-phung-cau/#hoc-tung-cau) để xem 72 vị trí câu. Đây là bài học *truy nguồn*, chưa phải âm nhạc được chứng nhận.

**Đã mở hồ sơ nguồn 20/20, nhưng nghiệm thu biểu diễn vẫn 0/20.** Địa chỉ web, README hoặc điểm kiểm thử phần mềm không phải chứng nhận của cơ quan chuyên môn.

[Nhật ký V3.2](../../docs/v3.2-khoi-dong.md) · [Chính sách source-first](../../docs/v3.2-quy-trinh-tham-dinh.md) · [Danh mục nguồn V2](../../docs/nguon-tham-khao.md).
