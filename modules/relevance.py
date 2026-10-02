"""
Relevance Analyzer Module
===========================
Measures how semantically related the response is to the prompt using
a pretrained transformer model (all-MiniLM-L6-v2).

Both the prompt and response are converted into dense vector embeddings,
then cosine similarity is computed between them.

Score interpretation:
  - Close to 1.0 → response is highly relevant to the prompt
  - Close to 0.0 → response is off-topic

This captures meaning, not just keyword overlap:
  "Cars drive on roads" and "Automobiles travel on highways" score high
  similarity even though they share no words.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch


class RelevanceAnalyzer:

    def __init__(self):
        if torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device=self.device,
        )

    def compute_score(self, prompt: str, response: str) -> float:
        """
        Compute semantic similarity between prompt and response.

        Args:
            prompt: The original user prompt.
            response: The AI model's response.

        Returns:
            A float between 0 and 1 representing semantic relevance.
        """
        embeddings = self.model.encode(
            [prompt, response],
            convert_to_numpy=True,
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]],
        )[0][0]

        return float(max(0.0, similarity))