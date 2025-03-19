# Econometrics 

## Author : Tran Minh Tam

## Installation

You can install the package via pip: 
```
pip install econometrics
```

## Linear Regression

A simple econometrics package for linear regression and plotting.


### Run with the package
```python

from LinearRegression.regression import LinearRegression

# Tạo một đối tượng (instance) của lớp LinearRegression và truyền vào file dữ liệu './data_file.csv' để sử dụng trong quá trình hồi quy tuyến tính
model = LinearRegression(data_file='./data_file.csv')

# Huấn luyện mô hình
model.fit()

# In ra kết quả summary
model.summary()

# Vẽ đồ thị
model.plot()
```

## Multiple Linear Regression
### Run with the package
```python
import numpy as np
from MultipleRegression.regression import MultipleRegression
from MultipleRegression.plot import plot_regression

# Đọc dữ liệu
filepath = "du_lieu.csv"
target_column = "Giá"  # Ví dụ: Cột giá nhà
model = MultipleRegression()
X, y = model.load_data(filepath, target_column)

# Huấn luyện mô hình
model.fit(X, y)

# In các hệ số hồi quy
print("Hệ số hồi quy:", model.get_coefficients())

# In tóm tắt mô hình
print("Tóm tắt mô hình:")
print(model.summary())

# Dự đoán thử
new_data = np.array([[2500, 3]])  # Chuyển new_data thành numpy array
prediction = model.predict(new_data)
print("Dự đoán:", prediction)

# Gọi hàm vẽ đồ thị
plot_regression(X, y, model)
