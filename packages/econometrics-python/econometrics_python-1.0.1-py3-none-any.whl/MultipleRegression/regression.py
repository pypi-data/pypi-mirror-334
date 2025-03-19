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
        self.X = X  # Lưu trữ X
        self.y = y  # Lưu trữ y

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
        Trả về thông tin mô hình hồi quy, bao gồm các hệ số và R-squared.
        """
        if self.coefficients is not None:
            # Tính toán giá trị dự đoán
            X_with_intercept = np.column_stack([np.ones(len(self.X)), self.X])  # Thêm cột intercept vào X
            y_pred = X_with_intercept @ self.coefficients  # Dự đoán giá trị

            # Tính R-squared
            residuals = self.y - y_pred  # Sai số giữa giá trị thực và giá trị dự đoán
            ss_res = np.sum(residuals**2)  # Tổng sai số bình phương
            ss_tot = np.sum((self.y - np.mean(self.y))**2)  # Tổng biến thiên
            r_squared = 1 - (ss_res / ss_tot)  # Tính R-squared

            # In thông tin tóm tắt
            summary = f"Hệ số hồi quy: {self.coefficients}\n"
            summary += f"R-squared: {r_squared}\n"
            return summary
        else:
            raise ValueError("Mô hình chưa được huấn luyện. Hãy gọi fit() trước.")
    
    def get_coefficients(self):
        """
        Trả về các hệ số hồi quy
        """
        return self.coefficients
    
   