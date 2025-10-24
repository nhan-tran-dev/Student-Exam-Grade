import re
import os
from pathlib import Path
import pandas as pd
import numpy as np

# Task 1: Tạo chương trình mở file và báo lỗi nếu không tìm thấy đúng file
# Tạo đường dẫn đến file chạy .py
def project_root() -> Path:
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd().resolve()

ROOT = project_root()
DATA_DIR = ROOT / "data-files" / "Data Files"     # Thư mục chứa files đầu vào
OUTPUT_DIR = ROOT / "Output Result"               # Thư mục chứa files đầu ra

# Tạo dict chứa key: file_name và path value tương ứng -> full path
files = {f"class{i}": (DATA_DIR / f"class{i}.txt") for i in range(1, 9)}

# Tạo danh sách để kiểm tra tên của các file trong dict
def list_available():
    print("\nCác tên file hợp lệ:", ", ".join(files.keys()))        #In danh sách key khả dụng.

# Tạo hàm để mở file dựa trên values của các key trong dict (chỉ kiểm tra tồn tại & trả về path)
def open_file(file_key):
    try:
        file_path = files[file_key]
    except KeyError:
        print("\nfile can not be found.")
        return None

    if file_path.exists():
        print(f"\nSuccessfully open {file_key}.txt")
        return str(file_path)
    else:
        print("\nfile can not be found.")
        return None

# Task 2: Tạo chương trình kiểm tra dữ liệu của file đảm bảo theo nguyên tắc, định dạng yêu cầu ban đầu

def file_analyzing(file_path):
    print("\n*****Analyzing****")
    valid = 0                       #đếm dòng hợp lệ
    invalid = 0                     #đếm dòng không hợp lệ
    valid_rows = []                 #danh sách rỗng chứa các dòng hợp lệ (string)

    
    try:
        df = pd.read_csv(
            file_path,
            header=None,
            names=["line"],
            sep=r"\n",
            engine="python",
            dtype=str,
            encoding="utf-8",
            keep_default_na=False,
            na_filter=False,
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            file_path,
            header=None,
            names=["line"],
            sep=r"\n",
            engine="python",
            dtype=str,
            encoding="latin-1",
            keep_default_na=False,
            na_filter=False,
        )

    for raw in df["line"].tolist():
        line = (raw or "").strip()
        if not line:                        #nếu không có line dữ liệu thì bỏ qua đi tiếp
            continue

        parts = line.split(",")             #tách các đối tượng ngăn cách bởi ","
        student_id = parts[0].strip()       #xác định student_id là parts[0]
        if not re.fullmatch(r"^N\d{8}$", student_id):
            print("\nInvalid line of data: N# is invalid")
            print(f"\n{line}")
            invalid += 1
            continue

        if len(parts) != 26:
            print("\nInvalid line of data: does not contain exactly 26 values:")
            print(f"\n{line}")
            invalid += 1
            continue

        valid += 1
        valid_rows.append(line)  # lưu dòng hợp lệ vào danh sách valid_rows

    # Nếu không có lỗi nào, in thông báo
    if invalid == 0:
        print("\nNo errors found!")

    # Báo cáo cuối
    print("\n**** REPORT ****")
    print(f"\nTotal valid lines of data: {valid}")
    print(f"\nTotal invalid lines of data: {invalid}")
    return valid_rows              # trả về những dòng hợp lệ để sử dụng cho nhưng task sau

#Task3: Chấm điểm, thống kê và lập báo cáo điểm của học sinh
ANSWER_KEY = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
NUM_QUESTION = 25
DEC = 1
def grade_and_statistic_student(valid_rows):

    scores = []                         #tạo list rỗng để lưu sau score
    skipped = [0] * NUM_QUESTION        #tạo list với 25 giá trị 0 cho skipped
    wrong = [0] * NUM_QUESTION          #tạo list với 25 giá trị 0 cho wrong

    for line in valid_rows:             #lặp tất cả các dòng trong những dòng hợp lệ của kết quả trước
        parts = line.strip().split(",")
        std_answer = parts[1:]          #lấy các đối tượng bắt đầu từ 1 đến hết danh sách của std_answer
        key = ANSWER_KEY.strip().split(",")
        score = 0
        for i in range(NUM_QUESTION):   #lặp index cho 25 đối tượng trong
            if std_answer[i] == key[i]: #điều kiện để so sánh từng cặp đối tượng
                score += 4
            elif std_answer[i] == "":
                skipped[i] += 1
            else:
                score -= 1
                wrong[i] += 1
        scores.append(score)                #chèn thêm vào danh sách scores rỗng ban đầu

    s = np.array(scores, dtype = float)     #tạo dãy cho scores với định dạng dữ liệu sử dụng numpy
    sk = np.array(skipped, dtype = int)     #tạo dãy cho skipped với định dạng dữ liệu sử dụng numpy
    wr = np.array(wrong, dtype = int)       #tạo dãy cho wrong với định dạng dữ liệu sử dụng numpy
    n = s.size

    #tính toán các thông số với hàm có sẵn của numpy
    high_score_count = int((s > 80).sum())
    print(f"\nTotal student of high score: {high_score_count}")
    mean_score = float(s.mean())
    print(f"\nmean (average) score: {mean_score}")
    high_score = int(s.max())
    print(f"\nHighest score: {high_score}")
    low_score = int(s.min())
    print(f"\nLowest score: {low_score}")
    range_score = int(s.max() - s.min())
    print(f"\nRange of scores: {range_score}")
    median_score = np.median(s)
    print(f"\nMedian score: {median_score}")

    # tìm danh sách các giá trị các skipped nhiều nhất với numpy
    max_skip = int(sk.max())
    if max_skip > 0:
        idx = np.where(sk == max_skip)[0]
        skip_report = ", ".join(f"{i+1} - {int(sk[i])} - {(sk[i]/n):.{DEC}f}" for i in idx)
    else:
        skip_report = "(none)"
    print(f"\nQuestion that most people skip: {skip_report}")

    # tìm danh sách các giá trị các wrong nhiều nhất với numpy
    max_wrong = int(wr.max())
    if max_wrong > 0:
        idx = np.where(wr == max_wrong)[0]
        wrong_report = ", ".join(f"{i+1} - {int(wr[i])} - {(wr[i]/n):.{DEC}f}" for i in idx)
    else:
        wrong_report = "(none)"
    print(f"\nQuestion that most people answer incorrectly: {wrong_report}")

    return scores       #trả về scores cho task4 sử dụng

#Task4: Ghi lại score của từng sinh viên vào file.txt mới theo từng hàng sử dụng pandas
#tạo hàm ghi lại score_record của từng sinh viên vào file
def student_records_to_txt(file_key, valid_rows, scores, out_dir):
    os.makedirs(out_dir, exist_ok=True)                             #tạo directory cho file lưu trữ
    out_path = Path(out_dir) / f"{file_key}_grades.txt"             #tạo đường dẫn cho file và tên cách đặt tên file dựa trên file_key tương ứng
    rows = []
    for line, sc in zip(valid_rows, scores):
        sid = line.strip().split(",")[0].strip()
        rows.append((sid, sc))

    # Make a DataFrame with two columns
    df = pd.DataFrame(rows, columns=["student_id", "score"])        #tạo dataframe cho dữ liệu với tên cột để trace back

    # Write as comma-separated text: N00000001,59
    df.to_csv(                                                      #ghi dữ liệu vào file
        out_path,
        index=False,
        header=False,           # no header line
        sep=",",
        encoding="utf-8"
    )
    return str(out_path)        #trả về đường dẫn để chạy caller

# Caller để chạy toàn bộ chương trình từ task1 -> task4.
while True:
    file_key = input("\nEnter a class file to grade (i.e. class1 for class1.txt): ")
    file_path = open_file(file_key)
    if file_path:
        valid_rows = file_analyzing(file_path)
        scores = grade_and_statistic_student(valid_rows)
        out_dir = OUTPUT_DIR
        student_records_to_txt(file_key, valid_rows, scores, out_dir)
    else:
        list_available()
