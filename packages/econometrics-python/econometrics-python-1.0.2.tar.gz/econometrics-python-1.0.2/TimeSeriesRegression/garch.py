import matplotlib.pyplot as plt
from arch import arch_model

class GARCHModel:
    def __init__(self, p=1, q=1):
        self.p = p  # Số lag cho phần AR (autoregressive)
        self.q = q  # Số lag cho phần MA (moving average)
        self.model = None
        self.results = None

    def fit(self, y):
        """
        Huấn luyện mô hình GARCH với chuỗi thời gian y.
        """
        self.model = arch_model(y, vol='Garch', p=self.p, q=self.q)
        self.results = self.model.fit(disp="off")  # disp="off" để tắt thông báo huấn luyện

    def predict(self, steps=1):
        """
        Dự báo phương sai cho các bước tiếp theo.
        """
        if self.results is None:
            raise ValueError("Mô hình chưa được huấn luyện.")
        return self.results.forecast(horizon=steps)

    def summary(self):
        """
        Tóm tắt mô hình GARCH.
        """
        if self.results:
            return self.results.summary()
        else:
            raise ValueError("Mô hình chưa được huấn luyện.")
    
    def plot(self, y):
        """
        Vẽ đồ thị phương sai ước lượng (volatility) và dữ liệu thực tế.
        """
        if self.results is None:
            raise ValueError("Mô hình chưa được huấn luyện.")
        
        # Dự báo phương sai (volatility) ước lượng
        volatility = self.results.conditional_volatility

        # Vẽ đồ thị
        plt.figure(figsize=(10, 6))
        plt.plot(y, label='Actual')
        plt.plot(volatility, label='Estimated Volatility', color='red')
        plt.legend()
        plt.title('GARCH Model: Actual vs Estimated Volatility')
        plt.show()
