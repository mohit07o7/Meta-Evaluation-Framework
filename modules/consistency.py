"""
Consistency Analyzer Module
============================
Uses a Natural Language Inference (NLI) model (DeBERTa-v3-small) to detect
logical contradictions in AI model responses.

Two dimensions are evaluated:
  1. Internal consistency — does the response contradict itself?
  2. Cross-model consistency — does this response contradict other models' responses?

NLI labels:
  - entailment  → logically consistent
  - neutral     → independent / no clear logical relationship
  - contradiction → logically inconsistent

The contradiction probability is used as a penalty.
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re


class ConsistencyAnalyzer:

    def __init__(self):
        model_name = "cross-encoder/nli-deberta-v3-small"

        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        # NLI label mapping for this model:
        # 0 → contradiction, 1 → entailment, 2 → neutral
        self.contradiction_idx = 0

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences using basic punctuation rules."""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        # Filter out very short fragments
        return [s.strip() for s in sentences if len(s.strip()) > 10]

    def _get_contradiction_score(self, premise: str, hypothesis: str) -> float:
        """
        Compute the contradiction probability between two text segments.
        Returns a value between 0 (no contradiction) and 1 (strong contradiction).
        """
        inputs = self.tokenizer(
            premise, hypothesis,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)

        contradiction_prob = probs[0][self.contradiction_idx].item()
        return contradiction_prob

    def compute_internal_consistency(self, response: str) -> float:
        """
        Check if the response contradicts itself internally.
        Compares all pairs of sentences within the response.

        Returns a score between 0 and 1, where:
          1.0 = perfectly consistent (no internal contradictions)
          0.0 = highly contradictory
        """
        sentences = self._split_sentences(response)

        if len(sentences) < 2:
            # Cannot check internal consistency with fewer than 2 sentences
            return 1.0

        contradiction_scores = []
        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                score = self._get_contradiction_score(sentences[i], sentences[j])
                contradiction_scores.append(score)

        if not contradiction_scores:
            return 1.0

        # Average contradiction across all pairs; invert so higher = more consistent
        avg_contradiction = sum(contradiction_scores) / len(contradiction_scores)
        return 1.0 - avg_contradiction

    def compute_cross_model_consistency(
        self, response: str, other_responses: list[str]
    ) -> float:
        """
        Check if the response contradicts what other models said.
        Compares this response against each other model's response.

        Returns a score between 0 and 1, where:
          1.0 = consistent with other models
          0.0 = contradicts other models
        """
        if not other_responses:
            return 1.0

        contradiction_scores = []
        for other in other_responses:
            score = self._get_contradiction_score(response, other)
            contradiction_scores.append(score)

        avg_contradiction = sum(contradiction_scores) / len(contradiction_scores)
        return 1.0 - avg_contradiction

    def compute_score(
        self,
        response: str,
        other_responses: list[str] | None = None,
        internal_weight: float = 0.5,
        cross_weight: float = 0.5,
    ) -> dict:
        """
        Compute the overall consistency score.

        Args:
            response: The model's response text.
            other_responses: List of other models' responses (for cross-model check).
            internal_weight: Weight for internal consistency (default 0.5).
            cross_weight: Weight for cross-model consistency (default 0.5).

        Returns:
            Dictionary with internal, cross-model, and combined scores.
        """
        internal = self.compute_internal_consistency(response)

        if other_responses:
            cross = self.compute_cross_model_consistency(response, other_responses)
            combined = (internal_weight * internal) + (cross_weight * cross)
        else:
            cross = None
            combined = internal

        return {
            "internal": round(internal, 4),
            "cross_model": round(cross, 4) if cross is not None else None,
            "combined": round(combined, 4),
        }
