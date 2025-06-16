import os
import sys
import types

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deneysel trade bot v2')))

import coin_utils
import config


def test_get_top_symbols(monkeypatch):
    fake_exchange = {
        'symbols': [
            {'symbol': 'AAAUSDT', 'status': 'TRADING', 'quoteAsset': 'USDT'},
            {'symbol': 'BBBUSDT', 'status': 'BREAK', 'quoteAsset': 'USDT'},
            {'symbol': 'CCCBTC', 'status': 'TRADING', 'quoteAsset': 'BTC'},
            {'symbol': 'EXCUSDT', 'status': 'TRADING', 'quoteAsset': 'USDT'},
        ]
    }

    def mock_get_exchange_info():
        return fake_exchange

    def mock_get_ticker(symbol):
        if symbol == 'AAAUSDT':
            return {'quoteVolume': '1000'}
        if symbol == 'EXCUSDT':
            return {'quoteVolume': '2000'}
        raise Exception('unexpected symbol')

    monkeypatch.setattr(coin_utils.client, 'get_exchange_info', mock_get_exchange_info)
    monkeypatch.setattr(coin_utils.client, 'get_ticker', mock_get_ticker)
    monkeypatch.setattr(config, 'EXCLUDED_SYMBOLS', ['EXCUSDT'])

    result = coin_utils.get_top_symbols(base_currency='USDT', top_n=10)
    assert result == ['AAAUSDT']
