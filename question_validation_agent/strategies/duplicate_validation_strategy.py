from strategies.validation_strategy import ValidationStrategy
from models.validation_result import ValidationResult

class DuplicateValidationStrategy(ValidationStrategy):

    def validate(self, questions):

        unique_questions = []

        duplicates = []

        for q in questions:

            if q not in unique_questions:
                unique_questions.append(q)
            else:
                duplicates.append(q)

        if len(duplicates) == 0:

            return ValidationResult(
                True,
                "No duplicate questions found."
            )

        return ValidationResult(
            False,
            f"Duplicate Questions Found:\n{duplicates}"
        )