"""Embedding adapters with lazy optional-dependency loading."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence


class EmbeddingError(RuntimeError):
    """Base error for embedding-related failures."""


class EmbeddingDependencyError(EmbeddingError):
    """Raised when an optional embedding dependency is unavailable."""


class EmbeddingConfigurationError(EmbeddingError):
    """Raised when embedder configuration is incomplete."""


class BaseEmbedder:
    """Common interface for embedding providers."""

    model_name: str

    def embed(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        raise NotImplementedError

    @staticmethod
    def _validate_texts(texts: Sequence[str] | Iterable[str]) -> list[str]:
        values = list(texts)
        if not values:
            return []
        if not all(isinstance(item, str) for item in values):
            raise TypeError("All inputs for embedding must be strings.")
        return values


@dataclass(slots=True)
class OpenAIEmbedder(BaseEmbedder):
    model_name: str = "gemini-embedding-2"
    api_key: str | None = None
    organization: str | None = None
    _client: Any = field(default=None, init=False, repr=False)

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise EmbeddingDependencyError(
                "OpenAI embeddings require the 'openai' package. Install it with `pip install openai`."
            ) from exc

        api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EmbeddingConfigurationError(
                "OpenAI API key not configured. Pass api_key or set OPENAI_API_KEY."
            )

        client_kwargs: dict[str, Any] = {"api_key": api_key}
        if self.organization:
            client_kwargs["organization"] = self.organization
        self._client = OpenAI(**client_kwargs)
        return self._client

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        payload = self._validate_texts(texts)
        if not payload:
            return []
        response = self._get_client().embeddings.create(model=self.model_name, input=payload)
        return [list(item.embedding) for item in response.data]


@dataclass(slots=True)
class GeminiEmbedder(BaseEmbedder):
    model_name: str = "gemini-embedding-2"
    api_key: str | None = None
    _client: Any = field(default=None, init=False, repr=False)
    _legacy_client: Any = field(default=None, init=False, repr=False)

    def _get_modern_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            from google import genai
        except ImportError:
            return None

        api_key = self.api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EmbeddingConfigurationError(
                "Gemini API key not configured. Pass api_key or set GEMINI_API_KEY/GOOGLE_API_KEY."
            )
        self._client = genai.Client(api_key=api_key)
        return self._client

    def _get_legacy_client(self) -> Any:
        if self._legacy_client is not None:
            return self._legacy_client
        try:
            import google.generativeai as legacy_genai
        except ImportError as exc:
            raise EmbeddingDependencyError(
                "Gemini embeddings require 'google-genai' or 'google-generativeai'."
            ) from exc

        api_key = self.api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EmbeddingConfigurationError(
                "Gemini API key not configured. Pass api_key or set GEMINI_API_KEY/GOOGLE_API_KEY."
            )
        legacy_genai.configure(api_key=api_key)
        self._legacy_client = legacy_genai
        return self._legacy_client

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        payload = self._validate_texts(texts)
        if not payload:
            return []

        # Use legacy client for batch embedding (more reliable)
        legacy_client = self._get_legacy_client()
        vectors: list[list[float]] = []
        
        try:
            # Try batch embedding first with legacy client
            response = legacy_client.embed_content(model=self.model_name, content=payload)
            if isinstance(response, dict):
                embeddings = response.get("embedding")
            else:
                embeddings = getattr(response, "embedding", None)
            
            # If batch embedding worked, return it
            if embeddings and isinstance(embeddings, list) and len(embeddings) == len(payload):
                if isinstance(embeddings[0], list):
                    return embeddings
        except Exception:
            pass  # Fall back to per-item embedding
        
        # Fall back to per-item embedding (guaranteed to work)
        for text in payload:
            try:
                response = legacy_client.embed_content(model=self.model_name, content=text)
                if isinstance(response, dict):
                    embedding = response.get("embedding")
                else:
                    embedding = getattr(response, "embedding", None)
                if embedding is None:
                    raise EmbeddingError(f"Gemini embedding response did not include an embedding vector for text: {text[:50]}...")
                vectors.append(list(embedding))
            except Exception as e:
                raise EmbeddingError(f"Failed to embed text: {str(e)}") from e
        
        return vectors


@dataclass(slots=True)
class LocalEmbedder(BaseEmbedder):
    model_name: str = "all-MiniLM-L6-v2"
    normalize_embeddings: bool = False
    _model: Any = field(default=None, init=False, repr=False)

    def _get_model(self) -> Any:
        if self._model is not None:
            return self._model
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise EmbeddingDependencyError(
                "Local embeddings require 'sentence-transformers'. Install it with `pip install sentence-transformers`."
            ) from exc

        self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        payload = self._validate_texts(texts)
        if not payload:
            return []
        embeddings = self._get_model().encode(
            payload,
            normalize_embeddings=self.normalize_embeddings,
            convert_to_numpy=False,
        )
        return [list(vector) for vector in embeddings]


def create_embedder(provider: str, **kwargs: Any) -> BaseEmbedder:
    """Create an embedder instance for the selected provider."""
    normalized = provider.strip().lower()
    if normalized in {"openai", "open-ai"}:
        return OpenAIEmbedder(**kwargs)
    if normalized in {"gemini", "google", "google-genai"}:
        return GeminiEmbedder(**kwargs)
    if normalized in {"local", "sentence-transformer", "sentence-transformers"}:
        return LocalEmbedder(**kwargs)
    raise ValueError(f"Unsupported embedding provider: {provider!r}")


__all__ = [
    "BaseEmbedder",
    "EmbeddingConfigurationError",
    "EmbeddingDependencyError",
    "EmbeddingError",
    "GeminiEmbedder",
    "LocalEmbedder",
    "OpenAIEmbedder",
    "create_embedder",
]
