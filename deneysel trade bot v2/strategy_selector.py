import strategies
from features import generate_features
from ml_model import load_model, predict


def volatility_breakout_signal(symbol, timeframes, return_score=False):
    buy = 0
    sell = 0
    for tf in timeframes:
        df = strategies.fetch_klines(symbol, tf)
        df['range'] = df['high'].astype(float) - df['low'].astype(float)
        df['target'] = df['open'].astype(float) + df['range'].shift(1) * 0.5
        latest = df.iloc[-1]
        prev_range = df['range'].shift(1).iloc[-1]
        if latest['close'] > latest['target']:
            buy += 1
        elif latest['close'] < float(latest['open']) - prev_range * 0.5:
            sell += 1
    if return_score:
        return buy - sell
    if buy == len(timeframes):
        return 'BUY'
    if sell == len(timeframes):
        return 'SELL'
    return 'HOLD'


def ml_model_signal(symbol, timeframes, return_score=False):
    try:
        features = generate_features(symbol)
        model = load_model()
        prediction = predict(features.tail(1), model).iloc[0]
    except Exception:
        prediction = 'HOLD'
    if return_score:
        mapping = {'BUY': 1, 'SELL': -1, 'HOLD': 0}
        return mapping.get(prediction, 0)
    return prediction


# Optional overrides for specific symbols. Any entry here will bypass the
# dynamic selection in ``select_strategy``.
OVERRIDE_STRATEGY_MAP = {
    'BTCUSDT': strategies.generate_signal,
    'PEPEUSDT': volatility_breakout_signal,
    'DOGEUSDT': ml_model_signal,
}


def select_strategy(symbol):
    """Choose a strategy for ``symbol`` based on recent volatility.

    Symbols present in :data:`OVERRIDE_STRATEGY_MAP` use the mapped strategy.
    All other symbols are classified automatically. Highly volatile coins use a
    volatility breakout approach, low-volatility coins keep the default EMA
    strategy, and the remainder utilise the ML model.
    """

    if symbol in OVERRIDE_STRATEGY_MAP:
        return OVERRIDE_STRATEGY_MAP[symbol]

    try:
        df = strategies.fetch_klines(symbol, '1h', limit=48)
        df['close'] = df['close'].astype(float)
        volatility = df['close'].pct_change().std()
    except Exception:
        # On failure fall back to the base strategy
        return strategies.generate_signal

    if volatility is None:
        return strategies.generate_signal

    if volatility > 0.05:
        return volatility_breakout_signal
    if volatility < 0.02:
        return strategies.generate_signal
    return ml_model_signal


def generate_signal(symbol, timeframes, return_score=False):
    """Generate a trading signal for ``symbol`` using its selected strategy."""

    strategy = select_strategy(symbol)
    return strategy(symbol, timeframes, return_score=return_score)

