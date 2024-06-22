import pandas as pd
import numpy as np

# Read the market cap data
df = pd.read_csv('market_cap_data.csv', parse_dates=['Date'])

# List of tickers (with BBVA changed to BBAR)
tickers = ['BMA', 'YPF', 'LOMA', 'CEPU', 'TS', 'CRESY', 'GGAL', 'PAM', 'CAAP', 'BIOX', 'VIST', 'TEO', 'AGRO', 'SUPV', 'EDN', 'TGS', 'BBAR']

# Create a list to store the results
results = []

for ticker in tickers:
    price_col = f'{ticker}_shr_px'
    mkt_cap_col = f'{ticker}_mkt_cap'
    
    # Find the all-time high market cap and its date
    ath_mkt_cap = df[mkt_cap_col].max()
    ath_date = df.loc[df[mkt_cap_col] == ath_mkt_cap, 'Date'].iloc[0]
    ath_price = df.loc[df[mkt_cap_col] == ath_mkt_cap, price_col].iloc[0]
    
    # Find the most recent (last) market cap and price
    last_mkt_cap = df[mkt_cap_col].iloc[0]
    last_price = df[price_col].iloc[0]
    
    # Calculate percentage changes
    price_pct_change = ((last_price - ath_price) / ath_price) * 100
    mkt_cap_pct_change = ((last_mkt_cap - ath_mkt_cap) / ath_mkt_cap) * 100
    
    results.append([
        ticker,
        round(ath_price, 1),
        round(last_price, 1),
        round(price_pct_change, 1),
        round(ath_mkt_cap),
        round(last_mkt_cap),
        round(mkt_cap_pct_change, 1),
        ath_date.strftime('%b-%y')
    ])

# Create a DataFrame from the results
result_df = pd.DataFrame(results, columns=['Tickers', 'shr px ATH', 'shr px last', 'shr px % chg', 'mkt cap ATH USDm', 'last mkt cap USDm', 'mkt cap % chg', 'mkt cap date ATH'])

# Sort the DataFrame by market cap percentage change
result_df = result_df.sort_values('mkt cap % chg', ascending=False)

# Calculate the median percentage change for market cap
median_pct_change = np.median(result_df['mkt cap % chg'])

# Add the median row
median_row = pd.DataFrame({
    'Tickers': ['Median'],
    'shr px ATH': [''],
    'shr px last': [''],
    'shr px % chg': [''],
    'mkt cap ATH USDm': [''],
    'last mkt cap USDm': [''],
    'mkt cap % chg': [round(median_pct_change, 1)],
    'mkt cap date ATH': ['']
})

result_df = pd.concat([result_df, median_row]).reset_index(drop=True)

# Save the results to a CSV file
result_df.to_csv('market_cap_comparison.csv', index=False)

print("CSV file has been saved as 'market_cap_comparison.csv'")
print(result_df.to_string(index=False))