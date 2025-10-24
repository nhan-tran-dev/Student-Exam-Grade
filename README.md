# 🧮 Chấm điểm trắc nghiệm từ file lớp (Python)

## 🚀 Tính năng

- Mở file theo “mã lớp” (class1, class2, …)
- Báo lỗi nếu không tìm thấy file hoặc dữ liệu không hợp lệ
- Kiểm tra định dạng:
- `student_id` dạng **N########** (N + 8 chữ số)
- Mỗi dòng có **26 giá trị** (1 id + 25 câu trả lời)
- Quy tắc chấm điểm: ✅ Đúng **+4** | ❌ Sai **−1** | ⭕ Bỏ trống **0**
- Thống kê:
  - Điểm cao nhất / thấp nhất
  - Điểm trung bình / median
  - Số học sinh đạt > 80 điểm
  - Câu bị bỏ qua hoặc sai nhiều nhất
- Xuất kết quả ra thư mục:  
  📄 `Output Result/{classX}_grades.txt`

---

## 📂 Cấu trúc dữ liệu đầu vào

Mỗi file (ví dụ: `class1.txt`, `class2.txt`, …) gồm nhiều dòng — mỗi dòng là dữ liệu của một học sinh:

```
N00000021,B,A,C,D,C,C,D,D,C,C,D,B,,B,A,C,B,,A,D,A,A,B,D,
```

🔹 **Giải thích:**
- `N00000021` → mã học sinh  
- 25 giá trị tiếp theo → đáp án (A/B/C/D hoặc trống)  
- Tổng cộng 26 phần tử, phân cách bằng dấu phẩy (,)

---

## 🛠️ Yêu cầu môi trường

- Python **3.9+**
- Thư viện: `pandas`, `numpy`

### Cài đặt:
```bash
pip install pandas numpy
```

---

## ▶️ Cách chạy

Chạy script bằng Python:

```bash
python lastname_firstname_grade_the_exams.py
```

Sau đó nhập mã lớp (ví dụ: `class1` tương ứng với `class1.txt`).

### 💡 Luồng chạy:
1. Nhập `class1` → chương trình tìm đường dẫn trong dict `files`
2. Mở file và kiểm tra định dạng
3. Chấm điểm & thống kê
4. Xuất file kết quả vào thư mục `Output Result/`

---

## 📊 Kết quả đầu ra

Ví dụ file `class1_grades.txt`:

```
N00000021,59
N00000035,84
```

🧾 **Giải thích:**
- Không có header
- Mỗi dòng: `student_id,score`

---

## 🧩 Cấu trúc hàm chính

| Task | Hàm | Mô tả |
|------|-----|-------|
| 1 | `list_available()`, `open_file(file_key)` | Mở và liệt kê file lớp |
| 2 | `file_analyzing(file_path)` | Kiểm tra định dạng dữ liệu |
| 3 | `grade_and_statistic_student(valid_rows)` | Chấm điểm & thống kê |
| 4 | `student_records_to_txt(file_key, valid_rows, scores, out_dir)` | Ghi file kết quả |

---

## ⚠️ Lỗi thường gặp

| Thông báo lỗi | Nguyên nhân |
|----------------|-------------|
| `file can not be found` | Nhập sai key hoặc file không tồn tại |
| `Invalid line of data: N# is invalid` | Mã học sinh không đúng định dạng |
| `does not contain exactly 26 values` | Dòng thiếu hoặc dư dấu phẩy |

---

## 🔮 Hướng phát triển



## 📜 License


