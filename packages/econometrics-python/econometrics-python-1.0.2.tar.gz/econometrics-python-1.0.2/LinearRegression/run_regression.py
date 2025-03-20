import sys
import os
import pandas as pd
from LinearRegression.regression import LinearRegression  # Đảm bảo import đúng


# Thêm thư mục cha vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_regression.py <path_to_csv_file>")
        sys.exit(1)
    
    # Lấy đường dẫn đến file CSV từ command line argument
    filepath = sys.argv[1]

    # Kiểm tra file tồn tại hay không
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        sys.exit(1)

    # Khởi tạo và huấn luyện mô hình hồi quy
    model = LinearRegression(data_file=filepath)
    model.fit()
    model.summary()
    model.plot()

if __name__ == "__main__":
    main()
