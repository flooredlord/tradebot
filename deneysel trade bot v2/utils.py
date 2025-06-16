from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
import json
import math
import logging
from logging.handlers import RotatingFileHandler
import config
from datetime import datetime


client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)

# Configure application logger
logger = logging.getLogger("tradebot")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    "trade_log.txt", maxBytes=1_000_000, backupCount=5, encoding="utf-8"
)
console_handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

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

def log(message, level=logging.INFO):
    """Log a message using the configured logger."""
    logger.log(level, message)
