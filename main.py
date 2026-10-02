"""
Meta-Evaluation Framework
===========================
A pipeline that takes a prompt and multiple AI model responses, runs them
through four (or six in RAG mode) evaluation modules, and produces a
ranked comparison with explainable scores.

Standard Evaluation Dimensions (4):
  1. Relevance       (35%) — Semantic similarity via all-MiniLM-L6-v2
  2. Quality         (25%) — Rule-based + JSON/Markdown structure analysis
  3. Bias            (25%) — Toxicity detection via toxic-bert
  4. Consistency     (15%) — NLI contradiction detection via DeBERTa-v3-small

RAG Mode (add --context, 6 dimensions):
  5. Faithfulness    (35%) — Hallucination detection via DeBERTa NLI
  6. Answer Relevance(15%) — Did the response answer the prompt, not echo context?

Usage:
    python main.py
    python main.py --use-learned-weights
    python main.py --context "The Eiffel Tower is 330m tall and located in Paris."
"""

import argparse
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
from modules.faithfulness import FaithfulnessChecker
from modules.answer_relevance import AnswerRelevanceChecker


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
    """Colour-code a score: green ≥ 0.7, yellow ≥ 0.4, red < 0.4."""
    if score >= 0.7:
        return f"{GREEN}{score:.4f}{RESET}"
    elif score >= 0.4:
        return f"{YELLOW}{score:.4f}{RESET}"
    else:
        return f"{RED}{score:.4f}{RESET}"


def explain_score(dimension: str, score: float) -> str:
    """Generate a human-readable explanation for each dimension score."""
    explanations = {
        "relevance": {
            "high": "Response is highly relevant and semantically aligned with the prompt.",
            "mid": "Response is partially relevant but may drift from the core topic.",
            "low": "Response is largely off-topic or unrelated to the prompt.",
        },
        "quality": {
            "high": "Response is well-structured with adequate length and diverse vocabulary.",
            "mid": "Response is acceptable but could be more detailed or varied.",
            "low": "Response is too short, repetitive, or structurally poor.",
        },
        "bias": {
            "high": "Response is clean and free from toxic or biased content.",
            "mid": "Response may contain mildly problematic or borderline content.",
            "low": "Response contains toxic, harmful, or biased language.",
        },
        "consistency": {
            "high": "Response is logically consistent internally and with other models.",
            "mid": "Response has minor logical inconsistencies.",
            "low": "Response contains significant contradictions.",
        },
    }

    if score >= 0.7:
        level = "high"
    elif score >= 0.4:
        level = "mid"
    else:
        level = "low"

    return explanations.get(dimension, {}).get(level, "")


def print_banner():
    """Print a styled banner for the framework."""
    banner = f"""
{CYAN}{'═' * 65}
  ╔══════════════════════════════════════════════════════════════╗
  ║          META-EVALUATION FRAMEWORK  v1.0                    ║
  ║          AI Model Output Evaluation & Ranking               ║
  ╚══════════════════════════════════════════════════════════════╝
{'═' * 65}{RESET}
"""
    print(banner)


# ─────────────────────────────────────────────────────────────────────────
# Core evaluation pipeline
# ─────────────────────────────────────────────────────────────────────────

def evaluate(
    prompt: str,
    responses: dict[str, str],
    context: str | None = None,
    use_learned_weights: bool = False,
) -> list[dict]:
    """
    Run the full meta-evaluation pipeline.

    Args:
        prompt: The original user prompt.
        responses: Dictionary mapping model names to their response strings.
        context: Optional RAG context. When provided, enables faithfulness
                 and answer relevance scoring (RAG mode).
        use_learned_weights: If True, load weights from trained model.

    Returns:
        A sorted list of result dictionaries (best model first).
    """
    rag_mode = bool(context and context.strip())

    # ── Initialise evaluation modules ──
    print(f"\n{DIM}Loading evaluation models...{RESET}")
    t0 = time.time()

    relevance    = RelevanceAnalyzer()
    quality      = QualityAnalyzer()
    bias         = BiasDetector()
    consistency  = ConsistencyAnalyzer()
    aggregator   = ScoreAggregator(use_learned=use_learned_weights)

    if rag_mode:
        # Reuse the DeBERTa model instance already loaded by ConsistencyAnalyzer
        faithfulness     = FaithfulnessChecker(
            shared_model=consistency.model,
            shared_tokenizer=consistency.tokenizer,
        )
        answer_relevance = AnswerRelevanceChecker(
            shared_model=relevance.model,
        )

    load_time = time.time() - t0
    print(f"{DIM}Models loaded in {load_time:.1f}s{RESET}\n")

    # Print mode and weight configuration
    if rag_mode:
        print(f"{BOLD}Mode: {CYAN}RAG Evaluation (6 dimensions){RESET}")
        print(f"{DIM}Context: \"{context[:100]}...\" {RESET}" if context and len(context) > 100 else f"{DIM}Context: \"{context}\"{RESET}")
    else:
        mode = aggregator.get_mode()
        mode_label = f"{GREEN}LEARNED{RESET}" if mode == "learned" else f"{YELLOW}STATIC (manual){RESET}"
        print(f"{BOLD}Mode: Standard | Weights: {mode_label}{RESET}")
        if mode == "learned":
            info = aggregator.get_training_info()
            if info and info.get("metrics"):
                r2 = info["metrics"].get("cv_r2_mean", "N/A")
                print(f"{DIM}  Trained model R²: {r2:.4f} | Trained at: {info.get('trained_at', 'N/A')}{RESET}")

    weights = aggregator.get_weights(rag_mode=rag_mode)
    print(f"{BOLD}Weight Configuration:{RESET}")
    for dim, w in weights.items():
        print(f"  {dim.replace('_',' ').capitalize():>20s} : {w:.1%}")
    print()

    # ── Evaluate each model ──
    results = []
    model_names = list(responses.keys())

    for model_name, response in responses.items():

        print(f"{BOLD}{'─' * 60}{RESET}")
        print(f"{BOLD}Evaluating: {CYAN}{model_name}{RESET}")
        print(f"{DIM}Response preview: \"{response[:80]}...\" {RESET}" if len(response) > 80 else f"{DIM}Response: \"{response}\"{RESET}")
        print()

        # 1. Relevance
        r_score = relevance.compute_score(prompt, response)
        print(f"  Relevance      : {color_score(r_score)}  — {explain_score('relevance', r_score)}")

        # 2. Quality
        q_score = quality.compute_score(response)
        print(f"  Quality        : {color_score(q_score)}  — {explain_score('quality', q_score)}")

        # 3. Bias
        b_score = bias.compute_score(response)
        print(f"  Bias           : {color_score(b_score)}  — {explain_score('bias', b_score)}")

        # 4. Consistency
        other_responses = [responses[m] for m in model_names if m != model_name]
        c_result = consistency.compute_score(response, other_responses)
        c_score = c_result["combined"]
        consistency_detail = (
            f"internal={c_result['internal']}"
            + (f", cross-model={c_result['cross_model']}" if c_result["cross_model"] is not None else "")
        )
        print(f"  Consistency    : {color_score(c_score)}  — {explain_score('consistency', c_score)}")
        print(f"  {DIM}({consistency_detail}){RESET}")

        f_score = None
        ar_score = None

        if rag_mode:
            # 5. Faithfulness (hallucination detection)
            f_result = faithfulness.compute_score(context, response)  # type: ignore[possibly-undefined]
            f_score = f_result["score"]
            if f_score is not None:
                hallucinated = f_result["hallucinated"]
                total = f_result["total_claims"]
                print(f"  Faithfulness   : {color_score(f_score)}  — {hallucinated}/{total} claims unsupported by context")
            else:
                print(f"  Faithfulness   : {DIM}N/A{RESET}  — {f_result.get('note', '')}")
                f_score = 1.0  # fallback

            # 6. Answer Relevance
            ar_result = answer_relevance.compute_score(prompt, response, context)  # type: ignore[possibly-undefined]
            ar_score = ar_result["score"]
            echo_flag = f" {YELLOW}[context echo detected]{RESET}" if ar_result["is_context_echo"] else ""
            print(f"  Answer Relevance: {color_score(ar_score)}  — prompt_sim={ar_result['prompt_similarity']}, context_sim={ar_result['context_similarity']}{echo_flag}")

        # Final score
        final_score = aggregator.compute_final(
            r_score, q_score, b_score, c_score,
            faithfulness=f_score,
            answer_relevance=ar_score,
        )
        print(f"\n  {BOLD}Final Score    : {color_score(final_score)}{RESET}")
        print()

        result = {
            "model":                    model_name,
            "relevance":               round(r_score, 4),
            "quality":                 round(q_score, 4),
            "bias":                    round(b_score, 4),
            "consistency":             round(c_score, 4),
            "consistency_internal":    c_result["internal"],
            "consistency_cross_model": c_result["cross_model"],
            "final_score":             round(final_score, 4),
        }
        if rag_mode:
            result["faithfulness"]     = round(f_score, 4) if f_score is not None else None
            result["answer_relevance"] = round(ar_score, 4) if ar_score is not None else None

        results.append(result)

    # Sort by final score (best first)
    results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    return results


def print_ranking(results: list[dict]):
    """Print the final ranking table."""
    print(f"\n{CYAN}{'═' * 65}{RESET}")
    print(f"{BOLD}{CYAN}  FINAL RANKING{RESET}")
    print(f"{CYAN}{'═' * 65}{RESET}\n")

    medals = ["🥇", "🥈", "🥉"]

    rag_mode = "faithfulness" in results[0] if results else False

    for i, r in enumerate(results):
        medal = medals[i] if i < len(medals) else f"  {i + 1}."
        bar_length = int(r["final_score"] * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)

        print(f"  {medal} {BOLD}{r['model']:<15s}{RESET}  {color_score(r['final_score'])}  [{bar}]")
        print(f"       Rel={r['relevance']:.3f}  Qual={r['quality']:.3f}  Bias={r['bias']:.3f}  Cons={r['consistency']:.3f}")
        if rag_mode:
            faith = r.get('faithfulness', 'N/A')
            ar    = r.get('answer_relevance', 'N/A')
            print(f"       Faith={faith}  AnswerRel={ar}")
        print()


def export_results(results: list[dict], prompt: str, output_dir: str = "results"):
    """Export results to CSV file with timestamp."""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"evaluation_{timestamp}.csv")

    df = pd.DataFrame(results)
    df.insert(0, "rank", range(1, len(df) + 1))
    df.insert(1, "prompt", prompt)

    df.to_csv(filename, index=False)
    print(f"\n{DIM}Results exported to: {filename}{RESET}")

    return filename


# ─────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Meta-Evaluation Framework")
    parser.add_argument(
        "--use-learned-weights",
        action="store_true",
        help="Use weights learned from labeled data instead of manual weights.",
    )
    parser.add_argument(
        "--context",
        type=str,
        default=None,
        help="RAG context string. When provided, enables faithfulness and answer relevance scoring.",
    )
    args = parser.parse_args()

    print_banner()

    # ── Define the evaluation scenario ──
    prompt = "Explain machine learning in simple terms."

    responses = {
        "GPT-4": (
            "Machine learning is a branch of artificial intelligence where "
            "computers learn patterns from data instead of being explicitly "
            "programmed. For example, a spam filter learns to identify junk "
            "emails by analyzing thousands of examples. The system improves "
            "its accuracy over time as it processes more data, making "
            "predictions and decisions without human intervention."
        ),
        "Llama-3": (
            "ML is computer learn data computer learn data computer. "
            "Machine learning data computer learning."
        ),
        "Mistral-7B": (
            "Machine learning is a fascinating technology that has many "
            "applications. It allows systems to learn and improve from "
            "experience. However, machine learning is completely useless "
            "and does not work at all in practice."
        ),
    }

    print(f"{BOLD}Prompt:{RESET} \"{prompt}\"\n")
    print(f"{BOLD}Models under evaluation:{RESET} {', '.join(responses.keys())}\n")

    if args.context:
        print(f"{BOLD}RAG Context:{RESET} \"{args.context[:120]}\"\n")

    # ── Run evaluation pipeline ──
    ranked_results = evaluate(
        prompt, responses,
        context=args.context,
        use_learned_weights=args.use_learned_weights,
    )

    # ── Display ranking ──
    print_ranking(ranked_results)

    # ── Export to CSV ──
    csv_path = export_results(ranked_results, prompt)

    # ── Summary ──
    best = ranked_results[0]
    worst = ranked_results[-1]
    print(f"\n{BOLD}Summary:{RESET}")
    print(f"  Best model  : {GREEN}{best['model']}{RESET} (score: {best['final_score']:.4f})")
    print(f"  Worst model : {RED}{worst['model']}{RESET} (score: {worst['final_score']:.4f})")
    print(f"  Score gap   : {best['final_score'] - worst['final_score']:.4f}")
    print()