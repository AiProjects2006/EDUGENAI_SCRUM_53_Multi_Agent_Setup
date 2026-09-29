"""ChromaDB vector store wrapper with lazy dependency loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


class VectorStoreError(RuntimeError):
    """Base error for vector-store failures."""




class VectorStoreDependencyError(VectorStoreError):
    """Raised when an optional vector-store dependency is unavailable."""


@dataclass(slots=True)
class SearchResult:
    id: str
    document: str | None = None
    metadata: dict[str, Any] | None = None
    distance: float | None = None
    embedding: list[float] | None = None


class ChromaVectorStore:
    """Minimal ChromaDB wrapper for storing and retrieving vectors."""

    def __init__(
        self,
        collection_name: str = "rag_documents",
        persist_directory: str | Path | None = None,
        collection_metadata: Mapping[str, Any] | None = None,
    ) -> None:
        if not collection_name:
            raise ValueError("collection_name must not be empty.")
        self.collection_name = collection_name
        self.persist_directory = str(Path(persist_directory)) if persist_directory else None
        self.collection_metadata = dict(collection_metadata or {})
        self._client: Any = None
        self._collection: Any = None

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            import chromadb
        except ImportError as exc:
            raise VectorStoreDependencyError(
                "ChromaVectorStore requires the 'chromadb' package. Install it with `pip install chromadb`."
            ) from exc

        if self.persist_directory:
            Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=self.persist_directory)
        else:
            self._client = chromadb.Client()
        return self._client

    def _get_collection(self) -> Any:
        if self._collection is None:
            metadata = self.collection_metadata or None
            self._collection = self._get_client().get_or_create_collection(
                name=self.collection_name,
                metadata=metadata,
            )
        return self._collection

    def upsert(
        self,
        ids: Sequence[str],
        *,
        documents: Sequence[str] | None = None,
        embeddings: Sequence[Sequence[float]] | None = None,
        metadatas: Sequence[Mapping[str, Any]] | None = None,
    ) -> None:
        if not ids:
            return
        size = len(ids)
        self._validate_lengths(size, documents=documents, embeddings=embeddings, metadatas=metadatas)
        payload: dict[str, Any] = {"ids": list(ids)}
        if documents is not None:
            payload["documents"] = list(documents)
        if embeddings is not None:
            payload["embeddings"] = [list(vector) for vector in embeddings]
        if metadatas is not None:
            payload["metadatas"] = [dict(item) for item in metadatas]
        self._get_collection().upsert(**payload)

    def query(
        self,
        *,
        query_embedding: Sequence[float] | None = None,
        query_text: str | None = None,
        n_results: int = 5,
        where: Mapping[str, Any] | None = None,
        include: Sequence[str] | None = None,
    ) -> list[SearchResult]:
        if query_embedding is None and query_text is None:
            raise ValueError("Provide either query_embedding or query_text.")

        kwargs: dict[str, Any] = {
            "n_results": n_results,
            "include": list(include or ["documents", "metadatas", "distances"]),
        }
        if where is not None:
            kwargs["where"] = dict(where)
        if query_embedding is not None:
            kwargs["query_embeddings"] = [list(query_embedding)]
        if query_text is not None:
            kwargs["query_texts"] = [query_text]

        response = self._get_collection().query(**kwargs)
        return self._flatten_query_response(response)

    def delete(self, ids: Sequence[str] | None = None, where: Mapping[str, Any] | None = None) -> None:
        kwargs: dict[str, Any] = {}
        if ids is not None:
            kwargs["ids"] = list(ids)
        if where is not None:
            kwargs["where"] = dict(where)
        if not kwargs:
            raise ValueError("Provide ids or where when deleting from the vector store.")
        self._get_collection().delete(**kwargs)

    def count(self) -> int:
        return int(self._get_collection().count())

    def persist(self) -> None:
        client = self._get_client()
        persist_method = getattr(client, "persist", None)
        if callable(persist_method):
            persist_method()

    def reset_collection(self) -> None:
        client = self._get_client()
        client.delete_collection(self.collection_name)
        self._collection = None

    @staticmethod
    def _validate_lengths(size: int, **collections: Sequence[Any] | None) -> None:
        for name, value in collections.items():
            if value is not None and len(value) != size:
                raise ValueError(f"{name} length must match ids length.")

    @staticmethod
    def _flatten_query_response(response: Mapping[str, Any]) -> list[SearchResult]:
        ids = response.get("ids", [[]])
        documents = response.get("documents", [[]])
        metadatas = response.get("metadatas", [[]])
        distances = response.get("distances", [[]])
        embeddings = response.get("embeddings", [[]])

        row_ids = ids[0] if ids else []
        row_documents = documents[0] if documents else []
        row_metadatas = metadatas[0] if metadatas else []
        row_distances = distances[0] if distances else []
        row_embeddings = embeddings[0] if embeddings else []

        results: list[SearchResult] = []
        for index, item_id in enumerate(row_ids):
            results.append(
                SearchResult(
                    id=item_id,
                    document=row_documents[index] if index < len(row_documents) else None,
                    metadata=dict(row_metadatas[index]) if index < len(row_metadatas) and row_metadatas[index] is not None else None,
                    distance=row_distances[index] if index < len(row_distances) else None,
                    embedding=list(row_embeddings[index]) if index < len(row_embeddings) and row_embeddings[index] is not None else None,
                )
            )
        return results


__all__ = [
    "ChromaVectorStore",
    "SearchResult",
    "VectorStoreDependencyError",
    "VectorStoreError",
]
