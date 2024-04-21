# Import libraries
import requests
import pandas as pd
import mplfinance as mpl
import numpy as np
import time
from mysource import pull_OHLC

#Possibly derive a metric for volatility on 1 minute to choose pair

# Args
pair = 'ADAUSD'
interval = '60'
funds = 1000
all_closed = False
n_hedge = 10
n_grid = 10
hedge_grid = np.cumsum([1]*n_hedge)*-1
size_quote = funds/(n_grid+n_hedge)

# Pull some data and fix pd 
dt = pull_OHLC(pair = pair, interval = interval)

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
	'size_usd': 50,
	'size_vol': size_quote/np.asarray(entries),
	'current_price': 'NA'
	}
		
trading_table = pd.DataFrame(dt_dic)

#mpl.plot(dt, type = 'candle', hlines = dict(hlines = entries, linewidths = 0.4, colors = 'g'))

while all_closed==False:
	last_price=pull_OHLC(pair = pair, interval = '1')['Close'][-1]
	trading_table.loc[last_price <= trading_table['entries'], 'status_entry'] = "Entered"
	sum_vol_entered = sum(trading_table.loc[trading_table['status_entry']=="Entered", 'size_vol'])
	sum_usd_entered = sum(trading_table.loc[trading_table['status_entry']=="Entered", 'size_usd'])
	sum_usd_current = sum_vol_entered*last_price
	current_eval_percent = ((sum_usd_current-sum_usd_entered)/sum_usd_entered)*100
	trading_table.loc[0, 'current_price'] = last_price
	print(trading_table)
	print(current_eval_percent)

	time.sleep(5)