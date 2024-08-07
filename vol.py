import sys
import json
import signal
import time
import websocket
import numpy as np
from sty import fg, bg, ef, rs

# Need to fix trades happening exactly at the same time.

#closes = []
#vol_buy =[]
#vol_sell = []
vol_sell_init = 0
vol_buy_init = 0

def ws_open(ws):
    ws.send('{"event":"subscribe","pair":["XBT/USD"], "subscription": {"name":"trade"}}')

def ws_message(ws, message):
    global vol_sell_init, vol_buy_init
    api_data = json.loads(message)
    
    if len(api_data)==4:
        dat = api_data
        #print(dat)
        if(dat[1][0][3]=="b"):
            vol_buy = dat[1][0][1]
            vol_buy_init = vol_buy_init+float(vol_buy)
            buy_message = bg.da_green + vol_buy + bg.rs
            print(buy_message)
        else:
            vol_sell=dat[1][0][1]
            vol_sell_init = vol_sell_init+float(vol_sell)
            sell_message = bg.da_red + vol_sell + bg.rs
            print(sell_message)
        percent=vol_buy_init/(vol_buy_init+vol_sell_init)
        
        print(percent)

ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
ws.run_forever()
      
