# HƯỚNG DẪN XUẤT BẢN WEBSITE V3 TRÊN GITHUB PAGES

**Dự án:** [Form997/Vong-co](https://github.com/Form997/Vong-co) · **Nhánh nguồn:** `v3-development` · **Phiên bản:** V3.0-alpha (nghiên cứu).

> **Trạng thái kiểm chứng ngày 28/10/2026:** Đã tạo workflow xuất bản và chạy được bước **đóng gói 7 tệp**. Tuy nhiên [lần thử triển khai Pages #40674839366](https://github.com/Form997/Vong-co/actions/runs/40674839366) **không thành công tại job Deploy trước khi các bước trên runner khởi chạy**. Không được ghi website đã lên mạng. Connector không lấy được log lỗi của job Deploy, nên **chưa xác định chắc chắn nguyên nhân**. Các mục dưới đây là cách kiểm tra cấu hình theo GitHub Docs, không phải khẳng định đã sửa lỗi.

## 1. Những gì đã được chuẩn bị

- **Giao diện:** [`web/v3/index.html`](../web/v3/index.html).
- **Dữ liệu máy đọc:** [`data/v3/catalog.json`](../data/v3/catalog.json) — 20 bài/30 hệ bản.
- **Đóng gói chỉ tệp được phép công bố:** [`scripts/v3_build_site.py`](../scripts/v3_build_site.py).
- **Quy trình xuất bản:** [`.github/workflows/pages-v3.yml`](../.github/workflows/pages-v3.yml).
- **Kiểm thử độc lập:** [GitHub Actions V3](../.github/workflows/kiem-thu-v3.yml) và [kiểm tra trình duyệt Chromium](../.github/workflows/kiem-thu-trinh-duyet-v3.yml).

Gói xuất bản chỉ gồm **7 tệp**: `index.html` (chuyển hướng), `.nojekyll`, `robots.txt`, `sitemap.xml`, `web/v3/index.html`, `data/v3/catalog.json`, `data/v3/schema.json`.

**Không** phát hành toàn bộ thư mục `ban-to/`, `docs/`, tệp Python, mã kiểm thử, hay bản chép có bản quyền dưới dạng thư mục website. Các biên bản vẫn được xem trên GitHub qua liên kết.

## 2. Các bước bật Pages bằng giao diện GitHub

Trên điện thoại, dùng Chrome và chọn **Trang web cho máy tính** nếu không thấy menu.

1. Mở [**Settings → Pages**](https://github.com/Form997/Vong-co/settings/pages).
2. Trong **Build and deployment**, chọn **Source → GitHub Actions** (không chọn `Deploy from a branch` khi sử dụng workflow đóng gói an toàn này).
3. Vào [**Settings → Environments**](https://github.com/Form997/Vong-co/settings/environments). Nếu có môi trường **`github-pages`**, mở và kiểm tra **Deployment branches and tags**.
4. Nếu đang chặn nhánh `v3-development`, thiết lập quy tắc **chỉ cho phép `v3-development`** triển khai bản thử nghiệm (hoặc thêm nhánh này vào các quy tắc hiện có phù hợp). **Không xóa bảo vệ `main` hoặc mở quyền tùy tiện cho mọi nhánh.** Chỉ thay đổi khi GitHub hiển thị nhánh không được phép triển khai.
5. Mở [**Actions → HAI DAT V3 - Thu xuat ban GitHub Pages**](https://github.com/Form997/Vong-co/actions/workflows/pages-v3.yml). Chọn lần chạy bị lỗi và **Re-run failed jobs** hoặc **Re-run all jobs** để thử lại sau khi cài đặt.
6. **Chỉ khi job `Deploy public research preview` chuyển sang Success** và GitHub Settings → Pages hiển thị `Your site is live at ...`, mới ghi địa chỉ công khai là hoạt động.

Trang web theo cấu trúc dự kiến sẽ nằm tại:

```text
https://form997.github.io/Vong-co/
https://form997.github.io/Vong-co/web/v3/
```

**Đây chỉ là địa chỉ theo quy tắc GitHub Pages, chưa xác nhận truy cập được.** URL chính thức phải đối chiếu với Settings → Pages sau khi deploy.

## 3. Nếu Pages tiếp tục báo lỗi

- **Failed trước bước Setup:** xem quy tắc môi trường `github-pages` và điều kiện nhánh; xem mục lỗi trực tiếp trên Actions.
- **GitHub Pages chưa được bật hoặc nguồn sai:** chọn `Source: GitHub Actions` tại Settings → Pages.
- **Bị chặn quyền deploy:** workflow đã khai báo `pages: write`, `id-token: write`; kiểm tra thông báo cụ thể ở job và chính sách repository/organization.
- **Mở website được nhưng không hiện dữ liệu:** dùng tab Network/Console xem `/Vong-co/data/v3/catalog.json`; artifact phải có cả `data/v3/`. Không mở riêng `file://` để thử `fetch` JSON.
- **Bị chặn bởi bảo vệ branch:** không tắt bảo vệ V1/main. Cần điều chỉnh đúng quy tắc môi trường hoặc chọn nhánh phát hành hợp lệ.

## 4. Kiểm định trước khi giới thiệu công khai

- [ ] Job GitHub Pages báo **Success**.
- [ ] Mở được trang root và `web/v3/` trên điện thoại.
- [ ] Giao diện nạp **20 bản Tổ, 30 hệ bản**.
- [ ] Tìm **`Phung Cau`** hiển thị đúng **Phụng Cầu**.
- [ ] Bốn bộ lọc hiện đúng **6/7/3/4** bài.
- [ ] Cổ Bản có **2 hệ Vắn/Trường**, Nam Ai hiển thị **84 và 68** như các hệ nguồn khác.
- [ ] Mọi đường dẫn nguồn/biên bản mở đúng trang GitHub.
- [ ] Banner công khai ghi **0/20 bài nghiệm thu diễn xướng** và các giới hạn giấy phép.

### Tài liệu chính thức

- [GitHub: Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
- [GitHub: Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

**Ghi nhớ:** “Mã nguồn đã có” ≠ “GitHub Pages đã chạy” ≠ “20 bản Tổ đã nghiệm thu nhạc”.
