from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class MCQStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):
        prompt = f"""
You are an expert instructional designer creating multiple-choice questions (MCQs).

Generate exactly {number_of_questions} MCQ question(s) based ONLY on the analyzed content below.

ANALYZED CONTENT:
{analysis}

Rules:
- Each question must be answerable strictly from the analyzed content, not outside knowledge.
- Provide exactly 4 options per question.
- Exactly one option must be correct; the other 3 must be plausible but clearly incorrect distractors.
- Distractors must be relevant to the topic (no random or obviously silly options).
- Do not reuse the same question or answer across items; vary topics/subtopics covered.
- Vary difficulty across the set (mix of recall and conceptual understanding) when enough content is available.
- "answer" must exactly match one of the strings in "options".
- Do not include markdown, explanations, or text outside the JSON array.
- Return ONLY valid JSON, parseable by a standard JSON parser.

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