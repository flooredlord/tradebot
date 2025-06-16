from binance.client import Client
from binance.exceptions import BinanceAPIException
import math
import config

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

def place_order(symbol, side, quantity):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        print(f"Order placed: {order}")
        return order
    except BinanceAPIException as e:
        print(f"Binance API error: {e}")
        return None

def log(message):
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # İşlem türüne göre emoji seç
    if 'BUY order' in message:
        emoji = '🟢'
    elif 'SELL order' in message:
        emoji = '🔴'
    elif 'HOLD' in message:
        emoji = '⚪'
    else:
        emoji = '📝'

    line = f"{emoji} [{timestamp}] {message}"
    with open('trade_log.txt', 'a') as f:
        f.write(line + '\\n')
    print(line)