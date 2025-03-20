import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Dùng cho đồ thị 3D


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
        Huấn luyện mô hình hồi quy tuyến tính nhiều biến bằng phương pháp bình phương nhỏ nhất (OLS).
        """
        # Thêm cột intercept vào X
        X = sm.add_constant(X)  # Thêm cột 1 vào X cho intercept
        self.model = sm.OLS(y, X).fit()  # Huấn luyện mô hình OLS
        self.coefficients = self.model.params  # Lưu hệ số hồi quy

    def predict(self, X):
        """
        Dự đoán giá trị từ các giá trị mới của biến độc lập.
        """
        if self.coefficients is None:
            raise ValueError("Mô hình chưa được huấn luyện. Hãy gọi fit() trước.")

        # Thêm cột intercept vào X nếu chưa có
        X = sm.add_constant(X)  # Thêm cột 1 vào X cho intercept
        return self.model.predict(X)  # Dự đoán với mô hình

    def summary(self):
        """
        Trả về thông tin mô hình hồi quy OLS.
        """
        if self.model is not None:
            return self.model.summary()  # Trả về tóm tắt của mô hình OLS
        else:
            raise ValueError("Mô hình chưa được huấn luyện. Hãy gọi fit() trước.")
    
    def get_coefficients(self):
        """
        Trả về các hệ số hồi quy
        """
        return self.coefficients

    def plot(self, X, y):
        """
        Vẽ đồ thị hồi quy dựa trên số lượng biến độc lập:
        - 1 biến: Đồ thị 2D
        - 2 biến: Đồ thị 3D
        - >= 3 biến: Không thể vẽ, chỉ hiển thị thông báo
        """
        if X.shape[1] == 1:  # Trường hợp 1 biến độc lập
            plt.scatter(X, y, color="blue", label="Dữ liệu thực tế")
            plt.plot(X, self.predict(X), color="red", label="Hồi quy tuyến tính")
            plt.xlabel("Biến độc lập")
            plt.ylabel("Biến phụ thuộc")
            plt.legend()
            plt.title("Hồi quy tuyến tính (1 biến)")
            plt.show()

        elif X.shape[1] == 2:  # Trường hợp 2 biến độc lập
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

            # Vẽ điểm dữ liệu
            ax.scatter(X[:, 0], X[:, 1], y, color="blue", label="Dữ liệu thực tế")

            # Vẽ mặt phẳng hồi quy
            x_range = np.linspace(X[:, 0].min(), X[:, 0].max(), 10)
            y_range = np.linspace(X[:, 1].min(), X[:, 1].max(), 10)
            X_grid, Y_grid = np.meshgrid(x_range, y_range)
            Z_pred = self.predict(np.c_[X_grid.ravel(), Y_grid.ravel()]).reshape(X_grid.shape)

            ax.plot_surface(X_grid, Y_grid, Z_pred, color="red", alpha=0.5)

            ax.set_xlabel("Biến 1")
            ax.set_ylabel("Biến 2")
            ax.set_zlabel("Biến phụ thuộc")
            plt.title("Hồi quy tuyến tính 3D")
            plt.legend()
            plt.show()

        else:  # Trường hợp >= 3 biến độc lập
            print("⚠️ Không thể vẽ đồ thị nếu có từ 3 biến độc lập trở lên.")
