# TradeBot

This repository contains a simple trading bot project.

## New Features

The bot now provides helper modules for:
* `features.py` – prepare machine-learning features from OHLCV data.
* `ml_model.py` – train a RandomForest model and make predictions.
* `daily_report.py` – create a daily PnL summary and optionally send it via Telegram.

* `dashboard.py` – a Tkinter GUI displaying open positions and trade history.
* `backtester.py` – run a basic historical backtest using Binance data.
* `position_manager.py` – keeps track of last exit times to allow re-entry checks.
* `utils.py` – includes retry logic for orders, partial sell support, and daily trade limit checks.

Additional helper modules include:
* `bot_command_handler.py` – polling Telegram bot for `/status`, `/pnl`, `/pause` and `/resume` commands.
* `regime_detector.py` – determine if the market is trending or ranging.
* `walk_forward.py` – perform walk-forward validation of machine-learning models.
* `paper_trade.py` – simulate trades without sending real orders.
* `metrics_db.py` – store trade and PnL metrics in a SQLite database.
* `healthcheck.py` – basic health monitor that can restart the bot.
* `autotune.py` – run a small grid search to find the best ML hyperparameters.


## Running Tests

The project uses [pytest](https://pytest.org/) for unit testing. To run the
test suite, execute the following command from the repository root:

```bash
pytest
```

This command will discover and run all tests inside the `tests/` directory.

## GUI Launcher

A simple Tkinter utility `gui_launcher.py` allows you to enter common configuration
parameters such as API keys and trade size before starting the bot. Run it with:

```bash
python gui_launcher.py
```

To build a standalone executable on Windows, install [PyInstaller](https://pyinstaller.org)
and execute:

```bash
pyinstaller --onefile gui_launcher.py
```

The resulting binary will be placed in the `dist/` directory and can be run with a
single click.
