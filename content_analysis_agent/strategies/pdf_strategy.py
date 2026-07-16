from strategies.analysis_strategy import ContentAnalysisStrategy
from openai_client import ask_llm
from models.analysis_result import AnalysisResult


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