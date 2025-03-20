import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

class SARIMAModel:
    def __init__(self, p=1, d=1, q=1, P=1, D=1, Q=1, s=12):
        self.p = p
        self.d = d
        self.q = q
        self.P = P
        self.D = D
        self.Q = Q
        self.s = s
        self.model = None
        self.results = None

    def fit(self, y):
        """
        Huấn luyện mô hình SARIMA với chuỗi thời gian y.
        """
        self.model = sm.tsa.SARIMAX(y, order=(self.p, self.d, self.q), seasonal_order=(self.P, self.D, self.Q, self.s))
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
        Tóm tắt mô hình SARIMA.
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
        plt.title('SARIMA Model: Actual vs Fitted')
        plt.show()
