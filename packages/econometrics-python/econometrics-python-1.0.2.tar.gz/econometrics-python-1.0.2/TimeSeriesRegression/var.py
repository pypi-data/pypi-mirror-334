import pandas as pd
from statsmodels.tsa.api import VAR

class VARModel:
    def __init__(self, p=1):
        self.p = p
        self.model = None
        self.results = None

    def fit(self, X):
        """
        Huấn luyện mô hình VAR với dữ liệu đầu vào X (các biến đa chiều).
        """
        self.model = VAR(X)
        self.results = self.model.fit(self.p)

    def predict(self, steps=1):
        """
        Dự báo các bước tiếp theo của các chuỗi thời gian.
        """
        if self.results is None:
            raise ValueError("Mô hình chưa được huấn luyện.")
        return self.results.forecast(self.results.endog, steps=steps)

    def summary(self):
        """
        Tóm tắt mô hình VAR.
        """
        if self.results:
            return self.results.summary()
        else:
            raise ValueError("Mô hình chưa được huấn luyện.")
