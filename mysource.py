import requests
import pandas as pd

def pull_OHLC(pair, interval):
	call = requests.get('https://api.kraken.com/0/public/OHLC?pair='+pair+'&interval='+interval)
	resp = call.json()
	resp = resp['result'][pair]
	dt = pd.DataFrame(resp)
	dt.rename(columns = {0: 'Time',
		1: 'Open',
		 2:'High',
		  3:'Low',
		   4:'Close',
		    5:'Vwap',
		     6:'Volume',
		      7:'Count'
		      }, inplace = True)
	dt['Time'] = pd.to_datetime(dt['Time'], unit = 's')
	dt = dt.set_index('Time')
	dt = dt.astype(float)
	return dt
