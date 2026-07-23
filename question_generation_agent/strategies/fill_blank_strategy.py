from strategies.question_strategy import QuestionStrategy
from openai_client import ask_llm

class FillBlankStrategy(QuestionStrategy):

    def generate(self, content):

        prompt = f"""
Generate ONE Fill in the Blank from:

{content}
"""

        return ask_llm(prompt)