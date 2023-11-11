from fyers_apiv3 import fyersModel
import pandas as pd
import datetime as dt
from fyers_apiv3.FyersWebsocket import data_ws
from datetime import datetime
import yfinance as yf
import pytz
from datetime import datetime
from datetime import datetime, timedelta


def datestring_to_epoch(date_string):
    """
    Convert a date string in "YYYY-MM-DD" format to epoch time (Unix timestamp).

    Parameters:
    - date_string: A date string in "YYYY-MM-DD" format

    Returns:
    - Epoch time as an integer
    """
    dt = datetime.strptime(date_string, "%Y-%m-%d")
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds())

def epoch_to_datetime(epoch_time):
    """
    Convert epoch time (Unix timestamp) to a datetime object in Indian timezone.

    Parameters:
    - epoch_time: Epoch time as an integer

    Returns:
    - datetime object in Indian timezone (without timezone info in string representation)
    """
    utc_datetime = datetime.utcfromtimestamp(epoch_time)
    utc_timezone = pytz.timezone('UTC')
    indian_timezone = pytz.timezone('Asia/Kolkata')

    utc_datetime = utc_timezone.localize(utc_datetime)
    indian_datetime = utc_datetime.astimezone(indian_timezone)

    return indian_datetime.replace(tzinfo=None)

def slice_dates_into_chunks(start_date, end_date):
    """
    Slice two dates into 3-month chunks.

    Parameters:
    - start_date: Start date as a string in "YYYY-MM-DD" format
    - end_date: End date as a string in "YYYY-MM-DD" format

    Returns:
    - List of lists, where each sublist represents a 3-month chunk [start_date, end_date]
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    chunks = []
    current_chunk_start = start_date

    while current_chunk_start < end_date:
        current_chunk_end = current_chunk_start + timedelta(days=90)
        
        # Check for the edge case where the chunk end date exceeds the end date
        if current_chunk_end > end_date:
            current_chunk_end = end_date

        chunks.append([current_chunk_start.strftime("%Y-%m-%d"), current_chunk_end.strftime("%Y-%m-%d")])

        current_chunk_start = current_chunk_end + timedelta(days=1)

    return chunks

def BuildDataFrame(d1, d2, stock, resolution):
    """
    Build a DataFrame using historical data from the FYERS API.

    Parameters:
    - d1: Start date as a string in "YYYY-MM-DD" format
    - d2: End date as a string in "YYYY-MM-DD" format
    - stock: Stock symbol
    - resolution: Resolution for the data (e.g., '5' for 5-minute intervals)

    Returns:
    - Pandas DataFrame containing historical stock data
    """
    Resultantdict = {}
    FinalDf = pd.DataFrame()

    # Slice the dates into three-month chunks
    date_list = slice_dates_into_chunks(d1, d2)
    date_list = [[datestring_to_epoch(date_string) for date_string in sublist] for sublist in date_list]

    # The FYERS API part
    for i in range(len(date_list)):
        data = {
            "symbol": stock,
            "resolution": resolution,
            "date_format": "0",
            "range_from": date_list[i][0],
            "range_to": date_list[i][1],
            "cont_flag": "1"
        }
        response = fyers.history(data)

        if response['code'] == 200 and response['s'] == 'ok':
            current_df = pd.DataFrame(response['candles'])
            current_df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
            FinalDf = pd.concat([FinalDf, current_df])

    FinalDf['Datetime'] = FinalDf['Datetime'].apply(epoch_to_datetime)
    FinalDf.set_index('Datetime', inplace=True)
    return FinalDf
