import json
import os
from datetime import datetime
from typing import List

import matplotlib.pyplot as plt
import pandas as pd


def _load_history(path: str) -> List[dict]:
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def generate_performance_graphs(history_file: str = 'trade_history.json', out_dir: str = 'graphs') -> None:
    """Create daily/weekly/monthly PnL graphs from trade history."""
    history = _load_history(history_file)
    if not history:
        return
    data = []
    positions = {}
    for entry in history:
        ts = datetime.fromisoformat(entry['timestamp'])
        symbol = entry['symbol']
        side = entry['type']
        price = float(entry['price'])
        qty = float(entry['quantity'])
        if side == 'BUY':
            positions[symbol] = (price, qty)
        elif side == 'SELL' and symbol in positions:
            buy_p, buy_q = positions.pop(symbol)
            pnl = (price - buy_p) * min(qty, buy_q)
            data.append({'timestamp': ts, 'pnl': pnl})
    if not data:
        return
    df = pd.DataFrame(data).set_index('timestamp')
    os.makedirs(out_dir, exist_ok=True)
    for freq, name in [('D', 'daily'), ('W', 'weekly'), ('M', 'monthly')]:
        series = df['pnl'].resample(freq).sum().cumsum()
        if series.empty:
            continue
        plt.figure()
        series.plot()
        plt.title(f'Cumulative PnL ({name})')
        plt.xlabel('Date')
        plt.ylabel('PnL (USDT)')
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f'pnl_{name}.png'))
        plt.close()
