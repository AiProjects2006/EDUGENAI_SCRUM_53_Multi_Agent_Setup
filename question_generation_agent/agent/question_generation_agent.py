class QuestionGenerationAgent:

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def generate(self, analysis, number_of_questions):
        return self.strategy.generate(
            analysis,
            number_of_questions
        )