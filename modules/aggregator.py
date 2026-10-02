"""
Score Aggregator Module
========================
Computes the weighted final score across all evaluation dimensions.

Standard Mode (4 dimensions):
  - Relevance, Quality, Bias, Consistency

RAG Mode (6 dimensions, when context is provided):
  - Relevance, Quality, Bias, Consistency,
    Faithfulness, Answer Relevance

Supports two weight modes:
  1. Static weights (default): Manually-set weights
  2. Learned weights: Loaded from trained regression model

Each dimension returns a value between 0 and 1.
The weighted sum produces a composite score also between 0 and 1.
"""

import json
import os


class ScoreAggregator:

    # Default weights for standard mode (4 dimensions)
    DEFAULT_WEIGHTS = {
        "relevance":       0.35,
        "quality":         0.25,
        "bias":            0.25,
        "consistency":     0.15,
    }

    # Default weights for RAG mode (6 dimensions, must sum to 1)
    # Faithfulness and Answer Relevance are critical for RAG quality
    RAG_WEIGHTS = {
        "relevance":       0.15,
        "quality":         0.15,
        "bias":            0.10,
        "consistency":     0.10,
        "faithfulness":    0.35,   # Most important in RAG — hallucination prevention
        "answer_relevance": 0.15,  # Did it actually answer the question?
    }

    LEARNED_WEIGHTS_PATH = os.path.join("models", "learned_weights.json")

    def __init__(
        self,
        w_relevance: float | None = None,
        w_quality: float | None = None,
        w_bias: float | None = None,
        w_consistency: float | None = None,
        w_faithfulness: float | None = None,
        w_answer_relevance: float | None = None,
        use_learned: bool = False,
        weights_path: str | None = None,
    ):
        """
        Initialise the aggregator.

        Args:
            w_relevance:       Manual override for relevance weight.
            w_quality:         Manual override for quality weight.
            w_bias:            Manual override for bias weight.
            w_consistency:     Manual override for consistency weight.
            w_faithfulness:    Manual override for faithfulness weight (RAG).
            w_answer_relevance: Manual override for answer relevance weight (RAG).
            use_learned:       If True, load weights from trained model file.
            weights_path:      Custom path to learned_weights.json.
        """
        self.mode = "static"
        self._training_metrics: dict = {}
        self._trained_at: str = "N/A"

        if use_learned:
            path = weights_path or self.LEARNED_WEIGHTS_PATH
            self._load_learned_weights(path)
            # RAG dims fall back to static since the trained model only covers 4 dims
            self.w_faithfulness = w_faithfulness if w_faithfulness is not None else self.RAG_WEIGHTS["faithfulness"]
            self.w_answer_relevance = w_answer_relevance if w_answer_relevance is not None else self.RAG_WEIGHTS["answer_relevance"]
        else:
            self.w_relevance       = w_relevance       if w_relevance       is not None else self.DEFAULT_WEIGHTS["relevance"]
            self.w_quality         = w_quality         if w_quality         is not None else self.DEFAULT_WEIGHTS["quality"]
            self.w_bias            = w_bias            if w_bias            is not None else self.DEFAULT_WEIGHTS["bias"]
            self.w_consistency     = w_consistency     if w_consistency     is not None else self.DEFAULT_WEIGHTS["consistency"]
            self.w_faithfulness    = w_faithfulness    if w_faithfulness    is not None else self.RAG_WEIGHTS["faithfulness"]
            self.w_answer_relevance = w_answer_relevance if w_answer_relevance is not None else self.RAG_WEIGHTS["answer_relevance"]

    def _load_learned_weights(self, path: str):
        """Load weights from the trained regression model output."""
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Learned weights file not found at '{path}'. "
                f"Run 'python train_weights.py' first to train the model."
            )

        with open(path, "r") as f:
            data = json.load(f)

        weights = data["weights"]
        self.w_relevance   = weights["relevance"]
        self.w_quality     = weights["quality"]
        self.w_bias        = weights["bias"]
        self.w_consistency = weights["consistency"]
        self.mode = "learned"

        self._training_metrics = data.get("metrics", {})
        self._trained_at = data.get("trained_at", "unknown")

    def compute_final(
        self,
        relevance: float,
        quality: float,
        bias: float,
        consistency: float,
        faithfulness: float | None = None,
        answer_relevance: float | None = None,
    ) -> float:
        """
        Compute the weighted final score.

        Standard mode (no RAG context):
            Final = w_rel×Rel + w_qual×Qual + w_bias×Bias + w_cons×Cons

        RAG mode (faithfulness + answer_relevance provided):
            Final = w_rel×Rel + w_qual×Qual + w_bias×Bias + w_cons×Cons
                  + w_faith×Faith + w_ar×AnswerRel
            All 6 weights are renormalised to sum to 1.

        Args:
            relevance:        Relevance score (0–1)
            quality:          Quality score (0–1)
            bias:             Bias score (0–1)
            consistency:      Consistency score (0–1)
            faithfulness:     Faithfulness score (0–1), RAG only.
            answer_relevance: Answer relevance score (0–1), RAG only.

        Returns:
            Weighted composite score (0–1).
        """
        rag_mode = faithfulness is not None and answer_relevance is not None

        if rag_mode:
            # Use RAG weight distribution
            raw = (
                self.RAG_WEIGHTS["relevance"]        * relevance
                + self.RAG_WEIGHTS["quality"]        * quality
                + self.RAG_WEIGHTS["bias"]           * bias
                + self.RAG_WEIGHTS["consistency"]    * consistency
                + self.RAG_WEIGHTS["faithfulness"]   * faithfulness         # type: ignore[operator]
                + self.RAG_WEIGHTS["answer_relevance"] * answer_relevance   # type: ignore[operator]
            )
            return round(raw, 4)

        # Standard 4-dimension mode
        return round(
            self.w_relevance   * relevance
            + self.w_quality   * quality
            + self.w_bias      * bias
            + self.w_consistency * consistency,
            4,
        )

    def get_weights(self, rag_mode: bool = False) -> dict:
        """Return the current weight configuration."""
        if rag_mode:
            return dict(self.RAG_WEIGHTS)
        return {
            "relevance":   self.w_relevance,
            "quality":     self.w_quality,
            "bias":        self.w_bias,
            "consistency": self.w_consistency,
        }

    def get_mode(self) -> str:
        """Return whether using 'static' or 'learned' weights."""
        return self.mode

    def get_training_info(self) -> dict | None:
        """Return training metadata if using learned weights."""
        if self.mode != "learned":
            return None
        return {
            "metrics":    getattr(self, "_training_metrics", {}),
            "trained_at": getattr(self, "_trained_at", "unknown"),
        }