# multiple_regression/utils.py
import numpy as np

def standardize(X):
    """
    Chuẩn hóa dữ liệu về trung bình = 0 và độ lệch chuẩn = 1.
    """
    return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

def split_data(X, y, test_size=0.2):
    """
    Chia dữ liệu thành tập huấn luyện và kiểm tra.
    """
    n = len(X)
    test_size = int(n * test_size)
    X_train, X_test = X[:-test_size], X[-test_size:]
    y_train, y_test = y[:-test_size], y[-test_size:]
    return X_train, X_test, y_train, y_test
