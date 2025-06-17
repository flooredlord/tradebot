import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = 'ml_model.pkl'


def train_model(features: pd.DataFrame, labels: pd.Series) -> RandomForestClassifier:
    """Train a RandomForest model using provided features and labels."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(features, labels)
    joblib.dump(model, MODEL_PATH)
    return model


def load_model() -> RandomForestClassifier | None:
    """Load a trained model from disk if available."""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def predict(features: pd.DataFrame, model: RandomForestClassifier | None = None) -> pd.Series:
    """Predict BUY/SELL/HOLD labels using the trained model."""
    if model is None:
        model = load_model()
    if model is None:
        raise ValueError('Model not trained')
    return pd.Series(model.predict(features), index=features.index)
