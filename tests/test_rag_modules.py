"""
Unit Tests for RAG Evaluation Modules
=======================================
Tests for FaithfulnessChecker and AnswerRelevanceChecker
without requiring real ML model loads (uses mocked outputs).

Run with:
    python -m pytest tests/test_rag_modules.py -v
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.answer_relevance import AnswerRelevanceChecker
from modules.faithfulness import FaithfulnessChecker
from modules.aggregator import ScoreAggregator


# =====================================================================
# Aggregator RAG mode tests (no ML needed)
# =====================================================================

class TestAggregatorRAGMode:
    """Test the extended aggregator with RAG dimensions."""

    def setup_method(self):
        self.agg = ScoreAggregator()

    def test_standard_mode_unchanged(self):
        """4-dim standard score should still work."""
        score = self.agg.compute_final(0.8, 0.7, 0.9, 0.6)
        assert 0.0 <= score <= 1.0

    def test_rag_mode_activated_when_both_provided(self):
        """Providing faithfulness + answer_relevance triggers RAG mode."""
        score = self.agg.compute_final(0.8, 0.7, 0.9, 0.6,
                                       faithfulness=0.9,
                                       answer_relevance=0.8)
        assert 0.0 <= score <= 1.0

    def test_rag_score_differs_from_standard(self):
        """RAG and standard modes should produce different weights."""
        standard = self.agg.compute_final(0.8, 0.7, 0.9, 0.6)
        rag = self.agg.compute_final(0.8, 0.7, 0.9, 0.6,
                                     faithfulness=0.3,
                                     answer_relevance=0.4)
        assert standard != rag

    def test_perfect_faithfulness_boosts_score(self):
        """High faithfulness should yield high RAG score."""
        score = self.agg.compute_final(0.9, 0.9, 0.9, 0.9,
                                       faithfulness=1.0,
                                       answer_relevance=1.0)
        assert score >= 0.85

    def test_zero_faithfulness_penalises_score(self):
        """Zero faithfulness (full hallucination) should tank the score significantly."""
        high_faith = self.agg.compute_final(0.8, 0.8, 0.9, 0.8,
                                            faithfulness=1.0, answer_relevance=0.9)
        low_faith = self.agg.compute_final(0.8, 0.8, 0.9, 0.8,
                                           faithfulness=0.0, answer_relevance=0.9)
        assert high_faith > low_faith + 0.25  # Large gap expected

    def test_get_weights_rag_mode(self):
        """RAG weight dict should have 6 keys."""
        weights = self.agg.get_weights(rag_mode=True)
        assert len(weights) == 6
        assert "faithfulness" in weights
        assert "answer_relevance" in weights

    def test_get_weights_standard_mode(self):
        """Standard weight dict should have 4 keys."""
        weights = self.agg.get_weights(rag_mode=False)
        assert len(weights) == 4
        assert "faithfulness" not in weights

    def test_rag_weights_sum_to_one(self):
        """RAG weights must sum to 1.0."""
        weights = self.agg.get_weights(rag_mode=True)
        assert sum(weights.values()) == pytest.approx(1.0, abs=1e-6)


# =====================================================================
# AnswerRelevanceChecker unit tests (lightweight, no heavy ML)
# =====================================================================

class TestAnswerRelevanceLogic:
    """
    Tests for the AnswerRelevanceChecker logic layer.
    Uses a mocked model to avoid loading sentence-transformers.
    """

    def test_no_context_returns_prompt_similarity(self, mocker):
        """Without context, score equals prompt-response similarity."""
        checker = AnswerRelevanceChecker.__new__(AnswerRelevanceChecker)
        checker._similarity = lambda a, b: 0.75
        result = checker.compute_score("What is AI?", "AI is...", context=None)
        assert result["score"] == pytest.approx(0.75, abs=0.01)
        assert result["context_similarity"] is None
        assert result["is_context_echo"] is False

    def test_echo_penalty_applied(self, mocker):
        """If context_sim >> prompt_sim, penalise the score."""
        checker = AnswerRelevanceChecker.__new__(AnswerRelevanceChecker)
        call_count = [0]

        def mock_sim(a, b):
            call_count[0] += 1
            # Alternates: first call = prompt→response, second = context→response
            return 0.4 if call_count[0] % 2 == 1 else 0.85

        checker._similarity = mock_sim
        result = checker.compute_score("What is AI?", "AI is...", context="Some context")
        assert result["is_context_echo"] is True
        assert result["score"] < 0.4  # Penalised below raw prompt sim

    def test_no_echo_no_penalty(self, mocker):
        """If prompt_sim ≥ context_sim, no penalty applied."""
        checker = AnswerRelevanceChecker.__new__(AnswerRelevanceChecker)
        call_count = [0]

        def mock_sim(a, b):
            call_count[0] += 1
            return 0.8 if call_count[0] % 2 == 1 else 0.55

        checker._similarity = mock_sim
        result = checker.compute_score("What is AI?", "AI is...", context="Some context")
        assert result["is_context_echo"] is False
        assert result["score"] == pytest.approx(0.8, abs=0.01)


# =====================================================================
# FaithfulnessChecker unit tests (lightweight, no heavy ML)
# =====================================================================

class TestFaithfulnessLogic:
    """
    Tests for the FaithfulnessChecker logic using a mocked _classify method.
    """

    def _make_checker(self):
        return FaithfulnessChecker.__new__(FaithfulnessChecker)

    def test_no_context_returns_none_score(self):
        checker = self._make_checker()
        result = checker.compute_score("", "Some response about AI.")
        assert result["score"] is None
        assert "not applicable" in result["note"].lower()

    def test_all_entailed_scores_1(self):
        checker = self._make_checker()
        checker._classify = lambda p, h: {"entailment": 0.9, "contradiction": 0.05, "neutral": 0.05}
        result = checker.compute_score("Paris is the capital of France.",
                                       "Paris is in France. France is a country.")
        assert result["score"] == pytest.approx(1.0, abs=0.01)
        assert result["hallucinated"] == 0

    def test_all_contradicted_scores_0(self):
        checker = self._make_checker()
        checker._classify = lambda p, h: {"entailment": 0.05, "contradiction": 0.9, "neutral": 0.05}
        result = checker.compute_score("The sky is blue.",
                                       "The sky is green. The sun is cold.")
        assert result["score"] == pytest.approx(0.0, abs=0.01)
        assert result["entailed"] == 0

    def test_mixed_gives_partial_score(self):
        checker = self._make_checker()
        responses = [
            {"entailment": 0.85, "contradiction": 0.05, "neutral": 0.10},
            {"entailment": 0.05, "contradiction": 0.85, "neutral": 0.10},
        ]
        call_count = [0]

        def mock_classify(p, h):
            r = responses[min(call_count[0], 1)]
            call_count[0] += 1
            return r

        checker._classify = mock_classify
        result = checker.compute_score("Context: Paris is in France.",
                                       "Paris is in France. Paris is in Germany.")
        # 1 entailed, 1 contradiction → score = (1 + 0.5*0) / 2 = 0.5
        assert result["score"] == pytest.approx(0.5, abs=0.01)
        assert result["entailed"] == 1
        assert result["hallucinated"] == 1

    def test_all_neutral_gives_half_score(self):
        checker = self._make_checker()
        checker._classify = lambda p, h: {"entailment": 0.05, "contradiction": 0.05, "neutral": 0.9}
        result = checker.compute_score(
            "Context here about some topic.",
            "This is a neutral claim about something. This is another neutral statement here."
        )
        # All neutral: score = (0 + 0.5 * total) / total = 0.5
        assert result["score"] == pytest.approx(0.5, abs=0.01)
        assert result["neutral"] == result["total_claims"]


    def test_claim_details_populated(self):
        checker = self._make_checker()
        checker._classify = lambda p, h: {"entailment": 0.8, "contradiction": 0.1, "neutral": 0.1}
        result = checker.compute_score("Context.", "One claim. Two claim.")
        assert len(result["claim_details"]) == result["total_claims"]
        for detail in result["claim_details"]:
            assert "claim" in detail
            assert "label" in detail
            assert detail["label"] in ("entailment", "contradiction", "neutral")
