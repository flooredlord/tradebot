from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
import json
import math
import logging
from logging.handlers import RotatingFileHandler
import config
from datetime import datetime


class DummyClient:
    """Fallback Binance client used when network access is unavailable."""

    def get_symbol_info(self, symbol):
        return {
            "filters": [
                {"filterType": "LOT_SIZE", "stepSize": "1"},
                {"filterType": "MIN_NOTIONAL", "minNotional": "10"},
            ]
        }

    def get_exchange_info(self):
        return {"symbols": []}

    def get_asset_balance(self, asset):
        return {"free": "0"}

    def create_order(self, **kwargs):
        qty = kwargs.get("quantity", 0)
        price = kwargs.get("price", "0")
        return {"fills": [{"price": price, "qty": qty}], "executedQty": qty}

    def create_oco_order(self, **kwargs):
        return {}

    def get_ticker(self, symbol):
        return {"quoteVolume": "0", "price": "0"}


# Attempt to create the real Binance client unless dummy mode is requested or
# initialization fails (e.g. due to network restrictions).
_use_dummy = os.getenv("USE_DUMMY_CLIENT", "0") == "1"
if not _use_dummy:
    try:
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
    except Exception as e:  # pragma: no cover - network failure
        print(f"Binance client init failed: {e}. Falling back to DummyClient")
        client = DummyClient()
else:  # pragma: no cover - explicit dummy mode
    client = DummyClient()

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

def place_order(symbol, side, quantity, stop_loss=None, take_profit=None, retries=3):
    """Place a market order and optionally set OCO take-profit and stop-loss.
    Retries automatically on API errors."""
    attempt = 0
    while attempt < retries:
        try:
            order = client.create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            print(f"Order placed: {order}")
            save_trade_history(symbol, side, float(order['fills'][0]['price']), float(order['executedQty']))

            if side == 'BUY' and stop_loss and take_profit:
                try:
                    stop_limit_price = round(stop_loss * 0.995, 6)
                    oco = client.create_oco_order(
                        symbol=symbol,
                        side='SELL',
                        quantity=quantity,
                        price=str(take_profit),
                        stopPrice=str(stop_loss),
                        stopLimitPrice=str(stop_limit_price),
                        stopLimitTimeInForce='GTC'
                    )
                    print(f"OCO order placed: {oco}")
                except BinanceAPIException as e:
                    print(f"Binance OCO error: {e}")

            return order
        except BinanceAPIException as e:
            print(f"Binance API error: {e}")
            attempt += 1
            if attempt >= retries:
                return None

def log(message, level=logging.INFO):
    """Log a message using the configured logger."""
    logger.log(level, message)


def trade_limit_exceeded(max_trades_per_day=10):
    """Check if the number of trades today exceeds the given limit."""
    if not os.path.exists("trade_history.json"):
        return False
    with open("trade_history.json", "r", encoding="utf-8") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return False

    today = datetime.now().date()
    count = sum(1 for h in history if datetime.fromisoformat(h["timestamp"]).date() == today)
    return count >= max_trades_per_day


def place_partial_sell(symbol, total_quantity, targets):
    """Sell fractions of a position at different target prices.

    Parameters
    ----------
    symbol : str
        Trading pair symbol.
    total_quantity : float
        Total quantity to sell.
    targets : list of tuple
        Each tuple should contain (target_price, fraction) where fraction is
        between 0 and 1.
    """
    for price, frac in targets:
        qty = round(total_quantity * frac, 8)
        place_order(symbol, 'SELL', qty, take_profit=price)

