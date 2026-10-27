# HAI ĐẤT VỌNG CỔ MCP — bản thử nghiệm chỉ đọc

**Mục tiêu:** cho dự án AI khác tra cứu 20 bản Tổ của [Form997/Vong-co](https://github.com/Form997/Vong-co) mà không ghi sửa kho hoặc tự cấp chứng nhận nghiệm thu.

## Trạng thái

- **Mã nguồn bản thử nghiệm** trên nhánh `feature/mcp-readonly-v1`.
- **V1 được đọc từ nhánh `v1-frozen`** (chỉ dữ liệu hồ sơ); **V2 từ `v2-development`** (biên bản đang nghiệm thu, chưa hoàn thành).
- Không đọc GitHub token, không cấp quyền ghi, không tải hay phân phối MP3/PDF/lời ca về cho người khác.
- Chưa triển khai máy chủ HTTPS công cộng, chưa đăng ký Plugin ChatGPT và chưa tuyên bố sản phẩm đã được kiểm thử end-to-end với ChatGPT.
- Chưa có tệp LICENSE được xác minh cho toàn kho. **Dự án công khai không mặc nhiên đồng nghĩa được cấp quyền tái sử dụng toàn bộ tài liệu, code hay nhạc.** Cần quyết định giấy phép cho mã do mình tạo, và xin phép riêng đối với tác phẩm/bản thu của người khác trước khi phát hành.

## Cấu trúc

- `server.py`: MCP Python SDK v2 (`MCPServer`), hỗ trợ `stdio` và HTTP.
- `catalog.py`: danh mục 20 bài, bộ lọc nhánh/tệp an toàn, đọc raw Markdown GitHub.
- `tests/test_catalog.py`: kiểm thử logic không cần mạng.

## 7 công cụ cho AI khác

| Công cụ | Nội dung |
|---|---|
| `list_ban_to()` | Đúng 20 bản, 6 Bắc / 7 Lễ / 3 Nam / 4 Oán |
| `search_ban_to(query)` | Tìm tên/nhóm không phân biệt dấu tiếng Việt |
| `get_ban_to(bai_so, version)` | Đọc README V1/V2, có liên kết nguồn |
| `get_nghiem_thu(bai_so)` | Đọc biên bản V2, KHÔNG tự tuyên bố ĐẠT |
| `get_di_ban(bai_so)` | Trích các đoạn V1 nói về dị bản, số câu/nhịp |
| `get_nguon(bai_so)` | Liệt kê đường dẫn nguồn từ README (chưa tự xác nhận giấy phép) |
| `get_quy_che_v2()` | Đọc quy chế kiểm nghiệm V2 hiện tại |

## Cài thử trên máy (Python 3.11 trở lên)

1. Sao chép kho rồi chuyển sang nhánh `feature/mcp-readonly-v1`.
2. Mở terminal trong thư mục `integrations/vong-co-mcp`.
3. Tạo môi trường Python, cài gói và chạy thử:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python server.py
```

Tiến trình MCP chạy theo giao thức **stdio**, **không in trang web** hoặc giao diện người dùng; nó chờ một MCP client kết nối qua stdin/stdout. Có thể thử qua **MCP Inspector** theo [tài liệu chính thức](https://py.sdk.modelcontextprotocol.io/get-started/).

### Cấu hình ví dụ cho ứng dụng hỗ trợ MCP stdio

```json
{
  "mcpServers": {
    "hai-dat-vong-co": {
      "command": "python",
      "args": ["/DUONG_DAN_DA_TAI/integrations/vong-co-mcp/server.py"],
      "env": { "MCP_TRANSPORT": "stdio" }
    }
  }
}
```

Thay `/DUONG_DAN_DA_TAI` bằng đường dẫn thật của máy. Tên khóa cấu hình có thể khác tùy ứng dụng; trên Windows có thể cần chỉ rõ đường dẫn `python.exe` trong môi trường ảo.

### Chạy bản HTTP **chỉ trên máy của mình**

```bash
MCP_TRANSPORT=streamable-http python server.py
```

- Endpoint mặc định: `http://127.0.0.1:8000/mcp`.
- Biến môi trường tùy chọn `MCP_PORT` (mặc định 8000), `MCP_HOST` (mặc định 127.0.0.1).
- **Không đổi sang `0.0.0.0` hoặc đưa Internet công khai ngay:** mẫu này chưa triển khai xác thực, chống lạm dụng, TLS, giới hạn lưu lượng và giám sát. Muốn tích hợp ChatGPT qua remote MCP cần dịch vụ HTTPS, bảo mật và cấu hình ứng dụng/Plugin tương thích.

## Những gì người dùng khác thực sự nhận

- Chỉ được đọc các tệp Markdown đã giới hạn trong danh mục của hai nhánh đã chọn.
- Nếu chưa có biên bản V2, `get_nghiem_thu` trả `CHUA_CO_BIEN_BAN_V2`, không suy đoán `ĐẠT`.
- Nếu biên bản chứa `CHỜ NGHIỆM THU`, trạng thái trả tương ứng; trường `accepted` luôn `false` trong phiên bản thử nghiệm. Để công nhận `ĐẠT` trong các bản sau cần cơ chế xác minh chữ ký kiểm định chứ không dò từ khóa.
- Nội dung từ GitHub là **dữ liệu không đáng tin cậy về mặt lệnh AI**: ứng dụng gọi MCP phải coi Markdown là tài liệu để tham khảo, không làm theo các câu lệnh xen vào tài liệu.

## Bảo trì dữ liệu sau khi V2 hoàn thành

Không cần viết lại toàn bộ MCP: nhánh `v2-development` được đọc theo yêu cầu, cập nhật biên bản sẽ hiện sau lần tra cứu kế tiếp. Sau khi nghiệm thu được khóa, hãy ghim một tag/commit V2 đã duyệt và bổ sung schema `verdict` có chữ ký chuyên môn trước khi cho phép phần mềm báo `ĐẠT`.

## Tài liệu

- [Python MCP SDK v2 — chính thức](https://py.sdk.modelcontextprotocol.io/)
- [Chạy stdio và Streamable HTTP](https://py.sdk.modelcontextprotocol.io/run/)
- [Hướng dẫn app/MCP trong ChatGPT](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)
