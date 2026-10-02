"""
Faithfulness Module (RAG Hallucination Detector)
=================================================
Checks whether a model's response is grounded in the provided context or
contains hallucinated (made-up) information.

Algorithm:
  1. Split the response into individual claims (sentences).
  2. For each claim, run NLI against the full context using DeBERTa:
       - ENTAILMENT  → claim is supported by context  ✅
       - NEUTRAL     → claim is not verifiable from context ⚠️
       - CONTRADICTION → claim directly contradicts context ❌
  3. Faithfulness Score = (entailed claims) / (total claims)

Score Interpretation:
  - 1.0 → fully grounded, zero hallucination
  - 0.5 → half the claims are unsupported
  - 0.0 → nothing is grounded (pure hallucination)

Note: Reuses the same DeBERTa NLI model as ConsistencyAnalyzer.
For efficiency in combined pipelines, share the model instance via
the shared_model parameter.
"""

import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class FaithfulnessChecker:
    """
    Hallucination detector for RAG pipelines.
    Checks each response claim against the provided context.
    """

    # NLI label indices for cross-encoder/nli-deberta-v3-small
    # 0 → contradiction, 1 → entailment, 2 → neutral
    CONTRADICTION_IDX = 0
    ENTAILMENT_IDX = 1
    NEUTRAL_IDX = 2

    def __init__(self, shared_model=None, shared_tokenizer=None):
        """
        Initialise the faithfulness checker.

        Args:
            shared_model: A pre-loaded DeBERTa model instance to reuse
                          (avoids loading it twice in a combined pipeline).
            shared_tokenizer: Matching tokenizer for the shared model.
        """
        model_name = "cross-encoder/nli-deberta-v3-small"

        # Device selection: MPS (Apple Silicon), then CPU
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

        if shared_model is not None and shared_tokenizer is not None:
            self.model = shared_model
            self.tokenizer = shared_tokenizer
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()

    def _split_claims(self, text: str) -> list[str]:
        """
        Split response text into individual claims (sentences).
        Filters out very short fragments that aren't useful for NLI.
        """
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if len(s.strip()) > 15]

    def _classify(self, premise: str, hypothesis: str) -> dict[str, float]:
        """
        Run NLI classification between premise (context) and hypothesis (claim).

        Args:
            premise: The reference context.
            hypothesis: A single claim from the response.

        Returns:
            Dict with probabilities for contradiction, entailment, neutral.
        """
        inputs = self.tokenizer(
            premise,
            hypothesis,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)[0]

        return {
            "contradiction": probs[self.CONTRADICTION_IDX].item(),
            "entailment":    probs[self.ENTAILMENT_IDX].item(),
            "neutral":       probs[self.NEUTRAL_IDX].item(),
        }

    def compute_score(self, context: str, response: str) -> dict:
        """
        Compute the faithfulness score for a response given a context.

        Args:
            context: The retrieved context that the RAG model used.
            response: The model's generated response.

        Returns:
            A dict containing:
              - score (float): Overall faithfulness (0–1)
              - entailed (int): Number of fully supported claims
              - hallucinated (int): Number of unsupported/contradicted claims
              - neutral (int): Number of claims that can't be verified
              - total_claims (int): Total claims checked
              - claim_details (list): Per-claim breakdown
        """
        if not context or not context.strip():
            # No context provided — faithfulness cannot be evaluated
            return {
                "score": None,
                "entailed": 0,
                "hallucinated": 0,
                "neutral": 0,
                "total_claims": 0,
                "claim_details": [],
                "note": "No context provided — faithfulness not applicable.",
            }

        claims = self._split_claims(response)

        if not claims:
            return {
                "score": 1.0,
                "entailed": 0,
                "hallucinated": 0,
                "neutral": 0,
                "total_claims": 0,
                "claim_details": [],
                "note": "Response too short to split into claims.",
            }

        claim_details = []
        n_entailed = 0
        n_hallucinated = 0
        n_neutral = 0

        for claim in claims:
            result = self._classify(context, claim)
            label = max(result, key=result.get)  # type: ignore[arg-type]

            if label == "entailment":
                n_entailed += 1
            elif label == "contradiction":
                n_hallucinated += 1
            else:
                n_neutral += 1

            claim_details.append({
                "claim": claim,
                "label": label,
                "entailment": round(result["entailment"], 4),
                "contradiction": round(result["contradiction"], 4),
                "neutral": round(result["neutral"], 4),
            })

        # Score: entailed claims / total claims
        # Neutral claims count as partial support (0.5 credit)
        # Contradictions count as 0
        total = len(claims)
        score = (n_entailed + 0.5 * n_neutral) / total

        return {
            "score": round(score, 4),
            "entailed": n_entailed,
            "hallucinated": n_hallucinated,
            "neutral": n_neutral,
            "total_claims": total,
            "claim_details": claim_details,
            "note": None,
        }
