import argparse
import numpy as np
import pandas as pd
from lstm_model import load_data, prepare_data, train_lstm_model, forecast_lstm, plot_predictions

# Hàm chạy toàn bộ chương trình
def run_lstm_from_file(filepath, feature_column="Value", time_steps=10, future_days=10):
    """
    Chạy toàn bộ chương trình: đọc dữ liệu, huấn luyện mô hình LSTM, dự báo và vẽ đồ thị.
    """
    # Load dữ liệu từ file CSV
    data = load_data(filepath)

    # Chuẩn bị dữ liệu
    X, y, scaler = prepare_data(data, feature_column, time_steps)

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    train_size = int(len(X) * 0.8)
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]

    # Huấn luyện mô hình
    model = train_lstm_model(X_train, y_train)

    # Dự báo giá trị trong tương lai
    predictions = forecast_lstm(model, data, feature_column, time_steps, future_days)

    # Chuyển đổi giá trị dự báo về dạng ban đầu
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    # In kết quả dự báo
    future_dates = pd.date_range(start=data.index[-1], periods=future_days + 1, freq="D")[1:]
    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted": predictions.flatten()})
    print("\nDự báo giá trị trong 10 ngày tới:")
    print(forecast_df)

    # Vẽ biểu đồ kết quả dự báo
    plot_predictions(data[feature_column], predictions.flatten(), future_dates)

# Thiết lập argparse để nhận filepath từ dòng lệnh
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chạy mô hình LSTM cho chuỗi thời gian từ file CSV.")
    parser.add_argument("filepath", type=str, help="Đường dẫn đến file CSV chứa dữ liệu chuỗi thời gian.")
    parser.add_argument("--feature_column", type=str, default="Value", help="Tên cột chứa giá trị chuỗi thời gian. Mặc định là 'Value'.")
    parser.add_argument("--time_steps", type=int, default=10, help="Số bước thời gian sử dụng làm đầu vào cho LSTM. Mặc định là 10.")
    parser.add_argument("--future_days", type=int, default=10, help="Số ngày dự báo trong tương lai. Mặc định là 10.")

    args = parser.parse_args()

    # Chạy mô hình LSTM với các tham số được cung cấp từ dòng lệnh
    run_lstm_from_file(args.filepath, args.feature_column, args.time_steps, args.future_days)
