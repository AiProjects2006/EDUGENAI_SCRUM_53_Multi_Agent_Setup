from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json


class TrueFalseStrategy(QuestionStrategy):

    def generate(self, analysis, activity_type, number_of_questions):

        prompt = f"""
You are an expert instructional designer creating True/False questions.

Generate exactly {number_of_questions} {activity_type} question(s) based ONLY on the analyzed content below.

ANALYZED CONTENT:
{analysis}

Rules:
- Each question must be a single, clear, unambiguous factual statement (no compound or double-barreled statements).
- Each answer must be exactly "True" or "False".
- Include exactly two options: "True" and "False", in that order.
- Questions must be based only on the analyzed content, not outside knowledge.
- Aim for a roughly balanced mix of True and False statements across the set.
- False statements must contain a plausible but clearly incorrect modification of a fact from the content (not an unrelated or absurd claim).
- Do not repeat the same fact or topic across multiple questions.
- Do not include markdown, explanations, or text outside the JSON array.
- Return ONLY valid JSON, parseable by a standard JSON parser.

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

