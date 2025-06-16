import config
from utils import client


def get_top_symbols(base_currency='USDT', top_n=50):
    exchange_info = client.get_exchange_info()
    symbols = [
        s['symbol'] for s in exchange_info['symbols']
        if s['status'] == 'TRADING' and s['quoteAsset'] == base_currency
    ]

    volume_list = []
    for symbol in symbols:
        try:
            ticker = client.get_ticker(symbol=symbol)
            volume = float(ticker['quoteVolume'])
            volume_list.append((symbol, volume))
        except:
            continue

    sorted_symbols = sorted(volume_list, key=lambda x: x[1], reverse=True)
    top_symbols = [s[0] for s in sorted_symbols[:top_n]]
    filtered = [s for s in top_symbols if s not in config.EXCLUDED_SYMBOLS]
    return filtered