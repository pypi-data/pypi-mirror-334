import unittest
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        
if __name__ == "__main__":
    unittest.main()
