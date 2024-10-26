import re
import requests
from config import settings
from .models import StockModel
from django.db import IntegrityError, OperationalError
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol):
    print('Fetching data for:', symbol)
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": settings.ALPHA_VANTAGE_API_KEY,
        "outputsize": "full",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return f"Error fetching data from API: {str(e)}", 500
    except ValueError:
        return "Error parsing JSON response from API", 500

    time_series = data.get("Time Series (Daily)")
    if not time_series:
        return "Error fetching data: No time series available", 404

    # Filter data to only the last two years
    cutoff_date = datetime.now() - timedelta(days=2 * 365)
    filtered_data = {
        date: daily_data for date, daily_data in time_series.items()
        if datetime.strptime(date, '%Y-%m-%d') >= cutoff_date
    }

    if not filtered_data:
        return "No data available for the last two years", 404

    # Save filtered data to the database
    for date, daily_data in filtered_data.items():
        try:
            StockModel.objects.update_or_create(
                symbol=symbol,
                date=date,
                defaults={
                    'open_price': daily_data['1. open'],
                    'close_price': daily_data['4. close'],
                    'high_price': daily_data['2. high'],
                    'low_price': daily_data['3. low'],
                    'volume': daily_data['5. volume'],
                }
            )
        except (IntegrityError, OperationalError) as db_error:
            return f"Database error while saving data: {str(db_error)}", 500
        except KeyError as key_error:
            return f"Missing expected data key: {str(key_error)}", 400

    return "Data successfully fetched", 200

def get_stock_data(symbol):
    try:
        stock_data = StockModel.objects.filter(symbol=symbol).order_by('date')

        # Check if stock data is empty
        if not stock_data.exists():
            return f"No data found for symbol: {symbol}", 404

        # Convert to DataFrame
        df = pd.DataFrame(list(stock_data.values('date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume')))

        # Check for missing values and report
        missing_data_count = df.isnull().sum().sum()
        if missing_data_count > 0:
            return f"Warning: Found {missing_data_count} missing values in stock data", 400

        return df, 200
    except OperationalError as db_error:
        return f"Database error while fetching data: {str(db_error)}", 500
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", 500
