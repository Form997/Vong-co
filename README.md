<h1 align="center">HAI ĐẤT</h1>

<p align="center"><strong>20 BẢN TỔ · ĐỜN CA TÀI TỬ NAM BỘ</strong></p>

<p align="center">Gìn giữ tiếng đờn bằng tư liệu có nguồn.<br>
Tra cứu dễ hiểu · Tôn trọng dị bản · Kết nối người học với nghiên cứu và công nghệ.</p>

<p align="center">
  <a href="README.en.md">English</a> ·
  <a href="#bắt-đầu-tại-đây">Bắt đầu</a> ·
  <a href="#danh-mục-20-bản-tổ">20 bản Tổ</a> ·
  <a href="web/v3/README.md">V3.0-alpha</a> ·
  <a href="docs/nhat-ky-phien-ban.md">Các thế hệ V</a> ·
  <a href="CONTRIBUTING.md">Đóng góp</a>
</p>

<p align="center">
  <a href="https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v3.yml"><img alt="GitHub Actions - V3 test status" src="https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v3.yml/badge.svg?branch=v3-development"></a>
  <a href="https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v2.yml"><img alt="GitHub Actions - V2 test status" src="https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v2.yml/badge.svg?branch=v2-development"></a>
  <img alt="V2: 20 trên 20 hồ sơ kiểm nguồn đã mở" src="https://img.shields.io/badge/V2-20%2F20%20h%E1%BB%93%20s%C6%A1%20ngu%E1%BB%93n-28776D">
  <img alt="Chưa có bài nghiệm thu diễn xướng" src="https://img.shields.io/badge/Di%E1%BB%85n%20x%C6%B0%E1%BB%9Bng-0%2F20%20nghi%E1%BB%87m%20thu-8B6F47">
</p>

> [!IMPORTANT]
> **Trạng thái nghiên cứu · 28/10/2026:** **20/20** bản Tổ đã có biên bản kiểm nguồn V2; **00/20** bài được nghiệm thu diễn xướng. Đây là kho **nghiên cứu và kiểm chứng tư liệu đang phát triển**, **chưa phải** thư viện ký âm/âm thanh được chứng nhận hay cấp phép để tái phân phối. Không xem các huy hiệu kiểm thử phần mềm là chứng nhận âm nhạc.

> [!NOTE]
> **V3.0-alpha đã khởi động 28/10/2026:** có [dữ liệu máy đọc 20 bản / 30 hệ bản](data/v3/catalog.json), [lược đồ JSON](data/v3/schema.json), [trang tra cứu tiếng Việt](web/v3/README.md) và [bộ kiểm thử GitHub Actions V3](https://github.com/Form997/Vong-co/actions/runs/40654050406) (**39 phép thử đạt, 170 liên kết nội bộ đạt**, kiểm cả HTTP thử nghiệm). Trang HTML **chưa được xuất bản thành GitHub Pages**. **V3 đang ở giai đoạn alpha, không phải nghiệm thu âm nhạc.**

---

### V3 thử nghiệm trên trình duyệt — đã kiểm, chưa xuất bản Pages

**42 bài thử Python đã đạt**, và [Chromium đã kiểm thành công các thao tác thực tế](https://github.com/Form997/Vong-co/actions/runs/40675487073): tìm không dấu, bộ lọc 6/7/3/4, tách Phụng Hoàng/Phụng Cầu, truy cập bài theo `#bai-20` và giao diện điện thoại rộng 390 px.

**Đóng gói Pages:** thành công với **7 tệp công khai**. **Xuất bản Pages:** **chưa bật**; job Deploy mặc định `Skipped` để chỉ công bố khi chủ dự án đồng ý. [Cách bật GitHub Pages an toàn](docs/v3-github-pages.md) · [Cách xem trước và chạy thử website V3](web/v3/README.md).

## Bắt đầu tại đây

| Bạn đến để… | Nơi nên mở trước |
|---|---|
| **Thử giao diện tra cứu V3** | [Hướng dẫn mở website trên Codespaces/máy tính](web/v3/README.md) · [Xem mã giao diện](web/v3/index.html) |
| **Khám phá 20 bản Tổ** và đọc từng bài | [Danh mục 20 bản ngay bên dưới](#danh-mục-20-bản-tổ) |
| **Học đờn – ca**, hiểu số câu và hơi điệu | [Hồ sơ từng bài](ban-to/) · [Hướng dẫn đọc và thực hành bài 01](docs/01-huong-dan-don-va-ca.md) |
| **Nghiên cứu và đối chiếu** ký âm, lời, dị bản | [Những phát hiện V2](docs/tong-hop-phat-hien-v2.md) · [Nguồn tham khảo](docs/nguon-tham-khao.md) |
| **Phát triển ứng dụng AI / RAG / MCP** | [Nguyên mẫu MCP chỉ đọc](https://github.com/Form997/Vong-co/tree/feature/mcp-readonly-v1/integrations/vong-co-mcp) · [Quy chế chứng cứ V2](docs/ke-hoach-v2.md) |
| **Đề xuất sửa lỗi hoặc đóng góp** | [Hướng dẫn đóng góp](CONTRIBUTING.md) · [Gửi vấn đề](https://github.com/Form997/Vong-co/issues/new/choose) |

### Vì sao dự án này khác một danh sách tên bài?

Một bản nhạc có thể tồn tại dưới nhiều **dị bản**, cách đếm **câu**, **lớp**, hệ **nhịp** và bộ **lời ca** khác nhau. Chúng tôi ghi rõ **nguồn nào nói gì**, **đã xem trang nào**, **câu nào còn mâu thuẫn** và **điều gì chưa được người thực hành xác nhận**.

**Ba nguyên tắc xuyên suốt:** nguồn phải truy được · dị bản không bị trộn · chưa đủ chứng cứ thì nói **“chưa xác minh”**.

UNESCO đã ghi danh **nghệ thuật Đờn ca tài tử Nam Bộ** năm 2013 ([quyết định chính thức](https://ich.unesco.org/en/decisions/8.COM/8.31)); điều đó **không** có nghĩa UNESCO chứng nhận, tài trợ hoặc hợp tác với kho GitHub HAI ĐẤT này.

## Dự án có gì để xem ngay?

| Hạng mục | Hiện trạng | Mở minh chứng |
|---|---|---|
| **Hồ sơ 20 bài** | Đã có 20 thư mục và biên bản kiểm nguồn V2 | [Danh mục bài](docs/20-ban-to.md) |
| **V3.0-alpha — dữ liệu máy đọc** | **20 bản, 30 hệ bản/dị bản**, JSON + JSON Schema, chưa nghiệm thu diễn xướng | [Catalog](data/v3/catalog.json) · [Tài liệu dữ liệu](data/v3/README.md) |
| **Trang tra cứu V3** | HTML tĩnh, lọc 4 nhóm, tìm tên có/không dấu; **chưa công bố Pages** | [Giao diện](web/v3/index.html) · [Cách chạy thử](web/v3/README.md) |
| **Sổ đối chiếu câu & dị bản** | Đã mở theo bài; mức kiểm chứng không đồng đều | [Báo cáo phát hiện V2](docs/tong-hop-phat-hien-v2.md) |
| **Nguồn tham khảo** | Có mã nguồn, liên kết, trang in và giới hạn sử dụng | [Sổ nguồn](docs/nguon-tham-khao.md) |
| **Kiểm thử mã nguồn** | Workflow GitHub Actions hoạt động trên V2; có các bài thử Python và kiểm cấu trúc | [Xem kết quả CI](https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v2.yml) |
| **Tích hợp cho AI** | Có **nguyên mẫu MCP chỉ đọc ở nhánh riêng**; chưa công bố là dịch vụ thương mại ổn định | [Xem prototype](https://github.com/Form997/Vong-co/tree/feature/mcp-readonly-v1/integrations/vong-co-mcp) |
| **Nghiệm thu biểu diễn** | **0/20**; còn đối chiếu phách, lối nhấn, song lang, bản thu, nghệ nhân | [Quy chế V2](docs/ke-hoach-v2.md) |

## Danh mục 20 bản Tổ

**Sáu Bắc (01–06) · Bảy Lễ (07–13) · Ba Nam (14–16) · Bốn Oán (17–20).** Mỗi liên kết mở **hồ sơ bài** hoặc **biên bản kiểm nguồn**, không phải bản ghi âm đã nghiệm thu.

| Số | Nhóm | Bản Tổ | Kiểm nguồn V2 |
|---:|---|---|---|
| 01 | Sáu Bắc | [Lưu Thủy Trường](ban-to/01-luu-thuy-truong/README.md) | [Xem hồ sơ V2](ban-to/01-luu-thuy-truong/v2-bien-ban-nghiem-thu.md) |
| 02 | Sáu Bắc | [Phú Lục Chấn](ban-to/02-phu-luc-chan/README.md) | [Xem hồ sơ V2](ban-to/02-phu-luc-chan/v2-bien-ban-nghiem-thu.md) |
| 03 | Sáu Bắc | [Bình Bán Chấn](ban-to/03-binh-ban-chan/README.md) | [Xem hồ sơ V2](ban-to/03-binh-ban-chan/v2-bien-ban-nghiem-thu.md) |
| 04 | Sáu Bắc | [Cổ Bản (Vắn / Trường)](ban-to/04-co-ban-van/README.md) | [Xem hồ sơ V2](ban-to/04-co-ban-van/v2-bien-ban-nghiem-thu.md) |
| 05 | Sáu Bắc | [Xuân Tình Chấn](ban-to/05-xuan-tinh-chan/README.md) | [Xem hồ sơ V2](ban-to/05-xuan-tinh-chan/v2-bien-ban-nghiem-thu.md) |
| 06 | Sáu Bắc | [Tây Thi (Vắn / Trường)](ban-to/06-tay-thi-van/README.md) | [Xem hồ sơ V2](ban-to/06-tay-thi-van/v2-bien-ban-nghiem-thu.md) |
| 07 | Bảy Lễ | [Xàng Xê](ban-to/07-xang-xe/README.md) | [Xem hồ sơ V2](ban-to/07-xang-xe/v2-bien-ban-nghiem-thu.md) |
| 08 | Bảy Lễ | [Ngũ Đối Thượng](ban-to/08-ngu-doi-thuong/README.md) | [Xem hồ sơ V2](ban-to/08-ngu-doi-thuong/v2-bien-ban-nghiem-thu.md) |
| 09 | Bảy Lễ | [Ngũ Đối Hạ](ban-to/09-ngu-doi-ha/README.md) | [Xem hồ sơ V2](ban-to/09-ngu-doi-ha/v2-bien-ban-nghiem-thu.md) |
| 10 | Bảy Lễ | [Long Đăng](ban-to/10-long-dang/README.md) | [Xem hồ sơ V2](ban-to/10-long-dang/v2-bien-ban-nghiem-thu.md) |
| 11 | Bảy Lễ | [Long Ngâm](ban-to/11-long-ngam/README.md) | [Xem hồ sơ V2](ban-to/11-long-ngam/v2-bien-ban-nghiem-thu.md) |
| 12 | Bảy Lễ | [Vạn Giá](ban-to/12-van-gia/README.md) | [Xem hồ sơ V2](ban-to/12-van-gia/v2-bien-ban-nghiem-thu.md) |
| 13 | Bảy Lễ | [Tiểu Khúc](ban-to/13-tieu-khuc/README.md) | [Xem hồ sơ V2](ban-to/13-tieu-khuc/v2-bien-ban-nghiem-thu.md) |
| 14 | Ba Nam | [Nam Xuân](ban-to/14-nam-xuan/README.md) | [Xem hồ sơ V2](ban-to/14-nam-xuan/v2-bien-ban-nghiem-thu.md) |
| 15 | Ba Nam | [Nam Ai](ban-to/15-nam-ai/README.md) | [Xem hồ sơ V2](ban-to/15-nam-ai/v2-bien-ban-nghiem-thu.md) |
| 16 | Ba Nam | [Đảo Ngũ Cung](ban-to/16-dao-ngu-cung/README.md) | [Xem hồ sơ V2](ban-to/16-dao-ngu-cung/v2-bien-ban-nghiem-thu.md) |
| 17 | Bốn Oán | [Tứ Đại Oán](ban-to/17-tu-dai-oan/README.md) | [Xem hồ sơ V2](ban-to/17-tu-dai-oan/v2-bien-ban-nghiem-thu.md) |
| 18 | Bốn Oán | [Phụng Hoàng](ban-to/18-phung-hoang/README.md) | [Xem hồ sơ V2](ban-to/18-phung-hoang/v2-bien-ban-nghiem-thu.md) |
| 19 | Bốn Oán | [Giang Nam](ban-to/19-giang-nam/README.md) | [Xem hồ sơ V2](ban-to/19-giang-nam/v2-bien-ban-nghiem-thu.md) |
| 20 | Bốn Oán | [Phụng Cầu](ban-to/20-phung-cau/README.md) | [Xem hồ sơ V2](ban-to/20-phung-cau/v2-bien-ban-nghiem-thu.md) |

**Cần lưu ý khi tìm hiểu:** *Cổ Bản* có hệ Vắn/Trường **34/68 câu**; *Tây Thi* có hệ **26/52 câu**. *Phụng Hoàng* (#18) **khác** *Phụng Cầu* (#20). Không suy từ số dòng trong sổ câu ra việc đã thẩm định nhạc. Những khác biệt khó hơn, như ranh lớp **Giang Nam**, được lưu đầy đủ trong [báo cáo phát hiện](docs/tong-hop-phat-hien-v2.md).

## Các thế hệ V — lịch sử có thể kiểm chứng

| Phiên bản | Bắt đầu ghi nhận | Bước tiến chính | Dung lượng bản chụp |
|---|---|---|---:|
| **V1 – Gieo nền tư liệu** | **12/10/2026** | Tạo hệ thống hồ sơ và nguồn cho 20 bản Tổ, ghi nhận dị bản và phần còn thiếu | **397,63 KiB** |
| **V2 – Đưa câu đờn trở về nguồn** | **19/10/2026**; bắt đầu quy chế kiểm nguồn toàn bộ **27/10** | Mở biên bản cho **20/20**, đối chiếu số câu, nguồn, trang in, lời ca và cách phân lớp; **chưa nghiệm thu biểu diễn** | **942,96 KiB** |
| **V3.0-alpha – Tra cứu có nguồn** | **28/10/2026** | JSON 20 bản, **30 hệ bản**, kiểm định tự động, tra cứu tiếng Việt; **chưa phát hành ổn định** | **1.055,84 KiB** |

*Dung lượng **Git chưa nén tại snapshot có commit cố định**, không phải ZIP hay kích thước nhánh thay đổi liên tục. V1: **407.176 byte**, 64 tệp tại [`f6537c8`](https://github.com/Form997/Vong-co/tree/f6537c83878bca079752dbdd4baec5b1164a1ab4). V2: **965.588 byte**, 112 tệp tại [`4d919d2`](https://github.com/Form997/Vong-co/tree/4d919d2ebdf63df61c8fd723f850830e7eaf5968). V3 alpha: **1.081.181 byte**, 133 tệp tại [`d7d9765`](https://github.com/Form997/Vong-co/tree/d7d976561215be5c28e1b10db7ddc868037ed386).*


[**Nhật ký V1–V2, mốc thời gian, số đo và mẫu ghi thế hệ tiếp theo**](docs/nhat-ky-phien-ban.md) · [Công cụ Python đo dung lượng](scripts/thong-ke-dung-luong.py)

## Dành cho nhà nghiên cứu, lập trình viên và tổ chức

```text
Nguồn gốc / ảnh trang sách / dị bản / dữ liệu mô tả
                           ↓
             Hồ sơ nghiên cứu V1
                           ↓
       Sổ đối chiếu & biên bản nguồn V2
                           ↓
         Kiểm thử cấu trúc và trích nguồn
                           ↓
     Nguyên mẫu MCP chỉ đọc (nhánh riêng)
                           ↓
       Ứng dụng tra cứu AI / giáo dục
```

Dự án ưu tiên **tra cứu bằng chứng trước khi đưa ra kết luận**. Bên tích hợp AI cần giữ nguyên tác giả, hệ dị bản, nguồn/trang, tình trạng xác minh và quyền sử dụng; khi không đủ dữ liệu thì phải có cơ chế **không khẳng định**.

**Đường dẫn cho kỹ thuật:**
[Nguyên mẫu MCP](https://github.com/Form997/Vong-co/tree/feature/mcp-readonly-v1/integrations/vong-co-mcp) · [Quy chế V2](docs/ke-hoach-v2.md) · [Sổ nguồn](docs/nguon-tham-khao.md) · [Workflow kiểm thử](.github/workflows/kiem-thu-v2.yml)

**V3.0-alpha đã có dữ liệu JSON, giao diện HTML thử nghiệm và kiểm thử tự động**, nhưng **chưa triển khai Pages/chưa phát hành V3 ổn định**. Các bước tiếp theo là ghi chứng cứ từng trang/câu, xem xét bản quyền âm thanh, đối chiếu diễn xướng và mới sau đó phát triển AI/MCP như tính năng chính thức. [Kế hoạch V3](docs/v3-khoi-dong.md).

## Nguồn, quyền sử dụng và liêm chính khoa học

- **Nguồn học thuật và tư liệu:** [Sổ nguồn đầy đủ](docs/nguon-tham-khao.md) gồm các mục đánh mã đến **REF-68**, có mức kiểm và giới hạn; không đồng nghĩa **68 nguồn độc lập đều được xác minh trực tiếp**.
- **Bản quyền:** kho có thể xem công khai **không** đồng nghĩa được sao chép, huấn luyện AI, dùng thương mại hoặc tái phát hành bản ký âm, ca từ, PDF và MP3. Hiện chưa xác nhận một giấy phép chung cho tất cả nội dung; mã nguồn và nội dung bên thứ ba cần xét riêng.
- **Không mạo nhận chứng nhận:** việc dẫn UNESCO, Viện Âm nhạc, ICHCAP, nghệ nhân và tác giả **không** có nghĩa các đơn vị/cá nhân đó chứng nhận kho này.
- **Sửa nguồn minh bạch:** không tự biến chỗ chưa rõ thành “đã đạt”; xem [quy trình đóng góp](CONTRIBUTING.md) trước khi gửi thay đổi.

## Cùng góp sức để giữ tiếng đờn đúng với nguồn

Một trang in, một điểm sai khác câu nhạc được chỉ rõ, hay một góp ý của người thực hành có dẫn chứng đều có thể giúp kho tư liệu tốt hơn. [**Gửi Issue**](https://github.com/Form997/Vong-co/issues/new/choose) · [**Đọc hướng dẫn đóng góp**](CONTRIBUTING.md).

<p align="center"><strong>HAI ĐẤT · Gìn giữ tiếng đờn, không đánh mất xuất xứ.</strong></p>

<p align="center"><sub>Research-first Vietnamese musical heritage knowledge base · Cập nhật giao diện README: 28/10/2026 · <a href="https://github.com/Form997/Vong-co/tree/v3-development">Nhánh V3 alpha</a></sub></p>
