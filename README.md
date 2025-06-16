# TradeBot

This repository contains a simple trading bot project.

## New Features

The bot now provides helper modules for:

* `dashboard.py` – a Tkinter GUI displaying open positions and trade history.
* `backtester.py` – run a basic historical backtest using Binance data.
* `position_manager.py` – keeps track of last exit times to allow re-entry checks.
* `utils.py` – includes retry logic for orders, partial sell support, and daily trade limit checks.


## Running Tests

The project uses [pytest](https://pytest.org/) for unit testing. To run the
test suite, execute the following command from the repository root:

```bash
pytest
```

This command will discover and run all tests inside the `tests/` directory.
