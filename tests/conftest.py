import sys
import types
from pathlib import Path

# Insert project directory with spaces into sys.path
PROJECT_DIR = Path(__file__).resolve().parents[1] / 'deneysel trade bot v2'
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# Provide stub 'binance' package so modules import correctly during tests
if 'binance' not in sys.modules:
    binance = types.ModuleType('binance')
    client_mod = types.ModuleType('binance.client')
    exceptions_mod = types.ModuleType('binance.exceptions')

    class DummyClient:
        def get_symbol_info(self, symbol):
            return {'filters': [{'filterType': 'LOT_SIZE', 'stepSize': '0.01'}]}

        def get_klines(self, symbol, interval, limit=100):
            return []

        def get_asset_balance(self, asset):
            return {'free': '0'}

        def create_order(self, **kwargs):
            return {'fills': [{'price': '0'}], 'executedQty': '0'}

    client_mod.Client = lambda api_key, api_secret: DummyClient()
    exceptions_mod.BinanceAPIException = Exception

    binance.client = client_mod
    binance.exceptions = exceptions_mod
    sys.modules['binance'] = binance
    sys.modules['binance.client'] = client_mod
    sys.modules['binance.exceptions'] = exceptions_mod

# Provide minimal stub 'ta' package
if 'ta' not in sys.modules:
    ta = types.ModuleType('ta')
    ta.trend = types.ModuleType('ta.trend')
    ta.momentum = types.ModuleType('ta.momentum')
    ta.volatility = types.ModuleType('ta.volatility')
    ta.volatility.BollingerBands = lambda series: None
    ta.volatility.average_true_range = lambda h,l,c,window=14: None
    sys.modules['ta'] = ta
    sys.modules['ta.trend'] = ta.trend
    sys.modules['ta.momentum'] = ta.momentum
    sys.modules['ta.volatility'] = ta.volatility


# Provide very small pandas stub with minimal DataFrame and Series
if 'pandas' not in sys.modules:
    class FakeSeries:
        def __init__(self, values):
            self._values = list(values)
            self.iloc = self
        def __getitem__(self, idx):
            return self._values[idx]
        def __iter__(self):
            return iter(self._values)

    class FakeSeriesWrapper:
        def __init__(self, values):
            self._series = FakeSeries(values)
        @property
        def iloc(self):
            return self._series
        def __getitem__(self, key):
            return self._series[key]
        def __len__(self):
            return len(self._series._values)

    class _ILoc:
        def __init__(self, row):
            self._row = row
        def __getitem__(self, idx):
            return self._row

    class FakeDataFrame(dict):
        def __init__(self, data, columns=None):
            if isinstance(data, dict):
                super().__init__({k: list(v) for k, v in data.items()})
            else:
                raise TypeError('Only dict data supported')
            self.iloc = _ILoc({k: v[-1] for k, v in self.items()})

        def __getitem__(self, key):
            return FakeSeriesWrapper(super().__getitem__(key))
    pandas_stub = types.ModuleType('pandas')
    pandas_stub.DataFrame = FakeDataFrame
    pandas_stub.Series = FakeSeries
    sys.modules['pandas'] = pandas_stub
