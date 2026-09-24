class EvaluationResult:

    def __init__(self, score, feedback):
        self.score = score
        self.feedback = feedback

    def __str__(self):
        return f"""
    Score: {self.score}

    Feedback:
    {self.feedback}
    """