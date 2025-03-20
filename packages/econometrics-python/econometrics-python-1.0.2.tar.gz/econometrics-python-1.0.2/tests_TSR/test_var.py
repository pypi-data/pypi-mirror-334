import unittest
import numpy as np
from TimeSeriesRegression.var import VARModel
import matplotlib.pyplot as plt

class TestVARModel(unittest.TestCase):

    def setUp(self):
        """
        Chuẩn bị dữ liệu giả lập cho test.
        """
        # Tạo dữ liệu chuỗi thời gian giả lập với 2 biến (2 cột)
        np.random.seed(42)
        y = np.random.randn(1000, 2)  # Dữ liệu giả lập (1000 mẫu, 2 biến)
        
        self.y = y
        self.model = VARModel(p=1)  # Khởi tạo mô hình VAR với p=1 (1 lag)
    
    def test_fit(self):
        """
        Kiểm tra xem mô hình có thể huấn luyện với dữ liệu hay không.
        """
        self.model.fit(self.y)  # Huấn luyện mô hình với dữ liệu y
        self.assertIsNotNone(self.model.results)  # Đảm bảo rằng kết quả huấn luyện không phải là None
    
    def test_predict(self):
        """
        Kiểm tra xem hàm predict có thể đưa ra dự báo đúng không.
        """
        self.model.fit(self.y)  # Huấn luyện mô hình với dữ liệu y
        forecast = self.model.predict(steps=5)  # Dự báo 5 bước tiếp theo
        self.assertEqual(forecast.shape[0], 5)  # Đảm bảo rằng số bước dự báo là 5
    
    def test_summary(self):
        """
        Kiểm tra xem hàm summary có trả về tóm tắt mô hình hay không.
        """
        self.model.fit(self.y)  # Huấn luyện mô hình với dữ liệu y
        summary = self.model.summary()  # Lấy tóm tắt mô hình
        self.assertIn("Model", summary)  # Kiểm tra xem tóm tắt có chứa từ "Model"
    
    def test_plot(self):
        """
        Kiểm tra xem hàm plot có thể vẽ đồ thị mà không gặp lỗi không.
        """
        self.model.fit(self.y)  # Huấn luyện mô hình với dữ liệu y
        try:
            self.model.plot(self.y)  # Vẽ đồ thị với dữ liệu và các giá trị dự đoán
            plt.close()  # Đảm bảo đóng đồ thị sau khi vẽ
        except Exception as e:
            self.fail(f"Hàm plot gặp lỗi: {e}")

if __name__ == "__main__":
    unittest.main()
