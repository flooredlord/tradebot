import ta
import pandas as pd
from utils import client

def fetch_klines(symbol, interval='1h', limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    return df

def calculate_atr_stop_loss_take_profit(symbol, atr_multiplier=1.5):
    df = fetch_klines(symbol)
    atr = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14).iloc[-1]
    current_price = df['close'].iloc[-1]

    stop_loss = current_price - (atr * atr_multiplier)
    take_profit = current_price + (atr * atr_multiplier)

    return round(stop_loss, 6), round(take_profit, 6)


def calculate_trailing_stop(entry_price, current_price, trailing_percentage=0.02):
    """Harekete duyarlı zarar kes fiyatı hesaplar."""
    base_stop = entry_price * (1 - trailing_percentage)
    if current_price > entry_price:
        new_stop = current_price * (1 - trailing_percentage)
        base_stop = max(base_stop, new_stop)
    return round(base_stop, 6)
