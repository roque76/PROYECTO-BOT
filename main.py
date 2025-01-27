from BINANCE import market_depth as mk
from scrapping import wallet as w

ws = mk.WebSocket()
ws.start_client()
wallet = w.WalletScrapping('https://bitinfocharts.com/bitcoin/address/1Ay8vMC7R1UbyCCZRVULMV7iQpHSAbguJP')
wallet.scrappe()
print(f'Asks Mr100: {wallet.asks}')
print(f'Bids Mr100: {wallet.bids}')
