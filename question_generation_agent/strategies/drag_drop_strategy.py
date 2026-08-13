import json

from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm


class DragDropStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):

        prompt = f"""
Generate {number_of_questions} drag-and-drop educational activities
using the following lesson content:

{analysis}

Return ONLY valid JSON.

Use exactly this structure:

[
  {{
    "question": "Drag each item to the correct category.",
    "items": [
      {{"id": "1", "text": "Carbon dioxide"}},
      {{"id": "2", "text": "Oxygen"}}
    ],
    "targets": [
      {{"id": "input", "text": "Input"}},
      {{"id": "product", "text": "Product"}}
    ],
    "answers": {{
      "1": "input",
      "2": "product"
    }}
  }}
]

Do not include markdown.
Do not include ```json.
Do not include explanations.
"""

        response = ask_llm(prompt)

        return json.loads(response)