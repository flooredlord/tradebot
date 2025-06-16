import types
import sys
from pathlib import Path
import pandas as pd
import importlib

# Ensure project directory is in sys.path (handled in conftest)
PROJECT_DIR = Path(__file__).resolve().parents[1] / 'deneysel trade bot v2'

# Helper function to import module by name from project directory

def load_module(name):
    spec = importlib.util.spec_from_file_location(name, PROJECT_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

utils = load_module('utils')
strategies = load_module('strategies')
risk_management = load_module('risk_management')
import config  # config can be imported normally via PROJECT_DIR in sys.path


def test_adjust_quantity_to_lot_size(monkeypatch):
    info = {
        'filters': [
            {'filterType': 'LOT_SIZE', 'stepSize': '0.01'}
        ]
    }
    monkeypatch.setattr(utils, 'get_symbol_info', lambda symbol: info)
    result = utils.adjust_quantity_to_lot_size('TESTUSDT', 1.2345)
    assert result == 1.23


def test_calculate_atr_stop_loss_take_profit(monkeypatch):
    df = pd.DataFrame({
        'high': [101, 102],
        'low': [99, 98],
        'close': [100, 100]
    })
    monkeypatch.setattr(risk_management, 'fetch_klines', lambda symbol: df)

    def fake_atr(high, low, close, window=14):
        return pd.Series([1.0] * len(close))

    monkeypatch.setattr(risk_management.ta.volatility, 'average_true_range', fake_atr)
    sl, tp = risk_management.calculate_atr_stop_loss_take_profit('TEST', atr_multiplier=1.5)
    assert sl == 98.5
    assert tp == 101.5


def test_generate_signal(monkeypatch):
    df = pd.DataFrame({
        'close': [90],
        'volume': [200],
        'ema': [80],
        'rsi': [20],
        'macd': [1],
        'macd_signal': [0],
        'bb_high': [110],
        'bb_low': [95],
        'bb_width': [1],
        'volume_ma': [100]
    })

    monkeypatch.setattr(strategies, 'fetch_klines', lambda symbol, interval: df)
    monkeypatch.setattr(strategies, 'apply_indicators', lambda d: d)

    result = strategies.generate_signal('TEST', ['1h', '4h'])
    assert result == 'BUY'

    score = strategies.generate_signal('TEST', ['1h', '4h'], return_score=True)
    assert score == 10
