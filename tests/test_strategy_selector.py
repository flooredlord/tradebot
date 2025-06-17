import sys
import types
from pathlib import Path
import importlib

PROJECT_DIR = Path(__file__).resolve().parents[1] / 'deneysel trade bot v2'


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, PROJECT_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

# Stubs for external deps used in strategy_selector
sys.modules.setdefault('joblib', types.ModuleType('joblib'))
sklearn = types.ModuleType('sklearn')
sklearn.ensemble = types.ModuleType('sklearn.ensemble')
sklearn.ensemble.RandomForestClassifier = object
sys.modules.setdefault('sklearn', sklearn)
sys.modules.setdefault('sklearn.ensemble', sklearn.ensemble)

strategies = load_module('strategies')
strategy_selector = load_module('strategy_selector')


class DummySeries(list):
    def astype(self, dtype):
        return DummySeries([dtype(x) for x in self])

    def pct_change(self):
        result = []
        prev = None
        for v in self:
            if prev is None:
                result.append(0)
            else:
                result.append((v - prev) / prev)
            prev = v
        return DummySeries(result)

    def std(self):
        if not self:
            return 0
        mean = sum(self) / len(self)
        var = sum((x - mean) ** 2 for x in self) / len(self)
        return var ** 0.5


class DummyDataFrame:
    def __init__(self, closes):
        self._closes = closes

    def __getitem__(self, key):
        if key == 'close':
            return DummySeries(list(self._closes))
        raise KeyError(key)

    def __setitem__(self, key, value):
        if key == 'close':
            self._closes = list(value)


def test_override_mapping(monkeypatch):
    monkeypatch.setattr(strategy_selector, 'volatility_breakout_signal', lambda *a, **k: 'VB')
    monkeypatch.setattr(strategy_selector, 'ml_model_signal', lambda *a, **k: 'ML')
    monkeypatch.setattr(strategies, 'generate_signal', lambda *a, **k: 'DEF')

    strategy_selector.OVERRIDE_STRATEGY_MAP = {'AAAUSDT': lambda *a, **k: 'OVR'}

    result = strategy_selector.generate_signal('AAAUSDT', ['1h'])
    assert result == 'OVR'


def test_high_volatility(monkeypatch):
    monkeypatch.setattr(strategy_selector, 'volatility_breakout_signal', lambda *a, **k: 'VB')
    monkeypatch.setattr(strategy_selector, 'ml_model_signal', lambda *a, **k: 'ML')
    monkeypatch.setattr(strategies, 'generate_signal', lambda *a, **k: 'DEF')

    monkeypatch.setattr(strategy_selector, 'OVERRIDE_STRATEGY_MAP', {})
    monkeypatch.setattr(strategies, 'fetch_klines', lambda symbol, tf, limit=48: DummyDataFrame([1, 2, 1, 3, 1]))

    result = strategy_selector.generate_signal('TEST', ['1h'])
    assert result == 'VB'


def test_low_volatility(monkeypatch):
    monkeypatch.setattr(strategy_selector, 'volatility_breakout_signal', lambda *a, **k: 'VB')
    monkeypatch.setattr(strategy_selector, 'ml_model_signal', lambda *a, **k: 'ML')
    monkeypatch.setattr(strategies, 'generate_signal', lambda *a, **k: 'DEF')

    monkeypatch.setattr(strategy_selector, 'OVERRIDE_STRATEGY_MAP', {})
    monkeypatch.setattr(strategies, 'fetch_klines', lambda symbol, tf, limit=48: DummyDataFrame([1]*5))

    result = strategy_selector.generate_signal('TEST', ['1h'])
    assert result == 'DEF'


def test_medium_volatility(monkeypatch):
    monkeypatch.setattr(strategy_selector, 'volatility_breakout_signal', lambda *a, **k: 'VB')
    monkeypatch.setattr(strategy_selector, 'ml_model_signal', lambda *a, **k: 'ML')
    monkeypatch.setattr(strategies, 'generate_signal', lambda *a, **k: 'DEF')

    monkeypatch.setattr(strategy_selector, 'OVERRIDE_STRATEGY_MAP', {})
    monkeypatch.setattr(strategies, 'fetch_klines', lambda symbol, tf, limit=48: DummyDataFrame([1, 1.02, 0.98, 1.01, 0.99]))

    result = strategy_selector.generate_signal('TEST', ['1h'])
    assert result == 'ML'

