# Nâng cấp mã nguồn — 03/11/2026

Phạm vi: bộ quét metadata và MCP trên `main`. Phần website V3.6 được kiểm riêng trên nhánh phát triển; không tự hợp nhất lịch sử phân kỳ.

## Thay đổi

- Tìm số bài MCP theo số chính xác: `1` và `01` chỉ trả bài 01.
- Từ chối đầu vào sai kiểu; kiểm giới hạn byte ngay cả với bộ đọc nguồn tùy biến.
- Từ chối chuyển hướng HTTP ở bộ quét và bộ đọc MCP, tránh đi ra ngoài địa chỉ nguồn đã chọn.
- Không gửi khóa OpenAlex sang Crossref; từ chối JSON trùng khóa và nội dung nguồn UTF-8 hỏng.
- Thử lại lỗi kết nối tối đa ba lần; thông báo lỗi không chứa chi tiết nhạy cảm.
- Báo `truncated` khi quy chế V2 bị cắt do giới hạn đầu ra.
- CI chạy toàn bộ kiểm thử scanner; MCP chạy trên PR và thay đổi main, có giới hạn thời gian.
- Kiểm tra nguồn trực tuyến MCP là job riêng khi chạy thủ công. Lỗi mạng không thay thế kết quả kiểm thử ngoại tuyến.
- Lưu báo cáo quét nguồn kể cả khi bước quét thất bại và đã tạo báo cáo.

## Kiểm chứng tại môi trường làm việc

13 kiểm thử scanner + 9 kiểm thử catalog hiện có + 6 kiểm thử hồi quy MCP: **28 đạt**.
Kiểm thử giao thức MCP cần gói `mcp>=2,<3`, chưa có trong môi trường này; GitHub Actions phải xác nhận trước khi hợp nhất.

```bash
python -m unittest discover -s tests -v
cd integrations/vong-co-mcp
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Không thay đổi nhánh `v1-frozen`, nội dung tư liệu hoặc trạng thái nghiệm thu diễn xướng. Kiểm thử phần mềm không chứng nhận âm nhạc hay pháp lý.
