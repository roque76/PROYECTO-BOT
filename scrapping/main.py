import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#Create headers to simulate a real request, parse the requested HTML
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
url = 'https://bitinfocharts.com/bitcoin/address/1Ay8vMC7R1UbyCCZRVULMV7iQpHSAbguJP'
r = requests.get(url, headers=headers)
print(r.status_code)
soup = BeautifulSoup(r.content, 'html.parser')
#Find the data needed
table = soup.find('table', id='table_maina')
rows = table.find_all('tr')
bids = {}
asks = {}

for row in rows:
    date = row.find('td', class_='utc hidden-phone')    
    if date:
        bid = row.find('span', class_='text-success')
        ask = row.find('span', class_='text-error')

        if bid:
            usd = re.sub(r"[($),]", '', bid.text.strip().split()[2])
            date = date.text.strip().split()[0]
            btc = re.sub(r"[+,]", '', bid.text.strip().split()[0])
            bids[float(usd),date] = float(btc)
        
        elif ask:
            usd = re.sub(r'[$(),]', '', ask.text.strip().split()[2])
            date = date.text.strip().split()[0]
            btc = re.sub(r'[-,]', '', ask.text.strip().split()[0])
            asks[float(usd),date] = float(btc)
            
            


print(f'Bids: {bids}')
print(f'Asks: {asks}')

