from fyers_apiv3 import fyersModel
import pandas as pd
import datetime as dt
from fyers_apiv3.FyersWebsocket import data_ws
from datetime import datetime
import yfinance as yf
import pytz
from datetime import datetime
import webbrowser
import pyautogui
import time
from urllib.parse import urlparse,parse_qs
import pyperclip
from Functions import  datestring_to_epoch,epoch_to_datetime,slice_dates_into_chunks,BuildDataFrame

client_id='' #Fill your client_id
secret_id='' #Fill your secret_id
url='' #Fill your url
response_type="code"
grant_type="authorization_code"
session=fyersModel.SessionModel(client_id=client_id,
                               secret_key=secret_id,
                               redirect_uri=url,
                               response_type=response_type,
                               grant_type=grant_type)
response=session.generate_authcode()
print(response)
link_to_open = response

webbrowser.open(link_to_open)

time.sleep(5)  
pyautogui.hotkey('ctrl', 'l')  
pyautogui.hotkey('ctrl', 'c')
parsed_url = urlparse(pyperclip.paste())
query_params = parse_qs(parsed_url.query)

auth_code = query_params.get('auth_code', [None])[0]
session.set_token(auth_code)
response=session.generate_token()
print(response)
df=pd.DataFrame()
df=response
tk=df['access_token']
fyers=fyersModel.FyersModel(client_id=client_id,is_async=False,token=tk,log_path="")


Stocks=pd.read_csv('ind_nifty200list.csv')
Stocks['Symbol']= str('NSE:')+Stocks['Symbol']+str('-EQ')
Securities=(Stocks['Symbol']).to_list()
Securities.append('NSE:NIFTY50-INDEX')
Securities.append('NSE:NIFTYBANK-INDEX')
Securities


MasterDictionary = {}
d1 = '2017-01-01'  # Corrected month format
d2 = '2023-12-01'  # Corrected month format
times = [1, 2, 5, 15]

for t in times:
    MasterDictionary[t] = {}  
    for i in range(len(Securities)):
        key = Securities[i].replace('-EQ', '').replace('NSE:', '')
        MasterDictionary[t][key] = BuildDataFrame(d1, d2, Securities[i], t)
        print(f"Appended {Securities[i]} for {t} minute timeframe")

# Clear output message
print("Data collection and appending to MasterDictionary completed.")
