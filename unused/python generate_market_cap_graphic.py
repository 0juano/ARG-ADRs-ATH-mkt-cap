import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

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
        f"{price_pct_change:.0f}%",
        round(ath_mkt_cap),
        round(last_mkt_cap),
        f"{mkt_cap_pct_change:.0f}%",
        ath_date.strftime('%b-%y')
    ])

# Create a DataFrame from the results
result_df = pd.DataFrame(results, columns=['Tickers', 'shr px ATH', 'shr px last', 'shr px % chg', 'mkt cap ATH USDm', 'last mkt cap USDm', 'mkt cap % chg', 'mkt cap date ATH'])

# Sort the DataFrame by market cap percentage change
result_df['mkt_cap_pct_change_numeric'] = result_df['mkt cap % chg'].str.rstrip('%').astype(float)
result_df = result_df.sort_values('mkt_cap_pct_change_numeric', ascending=False)

# Calculate the median percentage change for market cap
median_pct_change = np.median(result_df['mkt_cap_pct_change_numeric'])

# Add the median row
median_row = pd.DataFrame({
    'Tickers': ['Median'],
    'shr px ATH': [''],
    'shr px last': [''],
    'shr px % chg': [''],
    'mkt cap ATH USDm': [''],
    'last mkt cap USDm': [''],
    'mkt cap % chg': [f"{median_pct_change:.0f}%"],
    'mkt cap date ATH': [''],
    'mkt_cap_pct_change_numeric': [median_pct_change]
})

result_df = pd.concat([result_df, median_row]).reset_index(drop=True)

# Create the plot
fig, ax = plt.subplots(figsize=(16, 10))
ax.axis('tight')
ax.axis('off')

# Define colors for percentage change
def color_scale(val):
    if val == '':
        return 'white'
    val = float(val.strip('%'))
    if val > 50:
        return '#90EE90'  # light green
    elif val > 25:
        return '#98FB98'  # pale green
    elif val > 0:
        return '#E0FFE0'  # very light green
    elif val > -25:
        return '#FFFFE0'  # light yellow
    elif val > -50:
        return '#FFB6C1'  # light pink
    else:
        return '#FF6961'  # light red

# Create the table
table = ax.table(cellText=result_df.values[:, :-1], colLabels=result_df.columns[:-1], loc='center', cellLoc='center')

# Set font size and style
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.2, 1.5)

# Apply colors to percentage change columns
for i in range(len(result_df)):
    table[(i+1, 3)].set_facecolor(color_scale(result_df.iloc[i]['shr px % chg']))
    table[(i+1, 6)].set_facecolor(color_scale(result_df.iloc[i]['mkt cap % chg']))

# Set header style
for i in range(len(result_df.columns) - 1):
    table[(0, i)].set_facecolor('#4682B4')  # Steel Blue
    table[(0, i)].set_text_props(color='white', fontweight='bold')

# Adjust layout and save
plt.tight_layout()
plt.savefig('market_cap_comparison_extended.png', dpi=300, bbox_inches='tight')
print("Graphic has been saved as 'market_cap_comparison_extended.png'")