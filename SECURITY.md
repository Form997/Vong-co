# CHÍNH SÁCH BẢO MẬT — HAI ĐẤT V3.2

**Phiên bản:** HD-SECURITY-3.2.1 · **Cập nhật:** 29/10/2026  
**Phạm vi:** mã nguồn, JSON, giao diện web GitHub Pages, GitHub Actions và quy trình phát hành của [Form997/Vong-co](https://github.com/Form997/Vong-co).  
**Mức bảo đảm:** kiểm thử phần mềm và quy trình quản lý mã; **không tuyên bố đã đạt chứng nhận ISO 27001, NIST, cơ quan nhà nước hoặc kiểm toán độc lập**.

## 1. Báo cáo lỗ hổng an toàn

**Không công khai trên GitHub Issues hoặc Pull Requests:** khóa API, token truy cập, mật khẩu, ảnh giấy tờ, thông tin cá nhân, PoC đang khai thác, payload nguy hiểm, đường dẫn dữ liệu bí mật hoặc hướng dẫn giúp tấn công hệ thống.

Hãy kiểm tra [GitHub Security Advisories của repository](https://github.com/Form997/Vong-co/security/advisories) xem có nút **Report a vulnerability**. Tính năng nhận báo cáo riêng tư phụ thuộc việc chủ repository bật **Private vulnerability reporting** trong Settings → Security. **Không cam kết chức năng này đã được bật**. Nếu chưa có, chỉ gửi [Issue mô tả phi nhạy cảm](https://github.com/Form997/Vong-co/issues) yêu cầu chủ dự án cung cấp kênh trao đổi kín; tuyệt đối không gửi chi tiết có thể bị khai thác vào Issue.

**Mẫu thông báo an toàn (sau khi có kênh kín):** mô tả tác động; URL/file/commit bị ảnh hưởng; điều kiện tái hiện **không gây hại**; phiên bản; thời điểm phát hiện; đề nghị cách khắc phục; cách liên hệ không chứa bí mật trong repo. Không thử tấn công người dùng khác hoặc hệ thống không do mình sở hữu.

## 2. Phạm vi sản phẩm và mô hình đe dọa

Hệ thống hiện là trang tĩnh HTML/CSS/JavaScript và dữ liệu JSON tĩnh do GitHub Pages phục vụ. Không có backend cấp token, đăng nhập của ứng dụng, thanh toán, cơ sở dữ liệu người học hay API tải tệp từ người dùng.

Các đe dọa cần kiểm soát:

| Nguy cơ | Cơ chế đã có / cần duy trì | Điều chưa thể bảo đảm |
|---|---|---|
| JSON/tên/ghi chú gây XSS | Kiểm định JSON trước build, escape HTML trên trang sinh; giao diện dùng `textContent`/DOM API | Không thay cho pentest độc lập; phải thử dữ liệu mới |
| Tệp bí mật lọt lên Pages | Bộ đóng gói **allowlist** chỉ nhận HTML/JSON/schema/robots/sitemap; kiểm đếm file | Phải kiểm lại allowlist khi thêm file |
| Kho nguồn bị chiếm hoặc PR độc hại | Branch protection, quyền thành viên tối thiểu, quy trình Pull Request và CI | Chủ kho cần cấu hình thực tế 2FA, quyền và rule |
| Token/secret trong GitHub Actions | Workflow chỉ cấp `contents:read` ở build, `pages:write` + `id-token:write` ở Deploy | Trách nhiệm của admin quản lý secrets, OIDC/permissions |
| Action bên thứ ba bị đổi mã | Ưu tiên pin hành động vào **commit SHA đã kiểm** và kiểm cập nhật định kỳ; bản hiện tại còn dùng tag phiên bản `@v4`/`@v5` nên **chưa đạt độ pin SHA cao nhất** | Không được quảng cáo “supply chain hardened hoàn toàn” |
| Website bị giả mạo/đổi miền | Domain `form997.github.io/Vong-co/`, HTTPS do GitHub Pages hỗ trợ; kiểm nguồn của từng liên kết ngoài | Không kiểm soát hạ tầng GitHub và mọi bên thứ ba |
| Tải lại nhạc/PDF chưa rõ quyền | Không đưa PDF/MP3/ca từ/score vào artifact, không tự tạo ký âm | Giải quyết pháp lý nội dung tách khỏi an ninh kỹ thuật |
| Sai thông tin nghiên cứu | 60+ kiểm thử Python và Chromium, đối chiếu 72 nhãn với sổ V2 | Không đồng nghĩa nghệ nhân đã nghiệm thu nhạc |
| DoS/lưu lượng bất thường | GitHub vận hành hosting và có hạn mức/rate limit | Dự án không tự quản WAF, IP logs hoặc server runtime |

## 3. Kiểm soát thay đổi và phát hành

1. Mọi tính năng, file JS, quyền mới, pháp lý mới hoặc nguồn dữ liệu mới phải có ghi chú thay đổi.
2. GitHub Actions kiểm: dữ liệu V3/V3.2, liên kết nội bộ, Python tests, kiểm cú pháp JS và Chromium 360–1366 px.
3. Không tự ý sửa `v1-frozen`, `v2-development` hay `main`; phát triển trên nhánh riêng và merge vào `v3-development` sau CI.
4. Pages deploy **chỉ** từ `v3-development`, chỉ khi `HAI_DAT_PAGES_ENABLED = true`, môi trường `github-pages` cho phép và build đạt.
5. Mã website và JSON được đưa vào gói theo allowlist cố định. Khi thêm `legal.html` hay file chính sách phải cập nhật phép kiểm đếm và test rò rỉ.
6. Không biến thất bại/skipped thành thông báo triển khai thành công. Lưu link run, commit SHA, số tệp và dung lượng.
7. Cấm đặt token/email riêng/giấy tờ người dùng trong mã, YAML hoặc README. Nếu phát hiện, phải **thu hồi/rotate ngay**, xem lại lịch sử Git và cache/artifact — xóa ở commit mới không đủ bảo đảm đã xóa bản cũ.

## 4. Biện pháp quản trị phải được chủ dự án xác nhận

- [ ] Bật **2FA/MFA** cho tài khoản GitHub và email khôi phục phù hợp.
- [ ] Bảo vệ `main` và `v1-frozen`; xem thêm rule cho nhánh triển khai.
- [ ] Dùng tối thiểu hai mắt kiểm PR quan trọng khi có người cộng tác; tránh tự duyệt thay đổi nhạy cảm khi có thể.
- [ ] Không cấp PAT quyền rộng nếu GitHub App/OIDC/permissions tối thiểu đủ dùng.
- [ ] Bật **private vulnerability reporting** và xác minh người quản trị có kênh kín.
- [ ] Bật Dependabot alerts/secret scanning **nếu gói và repository hỗ trợ**, xem lại định kỳ.
- [ ] Pin critical GitHub Actions về SHA bất biến theo quy trình và theo dõi bản sửa lỗi.
- [ ] Đánh giá GitHub Pages branch/env/rules, xem ai được chỉnh biến `HAI_DAT_PAGES_ENABLED`.
- [ ] Kiểm sao lưu và phục hồi repository; bảo vệ bản V1 đóng băng.

Checkbox chưa được xác minh nghĩa là **công việc quản trị**, không phải tính năng đã bật.

## 5. Quy trình tiết lộ có trách nhiệm

Nếu được nhận báo cáo riêng, quản trị viên phân loại tác động, giữ bằng chứng tối thiểu, giảm thiệt hại, sửa qua PR, kiểm lại CI, phát hành bản sửa và công bố thông tin kỹ thuật đã được loại bỏ bí mật. Không đưa danh tính người báo cáo hoặc dữ liệu nạn nhân ra công khai khi không có cơ sở hợp pháp.

**Thời hạn đáp ứng:** không tự cam kết một mốc cố định khi chưa có tổ chức trực vận hành. Thời hạn **phải thông báo cơ quan/người liên quan** (nếu đủ điều kiện) do pháp luật từng nơi và loại sự cố quyết định; ví dụ GDPR Điều 33 có cơ chế 72 giờ cho trường hợp áp dụng. Xem [quy trình ứng phó sự cố](docs/quy-trinh-ung-pho-su-co.md).

## 6. Nguyên tắc an ninh quốc tế

Tham chiếu khung **NIST CSF 2.0: Govern–Identify–Protect–Detect–Respond–Recover** và **OWASP Top 10** như hướng thực hành tự nguyện. Không gọi tài liệu này là giấy phép hoạt động, chứng nhận an ninh mạng Việt Nam hoặc chứng nhận “đủ luật toàn cầu”.

Quy định bắt buộc chỉ xác định khi có quan hệ pháp lý/thị trường cụ thể; xem [docs/phap-ly-an-ninh-mang-v3.2.md](docs/phap-ly-an-ninh-mang-v3.2.md).

## 7. Khiếu nại bản quyền không phải báo lỗ hổng

Sai nguồn, quyền sao chép ký âm/ca từ/audio, thông tin cá nhân trong bài và tấn công phần mềm là **các loại vụ việc khác nhau**. Xem [RIGHTS_AND_LICENSING.md](RIGHTS_AND_LICENSING.md) và [PRIVACY.md](PRIVACY.md).

**Nâng cấp trước khi mở thương mại:** kiểm thử bảo mật độc lập nếu rủi ro phù hợp, xác định tổ chức chịu trách nhiệm, thủ tục bảo vệ dữ liệu và nghĩa vụ thông báo, hạ tầng phù hợp (GitHub Pages không phù hợp làm nền tảng giao dịch thương mại chính). Không chuyển lời cam kết trong tài liệu thành nhận định hệ thống đã có khả năng thực hiện.
