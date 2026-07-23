class QuestionValidationAgent:

    def __init__(self, strategy):

        self.strategy = strategy

    def set_strategy(self, strategy):

        self.strategy = strategy

    def validate(self, questions):

        return self.strategy.validate(questions)