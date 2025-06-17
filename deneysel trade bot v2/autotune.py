import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


BEST_PARAMS_FILE = "best_model_params.json"


def autotune(X, y) -> dict:
    """Run a small grid search and save best parameters."""
    param_grid = {
        "n_estimators": [50, 100],
        "max_depth": [None, 5, 10],
    }
    search = GridSearchCV(RandomForestClassifier(), param_grid, cv=3)
    search.fit(X, y)
    best_params = search.best_params_
    with open(BEST_PARAMS_FILE, "w", encoding="utf-8") as f:
        json.dump(best_params, f, indent=2)
    return best_params
