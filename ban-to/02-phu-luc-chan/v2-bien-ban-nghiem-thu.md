# BIÊN BẢN NGHIỆM THU V2 — BÀI 02 PHÚ LỤC CHẤN

**Khởi động:** 27/10/2026 · **Lần kiểm:** chứng cứ ký âm/lời, chưa kiểm biểu diễn  
**Mã phiên bản:** `PLC-NHI-TAN-VI-34-4` · **PHÁN QUYẾT: CHỜ NGHIỆM THU**.

## 1. Nguồn đối chiếu độc lập
| ID | Nguồn | Bằng chứng trực tiếp | Phạm vi |
|---|---|---|---|
| PLC-E01 | [Nhị Tấn, *Nhạc Tài Tử Nam Bộ*, tập II, năm đề trên bìa 1997](https://www.namkyluctinh.org/eBooks/AmNhac/Nhac%20Tai%20Tu%20Nam%20Bo%202%20-%20Nhi%20Tan.pdf) | **Phú Lục Chấn 34 câu nhịp tư, song lang 3–4**, chữ nhạc trang **126, 128, 130** (4 lớp **8–8–8–10**). Lời **Bá Nha, Tử Kỳ (tiếp theo)** trang **127,129**, đánh số **1–32** | **Đã xem ảnh từng trang**, chưa nghe bản biểu diễn |
| PLC-E02 | [Văn Dần, *Bài Phú Lục Chấn*, 18/8/2013](https://nhacsivandan.wordpress.com/2013/08/18/bai-phu-luc-chan/) | Chữ nhạc **1–34**, lời *Bá Nha Tử Kỳ (tiếp theo)* **1–34**. Một số chữ khác E01, rõ ở câu 08 và 34 | **Đã đọc văn bản**, không chứng minh tác giả lời |
| PLC-E03 | [Nhị Tấn, tập I, trang 58 trở đi](https://www.namkyluctinh.org/eBooks/AmNhac/Nhac%20Tai%20Tu%20Nam%20Bo%201%20-%20Nhi%20Tan.pdf) | **THỦ Phú Lục Chấn 34 câu**, khác chữ mở đầu và lời **Cắn tay mẹ đau lòng con** | **Đã xem ảnh trang 58**, không trộn với E01 |
| PLC-E04 | [Viện Âm nhạc, 20 bài bản Tổ](https://vienamnhac.vn/Media/Default/Download/20%20ban%20to%20ch.pdf) | Danh mục **Phú Lục Chân**, ca *Hội nghị Diên Hồng*, lời **Mười Phú**, ca **Đoàn Dự**; kèm tên nhạc công và nhạc cụ | Có thông tin tiết mục; **chưa ghép phách vào E01** |
| PLC-E05 | [GS.TS Trần Quang Hải, bài giới thiệu 20 bản Tổ](https://tranquanghai1944.wordpress.com/2014/09/17/hai-muoi-bai-to-co-nhac-mien-nam/) | Dẫn bản **Ba Tu đờn kìm** và tiết mục **Khổng Tử Khóc Nhan Hồi** (Đoàn Dự, *lớp 1,2 và 4*) | Trích đoạn ba lớp, không được coi là bản ca đủ 34 câu |

## 2. Phát hiện chính
| Mã lỗi | Mô tả | Phán quyết |
|---|---|---|
| PLC-001 | V1 ghi chưa có bản ký âm đủ 34 câu, trong khi E01 và E02 đều có chỉ mục chữ nhạc 1–34 | **CẦN HIỆU ĐÍNH V1 bằng chú giải trong V2**; chưa đạt thẩm định phách |
| PLC-002 | Nhị Tấn tập II có chữ nhạc 34 câu nhưng lời *Bá Nha Tử Kỳ* chỉ đánh số đến 32; Văn Dần có lời 33–34 | **CHỜ** xác định đây là thiếu câu, đoạn đờn kết hay dị bản |
| PLC-003 | Câu 08 và 34: Nhị Tấn ghi *Xáng Liu (—)*, Văn Dần ghi *Xáng Tồn (LIU)* | **DỊ BẢN CỤ THỂ**, chưa phân thắng thua |
| PLC-004 | Tập I **Thủ Phú Lục Chấn** khác tập II **Phú Lục Chấn** cả chữ đầu lẫn lời | **PHẢI TÁCH** `PLC-THU-34` khỏi `PLC-VI-34` |
| PLC-005 | Ba bộ lời khác nhau: *Hội nghị Diên Hồng* / *Bá Nha Tử Kỳ* / *Cắn tay mẹ đau lòng con* | **TÁCH nguồn**, không ghép lời tùy tiện |
| PLC-006 | Bản Đoàn Dự *Khổng Tử Khóc Nhan Hồi* chỉ được danh mục ghi lớp 1,2,4 | **TRÍCH ĐOẠN**, không nghiệm thu đủ bài |
| PLC-007 | Chưa có đối chiếu bản thu từng câu, kỹ thuật ca–đờn, song lang, người duyệt, giấy phép | **CHỜ NGHIỆM THU** |

## 3. Chấm các tiêu chí V2
| Tiêu chí | Tình trạng |
|---|---|
| Xác định bản thuộc Sáu Bắc, nhịp tư | **ĐẠT kiểm tra nguồn** |
| Xác định 4 lớp và 34 câu ở bản E01 | **ĐẠT kiểm tra nguồn** |
| Có chứng cứ chữ nhạc, nhãn câu và trang in cho 34 câu | **ĐẠT kiểm tra văn bản** |
| Xác định 34 câu lời ca cùng ấn bản E01 | **CHỜ — E01 có 32 câu lời, E02 có 34** |
| Đối chiếu các chữ/phách khác nhau giữa E01 và E02 | **CHỜ** (mới xác định một số vị trí) |
| Có bản thu cùng hệ, timecode 1–34 | **CHỜ** |
| Kiểm ngón, rung/nhấn, song lang, rao và điểm dứt với nghệ nhân | **CHỜ** |
| Quyền tái sử dụng toàn bộ nhạc/lời/MP3 | **CHỜ** |
| Người thẩm định độc lập ký nghiệm thu | **CHỜ** |

## 4. Hồ sơ kèm theo và bước khép
- [Bảng đối chiếu 34 câu, trang nguồn, chữ cuối và sự khác biệt lời](v2-ra-soat-34-cau.md).
- Chọn bản E01 làm **bản ký âm tham chiếu để kiểm**, không có nghĩa là chọn nó thành “nguyên bản đầu tiên”.
- Phải nghe bản Ba Tu 34 câu hoặc bản nghệ nhân có metadata, timecode đầy đủ; so câu 08/34, dấu nhịp song lang 3–4 và bộ lời được chọn.
- Cần tìm bản in/biểu diễn có lời 33–34 để phân biệt lỗi sách và dị bản; việc E02 ghi thêm không đủ chứng minh E01 in thiếu.
- Không sao chép toàn văn lời/ ký âm hoặc file MP3 khi chưa có quyền.

**Đợt hiện tại:** bài **01 CHỜ NGHIỆM THU**, bài **02 CHỜ NGHIỆM THU**; **0/20 bài đạt**, **2/20 bài đã mở kiểm nguồn V2**. **Đủ 34/34 câu để tra cứu bằng chứng văn bản; 0/34 câu được nghiệm thu biểu diễn.**
