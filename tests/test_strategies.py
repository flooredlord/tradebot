import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deneysel trade bot v2')))

import strategies


def _mock_df(**kwargs):
    return pd.DataFrame({k: [v] for k, v in kwargs.items()})


def test_generate_signal_buy(monkeypatch):
    monkeypatch.setattr(strategies, 'fetch_klines', lambda s, tf, limit=100: _mock_df(close=1))
    buy_df = _mock_df(macd=1, macd_signal=0, close=10, ema=5, volume=200, volume_ma=100,
                      rsi=20, bb_low=9, bb_high=11)
    monkeypatch.setattr(strategies, 'apply_indicators', lambda df: buy_df)
    result = strategies.generate_signal('AAA', ['1h', '4h'])
    assert result == 'BUY'
    score = strategies.generate_signal('AAA', ['1h'], return_score=True)
    assert score > 0


def test_generate_signal_sell_and_hold(monkeypatch):
    monkeypatch.setattr(strategies, 'fetch_klines', lambda s, tf, limit=100: _mock_df(close=1))
    sell_df = _mock_df(macd=0, macd_signal=1, close=12, ema=15, volume=50, volume_ma=100,
                       rsi=80, bb_low=9, bb_high=11)
    buy_df = _mock_df(macd=1, macd_signal=0, close=10, ema=5, volume=200, volume_ma=100,
                      rsi=20, bb_low=9, bb_high=11)

    def apply(df):
        # first timeframe -> sell, second -> buy
        if apply.counter == 0:
            apply.counter += 1
            return sell_df
        return buy_df
    apply.counter = 0
    monkeypatch.setattr(strategies, 'apply_indicators', apply)
    result = strategies.generate_signal('AAA', ['1h', '4h'])
    assert result == 'HOLD'
    monkeypatch.setattr(strategies, 'apply_indicators', lambda df: sell_df)
    assert strategies.generate_signal('AAA', ['1h', '4h']) == 'SELL'
