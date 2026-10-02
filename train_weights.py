"""
Learning-Assisted Weight Training Script
==========================================
Trains a regression model to learn optimal weights for the four evaluation
dimensions (relevance, quality, bias, consistency) from labeled data with
human quality ratings.

The learned weights replace the manually-set static weights (0.35, 0.25,
0.25, 0.15) in the aggregator.

Approach:
  - Uses Ridge Regression (L2-regularised linear model) with non-negative
    coefficients to learn a mapping:
        human_rating ≈ w1*relevance + w2*quality + w3*bias + w4*consistency
  - Coefficients are normalised to sum to 1.0 so they remain interpretable
    as percentage weights.
  - The model is evaluated using k-fold cross-validation and reports R²,
    MAE, and RMSE metrics.
  - Learned weights are saved to `models/learned_weights.json` for use
    by the aggregator.

Usage:
    python train_weights.py
    python train_weights.py --dataset data/labeled_dataset.csv
    python train_weights.py --folds 10
"""

import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_validate
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


# ─────────────────────────────────────────────────────────────────────────
# Display helpers
# ─────────────────────────────────────────────────────────────────────────

BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
DIM = "\033[2m"

FEATURE_COLUMNS = ["relevance", "quality", "bias", "consistency"]
TARGET_COLUMN = "human_rating"


def print_banner():
    banner = f"""
{CYAN}{'═' * 65}
  ╔══════════════════════════════════════════════════════════════╗
  ║       LEARNING-ASSISTED WEIGHT TRAINING                     ║
  ║       Training optimal evaluation weights from labeled data ║
  ╚══════════════════════════════════════════════════════════════╝
{'═' * 65}{RESET}
"""
    print(banner)


# ─────────────────────────────────────────────────────────────────────────
# Data loading and validation
# ─────────────────────────────────────────────────────────────────────────

def load_dataset(filepath: str) -> pd.DataFrame:
    """Load and validate the labeled dataset."""
    if not os.path.exists(filepath):
        print(f"{RED}Error: Dataset not found at '{filepath}'{RESET}")
        sys.exit(1)

    df = pd.read_csv(filepath)

    # Validate required columns
    required_cols = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"{RED}Error: Missing columns: {missing}{RESET}")
        sys.exit(1)

    # Validate value ranges
    for col in required_cols:
        if df[col].min() < 0 or df[col].max() > 1:
            print(f"{YELLOW}Warning: Column '{col}' has values outside [0, 1] range{RESET}")

    return df


def inspect_dataset(df: pd.DataFrame):
    """Print dataset statistics."""
    print(f"{BOLD}Dataset Summary:{RESET}")
    print(f"  Total samples     : {len(df)}")

    if "prompt" in df.columns:
        print(f"  Unique prompts    : {df['prompt'].nunique()}")
    if "model" in df.columns:
        print(f"  Unique models     : {df['model'].nunique()}")

    print(f"\n{BOLD}Feature Statistics:{RESET}")
    stats = df[FEATURE_COLUMNS + [TARGET_COLUMN]].describe().T[["mean", "std", "min", "max"]]
    stats.columns = ["Mean", "Std", "Min", "Max"]
    print(stats.to_string())
    print()

    # Correlation with human rating
    print(f"{BOLD}Correlation with Human Rating:{RESET}")
    for col in FEATURE_COLUMNS:
        corr = df[col].corr(df[TARGET_COLUMN])
        bar = "█" * int(abs(corr) * 20)
        color = GREEN if corr > 0.5 else YELLOW if corr > 0.3 else RED
        print(f"  {col:>15s} : {color}{corr:+.4f}{RESET}  [{bar}]")
    print()


# ─────────────────────────────────────────────────────────────────────────
# Model training
# ─────────────────────────────────────────────────────────────────────────

def train_model(
    df: pd.DataFrame,
    n_folds: int = 5,
    alpha: float = 1.0,
) -> dict:
    """
    Train a Ridge regression model to learn optimal weights.

    Args:
        df: Labeled dataset with feature columns and human_rating.
        n_folds: Number of cross-validation folds.
        alpha: Ridge regularisation strength.

    Returns:
        Dictionary with learned weights, metrics, and metadata.
    """
    X = df[FEATURE_COLUMNS].values
    y = df[TARGET_COLUMN].values

    # ── Cross-validation ──
    print(f"{BOLD}Cross-Validation ({n_folds}-fold):{RESET}")
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)

    cv_results = cross_validate(
        Ridge(alpha=alpha, fit_intercept=True),
        X, y,
        cv=kf,
        scoring=["r2", "neg_mean_absolute_error", "neg_mean_squared_error"],
        return_train_score=True,
    )

    metrics = {
        "cv_r2_mean": float(np.mean(cv_results["test_r2"])),
        "cv_r2_std": float(np.std(cv_results["test_r2"])),
        "cv_mae_mean": float(-np.mean(cv_results["test_neg_mean_absolute_error"])),
        "cv_mae_std": float(np.std(cv_results["test_neg_mean_absolute_error"])),
        "cv_rmse_mean": float(np.sqrt(-np.mean(cv_results["test_neg_mean_squared_error"]))),
        "train_r2_mean": float(np.mean(cv_results["train_r2"])),
    }

    for fold_i in range(n_folds):
        r2 = cv_results["test_r2"][fold_i]
        mae = -cv_results["test_neg_mean_absolute_error"][fold_i]
        color = GREEN if r2 > 0.7 else YELLOW if r2 > 0.4 else RED
        print(f"  Fold {fold_i + 1}: R²={color}{r2:.4f}{RESET}  MAE={mae:.4f}")

    print(f"\n  {BOLD}Mean R²  : {GREEN}{metrics['cv_r2_mean']:.4f}{RESET} (±{metrics['cv_r2_std']:.4f})")
    print(f"  {BOLD}Mean MAE : {metrics['cv_mae_mean']:.4f}{RESET} (±{metrics['cv_mae_std']:.4f})")
    print(f"  {BOLD}Mean RMSE: {metrics['cv_rmse_mean']:.4f}{RESET}")
    print(f"  {BOLD}Train R² : {metrics['train_r2_mean']:.4f}{RESET}")

    # Check for overfitting
    overfit_gap = metrics["train_r2_mean"] - metrics["cv_r2_mean"]
    if overfit_gap > 0.15:
        print(f"  {YELLOW}⚠ Potential overfitting detected (train-test gap: {overfit_gap:.3f}){RESET}")
    print()

    # ── Train final model on all data ──
    print(f"{BOLD}Training final model on full dataset...{RESET}")
    model = Ridge(alpha=alpha, fit_intercept=True)
    model.fit(X, y)

    # Extract raw coefficients
    raw_coeffs = model.coef_
    intercept = model.intercept_

    print(f"\n{BOLD}Raw Regression Coefficients:{RESET}")
    print(f"  Intercept: {intercept:.4f}")
    for name, coeff in zip(FEATURE_COLUMNS, raw_coeffs):
        color = GREEN if coeff > 0 else RED
        print(f"  {name:>15s} : {color}{coeff:+.4f}{RESET}")

    # ── Normalise coefficients to get interpretable weights ──
    # Clamp negatives to 0 (a dimension shouldn't have negative weight)
    clamped_coeffs = np.maximum(raw_coeffs, 0)

    if clamped_coeffs.sum() == 0:
        print(f"{RED}Error: All coefficients are zero or negative. Cannot normalise.{RESET}")
        # Fall back to equal weights
        normalised_weights = np.ones(len(FEATURE_COLUMNS)) / len(FEATURE_COLUMNS)
    else:
        normalised_weights = clamped_coeffs / clamped_coeffs.sum()

    learned_weights = {
        name: round(float(w), 4)
        for name, w in zip(FEATURE_COLUMNS, normalised_weights)
    }

    print(f"\n{BOLD}Learned Normalised Weights:{RESET}")
    for name, w in learned_weights.items():
        bar_length = int(w * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        print(f"  {name:>15s} : {GREEN}{w:.4f}{RESET} ({w:.1%})  [{bar}]")

    # ── Full-data metrics ──
    y_pred = model.predict(X)
    full_metrics = {
        "full_r2": float(r2_score(y, y_pred)),
        "full_mae": float(mean_absolute_error(y, y_pred)),
        "full_rmse": float(np.sqrt(mean_squared_error(y, y_pred))),
    }
    metrics.update(full_metrics)

    print(f"\n{BOLD}Full Dataset Fit:{RESET}")
    print(f"  R²   : {GREEN}{full_metrics['full_r2']:.4f}{RESET}")
    print(f"  MAE  : {full_metrics['full_mae']:.4f}")
    print(f"  RMSE : {full_metrics['full_rmse']:.4f}")

    # Compare with manual weights
    print(f"\n{BOLD}Weight Comparison (Manual vs Learned):{RESET}")
    manual = {"relevance": 0.35, "quality": 0.25, "bias": 0.25, "consistency": 0.15}
    print(f"  {'Dimension':>15s}   {'Manual':>8s}   {'Learned':>8s}   {'Change':>8s}")
    print(f"  {'─' * 48}")
    for name in FEATURE_COLUMNS:
        m = manual[name]
        l = learned_weights[name]
        diff = l - m
        color = GREEN if abs(diff) < 0.05 else YELLOW
        print(f"  {name:>15s}   {m:>7.1%}   {l:>7.1%}   {color}{diff:>+7.1%}{RESET}")
    print()

    return {
        "weights": learned_weights,
        "raw_coefficients": {
            name: round(float(c), 6) for name, c in zip(FEATURE_COLUMNS, raw_coeffs)
        },
        "intercept": round(float(intercept), 6),
        "metrics": metrics,
        "training_config": {
            "alpha": alpha,
            "n_folds": n_folds,
            "n_samples": len(df),
            "model_type": "Ridge Regression",
        },
    }


# ─────────────────────────────────────────────────────────────────────────
# Save results
# ─────────────────────────────────────────────────────────────────────────

def save_weights(result: dict, output_dir: str = "models"):
    """Save learned weights and training metadata to JSON."""
    os.makedirs(output_dir, exist_ok=True)

    # Add timestamp
    result["trained_at"] = datetime.now().isoformat()

    filepath = os.path.join(output_dir, "learned_weights.json")
    with open(filepath, "w") as f:
        json.dump(result, f, indent=2)

    print(f"{GREEN}✓ Learned weights saved to: {filepath}{RESET}")
    return filepath


# ─────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train optimal evaluation weights from labeled data."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="data/labeled_dataset.csv",
        help="Path to the labeled dataset CSV.",
    )
    parser.add_argument(
        "--folds",
        type=int,
        default=5,
        help="Number of cross-validation folds (default: 5).",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=1.0,
        help="Ridge regularisation strength (default: 1.0).",
    )
    args = parser.parse_args()

    print_banner()

    # Load data
    df = load_dataset(args.dataset)
    inspect_dataset(df)

    # Train
    result = train_model(df, n_folds=args.folds, alpha=args.alpha)

    # Save
    save_weights(result)

    print(f"\n{BOLD}Next Steps:{RESET}")
    print(f"  Run the evaluation with learned weights:")
    print(f"  {CYAN}python main.py --use-learned-weights{RESET}")
    print()
