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
#https://stackoverflow.com/questions/65656221/binance-websocket-realtime-plot-without-blocking-code
#https://konstantinmb.medium.com/websockets-101-practical-example-with-python-and-kraken-exchange-b2dce7323c11
closes = np.array([])
def ws_open(ws):
    ws.send('{"event":"subscribe","pair":["XBT/USD"], "subscription": {"name":"ohlc"}}')

def ws_message(ws, message):
    global closes
    api_data = json.loads(message)
    if len(api_data)==4:
      close= api_data[1][5]
      closes=np.append(closes, float(close))
      print(closes)
def wsthread(closes):
    ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
    ws.run_forever()


t = threading.Thread(target=wsthread, args=(closes,))
t.start()

fig, ax = plt.subplots()
plt.axis([0, 1000, 45000, 70000])
x= np.arange(1000)
y=[np.nan] * 1000
line, = ax.plot(x, y, linewidth = 2, color = "green")



def animate(i):
    global y
    # shift left to most recent 100 closing prices
    y[:len(closes)] = closes[-1000:]
    line.set_ydata(y)
    return line,

def init():
    line.set_ydata([np.nan] * 1000)
    return line,

anim = FuncAnimation(
    fig, animate, interval=20,
    init_func=init,
    blit=True
)

plt.show()
