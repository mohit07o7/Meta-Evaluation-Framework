"""
Visualisation Module
=====================
Generates publication-ready charts from evaluation results:
  1. Radar / spider chart — comparing models across all 4 dimensions
  2. Bar chart — ranked final scores
  3. Weight comparison chart — manual vs learned weights
  4. Heatmap — per-prompt × per-model scores (for benchmark results)

Usage:
    python visualise.py
    python visualise.py --benchmark results/benchmark_XXXXXXXX_XXXXXX.csv
"""

import argparse
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for saving files
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import FancyBboxPatch
import json


# ─────────────────────────────────────────────────────────────────────────
# Style config
# ─────────────────────────────────────────────────────────────────────────

# Dark theme colours
BG_COLOR = "#1a1a2e"
CARD_COLOR = "#16213e"
TEXT_COLOR = "#e0e0e0"
GRID_COLOR = "#2a2a4a"
ACCENT_COLORS = ["#00d4aa", "#ff6b6b", "#ffd93d", "#6bcbff", "#c084fc", "#ff9f43"]

plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": CARD_COLOR,
    "axes.edgecolor": GRID_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "text.color": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "grid.color": GRID_COLOR,
    "grid.alpha": 0.3,
    "font.family": "sans-serif",
    "font.size": 11,
})


# ─────────────────────────────────────────────────────────────────────────
# 1. Radar Chart
# ─────────────────────────────────────────────────────────────────────────

def plot_radar_chart(results: list[dict], output_path: str = "charts/radar_chart.png"):
    """
    Create a radar/spider chart comparing models across all 4 dimensions.
    """
    dimensions = ["relevance", "quality", "bias", "consistency"]
    labels = ["Relevance", "Quality", "Bias", "Consistency"]
    n = len(dimensions)

    # Compute angles for radar
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]  # Close the polygon

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    for i, result in enumerate(results):
        values = [result[d] for d in dimensions]
        values += values[:1]  # Close the polygon

        color = ACCENT_COLORS[i % len(ACCENT_COLORS)]
        ax.plot(angles, values, "o-", linewidth=2.5, label=result["model"], color=color)
        ax.fill(angles, values, alpha=0.15, color=color)

    # Customise
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=13, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=9)
    ax.yaxis.grid(True, color=GRID_COLOR, alpha=0.4)
    ax.xaxis.grid(True, color=GRID_COLOR, alpha=0.4)
    ax.spines["polar"].set_color(GRID_COLOR)

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.15),
        fontsize=12,
        framealpha=0.8,
        facecolor=CARD_COLOR,
        edgecolor=GRID_COLOR,
    )

    plt.title(
        "Model Comparison — Evaluation Dimensions",
        fontsize=16, fontweight="bold", pad=25, color=TEXT_COLOR,
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close()
    print(f"  ✓ Radar chart saved: {output_path}")


# ─────────────────────────────────────────────────────────────────────────
# 2. Bar Chart — Final Rankings
# ─────────────────────────────────────────────────────────────────────────

def plot_ranking_bar_chart(results: list[dict], output_path: str = "charts/ranking_bar.png"):
    """
    Create a horizontal bar chart of final model rankings.
    """
    sorted_results = sorted(results, key=lambda x: x["final_score"])
    models = [r["model"] for r in sorted_results]
    scores = [r["final_score"] for r in sorted_results]

    fig, ax = plt.subplots(figsize=(10, max(4, len(models) * 1.2)))

    colors = [ACCENT_COLORS[i % len(ACCENT_COLORS)] for i in range(len(models))]
    bars = ax.barh(models, scores, color=list(reversed(colors)), height=0.6, edgecolor="none")

    # Add score labels on bars
    for bar, score in zip(bars, scores):
        ax.text(
            bar.get_width() - 0.02, bar.get_y() + bar.get_height() / 2,
            f"{score:.4f}",
            ha="right", va="center", fontsize=12, fontweight="bold", color=BG_COLOR,
        )

    ax.set_xlim(0, 1.05)
    ax.set_xlabel("Final Score", fontsize=13, fontweight="bold")
    ax.set_title(
        "Model Ranking — Final Evaluation Scores",
        fontsize=16, fontweight="bold", pad=15,
    )
    ax.tick_params(axis="y", labelsize=13)
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    ax.grid(axis="x", alpha=0.2)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close()
    print(f"  ✓ Ranking bar chart saved: {output_path}")


# ─────────────────────────────────────────────────────────────────────────
# 3. Stacked Dimension Breakdown
# ─────────────────────────────────────────────────────────────────────────

def plot_dimension_breakdown(results: list[dict], output_path: str = "charts/dimension_breakdown.png"):
    """
    Create a stacked bar chart showing weighted contribution of each dimension.
    """
    dimensions = ["relevance", "quality", "bias", "consistency"]
    weights = {"relevance": 0.35, "quality": 0.25, "bias": 0.25, "consistency": 0.15}
    dim_colors = {
        "relevance": "#00d4aa",
        "quality": "#ffd93d",
        "bias": "#ff6b6b",
        "consistency": "#6bcbff",
    }

    sorted_results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    models = [r["model"] for r in sorted_results]

    fig, ax = plt.subplots(figsize=(10, max(4, len(models) * 1.2)))

    bottom = np.zeros(len(models))
    for dim in dimensions:
        values = [r[dim] * weights[dim] for r in sorted_results]
        ax.barh(
            models, values, left=bottom,
            label=f"{dim.capitalize()} ({weights[dim]:.0%})",
            color=dim_colors[dim], edgecolor="none", height=0.6,
        )
        bottom += values

    ax.set_xlim(0, 1.05)
    ax.set_xlabel("Weighted Score Contribution", fontsize=13, fontweight="bold")
    ax.set_title(
        "Score Breakdown — Weighted Dimension Contributions",
        fontsize=16, fontweight="bold", pad=15,
    )
    ax.legend(
        loc="lower right", fontsize=10,
        facecolor=CARD_COLOR, edgecolor=GRID_COLOR, framealpha=0.9,
    )
    ax.tick_params(axis="y", labelsize=13)
    ax.grid(axis="x", alpha=0.2)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close()
    print(f"  ✓ Dimension breakdown saved: {output_path}")


# ─────────────────────────────────────────────────────────────────────────
# 4. Weight Comparison (Manual vs Learned)
# ─────────────────────────────────────────────────────────────────────────

def plot_weight_comparison(output_path: str = "charts/weight_comparison.png"):
    """
    Compare manual vs learned weights side-by-side.
    """
    weights_path = os.path.join("models", "learned_weights.json")
    if not os.path.exists(weights_path):
        print("  ⚠ Skipping weight comparison (no learned weights found)")
        return

    with open(weights_path, "r") as f:
        data = json.load(f)

    learned = data["weights"]
    manual = {"relevance": 0.35, "quality": 0.25, "bias": 0.25, "consistency": 0.15}
    dimensions = list(manual.keys())

    x = np.arange(len(dimensions))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(x - width / 2, [manual[d] for d in dimensions], width,
                   label="Manual Weights", color="#ff6b6b", edgecolor="none", alpha=0.9)
    bars2 = ax.bar(x + width / 2, [learned[d] for d in dimensions], width,
                   label="Learned Weights", color="#00d4aa", edgecolor="none", alpha=0.9)

    # Add value labels
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{bar.get_height():.1%}", ha="center", fontsize=10, fontweight="bold")
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{bar.get_height():.1%}", ha="center", fontsize=10, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([d.capitalize() for d in dimensions], fontsize=13, fontweight="bold")
    ax.set_ylabel("Weight", fontsize=13, fontweight="bold")
    ax.set_ylim(0, 0.55)
    ax.set_title(
        "Weight Comparison — Manual vs Learned (Ridge Regression)",
        fontsize=16, fontweight="bold", pad=15,
    )
    ax.legend(fontsize=12, facecolor=CARD_COLOR, edgecolor=GRID_COLOR)
    ax.grid(axis="y", alpha=0.2)

    # Add R² annotation
    r2 = data.get("metrics", {}).get("cv_r2_mean", None)
    if r2:
        ax.text(
            0.98, 0.95, f"Model R² = {r2:.4f}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=11, fontstyle="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=CARD_COLOR, edgecolor=GRID_COLOR),
        )

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close()
    print(f"  ✓ Weight comparison saved: {output_path}")


# ─────────────────────────────────────────────────────────────────────────
# 5. Benchmark Heatmap
# ─────────────────────────────────────────────────────────────────────────

def plot_benchmark_heatmap(csv_path: str, output_path: str = "charts/benchmark_heatmap.png"):
    """
    Create a heatmap of final scores: prompts (rows) × models (columns).
    """
    df = pd.read_csv(csv_path)

    # Create pivot table
    pivot = df.pivot_table(index="prompt", columns="model", values="final_score")

    # Shorten prompt labels
    short_prompts = [p[:50] + "..." if len(p) > 50 else p for p in pivot.index]

    fig, ax = plt.subplots(figsize=(10, max(6, len(pivot) * 0.6)))

    # Create heatmap manually
    data = pivot.values
    im = ax.imshow(data, cmap="RdYlGn", aspect="auto", vmin=0.4, vmax=1.0)

    # Ticks
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, fontsize=12, fontweight="bold")
    ax.set_yticks(range(len(short_prompts)))
    ax.set_yticklabels(short_prompts, fontsize=10)

    # Add score text in cells
    for i in range(len(short_prompts)):
        for j in range(len(pivot.columns)):
            val = data[i, j]
            text_color = BG_COLOR if val > 0.65 else TEXT_COLOR
            ax.text(j, i, f"{val:.3f}", ha="center", va="center",
                    fontsize=10, fontweight="bold", color=text_color)

    ax.set_title(
        "Benchmark Heatmap — Final Scores per Prompt × Model",
        fontsize=16, fontweight="bold", pad=15,
    )

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label("Final Score", fontsize=12)
    cbar.ax.tick_params(colors=TEXT_COLOR)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close()
    print(f"  ✓ Benchmark heatmap saved: {output_path}")


# ─────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────

def generate_all_charts(results: list[dict] | None = None, benchmark_csv: str | None = None):
    """Generate all available charts."""
    print("\n📊 Generating charts...\n")

    if results:
        plot_radar_chart(results)
        plot_ranking_bar_chart(results)
        plot_dimension_breakdown(results)

    plot_weight_comparison()

    if benchmark_csv and os.path.exists(benchmark_csv):
        plot_benchmark_heatmap(benchmark_csv)

    print("\n✅ All charts saved to charts/ directory\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate evaluation visualisations")
    parser.add_argument(
        "--benchmark",
        type=str,
        default=None,
        help="Path to benchmark results CSV for heatmap.",
    )
    args = parser.parse_args()

    # Default results for charting (from a typical single-prompt run)
    default_results = [
        {"model": "GPT-4", "relevance": 0.674, "quality": 0.872, "bias": 0.999, "consistency": 0.750, "final_score": 0.816},
        {"model": "Llama-3", "relevance": 0.633, "quality": 0.621, "bias": 0.996, "consistency": 0.750, "final_score": 0.738},
        {"model": "Mistral-7B", "relevance": 0.651, "quality": 0.839, "bias": 0.998, "consistency": 0.176, "final_score": 0.714},
    ]

    # Find most recent benchmark CSV if not specified
    benchmark_csv = args.benchmark
    if not benchmark_csv:
        results_dir = "results"
        if os.path.exists(results_dir):
            bench_files = sorted([
                f for f in os.listdir(results_dir) if f.startswith("benchmark_")
            ])
            if bench_files:
                benchmark_csv = os.path.join(results_dir, bench_files[-1])

    generate_all_charts(results=default_results, benchmark_csv=benchmark_csv)
