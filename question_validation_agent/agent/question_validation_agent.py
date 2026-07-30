from question_validation_agent.models.validation_result import ValidationResult


class QuestionValidationAgent:

    def __init__(self, strategy):

        self.strategy = strategy

    def set_strategy(self, strategy):

        self.strategy = strategy

    def validate(self, questions):

        result = self.strategy.validate(questions)

        if result:
            return questions
        else:
            raise ValueError("Questions are invalid")