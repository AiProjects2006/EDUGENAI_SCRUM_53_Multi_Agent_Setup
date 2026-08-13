from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class FillBlankStrategy(QuestionStrategy):

    def generate(self, analysis, activity_type, number_of_questions):
        prompt = f"""
Generate {number_of_questions} {activity_type} Fill in the Blank questions.

Use the following analyzed lesson:

{analysis}

Rules:
- Replace one important word with ______.
- Provide the correct answer after each question.
- Return ONLY valid JSON.

Example:
[
  {{
    "question": "Photosynthesis occurs in ______.",
    "answer": "chlorophyll"
  }}
]
"""

        response = ask_llm(prompt)
        return json.loads(response)

