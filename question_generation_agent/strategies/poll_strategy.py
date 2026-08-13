import json

from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm


class PollStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):
        prompt = f"""
        Generate {number_of_questions} poll questions using this content:

        {analysis}

        Each poll must:
        - Have one correct answer
        - Have 4 options
        - Be suitable for educational assessment

        Return ONLY valid JSON.

        Format:

        [
          {{
            "question": "Which gas is released during photosynthesis?",
            "options": [
              "Carbon dioxide",
              "Oxygen",
              "Nitrogen",
              "Hydrogen"
            ],
            "correctAnswer": "Oxygen",
            "graded": true
          }}
        ]
        """

        response = ask_llm(prompt)
        return json.loads(response)