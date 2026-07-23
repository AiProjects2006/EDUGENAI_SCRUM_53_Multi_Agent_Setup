class AnalysisResult:

    def __init__(self, topic, keywords, learning_objectives):
        self.topic = topic
        self.keywords = keywords
        self.learning_objectives = learning_objectives

        def __str__(self):
            keywords = "\n".join(f"- {k}" for k in self.keywords)

            objectives = "\n".join(
                f"{i + 1}. {obj}"
                for i, obj in enumerate(self.learning_objectives)
            )

            return (
                f"Topic: {self.topic}\n\n"
                f"Keywords:\n{keywords}\n\n"
                f"Learning Objectives:\n{objectives}"
            )