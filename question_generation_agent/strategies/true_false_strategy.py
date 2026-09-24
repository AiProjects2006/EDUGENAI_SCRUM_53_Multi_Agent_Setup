from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json


class TrueFalseStrategy(QuestionStrategy):

    def generate(self, analysis, activity_type, number_of_questions):

        prompt = f"""
Generate {number_of_questions} {activity_type} question(s).

Use this analyzed content:

{analysis}

Rules:
- Each question must be a clear factual statement.
- Each answer must be either "True" or "False".
- Include exactly two options: "True" and "False".
- Questions must be based only on the analyzed content.
- Return ONLY valid JSON.

Format:

[
{{
    "question": "Plants use sunlight to produce food during photosynthesis.",
    "options": [
        "True",
        "False"
    ],
    "answer": "True"
}}
]
"""

        response = ask_llm(prompt)

        return json.loads(response)

