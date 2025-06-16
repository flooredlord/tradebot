import json
from datetime import datetime
import config

FEE_RATE = getattr(config, "FEE_RATE", 0.001)

def generate_tax_report(history_file="trade_history.json"):
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        print("🔍 No trade history found.")
        return

    positions = {}
    total_fees = 0.0
    total_profit = 0.0
    lines = [f"🧾 Tax Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]

    for entry in history:
        symbol = entry["symbol"]
        action = entry["type"]
        price = float(entry["price"])
        qty = float(entry["quantity"])
        value = price * qty
        fee = value * FEE_RATE
        total_fees += fee

        if action == "BUY":
            positions[symbol] = {"price": price, "qty": qty}
        elif action == "SELL" and symbol in positions:
            buy = positions.pop(symbol)
            pnl = (price - buy["price"]) * qty
            total_profit += pnl
            lines.append(
                f"{symbol}: BUY {buy['qty']} @ {buy['price']} / SELL {qty} @ {price} => PnL {pnl:.2f} USDT"
            )

    lines.append(f"Total Fees: {total_fees:.2f} USDT")
    lines.append(f"Net Profit After Fees: {total_profit - total_fees:.2f} USDT")

    report = "\n".join(lines)
    with open("tax_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print(report)

if __name__ == "__main__":
    generate_tax_report()
