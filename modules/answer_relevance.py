"""
Answer Relevance Module (RAG)
==============================
Measures whether the response actually *answers* the prompt, or merely
summarises / paraphrases the context without addressing the question.

This is a critical distinction in RAG systems:
  - A bad RAG output repeats the context verbatim instead of using it
    to construct an actual answer.
  - A good RAG output extracts relevant facts from context and uses them
    to directly answer the user's question.

Algorithm (dual-similarity approach):
  1. Compute PROMPT → RESPONSE similarity (using all-MiniLM-L6-v2)
       High score = response stays on-topic w.r.t. the question.
  2. Compute CONTEXT → RESPONSE similarity
       High score = response is a restatement of the context.
  3. Answer Relevance Score = prompt_sim - α × (context_sim - prompt_sim)
       Penalty is applied only when context similarity dominates,
       i.e., the model is summarising context instead of answering.

Score Interpretation:
  - Close to 1.0 → response directly answers the prompt
  - Close to 0.5 → response partially answers the prompt
  - Close to 0.0 → response is off-topic or just a context echo
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch


class AnswerRelevanceChecker:
    """
    Evaluates whether the model's response genuinely answers the prompt
    rather than just echoing the retrieved context.
    """

    def __init__(self, shared_model=None):
        """
        Args:
            shared_model: A pre-loaded SentenceTransformer instance,
                          to avoid loading it twice in a combined pipeline.
        """
        if shared_model is not None:
            self.model = shared_model
        else:
            device = "mps" if torch.backends.mps.is_available() else "cpu"
            self.model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

    def _similarity(self, text_a: str, text_b: str) -> float:
        """Compute cosine similarity between two texts."""
        embeddings = self.model.encode([text_a, text_b], convert_to_numpy=True)
        sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(max(0.0, sim))

    def compute_score(
        self,
        prompt: str,
        response: str,
        context: str | None = None,
        echo_penalty_alpha: float = 0.5,
    ) -> dict:
        """
        Compute the answer relevance score.

        Args:
            prompt: The original user question.
            response: The model's generated response.
            context: The retrieved context (optional).
                     If not provided, falls back to simple prompt-response similarity.
            echo_penalty_alpha: How strongly to penalise context-echoing (default 0.5).
                     0 = no penalty, 1 = strong penalty.

        Returns:
            A dict containing:
              - score (float): Final answer relevance (0–1)
              - prompt_similarity (float): How similar response is to the prompt
              - context_similarity (float | None): How similar response is to context
              - is_context_echo (bool): True if response is mostly a context restatement
        """
        prompt_sim = self._similarity(prompt, response)

        if not context or not context.strip():
            # No context — simple prompt-response similarity
            return {
                "score": round(prompt_sim, 4),
                "prompt_similarity": round(prompt_sim, 4),
                "context_similarity": None,
                "is_context_echo": False,
            }

        context_sim = self._similarity(context, response)

        # Determine if the response is mostly an echo of the context
        # (context similarity dominates prompt similarity)
        is_echo = context_sim > prompt_sim + 0.15

        # Penalise when the model is just copying the context
        # rather than using it to answer the question
        if is_echo:
            penalty = echo_penalty_alpha * (context_sim - prompt_sim)
            final_score = max(0.0, prompt_sim - penalty)
        else:
            final_score = prompt_sim

        return {
            "score": round(final_score, 4),
            "prompt_similarity": round(prompt_sim, 4),
            "context_similarity": round(context_sim, 4),
            "is_context_echo": is_echo,
        }
