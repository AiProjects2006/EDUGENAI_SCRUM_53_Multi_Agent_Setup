from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class MCQStrategy(QuestionStrategy):

    def generate(self, analysis, activity_type, number_of_questions):
        prompt = f"""
    Generate {number_of_questions} {activity_type} question(s).

    Use this analyzed content:

    {analysis}

Return ONLY valid JSON.

Format:

[
    {{
        "question": "What are the raw materials required for photosynthesis?",
        "options": [
            "Glucose and oxygen",
            "Carbon dioxide and water",
            "Oxygen and water",
            "Sunlight and glucose"
        ],
        "answer": "Carbon dioxide and water"
    }}
]
"""
        response = ask_llm(prompt)
        return json.loads(response)