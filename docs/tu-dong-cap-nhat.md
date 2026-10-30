# Tự động cập nhật bản dựng website

**Bắt đầu:** 30/10/2026. Tính năng này tạo mã nhận diện cho mỗi bản dựng website dựa trên nội dung công khai đã qua kiểm tra. Mã thay đổi khi gói website thay đổi; dựng lại cùng nội dung giữ cùng mã. Mã bản dựng không tự thay số phiên bản học liệu hoặc biến dữ liệu chưa kiểm thành bản Tổ đã được nghiệm thu.

Khi có thay đổi hợp lệ trên `v3-development`, GitHub Actions tự chạy các trình kiểm dữ liệu, quyền, Python và Chromium; sau khi đạt, Pages tự đóng gói và triển khai theo cấu hình `HAI_DAT_PAGES_ENABLED`. Không cần chạy lại thủ công chỉ vì tệp không nằm trong danh sách đường dẫn cũ. Bản đề xuất vẫn qua Pull Request và kiểm thử trước khi hợp nhất. Các nhánh `main`, `v1-frozen` và `v2-development` không phải đích của quy trình này.

Trang đang mở kiểm tra mã mới khi hoạt động và theo chu kỳ. Nếu website có bản mới, trình duyệt tải lại trang, giữ đường dẫn và phần neo; lỗi mạng không ngăn đọc trang đang mở. Cơ chế tránh lặp khi mạng phân phối còn trả bản cũ. Dữ liệu so sánh được lấy từ chính website, không gửi dữ liệu cá nhân tới dịch vụ ngoài. Không dùng service worker để lưu thêm bản nhạc hay âm thanh.

Chức năng này tự tạo **mã bản dựng và triển khai**, không tự nghiên cứu bài tiếp theo, sao chép lời/ký âm, mở quyền thương mại hoặc tự xác nhận diễn xướng. Việc mở rộng học liệu vẫn cần nguồn, thẩm định và kiểm thử như trước. Ngày, kết quả kiểm thử và kích thước của bản phát hành tính năng này được bổ sung vào nhật ký sau khi xác nhận trên GitHub.
