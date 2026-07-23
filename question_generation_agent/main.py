from agent.question_generation_agent import QuestionGenerationAgent
from strategies.mcq_strategy import MCQStrategy
from strategies.fill_blank_strategy import FillBlankStrategy

content = """
Photosynthesis is the process by which plants make food.
"""

agent = QuestionGenerationAgent(MCQStrategy())

print(agent.generate(content))

agent.set_strategy(FillBlankStrategy())

print(agent.generate(content))