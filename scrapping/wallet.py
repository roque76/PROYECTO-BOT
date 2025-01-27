import requests
from bs4 import BeautifulSoup
import re
import time



class WalletScrapping():
    def __init__(self, url):
        self.url = url
    
    def scrappe(self):
        self.bids = {}
        self.asks = {}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

        try:
            start = time.time()
            r = requests.get(url = self.url, headers=headers)
            print(r.status_code)
            print(f"Request time: {time.time() - start:.2f} seconds")
        except TimeoutError:
            print('Timed out.')
        
        soup = BeautifulSoup(r.content,'html.parser')
        table = soup.find('table', id='table_maina')
        rows = table.find_all('tr')

        for row in rows:
            date = row.find('td', class_='utc hidden-phone')    
            if date:
                bid = row.find('span', class_='text-success')
                ask = row.find('span', class_='text-error')
                if bid:
                    usd = re.sub(r"[($),]", '', bid.text.strip().split()[2])
                    date = date.text.strip().split()[0]
                    btc = re.sub(r"[+,]", '', bid.text.strip().split()[0])
                    self.bids[float(usd),date] = float(btc)
        
                elif ask:
                    usd = re.sub(r'[$(),]', '', ask.text.strip().split()[2])
                    date = date.text.strip().split()[0]
                    btc= re.sub(r'[-,]', '', ask.text.strip().split()[0])
                    self.asks[float(usd),date] = float(btc)
        
        