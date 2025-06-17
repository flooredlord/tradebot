from features import generate_features
from ml_model import load_model, predict


class MLAgent:
    """Agent that generates trading signals using a machine learning model."""

    def __init__(self):
        self.model = load_model()

    def get_signal(self, symbol: str) -> str:
        if self.model is None:
            return 'HOLD'
        try:
            features = generate_features(symbol)
            if features.empty:
                return 'HOLD'
            pred = predict(features.tail(1), self.model)
            return pred.iloc[0]
        except Exception:
            return 'HOLD'
