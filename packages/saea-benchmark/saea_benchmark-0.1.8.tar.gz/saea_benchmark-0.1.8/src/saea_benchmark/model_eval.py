from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

import numpy as np
import optuna
import pandas as pd
from scanpy import read_h5ad
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, f1_score, matthews_corrcoef


def gorodkin_coefficient(y_true, y_pred):
    c = confusion_matrix(y_true, y_pred)
    c = np.array(c, dtype=float)

    n = np.sum(c)  # Num samples
    trace_c = np.trace(c)

    c_row_sums = np.sum(c, axis=1)
    c_col_sums = np.sum(c, axis=0)

    sum_cicj = np.sum(c_row_sums * c_col_sums)
    numerator = n * trace_c - sum_cicj

    den_left = n**2 - np.sum(c_row_sums**2)
    den_right = n**2 - np.sum(c_col_sums**2)

    denominator = np.sqrt(den_left * den_right) + 1e-10
    return numerator / denominator


def create_folds(
    train_val_adata_path: str,
    test_adata_path: str,
    split_df_path: str,
) -> dict[str, tuple[np.ndarray] | np.ndarray]:
    split_df = pd.read_csv(split_df_path)
    train_val_adata = read_h5ad(train_val_adata_path)
    test_adata = read_h5ad(test_adata_path)
    assert all(
        attr in train_val_adata.obs.columns for attr in ["accession", "y"]
    ), 'train_val_adata must have columns "accession" and "y"'
    assert all(
        attr in test_adata.obs.columns for attr in ["accession", "y"]
    ), 'test_adata must have columns "accession" and "y"'

    idx2ac = {
        idx: train_val_adata.obs["accession"].iloc[idx]
        for idx in range(len(train_val_adata))
    }
    ac2idx = {ac: idx for idx, ac in idx2ac.items()}
    label2idx = {
        label: idx for idx, label in enumerate(train_val_adata.obs["y"].unique())
    }
    train_val_adata.obs["y"] = train_val_adata.obs["y"].map(label2idx)
    test_adata.obs["y"] = test_adata.obs["y"].map(label2idx)

    test_x, test_y = test_adata.X, test_adata.obs["y"]
    folds = []

    for fold_idx in sorted(split_df["cluster"].unique()):
        acs = set(split_df[split_df["cluster"] == fold_idx]["AC"].values)
        val_indices = [ac2idx[ac] for ac in acs]
        train_indices = [
            idx for idx in range(len(train_val_adata)) if idx not in val_indices
        ]
        val_x, val_y = (
            train_val_adata.X[val_indices],
            train_val_adata.obs["y"].iloc[val_indices],
        )
        train_x, train_y = (
            train_val_adata.X[train_indices],
            train_val_adata.obs["y"].iloc[train_indices],
        )
        folds.append((train_x, train_y, val_x, val_y))

    return {
        "folds": folds,
        "test_data": (test_x, test_y),
    }


def prepare_metric(
    metric_name: Literal["f1", "mcc", "gorodkin"],
) -> Callable[[float, float], float]:
    if metric_name == "f1":
        metric = f1_score
    elif metric_name == "mcc":
        metric = matthews_corrcoef
    elif metric_name == "gorodkin":
        metric = gorodkin_coefficient
    else:
        raise ValueError(f"Unknown metric {metric_name}")
    return metric


def start_study(
    folds: dict[str, tuple[np.ndarray] | np.ndarray],
    metric: Callable[[float, float], float],
    n_trials: int = 50,
    random_state: int = 42,
) -> dict[str, Any]:
    train_val_folds = folds["folds"]
    test_x, test_y = folds["test_data"]
    results = {}

    for idx, (train_x, train_y, val_x, val_y) in enumerate(train_val_folds):

        def objective(trial):
            nonlocal train_x, train_y, val_x, val_y
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 10, 200),
                "max_depth": trial.suggest_int("max_depth", 1, 20),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
            }

            rf = RandomForestClassifier(**params, random_state=random_state)
            rf.fit(train_x, train_y)
            val_pred = rf.predict(val_x)
            return metric(val_y, val_pred)

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=n_trials)

        trial = study.best_trial
        best_params = trial.params
        rf = RandomForestClassifier(**best_params, random_state=random_state)
        rf.fit(train_x, train_y)

        test_pred = rf.predict(test_x)
        test_score = gorodkin_coefficient(test_y, test_pred)
        results[idx] = {
            "best_params": trial.params,
            "best_validation_score": trial.value,
            "test_score": test_score,
        }

    return results


def evaluate_with_model(
    train_val_adata_path: str,
    test_adata_path: str,
    split_df_path: str,
    metric_name: Literal["f1", "mcc", "gorodkin"],
    n_trials: int = 50,
    random_state: int = 42,
    allow_logging: bool = False,
) -> dict[str, Any]:
    if not allow_logging:
        optuna.logging.disable_default_handler()
    folds = create_folds(train_val_adata_path, test_adata_path, split_df_path)
    metric = prepare_metric(metric_name)
    results = start_study(folds, metric, n_trials, random_state)
    return results
