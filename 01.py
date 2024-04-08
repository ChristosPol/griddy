# Import libraries
import requests
import pandas as pd
import mplfinance as mpl
import numpy as np
import time

# Args
pair = 'ADAUSD'
interval = '60'
funds = 1000
all_closed = False
n_hedge = 10
n_grid = 10
hedge_grid = np.cumsum([1]*n_hedge)*-1
size_quote = funds/(n_grid+n_hedge)
print(size_quote)

# Pull some data and fix pd (into a function?)
def pull_OHLC(pair, interval):
	call = requests.get('https://api.kraken.com/0/public/OHLC?pair='+pair+'&interval='+interval)
	resp = call.json()
	resp = resp['result'][pair]
	dt = pd.DataFrame(resp)
	dt.rename(columns = {0: 'Time', 1: 'Open', 2:'High', 3:'Low', 4:'Close', 
						 5:'Vwap', 6:'Volume', 7:'Count'}, inplace = True)
	dt['Time'] = pd.to_datetime(dt['Time'], unit = 's')
	dt = dt.set_index('Time')
	dt = dt.astype(float)
	return dt
dat=pull_OHLC(pair=pair, interval=interval)
print(dat)

# Start calculating grids
min_price = min(dt['Close'])
last_price = dt['Close'][-1]
frac = (((last_price-min_price)/last_price*100)/n_grid)
grid_net = np.cumsum((np.repeat(frac, n_grid)))*-1
grid_entries = (last_price + (grid_net/100*last_price)).tolist()
hedge_entries = (min_price + (hedge_grid/100*min_price)).tolist()
entries = grid_entries+hedge_entries

# Create trading table that will keep update status
dt_dic={'pair': pair,
		'entries': entries,
	    'type': ['grid']*len(grid_entries)+['hedge']*len(hedge_entries),
		'status_entry': 'NA',
	    'order_buy_id': 'NA',
	    'order_sell_id': 'NA',
		'size_vol': size_quote/np.asarray(entries),
		'current_price': 'NA'}
		
trading_table = pd.DataFrame(dt_dic)
#mpl.plot(dt,type = 'candle', hlines = dict(hlines = entries,
#										  linewidths = 0.4, colors = 'g'))


while all_closed==False:
	call_in = requests.get('https://api.kraken.com/0/public/OHLC?pair='+pair+'&interval='+interval)
	resp_in = call_in.json()
	resp_in = resp_in['result'][pair]
	dt_in = pd.DataFrame(resp_in)
	dt_in.rename(columns = {0: 'Time', 1: 'Open', 2:'High', 3:'Low', 4:'Close', 
						 5:'Vwap', 6:'Volume', 7:'Count'}, inplace = True)
	dt_in['Time'] = pd.to_datetime(dt_in['Time'], unit = 's')
	dt_in = dt_in.set_index('Time')
	dt_in = dt_in.astype(float)


	print(dt_in)
	time.sleep(1111)