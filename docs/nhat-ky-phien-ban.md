# NHẬT KÝ CÁC THẾ HỆ V — HAI ĐẤT · 20 BẢN TỔ

> **Mỗi lần mở một thế hệ V mới, bắt buộc có: (1) ngày bắt đầu, (2) điểm mới đáng giá, (3) dung lượng đo được.**
>
> Lưu trạng thái thành thật: **mở hồ sơ nguồn không đồng nghĩa đã nghiệm thu âm nhạc**. Không mượn uy tín UNESCO hoặc Viện Âm nhạc để chứng nhận cho kho này.

## 1. Tóm tắt các thế hệ đã có

| Thế hệ | Bắt đầu ghi nhận trên GitHub (UTC+7) | Điểm mới nổi bật | Dung lượng snapshot (Git, chưa nén) | Số tệp |
|---|---|---|---:|---:|
| **V1 — Đặt nền tư liệu** | **12/10/2026** (commit đầu tiên, không suy ra ngày bắt đầu làm ngoài GitHub) | Bắt đầu xây dựng thư mục 20 bản Tổ, đặt hệ thống nguồn, lời ca, ký âm tham khảo, nhận diện các dị bản và ghi nhận vấn đề còn thiếu | **397,63 KiB** (407.176 byte) | 64 |
| **V2 — Từ danh mục đến hồ sơ có chứng cứ** | **19/10/2026** (commit sớm nhất có nhãn V2 trong lịch sử); **27/10/2026** bắt đầu giai đoạn nghiệm thu V2 theo quy chế | Mở biên bản kiểm nguồn **20/20 bản**, xây sổ câu theo nguồn/trang, bóc tách khác biệt dị bản, cập nhật README và danh mục trích dẫn; **0/20 bài được nghiệm thu diễn xướng** | **942,96 KiB** (965.588 byte) | 112 |
| **V3.0-alpha — Dữ liệu tra cứu có chứng cứ** | **28/10/2026**, có commit khởi động riêng | JSON **20 bài + 30 hệ bản/dị bản**, lược đồ JSON, validator, trang tra cứu tiếng Việt trên điện thoại; **39 phép thử và 170 liên kết nội bộ đạt trên GitHub Actions**; chưa có bản thu/âm nhạc nghiệm thu hoặc website Pages đã triển khai | **1.055,84 KiB** (1.081.181 byte) | 133 |
| **V3.1 — 20 trang bài có thể tra cứu độc lập** | **28/10/2026**, nhánh khởi động `v3.1-development` | **20 trang HTML sinh tự động**, 3 mức lọc chứng cứ, A–Z tiếng Việt, liên kết nguồn V2, sitemap; **45 bài Python và Chromium đạt, Pages đã triển khai** | **1.111,14 KiB** (1.137.811 byte) | 140 |
| **V3.2 — Học từng câu có dấu vết nguồn** | **28/10/2026**, tạo `v3.2-development` | **72 nhãn câu thuộc 2 hệ riêng**, lớp và trang đối chiếu V2, phiếu thực hành, quy chế 5 tầng, chống bịa MIDI/âm thanh và trộn dị bản; **Pages đã triển khai thành công** | **1.225,20 KiB** (1.254.609 byte) | 150 |

### Mốc đo và bằng chứng

- **V1:** snapshot nhánh `v1-frozen`, commit [`f6537c8`](https://github.com/Form997/Vong-co/tree/f6537c83878bca079752dbdd4baec5b1164a1ab4), cây Git này có **64 tệp**, tổng kích thước Git blob **407.176 byte**. Ngày bắt đầu ghi nhận từ [initial commit 12/10/2026](https://github.com/Form997/Vong-co/commit/ee3fd39a56d17b6f73813fe8b8c10c079f723315). **Không sửa nhánh V1 chỉ để ghi lịch sử phiên bản.**
- **V2:** snapshot `v2-development`, commit [`4d919d2`](https://github.com/Form997/Vong-co/tree/4d919d2ebdf63df61c8fd723f850830e7eaf5968), cây Git này có **112 tệp**, tổng kích thước Git blob **965.588 byte**. Dấu mốc có nhãn **V2** sớm nhất tìm thấy là [commit 19/10/2026](https://github.com/Form997/Vong-co/commit/8f4e83e98f05e45a0563489ed718aeff2ac921fe). Việc lập **quy chế nghiệm thu V2** vào 27/10/2026 là mốc phát triển **riêng**, không được ngầm thay cho 19/10.
- **V3.0-alpha:** khởi động qua [commit `660cbe1`](https://github.com/Form997/Vong-co/commit/660cbe1d99a20f521a818cb514eee8ee2f8381cb) ngày **28/10/2026**. Bản chụp sau khi tạo danh mục, website và CI ở [commit `d7d9765`](https://github.com/Form997/Vong-co/tree/d7d976561215be5c28e1b10db7ddc868037ed386) có **133 tệp**, tổng **1.081.181 byte**, tức **1.055,84 KiB**. [CI run #40654050406](https://github.com/Form997/Vong-co/actions/runs/40654050406) xác nhận **39 bài test đạt**, **170 link nội bộ hợp lệ**, JSON **20 bản/30 hệ**. **V3 đang alpha**, không phải phát hành/Pages hoặc nghiệm thu biểu diễn.
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
3. **Kiểm thử tự động từ GitHub:** [workflow V3](../.github/workflows/kiem-thu-v3.yml) kiểm JSON, cấu trúc 20 bài, thiếu nguồn, liên kết nội bộ và cú pháp JavaScript. [Lần chạy #40654050406 thành công](https://github.com/Form997/Vong-co/actions/runs/40654050406), **39 phép thử, 170 liên kết** được kiểm.
4. **Giới hạn được lập trình thành quy tắc:** `performance_status=pending`, `rights_status=unverified`; không tự nâng cấp bài từ "biên bản đã mở" thành "đạt nghệ thuật"; có phần riêng cho nguồn chỉ mục/nguồn thuật lại/ánh xạ chưa thẩm định.

**Dung lượng V3 alpha ở mốc kiểm thử:** **1.081.181 byte** = **1.081,18 KB** = **1.055,84 KiB**, **133 tệp** tại [commit `d7d9765`](https://github.com/Form997/Vong-co/tree/d7d976561215be5c28e1b10db7ddc868037ed386). **Đây là kích thước snapshot chưa nén**, không phải dung lượng ZIP và không phải số byte cố định của nhánh khi có commit mới.

**Chưa hoàn thành:** chưa có dữ liệu âm thanh/ca/đờn đã cấp phép, chưa có thẩm định nghệ nhân, chưa kiểm toàn bộ từng phách, chưa triển khai Pages, chưa công bố API/MCP V3 ổn định. **00/20** bài nghiệm thu diễn xướng.

**Tài liệu V3:** [Báo cáo khởi động](v3-khoi-dong.md) · [Bộ dữ liệu](../data/v3/README.md) · [Giao diện thử nghiệm](../web/v3/README.md).

### Cập nhật V3.0-alpha — kiểm thử trình duyệt và chuẩn bị website (28/10/2026)

**Mới so với mốc alpha đầu tiên:**
- **Kiểm thử giao diện Chromium thật:** tìm có/không dấu, 4 bộ lọc 6/7/3/4, tách Phụng Hoàng–Phụng Cầu, Cổ Bản Vắn–Trường, liên kết sâu `#bai-20`, giao diện điện thoại 390 px; [kết quả thành công #40675487073](https://github.com/Form997/Vong-co/actions/runs/40675487073), có ảnh đối chứng mobile và desktop.
- **42 phép thử Python** và **174 liên kết nội bộ** được kiểm thành công tại [GitHub Actions V3](https://github.com/Form997/Vong-co/actions/runs/40675606514). Không hiểu các phép thử này là kiểm định đúng/đủ âm nhạc cổ truyền.
- **Gói website công khai 7 tệp:** [script đóng gói](../scripts/v3_build_site.py), [workflow Pages](../.github/workflows/pages-v3.yml). Gói được tạo và upload **thành công**; **job Deploy hiện Skipped theo thiết kế opt-in**, nên **website chưa được xác nhận công bố lên GitHub Pages**. Chủ kho cần kiểm cấu hình và bật [công tắc triển khai](v3-github-pages.md).
- **Đã sửa lỗi tìm kiếm**: từ ghi chú nhắc “Phụng Cầu” trong hồ sơ Phụng Hoàng, hệ thống trước đây trả 2 kết quả; nay ưu tiên tên bài/dị bản khớp trực tiếp.
- **Đã sửa deep-link** để URL `#bai-20` mở đúng hồ sơ số 20 khi trang đã được tải.

**Dung lượng tại bản chụp giai đoạn 2:** **1.105.876 byte** = **1.105,88 KB** = **1.079,96 KiB**, **139 tệp**, commit cố định [`193f3da`](https://github.com/Form997/Vong-co/tree/193f3da5f44d0e66c939c9e36fe1da1d3d7a1e34). Bản chụp này lớn hơn snapshot V3 alpha đầu tiên **39.019 byte**; đây chỉ là **chênh kích thước tổng hai Git tree**, không phải tổng của riêng các tệp mới.

**Mức hoàn thành âm nhạc:** **0/20** bài được nghiệm thu diễn xướng, không thay đổi. **V3 vẫn alpha**.

### V3.0 đã xuất bản website (sau các mốc alpha ban đầu)

**28/10/2026:** sau khi cấu hình nhánh được phép triển khai, [GitHub Pages run #40675923989, attempt 3](https://github.com/Form997/Vong-co/actions/runs/40675923989) có **Build Success và Deploy Success**. Địa chỉ do GitHub Deploy xác nhận: [https://form997.github.io/Vong-co/](https://form997.github.io/Vong-co/). Các mục V3.0 ở phần trên ghi “chưa có website” là **trạng thái tại snapshot trước khi triển khai**, không phải trạng thái hiện hành.

## 5. V3.1 — Mỗi bản Tổ có một trang riêng và đường dẫn trở về chứng cứ

**Ngày khởi động:** **28/10/2026** theo [commit khởi động V3.1](https://github.com/Form997/Vong-co/blob/v3.1-development/docs/v3.1-khoi-dong.md). **Nhánh:** `v3.1-development`, tách từ `v3-development`.

**Những điểm mới đã làm được:**
1. **20 địa chỉ riêng cho 20 bản Tổ:** từ một danh mục chung, mỗi bài có trang HTML được sinh từ JSON lúc build; hỗ trợ tiêu đề, phân nhóm, dị bản/hệ câu, nguồn, cảnh báo chưa nghiệm thu, bài trước/sau. Người đọc có thể mở đúng bài mình muốn; **không đưa ký âm, lời ca hoặc MP3 chưa được cấp phép** vào các trang này.
2. **Tìm kiếm và duyệt danh mục dễ hơn:** thêm lọc mức chứng cứ `source_indexed / source_reported / derived_unverified`, sắp xếp theo bảng chữ cái tiếng Việt, giữ tìm kiếm tên không dấu và lọc 4 nhóm Bắc–Lễ–Nam–Oán.
3. **Đường dẫn nguồn và công bố minh bạch:** từng hệ tham chiếu có link nguồn; trang bài đưa người đọc đến hồ sơ và biên bản V2. Sinh sitemap có 22 URL, gắn tiêu đề SEO và canonical theo từng bản.
4. **Kiểm thử phần mềm thực tế:** [45 bài Python thành công](https://github.com/Form997/Vong-co/actions/runs/40688707624); [Chromium kiểm tìm kiếm, bộ lọc, sắp xếp, trải nghiệm 390 px và 20 URL trả HTTP 200](https://github.com/Form997/Vong-co/actions/runs/40688596819).
5. **Đóng gói an toàn trước khi triển khai:** [workflow build V3.1](https://github.com/Form997/Vong-co/actions/runs/40688707588) đã tạo **27 tệp HTML/JSON liên quan, tổng 197.920 byte**. Đây là **dung lượng gói web chưa nén**, khác số liệu kho Git.

**Dung lượng bản chụp V3.1:** **1.130.175 byte** = **1.130,18 KB** = **1.103,69 KiB**, **140 tệp**, đo từ Git tree tại [commit `f868dc8`](https://github.com/Form997/Vong-co/tree/f868dc84c89a6aca82474a805665ecb2f026fc9d). **Không** coi số này là dung lượng ZIP hoặc kích thước nhánh luôn cố định. Ngày bắt đầu và thời điểm đo được giữ riêng.

**Dung lượng phiên bản phát hành V3.1:** tại [merge commit `5243541`](https://github.com/Form997/Vong-co/tree/5243541e3ba9e6bb5953994188853c6fd6612248), **140 tệp, 1.137.811 byte = 1.137,81 KB = 1.111,14 KiB**. Con số trên là snapshot *Git* chưa nén; **27 tệp / 197.920 byte** là gói website được tạo riêng. Mốc [`f868dc8`](https://github.com/Form997/Vong-co/tree/f868dc84c89a6aca82474a805665ecb2f026fc9d) ở trên là số đo **trước phát hành** và được giữ làm đối chứng, không sửa/xóa lịch sử.

**Tình trạng:** V3.1 **đã hợp nhất qua [PR #5](https://github.com/Form997/Vong-co/pull/5) và triển khai thành công [Pages #40689588576](https://github.com/Form997/Vong-co/actions/runs/40689588576)**. Bộ kiểm thử trên nhánh phát hành: [Python #40689588560](https://github.com/Form997/Vong-co/actions/runs/40689588560) và [Chromium #40689588524](https://github.com/Form997/Vong-co/actions/runs/40689588524) đều **Success**. Dữ liệu chuyên môn vẫn **20/20 hồ sơ có biên bản, 0/20 bài nghiệm thu diễn xướng**. Chưa có quyền tái phân phối âm thanh/ca từ hoặc chứng nhận nghệ nhân.

**Liên kết:** [Giới thiệu V3.1](v3.1-khoi-dong.md) · [Hướng dẫn chạy thử V3.1](../web/v3/README.md) · [Mã tạo trang](../scripts/v3_build_site.py).

## 6. V3.2 — Từ trang hồ sơ đến việc học một câu nhạc cho đúng nguồn

**Ngày khởi động:** **28/10/2026**, nhánh [`v3.2-development`](https://github.com/Form997/Vong-co/tree/v3.2-development) tách từ bản V3.1 công khai. **Lúc khởi động chưa phát hành; sau đó đã phát hành thành công theo mốc bên dưới.**

**Điểm mới có giá trị thực tế:**
1. **72 vị trí nhãn câu có thể tra lại:** 32 thuộc `LT-32-4` của *Lưu Thủy Trường* và 40 thuộc `PC-40-8` của *Phụng Cầu Hoàng Duyên*. Số câu/lớp/trang/chữ kết ngắn được đối chiếu với **từng hàng trong sổ V2**, không sinh từ số tổng hoặc lời đoán.
2. **Trang học câu thực dụng:** người học mở từng nhãn câu, xem lớp, trang nhạc/lời hoặc chữ kết đã ghi, nguồn gốc, điểm cần hỏi nghệ nhân, đường dẫn đến bản gốc và mẫu phiếu thực hành. Các trang vẫn thân thiện điện thoại và bàn phím.
3. **Cảnh báo chưa đủ chuyên môn:** cả **20 bài có bảng/sổ V2 ở các mức khác nhau**, nhưng chỉ **2 hệ được chuyển vào mô hình học máy đọc V3.2**. [Sổ kiểm toán 20 bài](v3.2-kiem-toan-20-ban.md) đánh dấu hệ đếm phức tạp (61/60, 84/80, 67/68), bảng còn “Chưa xác minh”, tránh khẳng định 18 bài không có tài liệu.
4. **An toàn dữ liệu:** [JSON 72 câu](../data/v3_2/phrase_index.json), [schema](../data/v3_2/schema.json), [trình kiểm](../scripts/v3_2_validate.py) và các bài kiểm thử cố ý đưa **dữ liệu sai** vào để bảo đảm website từ chối nốt/âm thanh/giấy phép không có bằng chứng.
5. **Phương pháp và đạo đức khoa học:** [quy chế 5 tầng](v3.2-quy-trinh-tham-dinh.md) phân biệt *nguồn, chỉ mục câu, cấu trúc âm nhạc, diễn xướng, quyền công bố*; [phiếu thực hành](v3.2-phieu-thuc-hanh.md) để nghệ nhân/người học tự lưu đánh giá.

**Kết quả kiểm thử trước khi phát hành:** [60/60 bài Python đạt](https://github.com/Form997/Vong-co/actions/runs/40692114438), [Chromium tương tác thật đạt](https://github.com/Form997/Vong-co/actions/runs/40692114437). Đây là **kiểm thử phần mềm**; **0/20 bài nghiệm thu biểu diễn**, chưa có bản thu/ký âm/lời được cấp phép để tải lại.

**Dung lượng snapshot V3.2 trước cập nhật README/nhật ký:** **150 tệp**, tổng **1.245.064 byte** = **1.245,06 KB** = **1.215,88 KiB**, lấy cây Git tại [commit `efb84fa`](https://github.com/Form997/Vong-co/tree/efb84fa0065465d6bdf5ed90cac2bbfc4e4063fd). **Snapshot cố định**, không phải ZIP và không phải dung lượng nhánh thay đổi liên tục. Số liệu phát hành cuối cùng đã được ghi riêng ở mốc merge commit bên dưới.

**Mốc phát hành V3.2:** [PR #8 đã merge](https://github.com/Form997/Vong-co/pull/8) ngày **28/10/2026** tại [commit `9c6b7e7`](https://github.com/Form997/Vong-co/tree/9c6b7e7b7deb4e2d896500a8a6a64db084e62386). Git tree phát hành có **150 tệp, 1.254.609 byte = 1.225,20 KiB** (tách biệt 1.245.064 byte trước merge). [Python 60/60](https://github.com/Form997/Vong-co/actions/runs/40694415249), [Chromium](https://github.com/Form997/Vong-co/actions/runs/40694415286) và [GitHub Pages Build + Deploy](https://github.com/Form997/Vong-co/actions/runs/40694415309) đều **Success**. Gói website riêng có **29 tệp / 348.588 byte**. GitHub ghi địa chỉ [HAI ĐẤT](https://form997.github.io/Vong-co/); chưa có phép kiểm HTTP công khai độc lập từ bên ngoài. **0/20 bài nghiệm thu biểu diễn**, trạng thái không thay đổi.

**Giới hạn quan trọng:** không được tự suy tính điểm song lang, nhịp 7–8 của từng câu, ngón đờn, BPM, nốt MIDI hoặc chữ ca từ số nhãn. Không tuyên bố V3.2 cung cấp một khóa học 20 bản Tổ đã được nghệ nhân duyệt.

**Tài liệu:** [Báo cáo V3.2](v3.2-khoi-dong.md) · [Kiểm toán đủ 20 sổ V2](v3.2-kiem-toan-20-ban.md) · [Dữ liệu 72 nhãn](../data/v3_2/README.md).

### Đợt cải tiến giao diện V3.2 — 28/10/2026

**Thiết kế lại để người thật muốn sử dụng, nhưng giữ tiêu chuẩn khoa học.** Sau khi có bản V3.2 phát hành, [PR #9](https://github.com/Form997/Vong-co/pull/9) hợp nhất một giao diện mới: bố cục biên tập **ngà / xanh rừng / vàng đồng**, hero đồ họa CSS do dự án tạo, thanh tìm kiếm và bộ lọc phân cấp rõ, danh mục 20 thẻ dễ xem hơn. **20 trang bài độc lập và bộ 72 nhãn câu** có cùng nhận diện, accordion sáng dễ đọc, hai cột trên máy tính và một cột trên điện thoại.

**Ngày hoàn thành phát hành:** 28/10/2026. [CI Python #40697296133](https://github.com/Form997/Vong-co/actions/runs/40697296133) có **62/62 phép thử đạt**; [Chromium #40697296268](https://github.com/Form997/Vong-co/actions/runs/40697296268) xác nhận không tràn ngang tại **360, 390, 768, 1024, 1366 px**, đồng thời lưu ảnh đối chứng trang chính và trang học; [GitHub Pages #40697296276](https://github.com/Form997/Vong-co/actions/runs/40697296276) báo **Deploy Success** tại `https://form997.github.io/Vong-co/`.

**Dung lượng chính xác, snapshot bất biến sau merge:** [commit `a16cf55`](https://github.com/Form997/Vong-co/tree/a16cf55499ba5912731db1cd10b0453ac49c0d15) có **150 tệp, 1.275.924 byte = 1.275,92 KB = 1.246,02 KiB** mã nguồn Git chưa nén; gói Pages **29 tệp, 462.065 byte**. Không đồng nhất hai kích thước với ZIP. Bản này vẫn là **thế hệ V3.2 có đợt cải tiến UI**, không tự đổi thành V3.3. **0/20 bài nghiệm thu diễn xướng**, không thêm audio hoặc ký âm không rõ quyền.

### Đợt bổ sung pháp lý và an ninh mạng V3.2 — 29/10/2026

**Mục tiêu:** bảo vệ một thư viện văn hóa phi thương mại đang hoạt động và đặt **cổng NO-GO** cho các tính năng kinh doanh tương lai, không tự tuyên bố đã có giấy chứng nhận pháp lý.

**Nguồn chính thức có thể kiểm tra lại:** [21 mục nguồn luật, điều ước, chuẩn tự nguyện và điều khoản nền tảng](../data/v3_2/legal_sources.json), trong đó có [Luật An ninh mạng 116/2025/QH15](https://vanban.chinhphu.vn/?docid=216499&pageid=27160) (01/07/2026), [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15](https://vanban.chinhphu.vn/?docid=214590&pageid=27160) (01/01/2026), [Nghị định 356/2025/NĐ-CP](https://vanban.chinhphu.vn/?docid=216387&pageid=27160) (01/01/2026), [Luật sửa đổi SHTT 131/2025/QH15](https://vanban.chinhphu.vn/?docid=216511&pageid=27160) (01/04/2026), các văn bản TMĐT năm 2025–2026 và [sửa đổi EU AI Act 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj). Một khung luật chỉ áp dụng khi đúng điều kiện địa bàn và hoạt động; công văn hành chính không tự được coi là văn bản quy phạm pháp luật.

**Nội dung viết mới:**
- [Quy chế Việt Nam và quốc tế](phap-ly-an-ninh-mang-v3.2.md): phạm vi thực tế, quyền tác giả/quyền liên quan, trang nghiên cứu và dịch vụ kinh doanh, trách nhiệm riêng tư.
- [PRIVACY.md](../PRIVACY.md), [SECURITY.md](../SECURITY.md), [RIGHTS_AND_LICENSING.md](../RIGHTS_AND_LICENSING.md): dữ liệu do trình duyệt xử lý và log IP hosting, báo lỗ hổng kín, điều kiện dùng mã/sách/ghi âm.
- [12 cổng thương mại hóa](quy-trinh-thuong-mai-hoa.md), [ứng phó sự cố 6 bước](quy-trinh-ung-pho-su-co.md).
- [Trình kiểm pháp lý-safety tĩnh](../scripts/v3_2_legal_validate.py): tên nguồn/ngày, liên kết chính sách, không thêm tracker hay form chưa được rà, trạng thái NO-GO; có **13 bài thử đối chứng âm tính** ở [test_v3_2_legal_security.py](../tests/test_v3_2_legal_security.py).
- [Trang thông báo công khai](../web/v3/legal.html), được đưa vào gói Pages theo danh sách tệp cho phép mới (**30 tệp khi phát hành**), có đường dẫn từ danh mục và các trang bài.

**Mốc phát hành ngày 29/10/2026:** [PR #10 đã merge](https://github.com/Form997/Vong-co/pull/10) tại [commit `3a68a9a`](https://github.com/Form997/Vong-co/tree/3a68a9afbd66cd7e0c80f5a137787ac84b1de69f). **75/75 bài Python** đạt ở [run #40791942971](https://github.com/Form997/Vong-co/actions/runs/40791942971), **290 liên kết nội bộ hợp lệ** trong **18 tài liệu**, và [GitHub Pages Build + Deploy = Success](https://github.com/Form997/Vong-co/actions/runs/40791942791). Trang thông báo [https://form997.github.io/Vong-co/web/v3/legal.html](https://form997.github.io/Vong-co/web/v3/legal.html) được đưa vào website, tuy trợ lý chưa tự truy cập độc lập qua trình duyệt web ngoài.

**Dung lượng snapshot phát hành có thể kiểm tra lại:** **160 tệp, 1.398.285 byte = 1.398,29 KB = 1.365,51 KiB** trong Git tree bất biến tại commit `3a68a9a` (không có truncated). **Gói web:** **30 tệp, 473.683 byte**. Đây là hai hệ số đo khác nhau, không phải ZIP. **Không thay nhánh `main`, `v1-frozen` hoặc `v2-development`.**

**Giới hạn:** chưa có chứng nhận tuân thủ toàn cầu, kênh báo lỗ hổng riêng chưa xác minh đã bật, không có giấy phép thương mại cho nhạc/bản ghi của người khác; bộ kiểm chỉ xác thực tính nhất quán của nguồn và mã.

### Đợt rà soát pháp lý sáu nước V3.2 — 29/10/2026

**Mục tiêu:** khắc phục thiếu sót nghiên cứu pháp luật của **Mỹ, Nga, Trung Quốc, Úc, Nhật Bản và Hàn Quốc** ở các đợt trước. Không nâng thành V3.3 trước khi nghiệm thu nội dung.

**Nội dung đã viết trên nhánh thử:** [sáu hồ sơ chuyên sâu](phap-ly-quoc-te/README.md), **28 nguồn luật/hướng dẫn có URL gốc** ở [dữ liệu kiểm](../data/v3_2/six_country_sources.json), bộ kiểm từ chối sai quốc gia, luật ngoài danh mục, ngày tương lai, trang giả mạo và đánh dấu trái phép “đã được phép kinh doanh”. Sáu trang HTML nguồn độc lập được sinh vào website khi build, giao diện thiết kế thống nhất với HAI ĐẤT; không tải nhạc/PDF/ảnh bên thứ ba.

**Dấu mốc thời gian không được sửa sai:** Trung Quốc 01/01/2026 (Luật An ninh mạng sửa 2025); Hàn Quốc 29/10/2026 (Luật Bản quyền sửa), 02/10/2026 (Luật Mạng), 11/09/2026 (PIPA), 21/07/2026 (AI Basic Act); Úc có hợp nhất năm 2026; sửa đổi Nhật 2026 phải phân biệt ngày công bố và hiệu lực.

**Kiểm chứng:** mỗi tệp ghi đúng nguyên ngữ, URL chính thức, điều kiện áp dụng, nội dung chưa thể kết luận. **Các nguồn Nga về 149-ФЗ có bản cơ quan nhà nước còn cũ**, phải đối chiếu cổng `pravo.gov.ru` bản hiện hành trước khi vận hành thương mại. **Không tuyên bố đã đủ luật 50 bang Mỹ hay mọi quốc gia trên thế giới.**

**Đã phát hành ngày 29/10/2026:** [Pull Request #11](https://github.com/Form997/Vong-co/pull/11) đã hợp nhất tại [commit `2278abb`](https://github.com/Form997/Vong-co/tree/2278abbf3be63c679c47ddf28540a130498275bf). Git tree không bị truncated có **171 tệp, tổng 1.521.759 byte = 1.521,76 KB = 1.486,09 KiB**; đây là mã nguồn chưa nén, không phải ZIP. [GitHub Pages #40794249686](https://github.com/Form997/Vong-co/actions/runs/40794249686) xác nhận **Build Success + Deploy Success**, với gói website **36 tệp / 540.826 byte** (sáu trang luật quốc gia). [Python #40794249729](https://github.com/Form997/Vong-co/actions/runs/40794249729) đạt **87/87** và **376 liên kết nội bộ trong 25 tệp** hợp lệ. Website vẫn phi thương mại; nghiệm thu thực tấu **0/20**. Đây là snapshot bất biến tại commit merge, các chỉnh sửa nhật ký sau đó không làm thay đổi số liệu snapshot.

## 6B. V3.3-alpha — Nâng cấp chỉ mục có nguồn, ngày 29/10/2026

**Bắt đầu:** **29/10/2026**, nhánh `v3.3-development` từ `v3-development`. V3.3 không tự xóa hoặc hợp nhất lại V1, V2 hay JSON V3.2. Đã biên soạn **`data/v3_3/phrase_index.json` với 4 hệ/150 nhãn câu**, tức V3.2 72 nhãn giữ nguyên + **PLC-34-4** và **BBC-44-4** từ hai sổ V2 đã có chứng cứ từng trang.

**Điều quan trọng được xử lý:** bài 02 có 34 nhạc nhưng 32 lời ở bản Nhị Tấn tập II; giữ `null` cho trang lời 33–34, ghi dị bản ở câu 08/34, không dùng số trang PDF tự suy đoán. Bài 03 44/4 tách với 22/8, ký hiệu cuối hàng chỉ là metadata, không phải âm thanh kiểm chứng.

**Tài liệu và thử nghiệm:** [đề cương V3.3](v3.3-khoi-dong.md) · [README dữ liệu](../data/v3_3/README.md) · [đối chiếu V2](v3.2-kiem-toan-20-ban.md) · [validator](../scripts/v3_3_validate.py) · [negative tests](../tests/test_v3_3_phrases.py). Bộ kiểm không tự tạo ghi âm, ký âm hoặc lời ca có quyền.

**Giới hạn phát hành:** `4/20` chỉ mục, `150` nhãn văn bản, `16/20` chưa chuẩn hóa; **0/20 bài nghiệm thu diễn xướng, quyền `unverified`**. V3.3 mới ở giai đoạn alpha; chưa ghi dung lượng nguồn/website cho đến lúc có commit merge và gói Pages hoàn chỉnh. Không suy 150 nhãn là 150 bài luyện đã được nghệ nhân xác nhận.

## 7. Quy tắc bắt buộc cho mọi thế hệ V tiếp theo

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
