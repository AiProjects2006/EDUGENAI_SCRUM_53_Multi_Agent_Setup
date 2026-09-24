from content_analysis_agent.strategies.analysis_strategy import ContentAnalysisStrategy
from content_analysis_agent.gemini_client import ask_llm


class PDFAnalysisStrategy(ContentAnalysisStrategy):

    def analyze(self, content):

        prompt = f"""
Analyze the lesson.

Extract:

- Topic
- Keywords
- Learning Objectives

Lesson:

{content}
"""

        answer = ask_llm(prompt)



        return answer