"""
Quality Analyzer Module (Enhanced)
=====================================
A rule-based module that checks structural properties of the response.

Now includes checks for:
  1. Length adequacy — is the response too short?
  2. Repetition penalty — is the model just repeating words?
  3. JSON structure — is it valid and well-structured?
  4. Markdown structure — are headers, lists, or code blocks used correctly?

These are combined into a final quality score (0.0–1.0).
"""

import json
import re


class QualityAnalyzer:

    def length_score(self, response: str) -> float:
        """
        Score based on word count.
        < 10 words → 0.3
        10-29 words → 0.6
        30-59 words → 0.8
        60+ words → 1.0
        """
        words = response.split()
        word_count = len(words)

        if word_count < 10:
            return 0.3
        elif word_count < 30:
            return 0.6
        elif word_count < 60:
            return 0.8
        else:
            return 1.0

    def repetition_score(self, response: str) -> float:
        """
        Score based on vocabulary diversity (unique / total).
        """
        words = response.lower().split()
        if not words:
            return 0.0
        unique = len(set(words))
        return unique / len(words)

    def json_score(self, response: str) -> float:
        """
        Check if the response contains valid or well-structured JSON.
        Returns 1.0 if it's perfectly valid JSON, lower scores for partial/broken JSON.
        Returns 0.0 if no JSON is detected.
        """
        # Look for perfectly valid JSON matches first
        match_perfect = re.search(r"(\{.*\}|\[.*\])", response, re.DOTALL)
        if match_perfect:
            json_str = match_perfect.group(0)
            try:
                data = json.loads(json_str)
                if isinstance(data, (dict, list)):
                    return 1.0 if len(data) > 0 else 0.8
            except json.JSONDecodeError:
                pass  # Try partial match below

        # Look for "stale" or "broken" JSON attempts
        # Does it start with { or [ and then have some text?
        stripped = response.strip()
        if re.search(r"^[\s]*[\{\[]", stripped):
            return 0.4
        
        # Or does it have key-value-like pairs?
        if re.search(r'"[^"]+"\s*:\s*("[^"]+"|\d+|true|false|null)', response):
            return 0.3

        return 0.0

    def markdown_score(self, response: str) -> float:
        """
        Score based on the presence of Markdown elements.
        - Headers (#)
        - Bullet points (- or *)
        - Code blocks (``` or `)
        - Bold/Italic (** or __)
        """
        score = 0.0
        # Headers
        if re.search(r"^#{1,6}\s+.+", response, re.MULTILINE):
            score += 0.3
        # Lists
        if re.search(r"^[\*\-\+]\s+.+", response, re.MULTILINE) or re.search(r"^\d+\.\s+.+", response, re.MULTILINE):
            score += 0.3
        # Code blocks
        if "```" in response or "`" in response:
            score += 0.2
        # Emphasis
        if re.search(r"(\*\*|__|_|\*).+\1", response):
            score += 0.2

        return min(1.0, score)

    def compute_score(self, response: str) -> float:
        """
        Compute the final quality score by combining all sub-scores.
        Weights:
           - Basic (Length + Repetition): 60%
           - Structural (JSON or Markdown): 40%
        """
        l_score = self.length_score(response)
        r_score = self.repetition_score(response)
        basic_score = (l_score + r_score) / 2

        j_score = self.json_score(response)
        m_score = self.markdown_score(response)

        # Structure score: pick the best one
        structure_score = max(j_score, m_score)

        # Final weighted score
        if structure_score == 0:
            return basic_score

        return 0.6 * basic_score + 0.4 * structure_score