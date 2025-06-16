# TradeBot

This repository contains **deneysel trade bot v2**, an experimental cryptocurrency trading bot designed for the Binance exchange. The bot selects liquid trading pairs, runs a multi‐timeframe strategy and manages trades automatically. Trade results are logged and summarized so you can monitor your performance over time.

## Setup

1. Install Python 3.10 or newer.
2. Install the required packages:
   ```bash
   pip install python-binance pandas ta requests
   ```
3. Copy `deneysel trade bot v2/config.py` and edit the values with your own API credentials and preferences.
4. (Optional) Create an `update` folder to place patch files. The bot automatically applies patches on start.

## Configuration

All settings are stored in `config.py`. Important variables include:

- `BINANCE_API_KEY` / `BINANCE_API_SECRET` – your Binance API credentials.
- `BASE_CURRENCY` – quote currency used for trading (default `USDT`).
- `TRADE_SYMBOLS` – list of symbols to trade. Leave empty to automatically load the top coins.
- `MIN_TRADE_AMOUNT` – minimum order value in USDT.
- `TRADE_PERCENTAGE` – percentage of available balance to use per trade.
- `TIMEFRAMES` – list of candle intervals used for signal generation.
- `TELEGRAM_ENABLED` – enable or disable notifications.
- `TELEGRAM_TOKEN` / `TELEGRAM_CHAT_ID` – credentials for Telegram messages.
- `USE_RSI`, `USE_BOLLINGER`, `MIN_BUY_SIGNALS`, `MIN_SELL_SIGNALS` – indicator options.
- `CHECK_INTERVAL` – how often the bot checks for new signals (in seconds).

Adjust these values as needed before running the bot.

## Running the Bot

From the project directory:
```bash
cd "deneysel trade bot v2"
python main.py
```
The bot will load the latest top symbols, evaluate trading signals and place market orders when conditions are met. Executed trades are stored in `trade_history.json` and a running log is written to `trade_log.txt`.

## Performance Analysis

After each cycle, the bot calls `analyze_performance()` which calculates total PnL and win/loss statistics from the trade history. A formatted report is printed and saved to `performance_report.txt` for later review.

## Telegram Notifications

When `TELEGRAM_ENABLED` is set to `True` and the credentials are provided, every buy, sell or profit-taking action generates a Telegram message. This allows you to track activity remotely on your phone.

---
Use responsibly. This project is for educational purposes and comes with no guarantee of profit or safety.
