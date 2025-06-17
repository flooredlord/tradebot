import pandas as pd
import numpy as np

from utils import client


def fetch_close(symbol: str, interval: str = "1h", limit: int = 200) -> pd.DataFrame:
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "qav", "trades", "tbav", "tqav", "ignore"
    ])
    df[["high", "low", "close"]] = df[["high", "low", "close"]].astype(float)
    return df


def bollinger_band_width(close: pd.Series, window: int = 20) -> pd.Series:
    ma = close.rolling(window).mean()
    std = close.rolling(window).std()
    upper = ma + 2 * std
    lower = ma - 2 * std
    width = (upper - lower) / ma
    return width


def detect_market_regime(df: pd.DataFrame) -> str:
    """Return 'TREND' or 'RANGE' based on simple metrics."""
    if len(df) < 20:
        return "UNKNOWN"

    width = bollinger_band_width(df["close"])
    slope = (df["close"].iloc[-1] - df["close"].iloc[0]) / len(df)
    adx_like = (df["high"].diff().abs() - df["low"].diff().abs()).abs().rolling(14).mean().iloc[-1]

    if width.iloc[-1] < width.mean() and abs(slope) < adx_like:
        return "RANGE"
    return "TREND"


if __name__ == "__main__":  # pragma: no cover - manual usage
    d = fetch_close("BTCUSDT")
    print(detect_market_regime(d))
