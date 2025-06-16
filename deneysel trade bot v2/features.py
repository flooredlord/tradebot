import pandas as pd
import ta
from utils import client


def fetch_klines(symbol: str, interval: str = '1h', limit: int = 100) -> pd.DataFrame:
    """Fetch historical klines from Binance and return as DataFrame."""
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df


def generate_features(symbol: str, interval: str = '1h') -> pd.DataFrame:
    """Generate ML features such as RSI, MACD and Bollinger bands."""
    df = fetch_klines(symbol, interval)
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    df['macd'] = ta.trend.macd(df['close'])
    df['macd_signal'] = ta.trend.macd_signal(df['close'])
    bb = ta.volatility.BollingerBands(df['close'])
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    df['volume_ma'] = df['volume'].rolling(window=20).mean()
    features = df[['rsi', 'macd', 'macd_signal', 'bb_high', 'bb_low', 'volume', 'volume_ma']].dropna()
    return features
