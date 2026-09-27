"""
RAG Integration Guide for EDUGENAI AI Service

This document explains how to integrate RAG into your existing agents and workflow.
"""

# ============================================================================
# INTEGRATION GUIDE: RAG INTO EDUGENAI MULTI-AGENT SYSTEM
# ============================================================================

"""
STEP 1: Update requirements.txt
================================
Add these dependencies to your requirements.txt:

chromadb>=0.3.21                          # Vector database
google-generativeai>=0.3.0                # For Gemini embeddings (already used)
# OR for OpenAI embeddings:
# openai>=1.0.0
# OR for local offline embeddings:
# sentence-transformers>=2.2.0

Then run: pip install -r requirements.txt
"""


# STEP 2: Modify content_analysis_agent/strategies/pdf_strategy.py
# ================================================================

"""
OLD CODE (without RAG):

from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class PDFAnalysisStrategy(ContentAnalysisStrategy):
    def analyze(self, content):
        prompt = f"Analyze the lesson...{content}"  # ← Full content in prompt
        answer = ask_llm(prompt)
        return answer
"""

# NEW CODE (with RAG):
"""
from content_analysis_agent.strategies.analysis_strategy import ContentAnalysisStrategy
from content_analysis_agent.gemini_client import ask_llm
from rag_service.rag_agent import RAGAgent

class PDFAnalysisStrategy(ContentAnalysisStrategy):
    def __init__(self):
        self.rag = RAGAgent(embedder_type="gemini")  # Use your existing Gemini key

    def analyze(self, content):
        # Index content for retrieval
        self.rag.index(content)
        
        # Retrieve only relevant chunks
        context = self.rag.get_context("learning objectives key concepts", top_k=5)
        
        # Use retrieved context instead of full content
        prompt = f"Analyze the lesson...{context}"  # ← Only relevant chunks
        answer = ask_llm(prompt)
        return answer
"""


# STEP 3: Modify workflow_manager.py
# ====================================

"""
Add RAG initialization:

from rag_service.rag_agent import RAGAgent

class WorkflowManager:
    def __init__(self):
        self.rag = RAGAgent(embedder_type="gemini")
        self.content_agent = ContentAnalysisAgent(
            PDFAnalysisStrategy()  # Will use RAG internally
        )
        # ... rest of initialization

    def run(self, lesson, activity_type, number_of_questions):
        # RAG now handles content retrieval internally
        analysis = self.content_agent.analyze(lesson)
        # ... rest of workflow
"""


# STEP 4: Use RAG in Question Generation Strategies
# ==================================================

"""
You can also use RAG in question generation for targeted retrieval:

Example for MCQStrategy with RAG:

from rag_service.rag_agent import RAGAgent

class MCQStrategy(QuestionStrategy):
    def __init__(self):
        self.rag = RAGAgent(embedder_type="gemini")

    def generate(self, analysis, number_of_questions):
        # Retrieve chunks most relevant for MCQ generation
        context = self.rag.get_context(
            "multiple choice question concepts facts",
            top_k=5
        )
        
        prompt = f"Generate {number_of_questions} MCQs from: {context}"
        response = ask_llm(prompt)
        return json.loads(response)
"""


# EXAMPLE USAGE PATTERNS
# ======================

from rag_service.rag_agent import RAGAgent
import json

# Pattern 1: Simple indexing and retrieval
def pattern_simple_retrieval():
    rag = RAGAgent(embedder_type="gemini")
    
    lesson_content = """
    Photosynthesis is the process by which plants convert light energy into chemical energy...
    The main reactants are carbon dioxide and water...
    Chlorophyll is the primary pigment...
    """
    
    # Index
    rag.index(lesson_content, metadata={"topic": "Biology", "subject": "Photosynthesis"})
    
    # Retrieve
    context = rag.get_context("How does photosynthesis work?", top_k=3)
    print(context)


# Pattern 2: Multiple topic retrieval
def pattern_topic_focused_retrieval():
    rag = RAGAgent(embedder_type="gemini")
    
    lesson_content = "..."  # Your lesson
    rag.index(lesson_content)
    
    # Get chunks about light reactions
    light_chunks = rag.retrieve("light reactions photosystem energy", top_k=3)
    
    # Get chunks about dark reactions (Calvin cycle)
    dark_chunks = rag.retrieve("dark reactions Calvin cycle carbon fixation", top_k=3)
    
    # Combine for specific question generation
    for chunk in light_chunks:
        print(f"Light reaction info: {chunk}\n")


# Pattern 3: Retrieve with metadata filtering
def pattern_with_metadata():
    rag = RAGAgent(embedder_type="gemini")
    
    # Index with rich metadata
    rag.index(
        content="...",
        metadata={
            "course": "Biology 101",
            "unit": "Cellular Processes",
            "difficulty": "intermediate",
            "language": "English"
        }
    )
    
    # Later, retrieve and use metadata
    results = rag.retrieve_with_metadata("photosynthesis", top_k=5)
    for result in results:
        print(f"Text: {result['text'][:100]}...")
        print(f"Score: {result['distance']}")
        print(f"Metadata: {result['metadata']}\n")


# ADVANTAGES OF RAG INTEGRATION
# ==============================

"""
1. ✅ LOWER TOKEN USAGE
   - Don't pass entire textbook to LLM every time
   - Only relevant 300-500 word chunks are sent
   - Example: 10,000 word textbook → 3 chunks (~1,500 words)
   - Saves 85% of tokens for each query

2. ✅ FASTER RESPONSE TIME
   - Smaller prompts = faster LLM processing
   - ChromaDB retrieval is milliseconds
   - Total time often faster despite retrieval step

3. ✅ BETTER ACCURACY
   - LLM focuses on relevant content
   - Less distraction from unrelated material
   - Handles "lost in the middle" problem

4. ✅ SCALABILITY
   - Handle textbooks, entire courses, multi-chapter materials
   - Vector DB persists = reuse for multiple queries
   - No need to reprocess content each time

5. ✅ TARGETED QUESTION GENERATION
   - Generate questions about specific topics
   - "Generate MCQs only about photosynthesis"
   - vs. "Generate MCQs from entire biology chapter"

6. ✅ PERSONALIZATION
   - Track which chunks are queried most
   - Recommend weak areas for students
   - Difficulty-based chunk selection
"""


# CONFIGURATION TIPS
# ==================

"""
A. Chunk Size (default: 500 characters)
   - Too small (100 chars): Creates noise, retrieves too many chunks
   - Too large (2000 chars): Loses precision, includes irrelevant material
   - Sweet spot: 300-500 words (400-800 chars)

B. Overlap (default: 100 characters)
   - Ensures context continuity at chunk boundaries
   - Prevents losing information between chunks
   - Set to 10-20% of chunk_size

C. Top-K Results (default: 5)
   - For analysis: top_k=5 (comprehensive)
   - For question generation: top_k=3-5 (balanced)
   - For fast queries: top_k=3 (speed)

D. Embedder Choice
   - Gemini: ✅ Already integrated, good quality
   - OpenAI: ✅ Best quality, costs money
   - Local: ✅ Offline, free, but slower and lower quality
"""


# MONITORING & OPTIMIZATION
# ==========================

"""
# Check RAG statistics
stats = rag.stats()
print(f"Indexed chunks: {stats['chunk_count']}")

# Monitor retrieval quality
results = rag.retrieve_with_metadata(query, top_k=5)
for result in results:
    print(f"Relevance score: {result['distance']}")  # Lower is better (0-1)

# Performance tips:
# - If retrieval is slow: use local embedder, reduce chunk_count
# - If results aren't relevant: adjust chunk_size, check embedder quality
# - If token usage is still high: reduce top_k, increase chunk_size
"""

# END OF INTEGRATION GUIDE
