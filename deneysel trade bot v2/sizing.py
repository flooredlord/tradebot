import pandas as pd
import numpy as np
import ta
from utils import client


def fetch_klines(symbol: str, interval: str = '1h', limit: int = 100) -> pd.DataFrame:
    """Fetch historical klines from Binance."""
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    return df


def _kelly_fraction(returns: pd.Series) -> float:
    """Compute Kelly fraction based on win/loss statistics."""
    if returns.empty:
        return 0.0
    win_rate = (returns > 0).mean()
    win_return = returns[returns > 0].mean()
    loss_return = -returns[returns < 0].mean()
    if loss_return == 0 or np.isnan(loss_return):
        return 0.0
    win_loss_ratio = win_return / loss_return
    return win_rate - (1 - win_rate) / win_loss_ratio


def calculate_position_size(balance: float, symbol: str, risk_portion: float = 0.1) -> float:
    """Return position size in base currency using Kelly and volatility factors."""
    df = fetch_klines(symbol)
    if df.empty:
        return 0.0

    price = df['close'].iloc[-1]
    atr = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14).iloc[-1]
    returns = df['close'].pct_change().dropna()

    sharpe = returns.mean() / returns.std() if returns.std() != 0 else 0.0
    kelly = _kelly_fraction(returns)
    kelly = min(max(kelly, 0.0), 1.0)

    vol_pct = atr / price if price else 0.0
    volatility_factor = 1 - min(vol_pct, 0.9)
    sharpe_factor = min(max((sharpe + 1) / 2, 0.1), 1.0)

    position_fraction = risk_portion * kelly * volatility_factor * sharpe_factor
    return balance * max(position_fraction, 0.0)
