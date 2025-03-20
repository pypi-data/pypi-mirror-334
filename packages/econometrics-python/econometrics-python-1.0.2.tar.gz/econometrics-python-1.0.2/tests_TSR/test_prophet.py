import unittest
import pandas as pd
import numpy as np
from TimeSeriesRegression.prophet import ProphetModel
import matplotlib.pyplot as plt

class TestProphetModel(unittest.TestCase):

    def setUp(self):
        """
        Chuẩn bị dữ liệu giả lập cho test.
        """
        # Tạo dữ liệu giả lập với các cột 'ds' (ngày) và 'y' (giá trị)
        dates = pd.date_range(start="2022-01-01", periods=100, freq='D')
        y = np.random.randn(100)  # Dữ liệu ngẫu nhiên cho 'y'
        
        self.dates = dates
        self.y = y
        self.model = ProphetModel()  # Khởi tạo mô hình Prophet
    
    def test_fit(self):
        """
        Kiểm tra xem mô hình có thể huấn luyện với dữ liệu hay không.
        """
        self.model.fit(self.y, self.dates)  # Huấn luyện mô hình với dữ liệu y và dates
        self.assertIsNotNone(self.model.model)  # Đảm bảo rằng mô hình đã được huấn luyện
    
    def test_predict(self):
        """
        Kiểm tra xem hàm predict có thể đưa ra dự báo đúng không.
        """
        self.model.fit(self.y, self.dates)  # Huấn luyện mô hình với dữ liệu y và dates
        forecast = self.model.predict(future_steps=10)  # Dự báo 10 bước tiếp theo
        self.assertEqual(len(forecast), 10)  # Đảm bảo rằng số bước dự báo là 10
    
    def test_summary(self):
        """
        Kiểm tra xem hàm summary có trả về tóm tắt mô hình hay không.
        """
        self.model.fit(self.y, self.dates)  # Huấn luyện mô hình với dữ liệu y và dates
        summary = self.model.summary()  # Lấy tóm tắt mô hình
        self.assertIn("Model", summary)  # Kiểm tra xem tóm tắt có chứa từ "Model"
    
    def test_plot(self):
        """
        Kiểm tra xem hàm plot có thể vẽ đồ thị mà không gặp lỗi không.
        """
        self.model.fit(self.y, self.dates)  # Huấn luyện mô hình với dữ liệu y và dates
        try:
            self.model.plot(self.y, future_steps=10)  # Vẽ đồ thị với dữ liệu và các giá trị dự đoán
            plt.close()  # Đảm bảo đóng đồ thị sau khi vẽ
        except Exception as e:
            self.fail(f"Hàm plot gặp lỗi: {e}")

if __name__ == "__main__":
    unittest.main()
