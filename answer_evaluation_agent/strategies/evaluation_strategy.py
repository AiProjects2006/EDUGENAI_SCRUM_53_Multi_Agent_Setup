from abc import ABC, abstractmethod

class EvaluationStrategy(ABC):

    @abstractmethod
    def evaluate(self, student_answer, correct_answer):
        pass