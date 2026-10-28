# HAI ĐẤT V3.1 — Tra cứu 20 bản Tổ và trang riêng từng bài

**Trạng thái:** V3.1 phát triển trên [`v3.1-development`](https://github.com/Form997/Vong-co/tree/v3.1-development) · khởi động **28/10/2026**. Website **V3.0** đã được GitHub Pages triển khai thành công [tại lần chạy #40675923989](https://github.com/Form997/Vong-co/actions/runs/40675923989). **Bản V3.1 chưa được đưa lên website công khai**; cần nghiệm thu Pull Request vào `v3-development`.

[**Website V3 công khai**](https://form997.github.io/Vong-co/) · [**Danh mục JSON**](../../data/v3/catalog.json) · [**Nhật ký V3.1**](../../docs/v3.1-khoi-dong.md)

## Có gì mới trong V3.1?

- **20 trang riêng có URL ổn định**: `/Vong-co/bai/01-luu-thuy-truong/` đến `/Vong-co/bai/20-phung-cau/`, **được tạo khi build** từ dữ liệu JSON. Những URL này **đã được GitHub báo xuất bản thành công** trước khi nhánh V3.1 được hợp nhất và xuất bản.
- Mỗi trang có tên bài, nhóm, tên khác, từng hệ câu/nhịp **theo nguồn**, mức chứng cứ, lưu ý nghiên cứu, liên kết biên bản V2, nút bài trước/sau và đường trở về danh mục.
- Tìm không dấu, lọc 4 nhóm **Sáu Bắc (6), Bảy Lễ (7), Ba Nam (3), Bốn Oán (4)**; thêm lọc **có chỉ mục ở V2 / nguồn thuật lại / ánh xạ chưa thẩm định** và sắp xếp theo tên tiếng Việt hoặc số bài.
- **Sitemap 22 địa chỉ**: trang gốc, danh mục và 20 trang bài; không gán chứng nhận hay chép nguyên nội dung được bảo hộ.
- Gói Pages giới hạn **27 tệp công khai**: 7 tệp nền (HTML, JSON, schema, robots, sitemap, nojekyll) và 20 trang HTML được tạo. **Không** chép `ban-to/`, `docs/`, mã Python, thử nghiệm, PDF hoặc MP3 vào website.

## Chạy và xem trang V3.1 thực sự

Trong nhánh `v3.1-development`, tại thư mục gốc của repository:

```bash
python scripts/v3_validate.py
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/v3_build_site.py --out _site
python -m http.server 8000 --directory _site
```

Mở trong trình duyệt (trên máy chạy thử):

```text
http://localhost:8000/web/v3/
http://localhost:8000/bai/01-luu-thuy-truong/
http://localhost:8000/bai/20-phung-cau/
```

Với Codespaces, mở cổng 8000 bằng tính năng **Ports**. Không mở trực tiếp `file://` vì trình duyệt có thể không cho `fetch` dữ liệu JSON.

**Chú ý:** chương trình không xóa thư mục `_site` đã có; lần build mới phải dùng thư mục đích rỗng hoặc xóa bản thử cũ có chủ đích.

### Kết quả kiểm thử

- [GitHub Actions V3.1 — 45 bài thử Python đạt](https://github.com/Form997/Vong-co/actions/runs/40688707624).
- [Chromium end-to-end](https://github.com/Form997/Vong-co/actions/runs/40688596819) đã kiểm tra tìm kiếm, lọc chứng cứ, sắp xếp tiếng Việt, 20 URL trả HTTP 200, liên kết nguồn và giao diện 390 px.
- [Đóng gói website V3.1](https://github.com/Form997/Vong-co/actions/runs/40688707588): **27 tệp, 197.920 byte**, job Build thành công, **Deploy = Skipped** đúng quy trình thử nhánh; chưa xuất bản ra Internet.

## Quy trình phát hành an toàn

`v3.1-development` → kiểm thử tự động → **Pull Request** vào `v3-development` → rà soát → merge → workflow Pages triển khai khi điều kiện được cấp → xác nhận trang web online.

Nhánh `main` và `v1-frozen` không bị thay đổi. V3.1 **không** tự cấp phép nội dung hay tuyên bố đã nghiệm thu âm nhạc: **20/20 đã mở hồ sơ kiểm nguồn; 0/20 nghiệm thu diễn xướng**.

**Giới hạn còn lại:** chưa có ký âm/audio đủ quyền công bố, chưa nghiệm thu thực tấu nghệ nhân, chưa có giao diện nhập/sửa dữ liệu hay API/AI chính thức; các bài V3.1 là trang **metadata**, không phải bài học hoàn chỉnh hoặc bản diễn nhạc.

## Phát hành V3.1 đã xác nhận

- [Kết quả GitHub Actions triển khai Pages](https://github.com/Form997/Vong-co/actions/runs/40689588576): **Build Success · Deploy Success**.
- [Kiểm thử Python sau merge](https://github.com/Form997/Vong-co/actions/runs/40689588560) và [Chromium sau merge](https://github.com/Form997/Vong-co/actions/runs/40689588524): **Success**.
- [Website tra cứu](https://form997.github.io/Vong-co/) · [Lưu Thủy Trường](https://form997.github.io/Vong-co/bai/01-luu-thuy-truong/) · [Phụng Cầu](https://form997.github.io/Vong-co/bai/20-phung-cau/).

*URL công khai đã được GitHub deploy ghi nhận. Kiểm thử HTTP 20 trang được thực hiện trong môi trường Chromium của GitHub Actions; chưa thực hiện kiểm tra truy cập web công khai độc lập từ bên ngoài.*
