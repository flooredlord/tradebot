from __future__ import annotations

import pandas as pd
from sklearn.metrics import accuracy_score


def walk_forward(model, data: pd.DataFrame, label_column: str, train_size: int = 100, test_size: int = 20) -> list[float]:
    """Simple walk-forward validation returning accuracy scores."""
    scores = []
    start = 0
    while start + train_size + test_size <= len(data):
        train = data.iloc[start:start + train_size]
        test = data.iloc[start + train_size:start + train_size + test_size]
        X_train = train.drop(label_column, axis=1)
        y_train = train[label_column]
        X_test = test.drop(label_column, axis=1)
        y_test = test[label_column]

        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        scores.append(accuracy_score(y_test, preds))
        start += test_size
    return scores
