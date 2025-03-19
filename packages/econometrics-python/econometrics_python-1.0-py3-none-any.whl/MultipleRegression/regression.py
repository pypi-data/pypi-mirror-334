# multiple_regression/regression.py
import numpy as np
import pandas as pd


class MultipleRegression:
    def __init__(self):
        self.model = None
        self.coefficients = None
    
    def load_data(self, filepath, target_column):
        """
        Đọc dữ liệu từ tệp .csv và chia thành X (biến độc lập) và y (biến phụ thuộc).
        filepath: đường dẫn tệp .csv
        target_column: tên cột chứa biến phụ thuộc
        """
        # Đọc dữ liệu từ tệp .csv
        data = pd.read_csv(filepath)
        
        # Kiểm tra tên cột phụ thuộc có hợp lệ không
        if target_column not in data.columns:
            raise ValueError(f"Cột '{target_column}' không tồn tại trong dữ liệu.")
        
        # Tách biến phụ thuộc (y) và biến độc lập (X)
        y = data[target_column].values
        X = data.drop(columns=[target_column]).values  # Loại bỏ cột phụ thuộc

        # In ra số cột của X để kiểm tra
        print(f"Số cột của X (biến độc lập): {X.shape[1]}")

        return X, y



    def fit(self, X, y):
        """
        Huấn luyện mô hình hồi quy tuyến tính nhiều biến bằng phương pháp bình phương nhỏ nhất.
        """
        X = np.column_stack([np.ones(X.shape[0]), X])  # Thêm cột intercept vào X
        self.coefficients = np.linalg.inv(X.T @ X) @ X.T @ y  # Tính hệ số hồi quy (bao gồm intercept)


    def predict(self, X):
        """
        Dự đoán giá trị từ các giá trị mới của biến độc lập.
        """
        if self.coefficients is None:
            raise ValueError("Mô hình chưa được huấn luyện. Hãy gọi fit() trước.")

        # Thêm cột bias (hệ số tự do)
        X = np.c_[np.ones(X.shape[0]), X]  # Thêm cột 1 vào X

        return X @ self.coefficients  # Nhân ma trận để dự đoán
    
    def summary(self):
        """
        Trả về thông tin mô hình hồi quy, bao gồm các hệ số.
        """
        if self.coefficients is not None:
            return f"Hệ số hồi quy: {self.coefficients}"
        else:
            raise ValueError("Mô hình chưa được huấn luyện. Hãy gọi fit() trước.")
    
    def get_coefficients(self):
        """
        Trả về các hệ số hồi quy
        """
        return self.coefficients
    
   