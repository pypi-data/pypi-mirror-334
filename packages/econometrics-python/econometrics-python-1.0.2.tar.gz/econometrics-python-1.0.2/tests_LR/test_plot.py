import unittest
import matplotlib.pyplot as plt
from LinearRegression.plot import plot_regression_line
import numpy as np

class TestPlot(unittest.TestCase):
    def setUp(self):
        # Tạo dữ liệu mẫu để vẽ
        self.x = np.linspace(0, 10, 100)
        self.y = 2 * self.x + 1  # Hồi quy tuyến tính giả lập: y = 2x + 1
        self.fitted_values = self.y  # Với dữ liệu này, fitted_values chính là y
        
    def test_plot_regression_line(self):
        # Kiểm tra xem đồ thị có thể vẽ không
        try:
            plot_regression_line(self.x, self.y, self.fitted_values, 'X', 'Y', 'Linear Regression')
            plt.close()  # Đóng lại sau khi kiểm tra
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Đã xảy ra lỗi khi vẽ đồ thị: {e}")
    
if __name__ == '__main__':
    unittest.main()
