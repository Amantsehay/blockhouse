from core.tasks import fetch_stock_data, get_stock_data
from datetime import datetime
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class StockPricePredictor:
    def __init__(self, stock_symbol, model_path='core/ml_price_prediction/stock_price_model.pkl'):
        self.stock_symbol = stock_symbol
        self.model_path = model_path
        self.model = None
        self.historical_data = None

    def fetch_historical_data(self):
        cutoff_date = (datetime.now() - pd.Timedelta(days=2 * 365)).date()
        stock_data = get_stock_data(self.stock_symbol)

        if stock_data.empty or stock_data['date'].min() > cutoff_date:
            fetch_stock_data(self.stock_symbol)
            stock_data = get_stock_data(self.stock_symbol)
        self.historical_data = stock_data
        self.historical_data['moving_average_5'] = self.historical_data['close_price'].rolling(window=5).mean()
        self.historical_data['moving_average_10'] = self.historical_data['close_price'].rolling(window=10).mean()
        self.historical_data.dropna(inplace=True)

    def train_model(self):
        if self.historical_data is None:
            self.fetch_historical_data()

        X = self.historical_data[['moving_average_5', 'moving_average_10']]
        y = self.historical_data['close_price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        joblib.dump(self.model, self.model_path)
        print("Model trained and saved to", self.model_path)

    def load_model(self):
        try:
            self.model = joblib.load(self.model_path)
            print("Model loaded successfully.")
        except FileNotFoundError:
            print("Model file not found. Please train the model first.")

    def predict_future_prices(self):
        if self.model is None:
            self.load_model()
        if self.historical_data is None:
            self.fetch_historical_data()

        X = self.historical_data[['moving_average_5', 'moving_average_10']].tail(30)
        future_dates = pd.date_range(start=self.historical_data['date'].iloc[-1] + pd.Timedelta(days=1), periods=30)
        predictions = self.model.predict(X)

        # Format predictions to 2 decimal places
        predictions = [round(prediction, 2) for prediction in predictions]
        
        return pd.DataFrame(predictions, index=future_dates, columns=['Predicted Price'])


