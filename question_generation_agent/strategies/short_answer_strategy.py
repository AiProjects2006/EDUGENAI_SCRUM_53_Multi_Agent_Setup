from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class ShortAnswerStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):

        prompt = f"""
You are an expert instructional designer creating short-answer educational questions.

Generate exactly {number_of_questions} short-answer question(s) based ONLY on the following lesson content.

CONTENT:
{analysis}

Rules:
- Questions must be answerable strictly from the provided content, not outside knowledge.
- Students should be able to answer using a few words or one short sentence.
- Avoid yes/no questions; prefer "what", "why", "how", or "explain" style questions.
- Do not repeat the same question or topic across items; cover different concepts from the content.
- "expectedAnswer" must be a concise, correct, self-contained sentence or phrase.
- "keywords" must list the 2-5 most important terms from the expected answer that a grader can use to evaluate a student's response.
- Do not include markdown.
- Do not include explanations outside the JSON.
- Return ONLY valid JSON, parseable by a standard JSON parser.

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
"""

        response = ask_llm(prompt)

        return json.loads(response)