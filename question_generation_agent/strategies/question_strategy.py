from abc import ABC, abstractmethod

class QuestionStrategy(ABC):

    @abstractmethod
    def generate(self, content):
        pass