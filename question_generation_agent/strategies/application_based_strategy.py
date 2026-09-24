from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class ApplicationBasedStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):

        prompt = f"""
Generate {number_of_questions} application-based educational questions
using the following lesson content.

CONTENT:
{analysis}

Each question must present a realistic situation where the student
must apply learned knowledge.

Return ONLY valid JSON.

Format:

[
  {{
    "scenario": "A student keeps one plant near a sunny window and another plant in a dark cupboard for several days.",
    "question": "Which plant is likely to produce more glucose and why?",
    "expectedAnswer": "The plant near the sunny window will produce more glucose because it receives more light energy for photosynthesis.",
    "keywords": [
      "sunlight",
      "light energy",
      "photosynthesis",
      "glucose"
    ]
  }}
]

Rules:
- Use practical or real-life situations.
- Do not ask simple recall questions.
- The student must apply knowledge from the provided content.
- Include the expected answer.
- Do not include markdown.
"""

        response = ask_llm(prompt)

        return json.loads(response)