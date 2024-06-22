import pandas as pd
import numpy as np
from tabulate import tabulate

# Read the market cap data
df = pd.read_csv('market_cap_data.csv', parse_dates=['Date'])

# List of tickers
tickers = ['BMA', 'YPF', 'LOMA', 'CEPU', 'TS', 'CRESY', 'GGAL', 'PAM', 'CAAP', 'BIOX', 'VIST', 'TEO', 'AGRO', 'SUPV', 'EDN', 'TGS', 'BBAR']

# Create a list to store the results
results = []

for ticker in tickers:
    mkt_cap_col = f'{ticker}_mkt_cap'
    
    # Find the all-time high market cap and its date
    ath_mkt_cap = df[mkt_cap_col].max()
    ath_date = df.loc[df[mkt_cap_col] == ath_mkt_cap, 'Date'].iloc[0]
    
    # Find the most recent (last) market cap
    last_mkt_cap = df[mkt_cap_col].iloc[0]
    
    # Calculate percentage change
    pct_change = ((last_mkt_cap - ath_mkt_cap) / ath_mkt_cap) * 100
    
    results.append([
        ticker,
        round(ath_mkt_cap),
        round(last_mkt_cap),
        f"{pct_change:.0f}%",
        ath_date.strftime('%b-%y')
    ])

# Create a DataFrame from the results
result_df = pd.DataFrame(results, columns=['Tickers', 'mkt cap ATH USDm', 'last mkt cap USDm', '% chg', 'Date ATH'])

# Sort the DataFrame by percentage change
result_df['pct_change_numeric'] = result_df['% chg'].str.rstrip('%').astype(float)
result_df = result_df.sort_values('pct_change_numeric', ascending=False)
result_df = result_df.drop('pct_change_numeric', axis=1)

# Calculate the median percentage change
median_pct_change = np.median([float(x.strip('%')) for x in result_df['% chg']])

# Add the median row
median_row = pd.DataFrame({
    'Tickers': ['Median'],
    'mkt cap ATH USDm': [''],
    'last mkt cap USDm': [''],
    '% chg': [f"{median_pct_change:.0f}%"],
    'Date ATH': ['']
})

result_df = pd.concat([result_df, median_row])

# Format the table
table = tabulate(result_df, headers='keys', tablefmt='pipe', showindex=False)

print(table)

# Optionally, save to a file
with open('market_cap_comparison.txt', 'w') as f:
    f.write(table)

print("\nTable has been saved to 'market_cap_comparison.txt'")