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

## Gửi lỗi hoặc đề xuất

1. Mở [Issues](https://github.com/Form997/Vong-co/issues/new/choose).
2. Chọn **Đối chiếu nguồn và dị bản** hoặc **Lỗi kỹ thuật và trải nghiệm**.
3. Ghi tên bài, số bài **01–20**, câu/lớp, nguồn có URL và số trang (nếu có), điều bạn phát hiện, cách xác minh.
4. Nếu bằng chứng chỉ là ghi nhớ truyền miệng hoặc nguồn thứ cấp, hãy ghi rõ **mức chưa chắc chắn**. Không hạ thấp giá trị truyền nghề; chỉ phân biệt cấp chứng cứ.

## Pull Request

- Đề nghị sửa nội dung nghiên cứu trên **`v2-development`**, không sửa **`v1-frozen`**.
- Mỗi Pull Request tập trung một chủ đề để dễ thẩm tra. Ghi các đường dẫn nguồn, những câu chịu ảnh hưởng, và lý do điều chỉnh.
- **Không tự đổi `CHỜ NGHIỆM THU` thành `ĐẠT`** nếu chưa có chứng cứ và người thẩm định chuyên môn phù hợp.
- Khi thay đổi số liệu các thế hệ, cập nhật [Nhật ký V](https://github.com/Form997/Vong-co/blob/v2-development/docs/nhat-ky-phien-ban.md) và thống kê dung lượng theo **commit cụ thể**.
- Chạy kiểm thử (nếu có Python): `python -m unittest discover -s tests -p "test_*.py" -v` và `python -m compileall -q scripts tests`. Kết quả CI xem tại [GitHub Actions](https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v2.yml).

## Quy định trích dẫn

Một thay đổi đủ để xem xét nên có: **định danh bài, hệ bản/dị bản, điều đang khẳng định, nguồn, trang hoặc vị trí trong nguồn, mức kiểm, vấn đề còn mở**. Với chữ nhạc, cần phân biệt **tìm thấy bản chép / xác nhận nhãn câu / thẩm định phách / thẩm định diễn xướng**.

Tài liệu tham khảo chính: [Sổ nguồn](https://github.com/Form997/Vong-co/blob/v2-development/docs/nguon-tham-khao.md) · [Quy chế V2](https://github.com/Form997/Vong-co/blob/v2-development/docs/ke-hoach-v2.md) · [Tổng hợp phát hiện](https://github.com/Form997/Vong-co/blob/v2-development/docs/tong-hop-phat-hien-v2.md).

## Bản quyền và quyền sử dụng

**Kho công khai không có nghĩa mọi nội dung có giấy phép tái sử dụng.** Không đăng nguyên văn lời ca, bản ký âm, MP3, video, ảnh sách hoặc bản dịch có bản quyền khi chưa có quyền hợp lệ. Đặt liên kết và metadata được phép thay vì sao chép nội dung. Không được tự tuyên bố dự án được UNESCO, Viện Âm nhạc hoặc nghệ nhân bảo trợ/chứng nhận.

Nếu gửi đóng góp, bạn cần có quyền chia sẻ nội dung ấy; việc gửi đóng góp **không mặc nhiên cấp quyền thương mại cho bên khác**. Khi kho công bố LICENSE rõ ràng, quy tắc áp dụng cho phần mã và dữ liệu của từng chủ thể phải được tách biệt.

## Quy tắc ứng xử

Thảo luận với sự tôn trọng đối với nghệ nhân, truyền thống địa phương và người giữ dị bản khác. Tranh luận về **bằng chứng**, không công kích người đưa thông tin. Khi có nguồn mâu thuẫn, ghi cả hai và xác định việc cần đối chiếu, không tự tạo ra một bản “chuẩn duy nhất”.

**Tình trạng dự án:** 20/20 bài đã mở hồ sơ kiểm nguồn V2; 0/20 bài được nghiệm thu diễn xướng tại thời điểm 28/10/2026.
