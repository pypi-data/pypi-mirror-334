import unittest
import numpy as np
from TimeSeriesRegression.arima import ARIMAModel

class TestARIMAModel(unittest.TestCase):
    def test_fit_predict(self):
        X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        model = ARIMAModel(p=1, d=0, q=0)
        model.fit(y)
        
        predictions = model.predict(steps=5)
        
        # Kiểm tra xem mô hình có đưa ra dự đoán chính xác không
        self.assertTrue(np.allclose(predictions, y[-5:]))
    
    def test_plot(self):
        X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        model = ARIMAModel(p=1, d=0, q=0)
        model.fit(y)
        model.plot(y)

if __name__ == "__main__":
    unittest.main()
