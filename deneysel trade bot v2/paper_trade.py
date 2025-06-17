import json
from datetime import datetime

TRADE_HISTORY = "paper_trade_history.json"


def paper_place_order(symbol: str, side: str, quantity: float, price: float) -> None:
    """Record a simulated trade to the paper trade history."""
    entry = {
        "symbol": symbol,
        "type": side,
        "price": price,
        "quantity": quantity,
        "timestamp": datetime.now().isoformat(),
    }

    history = []
    try:
        with open(TRADE_HISTORY, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(entry)
    with open(TRADE_HISTORY, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


class PaperBroker:
    """A simple broker that simulates order fills."""

    def market_buy(self, symbol: str, quantity: float, price: float) -> None:
        paper_place_order(symbol, "BUY", quantity, price)

    def market_sell(self, symbol: str, quantity: float, price: float) -> None:
        paper_place_order(symbol, "SELL", quantity, price)
