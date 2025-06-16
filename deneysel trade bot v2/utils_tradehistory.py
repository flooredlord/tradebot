import os
import shutil
from datetime import datetime

target = "utils.py"
backup_dir = "backup"
old_versions_dir = "old_versions"
patched_dir = "patched"

os.makedirs(backup_dir, exist_ok=True)
os.makedirs(old_versions_dir, exist_ok=True)
os.makedirs(patched_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(backup_dir, f"{target}.bak_{timestamp}")
old_version_file = os.path.join(old_versions_dir, f"{target}_old_{timestamp}")
patch_archive = os.path.join(patched_dir, f"patch_utils_tradehistory_{timestamp}.py")

print(f"🔧 Patching {target}...")

patched_code = """from binance.client import Client
from binance.exceptions import BinanceAPIException
import math
import config
import json
from datetime import datetime

if not config.BINANCE_API_KEY or not config.BINANCE_API_SECRET:
    raise ValueError(
        "Binance API credentials are missing. Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables."
    )

client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)

def get_symbol_info(symbol):
    return client.get_symbol_info(symbol)

def adjust_quantity_to_lot_size(symbol, quantity):
    symbol_info = get_symbol_info(symbol)
    lot_size = next(f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE')
    step_size = float(lot_size['stepSize'])
    adjusted_qty = math.floor(quantity / step_size) * step_size
    return float(f"{adjusted_qty:.8f}")

def adjust_notional_to_min(symbol, quantity, price):
    symbol_info = get_symbol_info(symbol)
    min_notional_filter = next((f for f in symbol_info['filters'] if f['filterType'] == 'MIN_NOTIONAL'), None)

    if not min_notional_filter:
        return quantity

    min_notional_value = float(min_notional_filter['minNotional'])
    total_value = quantity * price

    if total_value < min_notional_value:
        required_qty = min_notional_value / price
        return float(f"{required_qty:.8f}")
    return quantity

def get_balance(asset):
    balance = client.get_asset_balance(asset)
    return float(balance['free'])

def save_trade_history(symbol, side, price, quantity):
    entry = {
        "symbol": symbol,
        "type": side,
        "price": price,
        "quantity": quantity,
        "timestamp": datetime.now().isoformat()
    }

    history = []
    if os.path.exists("trade_history.json"):
        with open("trade_history.json", "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.append(entry)

    with open("trade_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def place_order(symbol, side, quantity):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        print(f"Order placed: {order}")
        save_trade_history(symbol, side, float(order['fills'][0]['price']), float(order['executedQty']))
        return order
    except BinanceAPIException as e:
        print(f"Binance API error: {e}")
        return None

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if 'BUY order' in message:
        emoji = '🟢'
    elif 'SELL order' in message:
        emoji = '🔴'
    elif 'HOLD' in message:
        emoji = '⚪'
    else:
        emoji = '📝'

    line = f"{emoji} [{timestamp}] {message}"
    with open('trade_log.txt', 'a', encoding='utf-8') as f:
        f.write(line + '\\n')
    print(line)
"""

# Yedekle
shutil.copyfile(target, backup_file)
shutil.copyfile(target, old_version_file)

# Yeni kodu uygula
with open(target, 'w', encoding='utf-8') as f:
    f.write(patched_code)

# Patch dosyasını arşivle
shutil.copyfile(__file__, patch_archive)

print(f"✅ {target} updated successfully.")
print(f"📦 Backup saved: {backup_file}")
print(f"📁 Old version saved: {old_version_file}")
print(f"📜 Patch archived as: {patch_archive}")