# Báo cáo phân tích quan hệ Bộ phận – Chỉnh thể (Meronym – Holonym) trong WordNet

**Nguồn dữ liệu:** Open English WordNet 2025 (`oewn:2025`)
**Công cụ:** thư viện Python `wn` 1.1.0
**Phạm vi:** toàn bộ 107.519 synset của WordNet
**Sản phẩm kèm theo:** `oewn2024_meronym_holonym.txt` (cây quan hệ dạng văn bản), thư mục `stats_output/` (biểu đồ + CSV)

---

## 1. Tóm tắt kết quả chính (Executive Summary)

- WordNet 2025 có **107.519 synset**. Trong đó chỉ **4.099 synset (3,81%)** đóng vai trò *chỉnh thể* (có ít nhất một bộ phận – meronym) và **5.954 synset (5,54%)** đóng vai trò *bộ phận* (thuộc về một chỉnh thể nào đó – holonym). ⇒ Quan hệ bộ phận/chỉnh thể là **quan hệ thưa** trong WordNet.
- **100% synset tham gia quan hệ đều là danh từ** (`n`) — đúng với đặc trưng ngôn ngữ học: meronymy chỉ áp dụng cho danh từ.
- Tổng số cạnh meronym và holonym **khớp tuyệt đối: 6.935 = 6.935** — kiểm chứng tính toàn vẹn (hai quan hệ là nghịch đảo của nhau).
- Loại quan hệ **`part` (bộ phận cấu thành) chiếm ưu thế tuyệt đối: 77,7%** tổng số cạnh. Hai loại `location` và `portion` **hoàn toàn không được dùng (0 cạnh)** trong phiên bản 2025 — một khoảng trống dữ liệu đáng lưu ý.
- Synset có nhiều bộ phận nhất: **`ship` (tàu thủy) – 31 bộ phận**. Synset thuộc về nhiều chỉnh thể nhất: **`handle, grip` (tay cầm) – 28 chỉnh thể**.
- Cây meronym sâu nhất đạt **14 cấp**; cây lớn nhất là **`body` (cơ thể)** mở rộng thành **645 dòng**.

---

## 2. Phương pháp

- **Quan hệ meronym** được gộp từ 5 phân loại: `mero_part`, `mero_member`, `mero_substance`, `mero_location`, `mero_portion`.
- **Quan hệ holonym** được gộp từ 5 phân loại tương ứng: `holo_part`, `holo_member`, `holo_substance`, `holo_location`, `holo_portion`.
- Duyệt **toàn bộ synset**; với mỗi synset có quan hệ, mở rộng **đệ quy** các synset liên quan trực tiếp, mỗi cấp sâu hơn thụt vào thêm **1 tab**. Định dạng mỗi dòng: `(cấp) {từ đồng nghĩa} [mã synset]: định nghĩa`.
- Có **cơ chế chặn chu trình** trên nhánh đang duyệt (một synset đã nằm trên đường đi hiện tại sẽ không mở rộng lại) để tránh lặp vô hạn giữa quan hệ nghịch đảo part↔whole.
- Toàn bộ số liệu trong báo cáo được tính **trực tiếp từ lexicon** (chính xác tuyệt đối, không bị ảnh hưởng bởi phần lặp lại trong file văn bản đã làm phẳng).

---

## 3. Độ bao phủ (Coverage)

| Chỉ số | Giá trị | % trên tổng synset |
|---|---:|---:|
| Tổng số synset | 107.519 | 100,00% |
| Chỉnh thể – có ≥1 meronym | 4.099 | 3,81% |
| Bộ phận – có ≥1 holonym | 5.954 | 5,54% |
| Số cạnh meronym | 6.935 | — |
| Số cạnh holonym | 6.935 | — |

> **Nhận xét:** Số synset là *bộ phận* (5.954) nhiều hơn số synset là *chỉnh thể* (4.099) — hợp lý, vì một chỉnh thể thường gồm nhiều bộ phận khác nhau, và nhiều bộ phận có thể được chia sẻ giữa các chỉnh thể.

---

## 4. Phân bố theo loại quan hệ (Subtype)

| Loại | Meronym (cạnh) | Holonym (cạnh) | Tỷ trọng |
|---|---:|---:|---:|
| **part** (bộ phận cấu thành) | 5.387 | 5.387 | 77,7% |
| **substance** (chất liệu) | 825 | 825 | 11,9% |
| **member** (thành viên) | 723 | 723 | 10,4% |
| **location** (vị trí) | 0 | 0 | 0,0% |
| **portion** (phần chia) | 0 | 0 | 0,0% |
| **Tổng** | **6.935** | **6.935** | 100% |

![Số cạnh theo loại quan hệ](stats_output/edges_by_subtype.png)

> **Nhận xét:** Cột meronym và holonym bằng nhau ở mọi loại — bằng chứng trực quan cho tính nghịch đảo. `part` áp đảo; `location`/`portion` tuy tồn tại trong lược đồ nhưng chưa có dữ liệu.

---

## 5. Phân bố bậc (Degree distribution)

*Số meronym trên mỗi chỉnh thể* = một synset được phân rã thành bao nhiêu bộ phận. *Số holonym trên mỗi bộ phận* = một synset thuộc về bao nhiêu chỉnh thể khác nhau.

| Thống kê | Meronym / chỉnh thể | Holonym / bộ phận |
|---|---:|---:|
| Số lượng | 4.099 | 5.954 |
| Trung bình | 1,69 | 1,16 |
| Trung vị | 1 | 1 |
| Phân vị 90 (p90) | 3 | 2 |
| Phân vị 99 (p99) | 10 | 4 |
| Lớn nhất | 31 | 28 |

![Phân bố bậc](stats_output/degree_distributions.png)

> **Nhận xét:** Phân bố lệch mạnh về bên phải (heavy-tailed). Đa số synset chỉ có **1 bộ phận / 1 chỉnh thể** (trung vị = 1); một số ít "trung tâm" (hub) có bậc rất cao. Trục tung dùng thang log để thấy rõ phần đuôi.

---

## 6. Các synset trung tâm (Hubs)

### 6.1. Top 15 synset có nhiều bộ phận nhất (meronym)

| # | Synset | Mã | Số bộ phận |
|---:|---|---|---:|
| 1 | ship | oewn-04201332-n | 31 |
| 2 | car, auto, automobile, machine, motorcar | oewn-02961779-n | 30 |
| 3 | Roman alphabet, Latin alphabet | oewn-06509863-n | 26 |
| 4 | body armor, suit of armor, coat of mail, cataphract | oewn-02865388-n | 25 |
| 5 | building, edifice | oewn-02916498-n | 24 |
| 6 | Greek alphabet | oewn-06511235-n | 24 |
| 7 | eye, oculus, optic | oewn-05318579-n | 23 |
| 8 | Hebrew alphabet, Hebraic alphabet, Hebrew script | oewn-06510560-n | 23 |
| 9 | motor vehicle, automotive vehicle | oewn-03796768-n | 21 |
| 10 | electromagnetic spectrum | oewn-11471859-n | 20 |
| 11 | body, organic structure | oewn-05223633-n | 19 |
| 12 | garment | oewn-03423924-n | 18 |
| 13 | torso, trunk, body | oewn-05557463-n | 17 |
| 14 | leg | oewn-05568420-n | 17 |
| 15 | skin, tegument, cutis | oewn-05245612-n | 16 |

![Top meronym hubs](stats_output/top_meronym_hubs.png)

### 6.2. Top 15 synset thuộc về nhiều chỉnh thể nhất (holonym)

| # | Synset | Mã | Số chỉnh thể |
|---:|---|---|---:|
| 1 | handle, grip, handgrip, hold | oewn-03491080-n | 28 |
| 2 | centavo | oewn-13687361-n | 19 |
| 3 | centime | oewn-13688070-n | 18 |
| 4 | electric motor | oewn-03277972-n | 12 |
| 5 | indole | oewn-92463112-n | 11 |
| 6 | cent | oewn-13686626-n | 9 |
| 7 | leg | oewn-03660152-n | 8 |
| 8 | anise, aniseed, anise seed | oewn-07842629-n | 8 |
| 9 | blade | oewn-02851454-n | 7 |
| 10 | haft, helve | oewn-03480019-n | 7 |
| 11 | shelf | oewn-04197095-n | 7 |
| 12 | copper, Cu, atomic number 29 | oewn-14659900-n | 7 |
| 13 | propionic acid, propanoic acid | oewn-14886904-n | 7 |
| 14 | hinge, flexible joint | oewn-03526239-n | 6 |
| 15 | keyboard | oewn-03619216-n | 6 |

![Top holonym hubs](stats_output/top_holonym_hubs.png)

> **Nhận xét:** Nhóm meronym-hub tập trung vào **vật thể phức tạp** (tàu, xe, tòa nhà, cơ thể, bảng chữ cái). Nhóm holonym-hub là các **bộ phận/chất liệu dùng chung** (tay cầm, đơn vị tiền tệ nhỏ, motor, nguyên tố hóa học) — xuất hiện trong rất nhiều chỉnh thể.

---

## 7. Hình dạng cây (Tree shape)

Mỗi "gốc" trong file văn bản được mở rộng đệ quy (có chặn chu trình). Bảng dưới đo **độ sâu tối đa** và **số dòng** (số hàng mà gốc đó đóng góp vào file).

| Chỉ số | Cây meronym | Cây holonym |
|---|---:|---:|
| Số cây gốc | 4.099 | 5.954 |
| Độ sâu tối đa | 14 | 14 |
| Độ sâu trung bình | 1,41 | 1,71 |
| Cây lớn nhất (số dòng) | 645 | 57 |
| Tổng số dòng | 17.026 | 18.881 |

![Phân bố độ sâu cây](stats_output/tree_depth.png)

*(Tổng số dòng node = 17.026 + 18.881 = 35.907; cộng dòng trống phân tách và tiêu đề ⇒ file `oewn2024_meronym_holonym.txt` có 45.966 dòng.)*

### 7.1. Top cây meronym lớn nhất

| Synset | Mã | Độ sâu | Số dòng |
|---|---|---:|---:|
| body, organic structure | oewn-05223633-n | 9 | 645 |
| animal, animate being, beast, brute, creature, fauna | oewn-00015568-n | 8 | 242 |
| head, caput | oewn-05546258-n | 7 | 239 |
| homo, man, human being, human | oewn-02474924-n | 7 | 192 |
| face, human face | oewn-05608392-n | 6 | 108 |
| endoskeleton | oewn-05594096-n | 6 | 106 |
| motor vehicle, automotive vehicle | oewn-03796768-n | 4 | 105 |
| nervous system, systema nervosum | oewn-05469891-n | 8 | 101 |
| building, edifice | oewn-02916498-n | 6 | 92 |
| Gregorian calendar, New Style calendar | oewn-15199265-n | 3 | 84 |

### 7.2. Top cây holonym lớn nhất

| Synset | Mã | Độ sâu | Số dòng |
|---|---|---:|---:|
| neuroepithelium | oewn-05248193-n | 7 | 57 |
| shank, stem | oewn-04191138-n | 3 | 37 |
| taste cell, gustatory cell | oewn-05312888-n | 7 | 37 |
| tastebud, taste bud, gustatory organ | oewn-05312635-n | 6 | 36 |
| handle, grip, handgrip, hold | oewn-03491080-n | 2 | 30 |
| urethral orifice, external orifice | oewn-05520321-n | 6 | 29 |
| selenium, Se, atomic number 34 | oewn-14678354-n | 6 | 24 |
| armature | oewn-02741276-n | 4 | 23 |
| selenite | oewn-92463440-n | 5 | 22 |
| vas deferens, ductus deferens | oewn-05533826-n | 6 | 22 |

> **Nhận xét:** Cây meronym lớn nhất đều thuộc **lĩnh vực giải phẫu/sinh học** (cơ thể, động vật, đầu, hệ thần kinh) — do cơ thể có cấu trúc phân rã sâu nhiều tầng. Cây holonym nhỏ hơn nhiều (tối đa 57 dòng so với 645), phản ánh việc "đi ngược lên chỉnh thể" nhanh chóng hội tụ.

---

## 8. Kết luận & khuyến nghị

1. **Quan hệ bộ phận/chỉnh thể phủ hẹp** (chỉ ~4–6% synset) nhưng **cô đọng và chính xác**: chủ yếu là danh từ chỉ vật thể cụ thể.
2. **`part` là loại quan hệ cốt lõi** (77,7%); nếu ứng dụng chỉ cần một loại, `mero_part`/`holo_part` là đủ cho phần lớn trường hợp.
3. **Thiếu dữ liệu `location` và `portion`** trong 2025 — cần lưu ý nếu hệ thống hạ nguồn kỳ vọng có hai loại này.
4. **Miền giải phẫu/sinh học là nơi cấu trúc phong phú nhất** — phù hợp để làm ví dụ minh họa hoặc trọng tâm cho ứng dụng.
5. Tính nghịch đảo được **kiểm chứng bằng số liệu** (6.935 = 6.935), đảm bảo dữ liệu trích xuất đáng tin cậy.

---

## 9. Phụ lục — tái lập kết quả

| Tệp | Mô tả |
|---|---|
| `extract_meronym_holonym.ipynb` | Notebook trích xuất cây meronym/holonym ra file văn bản |
| `oewn2024_meronym_holonym.txt` | Kết quả trích xuất (2 phần: MERONYM, HOLONYM), 45.966 dòng |
| `statistics_meronym_holonym.ipynb` | Notebook tính toàn bộ thống kê trong báo cáo này |
| `stats_output/*.png` | Biểu đồ (edges_by_subtype, degree_distributions, top hubs, tree_depth) |
| `stats_output/*.csv` | Bảng số liệu gốc (coverage, subtype, degree, hubs, tree) |

**Lệnh chạy lại thống kê:**

```bash
cd Ms_Trang
../.venv/bin/jupyter nbconvert --to notebook --execute --inplace statistics_meronym_holonym.ipynb
```

*Báo cáo tạo tự động từ kết quả đã chạy của `statistics_meronym_holonym.ipynb` trên `oewn:2025`.*
