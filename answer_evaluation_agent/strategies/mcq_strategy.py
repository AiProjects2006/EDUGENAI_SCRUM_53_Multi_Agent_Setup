from strategies.evaluation_strategy import EvaluationStrategy
from models.evaluation_result import EvaluationResult

class MCQStrategy(EvaluationStrategy):

    def evaluate(self, student_answer, correct_answer):

        if student_answer.strip().lower() == correct_answer.strip().lower():

            return EvaluationResult(
                score=1,
                feedback="Correct Answer!"
            )

        return EvaluationResult(
            score=0,
            feedback=f"Wrong Answer. Correct Answer is '{correct_answer}'."
        )