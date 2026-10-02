"""
Unit Tests for Meta-Evaluation Framework
==========================================
Tests all four evaluation modules, the aggregator, and edge cases.

Run with:
    python -m pytest tests/ -v
    python -m pytest tests/ -v --tb=short
"""

import json
import os
import sys
import tempfile

import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.quality import QualityAnalyzer
from modules.aggregator import ScoreAggregator


# =====================================================================
# Quality Analyzer Tests (no ML models needed — runs instantly)
# =====================================================================

class TestQualityAnalyzer:
    """Tests for the rule-based quality module."""

    def setup_method(self):
        self.analyzer = QualityAnalyzer()

    # ── Length score tests ──

    def test_length_very_short(self):
        """Responses under 10 words should score 0.3."""
        response = "This is short."
        score = self.analyzer.length_score(response)
        assert score == 0.3

    def test_length_short(self):
        """Responses between 10-29 words should score 0.6."""
        response = "This is a response with exactly enough words to be considered short but acceptable in length by our system."
        score = self.analyzer.length_score(response)
        assert score == 0.6

    def test_length_medium(self):
        """Responses between 30-59 words should score 0.8."""
        response = " ".join(["word"] * 40)
        score = self.analyzer.length_score(response)
        assert score == 0.8

    def test_length_long(self):
        """Responses with 60+ words should score 1.0."""
        response = " ".join(["word"] * 70)
        score = self.analyzer.length_score(response)
        assert score == 1.0

    # ── Repetition score tests ──

    def test_repetition_all_unique(self):
        """All unique words should score 1.0."""
        response = "every single word here is completely different and unique"
        score = self.analyzer.repetition_score(response)
        assert score == 1.0

    def test_repetition_all_same(self):
        """All repeated words should score low."""
        response = "data data data data data data data data data data"
        score = self.analyzer.repetition_score(response)
        assert score == pytest.approx(0.1)  # 1 unique / 10 total

    def test_repetition_empty(self):
        """Empty response should score 0.0."""
        score = self.analyzer.repetition_score("")
        assert score == 0.0

    def test_repetition_mixed(self):
        """Mix of unique and repeated words."""
        response = "the cat sat on the mat"  # 5 unique out of 6
        score = self.analyzer.repetition_score(response)
        assert 0.5 < score < 1.0

    # ── Combined score tests ──

    def test_compute_score_range(self):
        """Combined score should be between 0 and 1."""
        response = "Machine learning is a powerful tool for data analysis."
        score = self.analyzer.compute_score(response)
        assert 0.0 <= score <= 1.0

    def test_good_response_high_score(self):
        """A well-written response should score higher than a poor one."""
        good = (
            "Machine learning is a branch of artificial intelligence where "
            "computers learn patterns from data autonomously. It enables "
            "systems to improve their performance through experience without "
            "explicit programming. Applications range from image recognition "
            "to natural language processing and predictive analytics."
        )
        bad = "ML data computer learn data computer data ML data data"
        assert self.analyzer.compute_score(good) > self.analyzer.compute_score(bad)

    def test_empty_response(self):
        """Empty response should get the lowest possible score."""
        score = self.analyzer.compute_score("")
        assert score == pytest.approx(0.15)  # (0.3 + 0.0) / 2

    # ── JSON structure tests ──

    def test_json_valid_object(self):
        """Valid JSON object should score 1.0."""
        response = '{"key": "value"}'
        assert self.analyzer.json_score(response) == 1.0

    def test_json_valid_array(self):
        """Valid JSON array should score 1.0."""
        response = '[1, 2, 3]'
        assert self.analyzer.json_score(response) == 1.0

    def test_json_malformed(self):
        """Malformed JSON should score low but not 0."""
        response = '{"key": "value"'  # Missing closing brace
        assert 0.0 < self.analyzer.json_score(response) < 1.0

    def test_json_none(self):
        """No JSON should score 0.0."""
        response = "This is not JSON."
        assert self.analyzer.json_score(response) == 0.0

    # ── Markdown structure tests ──

    def test_markdown_header(self):
        """Response with markdown header."""
        response = "# Heading\nSome content."
        assert self.analyzer.markdown_score(response) >= 0.3

    def test_markdown_list(self):
        """Response with markdown list."""
        response = "- Item 1\n- Item 2"
        assert self.analyzer.markdown_score(response) >= 0.3

    def test_markdown_code(self):
        """Response with markdown code block."""
        response = "```python\nprint('hello')\n```"
        assert self.analyzer.markdown_score(response) >= 0.2

    def test_markdown_combination(self):
        """Multiple markdown elements give higher score."""
        simple = "# Header"
        complex = "# Header\n\n- List item\n- Another item\n\n```code```"
        assert self.analyzer.markdown_score(complex) > self.analyzer.markdown_score(simple)

    # ── Enhanced compute_score tests ──

    def test_compute_score_with_structure(self):
        """Structural data should score better than plain text with similar content."""
        plain = "Step 1 is to do this. Step 2 is to do that."
        structured = "# Instructions\n\n1. Step 1: do this\n2. Step 2: do that"
        assert self.analyzer.compute_score(structured) > self.analyzer.compute_score(plain)


# =====================================================================
# Score Aggregator Tests (no ML models needed)
# =====================================================================

class TestScoreAggregator:
    """Tests for the weighted score aggregation."""

    def setup_method(self):
        self.agg = ScoreAggregator()

    def test_default_weights(self):
        """Default weights should be 35/25/25/15."""
        weights = self.agg.get_weights()
        assert weights["relevance"] == pytest.approx(0.35)
        assert weights["quality"] == pytest.approx(0.25)
        assert weights["bias"] == pytest.approx(0.25)
        assert weights["consistency"] == pytest.approx(0.15)

    def test_weights_sum_to_one(self):
        """Default weights should sum to 1.0."""
        weights = self.agg.get_weights()
        assert sum(weights.values()) == pytest.approx(1.0)

    def test_perfect_scores(self):
        """All scores at 1.0 should give final score 1.0."""
        score = self.agg.compute_final(1.0, 1.0, 1.0, 1.0)
        assert score == pytest.approx(1.0)

    def test_zero_scores(self):
        """All scores at 0.0 should give final score 0.0."""
        score = self.agg.compute_final(0.0, 0.0, 0.0, 0.0)
        assert score == pytest.approx(0.0)

    def test_weighted_calculation(self):
        """Verify the weighted sum formula."""
        score = self.agg.compute_final(0.8, 0.6, 0.9, 0.7)
        expected = 0.35 * 0.8 + 0.25 * 0.6 + 0.25 * 0.9 + 0.15 * 0.7
        assert score == pytest.approx(expected)

    def test_custom_weights(self):
        """Custom weights should override defaults."""
        agg = ScoreAggregator(w_relevance=0.5, w_quality=0.2, w_bias=0.2, w_consistency=0.1)
        weights = agg.get_weights()
        assert weights["relevance"] == pytest.approx(0.5)

    def test_static_mode(self):
        """Default mode should be 'static'."""
        assert self.agg.get_mode() == "static"

    def test_training_info_none_for_static(self):
        """Static mode should return None for training info."""
        assert self.agg.get_training_info() is None

    def test_load_learned_weights(self):
        """Loading learned weights from JSON should work."""
        # Create a temporary weights file
        weights_data = {
            "weights": {
                "relevance": 0.3,
                "quality": 0.4,
                "bias": 0.1,
                "consistency": 0.2,
            },
            "metrics": {"cv_r2_mean": 0.85},
            "trained_at": "2026-01-01T00:00:00",
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(weights_data, f)
            tmp_path = f.name

        try:
            agg = ScoreAggregator(use_learned=True, weights_path=tmp_path)
            assert agg.get_mode() == "learned"
            assert agg.get_weights()["relevance"] == pytest.approx(0.3)
            assert agg.get_weights()["quality"] == pytest.approx(0.4)
            info = agg.get_training_info()
            assert info is not None
            assert info["metrics"]["cv_r2_mean"] == pytest.approx(0.85)
        finally:
            os.unlink(tmp_path)

    def test_missing_weights_file_raises(self):
        """Missing weights file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            ScoreAggregator(use_learned=True, weights_path="/nonexistent/path.json")

    def test_result_within_bounds(self):
        """Final score should always be between 0 and 1 for valid inputs."""
        import random
        random.seed(42)
        for _ in range(100):
            scores = [random.random() for _ in range(4)]
            result = self.agg.compute_final(*scores)
            assert 0.0 <= result <= 1.0


# =====================================================================
# ML-dependent tests (require model downloads, marked slow)
# =====================================================================

@pytest.mark.slow
class TestRelevanceAnalyzer:
    """Tests for the semantic relevance module (requires all-MiniLM-L6-v2)."""

    @pytest.fixture(autouse=True, scope="class")
    def load_model(self):
        """Load the model once for all tests in this class."""
        from modules.relevance import RelevanceAnalyzer
        TestRelevanceAnalyzer._analyzer = RelevanceAnalyzer()

    @property
    def analyzer(self):
        return self._analyzer

    def test_score_range(self):
        """Score should be between 0 and 1."""
        score = self.analyzer.compute_score(
            "What is AI?",
            "Artificial intelligence is the simulation of human intelligence by machines."
        )
        assert 0.0 <= score <= 1.0

    def test_relevant_response_high(self):
        """A directly relevant response should score > 0.5."""
        score = self.analyzer.compute_score(
            "What is machine learning?",
            "Machine learning is a subset of AI where computers learn from data."
        )
        assert score > 0.5

    def test_irrelevant_response_low(self):
        """A completely off-topic response should score lower."""
        relevant = self.analyzer.compute_score(
            "What is machine learning?",
            "Machine learning allows computers to learn from data automatically."
        )
        irrelevant = self.analyzer.compute_score(
            "What is machine learning?",
            "I had pasta for dinner last night and it was absolutely delicious."
        )
        assert relevant > irrelevant

    def test_semantic_similarity(self):
        """Semantically similar but lexically different texts should score well."""
        score = self.analyzer.compute_score(
            "Cars drive on roads",
            "Automobiles travel on highways"
        )
        assert score > 0.4  # Captures meaning, not just words


@pytest.mark.slow
class TestBiasDetector:
    """Tests for the toxicity detection module (requires toxic-bert)."""

    @pytest.fixture(autouse=True, scope="class")
    def load_model(self):
        from modules.bias import BiasDetector
        TestBiasDetector._detector = BiasDetector()

    @property
    def detector(self):
        return self._detector

    def test_score_range(self):
        """Score should be between 0 and 1."""
        score = self.detector.compute_score("The weather is nice today.")
        assert 0.0 <= score <= 1.0

    def test_clean_response_high(self):
        """A neutral, clean response should score high (close to 1.0)."""
        score = self.detector.compute_score(
            "Machine learning is a powerful technology for data analysis and prediction."
        )
        assert score > 0.7

    def test_toxic_response_low(self):
        """A toxic response should score lower than a clean one."""
        clean = self.detector.compute_score("Photosynthesis converts light to energy.")
        toxic = self.detector.compute_score("You are a stupid idiot and I hate you.")
        assert clean > toxic


@pytest.mark.slow
class TestConsistencyAnalyzer:
    """Tests for the NLI-based consistency module (requires DeBERTa)."""

    @pytest.fixture(autouse=True, scope="class")
    def load_model(self):
        from modules.consistency import ConsistencyAnalyzer
        TestConsistencyAnalyzer._analyzer = ConsistencyAnalyzer()

    @property
    def analyzer(self):
        return self._analyzer

    def test_consistent_response(self):
        """A logically consistent response should score high."""
        response = (
            "Machine learning is a powerful tool. "
            "It enables computers to learn from data. "
            "This technology has many practical applications."
        )
        score = self.analyzer.compute_internal_consistency(response)
        assert score > 0.7

    def test_contradictory_response(self):
        """A self-contradictory response should score low."""
        response = (
            "Machine learning is incredibly useful and powerful. "
            "Machine learning is completely useless and does not work at all."
        )
        score = self.analyzer.compute_internal_consistency(response)
        assert score < 0.7

    def test_single_sentence(self):
        """A single sentence should return 1.0 (can't contradict itself)."""
        score = self.analyzer.compute_internal_consistency("Machine learning is great.")
        assert score == 1.0

    def test_compute_score_returns_dict(self):
        """compute_score should return a dictionary with expected keys."""
        result = self.analyzer.compute_score("Test response.")
        assert "internal" in result
        assert "cross_model" in result
        assert "combined" in result

    def test_cross_model_consistent(self):
        """Agreeing models should have high cross-model consistency."""
        response = "Machine learning allows computers to learn from data."
        others = [
            "ML enables systems to learn patterns automatically.",
            "Machine learning is a branch of artificial intelligence.",
        ]
        score = self.analyzer.compute_cross_model_consistency(response, others)
        assert score > 0.5

    def test_cross_model_no_others(self):
        """With no other responses, cross-model should return 1.0."""
        score = self.analyzer.compute_cross_model_consistency("Test.", [])
        assert score == 1.0


# =====================================================================
# Edge case tests (no ML models needed)
# =====================================================================

class TestEdgeCases:
    """Edge case tests for robustness."""

    def test_quality_single_word(self):
        q = QualityAnalyzer()
        score = q.compute_score("Hello")
        assert 0.0 <= score <= 1.0

    def test_quality_very_long_response(self):
        q = QualityAnalyzer()
        response = " ".join(f"word{i}" for i in range(500))
        score = q.compute_score(response)
        assert score == pytest.approx(1.0)  # long + all unique

    def test_quality_numbers_only(self):
        q = QualityAnalyzer()
        score = q.compute_score("1 2 3 4 5 6 7 8 9 10 11 12")
        assert 0.0 <= score <= 1.0

    def test_quality_special_characters(self):
        q = QualityAnalyzer()
        score = q.compute_score("!!! ??? ... ### $$$ %%% &&& *** +++ ---")
        assert 0.0 <= score <= 1.0

    def test_aggregator_boundary_scores(self):
        """Test aggregator with boundary values."""
        agg = ScoreAggregator()
        assert agg.compute_final(0.0, 0.0, 0.0, 0.0) == pytest.approx(0.0)
        assert agg.compute_final(1.0, 1.0, 1.0, 1.0) == pytest.approx(1.0)
        assert agg.compute_final(0.5, 0.5, 0.5, 0.5) == pytest.approx(0.5)

    def test_aggregator_single_dimension_dominance(self):
        """When only one dimension scores high, it should reflect its weight."""
        agg = ScoreAggregator()
        # Only relevance = 1.0, rest = 0.0
        score = agg.compute_final(1.0, 0.0, 0.0, 0.0)
        assert score == pytest.approx(0.35)  # relevance weight


# =====================================================================
# Integration test (slow — loads all models)
# =====================================================================

@pytest.mark.slow
class TestIntegration:
    """End-to-end integration test."""

    def test_full_pipeline(self):
        """Test the complete evaluation pipeline produces valid results."""
        from modules.relevance import RelevanceAnalyzer
        from modules.quality import QualityAnalyzer
        from modules.bias import BiasDetector
        from modules.consistency import ConsistencyAnalyzer
        from modules.aggregator import ScoreAggregator

        prompt = "What is Python?"
        responses = {
            "Good": "Python is a high-level programming language known for its readability and versatility.",
            "Bad": "Python python python python python python python python.",
        }

        rel = RelevanceAnalyzer()
        qual = QualityAnalyzer()
        bias = BiasDetector()
        cons = ConsistencyAnalyzer()
        agg = ScoreAggregator()

        results = {}
        model_names = list(responses.keys())

        for name, resp in responses.items():
            r = rel.compute_score(prompt, resp)
            q = qual.compute_score(resp)
            b = bias.compute_score(resp)
            others = [responses[m] for m in model_names if m != name]
            c = cons.compute_score(resp, others)["combined"]
            final = agg.compute_final(r, q, b, c)

            results[name] = final
            assert 0.0 <= final <= 1.0

        # Good response should rank higher
        assert results["Good"] > results["Bad"]
