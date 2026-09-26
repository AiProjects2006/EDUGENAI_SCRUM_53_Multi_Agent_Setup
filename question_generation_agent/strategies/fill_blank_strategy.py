from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class FillBlankStrategy(QuestionStrategy):

    def generate(self, analysis, activity_type, number_of_questions):
        prompt = f"""
You are an expert instructional designer creating Fill in the Blank questions.

Generate exactly {number_of_questions} {activity_type} Fill in the Blank question(s) based ONLY on the analyzed lesson below.

ANALYZED LESSON:
{analysis}

Rules:
- Each question must be a complete sentence taken or adapted directly from the analyzed lesson.
- Replace exactly one key term, concept, or fact per sentence with a blank written as "______".
- The blanked term must be a single word or short phrase (no more than 3 words) that is essential to the sentence's meaning.
- Do not blank out trivial words (e.g., articles, prepositions, conjunctions).
- Provide the exact correct answer for the blank in the "answer" field.
- Do not repeat the same blanked term across multiple questions; cover different concepts.
- Do not include markdown, explanations, or text outside the JSON array.
- Return ONLY valid JSON, parseable by a standard JSON parser.

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

