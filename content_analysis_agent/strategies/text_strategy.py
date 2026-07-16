from strategies.analysis_strategy import ContentAnalysisStrategy
from openai_client import ask_llm

class TextAnalysisStrategy(ContentAnalysisStrategy):

    def analyze(self, content):

        prompt = f"""
Analyze the following lesson.

Find:

- Topic
- Keywords

{content}
"""

        answer = ask_llm(prompt)

        print(answer)

        return answer