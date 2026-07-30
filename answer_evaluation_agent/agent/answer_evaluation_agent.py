class AnswerEvaluationAgent:

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def evaluate(self, student_answer, correct_answer):
        return self.strategy.evaluate(
            student_answer,
            correct_answer
        )