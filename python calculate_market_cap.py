import pandas as pd
import numpy as np

# Read the weekly prices CSV
df_prices = pd.read_csv('weekly_pxs.csv', parse_dates=['Date'])

# Read the quarterly shares outstanding CSV
df_shares = pd.read_csv('shrs.csv', parse_dates=['date'])

# Ensure both dataframes are sorted by date
df_prices = df_prices.sort_values('Date')
df_shares = df_shares.sort_values('date')

# List of tickers
tickers = ['PAM', 'SUPV', 'TEO', 'EDN', 'BBAR', 'LOMA', 'YPF', 'BMA', 'TS', 'CEPU', 'TGS', 'AGRO', 'CAAP', 'GGAL', 'CRESY', 'BIOX', 'VIST']

# Create an empty DataFrame to store results
df_results = pd.DataFrame()

# Process each ticker
for ticker in tickers:
    print(f"Processing {ticker}...")
    
    # Extract price data for this ticker
    price_data = df_prices[['Date', ticker]].rename(columns={ticker: f'{ticker}_shr_px'})
    
    # Extract shares outstanding data for this ticker
    shares_data = df_shares[['date', f'{ticker}_shr_outs (m)']].rename(columns={'date': 'Date', f'{ticker}_shr_outs (m)': f'{ticker}_shrs'})
    
    # Merge price data with shares data
    merged_data = pd.merge_asof(price_data, shares_data, on='Date', direction='backward')
    
    # Forward fill NaN values in shares column
    merged_data[f'{ticker}_shrs'] = merged_data[f'{ticker}_shrs'].ffill()
    
    # Calculate market cap in millions
    merged_data[f'{ticker}_mkt_cap'] = merged_data[f'{ticker}_shr_px'] * merged_data[f'{ticker}_shrs']
    
    # Add to results
    if df_results.empty:
        df_results = merged_data
    else:
        df_results = pd.merge(df_results, merged_data, on='Date', how='outer')

# Sort by date in descending order
df_results = df_results.sort_values('Date', ascending=False)

# Reorder columns
column_order = ['Date']
for ticker in tickers:
    column_order.extend([f'{ticker}_shr_px', f'{ticker}_shrs', f'{ticker}_mkt_cap'])

df_results = df_results[column_order]

# Save the results to a CSV file
df_results.to_csv('market_cap_data.csv', index=False, date_format='%d/%m/%Y')

print("Processing complete. Results saved to 'market_cap_data.csv'.")
print(df_results.head())
print(df_results.columns.tolist())
print(f"Data range: {df_results['Date'].max().strftime('%d/%m/%Y')} to {df_results['Date'].min().strftime('%d/%m/%Y')}")
print(f"Total number of rows: {len(df_results)}")

# Print the number of non-null values for each column
print("\nNumber of non-null values for each column:")
print(df_results.count())

# Print the first few rows for PAM as an example
print("\nFirst few rows for PAM:")
print(df_results[['Date', 'PAM_shr_px', 'PAM_shrs', 'PAM_mkt_cap']].head().to_string(index=False))