from content_analysis_agent.strategies.analysis_strategy import ContentAnalysisStrategy
from content_analysis_agent.gemini_client import ask_llm
from rag_service.rag_agent import RAGAgent

class PDFAnalysisStrategy(ContentAnalysisStrategy):
    def __init__(self):
        # Use unique collection per request to avoid caching issues
        self.rag = None

    def analyze(self, content):
        # Create fresh RAG instance for each request
        # This ensures different subjects don't interfere with each other
        self.rag = RAGAgent(
            embedder_provider="gemini",
            persist_directory="rag_service/data/chroma_db",
            collection_name=f"lessons"  # Use consistent collection name
        )
        
        # Clear previous index to ensure fresh start
        try:
            self.rag._get_vector_store().delete_collection("lessons")
        except Exception:
            pass  # Collection doesn't exist yet, that's fine
        
        # Create fresh collection
        self.rag.configure_vector_store(collection_name="lessons")
        
        # Index & retrieve relevant chunks only
        self.rag.index_text(content)
        context = self.rag.build_context("objectives keywords", n_results=5)

        prompt = f"Analyze: {context}"
        return ask_llm(prompt)