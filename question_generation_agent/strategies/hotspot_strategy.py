from question_generation_agent.strategies.question_strategy import QuestionStrategy
from question_generation_agent.openai_client import ask_llm
import json

class HotspotStrategy(QuestionStrategy):

    def generate(self, analysis, number_of_questions):

        prompt = f"""
Generate {number_of_questions} hotspot educational activities
from the following educational content.

CONTENT:
{analysis}

A hotspot activity contains:
- a question
- an image description
- the part of the image that should be selected

Return ONLY valid JSON.

Format:

[
  {{
    "question": "Click on the part of the plant where most photosynthesis occurs.",
    "imageDescription": "A labelled diagram of a flowering plant showing roots, stem, leaves and flower.",
    "correctRegion": "leaf",
    "feedback": "Photosynthesis mainly occurs in the leaves because they contain chlorophyll."
  }}
]

Rules:
- The hotspot must be visually identifiable.
- Do not invent pixel coordinates.
- Return an image description that can later be associated with a real image.
- Do not include markdown.
"""

        response = ask_llm(prompt)

        return json.loads(response)