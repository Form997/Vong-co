# HAI ĐẤT V3 — Giao diện tra cứu tiếng Việt (alpha)

[**Mở mã trang web**](index.html) · [**Danh mục JSON**](../../data/v3/catalog.json) · [**Lược đồ dữ liệu**](../../data/v3/schema.json)

## Trang này đã làm được gì?

- Hiển thị **20 bản Tổ**, số hệ bản/dị bản theo dữ liệu V3; tìm kiếm tiếng Việt có dấu hoặc không dấu.
- Lọc theo **Sáu Bắc / Bảy Lễ / Ba Nam / Bốn Oán**.
- Mở từng bài để xem hệ câu, nhịp theo nguồn, mức chứng cứ và lý do chưa xác minh.
- Nhấn liên kết để đọc hồ sơ, biên bản V2 và URL tư liệu bên ngoài.
- Giao diện tĩnh đáp ứng màn hình điện thoại; không cần API riêng, cơ sở dữ liệu hoặc khóa bí mật.

**Đây là bản thử nghiệm V3.0-alpha, chưa phải website công khai đã triển khai trên GitHub Pages.** Khi cấu hình GitHub Pages, cần chạy từ **thư mục gốc kho** để đường dẫn `../../data/v3/catalog.json` vẫn tồn tại.

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
