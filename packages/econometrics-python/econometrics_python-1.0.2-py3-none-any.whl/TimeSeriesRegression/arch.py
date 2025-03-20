from arch import arch_model
import pandas as pd
import matplotlib.pyplot as plt 


class ARCHModel:
    def __init__(self, p=1):
        self.p = p
        self.model = None
        self.results = None

    def fit(self, y):
        """
        Huấn luyện mô hình ARCH với chuỗi thời gian y.
        """
        self.model = arch_model(y, vol='ARCH', p=self.p)
        self.results = self.model.fit()

    def predict(self, steps=1):
        """
        Dự báo phương sai cho các bước tiếp theo.
        """
        if self.results is None:
            raise ValueError("Mô hình chưa được huấn luyện.")
        return self.results.forecast(horizon=steps)

    def summary(self):
        """
        Tóm tắt mô hình ARCH.
        """
        if self.results:
            return self.results.summary()
        else:
            raise ValueError("Mô hình chưa được huấn luyện.")

    def plot(self, y):
        """
        Vẽ đồ thị dự đoán và dữ liệu thực tế.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(y, label='Actual')
        plt.legend()
        plt.title('ARCH Model: Actual vs Fitted')
        plt.show()