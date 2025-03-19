# Econometrics 

## Author : Tran Minh Tam

## Linear Regression

A simple econometrics package for linear regression and plotting.

### Installation

You can install the package via pip: pip install econometrics

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

