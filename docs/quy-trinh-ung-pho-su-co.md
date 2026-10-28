# QUY TRÌNH ỨNG PHÓ SỰ CỐ — AN NINH MẠNG, DỮ LIỆU VÀ QUYỀN TÁC GIẢ HAI ĐẤT V3.2

**Mã:** HD-IR-3.2.1 · **Ngày rà soát:** 29/10/2026.  
**Vai trò:** tài liệu vận hành nội bộ cho kho GitHub Pages phi thương mại. **Không mặc nhiên là quy trình thông báo đủ điều kiện pháp luật**; khi có sự cố thực tế, phải xác định đúng bên kiểm soát/xử lý dữ liệu, người bị ảnh hưởng, lãnh thổ, cơ quan và thời hạn luật yêu cầu.

## 1. Ai có thể khởi động xử lý?

- **Chủ repository/quản trị viên được ủy quyền**: phân công người điều phối và người ra quyết định công bố/tạm dừng.
- **Người phát hiện/đóng góp**: báo qua kênh riêng theo [SECURITY.md](../SECURITY.md) nếu là lỗi kỹ thuật/nhạy cảm; với sai nguồn thông thường có thể tạo GitHub Issue không chứa dữ liệu cá nhân.
- **Chuyên gia pháp lý / bảo vệ dữ liệu / quyền tác giả / nghệ nhân**: tham gia khi đúng loại sự cố và có cơ sở liên hệ phù hợp.

**Không công khai mật khẩu, token, số điện thoại, giấy tờ, bản scan quyền, bằng chứng cá nhân hoặc phương pháp tấn công trên GitHub Issues.** Hiện repository chưa xác minh kênh nhận báo cáo riêng được bật; khi chưa có, dùng mô tả không nhạy cảm để xin kênh kín.

## 2. Ma trận phân loại

| Loại sự cố | Dấu hiệu | Ưu tiên | Hành động đầu |
|---|---|---|---|
| **SEC-CRITICAL** | Lộ token có quyền ghi, bị chiếm tài khoản, deploy mã bị chèn, lộ thông tin đăng nhập, tấn công đang diễn ra | Khẩn cấp | Thu hồi token, khóa quyền/secret, hạn chế deploy, giữ chứng cứ tối thiểu |
| **PRIVACY** | Dữ liệu cá nhân hoặc bản ghi riêng tư bị đưa lên công khai, URL có thông tin nhạy cảm | Khẩn cấp tùy mức độ | Hạn chế hiển thị, rà lịch sử Git và nhà cung cấp, đánh giá nghĩa vụ thông báo |
| **COPYRIGHT** | PDF, ký âm, ca từ, bản thu hoặc giọng nghệ nhân bị xuất bản chưa có quyền | Cao tùy mức độ | Khoanh đúng URL/tệp, cân nhắc tạm gỡ, xác minh quyền và khiếu nại |
| **SOURCE-INTEGRITY** | Thêm sai số câu/trang, trộn hệ 32/4 với 16/8, tự tuyên bố nghệ nhân đã nghiệm thu | Cao về học thuật | Tạm ngừng phát hành nội dung sai, mở issue kiểm nguồn không lộ dữ liệu |
| **AVAILABILITY** | Pages 404/429, lỗi JSON, workflow Fail, mất quyền môi trường | Theo tác động | Xác minh status GitHub, kiểm commit/run và đường dẫn; rollback khi cần |
| **FRAUD/IMPERSONATION** | Trang giả mạo HAI ĐẤT, xin tiền thay mặt dự án, mượn danh cơ quan/UNESCO | Cao | Lưu bằng chứng công khai, báo nền tảng, thông báo phòng tránh không lộ thông tin người bị hại |

## 3. Sáu bước thực hiện

### Bước 1 — Ghi nhận và phân loại

Ghi **mã vụ việc, thời điểm Việt Nam UTC+7 và UTC, người chịu trách nhiệm, nguồn báo, URL/commit/run, tác động thực tế hay nghi ngờ, độ tin cậy**, phạm vi dữ liệu/tác phẩm bị ảnh hưởng. Tách **sự cố kỹ thuật** và **sai lệch nghiên cứu**; không đánh đồng mọi lỗi chính tả với sự cố an ninh quốc gia.

### Bước 2 — Khoanh vùng, giới hạn thiệt hại

- Với tài khoản bị chiếm: thu hồi/rotate token, đổi mật khẩu phù hợp, kiểm 2FA, hạn chế quyền thành viên và thay đổi branch/environment.
- Với website bị chèn nội dung: tạm ngừng deploy, đưa phiên bản lành trước đó lên Pages nếu an toàn và được quyền, hoặc tạm gỡ chức năng lỗi.
- Với quyền tác giả/riêng tư: cân nhắc **ẩn/gỡ đúng nội dung**, bảo vệ bằng chứng và quyền của chủ thể; kiểm mọi bản sao trong commit, artifact, cache và kho công khai.
- Khi nghi sự cố từ GitHub hạ tầng: xem [GitHub Status](https://www.githubstatus.com/) và báo GitHub Support theo quyền tài khoản.
- Không xóa log/chứng cứ bừa bãi hoặc chạy thử khai thác trên tài khoản người khác.

### Bước 3 — Bảo toàn bằng chứng tối thiểu

Lưu trong nơi hạn chế truy cập (không phải repo public): SHA, hash nội dung, ảnh/mốc log cần thiết, các lần quyền bị thay đổi, biên bản quyết định. Chỉ giữ dữ liệu tối thiểu phục vụ điều tra và nghĩa vụ áp dụng; hạn chế truy cập theo vai trò, có lịch xóa dữ liệu nhạy cảm sau khi hết mục đích hợp pháp. Không upload lên Issues công khai.

### Bước 4 — Đánh giá nghĩa vụ pháp lý và thông báo

**Không đặt thời hạn 72 giờ chung cho mọi sự cố ở Việt Nam và thế giới.** Tùy loại dữ liệu, địa bàn, vai trò chủ thể, ngành và quy định đang hiệu lực:

- **Việt Nam:** đối chiếu [Luật An ninh mạng 116/2025/QH15](https://vanban.chinhphu.vn/?docid=216499&pageid=27160), [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15](https://vanban.chinhphu.vn/?docid=215855&pageid=27160), [Nghị định 356/2025/NĐ-CP](https://vanban.chinhphu.vn/?docid=216387&pageid=27160) và hướng dẫn/cơ quan tương ứng. Chỉ lập hồ sơ thông báo khi thuộc trường hợp nghĩa vụ thực sự phát sinh.
- **EU:** [GDPR Điều 33](https://eur-lex.europa.eu/eli/reg/2016/679/oj) có nguyên tắc thông báo cơ quan giám sát **không chậm trễ và, khi khả thi, trong 72 giờ kể từ biết vi phạm** nếu đủ điều kiện của điều luật; Điều 34 về thông báo chủ thể khi rủi ro cao với điều kiện/ngoại lệ áp dụng. Không dùng quy tắc này như nghĩa vụ mặc định của mọi website Việt Nam.
- **Thư viện bên thứ ba:** nếu GitHub/nhà cung cấp có sự cố hạ tầng, phân định rõ trách nhiệm của hosting và trách nhiệm của bên vận hành dự án. Không hứa xóa log IP do GitHub nắm giữ.

Đánh giá trường hợp cần báo cơ quan chức năng, chủ thể dữ liệu, người nắm bản quyền, người dùng, khách hàng hoặc nền tảng; xác định **ai báo, nội dung được phép công khai, thời hạn luật định cụ thể, người phê duyệt**. Nếu không chắc, hỏi tư vấn pháp lý/chuyên trách trước khi đưa thông tin nhạy cảm ra công chúng.

### Bước 5 — Khắc phục, kiểm chứng và khôi phục

Mở nhánh sửa riêng, kiểm dữ liệu V3/V3.2, test negative cases, kiểm JavaScript, Chromium và Pages. Kiểm lại nguồn/giấy phép nếu sự cố là nội dung. Giữ dấu vết phiên bản lỗi và lý do phục hồi; không tuyên bố đã khôi phục khi mới chạy Build Success nhưng Deploy Failed/Skipped.

### Bước 6 — Tổng kết và phòng ngừa

Biên bản postmortem tối thiểu gồm: nguyên nhân đã chứng minh, tác động, thời gian, bằng chứng (đã khử dữ liệu nhạy cảm), quyết định kỹ thuật/pháp lý, ai phê duyệt, đào tạo và test cần bổ sung, thời điểm rà lại. Công bố bản công khai có chọn lọc để bảo vệ người dùng và quyền tài sản.

## 4. Kịch bản cụ thể để tập diễn tập

**Kịch bản A — Token GitHub bị lộ:** thu hồi token ngay; kiểm branch/Actions/Pages, đổi secret, xem commit/audit logs, kiểm mã website bị chèn; cấm tiếp tục dùng token cũ; chỉ tái triển khai từ commit đã đối chiếu.

**Kịch bản B — Tệp PDF/bản thu chưa có quyền vào artifact:** tạm ẩn tệp vi phạm, kiểm toàn bộ Pages artifact, báo chủ thể quyền khi thích hợp, xác minh giấy phép. Thêm trường hợp regression test chặn `.pdf/.mp3/.wav/.mid`.

**Kịch bản C — Sai nguồn 40 câu/nhịp tám:** xác định đúng hệ, kiểm bảng V2, sửa có biên bản, chạy đủ validator 72 câu, không áp phép đổi nhịp hoặc ghi “đã được nghệ nhân xác nhận”.

**Kịch bản D — Gửi Issue chứa giấy tờ cá nhân:** hạn chế hiển thị nội dung qua chức năng quản trị phù hợp, không repost vào báo cáo, hướng dẫn người gửi sử dụng kênh kín, xem lịch sử GitHub và quyền xóa theo nhà cung cấp.

**Kịch bản E — Website nhận traffic bất thường/404:** xem GitHub Status và hạn mức Pages; kiểm deploy workflow, DNS/HTTPS và URL thực tế. Không tự suy đó là tấn công nếu thiếu bằng chứng.

## 5. Mẫu sổ sự cố (không được điền dữ liệu cá nhân vào repo công khai)

```text
Mã sự cố:
Thời gian phát hiện (UTC / UTC+7):
Người điều phối / người được cấp quyền xử lý:
Loại sự cố / mức ưu tiên:
Tệp/URL/commit/run liên quan:
Điều chắc chắn / điều đang nghi ngờ:
Số lượng dữ liệu/tác phẩm liên quan (nếu có bằng chứng):
Biện pháp khẩn cấp đã thực hiện:
Bằng chứng lưu ở kho kín, ai có quyền:
Pháp luật/cơ quan có thể áp dụng (chưa kết luận nếu thiếu):
Đã đánh giá nghĩa vụ thông báo? Ai phê duyệt? Hạn chính xác:
Kết quả khắc phục và kiểm thử:
Ngày đóng sự cố / nguyên nhân gốc / việc phòng ngừa:
```

## 6. Chỉ số theo dõi quy trình, không tuyên bố đạt sẵn

- Tỷ lệ token được bảo vệ và có ngày rà soát.
- Tỷ lệ PR nhạy cảm qua CI và review.
- Tỷ lệ artifact chỉ chứa tệp allowlist.
- Thời gian phản ứng/khoanh vùng đo từ sự cố **có thật**.
- Tình trạng kiểm chứng nguồn và quyền của từng bài; **20/20 hồ sơ mở không phải 20/20 đạt biểu diễn**.

**Dự án chưa chứng minh có nhóm trực sự cố 24/7, SOC, pentest định kỳ, chứng chỉ ISO hoặc thời gian SLA; không ghi đó là cam kết hiện hữu.**

[SECURITY.md](../SECURITY.md) · [PRIVACY.md](../PRIVACY.md) · [RIGHTS_AND_LICENSING.md](../RIGHTS_AND_LICENSING.md) · [Chính sách tổng thể](phap-ly-an-ninh-mang-v3.2.md).
