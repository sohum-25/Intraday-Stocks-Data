# Intraday Stocks Data 2017 onwards

This code allows you to retrieve data for specific tickers. You can read the pickle file to obtain data for different timeframes such as 1, 2, 5, 10, and 15 minutes for both individual stocks and NIFTY/BANKNIFTY data. The code is flexible and can be extended to fetch data for any symbols of your choice.

The data can be stored in a pickle file, which is a dictionary containing keys in the format (timeframe, Stock).

```python

# Example: Get data for a specific stock and timeframe
import pandas as pd
import pickle

# Example usage:
pickle_file_path = 'MasterDictionary.pkl'

# Read the pickle file to get the data
with open(pickle_file_path, 'rb') as file:
    intraday_data = pickle.load(file)

stock_symbol = 'SBIN'
selected_timeframe = 5  # Replace with the desired timeframe

try:
    data_for_stock = intraday_data[(selected_timeframe, stock_symbol)]
    print(f"Intraday data for {stock_symbol} with {selected_timeframe}-minute timeframe:")
    print(data_for_stock.head())
except KeyError:
    print(f"No data found for {stock_symbol} with {selected_timeframe}-minute timeframe.")
