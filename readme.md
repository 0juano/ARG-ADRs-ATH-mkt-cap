# Argentine ADR Market Cap Calculator

This project calculates and analyzes market capitalization data for Argentine American Depositary Receipts (ADRs). It includes scripts to fetch weekly share prices, calculate market capitalization, and generate comparison reports.

## Components

1. `fetch_weekly_prices.py`: Fetches weekly closing prices for specified tickers.
2. `calculate_market_cap.py`: Calculates market capitalization using share prices and outstanding shares data.
3. `generate_market_cap_csv.py`: Generates a CSV report comparing current market caps to all-time highs.
4. `shrs.csv`: Input file containing quarterly shares outstanding data.

## Requirements

- Python 3.x
- pandas
- yfinance
- numpy

Install required packages using:
pip install pandas yfinance numpy


## Usage

1. Fetch weekly prices: python fetch_weekly_prices.py
This generates `weekly_pxs.csv` with weekly closing prices.

2. Calculate market capitalization: python calculate_market_cap.py
This generates `market_cap_data.csv` with calculated market caps.

3. Generate market cap comparison report: python generate_market_cap_csv.py
This creates `market_cap_comparison.csv` with a comparison of current vs. all-time high market caps.

## Input Data

- `shrs.csv`: Contains quarterly shares outstanding data for each ticker.

## Output Files

- `weekly_pxs.csv`: Weekly closing prices for each ticker.
- `market_cap_data.csv`: Calculated market capitalization data.
- `market_cap_comparison.csv`: Comparison report of current vs. all-time high market caps.

## Tickers Analyzed

PAM, SUPV, TEO, EDN, BBAR, LOMA, YPF, BMA, TS, CEPU, TGS, AGRO, CAAP, GGAL, CRESY, BIOX, VIST

## Notes

- The scripts use data from December 31, 2003, onwards.
- Ensure `shrs.csv` is up-to-date with the latest quarterly shares outstanding data.
- Market cap values are calculated in millions of USD.

## License

[Specify your license here]