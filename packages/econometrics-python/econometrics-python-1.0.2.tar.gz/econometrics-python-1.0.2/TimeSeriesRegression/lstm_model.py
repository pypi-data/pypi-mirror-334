import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# 1. Đọc dữ liệu và xử lý chuỗi thời gian từ file .csv
def load_data(filepath):
    """
    Đọc dữ liệu từ file CSV và xử lý nó.
    """
    data = pd.read_csv(filepath)
    
    # Giả sử file có cột "Date" là ngày và "Value" là giá trị chuỗi thời gian
    data["Date"] = pd.to_datetime(data["Date"])  # Chuyển cột "Date" thành datetime
    data.set_index("Date", inplace=True)  # Đặt cột "Date" làm index
    data = data.asfreq('D')  # Đặt tần suất là hàng ngày nếu cần

    return data

# 2. Chuẩn bị dữ liệu cho mô hình LSTM
def prepare_data(data, feature_column, time_steps=10):
    """
    Chuẩn bị dữ liệu cho mô hình LSTM với `time_steps` bước thời gian.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[[feature_column]])

    X, y = [], []
    for i in range(time_steps, len(scaled_data)):
        X.append(scaled_data[i-time_steps:i, 0])  # Lấy time_steps ngày trước đó làm đầu vào
        y.append(scaled_data[i, 0])  # Lấy giá trị hiện tại làm nhãn

    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))  # Định dạng đầu vào cho LSTM

    return X, y, scaler

# 3. Xây dựng mô hình LSTM
def build_lstm_model(time_steps):
    """
    Xây dựng mô hình LSTM với 2 lớp LSTM và 2 lớp Dense.
    """
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(time_steps, 1)),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# 4. Huấn luyện mô hình LSTM
def train_lstm_model(X_train, y_train, epochs=50, batch_size=16):
    """
    Huấn luyện mô hình LSTM với dữ liệu huấn luyện X_train và y_train.
    """
    time_steps = X_train.shape[1]
    model = build_lstm_model(time_steps)
    
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    return model

# 5. Dự báo giá trị tương lai
def forecast_lstm(model, data, feature_column, time_steps=10, future_days=10):
    """
    Dự báo giá trị trong tương lai dựa trên mô hình LSTM.
    """
    X_last = data[feature_column].values[-time_steps:]  # Lấy dữ liệu gần nhất
    X_last = X_last.reshape((1, time_steps, 1))  # Định dạng lại cho mô hình

    predictions = []
    for _ in range(future_days):
        pred = model.predict(X_last)[0, 0]
        predictions.append(pred)
        
        # Cập nhật dữ liệu dự báo để tiếp tục dự báo bước tiếp theo
        X_last = np.append(X_last[:, 1:, :], [[[pred]]], axis=1)

    return predictions

# 6. Vẽ đồ thị dự báo
def plot_predictions(actual_data, forecasted_data, future_dates):
    """
    Vẽ đồ thị kết quả dự báo và dữ liệu thực tế.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(actual_data.index, actual_data, label="Giá trị thực tế", color="blue")
    plt.plot(future_dates, forecasted_data, label="Dự báo", color="red", linestyle="dashed")
    plt.xlabel("Thời gian")
    plt.ylabel("Giá trị")
    plt.title("Dự báo chuỗi thời gian bằng LSTM")
    plt.legend()
    plt.grid(True)
    plt.show()
