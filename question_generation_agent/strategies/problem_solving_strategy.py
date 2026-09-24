from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class ProblemSolvingStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):

        prompt = f"""
Generate {number_of_questions} problem-solving exercises
from the following educational content.

CONTENT:
{analysis}

The problem should require the learner to apply concepts,
formulas, calculations, reasoning, or logical thinking.

Return ONLY valid JSON.

Format:

[
  {{
    "question": "A plant receives 8 hours of sunlight per day. Explain how reducing the light exposure could affect photosynthesis.",
    "expectedAnswer": "Reducing light exposure can decrease the rate of photosynthesis because less light energy is available.",
    "solutionSteps": [
      "Identify light as a requirement for photosynthesis.",
      "Determine what happens when less light energy is available.",
      "Conclude that the photosynthesis rate may decrease."
    ],
    "keywords": [
      "light energy",
      "photosynthesis",
      "decrease"
    ]
  }}
]

Rules:
- Generate problems based only on the provided educational content.
- Require reasoning, not simple recall.
- Provide a correct solution.
- Include logical solution steps.
- Do not include markdown.
"""

        response = ask_llm(prompt)

        return json.loads(response)