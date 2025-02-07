import json
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
import time
from scrapping import wallet 

class WebSocket():
     def __init__(self, url):
          self.ws_order_book = SpotWebsocketAPIClient(on_open=self.on_open,on_close=self.on_close,
                                                       on_error=self.on_error, on_message=self.order_book)
          self.ws_average_price = SpotWebsocketAPIClient(on_open=self.on_open, on_close=self.on_close
                                                         , on_error=self.on_error,on_message=self.average_price)
          self.whale_asks ={}
          self.whale_bids ={}
          self.wallet = wallet.WalletScrapping(url)

     def on_open(self,ws):
          print("Connection started")

     def on_close(self, ws): 
          print("Connection terminated")

     def on_error(self, ws,error):
          print(f'Error: {error}')

     def order_book(self, ws, message):
          self.bids = {}
          self.asks = {}
          message = json.loads(message)
          bids = message["result"]["bids"]
          asks = message["result"]["asks"]

          for price, quantity in bids:
               self.bids[float(price)] = float(quantity)
          for price, quantity in asks:
               self.asks[float(price)] = float(quantity)

     def average_price(self, ws, message):
          message =  json.loads(message)
          self.avg_price = float(message["result"]["price"])
          

     def market_depth(self, percentage=1):
          percentage = (self.avg_price*percentage)/100
          lowerLimit = self.avg_price-percentage
          upperLimit = self.avg_price+percentage
          
          self.bid_depth = 0
          self.ask_depth = 0
          for price in self.bids:
               if lowerLimit <= price and upperLimit >= price:
                    self.bid_depth+=self.bids[price]

          for price in self.asks:
               if lowerLimit <= price and upperLimit >= price:
                    self.ask_depth+= self.asks[price]

          print(f'Average price {self.avg_price}')
          print(f'Bid depth {self.bid_depth}')     
          print(f'Ask depth {self.ask_depth}')     
     
     def ping_movement(self):
          data, output = self.wallet.scrappe()
          print(data, output)
          if self.is_whale_movement(data, output):
               print("error")
          else:
               print("movement pinged")

     def is_whale_movement(self, volume, type):
          depth = self.bid_depth if type else self.ask_depth
          
          return (volume*100)/ depth > 65

     def start_client(self):
          while True:     
               try:
                    self.ws_order_book.order_book(symbol='btcusdt', limit= 100)
                    self.ws_average_price.avg_price(symbol='btcusdt')
                    time.sleep(5)
                    self.market_depth()
                    self.ping_movement()
               except KeyboardInterrupt:
                    self.ws_average_price.stop()
                    self.ws_order_book.stop()
                    print("Exciting")
                    break

