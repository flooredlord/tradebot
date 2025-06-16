import os
import sys
import json
import builtins
import types

import pytest

# Add project path with spaces
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deneysel trade bot v2')))

import utils


def test_adjust_quantity_to_lot_size(monkeypatch):
    def mock_info(symbol):
        return {'filters': [{'filterType': 'LOT_SIZE', 'stepSize': '0.1'}]}
    monkeypatch.setattr(utils, 'get_symbol_info', mock_info)
    assert utils.adjust_quantity_to_lot_size('AAA', 1.26) == 1.2


def test_adjust_notional_to_min(monkeypatch):
    def mock_info_no(symbol):
        return {'filters': []}
    monkeypatch.setattr(utils, 'get_symbol_info', mock_info_no)
    assert utils.adjust_notional_to_min('AAA', 5, 2) == 5

    def mock_info_with(symbol):
        return {'filters': [{'filterType': 'MIN_NOTIONAL', 'minNotional': '10'}]}
    monkeypatch.setattr(utils, 'get_symbol_info', mock_info_with)
    assert utils.adjust_notional_to_min('AAA', 4, 2) == 5.0
    assert utils.adjust_notional_to_min('AAA', 6, 2) == 6


def test_log_and_trade_history(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    utils.log('BUY order: AAA')
    with open('trade_log.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'BUY order: AAA' in content

    monkeypatch.setattr(utils, 'client', types.SimpleNamespace())
    # reuse mock get_symbol_info for trade history
    monkeypatch.setattr(utils, 'get_symbol_info', lambda s: {'filters': [{'filterType': 'LOT_SIZE', 'stepSize': '1'}]})
    # patch client.create_order to return minimal response
    utils.client.create_order = lambda **kwargs: {'fills':[{'price': '1'}], 'executedQty': kwargs['quantity']}
    utils.save_trade_history('AAA', 'BUY', 1.0, 2)
    with open('trade_history.json', 'r', encoding='utf-8') as f:
        hist = json.load(f)
    assert hist[-1]['symbol'] == 'AAA'
