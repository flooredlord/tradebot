# Tradebot

This project contains a simple trading bot. Credentials are loaded from environment variables.

## Environment Variables

The bot expects the following variables to be set:

- `BINANCE_API_KEY` – Binance API key
- `BINANCE_API_SECRET` – Binance API secret
- `TELEGRAM_TOKEN` – Telegram bot token
- `TELEGRAM_CHAT_ID` – ID of the chat where notifications are sent

An example `.env` file is provided as `example.env`.

If any of these variables are missing when the bot starts, `config.py` will raise an error.

