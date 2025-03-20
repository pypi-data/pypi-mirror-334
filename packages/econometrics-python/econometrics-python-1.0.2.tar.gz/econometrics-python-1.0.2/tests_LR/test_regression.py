# tests/test_regression.py
import unittest
import numpy as np
from MultipleRegression.regression import MultipleRegression

class TestMultipleRegression(unittest.TestCase):
    def test_fit_predict(self):
        X = np.array([[1], [2], [3], [4]])
        y = np.array([1, 2, 3, 4])

        model = MultipleRegression()
        model.fit(X, y)
        
        predictions = model.predict(X)
        
        # Kiểm tra xem mô hình có đưa ra dự đoán chính xác không
        self.assertTrue(np.allclose(predictions, y))
    
    def test_summary(self):
        X = np.array([[1], [2], [3], [4]])
        y = np.array([1, 2, 3, 4])
        
        model = MultipleRegression()
        model.fit(X, y)
        
        summary = model.summary()
        self.assertIn("R-squared", summary)  # Kiểm tra tóm tắt mô hình có chứa R-squared
    
    def test_plot(self):
        X = np.array([[1, 3], [2, 4], [3, 5], [4, 6]])
        y = np.array([1, 2, 3, 4])
        
        model = MultipleRegression()
        model.fit(X, y)
        
        try:
            model.plot(X, y)  # Kiểm tra vẽ đồ thị
            success = True
        except Exception as e:
            success = False
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()
