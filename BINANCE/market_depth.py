import json
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
import time
from decimal import Decimal

class WebSocket():
     def __init__(self):
          self.avg_price = 0
          self.bids = {}
          self.asks = {}
          self.ws_order_book = SpotWebsocketAPIClient(on_open=self.on_open,on_close=self.on_close,
                                                       on_error=self.on_error, on_message=self.order_book)
          self.ws_average_price = SpotWebsocketAPIClient(on_open=self.on_open, on_close=self.on_close
                                                         , on_error=self.on_error,on_message=self.average_price)
     def on_open(self,ws):
          print("Connection started")

     def on_close(self, ws): 
          print("Connection terminated")

     def on_error(self, ws,error):
          print(f'Error: {error}')

     def order_book(self, ws, message):
          message = json.loads(message)
          bids = message["result"]["bids"]
          asks = message["result"]["asks"]

          for price, quantity in bids:
               self.bids[float(price)] = float(quantity)
          for price, quantity in asks:
               self.asks[float  (price)] = float(quantity)
     
     def average_price(self, ws, message):
          message =  json.loads(message)
          print(message["result"]["price"])
          self.avg_price = message["result"]["price"]

     


     def start_client(self):
          while True:     
               try:
                    self.ws_order_book.order_book(symbol='btcusdt', limit= 5)
                    self.ws_average_price.avg_price(symbol='btcusdt')
                    time.sleep(5)
               except KeyboardInterrupt:
                    self.ws_average_price.stop()
                    self.ws_order_book.stop()
                    print("Exciting")
                    break

ws_client = WebSocket()
ws_client.start_client()