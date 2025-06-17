import config
from strategies import generate_signal


class SwingAgent:
    """Agent that uses indicator based swing trading strategy."""

    def get_signal(self, symbol: str) -> str:
        return generate_signal(symbol, config.TIMEFRAMES)
