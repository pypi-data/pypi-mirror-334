import sys
import os
from MultipleRegression.regression import MultipleRegression

# Thêm thư mục cha vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    if len(sys.argv) != 3:
        print("Usage: python run_regression.py <path_to_csv_file> <target_column>")
        sys.exit(1)

    # Lấy đường dẫn đến file CSV từ command line argument
    filepath = sys.argv[1]
    target_column = sys.argv[2]  # Lấy target_column từ đối số dòng lệnh

    # Kiểm tra file tồn tại hay không
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        sys.exit(1)

    # Khởi tạo mô hình hồi quy
    model = MultipleRegression()  # Không cần truyền data_file vào constructor

    # Tải dữ liệu
    X, y = model.load_data(filepath, target_column)  # Truyền target_column vào

    # Huấn luyện mô hình, truyền X và y vào
    model.fit(X, y)

    # In thông tin tóm tắt mô hình
    print("Tóm tắt mô hình:")
    print(model.summary())

    # Vẽ đồ thị
    model.plot(X, y)

if __name__ == "__main__":
    main()
