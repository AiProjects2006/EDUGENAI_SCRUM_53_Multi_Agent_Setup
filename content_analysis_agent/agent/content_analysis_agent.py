class ContentAnalysisAgent:

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def analyze(self, content):
        return self.strategy.analyze(content)