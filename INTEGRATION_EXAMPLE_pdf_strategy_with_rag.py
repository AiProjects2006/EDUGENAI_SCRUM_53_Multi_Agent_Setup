"""
Enhanced PDF Analysis Strategy with RAG

This is an example of how to integrate RAG into your existing content analysis pipeline.
Replace your current pdf_strategy.py with this to enable retrieval-augmented content analysis.
"""

from content_analysis_agent.strategies.analysis_strategy import ContentAnalysisStrategy
from content_analysis_agent.gemini_client import ask_llm
from rag_service.rag_agent import RAGAgent


class PDFAnalysisStrategyWithRAG(ContentAnalysisStrategy):
    """Enhanced PDF analysis using RAG for better content retrieval and analysis."""

    def __init__(self, embedder_type="gemini"):
        """
        Initialize with RAG support.

        Args:
            embedder_type (str): 'gemini', 'openai', or 'local'
        """
        self.rag = RAGAgent(embedder_type=embedder_type)

    def analyze(self, content):
        """
        Analyze lesson content using RAG-enhanced retrieval.

        Args:
            content (str): Raw PDF or lesson text

        Returns:
            str: Analysis with extracted topic, keywords, learning objectives
        """
        print("[PDF Analysis] Starting enhanced analysis with RAG...")

        # Step 1: Index the content
        index_result = self.rag.index(
            content=content,
            metadata={"type": "lesson", "analysis_task": "extract_objectives"}
        )

        if not index_result["success"]:
            print(f"[PDF Analysis] Indexing failed: {index_result.get('error')}")
            # Fallback: use full content if RAG fails
            return self._analyze_fallback(content)

        print(f"[PDF Analysis] Indexed {index_result['chunks_count']} chunks")

        # Step 2: Retrieve relevant chunks for analysis
        query = "learning objectives key concepts main topic educational goals"
        analysis_context = self.rag.get_context(query, top_k=5)

        # Step 3: Create enhanced prompt with RAG-retrieved context
        prompt = f"""
You are an expert educational content analyst. Analyze the lesson and extract key information.

RETRIEVED LESSON CONTENT (most relevant sections):
{analysis_context}

Based on the content above, extract and return:

1. **Topic**: The main topic or subject area
2. **Keywords**: 5-10 most important keywords/concepts
3. **Learning Objectives**: What students should learn (2-4 objectives)

Provide structured output. Be concise but comprehensive.
"""

        answer = ask_llm(prompt)
        print("[PDF Analysis] Analysis complete")

        return answer

    def _analyze_fallback(self, content):
        """Fallback analysis if RAG fails (uses full content)."""
        prompt = f"""
Analyze the lesson.

Extract:
- Topic
- Keywords
- Learning Objectives

Lesson:
{content}
"""
        return ask_llm(prompt)

    def analyze_with_focus_topic(self, content, focus_topic):
        """
        Analyze content with focus on a specific topic.

        Args:
            content (str): Raw content
            focus_topic (str): Topic to focus on (e.g., "photosynthesis")

        Returns:
            str: Focused analysis
        """
        print(f"[PDF Analysis] Analyzing with focus: {focus_topic}")

        # Index content
        self.rag.index(content, metadata={"focus_topic": focus_topic})

        # Retrieve chunks specifically about focus topic
        relevant_chunks = self.rag.retrieve(focus_topic, top_k=5)

        if not relevant_chunks:
            print(f"[PDF Analysis] No content found for topic: {focus_topic}")
            return f"Could not find content related to: {focus_topic}"

        context = "\n\n".join([f"[Section {i+1}]\n{chunk}" 
                               for i, chunk in enumerate(relevant_chunks)])

        prompt = f"""
Analyze this lesson content focused on: {focus_topic}

RETRIEVED CONTENT:
{context}

Provide:
1. Definition/Explanation of {focus_topic}
2. Key concepts related to {focus_topic}
3. Important facts and relationships
4. Suggested learning objectives for {focus_topic}
"""

        return ask_llm(prompt)
