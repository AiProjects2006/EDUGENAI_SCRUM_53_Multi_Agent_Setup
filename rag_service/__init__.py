"""
RAG Service Module - Retrieval-Augmented Generation for EDUGENAI

Handles document chunking, embedding, vector storage, and retrieval.
Integrates with Learning Resources Service to optimize content delivery for question generation.
"""

from rag_service.rag_agent import RAGAgent

__all__ = ['RAGAgent']
