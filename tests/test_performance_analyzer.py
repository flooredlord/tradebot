import os
import sys
import json

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deneysel trade bot v2')))

import performance_analyzer


def test_analyze_performance(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    history = [
        {'symbol': 'AAA', 'type': 'BUY', 'price': 10, 'quantity': 1, 'timestamp': 't1'},
        {'symbol': 'AAA', 'type': 'SELL', 'price': 12, 'quantity': 1, 'timestamp': 't2'},
        {'symbol': 'BBB', 'type': 'BUY', 'price': 10, 'quantity': 1, 'timestamp': 't3'},
        {'symbol': 'BBB', 'type': 'SELL', 'price': 8, 'quantity': 1, 'timestamp': 't4'},
    ]
    with open('trade_history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f)
    performance_analyzer.analyze_performance()
    out = capsys.readouterr().out
    assert 'Total PnL: 0.00 USDT' in out
    assert 'Success Rate: 50.00% (1/2)' in out
    with open('performance_report.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    assert 'AAA: PnL=2.00' in text


def test_analyze_performance_no_file(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    performance_analyzer.analyze_performance()
    out = capsys.readouterr().out
    assert 'No trade history found' in out
