"""
Benchmark Runner
==================
Runs the Meta-Evaluation Framework across a full benchmark dataset
(multiple prompts and model responses) and produces aggregate statistics.

This proves the framework generalises — not just works on one example.

Usage:
    python run_benchmark.py
    python run_benchmark.py --use-learned-weights
    python run_benchmark.py --dataset benchmarks/benchmark_prompts.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

import pandas as pd

from modules.relevance import RelevanceAnalyzer
from modules.quality import QualityAnalyzer
from modules.bias import BiasDetector
from modules.consistency import ConsistencyAnalyzer
from modules.aggregator import ScoreAggregator


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


def color_score(score: float) -> str:
    if score >= 0.7:
        return f"{GREEN}{score:.4f}{RESET}"
    elif score >= 0.4:
        return f"{YELLOW}{score:.4f}{RESET}"
    else:
        return f"{RED}{score:.4f}{RESET}"


def print_banner():
    banner = f"""
{CYAN}{'═' * 65}
  ╔══════════════════════════════════════════════════════════════╗
  ║          BENCHMARK RUNNER                                   ║
  ║          Multi-Prompt Evaluation Suite                       ║
  ╚══════════════════════════════════════════════════════════════╝
{'═' * 65}{RESET}
"""
    print(banner)


# ─────────────────────────────────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────────────────────────────────

def load_benchmark(filepath: str) -> list[dict]:
    """Load benchmark dataset from JSON file."""
    if not os.path.exists(filepath):
        print(f"{RED}Error: Benchmark file not found at '{filepath}'{RESET}")
        sys.exit(1)

    with open(filepath, "r") as f:
        data = json.load(f)

    print(f"{BOLD}Benchmark loaded:{RESET} {len(data)} prompts from '{filepath}'")
    return data


# ─────────────────────────────────────────────────────────────────────────
# Core benchmark logic
# ─────────────────────────────────────────────────────────────────────────

def run_benchmark(
    benchmark_data: list[dict],
    use_learned_weights: bool = False,
) -> pd.DataFrame:
    """
    Run the evaluation pipeline on the full benchmark dataset.

    Args:
        benchmark_data: List of benchmark entries with prompt and responses.
        use_learned_weights: Whether to use learned weights.

    Returns:
        DataFrame with all results.
    """
    # ── Load models once ──
    print(f"\n{DIM}Loading evaluation models (one-time)...{RESET}")
    t0 = time.time()

    relevance = RelevanceAnalyzer()
    quality = QualityAnalyzer()
    bias = BiasDetector()
    consistency = ConsistencyAnalyzer()
    aggregator = ScoreAggregator(use_learned=use_learned_weights)

    load_time = time.time() - t0
    print(f"{DIM}Models loaded in {load_time:.1f}s{RESET}")

    # Show weight config
    mode = aggregator.get_mode()
    mode_label = f"{GREEN}LEARNED{RESET}" if mode == "learned" else f"{YELLOW}STATIC{RESET}"
    weights = aggregator.get_weights()
    print(f"{BOLD}Weight Mode: {mode_label}{RESET}")
    print(f"{DIM}  Rel={weights['relevance']:.1%}  Qual={weights['quality']:.1%}  "
          f"Bias={weights['bias']:.1%}  Cons={weights['consistency']:.1%}{RESET}\n")

    # ── Evaluate all prompts ──
    all_results = []
    total = len(benchmark_data)

    for idx, entry in enumerate(benchmark_data, 1):
        prompt = entry["prompt"]
        responses = entry["responses"]
        bench_id = entry.get("id", f"bench_{idx:02d}")
        category = entry.get("category", "general")
        model_names = list(responses.keys())

        print(f"{BOLD}[{idx}/{total}]{RESET} {prompt[:60]}{'...' if len(prompt) > 60 else ''}")

        for model_name, response in responses.items():
            # 1. Relevance
            r_score = relevance.compute_score(prompt, response)

            # 2. Quality
            q_score = quality.compute_score(response)

            # 3. Bias
            b_score = bias.compute_score(response)

            # 4. Consistency
            other_responses = [responses[m] for m in model_names if m != model_name]
            c_result = consistency.compute_score(response, other_responses)
            c_score = c_result["combined"]

            # 5. Aggregate
            final_score = aggregator.compute_final(r_score, q_score, b_score, c_score)

            all_results.append({
                "benchmark_id": bench_id,
                "category": category,
                "prompt": prompt,
                "model": model_name,
                "relevance": round(r_score, 4),
                "quality": round(q_score, 4),
                "bias": round(b_score, 4),
                "consistency": round(c_score, 4),
                "consistency_internal": c_result["internal"],
                "consistency_cross_model": c_result["cross_model"],
                "final_score": round(final_score, 4),
            })

        # Show per-prompt ranking inline
        prompt_results = all_results[-len(responses):]
        prompt_results_sorted = sorted(prompt_results, key=lambda x: x["final_score"], reverse=True)
        rankings = "  →  ".join(
            f"{r['model']}={color_score(r['final_score'])}"
            for r in prompt_results_sorted
        )
        print(f"  {rankings}\n")

    df = pd.DataFrame(all_results)
    return df


def print_aggregate_stats(df: pd.DataFrame):
    """Print aggregate statistics across the full benchmark."""
    print(f"\n{CYAN}{'═' * 65}{RESET}")
    print(f"{BOLD}{CYAN}  AGGREGATE BENCHMARK RESULTS{RESET}")
    print(f"{CYAN}{'═' * 65}{RESET}\n")

    # ── Per-model averages ──
    model_stats = df.groupby("model").agg({
        "relevance": "mean",
        "quality": "mean",
        "bias": "mean",
        "consistency": "mean",
        "final_score": "mean",
    }).sort_values("final_score", ascending=False)

    print(f"{BOLD}Average Scores per Model (across {df['prompt'].nunique()} prompts):{RESET}\n")
    print(f"  {'Model':<15s}  {'Relevance':>10s}  {'Quality':>10s}  {'Bias':>10s}  {'Consistency':>10s}  {'Final':>10s}")
    print(f"  {'─' * 70}")

    medals = ["🥇", "🥈", "🥉"]
    for i, (model, row) in enumerate(model_stats.iterrows()):
        medal = medals[i] if i < len(medals) else "  "
        bar_len = int(row["final_score"] * 25)
        bar = "█" * bar_len + "░" * (25 - bar_len)
        print(
            f"  {medal} {model:<13s}"
            f"  {color_score(row['relevance']):>20s}"
            f"  {color_score(row['quality']):>20s}"
            f"  {color_score(row['bias']):>20s}"
            f"  {color_score(row['consistency']):>20s}"
            f"  {color_score(row['final_score']):>20s}"
            f"  [{bar}]"
        )
    print()

    # ── Win counts ──
    print(f"{BOLD}Win Count (how many prompts each model ranked #1):{RESET}\n")
    wins = {}
    for bench_id, group in df.groupby("benchmark_id"):
        best = group.loc[group["final_score"].idxmax(), "model"]
        wins[best] = wins.get(best, 0) + 1

    for model in model_stats.index:
        w = wins.get(model, 0)
        total = df["benchmark_id"].nunique()
        bar = "█" * w + "░" * (total - w)
        print(f"  {model:<15s}  {w:>2d}/{total}  [{bar}]")
    print()

    # ── Per-category breakdown ──
    if "category" in df.columns and df["category"].nunique() > 1:
        print(f"{BOLD}Average Final Score by Category:{RESET}\n")
        cat_stats = df.groupby(["category", "model"])["final_score"].mean().unstack()
        cat_stats = cat_stats[model_stats.index]  # order by overall ranking

        print(f"  {'Category':<15s}  ", end="")
        for model in cat_stats.columns:
            print(f"  {model:>12s}", end="")
        print()
        print(f"  {'─' * (15 + 14 * len(cat_stats.columns))}")

        for cat, row in cat_stats.iterrows():
            print(f"  {cat:<15s}  ", end="")
            for val in row:
                print(f"  {color_score(val):>22s}", end="")
            print()
        print()

    # ── Key findings ──
    print(f"{BOLD}Key Findings:{RESET}")
    best_model = model_stats.index[0]
    worst_model = model_stats.index[-1]
    gap = model_stats.loc[best_model, "final_score"] - model_stats.loc[worst_model, "final_score"]
    print(f"  • Best overall model  : {GREEN}{best_model}{RESET} (avg score: {model_stats.loc[best_model, 'final_score']:.4f})")
    print(f"  • Worst overall model : {RED}{worst_model}{RESET} (avg score: {model_stats.loc[worst_model, 'final_score']:.4f})")
    print(f"  • Score gap           : {gap:.4f}")

    # Find which dimension differentiates the most
    dim_spreads = {}
    for dim in ["relevance", "quality", "bias", "consistency"]:
        spread = model_stats[dim].max() - model_stats[dim].min()
        dim_spreads[dim] = spread
    most_diff = max(dim_spreads, key=dim_spreads.get)
    print(f"  • Most differentiating: {most_diff} (spread: {dim_spreads[most_diff]:.4f})")
    print()


def export_benchmark_results(df: pd.DataFrame, output_dir: str = "results") -> str:
    """Export full benchmark results to CSV."""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"benchmark_{timestamp}.csv")
    df.to_csv(filename, index=False)

    print(f"{GREEN}✓ Full results exported to: {filename}{RESET}")
    return filename


# ─────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Runner for Meta-Evaluation Framework")
    parser.add_argument(
        "--dataset",
        type=str,
        default="benchmarks/benchmark_prompts.json",
        help="Path to benchmark dataset JSON.",
    )
    parser.add_argument(
        "--use-learned-weights",
        action="store_true",
        help="Use learned weights instead of manual weights.",
    )
    args = parser.parse_args()

    print_banner()

    # Load benchmark data
    benchmark_data = load_benchmark(args.dataset)

    # Run the full benchmark
    t_start = time.time()
    results_df = run_benchmark(benchmark_data, use_learned_weights=args.use_learned_weights)
    total_time = time.time() - t_start

    # Print aggregate stats
    print_aggregate_stats(results_df)

    # Export
    csv_path = export_benchmark_results(results_df)

    print(f"{DIM}Total benchmark time: {total_time:.1f}s{RESET}")
    print()
