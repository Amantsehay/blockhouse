from .base_strategy import IStrategy
class SMAStrategy(IStrategy):
    def __init__(self, initial_investment, short_window=50, long_window=200):
        super().__init__(initial_investment)
        self.short_window = short_window
        self.long_window = long_window

    def buy(self, data):
        """Buy when the price goes below the short moving average."""
        return data['close_price'] < data[f'EMA_{self.short_window}']
    
    def sell(self, data):
        """Sell when the price goes above the long moving average."""
        return data['close_price'] > data[f'EMA_{self.long_window}']

    def apply_indicators(self, data):
        """Add indicators (EMA) to the data."""
        data[f'EMA_{self.short_window}'] = data['close_price'].ewm(span=self.short_window, adjust=True).mean()
        data[f'EMA_{self.long_window}'] = data['close_price'].ewm(span=self.long_window, adjust=True).mean()
        return data

