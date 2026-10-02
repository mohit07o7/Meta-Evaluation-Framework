"""
LLM Provider Integration
==========================
Provides a unified interface for querying multiple LLM providers:
  - Ollama (local models)
  - OpenAI (GPT-3.5, GPT-4, etc.)
  - Google Gemini

Each provider returns a standard response dict:
    {"model": str, "response": str, "latency_ms": float, "provider": str}

Usage:
    from modules.llm_providers import OllamaProvider, OpenAIProvider, GeminiProvider

    provider = OllamaProvider(model="llama3")
    result = provider.generate("Explain machine learning.")
"""

import os
import time
import json
from abc import ABC, abstractmethod
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────
# Base provider
# ─────────────────────────────────────────────────────────────────────────

class LLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    def __init__(self, model: str, provider_name: str):
        self.model = model
        self.provider_name = provider_name

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> dict:
        """
        Generate a response from the LLM.

        Returns:
            dict with keys: model, response, latency_ms, provider
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is configured and reachable."""
        pass

    def _build_result(self, response_text: str, latency_ms: float) -> dict:
        return {
            "model": self.model,
            "response": response_text.strip(),
            "latency_ms": round(latency_ms, 1),
            "provider": self.provider_name,
        }


# ─────────────────────────────────────────────────────────────────────────
# Ollama (local)
# ─────────────────────────────────────────────────────────────────────────

class OllamaProvider(LLMProvider):
    """
    Provider for Ollama — runs models locally.
    Requires: `ollama` installed and running (`ollama serve`).
    """

    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        super().__init__(model=model, provider_name="Ollama")
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> dict:
        import urllib.request
        import urllib.error

        url = f"{self.base_url}/api/generate"
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            raise ConnectionError(
                f"Ollama not reachable at {self.base_url}. "
                f"Make sure Ollama is running (`ollama serve`). Error: {e}"
            )
        latency_ms = (time.time() - t0) * 1000

        return self._build_result(data.get("response", ""), latency_ms)

    def is_available(self) -> bool:
        import urllib.request
        import urllib.error

        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200
        except (urllib.error.URLError, ConnectionError, OSError):
            return False

    def list_models(self) -> list[str]:
        """List available models on the local Ollama instance."""
        import urllib.request
        import urllib.error

        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return [m["name"] for m in data.get("models", [])]
        except (urllib.error.URLError, ConnectionError, OSError):
            return []


# ─────────────────────────────────────────────────────────────────────────
# OpenAI
# ─────────────────────────────────────────────────────────────────────────

class OpenAIProvider(LLMProvider):
    """
    Provider for OpenAI API (GPT-3.5-turbo, GPT-4, GPT-4o, etc.).
    Requires: OPENAI_API_KEY environment variable.
    """

    AVAILABLE_MODELS = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
    ]

    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        super().__init__(model=model, provider_name="OpenAI")
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> dict:
        import urllib.request
        import urllib.error

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not set. Set OPENAI_API_KEY environment variable "
                "or pass api_key to the constructor."
            )

        url = "https://api.openai.com/v1/chat/completions"
        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Provide clear, accurate, and detailed responses."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise ConnectionError(f"OpenAI API error ({e.code}): {body}")
        except urllib.error.URLError as e:
            raise ConnectionError(f"OpenAI API unreachable: {e}")
        latency_ms = (time.time() - t0) * 1000

        response_text = data["choices"][0]["message"]["content"]
        return self._build_result(response_text, latency_ms)

    def is_available(self) -> bool:
        return bool(self.api_key)


# ─────────────────────────────────────────────────────────────────────────
# Google Gemini
# ─────────────────────────────────────────────────────────────────────────

class GeminiProvider(LLMProvider):
    """
    Provider for Google Gemini API.
    Requires: GEMINI_API_KEY environment variable.
    """

    AVAILABLE_MODELS = [
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]

    def __init__(self, model: str = "gemini-2.0-flash", api_key: Optional[str] = None):
        super().__init__(model=model, provider_name="Gemini")
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> dict:
        import urllib.request
        import urllib.error

        if not self.api_key:
            raise ValueError(
                "Gemini API key not set. Set GEMINI_API_KEY environment variable "
                "or pass api_key to the constructor."
            )

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        payload = json.dumps({
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            },
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise ConnectionError(f"Gemini API error ({e.code}): {body}")
        except urllib.error.URLError as e:
            raise ConnectionError(f"Gemini API unreachable: {e}")
        latency_ms = (time.time() - t0) * 1000

        # Extract text from Gemini response
        try:
            response_text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            response_text = "(No response generated)"

        return self._build_result(response_text, latency_ms)

    def is_available(self) -> bool:
        return bool(self.api_key)


# ─────────────────────────────────────────────────────────────────────────
# Provider registry & discovery
# ─────────────────────────────────────────────────────────────────────────

PROVIDER_REGISTRY = {
    "ollama": {
        "class": OllamaProvider,
        "display_name": "Ollama (Local)",
        "description": "Run open-source models locally via Ollama",
        "requires": "Ollama installed & running",
    },
    "openai": {
        "class": OpenAIProvider,
        "display_name": "OpenAI",
        "description": "GPT-3.5, GPT-4, GPT-4o via OpenAI API",
        "requires": "OPENAI_API_KEY",
    },
    "gemini": {
        "class": GeminiProvider,
        "display_name": "Google Gemini",
        "description": "Gemini Flash & Pro via Google AI API",
        "requires": "GEMINI_API_KEY",
    },
}


def get_available_providers() -> dict:
    """Return dict of provider_name -> info for providers that are currently usable."""
    available = {}
    for name, info in PROVIDER_REGISTRY.items():
        provider_cls = info["class"]
        try:
            instance = provider_cls()
            if instance.is_available():
                available[name] = info
        except Exception:
            pass
    return available


def create_provider(provider_name: str, model: str, api_key: str = "") -> LLMProvider:
    """Factory to create a provider instance."""
    if provider_name not in PROVIDER_REGISTRY:
        raise ValueError(f"Unknown provider: {provider_name}. Available: {list(PROVIDER_REGISTRY.keys())}")

    cls = PROVIDER_REGISTRY[provider_name]["class"]

    if provider_name == "ollama":
        return cls(model=model)
    else:
        return cls(model=model, api_key=api_key)
