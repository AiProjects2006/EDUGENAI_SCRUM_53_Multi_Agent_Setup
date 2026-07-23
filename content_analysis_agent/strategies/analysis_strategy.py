from abc import ABC, abstractmethod

class ContentAnalysisStrategy(ABC):

    @abstractmethod
    def analyze(self, content):
        pass