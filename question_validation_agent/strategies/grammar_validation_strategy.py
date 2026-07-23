from strategies.validation_strategy import ValidationStrategy
from models.validation_result import ValidationResult
from llm_client import ask_llm

class GrammarValidationStrategy(ValidationStrategy):

    def validate(self, questions):

        prompt = f"""
You are an English teacher.

Check the following questions.

1. Correct grammar.
2. Correct spelling.
3. Keep the meaning unchanged.
4. Return the complete validated question, options, and answer.

Questions:

{questions}
"""

        answer = ask_llm(prompt)

        return ValidationResult(
            True,
            answer
        )
