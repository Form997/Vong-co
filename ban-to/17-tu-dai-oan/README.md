# BẢN TỔ 17 — TỨ ĐẠI OÁN

## V2 — NGHIỆM THU KIỂM NGUỒN TỨ ĐẠI OÁN (28/10/2026)

**[Biên bản V2 — 11 phát hiện](v2-bien-ban-nghiem-thu.md)** · **[Sổ 38 câu có trang ký âm/lời và lỗi nhãn nguồn](v2-ra-soat-38-cau.md)**.

**ĐÍNH CHÍNH CÓ BẰNG CHỨNG SO VỚI V1:** Đã tìm và **xem ảnh trực tiếp** sách **Nhị Tấn, *Nhạc Tài Tử Nam Bộ*, tập IV (1997)**, có **38 câu ký âm Tứ Đại Oán nhịp tám, song lang 6–8** ở trang in **302/304/306/308**, kèm **38 câu lời *Bá Lý Hề*** ở **303/305/307/309**. Đầu phần lời tr.303 ghi **“Soạn lời: Trần Quan Quờn”** theo đúng mặt chữ sách. V1 trước đó ghi **chưa kiểm được bản ký âm 38 câu đầy đủ**, kết luận thiếu nguồn này nay **đã được giải quyết**, nhưng **chưa kiểm theo bản thu, phách và kỹ thuật thực tấu**.

- **Khúc thức bản in 7 lớp:** **Thủ (1–6), Xang dài 1 (7–14), Xang dài 2 (15–22), Xang vắn 1 (23–26), Xang vắn 2 (27–30), Hồi thủ (31–34), Xang dứt (35–38)**. Tổng **6+8+8+4+4+4+4=38**. **Không tự gộp lớp nhỏ thành một sơ đồ số câu khác**.
- **Tứ Đại Vắn 19 câu nhịp tư, song lang 3–4** ở ngay trước Tứ Đại Oán trong tập IV tr.300–302, là **hệ nhạc khác**. Không dùng ký âm Vắn để tự dựng nốt nhịp tám.
- **Lời xưa *Bùi Kiệm, Bùi Ông, Nguyệt Nga*** có ở **Nhị Tấn tập II, phụ lục tr.181–184**; sách ghi mốc **Mỹ Tho 1910 / Vĩnh Long 1915** theo lời dẫn **được in lại năm 1997**, chưa kiểm tư liệu sự kiện đương thời. **Trang 183 in nhãn câu 21 hai lần, thiếu 22**; đã ghi lỗi để tra nguồn, không tự sửa ấn bản.
- Bộ lời **S1 *Bá Lý Hề* (Trần Quan Quờn)** và bộ lời **S2 *Bùi Kiệm – Bùi Ông – Nguyệt Nga* (“Lời xưa”, chưa rõ tác giả)** phải tách **`lyric_version_id`**, không chuyển nhầm tác giả. Ca *Mong Chờ* (Trần Ngọc Thạch/Kim Thanh) chỉ có đầu mối trích ca khác, chưa đủ 38 câu.
- **Đã xác minh hiện diện 38/38 câu nhạc và 38/38 câu lời ở tập IV**, nhưng **0/38 câu được nghiệm thu diễn xướng**; cần bản thu cùng hệ, nhịp mồ côi/mô/qua sông, ngón, song lang, nghệ nhân, quyền sử dụng. **CHỜ NGHIỆM THU**.
- Nhánh `v1-frozen` **giữ nguyên**, nội dung bên dưới là nghiên cứu V1 lịch sử; khi thông tin cũ mâu thuẫn nguồn in mới, dùng chứng cứ và biên bản V2.

---

**Nhóm:** Bốn Oán · **Hơi:** Oán · **Bản tham chiếu:** 38 câu nhịp tám · **Khảo cứu:** 27/10/2026.

> **Trạng thái:** Có nguồn Viện Âm nhạc về khúc thức và bản lời xưa có bằng chứng trong sách Nhị Tấn (1997); chưa nghiệm thu từng chữ đờn, trường độ, phách song lang và ngón đờn.

## 1. Nhận diện bản và lịch sử
- [Viện Âm nhạc, giới thiệu 20 bản Tổ](https://vienamnhac.vn/Media/Default/Download/20%20ban%20to%20ch.pdf): **Tứ Đại Oán, 38 câu nhịp tám**, phát triển từ *Tứ Đại Vắn/Tứ Đại Cảnh* thuộc hệ Huế sang thực hành tài tử Nam Bộ; không đồng nhất bản **Tứ Đại Vắn nhịp tư** với bản Oán nhịp tám.
- [Tài liệu độc tấu guitar phím lõm, Viện Âm nhạc](https://vienamnhac.vn/Media/Default/Default/Tai%20lieu/doc%20tau%20ghi%20ta%20phim%20lom.pdf) mô tả thang chữ **Hò–Y–Xang–Xê–Oan**, biến âm Cống/U; có **nhịp mồ côi**, các nhịp lặng **sang sông**, tổ chức **Thủ, Xang dài, Xang vắn, Hồi thủ**.
- [Nguyễn Tấn Nhì, *Từ Tứ Đại Cảnh đến Tứ Đại Oán*, đăng tại Văn Dần 2013](https://nhacsivandan.wordpress.com/2013/08/18/tu-tu-dai-canh-den-tu-dai-oan/) giải thích quá trình chuyển từ Tứ Đại Cảnh đến Tứ Đại Vắn và Tứ Đại Oán qua sáng tạo của nhiều thế hệ. Đây là **lập luận lịch sử có tác giả**, không có cơ sở gán toàn bài Oán hiện tại cho riêng một người.
- Một điểm học thuật còn tranh luận: **Oán là điệu riêng hay hơi trong hệ Nam**; Nguyễn Tấn Nhì nêu ý kiến khác với phân tích được quy cho GS Trần Văn Khê. Bảo lưu hai trường phái, không tuyên bố tranh luận đã ngã ngũ.

## 2. Phân câu và phân lớp: không gộp hệ tùy tiện
- Phiên bản quản lý **38 câu nhịp tám**. Viện Âm nhạc nêu các lớp **Thủ, Xang dài, Xang vắn, Hồi thủ** và các lần **mô/qua sông**.
- Tài liệu có **cách chia 4 lớp lớn** để mô tả hình thức và **cách liệt kê các đoạn nhỏ Thủ, Xang dài I/II, Xang vắn I/II, Hồi thủ, Xang dứt**. Các tên gọi không chứng minh đã có ranh giới câu cụ thể giống hệt trên mọi bản ký âm.
- **Không tự gán 38 câu cho các lớp khi chưa xem đúng bản chép và ghi âm cùng hệ**. [Sổ kiểm 38 câu](kiem-dinh-38-cau.md) dùng chỉ mục quản lý 01–38.

## 3. Nguồn lời ca có dấu vết lịch sử đặc biệt
### *Bùi Kiệm – Bùi Ông – Nguyệt Nga* (lời xưa)
- **[Nhị Tấn, *Nhạc Tài Tử Nam Bộ*, tập II (1997), phần phụ lục, trang in 181 trở đi](https://www.namkyluctinh.org/eBooks/AmNhac/Nhac%20Tai%20Tu%20Nam%20Bo%202%20-%20Nhi%20Tan.pdf)**.
- Đầu trang **181** ghi “TỨ ĐẠI OÁN — Bùi Kiệm, Bùi Ông, Nguyệt Nga”, **“Lời xưa”**, gắn mốc diễn tại **Minh Tân Khách Sạn, Mỹ Tho, 1910** và **ca ra bộ ở Vĩnh Long, 1915** (theo chính nguồn sách). Lời ca đánh số theo từng câu, có phân vai và nhãn lớp. **Đã kiểm trực tiếp trang PDF đầu tiên**, chưa đối chiếu toàn bộ từng âm tiết.
- **Người soạn lời đầu tiên:** chưa có chứng cứ xác nhận. “Lời xưa” là cách ghi của người biên soạn năm 1997; **không mặc nhiên là văn bản gốc in năm 1910 hoặc 1915**.
- Đối chiếu bài nghiên cứu [Nguyễn Tấn Nhì trên trang Văn Dần](https://nhacsivandan.wordpress.com/2013/08/18/tu-tu-dai-canh-den-tu-dai-oan/), cũng nhắc sự kiện ca ra bộ *Bùi Kiệm – Nguyệt Nga* năm 1915.
- **[Đọc bản lời ở sách gốc số hóa](https://www.namkyluctinh.org/eBooks/AmNhac/Nhac%20Tai%20Tu%20Nam%20Bo%202%20-%20Nhi%20Tan.pdf)**. Chưa có giấy phép sao chép toàn văn; repository không chép lại nguyên bài.

## 4. Bản ký âm, nghệ nhân và bản thu
- Nguồn Viện Âm nhạc mô tả **38 câu, nhịp tám, hệ Oán**, nhưng **chưa kiểm đủ bản chép chữ nhạc 38 câu với trường độ và dấu song lang**. Lời xưa tại tập II là văn bản **ca có dấu nhịp lời**, không thay thế ngay một bộ lòng bản ký âm cho từng nhạc cụ.
- [Tủ nhạc cổ Nam Kỳ Lục Tỉnh](https://www.namkyluctinh.org/am-nhac/tu-nhac-co-nhac-mien-nam.html) giới thiệu 20 bản Tổ **NSƯT Ba Tu độc tấu đờn kìm**, có mục Tứ Đại Oán; **chưa kiểm bằng tai, thời điểm và giấy phép track riêng**, không tự khẳng định đã chép chính xác kỹ thuật bản thu.
- [GS.TS Trần Quang Hải – nguồn liên kết 20 bản Tổ](https://tranquanghai1944.wordpress.com/2014/09/17/hai-muoi-bai-to-co-nhac-mien-nam/) là chỉ dẫn tìm nghệ nhân/bản thu khác, không tự cấp quyền tải lên GitHub.

## 5. Giáo trình tập đờn và ca: phương pháp có điều kiện
1. **Chọn bản 38 câu nhịp tám**, khác Tứ Đại Vắn 19/38 câu theo các hệ nhịp đã giãn. Người đờn dẫn thống nhất dây, cung hò và cách rao **hơi Oán**, không áp rung nhấn của hơi Ai một cách máy móc.
2. **Rao và vào lòng bản:** người đờn kìm giữ chữ trục; đờn tranh/cò/sến/guitar phím lõm chỉ dùng nếu có trong dàn thực tế. Không biến một bản độc tấu Ba Tu thành phối khí tập thể giả định.
3. **Mô / qua sông:** đây là các vị trí nghỉ/đệm có tổ chức; **phải xác minh số nhịp và chỗ vào lại từ bản chép cùng nghệ nhân** trước khi dạy hát đúng vị trí. Không lấy 4 lần mô rồi gán 4 vị trí không nguồn.
4. **Khi ca bản lời xưa:** chia vai Bùi Kiệm, Bùi Ông, Nguyệt Nga theo chỉ dẫn tập II. Đối chiếu từng câu ca/nhịp với bản đờn tương ứng, dấu thanh, chữ ngân và chỗ lấy hơi. Không tự thêm thoại hoặc lời mang nhãn “nguyên bản”.
5. **Song lang:** với 38 câu nhịp tám, tín hiệu vào, ra, nhịp mồ côi và chỗ sang sông cần thẩm âm và người truyền dạy xác nhận, không tự lập quy tắc gõ cố định cho mọi bản.
6. **Kết bài:** xác minh câu kết và chữ đờn theo bản thu/ ký âm được chọn; phân biệt kết đầy đủ và chuyển lớp/qua sông.

## 6. Kiểm định và yêu cầu chốt
- [x] Có nguồn viện chuyên ngành xác định Tứ Đại Oán **38 câu nhịp tám**.
- [x] Có bài nghiên cứu truyền biến Tứ Đại Cảnh → Tứ Đại Vắn → Tứ Đại Oán, ghi người nghiên cứu.
- [x] Có nguồn **Nhị Tấn 1997, tr.181**, ghi lời xưa *Bùi Kiệm – Bùi Ông – Nguyệt Nga*, mốc 1910/1915.
- [x] Có đầu mối bản thu đờn kìm của Ba Tu.
- [ ] Chưa thẩm định 38 câu lòng bản, ngón đàn, điểm song lang và 4 mô từ bản thu.
- [ ] Chưa kiểm văn bản lời năm 1910 hoặc 1915 cấp bản gốc; chưa xác định tác giả lời.
- [ ] Chưa xác minh quyền tái bản lời xưa/scan sách hoặc phát hành lại MP3.
- [ ] Chưa có nghệ nhân duyệt toàn bộ giáo trình.

**KẾT LUẬN: Chốt HỒ SƠ NGUỒN V1; CHƯA chốt bản biểu diễn.**  
[Sổ kiểm 38 câu](kiem-dinh-38-cau.md) · [Danh mục nguồn và câu hỏi lịch sử](nguon-va-di-ban.md).
