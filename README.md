Stock Data API
==============

This Django-based REST API provides endpoints for:

1.  **EMA Backtesting**: Calculates and simulates an Exponential Moving Average (EMA) strategy for a stock.
2.  **Stock Data Fetching**: Fetches and stores historical stock data for a given symbol.
3.  **Price Prediction**: Predicts future stock prices using a pre-trained ML model and stores the results.

* * *

Table of Contents
-----------------

1.  [Requirements](#requirements)
2.  [Installation](#installation)
3.  [Usage](#usage)
4.  [API Endpoints](#api-endpoints)
5.  [Database Models](#database-models)
6.  [Error Handling](#error-handling)
7.  [Testing](#testing)

* * *

Requirements
------------

*   **Python 3.x**
*   **Django REST Framework**
*   **Pandas, Numpy**
*   **PostgreSQL**: Database for storing stock data and predictions.
*   Additional dependencies as listed in `requirements.txt`.

* * *

Installation
------------

1.  **Clone the repository**:
    
        git clone https://github.com/Amantsehay/blockhouse
        cd blockhouse/tradingbot
    
2.  **Install dependencies**:
    
        pip install -r requirements.txt
    
3.  **Run database migrations**:
    
        python manage.py migrate
    
4.  **Start the development server**:
    
        python manage.py runserver
    

* * *

Usage
-----

Send POST requests to each endpoint with JSON data formatted as specified in [API Endpoints](#api-endpoints).

**Note**: Update configurations for any external services as needed.

* * *

API Endpoints
-------------

### 1\. EMA Strategy Endpoint

**Endpoint**: `/ema-strategy/`  
**Method**: `POST`  
**Description**: Backtests an EMA strategy with user-specified parameters.

**Request Body**:

    {
        "short_window": 10,
        "long_window": 50,
        "stock_symbol": "AAPL",
        "initial_investment": 10000.00
    }

**Response**:

*   **Success (200 OK)**:
    
        {
                    "message": "Backtest completed successfully",
                    "final_value": 12000.00,
                    "report": {
                        "total_trades": 5,
                        "profit": 2000.00,
                        ...
                    }
                }
    
*   **Error (400/500)**:
    
        {
                    "error": "Error message here"
                }
    

### 2\. Fetch Stock Data Endpoint

**Endpoint**: `/fetch-stock-data/`  
**Method**: `POST`  
**Description**: Fetches historical data for a given stock symbol and stores it in the database.

**Request Body**:

    {
        "stock_symbol": "AAPL"
    }

**Response**:

*   **Success (200 OK)**:
    
        {
                    "message": "Data fetched successfully"
                }
    
*   **Error (400/500)**:
    
        {
                    "error": "Error message here"
                }
    

### 3\. Predict Stock Price Endpoint

**Endpoint**: `/predict-stock-price/`  
**Method**: `POST`  
**Description**: Predicts future prices for a stock symbol using a pre-trained model and stores predictions in the database.

**Request Body**:

    {
        "stock_symbol": "AAPL"
    }

**Response**:

*   **Success (200 OK)**:
    
        {
                    "message": "Predictions generated successfully",
                    "predictions": [
                        {"date": "2023-10-25", "predicted_price": 150.00},
                        {"date": "2023-10-26", "predicted_price": 152.50},
                        ...
                    ]
                }
    
*   **Error (400/500)**:
    
        {
                    "error": "Error message here"
                }
    

* * *

Database Models
---------------

*   **StockModel**: Stores historical stock data.
*   **PredictedPriceModel**: Stores predicted future prices for a stock.

* * *

Error Handling
--------------

*   **400 Bad Request**: Returns if the request body fails validation or required fields are missing.
*   **500 Internal Server Error**: Returns if any unhandled exception occurs during processing.

Each endpoint validates incoming data with Django serializers. Errors are returned with descriptive messages to help diagnose issues quickly.

* * *

Testing
-------

To run unit tests for the API:

    python manage.py test

Make sure to write test cases for each endpoint and data validation method to ensure functionality and reliability.

* * *