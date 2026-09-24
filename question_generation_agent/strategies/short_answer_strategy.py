from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class ShortAnswerStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):

        prompt = f"""
Generate {number_of_questions} short-answer educational questions
from the following lesson content.

CONTENT:
{analysis}

Students should answer using a few words or one short sentence.

Return ONLY valid JSON.

Format:

[
  {{
    "question": "What is the main function of chlorophyll?",
    "expectedAnswer": "Chlorophyll absorbs light energy for photosynthesis.",
    "keywords": [
      "chlorophyll",
      "absorbs",
      "light energy"
    ]
  }}
]

Rules:
- Questions must come from the provided content.
- Keep answers short.
- Include important keywords that can help evaluate the student's answer.
- Do not include markdown.
- Do not include explanations outside the JSON.
"""

        response = ask_llm(prompt)

        return json.loads(response)