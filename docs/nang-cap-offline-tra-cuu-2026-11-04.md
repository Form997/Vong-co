# Nâng cấp MCP ngoại tuyến và tra cứu — 04/11/2026

Ngày bắt đầu: **04/11/2026**, giờ Việt Nam. Đợt này mở rộng PR #32,
bao gồm bản đóng gói an toàn trước đó; không tăng phiên bản của dữ liệu câu.

## Chức năng mới

1. **Bộ tư liệu ngoại tuyến có kiểm tra toàn vẹn:** xuất 61 đường dẫn Markdown
   V1/V2 từ commit Git; lập manifest chứa commit và SHA-256. Đọc không cần mạng,
   phát hiện tệp thay đổi hoặc bị mất, từ chối symlink và đường dẫn ngoài danh mục.
2. **Nguồn trả về minh bạch:** công cụ MCP thứ 8 `get_source_status`; mỗi phản hồi
   có nội dung kèm `source_mode`, `content_sha256`; liên kết nguồn ngoại tuyến
   trỏ commit cố định. Không tự chuyển sang mạng khi bộ ngoại tuyến bị lỗi.
3. **Tìm kiếm MCP linh hoạt:** bỏ dấu, chuẩn hóa khoảng trắng và tìm theo các từ
   ở thứ tự khác nhau; số bài vẫn khớp chính xác.
4. **Tra cứu web:** tìm chính xác số bài; xóa tất cả bộ lọc một lần; giữ tìm kiếm,
   nhóm, mức chứng cứ, trạng thái chỉ mục và thứ tự sắp xếp trong URL. Mở lại
   hoặc chia sẻ đường dẫn sẽ phục hồi các lựa chọn hợp lệ.
5. **Phục hồi khi tải lỗi:** giới hạn chờ 12 giây, hủy yêu cầu treo và cho bấm
   “Thử lại”; thông báo dễ hiểu, không bắt người dùng cuối chạy lệnh máy chủ.

## Đã kiểm tại môi trường phát triển

- 136 bài kiểm thử Python dự án và 6 bài JavaScript tự cập nhật đạt.
- MCP: 27 bài đạt, 2 bài đọc mạng được bỏ qua theo thiết lập của kho.
- Xuất thực tế đủ **61/61 tệp**; thực hiện **101 thao tác đọc ngoại tuyến** trên
  20 bài, 2 phiên bản, biên bản, dị bản, nguồn và quy chế; chặn toàn bộ truy cập
  mạng trong bài thử này.
- Kiểm thử giao thức MCP bao gồm đọc ngoại tuyến và tệp bị sửa: trả lỗi thay vì
  đưa nội dung thay đổi ra như nguồn hợp lệ.
- Đóng gói thành công 48 tệp website, kiểm tra cú pháp Python/JavaScript đạt.
- Chromium cục bộ bị môi trường chặn tạo socket; kiểm thử trình duyệt đầy đủ,
  bao gồm ca mới về tìm số, chia sẻ bộ lọc và phục hồi mạng, chạy ở GitHub Actions.
  Xem kết quả theo commit mới nhất tại [PR #32](https://github.com/Form997/Vong-co/pull/32).

## Dung lượng đo thực tế

| Bộ dữ liệu | Byte | KB thập phân | Bit |
| --- | ---: | ---: | ---: |
| Website sau nâng cấp | 1.194.337 | 1.194,337 | 9.554.696 |
| Ngoại tuyến V1/V2, gồm manifest | 505.889 | 505,889 | 4.047.112 |

Snapshot đã thử dùng V1 `f6537c83878bca079752dbdd4baec5b1164a1ab4` và V2
`cae843ef2aec3bf1af4532949f9042604171e8a9`. Các con số không phải dung lượng
Python, trình duyệt hoặc toàn bộ lịch sử Git. Không đóng gói bản thu/PDF.

## Cách dùng và cập nhật

Xem [hướng dẫn MCP cho Windows/Linux/macOS](../integrations/vong-co-mcp/README.md).
Cần cài phụ thuộc và tải Git trước khi dùng ngoại tuyến. Snapshot không tự cập
nhật: fetch nguồn, xuất sang thư mục mới, đổi cấu hình rồi khởi động lại MCP.
SHA-256 không phải chữ ký số; phải chọn kho và commit đáng tin cậy.

Chế độ ngoại tuyến áp dụng cho MCP; website vẫn cần tải HTML/JSON qua máy chủ
HTTP. Chưa có service worker hoặc ứng dụng Android riêng. Nghiệm thu diễn xướng
vẫn **0/20**. PR và kiểm thử thành công không đồng nghĩa đã phát hành website.
