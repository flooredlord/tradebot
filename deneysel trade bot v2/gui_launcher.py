import tkinter as tk
from tkinter import ttk

import config
import main


class ConfigField:
    def __init__(self, root, label, default=""):
        ttk.Label(root, text=label).pack(anchor="w")
        self.var = tk.StringVar(value=default)
        ttk.Entry(root, textvariable=self.var, width=40).pack(fill="x")

    def get(self):
        return self.var.get().strip()


def start_bot(fields, root):
    config.BINANCE_API_KEY = fields["api_key"].get()
    config.BINANCE_API_SECRET = fields["api_secret"].get()
    config.TELEGRAM_TOKEN = fields["telegram_token"].get()
    config.TELEGRAM_CHAT_ID = fields["telegram_chat_id"].get()
    base_currency = fields["base_currency"].get()
    if base_currency:
        config.BASE_CURRENCY = base_currency

    try:
        trade_pct = fields["trade_percentage"].get()
        if trade_pct:
            config.TRADE_PERCENTAGE = float(trade_pct)
    except ValueError:
        pass

    try:
        min_trade = fields["min_trade_amount"].get()
        if min_trade:
            config.MIN_TRADE_AMOUNT = float(min_trade)
    except ValueError:
        pass

    try:
        interval = fields["check_interval"].get()
        if interval:
            config.CHECK_INTERVAL = int(interval)
    except ValueError:
        pass

    tfs = fields["timeframes"].get()
    if tfs:
        config.TIMEFRAMES = [t.strip() for t in tfs.split(",") if t.strip()]

    root.destroy()
    main.main()


def main_gui():
    root = tk.Tk()
    root.title("TradeBot Launcher")

    fields = {
        "api_key": ConfigField(root, "Binance API Key", config.BINANCE_API_KEY),
        "api_secret": ConfigField(root, "Binance API Secret", config.BINANCE_API_SECRET),
        "telegram_token": ConfigField(root, "Telegram Token", config.TELEGRAM_TOKEN),
        "telegram_chat_id": ConfigField(root, "Telegram Chat ID", config.TELEGRAM_CHAT_ID),
        "base_currency": ConfigField(root, "Base Currency", config.BASE_CURRENCY),
        "trade_percentage": ConfigField(root, "Trade Percentage", str(config.TRADE_PERCENTAGE)),
        "min_trade_amount": ConfigField(root, "Min Trade Amount", str(config.MIN_TRADE_AMOUNT)),
        "check_interval": ConfigField(root, "Check Interval (s)", str(config.CHECK_INTERVAL)),
        "timeframes": ConfigField(root, "Timeframes (comma separated)", ",".join(config.TIMEFRAMES)),
    }

    ttk.Button(
        root,
        text="Start Bot",
        command=lambda: start_bot(fields, root)
    ).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main_gui()
