from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt 

class ProphetModel:
    def __init__(self, yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False):
        self.model = None
        self.results = None
        self.yearly_seasonality = yearly_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.daily_seasonality = daily_seasonality

    def fit(self, y, dates):
        """
        Huấn luyện mô hình Prophet với chuỗi thời gian y và các ngày (dates).
        """
        # Tạo DataFrame cho Prophet
        data = pd.DataFrame({'ds': dates, 'y': y})
        
        # Khởi tạo mô hình Prophet
        self.model = Prophet(
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            daily_seasonality=self.daily_seasonality
        )
        
        # Huấn luyện mô hình
        self.model.fit(data)

    def predict(self, future_steps=30):
        """
        Dự báo giá trị cho các bước tiếp theo.
        """
        if self.model is None:
            raise ValueError("Mô hình chưa được huấn luyện.")
        
        # Tạo DataFrame các ngày trong tương lai
        future = self.model.make_future_dataframe(self.model.history, periods=future_steps)
        
        # Dự báo giá trị
        forecast = self.model.predict(future)
        
        return forecast

    def summary(self):
        """
        Tóm tắt mô hình Prophet.
        """
        if self.model:
            return self.model.summary()
        else:
            raise ValueError("Mô hình chưa được huấn luyện.")
    
    def plot(self, y, future_steps=30):
        """
        Vẽ đồ thị dự đoán và dữ liệu thực tế.
        """
        forecast = self.predict(future_steps)
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.model.history['ds'], y, label='Actual')
        plt.plot(forecast['ds'], forecast['yhat'], label='Predicted', color='red')
        plt.legend()
        plt.title('Prophet Model: Actual vs Predicted')
        plt.show()
