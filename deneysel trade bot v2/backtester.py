"""Simple historical backtesting module."""
import pandas as pd
from binance.client import Client
from strategies import apply_indicators
import config

client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)


def fetch_history(symbol, interval='1h', limit=500):
    klines = client.get_historical_klines(symbol, interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df


def run_backtest(symbol, interval='1h', limit=500):
    df = fetch_history(symbol, interval, limit)
    df = apply_indicators(df)
    balance = 100.0
    position = None
    for _, row in df.iterrows():
        price = row['close']
        if position is None and row['macd'] > row['macd_signal']:
            position = price
        elif position is not None and row['macd'] < row['macd_signal']:
            balance *= price / position
            position = None
    if position:
        balance *= df['close'].iloc[-1] / position
    print(f"Backtest result for {symbol}: {balance:.2f} USDT")


if __name__ == '__main__':
    run_backtest('BTCUSDT')
