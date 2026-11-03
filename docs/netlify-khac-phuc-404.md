# Khắc phục lỗi 404 trên Netlify cho HAI ĐẤT Vọng cổ

**Áp dụng cho**: dự án `Form997/Vong-co`, bản V3.6 từ nhánh `v3-development`.  
**Trang Netlify do người dùng báo lỗi:** https://cailuong.netlify.app/  
**Trang GitHub Pages đã chạy:** https://form997.github.io/Vong-co/

## Chẩn đoán quan trọng

Nhánh mặc định `main` là kho mã/robot nghiên cứu V3.6, **không chứa website hoàn chỉnh hoặc `index.html` tại thư mục gốc**. Trang thực được xây bằng `scripts/v3_build_site.py` trên nhánh `v3-development`. Nếu Netlify chọn nhầm `main` hay xuất bản thư mục gốc, trang 404 có thể xảy ra.

**Cần kiểm chứng:** Chúng tôi chưa có quyền xem bảng quản trị Netlify, nên chưa thể xác nhận `cailuong.netlify.app` có thực sự liên kết tới repository trên hay không. Đừng thay cấu hình của một trang khác khi chưa kiểm tra Git repository đã chọn.

## Cách sửa trên Netlify — B1 đến B6

**B1.** Đăng nhập https://app.netlify.com/ bằng tài khoản sở hữu trang. Chọn site `cailuong` hoặc site có URL `cailuong.netlify.app`.

**B2.** Mở **Project configuration → Developer settings → Continuous deployment**. Ở mục liên kết Git, xác nhận chính xác `Form997/Vong-co`. Nếu không phải repository này, dừng lại, tìm mã nguồn đúng của site trước.

**B3.** Ở **Branches and deploy contexts → Configure**, chọn **Production branch = `v3-development`**, lưu lại. Chỉ branch production mới cập nhật URL `cailuong.netlify.app`.

**B4.** Ở **Build settings → Configure**, đặt:
- **Base directory:** để trống (repository root)
- **Build command:** `python3 scripts/v3_build_site.py --out _site`
- **Publish directory:** `_site`
- **Python:** 3.11 (`PYTHON_VERSION = 3.11`)

Trong nhánh `v3-development`, tệp `netlify.toml` đã khai báo lệnh build và thư mục publish trên. Cấu hình tệp được Netlify ưu tiên; đường dẫn branch production vẫn phải được chọn trong UI.

**B5.** Vào **Deploys → Trigger deploy → Deploy site** hoặc **Deploy without cache**, tùy màn hình. Xem Deploy log: cần thấy lệnh Python thành công, `_site/index.html` tồn tại và trạng thái **Published**.

**B6.** Vào **Deploys → Latest published deploy → Deploy File Explorer**. Kiểm tra:
- `index.html`
- `web/v3/index.html`
- `nhom/sau-bac/index.html`
- `nhom/bay-le/index.html`
- `nhom/ba-nam/index.html`
- `nhom/bon-oan/index.html`
- các trang `bai/<slug>/index.html`

Sau khi Published thành công, thử https://cailuong.netlify.app/ và https://cailuong.netlify.app/web/v3/ . Nếu URL đầu còn 404 nhưng tệp `index.html` hiện trong File Explorer, kiểm tra deploy đã Published lên đúng site, redirects, firewall và domain settings.

## Vì sao không thêm `/* /index.html 200`?

Website này không phải React SPA; nó chứa các trang tĩnh riêng với `index.html` ở từng đường dẫn. Một redirect chung sẽ che lấp lỗi 404 thực tế và có thể trả trang chủ thay cho trang bài bị thiếu.

## Giới hạn và an toàn

- Cấu hình này **không tác động** đến GitHub Pages, không sửa dữ liệu V1/V2, không sửa 300 nhãn câu đã kiểm nguồn của V3.5.
- Không đặt Netlify token, khóa API hay mật khẩu trong `netlify.toml`.
- Thêm cấu hình GitHub **không tự thay đổi** Production branch và không tự redeploy Netlify nếu tài khoản Netlify chưa nối đúng repository.
- Nếu Netlify đang kết nối một repository khác, mã cấu hình này không sửa được site đó; hãy dùng log/ảnh chụp **Build settings** của site để xác định nguồn gốc trước.

## Tài liệu Netlify chính thức

- [Page not found — troubleshooting](https://docs.netlify.com/resources/troubleshooting/page-not-found-error-guide/)
- [Build config / publish directory](https://docs.netlify.com/build/configure-builds/file-based-configuration/)
- [Production branch settings](https://docs.netlify.com/deploy/deploy-overview/)
