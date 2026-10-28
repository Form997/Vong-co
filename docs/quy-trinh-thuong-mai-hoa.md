# CỔNG KIỂM SOÁT THƯƠNG MẠI HÓA — HAI ĐẤT V3.2

**Mã:** HD-COMMERCE-GATE-3.2.1 · **Rà soát:** 29/10/2026.  
**Trạng thái quyết định hiện tại:** **NO-GO — không mở kinh doanh hoặc giao dịch trên website V3.2**.  
**Lưu ý:** Phi thương mại hiện tại không miễn luật bảo vệ dữ liệu, an ninh mạng hoặc quyền tác giả. Dự án không tự tuyên bố mọi hoạt động thương mại là bất hợp pháp; chúng cần đáp ứng luật, giấy phép và nền tảng áp dụng.

## A. Các mô hình khác nhau phải phân loại trước

| Mô hình | Ví dụ HAI ĐẤT | Trạng thái hiện tại | Kiểm tra chính |
|---|---|---|---|
| **Tra cứu phi thương mại** | 20 bản Tổ, nguồn V2, 72 nhãn câu | **Đang vận hành** | Nguồn, quyền tác giả, an ninh và quyền riêng tư |
| **Nhận ủng hộ không đổi quyền sử dụng** | Donation/crowdfunding | **Chưa tích hợp** | Theo chính sách GitHub Pages có thể cho phép một số hình thức quyên góp; kiểm thuế/điều khoản; không tự suy miễn nghĩa vụ |
| **Quảng cáo, affiliate, tài trợ** | Logo/đường dẫn có trả phí | **Chưa tích hợp** | Chính sách host, nội dung quảng cáo, người tiêu dùng, nghĩa vụ thuế, dữ liệu/trackers nếu có |
| **Khóa học trả phí/sản phẩm số** | Bán quyền xem bài/âm thanh/ký âm | **NO-GO cho tới khi duyệt** | Chủ thể kinh doanh, quyền tư liệu, bảo vệ người dùng, điều kiện website thương mại, thuế/hóa đơn |
| **SaaS/API/gói doanh nghiệp** | Thu phí AI, MCP, API dữ liệu | **NO-GO** | GitHub Pages không phù hợp làm hosting e-commerce/SaaS chính; chuyển hạ tầng, hợp đồng API, giấy phép dữ liệu, an ninh |
| **Thu giọng/ảnh học viên để AI ca** | Giọng hát, voice clone, chấm luyện | **NO-GO** | Thẩm định dữ liệu nhạy cảm, quyền nhân thân, consent, mô hình AI và lưu trữ an toàn; đặc biệt trẻ em |

Nguồn nền tảng bắt buộc kiểm: [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) và [GitHub Terms for Additional Products and Features](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features). Một số hình thức donation/crowdfunding **có thể được phép** trên Pages; không đánh đồng với việc được hosting một hệ thống thanh toán/thuê bao chủ yếu vì mục tiêu thương mại.

## B. Mẫu hồ sơ quyết định (chưa thể mặc định đánh dấu đạt)

| Mã | Cổng đánh giá | Người chịu trách nhiệm / bằng chứng cần có | Kết quả mặc định |
|---|---|---|---|
| G01 | Đơn vị vận hành có tư cách phù hợp, thông tin liên hệ hợp lệ | Hồ sơ chủ thể kinh doanh, đăng ký/thuế theo từng nơi | **CHƯA THẨM ĐỊNH** |
| G02 | Mô tả sản phẩm/dịch vụ, đối tượng người dùng, quốc gia phục vụ | Hồ sơ tính năng, trang giao dịch, điều khoản | **CHƯA THẨM ĐỊNH** |
| G03 | Phân loại loại website TMĐT, nghĩa vụ thông báo/đăng ký khi thuộc phạm vi | Đối chiếu Luật TMĐT 122/2025 và NĐ 248/2026, cơ quan có thẩm quyền | **CHƯA THẨM ĐỊNH** |
| G04 | Quyền mã nguồn, sách/ký âm, lời ca, ảnh, nhạc cụ, bản thu | Bảng phân tích quyền từng thành phần; giấy phép hợp lệ | **CHƯA THẨM ĐỊNH** |
| G05 | Giấy phép phạm vi **thương mại**, sửa đổi, truyền phát, sublicensing, AI | Hợp đồng/quyền liên quan đúng phạm vi/vùng/thời hạn | **CHƯA THẨM ĐỊNH** |
| G06 | Luật bảo vệ người tiêu dùng: giá, điều kiện, hoàn tiền, khiếu nại | Bộ điều khoản thực tế, đầu mối xử lý | **CHƯA THẨM ĐỊNH** |
| G07 | Thuế, thanh toán, hóa đơn, xử lý gian lận và hoàn tiền | Hợp đồng nhà cung cấp thanh toán và nghĩa vụ thuế | **CHƯA THẨM ĐỊNH** |
| G08 | Quyền riêng tư và dữ liệu: thông báo, cơ sở, đánh giá tác động, xóa dữ liệu | Bảng luồng dữ liệu, hợp đồng xử lý, sổ yêu cầu và sự cố | **CHƯA THẨM ĐỊNH** |
| G09 | An ninh: MFA, nhật ký, quyền tối thiểu, backup, pentest phù hợp | Kiểm thử và hồ sơ triển khai thực tế | **CHƯA THẨM ĐỊNH** |
| G10 | Trẻ em (nếu có), giáo dục/đào tạo và rủi ro xuyên biên giới | Đánh giá từng địa bàn, trách nhiệm đối với người học | **CHƯA THẨM ĐỊNH** |
| G11 | Hạ tầng đáp ứng quy mô, giao dịch, tính sẵn sàng | Website thương mại **không chạy như e-commerce/SaaS chính trên Pages** | **CHƯA THẨM ĐỊNH** |
| G12 | Phê duyệt cuối và liên hệ vận hành công khai | Biên bản được người có trách nhiệm ký; phiên bản/cửa sổ phát hành | **CHƯA THẨM ĐỊNH** |

**Quy tắc không được vượt rào:** Không lấy CI xanh, logo UNESCO, README nhiều nguồn, mật khẩu tài khoản GitHub, hoặc tệp `license` giả để thay cho G01–G12. **Mặc định `commercial_enabled = false`** cho tới khi chủ dự án kiểm định mọi mục liên quan và ghi hồ sơ rõ, không tự bật bằng commit.

## C. Danh mục pháp lý cần kiểm theo nơi triển khai

**Việt Nam (đã đối chiếu số văn bản và hiệu lực tại thời điểm rà soát):**
- [Luật TMĐT 122/2025/QH15](https://vanban.chinhphu.vn/?docid=216503&pageid=27160): 01/07/2026.
- [Nghị định 248/2026/NĐ-CP](https://vanban.chinhphu.vn/?docid=218747&pageid=27160): 01/07/2026.
- [Luật An ninh mạng 116/2025/QH15](https://vanban.chinhphu.vn/?docid=216499&pageid=27160): 01/07/2026.
- [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15](https://vanban.chinhphu.vn/?docid=215855&pageid=27160) và [Nghị định 356/2025/NĐ-CP](https://vanban.chinhphu.vn/?docid=216387&pageid=27160): 01/01/2026.
- [Luật sửa đổi Luật SHTT 131/2025/QH15](https://vanban.chinhphu.vn/?docid=216511&pageid=27160): 01/04/2026.

Đánh giá **còn cần** xác định loại hình và nghĩa vụ cụ thể về đăng ký, thông báo, thương mại điện tử, bảo vệ người tiêu dùng, quảng cáo, hóa đơn và thuế. Chỉ có một địa chỉ `github.io` không xác định được tất cả nghĩa vụ.

**EU:** nếu thực sự tiếp cận thị trường và có hoạt động thuộc phạm vi GDPR/DSA/AI Act, kiểm luật hợp nhất tại ngày ra mắt, đánh giá controller/processor, quốc gia, trẻ em, chuyển dữ liệu và quyền ảnh/giọng. **UK, Hoa Kỳ, Nhật Bản, Singapore, Trung Quốc, Úc và các nơi khác:** phải đánh giá riêng theo nơi có khách hàng, hợp đồng và dữ liệu; không đóng dấu “đã tuân thủ luật toàn cầu”.

## D. Cách tổ chức phát hành thương mại an toàn

1. Tạo **môi trường thử nghiệm thương mại riêng**, không ghi mật khẩu/thẻ vào HTML/JS của GitHub Pages.
2. Chỉ đưa **nội dung có quyền công bố phù hợp**; ký âm/lời ca/audio có quyền chưa xác minh bị loại khỏi sản phẩm.
3. Nhà cung cấp thanh toán chịu phần xử lý thẻ theo hợp đồng và chuẩn áp dụng; **không tự tạo form lấy dữ liệu thẻ** trên web tĩnh.
4. Tạo nhật ký xử lý dữ liệu và cơ chế người dùng thực sự: privacy notice, điều khoản, đơn hàng, hỗ trợ, yêu cầu/xóa dữ liệu, sự cố.
5. Kiểm luật đúng lãnh thổ trước khi quảng cáo/cho thanh toán xuyên biên giới; đánh giá thêm điều khoản nền tảng.
6. Kiểm chứng end-to-end, kiểm bảo mật, kiểm hoàn tiền và trải nghiệm người dùng.
7. Có **biên bản phê duyệt** ghi ngày, SHA mã, pháp nhân, thị trường, phạm vi tài sản, giấy phép và người chịu trách nhiệm. Nếu thiếu, **NO-GO**.

## E. Mẫu biên bản đánh giá thương mại hóa

```text
HAI ĐẤT — BIÊN BẢN GO / NO-GO
Ngày đánh giá: ...
Commit SHA: ...
Tổ chức/đơn vị vận hành: ...
Thị trường người dùng dự kiến: ...
Phương thức thu tiền: ...
Nhóm tác phẩm/giấy phép đã xác minh: ...
Kết quả G01 ... G12: ...
Rủi ro/công việc chưa xử lý: ...
Kết luận: NO-GO / GO (chỉ cho phạm vi được phê duyệt)
Người chịu trách nhiệm / người thẩm định: ...
Tài liệu, giấy phép, bản kiểm thử đính kèm: ...
```

**Bản V3.2 hiện tại:** `NO-GO` đối với tất cả phương thức thương mại chưa được thẩm định, kể cả cấp API trả phí và phân phối bản ghi. Định nghĩa “không thương mại” chỉ mô tả mô hình hiện tại; không phải một giấy phép bản quyền.

Xem [Chính sách tổng thể](phap-ly-an-ninh-mang-v3.2.md) · [RIGHTS_AND_LICENSING.md](../RIGHTS_AND_LICENSING.md) · [SECURITY.md](../SECURITY.md) · [PRIVACY.md](../PRIVACY.md).
