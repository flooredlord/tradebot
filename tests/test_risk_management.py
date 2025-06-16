import os
import sys
import pandas as pd
import ta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deneysel trade bot v2')))

import risk_management


def test_calculate_atr(monkeypatch):
    df = pd.DataFrame({
        'high': [2, 3, 4],
        'low': [1, 2, 3],
        'close': [1.5, 2.5, 3.5]
    })
    monkeypatch.setattr(risk_management, 'fetch_klines', lambda symbol: df)
    atr = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14).iloc[-1]
    expected_sl = df['close'].iloc[-1] - atr * 1.5
    expected_tp = df['close'].iloc[-1] + atr * 1.5
    sl, tp = risk_management.calculate_atr_stop_loss_take_profit('AAA')
    assert round(sl, 6) == round(expected_sl, 6)
    assert round(tp, 6) == round(expected_tp, 6)
