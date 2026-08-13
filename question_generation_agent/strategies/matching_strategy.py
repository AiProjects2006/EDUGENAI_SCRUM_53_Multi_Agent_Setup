import json

from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm


class MatchingStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):

        prompt = f"""
Generate {number_of_questions} Match the Following activities
using the educational content below.

Content:
{analysis}

Return ONLY valid JSON.

Use exactly this format:

[
  {{
    "question": "Match the following terms with their meanings.",
    "leftItems": [
      {{
        "id": "1",
        "text": "Photosynthesis"
      }},
      {{
        "id": "2",
        "text": "Chlorophyll"
      }}
    ],
    "rightItems": [
      {{
        "id": "A",
        "text": "Process plants use to make food"
      }},
      {{
        "id": "B",
        "text": "Green pigment"
      }}
    ],
    "answers": {{
      "1": "A",
      "2": "B"
    }}
  }}
]

Do not return markdown.
Do not return ```json.
Do not return explanations.
"""

        response = ask_llm(prompt)
        return json.loads(response)