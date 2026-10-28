# HƯỚNG DẪN XUẤT BẢN WEBSITE V3 TRÊN GITHUB PAGES

> **CẬP NHẬT THỰC TẾ — 28/10/2026:** GitHub đã **triển khai thành công website V3.0** ở [run #40675923989, attempt 3](https://github.com/Form997/Vong-co/actions/runs/40675923989), job **Deploy public research preview = Success**. GitHub xác nhận địa chỉ [https://form997.github.io/Vong-co/](https://form997.github.io/Vong-co/). Các lỗi và hướng dẫn bên dưới là **lịch sử xử lý ban đầu**, không phải trạng thái hiện tại.
>
> **V3.1:** nhánh `v3.1-development` hiện **chỉ build và kiểm thử**, không tự deploy. Gói V3.1 gồm **27 tệp** (20 trang bài mới); chỉ sau khi xét duyệt Pull Request vào `v3-development` mới kích hoạt xuất bản V3.1. Xem [hướng dẫn thử V3.1](../web/v3/README.md).



**Dự án:** [Form997/Vong-co](https://github.com/Form997/Vong-co) · **Nhánh nguồn:** `v3-development` · **Phiên bản:** V3.0-alpha (nghiên cứu).

> **Trạng thái kiểm chứng ngày 28/10/2026:** Đã tạo workflow xuất bản và chạy được bước **đóng gói 7 tệp**. Tuy nhiên [lần thử triển khai Pages #40674839366](https://github.com/Form997/Vong-co/actions/runs/40674839366) **không thành công tại job Deploy trước khi các bước trên runner khởi chạy**. Sau đó workflow đã được thiết kế **opt-in**, [lượt mới có Build thành công, Deploy = Skipped](https://github.com/Form997/Vong-co/actions/runs/40675606473). **Tại lần thử đó chưa có website đã xuất bản**; không được lấy trạng thái workflow xanh khi Deploy bỏ qua làm bằng chứng website đã lên mạng. Connector không lấy được log lỗi của job Deploy, nên **chưa xác định chắc chắn nguyên nhân**. Các mục dưới đây là cách kiểm tra cấu hình theo GitHub Docs, không phải khẳng định đã sửa lỗi.

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
4. Nếu GitHub đang chặn nhánh `v3-development`, thêm quy tắc cho phép **đúng nhánh `v3-development`** triển khai bản thử nghiệm. **Không xóa bảo vệ `main` hoặc mở quyền tùy tiện cho mọi nhánh.** Chỉ thay đổi khi đã hiểu chính sách môi trường.
5. Khi đã kiểm tra Pages và quyền nhánh, vào **Settings → Secrets and variables → Actions → Variables → New repository variable**, đặt **Name: `HAI_DAT_PAGES_ENABLED`** và **Value: `true`**. Đây là **công tắc đồng ý công bố website**: mặc định không có biến thì job Deploy bị **skipped** để tránh báo lỗi lặp lại và tránh xuất bản ngoài ý muốn. Không cần điền mật khẩu/token vào biến này.
6. Mở [**Actions → HAI DAT V3 - Thu xuat ban GitHub Pages**](https://github.com/Form997/Vong-co/actions/workflows/pages-v3.yml). Chọn lần chạy mới nhất và **Re-run all jobs** sau khi cài đặt; hoặc cập nhật một tệp trong `web/v3/` để tự kích hoạt lại.
7. **Chỉ khi job `Deploy public research preview (opt-in)` có kết quả Success** (**không phải Skipped**) và Settings → Pages hiển thị `Your site is live at ...`, mới được thông báo website đã hoạt động.

Trang web theo cấu trúc dự kiến sẽ nằm tại:

```text
https://form997.github.io/Vong-co/
https://form997.github.io/Vong-co/web/v3/
```

**Sau khi khắc phục lỗi**, GitHub Deploy xác nhận địa chỉ trên trong nhật ký chạy thành công. URL triển khai của riêng V3.1 sẽ được xác nhận lại sau khi phát hành.

## 3. Nếu Pages tiếp tục báo lỗi

- **Failed trước bước Setup:** xem quy tắc môi trường `github-pages` và điều kiện nhánh; xem mục lỗi trực tiếp trên Actions.
- **GitHub Pages chưa được bật hoặc nguồn sai:** chọn `Source: GitHub Actions` tại Settings → Pages.
- **Workflow xanh nhưng job Deploy = Skipped:** chưa bật biến repository `HAI_DAT_PAGES_ENABLED=true`; xem bước 5. Không được nhầm Build Success với website đã xuất bản.
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
