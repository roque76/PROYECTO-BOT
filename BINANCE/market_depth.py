import json
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
import time

def on_open(ws):
    print("Conection started")

def on_message(ws, message):
     print(f"New data received: {message}")

def on_close(ws):
     print("Connection terminated")

def on_error(ws,error):
     print(f'Error: {error}')

ws = SpotWebsocketAPIClient(on_open=on_open,on_message=on_message,on_close=on_close,on_error=on_error)

while True:
     try:
          ws.order_book(symbol='btcusdt', limit=100)
          time.sleep(5)
     except KeyboardInterrupt:
          print("Exciting")
          break

ws.stop()