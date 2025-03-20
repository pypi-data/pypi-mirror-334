import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def plot_regression(X, y, model):
    """
    Vẽ đồ thị hồi quy dựa trên số lượng biến độc lập:
    - 1 biến: Đồ thị 2D
    - 2 biến: Đồ thị 3D
    - >= 3 biến: Không thể vẽ, chỉ hiển thị thông báo
    """
    
    if X.shape[1] == 1:  # Trường hợp 1 biến độc lập
        plt.scatter(X, y, color="blue", label="Dữ liệu thực tế")
        plt.plot(X, model.predict(X), color="red", label="Dự đoán hồi quy")
        plt.xlabel("Biến độc lập")
        plt.ylabel("Biến phụ thuộc")
        plt.legend()
        plt.title("Mô hình hồi quy tuyến tính (1 biến)")
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
        Z_pred = model.predict(np.c_[X_grid.ravel(), Y_grid.ravel()]).reshape(X_grid.shape)

        ax.plot_surface(X_grid, Y_grid, Z_pred, color="red", alpha=0.5)

        ax.set_xlabel("Biến 1")
        ax.set_ylabel("Biến 2")
        ax.set_zlabel("Biến phụ thuộc")
        plt.title("Mô hình hồi quy tuyến tính 3D")
        plt.legend()
        plt.show()

    else:  # Trường hợp >= 3 biến độc lập
        print("⚠️ Không thể vẽ đồ thị nếu có từ 3 biến độc lập trở lên.")
