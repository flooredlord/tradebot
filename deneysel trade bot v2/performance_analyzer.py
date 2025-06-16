import json
from datetime import datetime
from collections import defaultdict

def analyze_performance():
    try:
        with open('trade_history.json', 'r', encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        print("🔍 No trade history found.")
        return

    positions = {}
    pnl_data = defaultdict(lambda: {"total_pnl": 0, "win": 0, "loss": 0, "count": 0})

    for entry in history:
        symbol = entry['symbol']
        action = entry['type']
        price = float(entry['price'])
        qty = float(entry['quantity'])
        ts = entry['timestamp']

        if action == 'BUY':
            positions[symbol] = {"price": price, "quantity": qty, "timestamp": ts}
        elif action == 'SELL' and symbol in positions:
            buy = positions.pop(symbol)
            entry_total = buy['price'] * buy['quantity']
            exit_total = price * qty
            pnl = exit_total - entry_total
            pnl_data[symbol]["total_pnl"] += pnl
            pnl_data[symbol]["count"] += 1
            if pnl >= 0:
                pnl_data[symbol]["win"] += 1
            else:
                pnl_data[symbol]["loss"] += 1

    total_win = sum(v["win"] for v in pnl_data.values())
    total_count = sum(v["count"] for v in pnl_data.values())
    total_pnl = sum(v["total_pnl"] for v in pnl_data.values())
    success_rate = (total_win / total_count * 100) if total_count else 0

    report_lines = [
        f"📊 Trade Performance Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total PnL: {total_pnl:.2f} USDT",
        f"Success Rate: {success_rate:.2f}% ({total_win}/{total_count})",
        "-" * 40
    ]

    sorted_coins = sorted(pnl_data.items(), key=lambda x: x[1]['total_pnl'], reverse=True)
    for coin, stats in sorted_coins:
        report_lines.append(
            f"{coin}: PnL={stats['total_pnl']:.2f}, Win={stats['win']}, Loss={stats['loss']}, Trades={stats['count']}"
        )

    report = "\n".join(report_lines)
    print(report)

    with open("performance_report.txt", "w", encoding="utf-8") as f:
        f.write(report)