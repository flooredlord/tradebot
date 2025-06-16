import os
import sys
import types

# Add the path to the module directory which has spaces in its name
MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deneysel trade bot v2'))
sys.path.insert(0, MODULE_PATH)

# Create a dummy binance module to satisfy imports in utils
binance_mod = types.ModuleType('binance')
binance_client_mod = types.ModuleType('binance.client')
binance_exceptions_mod = types.ModuleType('binance.exceptions')

class DummyBinanceClient:
    def __init__(self, *args, **kwargs):
        pass

binance_client_mod.Client = DummyBinanceClient
binance_mod.client = binance_client_mod
binance_exceptions_mod.BinanceAPIException = type('BinanceAPIException', (Exception,), {})
binance_mod.exceptions = binance_exceptions_mod

sys.modules['binance'] = binance_mod
sys.modules['binance.client'] = binance_client_mod
sys.modules['binance.exceptions'] = binance_exceptions_mod

import coin_utils
import config

class DummyClient:
    def __init__(self, exchange_info, tickers):
        self._exchange_info = exchange_info
        self._tickers = tickers

    def get_exchange_info(self):
        return self._exchange_info

    def get_ticker(self, symbol):
        return self._tickers[symbol]

def test_get_top_symbols_respects_top_n_and_excludes(monkeypatch):
    exchange_info = {
        'symbols': [
            {'symbol': 'BTCUSDT', 'status': 'TRADING', 'quoteAsset': 'USDT'},
            {'symbol': 'ETHUSDT', 'status': 'TRADING', 'quoteAsset': 'USDT'},
            {'symbol': 'BNBUSDT', 'status': 'TRADING', 'quoteAsset': 'USDT'},
            {'symbol': 'XRPUSDT', 'status': 'TRADING', 'quoteAsset': 'USDT'},
            {'symbol': 'DOGEUSDT', 'status': 'TRADING', 'quoteAsset': 'USDT'},
        ]
    }
    tickers = {
        'BTCUSDT': {'quoteVolume': '1000'},
        'ETHUSDT': {'quoteVolume': '800'},
        'BNBUSDT': {'quoteVolume': '500'},
        'XRPUSDT': {'quoteVolume': '300'},
        'DOGEUSDT': {'quoteVolume': '100'},
    }

    dummy = DummyClient(exchange_info, tickers)
    monkeypatch.setattr(coin_utils, 'client', dummy)

    # Ensure BNBUSDT is in excluded symbols
    monkeypatch.setattr(config, 'EXCLUDED_SYMBOLS', ['BNBUSDT'], raising=False)

    top_symbols = coin_utils.get_top_symbols(top_n=3)
    assert len(top_symbols) <= 3
    assert 'BNBUSDT' not in top_symbols

