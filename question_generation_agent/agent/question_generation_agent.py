class QuestionGenerationAgent:

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def generate(self, content):
        return self.strategy.generate(content)