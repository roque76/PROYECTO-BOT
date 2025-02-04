from BINANCE import market_depth as mk
ws = mk.WebSocket('https://bitinfocharts.com/bitcoin/address/1Ay8vMC7R1UbyCCZRVULMV7iQpHSAbguJP')
ws.start_client()
ws.get_whale_movements()
