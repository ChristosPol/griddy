import sys
import json
import signal
import time
import _thread
import websocket
import numpy as np
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def ws_open(ws):
    #ws.send('{"event":"subscribe","pair":["XBT/USD"], "subscription": {"name":"ohlc"}}')
	ws.send('{"event":"subscribe","pair":["XBT/USD"], "subscription": {"name":"book", "depth":100}}')

def ws_message(ws, message):
    api_data = json.loads(message)
    print(api_data)

ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
ws.run_forever()
