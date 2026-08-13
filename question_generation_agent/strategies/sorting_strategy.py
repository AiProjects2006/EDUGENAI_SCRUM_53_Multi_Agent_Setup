import json

from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm


class SortingStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):

        prompt = f"""
Generate {number_of_questions} educational sorting activities
from the following content:

{analysis}

There are TWO allowed sorting types:

1. sequence
   Students arrange items in the correct order.

2. category
   Students place items into the correct categories.

Return ONLY valid JSON.

For sequence sorting use:

[
  {{
    "question": "Arrange the stages in the correct order.",
    "sortMode": "sequence",
    "items": [
      "Step C",
      "Step A",
      "Step B"
    ],
    "correctOrder": [
      "Step A",
      "Step B",
      "Step C"
    ],
    "correctGroups": null
  }}
]

For category sorting use:

[
  {{
    "question": "Sort the following into the correct categories.",
    "sortMode": "category",
    "items": [
      "Carbon Dioxide",
      "Oxygen",
      "Glucose",
      "Water"
    ],
    "correctOrder": null,
    "correctGroups": {{
      "Raw Materials": [
        "Carbon Dioxide",
        "Water"
      ],
      "Products": [
        "Glucose",
        "Oxygen"
      ]
    }}
  }}
]

Return only JSON.
Do not include markdown.
Do not include ```json.
Do not include explanations.
"""

        response = ask_llm(prompt)
        return json.loads(response)