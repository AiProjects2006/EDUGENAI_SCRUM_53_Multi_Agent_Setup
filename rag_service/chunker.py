"""Utilities for splitting text into retrieval-friendly chunks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping



@dataclass(slots=True)
class TextChunk:
    """Represents a chunk of text and its source offsets."""

    content: str
    index: int
    start: int
    end: int
    metadata: dict[str, Any] = field(default_factory=dict)



class TextChunker:
    """Splits text into overlapping chunks using separator-aware boundaries."""

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        separators: tuple[str, ...] | None = None,
        trim_whitespace: bool = True,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size.")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ("\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ")
        self.trim_whitespace = trim_whitespace

    def split_text(self, text: str, metadata: Mapping[str, Any] | None = None) -> list[TextChunk]:
        """Split a single string into retrieval chunks."""
        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        raw_text = text
        if not raw_text:
            return []

        chunks: list[TextChunk] = []
        start = 0
        index = 0
        metadata_dict = dict(metadata or {})
        text_length = len(raw_text)

        while start < text_length:
            max_end = min(start + self.chunk_size, text_length)
            end = self._find_split_point(raw_text, start, max_end)
            if end <= start:
                end = max_end

            chunk_text = raw_text[start:end]
            normalized_chunk = chunk_text.strip() if self.trim_whitespace else chunk_text
            if normalized_chunk:
                leading_trim = len(chunk_text) - len(chunk_text.lstrip()) if self.trim_whitespace else 0
                trailing_trim = len(chunk_text) - len(chunk_text.rstrip()) if self.trim_whitespace else 0
                chunk_start = start + leading_trim
                chunk_end = end - trailing_trim
                chunks.append(
                    TextChunk(
                        content=normalized_chunk,
                        index=index,
                        start=chunk_start,
                        end=chunk_end,
                        metadata=dict(metadata_dict),
                    )
                )
                index += 1

            if end >= text_length:
                break

            next_start = max(end - self.chunk_overlap, start + 1)
            start = self._skip_leading_whitespace(raw_text, next_start)

        return chunks

    def split_documents(self, documents: Iterable[str | Mapping[str, Any]]) -> list[TextChunk]:
        """Split multiple documents into a flat list of chunks."""
        all_chunks: list[TextChunk] = []
        for document_index, document in enumerate(documents):
            text, metadata = self._coerce_document(document)
            metadata.setdefault("document_index", document_index)
            all_chunks.extend(self.split_text(text, metadata=metadata))
        return all_chunks

    def _find_split_point(self, text: str, start: int, max_end: int) -> int:
        if max_end >= len(text):
            return len(text)

        search_window = text[start:max_end]
        best_end = -1
        for separator in self.separators:
            separator_index = search_window.rfind(separator)
            if separator_index != -1:
                candidate_end = start + separator_index + len(separator)
                if candidate_end > best_end:
                    best_end = candidate_end
        if best_end <= start:
            return max_end
        return best_end

    @staticmethod
    def _skip_leading_whitespace(text: str, start: int) -> int:
        while start < len(text) and text[start].isspace():
            start += 1
        return start

    @staticmethod
    def _coerce_document(document: str | Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
        if isinstance(document, str):
            return document, {}
        if not isinstance(document, Mapping):
            raise TypeError("Each document must be a string or mapping.")

        text = document.get("text") or document.get("content")
        if not isinstance(text, str):
            raise ValueError("Document mappings must include a string 'text' or 'content' field.")

        metadata = document.get("metadata")
        if metadata is None:
            metadata = {key: value for key, value in document.items() if key not in {"text", "content", "metadata"}}
        elif not isinstance(metadata, Mapping):
            raise TypeError("Document metadata must be a mapping when provided.")
        return text, dict(metadata)


__all__ = ["TextChunk", "TextChunker"]
