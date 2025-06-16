import shutil
from datetime import datetime

target = "strategies.py"
backup = f"{target}.bak"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
archive = f"patched/patch_strategies_{timestamp}.py"

print("🔧 Patching strategies.py...")

with open(target, 'r', encoding='utf-8') as f:
    original = f.read()

patched = '''import pandas as pd
import ta
from utils import client
import config

def fetch_klines(symbol, interval, limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df

def apply_indicators(df):
    df['ema'] = ta.trend.ema_indicator(df['close'], window=21)
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)

    macd = ta.trend.macd(df['close'])
    macd_signal = ta.trend.macd_signal(df['close'])
    df['macd'] = macd
    df['macd_signal'] = macd_signal

    bb = ta.volatility.BollingerBands(df['close'])
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    df['bb_width'] = bb.bollinger_wband()

    df['volume_ma'] = df['volume'].rolling(window=20).mean()
    return df

def generate_signal(symbol, timeframes):
    buy_signals = []
    sell_signals = []

    for tf in timeframes:
        df = fetch_klines(symbol, tf)
        df = apply_indicators(df)
        latest = df.iloc[-1]

        buy = 0
        sell = 0

        if latest['macd'] > latest['macd_signal']:
            buy += 1
        elif latest['macd'] < latest['macd_signal']:
            sell += 1

        if latest['close'] > latest['ema']:
            buy += 1
        elif latest['close'] < latest['ema']:
            sell += 1

        if latest['volume'] > latest['volume_ma']:
            buy += 1

        if config.USE_RSI:
            if latest['rsi'] < config.RSI_BUY_THRESHOLD:
                buy += 1
            elif latest['rsi'] > config.RSI_SELL_THRESHOLD:
                sell += 1

        if config.USE_BOLLINGER:
            if latest['close'] < latest['bb_low']:
                buy += 1
            elif latest['close'] > latest['bb_high']:
                sell += 1

        if buy >= config.MIN_BUY_SIGNALS:
            buy_signals.append(tf)
        elif sell >= config.MIN_SELL_SIGNALS:
            sell_signals.append(tf)

    if len(buy_signals) == len(timeframes):
        return 'BUY'
    elif len(sell_signals) == len(timeframes):
        return 'SELL'
    else:
        return 'HOLD'
'''

# Yedekleme
shutil.copyfile(target, backup)

# Yeni kodu yaz
with open(target, 'w', encoding='utf-8') as f:
    f.write(patched)

# Arşivle
shutil.copyfile(__file__, archive)

print(f"✅ {target} updated successfully.")
print(f"📦 Patch archived as: {archive}")