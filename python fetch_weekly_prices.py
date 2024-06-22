import pandas as pd
import yfinance as yf
from datetime import datetime

# List of tickers
tickers = ['PAM', 'SUPV', 'TEO', 'EDN', 'BBAR', 'LOMA', 'YPF', 'BMA', 'TS', 'CEPU', 'TGS', 'AGRO', 'CAAP', 'GGAL', 'CRESY', 'BIOX', 'VIST']

# Set the start date
start_date = datetime(2003, 12, 31)
end_date = datetime.now()

# Create a dictionary to store DataFrames for each ticker
data_frames = {}

# Fetch data for each ticker
for ticker in tickers:
    print(f"Processing {ticker}...")
    
    # Fetch weekly historical data
    stock_data = yf.Ticker(ticker).history(start=start_date, end=end_date, interval="1wk")
    
    # Convert index to timezone-naive
    stock_data.index = stock_data.index.tz_localize(None)
    
    # Keep only the 'Close' prices
    data_frames[ticker] = stock_data[['Close']].rename(columns={'Close': ticker})

# Combine all DataFrames
df_results = pd.concat(data_frames.values(), axis=1)

# Reset index to make Date a column
df_results = df_results.reset_index().rename(columns={'index': 'Date'})

# Sort by date in descending order
df_results = df_results.sort_values('Date', ascending=False)

# Save the results to a CSV file
df_results.to_csv('weekly_pxs.csv', index=False)

print("Processing complete. Results saved to 'weekly_pxs.csv'.")
print(df_results.head())
print(df_results.columns.tolist())
print(f"Data range: {df_results['Date'].max()} to {df_results['Date'].min()}")
print(f"Total number of rows: {len(df_results)}")

# Print the number of non-null values for each ticker
print("\nNumber of non-null values for each ticker:")
print(df_results.count())