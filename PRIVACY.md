# CHÍNH SÁCH QUYỀN RIÊNG TƯ — HAI ĐẤT V3.2

**Mã:** HD-PRIVACY-3.2.1 · **Rà soát:** 29/10/2026.  
**Áp dụng cho:** trang tĩnh [HAI ĐẤT](https://form997.github.io/Vong-co/) và thư mục nghiên cứu [Form997/Vong-co](https://github.com/Form997/Vong-co).  
**Mô hình hoạt động:** tra cứu miễn phí, hiện không có chức năng đăng ký tài khoản, mua hàng, trò chuyện với bot, tải file của người xem lên hoặc gửi biểu mẫu về máy chủ HAI ĐẤT.

## 1. Bản tóm tắt minh bạch

Mã website hiện tại dùng JavaScript để **tải hai tệp JSON tĩnh từ chính website**, tìm kiếm và lọc nội dung **trực tiếp trong trình duyệt**. Tại thời điểm rà soát mã, website **không có** SDK phân tích truy cập, thẻ quảng cáo, tracker hành vi, cookie do ứng dụng tự tạo, `localStorage`, biểu mẫu thu tên/email, API lưu dữ liệu người học, trình phát âm thanh hay cơ chế nhận thanh toán.

**Nhưng không tuyên bố “không ai thu thập bất cứ dữ liệu nào”.** GitHub Pages, đơn vị cung cấp hosting, nêu rõ **địa chỉ IP người truy cập được ghi và lưu cho mục đích an ninh**, bất kể có tài khoản GitHub hay không. Ngoài ra, trình duyệt/nhà mạng và trang bên ngoài bạn tự nhấn liên kết có thể xử lý dữ liệu theo chính sách của họ.

Nguồn nền tảng: [GitHub Pages — Data collection](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) · [GitHub General Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).

## 2. Bảng dòng dữ liệu hiện có

| Hoạt động | Dữ liệu | Hệ thống xử lý | Mục đích | HAI ĐẤT có lưu cơ sở dữ liệu người xem? |
|---|---|---|---|---|
| Mở trang web | Địa chỉ IP/metadata mạng theo vận hành hosting | **GitHub Pages** và hạ tầng hỗ trợ | Truyền trang, bảo vệ an ninh | **Không** có dữ liệu log IP trong repo do HAI ĐẤT tự lưu; GitHub có log độc lập |
| Tìm tên/nhóm/dị bản/hệ câu | Từ khóa và lựa chọn bộ lọc | JavaScript trong trình duyệt | Hiển thị kết quả phù hợp | **Không**, trong mã đang có |
| Tải danh mục và sổ câu | Yêu cầu HTTP đến các tệp `catalog.json`, `phrase_index.json` | GitHub Pages | Cung cấp dữ liệu công khai cho trang | **Không** theo ứng dụng; có thể có log HTTP phía hosting |
| Mở nguồn PDF/GitHub/website tham khảo | URL bạn chọn và dữ liệu mà website đích xử lý | **Bên thứ ba** | Xem tư liệu/báo lỗi | Không mặc định; đọc chính sách của trang đích |
| Gửi Issue/Pull Request trên GitHub | Nội dung và hồ sơ tài khoản bạn công khai trên GitHub | **GitHub** | Thảo luận, phản biện, đóng góp | Nội dung Issue/PR trong repo **có thể công khai và lưu theo lịch sử GitHub** |
| Liên hệ riêng với chủ dự án | **Chưa có kênh riêng chính thức được xác minh/cấu hình** | Chưa xác định | Tiếp nhận vấn đề nhạy cảm | Chưa có cơ sở để mô tả là đã vận hành |

**Không lưu tên, email, tài khoản, vị trí, giọng nói hay ảnh riêng của người học** vì chưa có chức năng này. Không suy rằng thông tin về nghệ nhân xuất hiện trong nguồn công khai đương nhiên được dùng để nhận diện, quảng cáo, giọng AI hay khai thác thương mại.

## 3. Dữ liệu người đóng góp

Khi bạn tự gửi Issue, PR hoặc bình luận, hệ thống GitHub có thể hiển thị tài khoản, nội dung, thời điểm và lịch sử thay đổi theo cài đặt/điều khoản GitHub. **Không đăng vào Issues công khai**: số điện thoại, địa chỉ nhà, giấy tờ định danh, bệnh án, tài khoản, mã khóa, hợp đồng bản quyền chưa công bố, dữ liệu trẻ em, bản thu riêng hoặc giấy tờ cá nhân người biểu diễn.

Muốn phản ánh dữ liệu bị đăng nhầm, hãy báo tại [Issues](https://github.com/Form997/Vong-co/issues) **chỉ bằng mô tả không nhạy cảm** và đề nghị thiết lập đường trao đổi kín. Chủ dự án **chưa công bố email liên hệ bảo mật đã xác minh**, nên chính sách này không bịa địa chỉ hay cam kết phản hồi qua hộp thư không tồn tại.

## 4. Cơ sở pháp lý và địa bàn áp dụng

Tại Việt Nam, khi dự án xử lý dữ liệu cá nhân theo tư cách chủ thể chịu điều chỉnh, phải xem [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15](https://vanban.chinhphu.vn/?docid=215855&pageid=27160) (hiệu lực 01/01/2026) và [Nghị định 356/2025/NĐ-CP](https://vanban.chinhphu.vn/?docid=216387&pageid=27160), cùng các quy định áp dụng khác. Phạm vi quyền/nghĩa vụ **phụ thuộc vai trò, dữ liệu, địa bàn và hoạt động thực tế**, không vì trang miễn phí mà tự miễn trừ.

Khi chủ động phục vụ/giám sát người tại EU, đánh giá [GDPR Điều 3](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (kể cả dịch vụ miễn phí); **website có thể truy cập ở EU không tự động đủ** để kết luận áp dụng ngoại lãnh thổ. Đối với Anh/những nước khác, đánh giá riêng theo từng phạm vi.

## 5. Cookie, lưu trữ thiết bị, bên thứ ba

**Mã HAI ĐẤT đang triển khai** không viết cookie/localStorage, không gắn Google Analytics, Meta Pixel hay trình quảng cáo. Điều này **không phải** cam kết rằng GitHub hay trình duyệt không dùng bất kỳ công nghệ/log nào. Nếu gắn phân tích, nhúng trình phát bên thứ ba, captcha, mạng xã hội hoặc SDK sau này, phải cập nhật chính sách này **trước khi bật tính năng** và thiết lập cơ chế chấp thuận theo địa bàn nếu cần.

Link ngoài chuyển bạn sang website khác; chính sách tại đó điều chỉnh cách họ xử lý dữ liệu.

## 6. Bảo mật, lưu giữ và quyền của người dùng

- Mã ứng dụng không tạo cơ sở dữ liệu người dùng và không đặt dữ liệu tìm kiếm vào repo.
- Hạ tầng GitHub Pages duy trì log an ninh **theo chính sách/lịch lưu trữ của GitHub**; HAI ĐẤT không kiểm soát thời hạn này và không cam kết có thể xóa log của nhà cung cấp từ repository.
- Vấn đề tài khoản GitHub, log nền tảng hoặc quyền riêng tư liên quan GitHub: xem [GitHub privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement) và kênh hỗ trợ của họ.
- Nếu nội dung PR/Issue công khai của bạn có dữ liệu cá nhân bị lộ, liên hệ quản trị qua mô tả **không lộ thêm thông tin** để xử lý theo quyền và khả năng của repository; GitHub có các lưu vết/lịch sử riêng cần được xem xét.

## 7. Trẻ em và tính năng sắp thêm

Website hiện không chủ động tạo hồ sơ trẻ em, thu thông tin về lứa tuổi hoặc phát triển sản phẩm hướng tới thu dữ liệu trẻ nhỏ. **Không xây tính năng thu dữ liệu của trẻ em** trước khi kiểm nghĩa vụ đồng ý/đại diện, bảo vệ trẻ em và luật địa phương (ví dụ COPPA của Hoa Kỳ khi thuộc phạm vi). Với người học nhỏ tuổi, việc truy cập website không đồng nghĩa đồng ý thu dữ liệu cá nhân.

## 8. Khi mở tài khoản, lớp học có thu phí hoặc AI

Các thay đổi như **đăng nhập/đăng ký, thanh toán, ghi điểm, theo dõi bài học, gửi bình luận, upload audio/ảnh, gợi ý AI theo người học, voice clone, phân tích hành vi** phải trải qua đánh giá tác động về riêng tư/luật/bảo mật trước khi phát hành. Cần xác định bên xử lý dữ liệu, các mục đích, cơ sở xử lý, nơi lưu trữ, thời hạn xóa, yêu cầu của chủ thể, danh sách nhà cung cấp, lưu/chuyển dữ liệu xuyên biên giới, trẻ em và thủ tục sự cố tương ứng.

**Không có tính năng đó hôm nay** nên không dùng mẫu cookie banner hay ô “Tôi đồng ý” giả để tạo cảm giác đã tuân thủ.

## 9. Cập nhật chính sách và liên hệ

Phiên bản văn bản này được theo dõi tại repository GitHub bằng lịch sử commit. Khi tính năng hoặc nhà cung cấp thay đổi, phải sửa trước khi triển khai. Xem [SECURITY.md](SECURITY.md) cho cách báo lỗ hổng bảo mật, [quy chế pháp lý](docs/phap-ly-an-ninh-mang-v3.2.md) và [nguồn văn bản](data/v3_2/legal_sources.json).

**Giới hạn:** chính sách này mô tả **hệ thống đã kiểm qua mã nguồn** và các bên ngoài được biết; không phải đánh giá kiểm toán toàn bộ hệ thống GitHub hoặc chứng nhận GDPR/luật Việt Nam.
