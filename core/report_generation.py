import pandas as pd

def generate_report(data, initial_investment, final_value, trades):
    report = {}
    report['Initial Investment'] = float(initial_investment)   
    report['Final Portfolio Value'] = float(final_value)  
    report['Net Profit/Loss'] = float(final_value - initial_investment)  
    report['Total Trades'] = len(trades)

    trades_df = pd.DataFrame(trades)
    trades_df['Profit'] = None
    trades_df['Profit Percentage'] = None
    for i in range(1, len(trades_df), 2):
        entry = trades_df.iloc[i - 1]
        exit_trade = trades_df.iloc[i]
        
        if entry['Action'] == 'Buy':
            profit = (exit_trade['Price'] - entry['Price']) * entry['Quantity']
            profit_percentage = (profit / (entry['Price'] * entry['Quantity'])) * 100 if entry['Price'] != 0 else 0
        else:  # Short position
            profit = (entry['Price'] - exit_trade['Price']) * entry['Quantity']
            profit_percentage = (profit / (entry['Price'] * entry['Quantity'])) * 100 if entry['Price'] != 0 else 0
        
        trades_df.at[i - 1, 'Profit'] = profit
        trades_df.at[i - 1, 'Profit Percentage'] = profit_percentage

    profits = trades_df['Profit'].dropna()  
    report['Win Rate (%)'] = (sum(1 for p in profits if p > 0) / len(profits)) * 100 if len(profits) > 0 else 0
    report['Average Profit per Trade'] = profits.mean() if not profits.empty else 0

    # Calculate Maximum Drawdown
    cumulative_returns = data['close_price'].pct_change().cumsum()  # Cumulative returns over time
    max_drawdown = (cumulative_returns.cummax() - cumulative_returns).max()
    report['Maximum Drawdown (%)'] = max_drawdown * 100


    report['Total Returns (%)'] = ((final_value - initial_investment) / initial_investment) * 100


    with open('results/trade_report.txt', 'w') as f:
        f.write("==== Trade Report ====\n")
        for key, value in report.items():
            f.write(f"{key}: {value}\n")
        f.write("\n==== Trade Details ====\n")
        f.write(trades_df.fillna('-').to_string(index=False))  # Replace None with '-'

    print("Report generated as 'results/trade_report.txt'.")
    
    return report  
