import json
from collections import defaultdict
from datetime import datetime, date
import config
from telegram_notifier import send_telegram_message


def _load_history(path: str = 'trade_history.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def generate_daily_report(path: str = 'trade_history.json'):
    """Generate daily PnL report and optionally send via Telegram."""
    history = _load_history(path)
    today = date.today()
    day_trades = [h for h in history if datetime.fromisoformat(h['timestamp']).date() == today]
    if not day_trades:
        print('No trades for today')
        return

    positions = {}
    pnl_per_coin = defaultdict(float)

    for entry in day_trades:
        symbol = entry['symbol']
        price = float(entry['price'])
        qty = float(entry['quantity'])
        if entry['type'] == 'BUY':
            positions[symbol] = {'price': price, 'qty': qty}
        elif entry['type'] == 'SELL' and symbol in positions:
            buy = positions.pop(symbol)
            pnl = (price - buy['price']) * buy['qty']
            pnl_per_coin[symbol] += pnl

    total_pnl = sum(pnl_per_coin.values())
    best = max(pnl_per_coin.items(), key=lambda x: x[1])[0] if pnl_per_coin else None
    worst = min(pnl_per_coin.items(), key=lambda x: x[1])[0] if pnl_per_coin else None

    report_lines = [
        f"Daily Report - {today}",
        f"Total PnL: {total_pnl:.2f} USDT",
    ]
    if best:
        report_lines.append(f"Best Coin: {best} ({pnl_per_coin[best]:.2f})")
    if worst:
        report_lines.append(f"Worst Coin: {worst} ({pnl_per_coin[worst]:.2f})")

    report = "\n".join(report_lines)
    print(report)

    if config.TELEGRAM_ENABLED:
        send_telegram_message(report)
