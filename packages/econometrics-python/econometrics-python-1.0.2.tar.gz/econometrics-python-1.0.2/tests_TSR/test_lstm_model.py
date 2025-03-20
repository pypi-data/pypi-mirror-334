import unittest
import numpy as np
import pandas as pd 
from TimeSeriesRegression.lstm_model import load_data, prepare_data, train_lstm_model, forecast_lstm, plot_predictions


class TestLSTMModel(unittest.TestCase):

    def test_train_lstm_model(self):
        # Giả sử có sẵn dữ liệu training
        filepath = 'time_series_data.csv'
        data = load_data(filepath)
        feature_column = 'Value'
        time_steps = 10
        X, y, scaler = prepare_data(data, feature_column, time_steps)
        model = train_lstm_model(X, y)
        
        # Kiểm tra mô hình huấn luyện thành công
        self.assertIsNotNone(model)

    def test_forecast_lstm_reshape(self):
        # Giả sử có sẵn dữ liệu và mô hình đã huấn luyện
        filepath = 'time_series_data.csv'
        data = load_data(filepath)
        feature_column = 'Value'
        time_steps = 10
        X, y, scaler = prepare_data(data, feature_column, time_steps)
        model = train_lstm_model(X, y)

        # Dự báo giá trị trong 5 ngày tới
        future_days = 5
        forecast = forecast_lstm(model, data, feature_column, time_steps, future_days)

        # Chuyển dự báo thành NumPy array nếu nó là list
        forecast = np.array(forecast)

        # Kiểm tra xem forecast có hình dạng (5,) hay không
        self.assertEqual(forecast.shape, (5,))  # Dự báo là mảng 1 chiều với 5 giá trị

    def test_plot_predictions(self):
        # Kiểm tra hàm vẽ dự báo
        filepath = 'time_series_data.csv'
        data = load_data(filepath)
        feature_column = 'Value'
        time_steps = 10
        X, y, scaler = prepare_data(data, feature_column, time_steps)
        model = train_lstm_model(X, y)

        # Dự báo
        future_days = 5
        forecast = forecast_lstm(model, data, feature_column, time_steps, future_days)

        # Chuyển dự báo thành NumPy array
        forecast = np.array(forecast)
        
        # Vẽ đồ thị dự báo
        plot_predictions(data[feature_column], forecast.flatten(), pd.date_range(start=data.index[-1], periods=future_days + 1, freq="D")[1:])

if __name__ == "__main__":
    unittest.main()
