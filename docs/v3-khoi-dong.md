# HAI ĐẤT V3.0-alpha — TỪ HỒ SƠ NGHIÊN CỨU ĐẾN THƯ VIỆN DỮ LIỆU TRA CỨU

**Ngày bắt đầu:** 28/10/2026 (giờ Việt Nam; xem commit tạo tệp này trên nhánh `v3-development`).  
**Xuất phát từ:** nhánh `v2-development`, **không sửa** `v1-frozen`, `v2-development` hoặc `main`.  
**Tình trạng:** **KHỞI ĐỘNG V3.0-alpha**, đang xây dựng, chưa phát hành V3 ổn định.

> **Bắt đầu V3 không đồng nghĩa V2 đã nghiệm thu âm nhạc.** Có 20/20 biên bản kiểm nguồn V2, nhưng **0/20 bài nghiệm thu diễn xướng**; những điều V2 chưa xác minh phải đi nguyên vẹn vào dữ liệu V3.

## Vì sao cần V3?

Ở V2, thông tin đã có trong Markdown nhưng người dùng AI hoặc một website rất dễ nhầm thông tin của các **dị bản khác nhau**. V3 đặt mục tiêu biến các thông tin đã được ghi nguồn thành **dữ liệu đọc được bằng máy** để tìm kiếm nhanh, đối chiếu dị bản và truy ngược tới biên bản gốc, đồng thời giữ nhãn **chưa xác minh** ở mọi chỗ còn thiếu.

## Phạm vi V3.0-alpha được triển khai

1. **Danh mục JSON 20 bản Tổ**: mã số, tên, nhóm, danh sách dị bản, hệ câu/nhịp có nguồn, mốc tài liệu nội bộ và tình trạng thẩm định.
2. **Kiểm định dữ liệu tự động**: chống trùng số, chống nhầm Phụng Hoàng/Phụng Cầu, chống gán V2 là đã nghiệm thu, kiểm các đường dẫn nội bộ và cấu trúc JSON.
3. **Giao diện tra cứu tiếng Việt dùng trên điện thoại**: lọc theo Sáu Bắc/Bảy Lễ/Ba Nam/Bốn Oán, tìm tên bài, xem từng dị bản và mở ngay nguồn V2.
4. **Chạy thử GitHub Actions**: kiểm thử dữ liệu và ứng dụng tĩnh ở mỗi lần cập nhật nhánh V3.
5. **Nhật ký V3**: ngày bắt đầu, điều đã làm được, dung lượng tệp chính xác từ Git tree tại commit xác định, những điều chưa hoàn thành.

## Điều **KHÔNG** được tuyên bố ở alpha

- Chưa có bộ tổng phổ chuẩn 20 bài, chưa có bản thu có quyền phát lại và chưa được nghệ nhân duyệt.
- Không có quyền tự động sử dụng thương mại ký âm/lời/âm thanh của bên thứ ba.
- MCP và AI sinh lời/nhạc **không** được coi đã tích hợp vào sản phẩm V3 nếu chưa triển khai và kiểm thử.
- Các biến thể ghi theo nguồn là **bản ghi tham chiếu**, không được đồng nhất chỉ vì có cùng số câu.

## Quy tắc dữ liệu

Mỗi mục mới phải có `review_document` liên kết đến biên bản V2; mỗi hệ câu/nhịp ghi mức chứng cứ và ghi chú giới hạn. Nếu số câu/nhịp còn tranh luận, đặt `null` hoặc tách **hai hệ tham chiếu**, không chọn một làm chuẩn tuyệt đối. Tất cả mục V3 ban đầu có `performance_status: "pending"`.

## Lộ trình tiếp

- **V3.0-alpha:** danh mục JSON + validator + thử nghiệm web tĩnh + kiểm thử GitHub Actions.
- **V3.x tiếp theo:** bổ sung trích dẫn tới **từng trang in/từng câu** và dữ liệu có giấy phép; kiểm trình diễn với nghệ nhân.
- **V4 dự kiến:** API/MCP chỉ đọc được thử nghiệm và quản lý bản quyền. **Chưa tự gọi là đã hoàn thành.**

**Nguồn nền:** [20 bản Tổ](20-ban-to.md) · [Quy chế V2](ke-hoach-v2.md) · [Danh mục nguồn](nguon-tham-khao.md) · [Nhật ký các thế hệ](nhat-ky-phien-ban.md).
