# RAG Service

Retrieval-Augmented Generation utilities for document chunking, embedding, vector storage, and retrieval.

## Modules
- `chunker.py`: stdlib-based text chunking with overlap support.
- `embedder.py`: lazy embedding adapters for Gemini, OpenAI, and local sentence-transformer models.
- `vector_store.py`: lazy ChromaDB wrapper for storing and querying vectors.
- `rag_agent.py`: orchestration layer for indexing documents and retrieving context.

## Optional dependencies
Install only the providers you plan to use:
- OpenAI: `pip install openai`
- Gemini: `pip install google-genai` or `pip install google-generativeai`
- Local embeddings: `pip install sentence-transformers`
- Vector store: `pip install chromadb`

## Example
```python
from rag_service import RAGAgent

agent = RAGAgent(
    embedder_provider="openai",
    embedder_config={"api_key": "your-key"},
    collection_name="learning-resources",
    persist_directory="rag_service/data/chroma",
)

agent.index_text("Newton's first law describes inertia.", metadata={"source": "physics"})
results = agent.retrieve("What is inertia?", n_results=3)
print(agent.build_context("What is inertia?"))
```
