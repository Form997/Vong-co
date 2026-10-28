# HAI ĐẤT V3 — Giao diện tra cứu tiếng Việt (alpha)

[**Mở mã trang web**](index.html) · [**Danh mục JSON**](../../data/v3/catalog.json) · [**Lược đồ dữ liệu**](../../data/v3/schema.json)

## Trang này đã làm được gì?

- Hiển thị **20 bản Tổ**, số hệ bản/dị bản theo dữ liệu V3; tìm kiếm tiếng Việt có dấu hoặc không dấu.
- Lọc theo **Sáu Bắc / Bảy Lễ / Ba Nam / Bốn Oán**.
- Mở từng bài để xem hệ câu, nhịp theo nguồn, mức chứng cứ và lý do chưa xác minh.
- Nhấn liên kết để đọc hồ sơ, biên bản V2 và URL tư liệu bên ngoài.
- Giao diện tĩnh đáp ứng màn hình điện thoại; không cần API riêng, cơ sở dữ liệu hoặc khóa bí mật.

**Đây là bản thử nghiệm V3.0-alpha, chưa phải website công khai đã triển khai trên GitHub Pages.** Khi cấu hình GitHub Pages, cần chạy từ **thư mục gốc kho** để đường dẫn `../../data/v3/catalog.json` vẫn tồn tại.

## Xuất bản GitHub Pages — đã chuẩn bị, chưa lên mạng

Workflow [**thử xuất bản V3**](../../.github/workflows/pages-v3.yml) đã tạo được gói website **7 tệp**, nhưng job Deploy [chưa thành công ở lần chạy #40674839366](https://github.com/Form997/Vong-co/actions/runs/40674839366). GitHub Pages **chưa được xác nhận hoạt động**. Không chia sẻ đường dẫn như một website đang online.

**Chủ kho cần kiểm tra Settings → Pages (Source: GitHub Actions) và quy tắc môi trường `github-pages`**. Đọc [**hướng dẫn khắc phục chi tiết theo GitHub Docs**](../../docs/v3-github-pages.md).

## Đã kiểm thử thao tác bằng Chromium thật

[**GitHub Actions: kiểm thử trình duyệt thành công — run #40675487073**](https://github.com/Form997/Vong-co/actions/runs/40675487073). Kết quả đã kiểm trên trang chạy qua HTTP:

- Nạp đúng **20 bản Tổ và 30 hệ bản**;
- Lọc bốn nhóm **6/7/3/4**;
- Tìm `phung cau` chỉ hiện **Phụng Cầu** (không lấy Phụng Hoàng vì ghi chú nhắc tên bài khác);
- Tìm `co ban van` nhận đúng **Cổ Bản Vắn/Trường**;
- Xem **Nam Ai 84/68** theo hai nguồn khác nhau;
- Liên kết `#bai-20` hoạt động khi điều hướng mà không tải lại trang;
- Màn hình điện thoại **390 px không tràn ngang**, không có lỗi JavaScript không được bắt.

Run đã tạo ảnh chụp **`v3-mobile.png`** và **`v3-desktop.png`** trong artifact `hai-dat-v3-browser-evidence`. Đây là **kiểm thử chức năng giao diện**, không phải bảo chứng âm nhạc hay kiểm trực tiếp Chrome Android trên thiết bị thật.

**Kiểm thử Python riêng:** [GitHub Actions V3](../../.github/workflows/kiem-thu-v3.yml) có **42 bài thử**, xác thực danh mục/nguồn/website HTTP, khoảng **174 đường dẫn nội bộ** tại mốc kiểm thử ngày 28/10/2026.

## Chạy thử bằng Python trên Codespaces hoặc máy tính

Tại thư mục gốc repository, nhánh `v3-development`:

```bash
python -m http.server 8000 --bind 0.0.0.0
```

Sau đó mở:

```text
http://localhost:8000/web/v3/
```

Trên Codespaces, chuyển tiếp cổng **8000** rồi dùng URL được cung cấp. Nếu dùng máy tính, mở trực tiếp `file://` có thể khiến trình duyệt chặn `fetch` dữ liệu JSON; phải sử dụng máy chủ HTTP.

### Các lệnh kiểm định

```bash
python scripts/v3_validate.py --json
python -m unittest discover -s tests -p "test_*.py" -v
```

Sau khi cấu hình Pages tại **Settings → Pages**, nếu chọn nhánh `v3-development`, thư mục **/(root)** và site triển khai thành công, trang dự kiến theo kiểu đường dẫn:

```text
https://form997.github.io/Vong-co/web/v3/
```

**Đừng coi đây là một địa chỉ đã hoạt động trước khi có trang Pages/Actions báo triển khai thành công.** Cấu hình xuất bản thuộc quyền chủ kho.

## Những điều chưa làm

- Chưa có audio/score được phép phân phối, trình ca, mô phỏng nhạc hoặc khả năng tự viết ký âm.
- Chưa có dữ liệu từng phách/ngón đã được nghệ nhân duyệt.
- Chưa có backend/AI chat trực tiếp trong bản web này; nguyên mẫu MCP ở [nhánh thử nghiệm riêng](https://github.com/Form997/Vong-co/tree/feature/mcp-readonly-v1/integrations/vong-co-mcp).
- Chưa có chứng cứ cấp phép thương mại cho mọi nội dung bên thứ ba.

**Quy tắc:** Khi thiếu nguồn, hiển thị “chưa xác minh” — không tự trả lời dứt khoát.
