import requests

url = "http://127.0.0.1:8000/api/predict-future-price/"
data = {
    # "short_window": 50,
    # "long_window": 200,
    # "initial_investment": 10000,
    "stock_symbol": "MSFT"
    # 'ticker':'AAPL'
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Response JSON:", "OK", response.json())
else:
    print("Error:", response)
