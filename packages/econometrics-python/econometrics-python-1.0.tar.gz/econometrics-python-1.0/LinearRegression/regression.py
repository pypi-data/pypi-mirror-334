import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression as SklearnLR


class LinearRegression:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.load_data()
        self.x_column = self.data.columns[0]  # Cột đầu tiên là X
        self.y_column = self.data.columns[1]  # Cột thứ hai là Y
        self.results = None

    def load_data(self):
        data = pd.read_csv(self.data_file, sep=';')
        print("Columns in the data:", data.columns)
        return data

    def fit(self):
        X = self.data[[self.x_column]].values  # X phải là mảng 2D
        Y = self.data[self.y_column].values
        model = SklearnLR()
        model.fit(X, Y)  # Huấn luyện mô hình
        fittedvalues = model.predict(X)  # Dự đoán các giá trị Y từ X
        self.results = {
            "slope": model.coef_[0],
            "intercept": model.intercept_,
            "fittedvalues": fittedvalues  # Lưu giá trị dự đoán vào results
        }

    def summary(self):
        if self.results is None:
            print("Model is not trained yet.")
            return
        print(f"Slope: {self.results['slope']}")
        print(f"Intercept: {self.results['intercept']}")
        print(f"Using {self.x_column} as the independent variable (X) and {self.y_column} as the dependent variable (Y).")

    def plot(self):
        if self.results is None:
            print("Model is not trained yet.")
            return
        # Vẽ biểu đồ
        X = self.data[self.x_column].values
        Y = self.data[self.y_column].values
        plt.scatter(X, Y, color='blue', label='Dữ liệu thực tế')
        plt.plot(X, self.results["fittedvalues"], color='red', label='Hồi quy tuyến tính')
        plt.xlabel(self.x_column)
        plt.ylabel(self.y_column)
        plt.legend()
        plt.show()

# Ví dụ sử dụng
if __name__ == "__main__":
    # Đảm bảo đường dẫn đến file CSV đúng
    model = LinearRegression(data_file='linear_regression.csv')
    model.fit()
    model.summary()
    model.plot()