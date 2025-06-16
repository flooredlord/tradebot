# Trade Bot

This repository contains a simple experimental cryptocurrency trading bot built with
[python-binance](https://github.com/sammchardy/python-binance). It fetches market
information from Binance, generates basic buy/sell signals and can notify a
Telegram chat when trades are executed.

## Requirements

- Python 3.10 or newer
- The following Python packages:
  - `python-binance`
  - `pandas`
  - `ta`
  - `requests`

You can install them with:

```bash
pip install python-binance pandas ta requests
```

## Configuration

Most settings are read from environment variables with sensible defaults. Create
a `.env` file or export variables in your shell before running the bot. Important
variables include:

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `BINANCE_API_KEY` | Binance API key | *required* |
| `BINANCE_API_SECRET` | Binance API secret | *required* |
| `BASE_CURRENCY` | Quote currency used for trading | `USDT` |
| `TRADE_SYMBOLS` | Comma separated list of symbols to trade. Leave empty to
  auto-load the top 50 symbols | *(empty)* |
| `MIN_TRADE_AMOUNT` | Minimum trade notional in USDT | `10` |
| `TRADE_PERCENTAGE` | Portion of balance used per trade (0-1) | `0.1` |
| `STOP_LOSS_PERCENTAGE` | Stop loss percentage | `0.05` |
| `TAKE_PROFIT_PERCENTAGE` | Take profit percentage | `0.02` |
| `TIMEFRAMES` | Comma separated candle intervals | `1h,4h` |
| `EXCLUDED_SYMBOLS` | Symbols excluded from the top list | `BNBUSDT,USDCUSDT` |
| `TELEGRAM_ENABLED` | Enable Telegram notifications (`true`/`false`) | `True` |
| `TELEGRAM_TOKEN` | Telegram bot token | *(empty)* |
| `TELEGRAM_CHAT_ID` | Destination chat ID | *(empty)* |
| `USE_RSI` | Toggle RSI filter | `True` |
| `USE_BOLLINGER` | Toggle Bollinger Bands filter | `True` |
| `RSI_BUY_THRESHOLD` | RSI buy level | `30` |
| `RSI_SELL_THRESHOLD` | RSI sell level | `70` |
| `MIN_BUY_SIGNALS` | Minimum indicators signalling buy | `2` |
| `MIN_SELL_SIGNALS` | Minimum indicators signalling sell | `2` |
| `CHECK_INTERVAL` | Seconds to wait between cycles | `1800` |

## Usage

After installing the requirements and setting environment variables, start the
bot with:

```bash
python main.py
```

The bot automatically loads any patches from the `update` folder on startup and
logs trades to `trade_log.txt`. Trade history is recorded in
`trade_history.json`, and performance reports are written to
`performance_report.txt`.

## Example

```bash
export BINANCE_API_KEY=your_key_here
export BINANCE_API_SECRET=your_secret_here
export TELEGRAM_TOKEN=your_telegram_token
export TELEGRAM_CHAT_ID=123456789
python main.py
```

This will run the bot using your API credentials and send notifications to the
specified Telegram chat.
