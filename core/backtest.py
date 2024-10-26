from core.tasks import get_stock_data, fetch_stock_data
from .strategies.sample_strategy import SMAStrategy

def run_backtest(symbol, initial_investment, short_window=50, long_window=200):
    print("Running backtest for symbol:", symbol)
    fetch_stock_data(symbol)
    
   
    try:
        data = get_stock_data(symbol)
        

        if data.empty:
            print(f"No data found for symbol {symbol}. Fetching new data...")
            fetch_stock_data(symbol)
            data = get_stock_data(symbol)
            
            # Check again in case data retrieval fails
            if data.empty:
                raise ValueError(f"No data available for symbol {symbol} after fetching.")
    
    except Exception as e:
        print(f"Error retrieving data for {symbol}: {str(e)}")
        return None, None, None

    # Initialize and run the strategy
    strategy = SMAStrategy(initial_investment, short_window=short_window, long_window=long_window)
    data = strategy.apply_indicators(data)
    data, trades, final_value = strategy.run(data)
    
    # Save results to CSV
    data.to_csv('results/backtest_results.csv', index=False)
    return data, trades, final_value
