# Nâng cấp website V3.6 — 03/11/2026

Ngày bắt đầu đợt sửa: **03/11/2026**. Nhánh cơ sở: `v3.6-development`, commit `0fe6b26de0caae71052429289c49c92bfb97dcab`.

## Nội dung mới

- Dựng website phải kiểm cả chỉ mục V3.2, V3.3 và V3.4 trước khi ghi tệp, ngoài các kiểm định V3.5 và danh mục hiện có. Chỉ mục cũ lỗi không được xuất kèm bản mới.
- Kiểm tra cập nhật website có thời hạn 10 giây. Nếu mạng treo, hủy yêu cầu rồi cho lượt kiểm sau chạy tiếp; không khóa chức năng cập nhật mãi mãi.
- CI Python/JavaScript và Chromium chạy cho PR tới các nhánh phát triển; mở rộng push tới V3.3–V3.6.
- Đo dung lượng qua GitHub API chỉ chạy thủ công, tránh phụ thuộc mạng ngoài trong kiểm thử mã trên PR.

## Kiểm chứng

- **115** kiểm thử Python đạt, gồm dựng trang, kiểm dữ liệu, nguồn, liên kết và HTTP cục bộ.
- **6** kiểm thử JavaScript đạt, gồm mạng treo, hồi phục sau timeout và ngăn vòng lặp tải lại.
- `compileall` đạt.
- Dựng **48 tệp**, gồm **20 trang bài**, **4 trang nhóm** và **6 trang quốc gia**.
- Dung lượng đầu ra chưa nén: **1.192.347 byte**, khoảng **1.164,40 KiB**, **9.538.776 bit**.
- Mã bản dựng: `afd7ce1ce29ca6676d1053c124c03270ebf65a52259eef7526f5298745b0e666`.

Đây là kết quả dựng và kiểm thử, chưa phải xác nhận website công khai đã triển khai bản này. CI Chromium cần được xác nhận trên PR. Không sửa `v1-frozen`, không tự chứng nhận diễn xướng hoặc tính tuân thủ pháp luật của tư liệu.
