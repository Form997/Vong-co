# Đóng góp cho HAI ĐẤT — 20 BẢN TỔ

Cảm ơn bạn muốn cùng gìn giữ tư liệu đờn ca tài tử Nam Bộ. Chúng tôi trân trọng nghệ nhân, người học, nhà nghiên cứu, thư viện và người phát triển công nghệ.

> **Nguyên tắc số 1:** Dẫn được nguồn, chỉ rõ dị bản và thừa nhận điều chưa biết có giá trị hơn một kết luận nghe có vẻ hoàn chỉnh.

## Chọn cách đóng góp phù hợp

| Bạn có thể đóng góp | Nên gửi gì? |
|---|---|
| Sửa sai tên bài, số câu, lớp, hơi/nhịp | Tên bản, số câu chính xác, ảnh/trang in có quyền chia sẻ hoặc đường dẫn nguồn và lập luận so sánh |
| Phát hiện sai khác giữa ký âm và lời | Mã bài, câu, nhịp/phách nếu biết, hai nguồn đối chiếu, chỗ không khớp |
| Đưa bản thu hoặc chỉ dẫn nghệ nhân | Tên nghệ sĩ, thời điểm/nơi xuất bản, URL hoặc giấy phép; không tải lại âm thanh khi chưa có quyền |
| Sửa README, Markdown, Python/CI | Nêu lỗi trước/sau, tệp chỉnh, cách kiểm thử đã chạy |
| Đề xuất tích hợp AI/MCP | Cách trích nguồn, giới hạn dữ liệu và biện pháp trả lời “chưa xác minh” |

## Đóng góp V3.2 — một nhãn câu phải có đường trở về nguồn

**Bắt đầu áp dụng 28/10/2026.** Những thay đổi ở `data/v3_2/phrase_index.json` cần kèm **bài + mã hệ + nhãn câu + lớp + dòng bảng V2 + URL/trang in**, không được gộp các hệ Vắn/Trường hoặc nhịp tư/tám. [Quy trình thẩm định](docs/v3.2-quy-trinh-tham-dinh.md) quy định năm tầng tách biệt nguồn → chỉ mục → âm nhạc → thực tấu → quyền.

**Dữ liệu V3.2 hiện chỉ chuẩn hóa 2 hệ (72 nhãn)**. Các bản khác có sổ câu V2 nhưng chưa chuyển thành dữ liệu học công khai; [sổ kiểm toán 20 bài](docs/v3.2-kiem-toan-20-ban.md) ghi tồn đọng. Đừng biến giá trị “Chưa xác minh” thành số trang hoặc nốt nhạc suy đoán.

Mỗi Pull Request cập nhật bài học phải chạy `python scripts/v3_2_validate.py --json`, toàn bộ unittest và Chromium, giữ `performance_status=pending` và `rights_status=unverified` trừ khi có thủ tục thẩm định/giấy phép khác được tài liệu hóa độc lập. Không gửi file âm thanh, scan PDF, toàn văn ký âm/ca từ vào kho khi chưa có quyền.

## Đóng góp pháp lý và báo lỗi bảo mật V3.2

**Không tạo GitHub Issue công khai nếu chứa mật khẩu, khóa, dữ liệu cá nhân, bản thu riêng hoặc hướng dẫn khai thác lỗ hổng.** Đọc [SECURITY.md](SECURITY.md) và xác minh khả năng dùng GitHub **private vulnerability reporting** (chủ repository phải bật; chính sách không nói đã bật sẵn). Với nội dung phi nhạy cảm, Issues có thể được dùng để đề nghị sửa trích dẫn.

Khi đề xuất luật, phải ghi rõ **số hiệu, loại văn bản, ngày hiệu lực, cơ quan ban hành, URL chính thức, lãnh thổ và điều kiện áp dụng**; không gán nhãn “tuân thủ toàn cầu” khi chưa có cơ sở. Xem [chính sách pháp lý V3.2](docs/phap-ly-an-ninh-mang-v3.2.md) và [sổ nguồn văn bản](data/v3_2/legal_sources.json).

Chỉ đề nghị thêm tính năng thanh toán, tài khoản, phân tích người dùng hay dùng bản ghi/giọng AI khi kèm đánh giá **quyền tài sản, quyền riêng tư, an ninh, hạ tầng, giấy phép và cổng phê duyệt thương mại**.

## Gửi lỗi hoặc đề xuất

1. Mở [Issues](https://github.com/Form997/Vong-co/issues/new/choose).
2. Chọn **Đối chiếu nguồn và dị bản** hoặc **Lỗi kỹ thuật và trải nghiệm**.
3. Ghi tên bài, số bài **01–20**, câu/lớp, nguồn có URL và số trang (nếu có), điều bạn phát hiện, cách xác minh.
4. Nếu bằng chứng chỉ là ghi nhớ truyền miệng hoặc nguồn thứ cấp, hãy ghi rõ **mức chưa chắc chắn**. Không hạ thấp giá trị truyền nghề; chỉ phân biệt cấp chứng cứ.

## Pull Request

- **Tư liệu chuyên môn V2:** đề nghị chỉnh trên `v2-development` với nguồn/biên bản; **thay đổi bài học V3.2:** phát triển trên `v3.2-development`, mở Pull Request vào `v3-development` sau khi kiểm thử; **không sửa `v1-frozen`**.
- Mỗi thay đổi V3 về `data/v3/catalog.json` phải giữ **mã hệ bản, đường dẫn biên bản V2, nguồn URL, nhãn chứng cứ, ghi chú giới hạn**; không gộp các hệ câu không tương thích.
- Mỗi Pull Request tập trung một chủ đề để dễ thẩm tra. Ghi các đường dẫn nguồn, những câu chịu ảnh hưởng, và lý do điều chỉnh.
- **Không tự đổi `CHỜ NGHIỆM THU` thành `ĐẠT`** nếu chưa có chứng cứ và người thẩm định chuyên môn phù hợp.
- Khi thay đổi số liệu các thế hệ, cập nhật [Nhật ký V](docs/nhat-ky-phien-ban.md) và thống kê dung lượng theo **commit cụ thể**.
- Chạy kiểm thử (nếu có Python): `python -m unittest discover -s tests -p "test_*.py" -v` và `python -m compileall -q scripts tests`. Kết quả CI xem tại [GitHub Actions V2](https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v2.yml) hoặc [GitHub Actions V3](https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v3.yml). Với V3 chạy thêm `python scripts/v3_validate.py --json` và `python scripts/kiem-tra-lien-ket.py`.

## Quy định trích dẫn

Một thay đổi đủ để xem xét nên có: **định danh bài, hệ bản/dị bản, điều đang khẳng định, nguồn, trang hoặc vị trí trong nguồn, mức kiểm, vấn đề còn mở**. Với chữ nhạc, cần phân biệt **tìm thấy bản chép / xác nhận nhãn câu / thẩm định phách / thẩm định diễn xướng**.

Tài liệu tham khảo chính: [Sổ nguồn](docs/nguon-tham-khao.md) · [Quy chế V2](docs/ke-hoach-v2.md) · [Tổng hợp phát hiện](docs/tong-hop-phat-hien-v2.md).

## Bản quyền và quyền sử dụng

**Kho công khai không có nghĩa mọi nội dung có giấy phép tái sử dụng.** Không đăng nguyên văn lời ca, bản ký âm, MP3, video, ảnh sách hoặc bản dịch có bản quyền khi chưa có quyền hợp lệ. Đặt liên kết và metadata được phép thay vì sao chép nội dung. Không được tự tuyên bố dự án được UNESCO, Viện Âm nhạc hoặc nghệ nhân bảo trợ/chứng nhận.

Nếu gửi đóng góp, bạn cần có quyền chia sẻ nội dung ấy; việc gửi đóng góp **không mặc nhiên cấp quyền thương mại cho bên khác**. Khi kho công bố LICENSE rõ ràng, quy tắc áp dụng cho phần mã và dữ liệu của từng chủ thể phải được tách biệt.

## Quy tắc ứng xử

Thảo luận với sự tôn trọng đối với nghệ nhân, truyền thống địa phương và người giữ dị bản khác. Tranh luận về **bằng chứng**, không công kích người đưa thông tin. Khi có nguồn mâu thuẫn, ghi cả hai và xác định việc cần đối chiếu, không tự tạo ra một bản “chuẩn duy nhất”.

**Tình trạng dự án:** 20/20 bài đã mở hồ sơ kiểm nguồn V2; 0/20 bài được nghiệm thu diễn xướng tại thời điểm 28/10/2026.
