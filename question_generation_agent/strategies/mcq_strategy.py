from strategies.question_strategy import QuestionStrategy
from openai_client import ask_llm

class MCQStrategy(QuestionStrategy):

    def generate(self, content):

        prompt = f"""
Generate ONE Multiple Choice Question from:

{content}

Use this exact format:
Question: <question>
Options:
A. <option>
B. <option>
C. <option>
D. <option>
Answer: <correct option letter and text>
"""

        return ask_llm(prompt)
