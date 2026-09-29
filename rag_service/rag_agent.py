"""High-level Retrieval-Augmented Generation orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
from uuid import uuid4

from rag_service.chunker import TextChunk, TextChunker
from rag_service.embedder import BaseEmbedder, create_embedder
from rag_service.vector_store import ChromaVectorStore, SearchResult


class RAGAgentConfigurationError(RuntimeError):
    """Raised when the RAG agent is missing required configuration."""


@dataclass(slots=True)
class RetrievedChunk:
    id: str
    content: str | None
    metadata: dict[str, Any]
    distance: float | None = None


class RAGAgent:
    """Coordinates chunking, embedding, storage, and retrieval."""

    def __init__(
        self,
        *,
        chunker: TextChunker | None = None,
        embedder: BaseEmbedder | None = None,
        vector_store: ChromaVectorStore | None = None,
        embedder_provider: str | None = None,
        embedder_config: Mapping[str, Any] | None = None,
        collection_name: str = "rag_documents",
        persist_directory: str | Path | None = None,
        collection_metadata: Mapping[str, Any] | None = None,
    ) -> None:
        self.chunker = chunker or TextChunker()
        self._embedder = embedder
        self._vector_store = vector_store
        self._embedder_provider = embedder_provider
        self._embedder_config = dict(embedder_config or {})
        self._collection_name = collection_name
        self._persist_directory = str(Path(persist_directory)) if persist_directory else None
        self._collection_metadata = dict(collection_metadata or {})

    def configure_embedder(
        self,
        provider: str | None = None,
        *,
        embedder: BaseEmbedder | None = None,
        **config: Any,
    ) -> None:
        if embedder is not None:
            self._embedder = embedder
        if provider is not None:
            self._embedder_provider = provider
        if config:
            self._embedder_config.update(config)

    def configure_vector_store(
        self,
        *,
        vector_store: ChromaVectorStore | None = None,
        collection_name: str | None = None,
        persist_directory: str | Path | None = None,
        collection_metadata: Mapping[str, Any] | None = None,
    ) -> None:
        if vector_store is not None:
            self._vector_store = vector_store
            return
        if collection_name is not None:
            self._collection_name = collection_name
        if persist_directory is not None:
            self._persist_directory = str(Path(persist_directory))
        if collection_metadata is not None:
            self._collection_metadata = dict(collection_metadata)
        self._vector_store = None

    def chunk_text(self, text: str, metadata: Mapping[str, Any] | None = None) -> list[TextChunk]:
        return self.chunker.split_text(text, metadata=metadata)

    def index_text(
        self,
        text: str,
        *,
        metadata: Mapping[str, Any] | None = None,
        document_id: str | None = None,
    ) -> list[str]:
        chunks = self.chunk_text(text, metadata=metadata)
        if not chunks:
            return []
        base_id = document_id or str(uuid4())
        return self._store_chunks(chunks, base_id)

    def index_documents(self, documents: Sequence[str | Mapping[str, Any]]) -> list[str]:
        all_chunks: list[TextChunk] = []
        chunk_ids: list[str] = []
        for document in documents:
            text, metadata, document_id = self._coerce_document(document)
            chunks = self.chunk_text(text, metadata=metadata)
            if not chunks:
                continue
            ids = [f"{document_id}::{chunk.index}" for chunk in chunks]
            chunk_ids.extend(ids)
            all_chunks.extend(chunks)

        if not all_chunks:
            return []

        texts = [chunk.content for chunk in all_chunks]
        metadatas = [self._enrich_metadata(chunk) for chunk in all_chunks]
        embeddings = self._get_embedder().embed_texts(texts)
        
        # Ensure we have embeddings for all chunks
        if len(embeddings) != len(texts):
            raise ValueError(
                f"Embedding mismatch: expected {len(texts)} embeddings but got {len(embeddings)}. "
                f"This usually means some texts failed to embed. Try checking your API key and network connection."
            )
        
        self._get_vector_store().upsert(
            chunk_ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        self._get_vector_store().persist()
        return chunk_ids

    def retrieve(
        self,
        query: str,
        *,
        n_results: int = 5,
        where: Mapping[str, Any] | None = None,
    ) -> list[RetrievedChunk]:
        if not query:
            return []
        query_embedding = self._get_embedder().embed(query)
        results = self._get_vector_store().query(
            query_embedding=query_embedding,
            n_results=n_results,
            where=where,
        )
        return [self._to_retrieved_chunk(result) for result in results]

    def build_context(
        self,
        query: str,
        *,
        n_results: int = 5,
        where: Mapping[str, Any] | None = None,
        separator: str = "\n\n",
    ) -> str:
        results = self.retrieve(query, n_results=n_results, where=where)
        return separator.join(result.content for result in results if result.content)

    def similarity_search(
        self,
        query_embedding: Sequence[float],
        *,
        n_results: int = 5,
        where: Mapping[str, Any] | None = None,
    ) -> list[RetrievedChunk]:
        results = self._get_vector_store().query(
            query_embedding=query_embedding,
            n_results=n_results,
            where=where,
        )
        return [self._to_retrieved_chunk(result) for result in results]

    def _store_chunks(self, chunks: Sequence[TextChunk], base_id: str) -> list[str]:
        ids = [f"{base_id}::{chunk.index}" for chunk in chunks]
        texts = [chunk.content for chunk in chunks]
        metadatas = [self._enrich_metadata(chunk) for chunk in chunks]
        
        # Get embeddings
        embeddings = self._get_embedder().embed_texts(texts)
        
        # Ensure we have embeddings for all chunks
        if len(embeddings) != len(texts):
            raise ValueError(
                f"Embedding mismatch: expected {len(texts)} embeddings but got {len(embeddings)}. "
                f"This usually means some texts failed to embed. Try checking your API key and network connection."
            )
        
        # Validate embeddings are not empty
        if not embeddings:
            raise ValueError("No embeddings generated for chunks. Check if texts are empty.")
        
        # Store in vector database
        self._get_vector_store().upsert(
            ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        self._get_vector_store().persist()
        return ids

    def _get_embedder(self) -> BaseEmbedder:
        if self._embedder is None:
            if not self._embedder_provider:
                raise RAGAgentConfigurationError(
                    "No embedder configured. Pass an embedder instance or set embedder_provider to 'openai', 'gemini', or 'local'."
                )
            self._embedder = create_embedder(self._embedder_provider, **self._embedder_config)
        return self._embedder

    def _get_vector_store(self) -> ChromaVectorStore:
        if self._vector_store is None:
            self._vector_store = ChromaVectorStore(
                collection_name=self._collection_name,
                persist_directory=self._persist_directory,
                collection_metadata=self._collection_metadata,
            )
        return self._vector_store

    @staticmethod
    def _enrich_metadata(chunk: TextChunk) -> dict[str, Any]:
        metadata = dict(chunk.metadata)
        metadata.setdefault("chunk_index", chunk.index)
        metadata.setdefault("start_offset", chunk.start)
        metadata.setdefault("end_offset", chunk.end)
        return metadata

    @staticmethod
    def _to_retrieved_chunk(result: SearchResult) -> RetrievedChunk:
        return RetrievedChunk(
            id=result.id,
            content=result.document,
            metadata=result.metadata or {},
            distance=result.distance,
        )

    @staticmethod
    def _coerce_document(document: str | Mapping[str, Any]) -> tuple[str, dict[str, Any], str]:
        if isinstance(document, str):
            return document, {}, str(uuid4())
        if not isinstance(document, Mapping):
            raise TypeError("Documents must be strings or mappings.")

        text = document.get("text") or document.get("content")
        if not isinstance(text, str):
            raise ValueError("Document mappings must include a string 'text' or 'content' field.")

        metadata = document.get("metadata")
        if metadata is None:
            metadata = {
                key: value
                for key, value in document.items()
                if key not in {"id", "text", "content", "metadata"}
            }
        elif not isinstance(metadata, Mapping):
            raise TypeError("Document metadata must be a mapping when provided.")

        document_id = document.get("id")
        if document_id is None:
            document_id = str(uuid4())
        elif not isinstance(document_id, str):
            document_id = str(document_id)
        return text, dict(metadata), document_id


__all__ = ["RAGAgent", "RAGAgentConfigurationError", "RetrievedChunk"]
