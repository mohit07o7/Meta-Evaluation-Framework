"""
Batch Processing Pipeline
===========================
Processes evaluation datasets (CSV/JSON) with concurrent execution,
generating statistical reports and analytics.

Supports:
  - CSV/JSON ingestion with columns: prompt, model, response [, context]
  - Multi-threaded processing via concurrent.futures
  - Full 4-dimension or 6-dimension (RAG) evaluation per row
  - Statistical summary + detailed results export

Usage:
    python batch_runner.py --file data/batch_sample.csv
    python batch_runner.py --file data/batch_sample.csv --workers 4
    python batch_runner.py --file data/batch_rag.json --rag
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import pandas as pd
import numpy as np

from modules.relevance import RelevanceAnalyzer
from modules.quality import QualityAnalyzer
from modules.bias import BiasDetector
from modules.consistency import ConsistencyAnalyzer
from modules.aggregator import ScoreAggregator
from modules.faithfulness import FaithfulnessChecker
from modules.answer_relevance import AnswerRelevanceChecker


# ─────────────────────────────────────────────────────────────────────────
# Display helpers
# ─────────────────────────────────────────────────────────────────────────

BOLD   = "\033[1m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
DIM    = "\033[2m"


def print_banner():
    banner = f"""
{CYAN}{'═' * 65}
  ╔══════════════════════════════════════════════════════════════╗
  ║       BATCH PROCESSING PIPELINE                             ║
  ║       Process N prompts × M models with full evaluation     ║
  ╚══════════════════════════════════════════════════════════════╝
{'═' * 65}{RESET}
"""
    print(banner)


# ─────────────────────────────────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────────────────────────────────

def load_batch_file(filepath: str) -> pd.DataFrame:
    """
    Load a batch dataset from CSV or JSON.

    Expected columns:
      - prompt (required)
      - model  (required)
      - response (required)
      - context (optional — enables RAG mode per row)
    """
    if not os.path.exists(filepath):
        print(f"{RED}Error: File not found: {filepath}{RESET}")
        sys.exit(1)

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(filepath)
    elif ext == ".json":
        df = pd.read_json(filepath)
    else:
        print(f"{RED}Error: Unsupported format '{ext}'. Use .csv or .json{RESET}")
        sys.exit(1)

    # Validate required columns
    required = ["prompt", "model", "response"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"{RED}Error: Missing required columns: {missing}{RESET}")
        print(f"{DIM}Expected columns: prompt, model, response [, context]{RESET}")
        sys.exit(1)

    return df


# ─────────────────────────────────────────────────────────────────────────
# Evaluation engine
# ─────────────────────────────────────────────────────────────────────────

class BatchEvaluator:
    """
    Evaluates a batch of (prompt, model, response) rows using
    shared model instances and optional concurrency.
    """

    def __init__(self, rag_enabled: bool = False, use_learned: bool = False):
        print(f"{DIM}Loading evaluation models...{RESET}")
        t0 = time.time()

        self.relevance   = RelevanceAnalyzer()
        self.quality     = QualityAnalyzer()
        self.bias        = BiasDetector()
        self.consistency = ConsistencyAnalyzer()
        self.aggregator  = ScoreAggregator(use_learned=use_learned)

        self.rag_enabled = rag_enabled
        self.faithfulness     = None
        self.answer_relevance = None

        if rag_enabled:
            self.faithfulness = FaithfulnessChecker(
                shared_model=self.consistency.model,
                shared_tokenizer=self.consistency.tokenizer,
            )
            self.answer_relevance = AnswerRelevanceChecker(
                shared_model=self.relevance.model,
            )

        elapsed = time.time() - t0
        print(f"{DIM}Models loaded in {elapsed:.1f}s{RESET}\n")

    def evaluate_row(self, row: dict, all_responses: list[str] | None = None) -> dict:
        """
        Evaluate a single row (prompt, model, response, [context]).

        Args:
            row: Dict with prompt, model, response keys.
            all_responses: Other model responses for the same prompt (for cross-model consistency).

        Returns:
            Dict with all dimension scores.
        """
        prompt   = str(row["prompt"])
        model    = str(row["model"])
        response = str(row["response"])
        context  = str(row.get("context", "")) if row.get("context") else None

        r_score = self.relevance.compute_score(prompt, response)
        q_score = self.quality.compute_score(response)
        b_score = self.bias.compute_score(response)

        other = [r for r in (all_responses or []) if r != response]
        c_result = self.consistency.compute_score(response, other if other else None)
        c_score  = c_result["combined"]

        f_score  = None
        ar_score = None

        if self.rag_enabled and context and context.strip():
            f_result = self.faithfulness.compute_score(context, response)
            f_score = f_result["score"] if f_result["score"] is not None else 1.0

            ar_result = self.answer_relevance.compute_score(prompt, response, context)
            ar_score = ar_result["score"]

        final = self.aggregator.compute_final(
            r_score, q_score, b_score, c_score,
            faithfulness=f_score,
            answer_relevance=ar_score,
        )

        result = {
            "prompt":      prompt,
            "model":       model,
            "relevance":   round(r_score, 4),
            "quality":     round(q_score, 4),
            "bias":        round(b_score, 4),
            "consistency": round(c_score, 4),
            "final_score": round(final, 4),
        }
        if f_score is not None:
            result["faithfulness"]     = round(f_score, 4)
        if ar_score is not None:
            result["answer_relevance"] = round(ar_score, 4)

        return result


def run_batch(
    df: pd.DataFrame,
    evaluator: BatchEvaluator,
    max_workers: int = 2,
) -> pd.DataFrame:
    """
    Process all rows in the batch dataset.

    Groups rows by prompt to enable cross-model consistency checks,
    then processes groups concurrently.
    """
    total_rows = len(df)
    print(f"{BOLD}Processing {total_rows} rows ({df['model'].nunique()} models, "
          f"{df['prompt'].nunique()} prompts)...{RESET}\n")

    all_results = []
    grouped = df.groupby("prompt")
    completed = 0

    def process_group(prompt_text, group_df):
        """Evaluate all models for a single prompt."""
        group_results = []
        all_responses = group_df["response"].tolist()

        for _, row in group_df.iterrows():
            result = evaluator.evaluate_row(row.to_dict(), all_responses)
            group_results.append(result)

        return group_results

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for prompt_text, group_df in grouped:
            future = executor.submit(process_group, prompt_text, group_df)
            futures[future] = prompt_text

        for future in as_completed(futures):
            prompt_text = futures[future]
            try:
                group_results = future.result()
                all_results.extend(group_results)
                completed += len(group_results)

                pct = completed / total_rows
                bar_len = int(pct * 30)
                bar = "█" * bar_len + "░" * (30 - bar_len)
                print(f"\r  [{bar}] {completed}/{total_rows} rows ({pct:.0%})", end="", flush=True)
            except Exception as e:
                print(f"\n{RED}Error processing prompt '{prompt_text[:50]}...': {e}{RESET}")

    print("\n")
    return pd.DataFrame(all_results)


# ─────────────────────────────────────────────────────────────────────────
# Statistics and reporting
# ─────────────────────────────────────────────────────────────────────────

def print_statistics(results_df: pd.DataFrame):
    """Print detailed statistical summary of batch results."""
    score_cols = ["relevance", "quality", "bias", "consistency", "final_score"]
    rag_cols = ["faithfulness", "answer_relevance"]

    # Add RAG cols if present
    for col in rag_cols:
        if col in results_df.columns:
            score_cols.append(col)

    print(f"\n{CYAN}{'═' * 65}{RESET}")
    print(f"{BOLD}{CYAN}  BATCH EVALUATION STATISTICS{RESET}")
    print(f"{CYAN}{'═' * 65}{RESET}\n")

    # Overall statistics
    print(f"{BOLD}Overall Statistics:{RESET}")
    stats = results_df[score_cols].describe().T[["mean", "std", "min", "max"]]
    stats.columns = ["Mean", "Std", "Min", "Max"]
    for col in stats.columns:
        stats[col] = stats[col].map(lambda x: f"{x:.4f}")
    print(stats.to_string())
    print()

    # Per-model rankings
    print(f"{BOLD}Per-Model Average Scores:{RESET}")
    model_means = results_df.groupby("model")[score_cols].mean()
    model_means = model_means.sort_values("final_score", ascending=False)

    medals = ["🥇", "🥈", "🥉"]
    for i, (model, scores) in enumerate(model_means.iterrows()):
        medal = medals[i] if i < len(medals) else f"  {i+1}."
        bar_len = int(scores["final_score"] * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        color = GREEN if scores["final_score"] >= 0.7 else YELLOW if scores["final_score"] >= 0.4 else RED
        print(f"  {medal} {str(model):<15s}  {color}{scores['final_score']:.4f}{RESET}  [{bar}]")
        details = "  ".join([f"{c[:4]}={scores[c]:.3f}" for c in score_cols if c != "final_score"])
        print(f"       {DIM}{details}{RESET}")
    print()

    # Worst prompts (where models disagree most)
    if results_df["prompt"].nunique() > 1:
        std_by_prompt = results_df.groupby("prompt")["final_score"].std().sort_values(ascending=False)
        print(f"{BOLD}Most Controversial Prompts (highest score variance):{RESET}")
        for prompt_text, std in std_by_prompt.head(5).items():
            print(f"  σ={std:.4f}  \"{str(prompt_text)[:80]}\"")
        print()


def export_batch_results(results_df: pd.DataFrame, output_dir: str = "results") -> str:
    """Save batch results to CSV with timestamp."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"batch_{timestamp}.csv")
    results_df.to_csv(filepath, index=False)
    print(f"{GREEN}✓ Results saved to: {filepath}{RESET}")
    return filepath


# ─────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Evaluation Pipeline")
    parser.add_argument(
        "--file", type=str, required=True,
        help="Path to CSV or JSON batch file (columns: prompt, model, response [, context])",
    )
    parser.add_argument(
        "--workers", type=int, default=2,
        help="Number of concurrent workers (default: 2)",
    )
    parser.add_argument(
        "--rag", action="store_true",
        help="Enable RAG evaluation (requires 'context' column in dataset)",
    )
    parser.add_argument(
        "--use-learned-weights", action="store_true",
        help="Use trained weights instead of static weights.",
    )
    args = parser.parse_args()

    print_banner()

    # Load data
    df = load_batch_file(args.file)
    print(f"{BOLD}Dataset:{RESET} {args.file}")
    print(f"  Rows: {len(df)} | Models: {df['model'].nunique()} | Prompts: {df['prompt'].nunique()}")
    has_context = "context" in df.columns and df["context"].notna().any()
    rag = args.rag or has_context
    if rag:
        print(f"  {CYAN}RAG mode: enabled (context column detected){RESET}")
    print()

    # Init evaluator
    evaluator = BatchEvaluator(rag_enabled=rag, use_learned=args.use_learned_weights)

    # Run batch
    t0 = time.time()
    results_df = run_batch(df, evaluator, max_workers=args.workers)
    elapsed = time.time() - t0

    # Statistics
    print_statistics(results_df)
    print(f"{DIM}Total processing time: {elapsed:.1f}s ({len(df)/elapsed:.1f} rows/sec){RESET}")

    # Export
    export_batch_results(results_df)
