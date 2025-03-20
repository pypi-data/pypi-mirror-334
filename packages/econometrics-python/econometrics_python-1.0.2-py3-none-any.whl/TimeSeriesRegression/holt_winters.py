import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt

class HoltWintersModel:
    def __init__(self, trend='add', seasonal='add', seasonal_periods=12):
        self.trend = trend
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        self.model = None
        self.results = None

    def fit(self, y):
        """
        Huấn luyện mô hình Holt-Winters với chuỗi thời gian y.
        """
        self.model = ExponentialSmoothing(y, trend=self.trend, seasonal=self.seasonal, seasonal_periods=self.seasonal_periods)
        self.results = self.model.fit()

    def predict(self, steps=1):
        """
        Dự báo giá trị cho các bước tiếp theo.
        """
        if self.results is None:
            raise ValueError("Mô hình chưa được huấn luyện.")
        return self.results.forecast(steps=steps)

    def summary(self):
        """
        Tóm tắt mô hình Holt-Winters.
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
        plt.plot(self.results.fittedvalues, label='Fitted', color='red')
        plt.legend()
        plt.title('Holt-Winters Model: Actual vs Fitted')
        plt.show()
