from decimal import Decimal
from abc import ABC, abstractmethod
import pandas as pd

class IStrategy(ABC):
    def __init__(self, initial_investment):
        self.initial_investment = Decimal(initial_investment)
        self.position = 0
        self.cash = Decimal(initial_investment)
        self.stock_quantity = 0
        self.trades = []  # Store trade details
    
    @abstractmethod
    def buy(self, data):
        """Define the conditions for buying here."""
        pass
    
    @abstractmethod
    def sell(self, data):
        """Define the conditions for selling here."""
        pass

    def log_trade(self, action, price, quantity, cash, position_type):
        """Log each trade with action (buy/sell), price, quantity, cash balance, and position type."""
        trade = {
            'Action': action,
            'Price': float(price),  # Convert to float for better readability
            'Quantity': quantity,
            'Position': 'Long' if action == 'Buy' else 'Short',
            'Cash': float(cash),  # Convert to float for better readability
            'Type': position_type  # Indicate whether opening or closing
        }
        self.trades.append(trade)

    def run(self, data):
        """Executes the strategy with alternating long and short positions."""
        data['signal'] = 0  
        self.position = 0  
        print('Running strategy...')
        
        try:
            for i in range(1, len(data)):
                if self.cash < 0:
                    print("Cash depleted, stopping trades.")
                    return data, self.trades, 0

                close_price = Decimal(data.iloc[i]['close_price'])  # Convert close price to Decimal

                if self.position == 0:  # No position open
                    if self.buy(data.iloc[i]):
                        data.at[i, 'signal'] = 1
                        self.stock_quantity = int(self.cash // close_price)  # Floor division for stock quantity
                        self.cash -= Decimal(self.stock_quantity) * close_price
                        self.position = 1  
                        self.log_trade('Buy', close_price, self.stock_quantity, self.cash, 'Opening')

                    elif self.sell(data.iloc[i]):
                        data.at[i, 'signal'] = -1
                        self.stock_quantity = int(self.cash // close_price)
                        self.cash += Decimal(self.stock_quantity) * close_price
                        self.position = -1  
                        self.log_trade('Sell', close_price, self.stock_quantity, self.cash, 'Opening')

                elif self.position == 1:  # Currently in a long position
                    if self.sell(data.iloc[i]):  # Closing long and opening short
                        data.at[i, 'signal'] = -1
                        self.cash += Decimal(self.stock_quantity) * close_price
                        self.log_trade('Sell', close_price, self.stock_quantity, self.cash, 'Closing')

                        # Open a new short position
                        self.stock_quantity = int(self.cash // close_price)
                        self.cash += Decimal(self.stock_quantity) * close_price
                        self.position = -1  
                        self.log_trade('Sell', close_price, self.stock_quantity, self.cash, 'Opening')

                elif self.position == -1:  # Currently in a short position
                    if self.buy(data.iloc[i]):  # Closing short and opening long
                        data.at[i, 'signal'] = 1
                        self.cash -= Decimal(self.stock_quantity) * close_price
                        self.log_trade('Buy', close_price, self.stock_quantity, self.cash, 'Closing')

                        self.stock_quantity = int(self.cash // close_price)
                        self.cash -= Decimal(self.stock_quantity) * close_price
                        self.position = 1  
                        self.log_trade('Buy', close_price, self.stock_quantity, self.cash, 'Opening')

            # Final position closing logic with error handling
            try:
                if self.position == 1:  
                    final_value = self.cash + Decimal(self.stock_quantity) * Decimal(data.iloc[-1]['close_price'])
                    self.log_trade('Sell', Decimal(data.iloc[-1]['close_price']), self.stock_quantity, self.cash, 'Closing')  
                elif self.position == -1:
                    final_value = self.cash - Decimal(self.stock_quantity) * Decimal(data.iloc[-1]['close_price'])
                    self.log_trade('Buy', Decimal(data.iloc[-1]['close_price']), self.stock_quantity, self.cash, 'Closing')  # Closing short
                else:  
                    final_value = self.cash  
            except Exception as e:
                print(f"Error in final position closing: {str(e)}")
                final_value = self.cash  # Return remaining cash if there's an issue

            return data, self.trades, final_value
        
        except ZeroDivisionError:
            print("Division by zero encountered in price calculation. Check data integrity.")
            return data, self.trades, self.cash
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return data, self.trades, self.cash
