import os
import shutil
from datetime import datetime

target = "performance_analyzer.py"
backup_dir = "backup"
old_versions_dir = "old_versions"
patched_dir = "patched"

os.makedirs(backup_dir, exist_ok=True)
os.makedirs(old_versions_dir, exist_ok=True)
os.makedirs(patched_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(backup_dir, f"{target}.bak_{timestamp}")
old_version_file = os.path.join(old_versions_dir, f"{target}_old_{timestamp}")
patch_archive = os.path.join(patched_dir, f"patch_performance_{timestamp}.py")

print(f"🔧 Patching {target}...")

# Patch içeriği:
patched_code = '''import json
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
        report_lines.append(f"{coin}: PnL={stats['total_pnl']:.2f}, Win={stats['win']}, Loss={stats['loss']}, Trades={stats['count']}")

    report = "\\n".join(report_lines)
    print(report)

    with open("performance_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
'''

# Backup
shutil.copyfile(target, backup_file)
shutil.copyfile(target, old_version_file)

# Write patch
with open(target, 'w', encoding='utf-8') as f:
    f.write(patched_code)

# Archive patch
shutil.copyfile(__file__, patch_archive)

print(f"✅ {target} updated successfully.")
print(f"📦 Backup saved: {backup_file}")
print(f"📁 Old version saved: {old_version_file}")
print(f"📜 Patch archived as: {patch_archive}")