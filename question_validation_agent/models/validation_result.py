class ValidationResult:

    def __init__(self, valid, feedback):

        self.valid = valid
        self.feedback = feedback

    def __str__(self):
        return f"""
    Status: {"VALID" if self.valid else "INVALID"}

    Feedback:
    {self.feedback}
    """