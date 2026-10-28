# NHẬT KÝ CÁC THẾ HỆ V — HAI ĐẤT · 20 BẢN TỔ

> **Mỗi lần mở một thế hệ V mới, bắt buộc có: (1) ngày bắt đầu, (2) điểm mới đáng giá, (3) dung lượng đo được.**
>
> Lưu trạng thái thành thật: **mở hồ sơ nguồn không đồng nghĩa đã nghiệm thu âm nhạc**. Không mượn uy tín UNESCO hoặc Viện Âm nhạc để chứng nhận cho kho này.

## 1. Tóm tắt các thế hệ đã có

| Thế hệ | Bắt đầu ghi nhận trên GitHub (UTC+7) | Điểm mới nổi bật | Dung lượng snapshot (Git, chưa nén) | Số tệp |
|---|---|---|---:|---:|
| **V1 — Đặt nền tư liệu** | **12/10/2026** (commit đầu tiên, không suy ra ngày bắt đầu làm ngoài GitHub) | Bắt đầu xây dựng thư mục 20 bản Tổ, đặt hệ thống nguồn, lời ca, ký âm tham khảo, nhận diện các dị bản và ghi nhận vấn đề còn thiếu | **397,63 KiB** (407.176 byte) | 64 |
| **V2 — Từ danh mục đến hồ sơ có chứng cứ** | **19/10/2026** (commit sớm nhất có nhãn V2 trong lịch sử); **27/10/2026** bắt đầu giai đoạn nghiệm thu V2 theo quy chế | Mở biên bản kiểm nguồn **20/20 bản**, xây sổ câu theo nguồn/trang, bóc tách khác biệt dị bản, cập nhật README và danh mục trích dẫn; **0/20 bài được nghiệm thu diễn xướng** | **942,96 KiB** (965.588 byte) | 112 |
| **V3.0-alpha — Dữ liệu tra cứu có chứng cứ** | **28/10/2026**, có commit khởi động riêng | JSON **20 bài + 30 hệ bản/dị bản**, lược đồ JSON, validator, trang tra cứu tiếng Việt trên điện thoại; **32 phép thử và 144 liên kết nội bộ đạt trên GitHub Actions**; chưa có bản thu/âm nhạc nghiệm thu hoặc website Pages đã triển khai | **1.041,85 KiB** (1.066.857 byte) | 132 |

### Mốc đo và bằng chứng

- **V1:** snapshot nhánh `v1-frozen`, commit [`f6537c8`](https://github.com/Form997/Vong-co/tree/f6537c83878bca079752dbdd4baec5b1164a1ab4), cây Git này có **64 tệp**, tổng kích thước Git blob **407.176 byte**. Ngày bắt đầu ghi nhận từ [initial commit 12/10/2026](https://github.com/Form997/Vong-co/commit/ee3fd39a56d17b6f73813fe8b8c10c079f723315). **Không sửa nhánh V1 chỉ để ghi lịch sử phiên bản.**
- **V2:** snapshot `v2-development`, commit [`4d919d2`](https://github.com/Form997/Vong-co/tree/4d919d2ebdf63df61c8fd723f850830e7eaf5968), cây Git này có **112 tệp**, tổng kích thước Git blob **965.588 byte**. Dấu mốc có nhãn **V2** sớm nhất tìm thấy là [commit 19/10/2026](https://github.com/Form997/Vong-co/commit/8f4e83e98f05e45a0563489ed718aeff2ac921fe). Việc lập **quy chế nghiệm thu V2** vào 27/10/2026 là mốc phát triển **riêng**, không được ngầm thay cho 19/10.
- **V3.0-alpha:** khởi động qua [commit `660cbe1`](https://github.com/Form997/Vong-co/commit/660cbe1d99a20f521a818cb514eee8ee2f8381cb) ngày **28/10/2026**. Bản chụp sau khi tạo danh mục, website và CI ở [commit `7ff24c4`](https://github.com/Form997/Vong-co/tree/7ff24c4f9399a482cfee14c33119f0ddc4d27f35) có **132 tệp**, tổng **1.066.857 byte**, tức **1.041,85 KiB**. [CI run #40653394677](https://github.com/Form997/Vong-co/actions/runs/40653394677) xác nhận **32 bài test đạt**, **144 link nội bộ hợp lệ**, JSON **20 bản/30 hệ**. **V3 đang alpha**, không phải phát hành/Pages hoặc nghiệm thu biểu diễn.
- **Chênh lệch giữa hai snapshot:** **558.412 byte = 545,32 KiB**. Đây là **mức chênh tổng cây Git**, **không phải** một phép đo chính xác dung lượng riêng của những file được thêm vào V2.
- **Lưu ý rất quan trọng:** đây là kích thước **các tệp tại một commit đã định danh**, không phải dung lượng **ZIP**, thư mục `.git`, lịch sử commit, dữ liệu Git LFS hay các dữ liệu bên ngoài GitHub. Sau commit đo V2, khi thêm các tệp nhật ký/chương trình mới thì dung lượng nhánh làm việc **sẽ tăng**, nhưng số snapshot ở đây vẫn truy ngược kiểm chứng được.
- Hai số kích thước trên được tính bằng [Git Trees API của GitHub](https://docs.github.com/en/rest/git/trees#get-a-tree), lấy `size` của toàn bộ đối tượng `blob` trong cây đệ quy, **không phải kích thước hiển thị ước lượng của repository**. Công cụ tự kiểm lại: [`scripts/thong-ke-dung-luong.py`](../scripts/thong-ke-dung-luong.py).

## 2. V1 — Gieo nền cho tiếng đờn được lưu giữ

**Ngày bắt đầu ghi nhận:** **12/10/2026**, theo commit đầu tiên của kho; ngày khởi sự nghiên cứu trước đó **chưa có bằng chứng GitHub**.

**V1 mang lại điều gì?** Từ ý tưởng giữ gìn 20 bản Tổ, dự án tạo một chỗ tập hợp tư liệu có cấu trúc: mỗi bài có hồ sơ, lời dẫn, nguồn nghiên cứu, tên dị bản và điểm cần kiểm. Quan trọng không kém, V1 đặt nền cho cách **không nhận nhầm lời mới thành lời cổ** hay nhầm một bản rút gọn với toàn bản.

**Dung lượng bản lưu V1:** **397,63 KiB** = **407,18 KB** = **407.176 byte**, tổng **64 tệp** theo snapshot [`f6537c8`](https://github.com/Form997/Vong-co/tree/f6537c83878bca079752dbdd4baec5b1164a1ab4). **V1 là lớp nền**, không được tự gọi là hoàn thiện tổng phổ hay giấy phép biểu diễn.

## 3. V2 — Mỗi câu đờn phải có đường dẫn trở về nguồn

**Ngày bắt đầu ghi nhận:** **19/10/2026** có commit dùng nhãn V2. **27/10/2026** (giờ Việt Nam) đánh dấu bước chuyển sang **quy chế rà nguồn/nghiệm thu 20 bản**.

**V2 có gì mới?** Không chỉ xếp đủ 20 tên bài, V2 mở biên bản rà soát cho **toàn bộ 20 bản Tổ**, đánh số câu để có thể lần theo ký âm và lời ca, ghi nguồn/trang, phân biệt bản Vắn/Trường, nhịp tư/nhịp tám, ghi nhận các lỗi in, cách chia lớp bất đồng. V2 còn làm rõ ranh giới giữa **đã có chứng cứ văn bản** và **chưa được nghe, kiểm phách hoặc nghệ nhân xác nhận**, để người học và AI không được lấp khoảng trống bằng phỏng đoán.

**Điểm chưa hoàn thành:** trạng thái **20/20 đã mở hồ sơ kiểm nguồn** nhưng **0/20 đã nghiệm thu diễn xướng**. Một số sổ chỉ là khung vị trí chờ đối chứng, điển hình **Phụng Hoàng (#18)**. Chưa công bố lại ký âm/lời/MP3 bên thứ ba nếu không có quyền.

**Dung lượng snapshot V2:** **942,96 KiB** = **965,59 KB** = **965.588 byte**, tổng **112 tệp**, tại commit [`4d919d2`](https://github.com/Form997/Vong-co/tree/4d919d2ebdf63df61c8fd723f850830e7eaf5968).

## 4. V3.0-alpha — Đưa tư liệu có nguồn đến người học và máy tính

**Bắt đầu có chứng cứ:** **28/10/2026**; nhánh riêng `v3-development`, xuất phát từ V2. **Không thay đổi** `v1-frozen`, `v2-development` hoặc `main`.

**Điểm mới đáng chú ý:**
1. **20 bài, 30 hệ tham chiếu trong JSON:** mỗi bài có mã, tên, nhóm; hệ Vắn/Trường hay 67/68 được tách riêng, có `reference_url`, ghi chú sai biệt và trạng thái **chưa nghiệm thu**.
2. **Người học có thể tìm bài bằng tiếng Việt:** đã viết [giao diện web tĩnh](../web/v3/index.html) dùng trên điện thoại, có lọc theo bốn nhóm và thông tin chi tiết từng dị bản. **Chưa xác nhận xuất bản GitHub Pages**, xem [hướng dẫn chạy thử](../web/v3/README.md).
3. **Kiểm thử tự động từ GitHub:** [workflow V3](../.github/workflows/kiem-thu-v3.yml) kiểm JSON, cấu trúc 20 bài, thiếu nguồn, liên kết nội bộ và cú pháp JavaScript. [Lần chạy #40653394677 thành công](https://github.com/Form997/Vong-co/actions/runs/40653394677), **32 phép thử, 144 liên kết** được kiểm.
4. **Giới hạn được lập trình thành quy tắc:** `performance_status=pending`, `rights_status=unverified`; không tự nâng cấp bài từ "biên bản đã mở" thành "đạt nghệ thuật"; có phần riêng cho nguồn chỉ mục/nguồn thuật lại/ánh xạ chưa thẩm định.

**Dung lượng V3 alpha ở mốc kiểm thử:** **1.066.857 byte** = **1.066,86 KB** = **1.041,85 KiB**, **132 tệp** tại [commit `7ff24c4`](https://github.com/Form997/Vong-co/tree/7ff24c4f9399a482cfee14c33119f0ddc4d27f35). **Đây là kích thước snapshot chưa nén**, không phải dung lượng ZIP và không phải số byte cố định của nhánh khi có commit mới.

**Chưa hoàn thành:** chưa có dữ liệu âm thanh/ca/đờn đã cấp phép, chưa có thẩm định nghệ nhân, chưa kiểm toàn bộ từng phách, chưa triển khai Pages, chưa công bố API/MCP V3 ổn định. **00/20** bài nghiệm thu diễn xướng.

**Tài liệu V3:** [Báo cáo khởi động](v3-khoi-dong.md) · [Bộ dữ liệu](../data/v3/README.md) · [Giao diện thử nghiệm](../web/v3/README.md).

## 5. Quy tắc bắt buộc cho mọi thế hệ V tiếp theo

**Khi bắt đầu giai đoạn V3.x, V4, V5... tiếp theo**, tạo ngay mục theo mẫu sau, rồi bổ sung dần. Không để mục trống biến thành một lời hứa đã hoàn thành.

```markdown
## V4 — [Một tên ngắn thể hiện bước tiến]

**Bắt đầu:** DD/MM/YYYY (giờ Việt Nam; nguồn: commit/biên bản khởi động)
**Tình trạng:** Đang phát triển / Bản xem trước / Đã phát hành / Chờ nghiệm thu

**Điểm mới của thế hệ này:**
- [Thay đổi 1: người học hoặc nhà nghiên cứu được lợi gì?]
- [Thay đổi 2: bổ sung chức năng/dữ liệu nào có thể kiểm được?]
- [Thay đổi 3: xử lý được vấn đề gì còn thiếu ở bản trước?]

**Dung lượng:**
- Chưa đo (nếu chưa có commit đo), hoặc:
- Số tệp: N
- Tổng dung lượng Git chưa nén: X byte = Y KiB / MiB / GiB
- Ref + commit/tree SHA: ...
- Ngày đo: DD/MM/YYYY
- So với bản trước: +/− Z byte (chênh lệch snapshot, không phải dung lượng riêng các tệp mới)

**Bằng chứng:** [changelog / commit / biên bản / nguồn]
**Giới hạn còn tồn tại:** [thẳng thắn nêu điều chưa kiểm, quyền sử dụng, thử nghiệm chưa xong]
```

### Mỗi lần thay đổi phiên bản, thực hiện lần lượt

1. **Ngày bắt đầu:** ghi bằng **ngày có commit/biên bản khởi động thực tế**; nếu không chứng minh được, ghi rõ **“chưa xác minh”**. Không tự lấy ngày đo dung lượng làm ngày bắt đầu V.
2. **Nội dung mới:** viết **ngắn, giàu ý nghĩa, dễ đọc**, nêu người dùng được gì, dữ liệu nào tăng chất lượng, các lỗi nào đã sửa. Tách **đã hoàn thành** khỏi **đang dự kiến**.
3. **Dung lượng:** dùng lệnh bên dưới; ghi **byte**, **KiB/MiB/GiB**, **số file**, **commit**, **ngày đo**. Không phỏng đoán GB từ số trang hoặc tuyên bố “nặng hơn” nếu chưa đo.
4. **Phiên bản phát hành:** ưu tiên tạo **Git tag/Release** bất biến sau khi kiểm nguồn, rồi đo chính tag ấy; README có thể dẫn link đến snapshot. Các phiên bản `vX-development` vẫn là dữ liệu thay đổi theo thời gian.
5. **Chỉnh hai nơi:** cập nhật mục tóm tắt **README chung** và mục đầy đủ ở **nhật ký này**. Nhánh `v1-frozen` giữ bất biến; đưa thay đổi từ `v2-development` lên `main` qua Pull Request sau khi kiểm.

### Cách đo lại bằng công cụ miễn phí

Chạy trên máy có Python 3 và Internet:

```bash
python scripts/thong-ke-dung-luong.py --refs v1-frozen v2-development
python scripts/thong-ke-dung-luong.py --refs v1-frozen v2-development --json
```

Để đo một bản cố định, thay tên nhánh bằng **commit SHA** hoặc **Git tag**. GitHub API phải trả cây **không bị cắt ngắn**; nếu có lỗi `truncated`, chương trình **dừng** để tránh báo số thiếu.

**Cách đọc đơn vị:** 1 byte = 8 bit; **1 KB = 1.000 byte**, **1 KiB = 1.024 byte**; **1 MiB = 1.048.576 byte**; **1 GiB = 1.073.741.824 byte**. Khi dự án lớn hơn, chuyển sang MiB/GiB; không báo hàng triệu bit gây khó đọc.

---

**Nguyên tắc ghi phiên bản HAI ĐẤT:** Lịch sử có chứng cứ · thay đổi có ích · kích thước đo được · trạng thái nói thật.
